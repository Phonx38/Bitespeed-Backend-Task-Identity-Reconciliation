from django.db import models
from django.utils import timezone


class LinkPrecedenceTypes(models.TextChoices):
    PRIMARY = "Primary"
    SECONDARY = "Secondary"


class Contact(models.Model):
    phoneNumber = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    linkedId = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )
    linkPrecedence = models.CharField(
        max_length=10,
        choices=LinkPrecedenceTypes.choices,
        default=LinkPrecedenceTypes.PRIMARY,
    )
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)
