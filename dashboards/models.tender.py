from django.db import models
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser


class TenderContent(models.Model):
    class SimSpec(models.TextChoices):
        STANDARD = "SIM+SIM", "Сим+Сим"
        PREMIUM = "ESIM", "ЕСим"
        ULTRA = "SIM+ESIM", "Сим+ЕСим"

    model = models.CharField(max_length=80)
    sim_spec = models.CharField(
        max_length=7, choices=SimSpec.choices, default=SimSpec.STANDARD
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
        related_name="edited_offers",
    )


class PartnerOffersActions(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="edited_offers",
    )
    action = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
