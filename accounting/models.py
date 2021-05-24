from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
import datetime

# Create your models here.
#
DEBIT = 'debit'
CREDIT = 'credit'
BALANCE_TYPE = [
        (CREDIT, _('Credit')),
        (DEBIT, _('Debit'))
]

class AccountCategory(models.Model):

    name = models.CharField(max_length=100, verbose_name=_('Account Name'))

    balance_type = models.CharField(max_length=6, choices=BALANCE_TYPE, verbose_name=_('Account Balance Type'))



    def __str__(self):
        return self.name

    def balance(self):

        accounts=self.account.all()

        debit_total=0
        credit_total=0
        for account in accounts:
           transaction=account.transaction.all()
           debit_tnxs=transaction.filter(tnx_type='debit')
           credit_tnxs=transaction.filter(tnx_type='credit')

           for tnx in debit_tnxs:
               debit_total=debit_total+tnx.amount

           for tnx in credit_tnxs:
               credit_total=credit_total+tnx.amount


        if self.balance_type==DEBIT:
            return debit_total-credit_total
        else:
            return credit_total-debit_total



class Account(models.Model):
    #uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    code = models.CharField(max_length=10, unique=True, verbose_name=_('Account Code'))
    account_category = models.ForeignKey(
            AccountCategory, related_name='account',on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100, verbose_name=_('Account Name'))





    def __str__(self):
        return self.account_category.name.upper()+'-'+self.code+': '+self.name

    def full_name(self):

        return self.account_category.name.upper()+'-'+self.code+': '+self.name

    def category_name(self):
        return self.account_category.name





class Transaction(models.Model):

    account = models.ForeignKey(
                Account, related_name='transaction',on_delete=models.CASCADE
        )
    tnx_type = models.CharField(max_length=6, choices=BALANCE_TYPE, verbose_name=_('Transaction Balance Type'))
    amount=models.FloatField(default=0)


    tnx_description=models.CharField(max_length=500, verbose_name=_('Transsaction Description'))
    added_on=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.account.full_name()+ '.......'+str(self.amount)

    def category_name(self):
        return self.account.account_category.name

    def account_name(self):
        return self.account.name

    def account_code(self):
        return self.account.code
