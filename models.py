from __future__ import unicode_literals

from django.db import models

# Create your models here.

class AddbankAccount(models.Model):
    accountnumber = models.CharField(default='', max_length=255, blank=True, null=True)
    balance = models.FloatField(default=0.0, max_length=255, blank=True, null=True)

    class Meta:
        db_table = "add_bank_account"


class TransactionList(models.Model):
    accountnumber = models.CharField(default='', max_length=255, blank=True, null=True)
    charge = models.FloatField(default=0.0, max_length=255, blank=True, null=True)

    class Meta:
        db_table = "transactions"
