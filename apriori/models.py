from django.core.validators import FileExtensionValidator
from django.db import models


class Csv(models.Model):
    """model for products"""

    csv = models.FileField(
        null=True,
        blank=True,
        validators=[FileExtensionValidator(["csv"])],
        upload_to="files/",
    )
    min_support = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
