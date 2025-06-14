# Generated by Django 5.2 on 2025-06-15 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stock", "0019_article_proprietaire_categorie_proprietaire_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="categorie",
            name="type_categorie",
            field=models.CharField(
                blank=True,
                choices=[
                    ("chaussures", "Chaussures"),
                    ("vetements", "Vetements"),
                    ("sacs", "Sacs"),
                    ("autre", "Autre"),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]
