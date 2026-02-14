from fasthtml.common import *
from fasthtml.svg import *
import os
from dotenv import load_dotenv

load_dotenv()

def login_page():
    return Html(
    Head(
        Meta(charset='UTF-8'),
        Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
        Meta(name='theme-color', content='#2F7A73'),
        Meta(name='description', content='Secure login with Google authentication'),
        Meta(name='apple-mobile-web-app-capable', content='yes'),
        Meta(name='apple-mobile-web-app-status-bar-style', content='black-translucent'),
        Meta(name='apple-mobile-web-app-title', content='Auth'),
        Link(rel='manifest', href='/manifest.json'),
        Link(rel='icon', type='image/svg+xml', href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 180 180'><rect fill='%232F7A73' width='180' height='180'/><text x='50%' y='50%' font-size='80' font-weight='bold' fill='white' text-anchor='middle' dominant-baseline='central'>A</text></svg>"),
        Link(rel='stylesheet', href='/css/login.css'),
        Script(src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"),
        Script(f"""
            window.SUPABASE_URL = '{os.environ.get("SUPABASE_URL", "")}';
            window.SUPABASE_KEY = '{os.environ.get("SUPABASE_KEY", "")}';
        """),
        Title('Login - Auth')
    ),
    Body(
        Div(cls='background-gradient'),
        Div(
            Div(
                A(
                    Svg(
                        Path(d='M19 12H5M12 19l-7-7 7-7'),
                        viewbox='0 0 24 24',
                        fill='none',
                        stroke='currentColor',
                        stroke_width='2',
                        stroke_linecap='round',
                        stroke_linejoin='round',
                        width='20',
                        height='20'
                    ),
                    Span('Back to Home'),
                    href='/',
                    style='display: flex; align-items: center; gap: 8px; color: #666; text-decoration: none; margin-bottom: 20px; font-size: 14px; transition: color 0.2s;',
                    onmouseover="this.style.color='#2F7A73'",
                    onmouseout="this.style.color='#666'"
                ),
                Div(
                    Span("🐾", style="font-size: 60px; display: block; text-align: center;"),
                    H1("LuluPet", style="margin-top: 10px; margin-bottom: 0; color: #2F7A73; text-align: center;"),
                    style="text-align: center; margin-bottom: 30px;"
                ),
                H2('Welcome Back', style="margin-top: 0; margin-bottom: 10px; text-align: center;"),
                P('Sign in with your Google account to continue', cls='subtitle', style="text-align: center;"),
                Button(
                    Svg(
                        Path(fill='#4285F4', d='M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z'),
                        Path(fill='#34A853', d='M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z'),
                        Path(fill='#FBBC05', d='M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z'),
                        Path(fill='#EA4335', d='M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z'),
                        viewbox='0 0 24 24',
                        width='20',
                        height='20'
                    ),
                    Span('Continue with Google'),
                    type='button',
                    id='googleBtn',
                    cls='btn btn-google',
                    style="margin-top: 30px; padding: 15px 30px; font-size: 16px;"
                ),
                Div(id='errorBanner', cls='error-banner', style="margin-top: 20px;"),
                cls='login-card'
            ),
            Footer(
                A('Privacy', href='#'),
                A('Terms', href='#'),
                A('Support', href='#'),
                cls='footer'
            ),
            cls='container'
        ),
        Script(src='/js/login.js')
    ),
    lang='en'
)
    