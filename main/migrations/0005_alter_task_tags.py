# Generated by Django 4.1.6 on 2023-05-22 09:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_rename_header_tag_title_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="tags",
            field=models.ManyToManyField(blank=True, to="main.tag"),
        ),
    ]
