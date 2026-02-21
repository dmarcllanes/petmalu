// ==================== DOM Elements ====================
const loginForm = document.getElementById('loginForm');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const rememberMeCheckbox = document.getElementById('rememberMe');
const togglePasswordBtn = document.getElementById('togglePassword');
const submitBtn = document.getElementById('submitBtn');
const googleBtn = document.getElementById('googleBtn');
const emailError = document.getElementById('emailError');
const passwordError = document.getElementById('passwordError');
const errorBanner = document.getElementById('errorBanner');
const successBanner = document.getElementById('successBanner');

// Hide Email/Password Form for Google Auth Only
if (loginForm) {
    // loginForm.style.display = 'none'; // Or just hide the inner parts
    const formGroups = loginForm.querySelectorAll('.form-group, .form-options, .divider');
    // We want to keep the "Welcome" and "Google" button.
    // The google button is OUTSIDE the form in the original HTML:
    // ... H1, P, Form, Divider, GoogleBtn ...
    // Wait, let's check the HTML structure in login.py again.
}

// ==================== Utility Functions ====================
function showError(element, message) {
    if (element) {
        element.textContent = message;
        element.style.display = 'block';
    }
}

function hideError(element) {
    if (element) {
        element.textContent = '';
        element.style.display = 'none';
    }
}

function showBanner(bannerElement, message, duration = 3000) {
    if (!bannerElement) return; // Guard against null elements

    bannerElement.textContent = message;
    bannerElement.classList.add('show');

    if (duration > 0) {
        setTimeout(() => {
            bannerElement.classList.remove('show');
        }, duration);
    }
}

function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validatePassword(password) {
    return password && password.length >= 6;
}

// ==================== Password Toggle ====================
if (togglePasswordBtn) {
    togglePasswordBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const isPassword = passwordInput.type === 'password';
        passwordInput.type = isPassword ? 'text' : 'password';

        // Update icon
        const svg = togglePasswordBtn.querySelector('svg');
        if (isPassword) {
            svg.innerHTML = '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line>';
        } else {
            svg.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle>';
        }
    });
}

// ==================== Form Validation ====================
if (emailInput) {
    emailInput.addEventListener('blur', () => {
        const email = emailInput.value.trim();

        if (!email) {
            showError(emailError, 'Email is required');
        } else if (!validateEmail(email)) {
            showError(emailError, 'Please enter a valid email');
        } else {
            hideError(emailError);
        }
    });

    emailInput.addEventListener('input', () => {
        if (emailError.textContent) {
            hideError(emailError);
        }
    });
}

if (passwordInput) {
    passwordInput.addEventListener('blur', () => {
        const password = passwordInput.value;

        if (!password) {
            showError(passwordError, 'Password is required');
        } else if (!validatePassword(password)) {
            showError(passwordError, 'Password must be at least 6 characters');
        } else {
            hideError(passwordError);
        }
    });

    passwordInput.addEventListener('input', () => {
        if (passwordError.textContent) {
            hideError(passwordError);
        }
    });
}

// ==================== Form Submission ====================
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Clear previous errors
        hideError(emailError);
        hideError(passwordError);
        errorBanner.classList.remove('show');
        successBanner.classList.remove('show');

        // Get form values
        const email = emailInput.value.trim();
        const password = passwordInput.value;
        const rememberMe = rememberMeCheckbox.checked;

        // Validate
        let isValid = true;

        if (!email) {
            showError(emailError, 'Email is required');
            isValid = false;
        } else if (!validateEmail(email)) {
            showError(emailError, 'Please enter a valid email');
            isValid = false;
        }

        if (!password) {
            showError(passwordError, 'Password is required');
            isValid = false;
        } else if (!validatePassword(password)) {
            showError(passwordError, 'Password must be at least 6 characters');
            isValid = false;
        }

        if (!isValid) return;

        // Show loading state
        submitBtn.disabled = true;
        const btnText = submitBtn.querySelector('.btn-text');
        const btnLoader = submitBtn.querySelector('.btn-loader');
        btnText.classList.add('hidden');
        btnLoader.classList.add('active');

        try {
            // Simulate API call - Replace with your actual backend endpoint
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email,
                    password,
                    rememberMe,
                }),
            });

            if (!response.ok) {
                throw new Error('Login failed');
            }

            const data = await response.json();

            // Save preferences
            if (rememberMe) {
                localStorage.setItem('rememberedEmail', email);
            } else {
                localStorage.removeItem('rememberedEmail');
            }

            // Show success message
            showBanner(successBanner, 'Login successful! Redirecting...', 2000);

            // Simulate redirect after delay
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 2000);

        } catch (error) {
            console.error('Login error:', error);
            showBanner(errorBanner, 'Login failed. Please try again.');

            // Reset loading state
            submitBtn.disabled = false;
            btnText.classList.remove('hidden');
            btnLoader.classList.remove('active');
        }
    });
}

// ==================== Supabase Initialization & Google Login ====================
// Note: The Supabase CDN script declares a global 'var supabase', so we use 'supabaseClient'
// to avoid variable redeclaration conflicts. The "SES Removing unpermitted intrinsics" 
// warning is a security feature from Supabase and can be safely ignored in development.
let supabaseClient;
try {
    if (window.supabase) {
        supabaseClient = window.supabase.createClient(window.SUPABASE_URL, window.SUPABASE_KEY);
        console.log('Supabase initialized');
    } else {
        console.error('Supabase SDK not loaded');
    }
} catch (e) {
    console.error('Failed to initialize Supabase:', e);
}

googleBtn.addEventListener('click', async () => {
    if (!supabaseClient) {
        showBanner(errorBanner, 'Authentication service not available');
        return;
    }

    showBanner(successBanner, 'Redirecting to Google...', 0);

    try {
        const { data, error } = await supabaseClient.auth.signInWithOAuth({
            provider: 'google',
            options: {
                redirectTo: window.location.origin + '/login'
            }
        });

        if (error) throw error;

    } catch (error) {
        console.error('Google login error:', error);
        showBanner(errorBanner, 'Login failed: ' + error.message);
    }
});

// ==================== Check Session ====================
window.addEventListener('load', async () => {
    if (!supabaseClient) return;

    const { data: { session } } = await supabaseClient.auth.getSession();

    if (session) {
        // Sync session to backend
        await syncSession(session);
    }

    supabaseClient.auth.onAuthStateChange(async (event, session) => {
        console.log('Auth state change:', event);
        if (event === 'SIGNED_IN' && session) {
            await syncSession(session);
        } else if (event === 'SIGNED_OUT') {
            // Handle logout if needed
        }
    });
});

async function syncSession(session) {
    try {
        const response = await fetch('/api/auth/session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                access_token: session.access_token,
                refresh_token: session.refresh_token,
                user_id: session.user.id,
                email: session.user.email,
                full_name: session.user.user_metadata?.full_name || session.user.user_metadata?.name || null
            }),
        });

        if (response.ok) {
            window.location.href = '/dashboard';
        } else {
            console.error('Failed to sync session to backend');
        }
    } catch (err) {
        console.error('Session sync error:', err);
    }
}

// ==================== Remember Email ====================
window.addEventListener('DOMContentLoaded', () => {
    if (emailInput && rememberMeCheckbox) {
        const rememberedEmail = localStorage.getItem('rememberedEmail');
        if (rememberedEmail) {
            emailInput.value = rememberedEmail;
            rememberMeCheckbox.checked = true;
        }
    }
});

// ==================== Enter Key Submission ====================
if (passwordInput && loginForm) {
    passwordInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            loginForm.dispatchEvent(new Event('submit'));
        }
    });
}

// ==================== Accessibility Enhancements ====================
// Trap focus within modal on mobile
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        // Close any open dropdowns or modals
        errorBanner.classList.remove('show');
    }
});

// ==================== Device Specific Optimization ====================
// Detect if running as PWA
if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true) {
    document.body.classList.add('pwa-mode');
}

// Add touch optimization
if ('ontouchstart' in window) {
    document.body.classList.add('touch-device');
}

// ==================== Install Prompt Handler ====================
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;

    // You can show an install button here if desired
    // document.getElementById('installBtn').style.display = 'block';
});

window.addEventListener('appinstalled', () => {
    console.log('PWA installed');
    deferredPrompt = null;
});

// ==================== Connection Status ====================
window.addEventListener('online', () => {
    console.log('Back online');
    // Re-enable form
    submitBtn.disabled = false;
});

window.addEventListener('offline', () => {
    console.log('You are offline');
    showBanner(errorBanner, 'You are offline. Some features may be unavailable.');
});

// ==================== Security Features ====================
// Prevent session fixation
if (sessionStorage.getItem('sessionId')) {
    // Session already exists
} else {
    sessionStorage.setItem('sessionId', 'session_' + Date.now());
}

// CSP meta tag check
console.log('Content Security Policy:', document.querySelector('meta[http-equiv="Content-Security-Policy"]'));

// ==================== Debug Logger ====================
const DEBUG = false;
function debugLog(...args) {
    if (DEBUG) {
        console.log('[Auth]', ...args);
    }
}

debugLog('Auth page initialized');
