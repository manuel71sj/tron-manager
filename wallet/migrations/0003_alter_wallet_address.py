# Generated by Django 4.0.4 on 2022-04-22 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_wallet_passphrase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='address',
            field=models.CharField(max_length=34, verbose_name='지갑주소'),
        ),
    ]
