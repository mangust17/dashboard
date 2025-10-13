from django.db import models
from django.contrib.auth.models import User

class TenderContent(models.Model):
    class SimSpec(models.TextChoices):
        STANDARD = "SIM+SIM", "Сим+Сим"
        PREMIUM = "ESIM", "ЕСим"
        ULTRA = "SIM+ESIM", "Сим+ЕСим"

    model = models.CharField(max_length=80)
    sim_spec = models.CharField(
        max_length=10, choices=SimSpec.choices, default=SimSpec.STANDARD
    )
    order_qty = models.IntegerField()

    partner_min_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    partner_max_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    stat_min_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    stat_max_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )


class PartnerOffers(models.Model):
    tender = models.ForeignKey(
        TenderContent, on_delete=models.CASCADE, related_name="offers"
    )
    seller_name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_editor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="offers_edited",
        
    )


class PartnerOffersActions(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="offers_actions",
        null=True,
        blank=True,
    )
    action = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
