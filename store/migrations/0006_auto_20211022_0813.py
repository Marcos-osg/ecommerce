# Generated by Django 3.2.7 on 2021-10-22 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_remove_payment_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='mercado_pago_id',
            field=models.CharField(blank=True, db_index=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='mercado_pago_status',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='mercado_pago_status_detail',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]