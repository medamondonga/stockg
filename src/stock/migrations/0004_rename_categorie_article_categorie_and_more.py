# Generated by Django 5.2 on 2025-05-13 07:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stock", "0003_article_couleur"),
    ]

    operations = [
        migrations.RenameField(
            model_name="article",
            old_name="Categorie",
            new_name="categorie",
        ),
        migrations.AddField(
            model_name="article",
            name="point_de_vente",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="stock.pointdevente",
            ),
        ),
        migrations.AddField(
            model_name="vente",
            name="point_de_vente",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="stock.pointdevente",
            ),
        ),
    ]
