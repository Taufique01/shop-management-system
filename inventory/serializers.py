from rest_framework import serializers

from inventory.models import  Employee, Customer, Bill, EmployeeBank, EmployeeSalary, BillDetails

from inventory.models import Product,StockIn,ProductDetail,Customer,Supplier,StockIn,PurchaseBillDetails,PurchaseBill, CashPaid, CashReceived,Sim

class CustomerSerliazer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=('id','name','address','phone','balance')

class SupplierSerliazer(serializers.ModelSerializer):
    class Meta:
        model=Supplier
        fields=('id','name','phone','company','address','total_debit','total_credit','balance')




########***************
class ProductSerliazer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"

class ProductDetailsSerliazer(serializers.ModelSerializer):
    id = serializers.CharField(source='product.id')
    name = serializers.CharField(source='product.name')
    brand_name = serializers.CharField(source='product.brand_name')
    unit_type = serializers.CharField(source='product.unit_type')
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = ProductDetail
        fields = ('id', 'retail_price', 'consumer_price','purchased_item','available_item','name','brand_name','unit_type','updated_at')


class BillSerializer(serializers.ModelSerializer):
     customer_name = serializers.CharField(source='customer.name')
     #added_on = serializers.SerializerMethodField('det_added_on')
     class Meta:
         model=Bill




class StockInSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name')
    added_on = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
         model=StockIn
         fields=('id','supplier_name','quantity','buying_price','selling_price_unit','buying_price_unit','added_on')







class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields="__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields="__all__"

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bill
        fields="__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['customer'] = CustomerSerializer(instance.customer_id).data
        return response




class EmployeeBankSerializer(serializers.ModelSerializer):
    class Meta:
        model=EmployeeBank
        fields="__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['employee'] = EmployeeSerializer(instance.employee_id).data
        return response


class EmployeeSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model=EmployeeSalary
        fields="__all__"



class BillDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=BillDetails
        fields=('quantity', 'product_name','product_price','product_unit','product_company','cost')




class BillAllDetailsSerializer(serializers.ModelSerializer):
    bill_details=BillDetailsSerializer(many=True, read_only=True)
    customer = CustomerSerliazer()
    added_on=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model=Bill
        fields=('id','paid','added_on','total','grand_total', 'discount','due','bill_details','customer')




class BillSerializer(serializers.ModelSerializer):
     customer_name = serializers.CharField(source='customer.name')
     added_on = serializers.SerializerMethodField('det_added_on')
     class Meta:
         model=Bill
         fields=('id','paid','added_on','grand_total','customer_name','due')
     def  det_added_on(self, obj):
         return obj.added_on.date()

class PurchaseSerializer(serializers.ModelSerializer):
     supplier_name = serializers.CharField(source='supplier.name')
     added_on = serializers.SerializerMethodField('det_added_on')
     class Meta:
         model=PurchaseBill
         fields=('id','paid','added_on','grand_total','supplier_name','due')

     def  det_added_on(self, obj):
         return obj.added_on.date()



class PurchaseDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=PurchaseBillDetails
        fields=('quantity', 'product_name','unit_price','unit_type','product_company','cost')




class PurchaseAllDetailsSerializer(serializers.ModelSerializer):
    purchase_bill_details=PurchaseDetailsSerializer(many=True, read_only=True)
    supplier = SupplierSerliazer()
    added_on=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model=PurchaseBill
        fields=('id','paid','added_on','total','grand_total', 'discount','due','purchase_bill_details','supplier')

		
		
###Sim Serializers####
class SimSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sim
        fields="__all__"