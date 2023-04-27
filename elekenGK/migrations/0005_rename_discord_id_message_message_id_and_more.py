# Generated by Django 4.2 on 2023-04-26 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elekenGK', '0004_message_version_id_alter_message_discord_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='discord_id',
            new_name='message_id',
        ),
        migrations.AddField(
            model_name='message',
            name='channel_id',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='userdata',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
