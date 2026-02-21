from fasthtml.common import *
import os
from dotenv import load_dotenv

load_dotenv()


def navbar():
    supabase_url = os.environ.get("SUPABASE_URL", "")
    supabase_key = os.environ.get("SUPABASE_KEY", "")

    return Nav(
        Div(
            # Logo
            A(
                Span("🐾", cls="logo-icon"),
                Span("MukaPet", cls="logo-text"),
                href="/dashboard",
                cls="logo",
            ),
            # Hamburger (CSS-only, mobile)
            Input(type="checkbox", id="nav-toggle", cls="nav-toggle"),
            Label(
                Span(cls="hamburger-bar"),
                _for="nav-toggle",
                cls="nav-toggle-label",
            ),
            # Links + Logout
            Ul(
                Li(A("Dashboard", href="/dashboard")),
                Li(A("Add Pet", href="/pets/new")),
                Li(A("Profile", href="/settings")),
                Li(A("Logout", href="#", cls="btn-logout", id="logoutBtn",
                      onclick="handleLogout(event)")),
                cls="nav-links",
            ),
            cls="nav-container",
        ),
        Script(src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"),
        Script(f"""
            async function handleLogout(e) {{
                e.preventDefault();
                try {{
                    const sb = window.supabase.createClient('{supabase_url}', '{supabase_key}');
                    await sb.auth.signOut();
                }} catch (err) {{
                    console.error('Supabase sign-out error:', err);
                }}
                window.location.href = '/logout';
            }}
        """),
        cls="navbar",
    )
