from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class TenderContent(models.Model):
    class SimSpec(models.TextChoices):
        STANDARD = "SIM+SIM", "Сим+Сим"
        PREMIUM = "ESIM", "ЕСим"
        ULTRA = "SIM+ESIM", "Сим+ЕСим"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        CLOSED = "closed", "Closed"
        CANCELED = "canceled", "Canceled"

    model = models.CharField(max_length=80)
    buyer_name = models.CharField(default="unknown")
    colors = ArrayField(
        models.CharField(max_length=50),
        blank=True,
        null=True,
        default=list,
    )
    sim_spec = models.CharField(
        max_length=10, choices=SimSpec.choices, default=SimSpec.STANDARD
    )
    order_qty = models.IntegerField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    finish_reason = models.CharField(max_length=70, blank=True, null=True)

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
    qty = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_editor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="offers_edited",
    )


class OfferWinners(models.Model):
    tender = models.ForeignKey(
        TenderContent, on_delete=models.CASCADE, related_name="winners"
    )
    offer = models.ForeignKey(
        PartnerOffers, on_delete=models.CASCADE, related_name="winners"
    )
    qty = models.IntegerField()


class PartnerOffersActions(models.Model):
    user = models.CharField(max_length=40)
    action = models.CharField(max_length=40)
    target = models.CharField(max_length=40, blank=True, null=True)
    old_value = models.CharField(max_length=40, blank=True, null=True)
    new_value = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
