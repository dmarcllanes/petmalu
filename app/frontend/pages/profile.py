from fasthtml.common import *
from app.frontend.components.navbar import navbar


def profile_page(user, settings):
    """Profile and settings page"""
    
    return (
        navbar(),
        Div(
            H2("Profile & Settings"),
            
            # Account Details Section
            Div(
                H3("Account Details"),
                Form(
                    Div(
                        Label("Email", _for="email"),
                        Input(
                            name="email",
                            id="email",
                            type="email",
                            value=user.get('email', ''),
                            readonly=True,
                            cls="readonly",
                        ),
                        Span("Email cannot be changed", cls="help-text"),
                        cls="form-group",
                    ),
                    Div(
                        Label("Full Name", _for="full_name"),
                        Input(
                            name="full_name",
                            id="full_name",
                            type="text",
                            value=user.get('full_name', ''),
                            required=True,
                        ),
                        cls="form-group",
                    ),
                    Button("Update Profile", type="submit", cls="btn btn-primary"),
                    method="post",
                    action="/profile/update",
                    cls="profile-form",
                ),
                cls="settings-section",
            ),
            
            # Notification Preferences Section
            Div(
                H3("Notification Preferences"),
                Form(
                    Div(
                        Input(
                            type="checkbox",
                            name="email_notifications",
                            id="email_notifications",
                            checked=settings.email_notifications if settings else True,
                        ),
                        Label("Email Notifications", _for="email_notifications"),
                        P("Receive general updates via email", cls="checkbox-help"),
                        cls="checkbox-group",
                    ),
                    Div(
                        Input(
                            type="checkbox",
                            name="feeding_reminders",
                            id="feeding_reminders",
                            checked=settings.feeding_reminders if settings else True,
                        ),
                        Label("Feeding Reminders", _for="feeding_reminders"),
                        P("Get reminders about your pet's feeding schedule", cls="checkbox-help"),
                        cls="checkbox-group",
                    ),
                    Div(
                        Input(
                            type="checkbox",
                            name="weight_reminders",
                            id="weight_reminders",
                            checked=settings.weight_reminders if settings else True,
                        ),
                        Label("Weight Tracking Reminders", _for="weight_reminders"),
                        P("Reminders to log your pet's weight regularly", cls="checkbox-help"),
                        cls="checkbox-group",
                    ),
                    Button("Save Preferences", type="submit", cls="btn btn-primary"),
                    method="post",
                    action="/profile/settings",
                    cls="settings-form",
                ),
                cls="settings-section",
            ),
            
            # Privacy Settings Section
            Div(
                H3("Privacy Settings"),
                Form(
                    Div(
                        Input(
                            type="checkbox",
                            name="data_sharing",
                            id="data_sharing",
                            checked=settings.data_sharing if settings else False,
                        ),
                        Label("Allow Anonymous Data Sharing", _for="data_sharing"),
                        P("Help us improve MukaPet by sharing anonymized usage data", cls="checkbox-help"),
                        cls="checkbox-group",
                    ),
                    Button("Save Privacy Settings", type="submit", cls="btn btn-primary"),
                    method="post",
                    action="/profile/privacy",
                    cls="settings-form",
                ),
                cls="settings-section",
            ),
            
            cls="container profile-container",
        ),
    )
