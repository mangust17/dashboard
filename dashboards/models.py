from django.db import models
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
from .models_tender import *


class InnerCompanys(models.Model):
    company_id = models.CharField(max_length=40, primary_key=True, unique=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "main_innercompanys"


class Customers(models.Model):
    customer_id = models.CharField(
        max_length=40, primary_key=True, unique=True, db_column="customer_id"
    )
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "main_customers"


class Sponsors(models.Model):
    sponsor_id = models.CharField(
        max_length=40, unique=True, primary_key=True, db_column="sponsor_id"
    )
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "main_sponsors"


class Invoices(models.Model):
    created_date = models.DateField()
    invoice = models.IntegerField(primary_key=True, unique=True)
    real_number = models.CharField(max_length=40, blank=True, null=True)
    inner_number = models.IntegerField(blank=True, null=True)
    customer = models.ForeignKey(
        Customers, on_delete=models.CASCADE, db_column="customer", blank=True, null=True
    )
    sponsor = models.ForeignKey(
        Sponsors, on_delete=models.CASCADE, db_column="sponsor", blank=True, null=True
    )
    inner_company = models.ForeignKey(
        InnerCompanys,
        on_delete=models.CASCADE,
        db_column="inner_company",
        blank=True,
        null=True,
    )
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    rate_value = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "main_invoices"


class SpecsDetail(models.Model):
    country_short = models.CharField(max_length=40, primary_key=True, unique=True)
    spec = models.CharField(max_length=50, blank=True, null=True)
    iso_alpha = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "main_specsdetail"


class TaxRates(models.Model):
    model_type = models.CharField(primary_key=True, max_length=40)
    tax_rate = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.model_type

    class Meta:
        managed = False
        db_table = "main_taxrates"


class AggregatedModel(models.Model):
    color = models.CharField(max_length=80)
    model = models.CharField(max_length=80)
    model_type = models.ForeignKey(
        TaxRates, on_delete=models.CASCADE, blank=True, null=True
    )
    first_model_id_ns = models.CharField(max_length=10, primary_key=True)
    brand = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "main_aggregatedmodel"


class PricesClean(models.Model):
    # Define the fields that match the existing table's columns
    id = models.AutoField(primary_key=True, unique=True)
    date = models.DateField()
    datetime = models.DateTimeField(blank=True, null=True)
    vendor = models.CharField(max_length=50, default="None")
    country = models.CharField(max_length=50, default="None")
    model = models.CharField(max_length=50, default="None")
    color = models.CharField(max_length=40, default="None")
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    country_id = models.ForeignKey(
        SpecsDetail,
        db_column="country_id",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="countries",
    )
    model_id = models.ForeignKey(
        AggregatedModel,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="model_id",
        related_name="pricescleans",
    )

    class Meta:
        managed = False
        db_table = "main_pricesclean"


class CleanReportsBuy(models.Model):
    id = models.AutoField(primary_key=True)
    message_id = models.IntegerField(blank=True, null=True)
    date_time = models.DateTimeField(default=datetime.now)
    editor = models.CharField(max_length=20, blank=True, null=True)
    model = models.CharField(max_length=40)
    model_id_ns = models.CharField(max_length=40, default=None, blank=True, null=True)
    color = models.CharField(max_length=80)
    quantity = models.IntegerField()
    type = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, default="Not")
    invoice_id = models.IntegerField(default=0)
    date_bought = models.DateTimeField(default=None, blank=True, null=True)
    date_distributed = models.DateTimeField(default=None, blank=True, null=True)
    date_rdy_for_ship = models.DateTimeField(default=None, blank=True, null=True)
    date_shipped = models.DateTimeField(default=None, blank=True, null=True)
    date_rdy_for_close = models.DateTimeField(default=None, blank=True, null=True)
    date_finished = models.DateTimeField(default=None, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "main_cleanreportsbuy"


class InvoiceContent(models.Model):
    invoice = models.ForeignKey(
        Invoices,
        on_delete=models.CASCADE,
        db_column="invoice",
        related_name="invoicecontents",
    )
    model = models.CharField(max_length=80)
    color = models.CharField(max_length=80)
    quantity = models.IntegerField()
    price = models.FloatField(default=0)
    comment = models.CharField(max_length=70, blank=True, null=True)
    status = models.CharField(max_length=40, blank=True, null=True)
    model_id = models.ForeignKey(
        AggregatedModel,
        on_delete=models.CASCADE,
        db_column="model_id",
        related_name="invoicecontents",
    )
    price_per_unit = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "main_invoicecontent"


class CurrencyNew(models.Model):
    id = models.AutoField(primary_key=True, db_column="id")
    datetime = models.DateTimeField()
    code = models.CharField(max_length=40)
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = "main_currencynew"
