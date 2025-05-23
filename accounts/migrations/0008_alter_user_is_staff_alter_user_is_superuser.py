# Generated by Django 5.1.2 on 2024-11-14 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_alter_user_created_at_alter_user_updated_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="is_staff",
            field=models.BooleanField(
                default=False,
                help_text="Определяет может ли пользователь попасть в админ-панель",
                verbose_name="Администратор?",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_superuser",
            field=models.BooleanField(
                default=False,
                help_text="Определяет имеет ли пользователь доступ ко всему без предварительного разрешения.",
                verbose_name="Суперпользователь?",
            ),
        ),
    ]
