from fasthtml.common import Nav, A, Div, Span, Input, Label, Ul, Li, Button


def navbar():
    return Nav(
        Div(
            # Logo
            A(
                Span("\U0001f43e", cls="logo-icon"),
                Span("LuluPet", cls="logo-text"),
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
                Li(A("Logout", href="/logout", cls="btn-logout")),
                cls="nav-links",
            ),
            cls="nav-container",
        ),
        cls="navbar",
    )
