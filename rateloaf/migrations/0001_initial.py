# Generated by Django 4.2.15 on 2024-09-03 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CatLoaf",
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
                ("is_rated", models.BooleanField(default=False)),
                ("is_rating", models.BooleanField(default=False)),
                ("has_cat_outline", models.BooleanField(default=False)),
                ("unique_name", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=300, null=True),
                ),
                (
                    "only_cat_filter",
                    models.IntegerField(blank=True, null=True),
                ),
                ("blemish_pass_1", models.IntegerField(blank=True, null=True)),
                ("blemish_pass_2", models.IntegerField(blank=True, null=True)),
                ("image_url_user", models.CharField(max_length=100)),
                (
                    "image_url_original",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "image_url_blemish_1",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "image_url_blemish_2",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
            ],
        ),
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
            ],
        ),
    ]
