# Generated by Django 4.2.4 on 2023-09-08 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0005_commissionincome'),
    ]

    operations = [
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('commission', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='transferhistory',
            name='account_external',
            field=models.CharField(max_length=50),
        ),
    ]
