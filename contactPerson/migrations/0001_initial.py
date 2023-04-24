# Generated by Django 4.2 on 2023-04-11 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContactPerson",
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
                ("person_id", models.IntegerField()),
                ("email", models.TextField()),
                ("name", models.TextField()),
                ("phone_1", models.BigIntegerField()),
                ("phone_2", models.BigIntegerField(null=True)),
            ],
        ),
    ]