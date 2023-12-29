# Generated by Django 5.0 on 2023-12-27 18:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"ordering": ["first_name", "last_name"]},
        ),
        migrations.AlterField(
            model_name="user",
            name="profile_image",
            field=models.ImageField(blank=True, null=True, upload_to="users/"),
        ),
    ]
