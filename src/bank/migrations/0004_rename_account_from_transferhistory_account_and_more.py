# Generated by Django 4.2.4 on 2023-09-07 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0003_transferhistory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transferhistory',
            old_name='account_from',
            new_name='account',
        ),
        migrations.RenameField(
            model_name='transferhistory',
            old_name='account_to',
            new_name='account_external',
        ),
    ]
