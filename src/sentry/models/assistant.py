from django.conf import settings
from django.db import models

from sentry.db.models import (
    BoundedPositiveIntegerField,
    FlexibleForeignKey,
    Model,
    control_silo_only_model,
    sane_repr,
)


@control_silo_only_model
class AssistantActivity(Model):
    """Records user interactions with the assistant guides."""

    __include_in_export__ = False

    user = FlexibleForeignKey(settings.AUTH_USER_MODEL, null=False)
    guide_id = BoundedPositiveIntegerField()
    # Time the user completed the guide. If this is set, dismissed_ts will be null.
    viewed_ts = models.DateTimeField(null=True)
    # Time the user dismissed the guide. If this is set, viewed_ts will be null.
    dismissed_ts = models.DateTimeField(null=True)
    # Whether the user found the guide useful.
    useful = models.BooleanField(null=True)

    __repr__ = sane_repr("user", "guide_id", "viewed_ts", "dismissed_ts", "useful")

    class Meta:
        app_label = "sentry"
        db_table = "sentry_assistant_activity"
        unique_together = (("user", "guide_id"),)
