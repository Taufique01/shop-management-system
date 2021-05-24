"""InventoryManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from inventory import views
from inventory.views import SupplierViewSet,PurchaseBillViewSet
from inventory.views import StockInViewset

from accounting.views import TransactionViewSet,AccountViewSet,AccountCategoryViewSet
from InventoryManagementSystem import settings

router=routers.DefaultRouter()
router.register("product",views.ProductViewSet,basename="product")
router.register("employee",views.EmployeeViewset,basename="employee")
router.register("employee_all_bank",views.EmployeeBankViewset,basename="employee_all_bank")
router.register("employee_all_salary",views.EmployeeSalaryViewset,basename="employee_all_salary")
router.register("generate_bill_api",views.GenerateBillViewSet,basename="generate_bill_api")

router.register("home_api",views.HomeApiViewset,basename="home_api")

router.register("customer-api",views.CustomerViewSet,basename="customer_api")
router.register("supplier-api",views.SupplierViewSet,basename="supplier_api")
router.register("purchase-api",views.PurchaseBillViewSet,basename="purchase_api")
router.register("stockin-api",views.StockInViewset,basename="stockin")
router.register("sim-api",views.SimViewSet,basename="sim-view")


##Accounting App
router.register("transaction-api", TransactionViewSet,basename="transaction_api")
router.register("account-api", AccountViewSet,basename="transaction_api")


import os

urlpatterns = [
	path('', TemplateView.as_view( template_name = "build/index.html")),
	path('home', TemplateView.as_view( template_name = "build/index.html")),
	path('manifest.json', TemplateView.as_view( template_name = "build/manifest.json")),
	
	path('manageProduct', TemplateView.as_view( template_name = "build/index.html")),
	
	path('manageCustomer', TemplateView.as_view( template_name = "build/index.html")),
	path('addCustomer', TemplateView.as_view( template_name = "build/index.html")),
	path('addProduct', TemplateView.as_view( template_name = "build/index.html")),
	path('generateBill', TemplateView.as_view( template_name = "build/index.html")),
	path('manageBills', TemplateView.as_view( template_name = "build/index.html")),
	path('addPurchase', TemplateView.as_view( template_name = "build/index.html")),
	path('managePurchase', TemplateView.as_view( template_name = "build/index.html")),
	path('manageSupplier', TemplateView.as_view( template_name = "build/index.html")),
	path('supplierLedger', TemplateView.as_view( template_name = "build/index.html")),
	path('addTransactions', TemplateView.as_view( template_name = "build/index.html")),
	path('transactions', TemplateView.as_view( template_name = "build/index.html")),
	path('employeeManage', TemplateView.as_view( template_name = "build/index.html")),
	path('simManagement', TemplateView.as_view( template_name = "build/index.html")),

    path('admin/', admin.site.urls),
    path('api/',include(router.urls)),
    path('api/gettoken/',TokenObtainPairView.as_view(),name="gettoken"),
    path('api/resfresh_token/',TokenRefreshView.as_view(),name="refresh_token"),
    path('api/employee_bankby_id/<str:employee_id>',views.EmployeeBankByEIDViewSet.as_view(),name="employee_bankby_id"),
    path('api/employee_salaryby_id/<str:employee_id>',views.EmployeeSalaryByEIDViewSet.as_view(),name="employee_salaryby_id"),

    path('api/supplier-payment/',views.supplierPayment, name="supplier_payment"),
    path('api/customer-payment/',views.customerPayment, name='customer_payment'),
	path('api/save-sim-sell/',views.saveSimSell, name='save_sim_sell'),
	path('api/sim-monthly-sell/',views.getSimMonthlyLedger, name='sim_monthly_ledger'),
	path('api/sim-company-payment/',views.saveSimCompanyPayment, name='sim_company_payment'),

	path('logout', TemplateView.as_view( template_name = "build/index.html")),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
