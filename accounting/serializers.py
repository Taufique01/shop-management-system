from rest_framework import serializers

from accounting.models import AccountCategory, Account, Transaction

class AccountCategorySerializers(serializers.ModelSerializer):

    class Meta:
        model=AccountCategory
        fields=('id','name','balance')

class AccountSerializers(serializers.ModelSerializer):

    class Meta:
        model=Account
        fields=('id','code','name','account_category','full_name')




class AccountShortSerializers(serializers.ModelSerializer):

    class Meta:
        model=Account
        fields=('id','code','name','account_category','full_name')




class TransactionSerializers(serializers.ModelSerializer):
    added_on = serializers.DateTimeField(format="%Y-%m-%d")
    debit = serializers.SerializerMethodField('get_debit')
    credit = serializers.SerializerMethodField('get_credit')

    class Meta:
        model=Transaction
        fields=('id','debit','credit','tnx_description','category_name','account_name','account_code','added_on')

    def  get_debit(self, transaction):

         if transaction.tnx_type == 'debit':
            return transaction.amount
         else:
            return ''

    def  get_credit(self, transaction):

         if transaction.tnx_type == 'credit':
            return transaction.amount
         else:
            return ''
