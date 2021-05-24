from django.contrib import admin
from accounting.models import AccountCategory, Account, Transaction

# Register your models here.

admin.site.register(AccountCategory)
admin.site.register(Account)
admin.site.register(Transaction)
