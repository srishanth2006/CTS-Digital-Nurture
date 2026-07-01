"""
Signal handlers for the Course Management API.

Currently used for basic logging hooks on Enrollment creation/deletion.
These can be extended for notifications, audit trails, etc.
"""

import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from courses.models import Enrollment

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Enrollment)
def log_enrollment_created(sender, instance, created, **kwargs):
    """Log whenever a new enrollment record is created."""
    if created:
        logger.info(
            "New enrollment created: student=%s course=%s",
            instance.student_id,
            instance.course_id,
        )


@receiver(post_delete, sender=Enrollment)
def log_enrollment_deleted(sender, instance, **kwargs):
    """Log whenever an enrollment record is deleted."""
    logger.info(
        "Enrollment deleted: student=%s course=%s",
        instance.student_id,
        instance.course_id,
    )
