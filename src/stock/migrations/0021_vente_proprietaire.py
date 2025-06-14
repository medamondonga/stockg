# Generated by Django 5.2 on 2025-06-15 17:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stock", "0020_alter_categorie_type_categorie"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="vente",
            name="proprietaire",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="proprio_vente",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
