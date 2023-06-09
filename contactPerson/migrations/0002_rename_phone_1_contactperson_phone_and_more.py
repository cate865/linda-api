# Generated by Django 4.2 on 2023-04-12 20:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contactPerson", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="contactperson",
            old_name="phone_1",
            new_name="phone",
        ),
        migrations.RemoveField(
            model_name="contactperson",
            name="person_id",
        ),
        migrations.RemoveField(
            model_name="contactperson",
            name="phone_2",
        ),
        migrations.AddField(
            model_name="contactperson",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
