# Generated by Django 5.0.4 on 2024-05-08 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0008_alter_message_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.TextField(),
        ),
    ]
