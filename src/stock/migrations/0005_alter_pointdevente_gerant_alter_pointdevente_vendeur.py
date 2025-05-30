# Generated by Django 5.2 on 2025-05-20 20:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stock", "0004_rename_categorie_article_categorie_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="pointdevente",
            name="gerant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="gerant",
                to=settings.AUTH_USER_MODEL,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="pointdevente",
            name="vendeur",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="vendeur",
                to=settings.AUTH_USER_MODEL,
                unique=True,
            ),
        ),
    ]
