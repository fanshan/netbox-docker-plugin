"""Models definitions"""

from django.db import models
from django.urls import reverse
from django.core.validators import (
    URLValidator,
    MinLengthValidator,
    MaxLengthValidator,
)
from utilities.choices import ChoiceSet
from netbox.models import NetBoxModel


class ImageProviderChoices(ChoiceSet):
    """ImageProvider choices definition class"""

    key = "Image.provider"

    DEFAULT_VALUE = "dockerhub"

    CHOICES = [
        ("dockerhub", "Docker Hub", "dark"),
        ("github", "GitHub", "blue"),
    ]


class Host(NetBoxModel):
    """Host definition class"""

    endpoint = models.CharField(max_length=1024, validators=[URLValidator()])
    name = models.CharField(
        unique=True,
        max_length=255,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=255),
        ],
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        """override"""
        return reverse("plugins:netbox_docker:host", args=[self.pk])


class Image(NetBoxModel):
    """Image definition class"""

    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="images")
    name = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=255),
        ],
    )
    version = models.CharField(
        default="latest",
        max_length=32,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=32),
        ],
    )
    provider = models.CharField(
        max_length=32,
        choices=ImageProviderChoices,
        default=ImageProviderChoices.DEFAULT_VALUE,
        blank=False,
    )

    class Meta:
        unique_together = ["host", "name", "version"]
        ordering = ("name", "version")

    def __str__(self):
        return f"{self.name}:{self.version}"

    def get_absolute_url(self):
        """override"""
        return reverse("plugins:netbox_docker:image", args=[self.pk])