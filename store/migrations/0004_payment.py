# Generated by Django 3.2.7 on 2021-10-21 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor da Transação')),
                ('installments', models.IntegerField(verbose_name='Parcelas')),
                ('payment_method_id', models.CharField(max_length=250, verbose_name='Método de Pagamento')),
                ('email', models.EmailField(max_length=254)),
                ('mercado_pago_id', models.CharField(blank=True, db_index=True, max_length=250)),
                ('mercado_pago_status', models.CharField(blank=True, max_length=250)),
                ('mercado_pago_status_detail', models.CharField(blank=True, max_length=250)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='store.shippingadress')),
            ],
        ),
    ]
