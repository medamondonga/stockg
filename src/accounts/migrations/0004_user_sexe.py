# Generated by Django 5.2 on 2025-05-06 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_alter_user_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="sexe",
            field=models.CharField(
                choices=[("homme", "Homme"), ("femme", "Femme")],
                default="Unknown",
                max_length=10,
            ),
        ),
    ]
