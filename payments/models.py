from django.db import models

from store.models import ShippingAdress


class Payment(models.Model):
    order = models.ForeignKey(ShippingAdress, related_name="payments", on_delete=models.CASCADE)
    transaction_amount = models.DecimalField(
        "Valor da Transação", max_digits=10, decimal_places=2
    )
    installments = models.IntegerField("Parcelas")
    payment_method_id = models.CharField("Método de Pagamento", max_length=250)
    email = models.EmailField()
    mercado_pago_id = models.CharField(max_length=250, blank=True, db_index=True)
    mercado_pago_status = models.CharField(max_length=250, blank=True)
    mercado_pago_status_detail = models.CharField(max_length=250, blank=True)


    def __str__(self):
        return f"Pagamento {self.id}"