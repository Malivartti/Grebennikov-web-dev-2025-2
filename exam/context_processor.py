from typing import TYPE_CHECKING

from exam.adoption.types import AdoptionStatus, adoption_status_label
from exam.animal.types import (
    AnimalStatus,
    animal_status_label,
    sex_label,
)
from exam.auth import check_rights
from exam.user.types import Right
from exam.utils import sanitize_and_render_markdown

if TYPE_CHECKING:
    from exam.app import Application


def setup_context_processor(app: "Application"):
    @app.context_processor
    def utility_processor():
        return {
            "check_rights": check_rights,
            "Right": Right,
            "AnimalStatus": AnimalStatus,
            "sex_label": sex_label,
            "animal_status_label": animal_status_label,
            "AdoptionStatus": AdoptionStatus,
            "adoption_status_label": adoption_status_label,
            "render_markdown": sanitize_and_render_markdown,
        }
