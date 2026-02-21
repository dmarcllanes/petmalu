from fasthtml.common import *


STEP_LABELS = ["Basic Info", "Health Profile", "Activity & Review"]


def wizard_steps(current_step: int):
    items = []
    for i, label in enumerate(STEP_LABELS, start=1):
        if i < current_step:
            cls = "wizard-step completed"
        elif i == current_step:
            cls = "wizard-step active"
        else:
            cls = "wizard-step"

        items.append(
            Div(
                Span(str(i), cls="wizard-step-circle"),
                Span(label, cls="wizard-step-label"),
                cls=cls,
            )
        )

        if i < len(STEP_LABELS):
            connector_cls = "wizard-connector completed" if i < current_step else "wizard-connector"
            items.append(Div(cls=connector_cls))

    return Div(*items, cls="wizard-steps")
