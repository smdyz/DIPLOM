# Generated by Django 5.0.6 on 2024-06-23 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0002_course_owner_lesson_owner"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="course",
            name="owner",
        ),
        migrations.RemoveField(
            model_name="lesson",
            name="owner",
        ),
    ]
