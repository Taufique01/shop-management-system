from django.contrib import admin

#Register your models here.
from inventory.models import  EmployeeSalary, BillDetails, \
    EmployeeBank, Bill, Customer, Employee

from inventory.models import Product,StockIn,ProductDetail,Supplier,PurchaseBillDetails,PurchaseBill,CashReceived, CashPaid,Sim,SimSell,SimCompanyPayment,Cash

from inventory.models import SellSimAdmin

admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Bill)
admin.site.register(EmployeeSalary)
admin.site.register(BillDetails)
admin.site.register(EmployeeBank)


admin.site.register(Product)
admin.site.register(StockIn)
admin.site.register(ProductDetail)
admin.site.register(Supplier)

admin.site.register(PurchaseBill)
admin.site.register(PurchaseBillDetails)

admin.site.register(CashReceived)
admin.site.register(CashPaid)
admin.site.register(Sim)
admin.site.register(SimSell,SellSimAdmin)
admin.site.register(SimCompanyPayment)
admin.site.register(Cash)




