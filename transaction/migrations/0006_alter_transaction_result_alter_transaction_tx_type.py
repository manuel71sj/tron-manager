# Generated by Django 4.0.4 on 2022-04-27 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0005_transaction_tx_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='result',
            field=models.CharField(choices=[('SUCCESS', '성공'), ('FAILED', '실패'), ('PENDING', '대기')], default='FAILED', help_text='트랜잭션 결과값', max_length=7, verbose_name='결과'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='tx_type',
            field=models.CharField(choices=[('CREATE_SMART_CONTRACT', '스마트컨트랙트 생성'), ('SEND_TRX', 'TRX 전송')], default='CREATE_SMART_CONTRACT', max_length=21, verbose_name='거래구분'),
        ),
    ]
