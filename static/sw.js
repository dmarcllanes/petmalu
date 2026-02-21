const CACHE_NAME = 'lulupet-v11';
const STATIC_ASSETS = [
  '/styles.css',
  '/manifest.json',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Skip service worker for auth callback URLs (contain access_token in hash)
  if (event.request.mode === 'navigate' && url.href.includes('access_token=')) {
    return;
  }

  // Cache-first for static assets (css, json, icons)
  if (url.pathname.match(/\.(css|js|json|png|svg|ico|woff2?)$/)) {
    event.respondWith(
      caches.match(event.request).then((cached) => cached || fetch(event.request))
    );
    return;
  }

  // Network-first for HTML pages
  if (event.request.headers.get('accept')?.includes('text/html')) {
    event.respondWith(
      fetch(event.request)
        .then((response) => response)
        .catch(() =>
          caches.match(event.request).then(
            (cached) => cached || new Response('Offline', { status: 503, headers: { 'Content-Type': 'text/html' } })
          )
        )
    );
    return;
  }

  event.respondWith(
    fetch(event.request).catch(() =>
      caches.match(event.request).then(
        (cached) => cached || new Response('Offline', { status: 503 })
      )
    )
  );
});
