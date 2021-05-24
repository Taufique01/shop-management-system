from django.db import models
from django.contrib import admin
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
import calendar





###my edit
from django.utils import timezone



class DatedModel(models.Model):
    class Meta:
        abstract = True

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)



class Product(models.Model):
    UNIT_TYPE_KG = 'Kilogram'
    UNIT_TYPE_GRAM = 'Gram'
    UNIT_TYPE_LITRE = 'Litre'
    UNIT_TYPE_QUANTITY = 'Quantity'

    UNIT_TYPES = (
        (UNIT_TYPE_QUANTITY, 'Quantity'),
        (UNIT_TYPE_GRAM, 'Gram'),
        (UNIT_TYPE_LITRE, 'Litre'),
        (UNIT_TYPE_KG, 'Kilogram'),
    )
    unit_type = models.CharField(
        choices=UNIT_TYPES, default=UNIT_TYPE_QUANTITY,
        blank=True, null=True, max_length=200
    )
    name = models.CharField(max_length=100, unique=True)
    brand_name = models.CharField(max_length=200, blank=True, null=True)




    def __str__(self):
        return self.name



    def total_items(self):
        try:
            obj_stock_in = self.stockin_product.aggregate(Sum('quantity'))
            stock_in = float(obj_stock_in.get('quantity__sum'))
        except:
            stock_in = 0

        return stock_in








@receiver(post_save, sender=Product)
def create_produc_detail(sender, instance, created, **kwargs):
    if created:
        #Tabel.objects.create(employee=instance.employee)
        ProductDetail.objects.create(product=instance)




class ProductDetail(DatedModel):
    product = models.OneToOneField(
        Product, related_name='product_detail',on_delete=models.CASCADE
    )
    retail_price = models.FloatField(
         default=0
    )
    consumer_price = models.FloatField(
        default=0
    )

    available_item = models.FloatField(default=0)
    purchased_item = models.FloatField(default=0)


    def __str__(self):
        return self.product.name


    def current_profit(self):
        profit=self.consumer_price-self.retail_price
        return round(profit,2)




class StockIn(models.Model):
    product = models.ForeignKey(
        Product, related_name='stockin_product',on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        'Supplier',
        related_name='stockin_supplier',on_delete=models.CASCADE
    )
    quantity = models.FloatField(

    )
    buying_price = models.FloatField(
        default=0
    )

    selling_price_unit = models.FloatField(
        default=0
    )

    added_on=models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def buying_price_unit(self):
        bpu=float(self.buying_price)/float(self.quantity)
        #print(bpu)
        return round(bpu,2)

    def __str__(self):
        return str(self.id)+'.....'+ self.product.name +"  "+ self.supplier.name


@receiver(post_save, sender=StockIn)
def update_produc_detail(sender, instance, created, **kwargs):
    if created:
        #print("here")
        #Tabel.objects.create(employee=instance.employee)
        pd=instance.product.product_detail
        pd.retail_price=(pd.retail_price*pd.available_item+float(instance.buying_price))/(float(instance.quantity)+pd.available_item)
        pd.retail_price=round(pd.retail_price,2)
        pd.consumer_price=instance.selling_price_unit
        pd.available_item=pd.available_item+float(instance.quantity)
        pd.purchased_item=pd.purchased_item+float(instance.quantity)

        pd.save()






class Employee(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    joining_date=models.DateField()
    phone=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    added_on=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return self.name

####edited
class Customer(models.Model):

    name=models.CharField(max_length=255)

    phone=models.CharField(max_length=255)
    address=models.TextField(max_length=255)
    added_on=models.DateTimeField(auto_now_add=True)


    def total_debit(self):
        bills=self.bill.all()

        total=0
        for bill in bills:
            total=total+bill.grand_total()
        return round(total,2)


    def total_credit(self):
        cash_receiveds=self.cash_received.all()

        total=0
        for cash_received in cash_receiveds:
            total=total+cash_received.amount

        return round(total,2)


    def balance(self):
        balance=self.total_debit()-self.total_credit()
        return round(balance,2)




    def __str__(self):
        return self.name




class Supplier(models.Model):

    name=models.CharField(max_length=255)

    phone=models.CharField(max_length=255)
    company=models.CharField(max_length=255)
    address=models.TextField(max_length=255)
    added_on=models.DateTimeField(auto_now_add=True)


    def total_credit(self):
        purchases=self.purchase_bill.all()

        total=0
        for purchase in purchases:
            total=total+purchase.grand_total()
        return round(total,2)


    def total_debit(self):
        cash_paids=self.cash_paid.all()

        total=0
        for cash_paid in cash_paids:
            total=total+cash_paid.amount

        return round(total,2)


    def balance(self):
        balance=self.total_debit()-self.total_credit()
        return round(balance,2)




    def __str__(self):
        return self.name + "  "+ self.company






class EmployeeSalary(models.Model):
    id=models.AutoField(primary_key=True)
    employee_id=models.ForeignKey(Employee,on_delete=models.CASCADE)
    salary_date=models.DateField()
    salary_amount=models.CharField(max_length=255)
    added_on=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return self.employee_id.name

@receiver(post_save, sender=EmployeeSalary)
def substract_from_cash(sender, instance, created, **kwargs):
    if created:
        Cash.load().add_cash(-1*int(instance.salary_amount))


class CashReceived(models.Model):
    customer=models.ForeignKey(Customer,related_name='cash_received',on_delete=models.CASCADE)
    amount=models.FloatField(default=0)

    method=models.CharField(default='cash', max_length=100)



    def __str__(self):
        return self.customer.name+"........."+str(self.amount)

@receiver(post_save, sender=CashReceived)
def add_to_cash(sender, instance, created, **kwargs):
    if created:
        Cash.load().add_cash(instance.amount)
    else:
        Cash.load().add_cash(instance.amount)
        


class CashPaid(models.Model):
    supplier=models.ForeignKey(Supplier,related_name='cash_paid',on_delete=models.CASCADE)
    amount=models.FloatField(default=0)
    method=models.CharField(default='cash', max_length=100)


    def __str__(self):
        return self.supplier.name+"........."+str(self.amount)

@receiver(post_save, sender=CashPaid)
def substract_from_cash(sender, instance, created, **kwargs):
    if created:
        Cash.load().add_cash(-1*instance.amount)
    else:
        Cash.load().add_cash(-1*instance.amount)


class Bill(models.Model):

    customer=models.ForeignKey(Customer,related_name='bill',on_delete=models.CASCADE)

    cash_received=models.ForeignKey(CashReceived,related_name='bill',on_delete=models.CASCADE)

    discount=models.FloatField(default=0)


    added_on=models.DateTimeField(auto_now_add=True)


    def grand_total(self):

        grand_total=self.total()-self.discount
        return round(grand_total,2)

    def total(self):
        bill_details=self.bill_details.all()

        total=0
        for item in bill_details:
            total=total+item.product_price*item.quantity
            #print("one"+ str(total))
        return round(total,2)


    def profit(self):
        bill_details=self.bill_details.all()

        total=0
        for item in bill_details:
            total=total+item.profit
        profit=total-self.discount
        return round(profit,2)


    def paid(self):
        return self.cash_received.amount


    def due(self):
        due=self.grand_total()-self.paid()
        return round(due,2)
    def __str__(self):
        return 'iD: '+str(self.id)+'.....'+'Total: '+str(self.grand_total())






class BillDetails(models.Model):
	bill=models.ForeignKey(Bill,related_name='bill_details',on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	quantity=models.FloatField(default=0)
	profit=models.FloatField(default=0)
	product_price=models.FloatField(default=0)
	added_on=models.DateTimeField(auto_now_add=True)

	def __self__():
		return str(self.bill.id)+' '+ self.product.name

	def product_name(self):
		return self.product.name

	def product_unit(self):
		return self.product.unit_type
	
	def product_company(self):
		return self.product.brand_name
	def cost(self):
		cost=self.quantity * self.product_price
		return round(cost,2)


	def save(self, *args, **kwargs):
		if 'form' in kwargs:
			form=kwargs['form']
		else:
			form=None



		if self.pk is None:
			product_detail=self.product.product_detail
			product_detail.available_item = product_detail.available_item-self.quantity
			product_detail.save()

			self.profit=self.quantity*product_detail.current_profit()
			self.product_price=self.product.product_detail.consumer_price

		super(BillDetails, self).save(*args, **kwargs)


	def __str__(self):
		return 'Bill id: '+str(self.bill.id )+ ' ..........Product_name: '+self.product.name+'..........'+str(self.cost())




class PurchaseBill(models.Model):

    supplier=models.ForeignKey(Supplier,related_name='purchase_bill',on_delete=models.CASCADE)
    cash_paid=models.ForeignKey(CashPaid,related_name='purchase_bill',on_delete=models.CASCADE)

    discount=models.FloatField(default=0)

    added_on=models.DateTimeField(auto_now_add=True)


    def grand_total(self):


        grand_total=self.total()-self.discount
        return round(grand_total,2)


    def total(self):
        bill_details=self.purchase_bill_details.all()

        total=0
        for item in bill_details:
            total=total+item.cost()
            #print("one"+ str(total))

        return round(total,2)

    def paid(self):
      return self.cash_paid.amount


    def due(self):
        due=self.grand_total()-self.paid()
        return round(due,2)

    def __str__(self):
        return 'iD: '+str(self.id)+'.....'+'Total: '+str(self.grand_total())


class PurchaseBillDetails(models.Model):

    purchase_bill=models.ForeignKey(PurchaseBill,related_name='purchase_bill_details',on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    quantity=models.FloatField(default=0)

    unit_type=models.CharField(max_length=100)
    unit_price=models.FloatField(default=0)


    added_on=models.DateTimeField(auto_now_add=True)

    def __self__():
        return str(self.bill.id)+' '+ self.product.name

    def product_name(self):
        return self.product.name


    def product_company(self):
        return self.product.brand_name

    def cost(self):
        cost=self.quantity * self.unit_price
        return round(cost,2)

    def __str__(self):
        return 'Bill id: '+str(self.purchase_bill.id )+ ' ..........Product_name: '+self.product.name+'..........'+str(self.cost())


    #def save(self, *args, **kwargs):
    #    if 'form' in kwargs:
    #        form=kwargs['form']
    #    else:
    #        form=None

    #    if self.pk is None:

    #        product_detail=self.product.product_detail
    #        product_detail.available_item = product_detail.available_item+self.quantity
    #        product_detail.save()

    #    super(BillDetails, self).save(*args, **kwargs)







class EmployeeBank(models.Model):
    id=models.AutoField(primary_key=True)
    bank_account_no=models.CharField(max_length=255)
    ifsc_no=models.CharField(max_length=255)
    employee_id=models.ForeignKey(Employee,on_delete=models.CASCADE)
    added_on=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):

        return self.employee_id.name
		
		
		
		
####code for sim management#####
SIM_COMPANIES = (
	('GP', 'GP'),
	('ROBI', 'ROBI'),
	('BANGLALINK', 'BANGLALINK'),
	('TELETALK', 'TELETALK'),
)

class Sim(DatedModel):
	
	title=models.CharField(max_length=200)
	company=models.CharField(max_length=200,choices=SIM_COMPANIES)
	retail_price = models.FloatField(default=0)
	consumer_price = models.FloatField(default=0)
	available_item = models.FloatField(default=0)
	purchased_item = models.FloatField(default=0)
	
	def __str__(self):
		return self.title


class SimSell(DatedModel):
	PAID_BY_OPTIONS = (
		('customer', 'CUSTOMER'),
		('company', 'COMPANY'),
	)

	sim=models.ForeignKey(Sim,related_name='sim_sell',on_delete=models.CASCADE)
	customer=models.ForeignKey(Customer,related_name='sim_sell',on_delete=models.CASCADE)

	sim_number=models.CharField(max_length=15,unique=True)
	notes=models.CharField(max_length=500)
	paid_by=models.CharField(max_length=15,choices=PAID_BY_OPTIONS)
	
	price = models.FloatField(default=0)
	profit = models.FloatField(default=0)

	


	
	def __str__(self):
		return self.sim.title
	def sim_company(self):
		return self.sim.company

@receiver(post_save, sender=SimSell)
def add_to_cash(sender, instance, created, **kwargs):
	if created:
		if instance.paid_by=='customer':
			Cash.load().add_cash(instance.price)


		
class SimCompanyPayment(DatedModel):

	year=models.IntegerField()
	month=models.IntegerField()
	company=models.CharField(max_length=200,choices=SIM_COMPANIES)

	paid=models.IntegerField(default=0)
	
	class Meta:
		unique_together = ('year', 'month','company')
	
	def __str__(self):
		return calendar.month_name[self.month]+', '+str(self.year) +' ..... '+ self.company
	



			
# Create your models here.
class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class Cash(SingletonModel):

	amount=models.FloatField(default=0)
	
	def __str__(self):
		return str(self.amount)
	
	def add_cash(self,amount):
		self.amount=self.amount+amount
		#print(amount)
		#print(self.amount)
		
		self.save(update_fields=["amount"])



	
	

###Model Admins
class SellSimAdmin(admin.ModelAdmin):

	list_display= ['id','sim','customer','sim_number','price','profit','paid_by']  
	
	

	
	