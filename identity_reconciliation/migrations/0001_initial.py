# Generated by Django 4.2.2 on 2023-06-20 06:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "phoneNumber",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("email", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "linkPrecedence",
                    models.CharField(
                        choices=[("Primary", "Primary"), ("Secondary", "Secondary")],
                        default="Primary",
                        max_length=10,
                    ),
                ),
                ("createdAt", models.DateTimeField(default=django.utils.timezone.now)),
                ("updatedAt", models.DateTimeField(auto_now=True)),
                ("deletedAt", models.DateTimeField(blank=True, null=True)),
                (
                    "linkedId",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="identity_reconciliation.contact",
                    ),
                ),
            ],
        ),
    ]
