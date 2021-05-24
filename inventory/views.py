from datetime import datetime, timedelta,date
from django.utils import timezone
import pytz
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
import calendar
from django.db.models import F

import json
from django.db.models import Sum
from rest_framework import viewsets, generics
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from InventoryManagementSystem import settings

from inventory.models import Employee, \
    EmployeeBank, EmployeeSalary, Bill, BillDetails,Sim,SimSell,SimCompanyPayment,Cash
##list
from inventory.models  import SIM_COMPANIES
from inventory.serializers import  EmployeeSerializer, \
    EmployeeBankSerializer, EmployeeSalarySerializer, CustomerSerializer, BillSerializer, BillDetailsSerializer,SimSerializer

from inventory.serializers import ProductSerliazer,ProductDetailsSerliazer,CustomerSerliazer,BillSerializer,\
    BillAllDetailsSerializer,SupplierSerliazer,StockInSerializer,PurchaseSerializer,PurchaseAllDetailsSerializer


from inventory.models import Product,StockIn,ProductDetail,Customer,Bill,Supplier,PurchaseBillDetails,PurchaseBill, CashPaid, CashReceived


from accounting.models import AccountCategory
from accounting.serializers import AccountCategorySerializers

from .utils import monthFirstAndLastDate
#OLD Viewset
# class CompanyViewSet(viewsets.ModelViewSet):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerliazer


class CustomerViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request):
        customer=Customer.objects.all().order_by('-id')
        serializer=CustomerSerliazer(customer,many=True,context={"request":request})
        #print(serializer.data)
        response_dict={"error":False,"message":"All Customer List Data","data":serializer.data}
        return Response(response_dict)


    def create(self,request):
        try:
            serializer=CustomerSerliazer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Customer Data Save Successfully"}
        except Exception as e:
            #print(e)
            dict_response={"error":True,"message":"Error During Saving Cust Data"}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        #queryset = Company.objects.all()
        #company = get_object_or_404(queryset, pk=pk)
        #serializer = CompanySerliazer(company, context={"request": request})

        #serializer_data = serializer.data
        # Accessing All the Medicine Details of Current Medicine ID
        #company_bank_details = CompanyBank.objects.filter(company_id=serializer_data["id"])
        #companybank_details_serializers = CompanyBankSerializer(company_bank_details, many=True)
        #serializer_data["company_bank"] = companybank_details_serializers.data

        #return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})
        pass
    def update(self,request,pk=None):
        try:

            queryset=Customer.objects.all()
            customer=get_object_or_404(queryset,pk=pk)
            serializer=CustomerSerliazer(customer,data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Successfully Updated Customer Data"}
        except:
            dict_response={"error":True,"message":"Error During Updating Customer Data."}
        return  Response(dict_response)



class SupplierViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request):
        supplier=Supplier.objects.all().order_by('-id')
        serializer=SupplierSerliazer(supplier,many=True,context={"request":request})
        #print(serializer.data)
        response_dict={"error":False,"message":"All Supplier List Data","data":serializer.data}
        return Response(response_dict)

    def create(self,request):
        try:
            serializer=SupplierSerliazer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Supplier Data Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Supplier Data"}
        return Response(dict_response)

    def update(self,request,pk=None):
        try:

            queryset=Supplier.objects.all()
            supplier=get_object_or_404(queryset,pk=pk)
            serializer=SupplierSerliazer(supplier,data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Successfully Updated Customer Data"}
        except:
            dict_response={"error":True,"message":"Error During Updating Customer Data."}
        return  Response(dict_response)













class ProductViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):
        #print(request.data)
        try:
            serializer=ProductSerliazer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()


            dict_response={"error":False,"message":"Product Data Save Successfully"}
        except Exception as e:
            print(e)
            dict_response={"error":True,"message":"Error During Saving Product Data"}
        return Response(dict_response)

    def list(self,request):
        products=ProductDetail.objects.all()
        serializer=ProductDetailsSerliazer(products,many=True,context={"request":request})

        product_datas=serializer.data




        #print(product_datas)
        response_dict={"error":False,"message":"All Product List Data","data":product_datas}
        return Response(response_dict)

#Company Account Viewset
class StockInViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):
        #print(request.data)
        try:
            supplier=Supplier.objects.get(id=request.data['supplier_id'])
            product=Product.objects.get(id=request.data['product_id'])
            stockin=StockIn()

            stockin.supplier=supplier
            stockin.product=product
            stockin.selling_price_unit=request.data['selling_price_unit']
            stockin.buying_price=request.data['buying_price']
            stockin.quantity=request.data['quantity']

            stockin.save()




            serializer=StockInSerializer(stockin)





            dict_response={"error":False,"message":"Stock in Data Save Successfully",'data':serializer.data}
        except Exception as e:
            print(e)
            dict_response={"error":True,"message":"Error During Saving Company Account Data"}
        return Response(dict_response)

    def list(self,request):

        stockin=StockIn.objects.all()
        serializer=StockInSerializer(stockin,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Stock in List Data","data":'a'}
        return Response(response_dict)



    def retrieve(self,request,pk=None):
        print("here")
        print(pk)
        stockin=StockIn.objects.filter(product__pk=pk)
        serializer=StockInSerializer(stockin,many=True,context={"request":request})
        response_dict={"error":False,"message":"All StockIn List Data","data":serializer.data}
        return Response(response_dict)
        #return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})




#Employee Viewset
class EmployeeViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):
        try:
            serializer=EmployeeSerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Employee Data Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Employee Data"}
        return Response(dict_response)

    def list(self,request):
        employee=Employee.objects.all()
        serializer=EmployeeSerializer(employee,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Employee List Data","data":serializer.data}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset=Employee.objects.all()
        employee=get_object_or_404(queryset,pk=pk)
        serializer=EmployeeSerializer(employee,context={"request":request})
        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})

    def update(self,request,pk=None):
        queryset=Employee.objects.all()
        employee=get_object_or_404(queryset,pk=pk)
        serializer=EmployeeSerializer(employee,data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()
        return Response({"error":False,"message":"Data Has Been Updated"})

#Employee Bank Viewset
class EmployeeBankViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):
        try:
            serializer=EmployeeBankSerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Employee Bank Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Employee Bank"}
        return Response(dict_response)

    def list(self,request):
        employeebank=EmployeeBank.objects.all()
        serializer=EmployeeBankSerializer(employeebank,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Employee Bank List Data","data":serializer.data}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset=EmployeeBank.objects.all()
        employeebank=get_object_or_404(queryset,pk=pk)
        serializer=EmployeeBankSerializer(employeebank,context={"request":request})
        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})

    def update(self,request,pk=None):
        queryset=EmployeeBank.objects.all()
        employeebank=get_object_or_404(queryset,pk=pk)
        serializer=EmployeeBankSerializer(employeebank,data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()
        return Response({"error":False,"message":"Data Has Been Updated"})

#Employee Salary Viewset
class EmployeeSalaryViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):
        try:
            serializer=EmployeeSalarySerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Employee Salary Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Employee Salary"}
        return Response(dict_response)

    def list(self,request):
        employeesalary=EmployeeSalary.objects.all()
        serializer=EmployeeSalarySerializer(employeesalary,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Employee Salary List Data","data":serializer.data}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset=EmployeeSalary.objects.all()
        employeesalary=get_object_or_404(queryset,pk=pk)
        serializer=EmployeeSalarySerializer(employeesalary,context={"request":request})
        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})

    def update(self,request,pk=None):
        queryset=EmployeeSalary.objects.all()
        employeesalary=get_object_or_404(queryset,pk=pk)
        serializer=EmployeeSalarySerializer(employeesalary,data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()
        return Response({"error":False,"message":"Data Has Been Updated"})

class EmployeeBankByEIDViewSet(generics.ListAPIView):
    serializer_class = EmployeeBankSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        employee_id=self.kwargs["employee_id"]
        return EmployeeBank.objects.filter(employee_id=employee_id)

class EmployeeSalaryByEIDViewSet(generics.ListAPIView):
    serializer_class = EmployeeSalarySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        employee_id=self.kwargs["employee_id"]
        return EmployeeSalary.objects.filter(employee_id=employee_id)



class GenerateBillViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def list(self,request):
        bill=Bill.objects.all().order_by('-id')
        serializer=BillSerializer(bill,many=True,context={"request":request})

        response_dict={"error":False,"message":"All Bills List Data ","data":serializer.data}
        return Response(response_dict)


    def create(self, request):


        try:
            customer=Customer.objects.get(id=request.data['customer_id'])
            cash_received=CashReceived.objects.create(customer=customer, amount=float(request.data['paid']))


            bill=Bill.objects.create(customer=customer, cash_received=cash_received, discount=float(request.data['discount']))

            for  item in request.data['product_details']:


                if not str(item['product_id']):
                    continue

                pdt=Product.objects.get(id=item['product_id'])
                bill_details=BillDetails.objects.create(bill=bill,product=pdt,quantity=float(item['quantity']))


            dict_response = {"error": False, "message": "Bill Generate Successfully","bill_id":bill.id,'time':(bill.added_on+timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S")}
        except  Exception as e:
            print(e)
            dict_response = {"error": True, "message": "Error During Generating BIll"}
        return Response(dict_response)
    def retrieve(self,request,pk=None):

        queryset=Bill.objects.all()
        bill_details=get_object_or_404(queryset,pk=pk)


        serializer=BillAllDetailsSerializer(bill_details,context={"request":request})
        #print(serializer.data)
        return Response({"error":False,"message":" Bill details Fetch Success","data":serializer.data})

    def update(self,request,pk=None):
        print("on bill update")
        try:
            #print(request.data)
            bill=Bill.objects.get(pk=pk)
            bill.discount=float(request.data['discount'])
            Cash.load().add_cash(-1*bill.cash_received.amount)
            bill.cash_received.amount=float(request.data['paid'])
            bill.cash_received.save()



            bill.save()

            data={

                'discount':bill.discount,
                'paid':bill.cash_received.amount,
                'due':bill.due(),
                'grand_total': bill.grand_total()


            }
            dict_response={"error":False,"message":"Successfully Updated Bill Data",'data':data}
        except Exception as  e:
            print(e)
            dict_response={"error":True,"message":"Error During Updating Bill Data"}

        return Response(dict_response)









class PurchaseBillViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def list(self,request):
        bill=PurchaseBill.objects.all().order_by('-id')
        serializer=PurchaseSerializer(bill,many=True,context={"request":request})

        response_dict={"error":False,"message":"All Bills List Data ","data":serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            #print("here")
            print(request.data)


            supplier=Supplier.objects.get(id=request.data['supplier_id'])

            cash_paid=CashPaid.objects.create(supplier=supplier, amount=float(request.data['paid']))
            purchase_bill=PurchaseBill.objects.create(supplier=supplier, cash_paid=cash_paid, discount=float(request.data['discount']))

            for  item in request.data['product_details']:


                if not str(item['product_id']):
                    continue

                pdt=Product.objects.get(id=item['product_id'])
                bill_details=PurchaseBillDetails.objects.create(purchase_bill=purchase_bill,product=pdt,
                    quantity=float(item['quantity']), unit_type=item['unit_type'], unit_price=item['unit_price'])


            dict_response = {"error": False, "message": "Bill Generate Successfully"}
        except  Exception as e:
            #print(e)
            dict_response = {"error": True, "message": "Error During Generating BIll"}
        return Response(dict_response)

    def retrieve(self,request,pk=None):
        #print("here")

        queryset=PurchaseBill.objects.all()
        purchase_details=get_object_or_404(queryset,pk=pk)


        serializer=PurchaseAllDetailsSerializer(purchase_details,context={"request":request})
        #print(serializer.data)
        return Response({"error":False,"message":" Bill details Fetch Success","data":serializer.data})


    def update(self,request,pk=None):
        #print("on purchase update")


        try:
            #print(request.data)
            purchase_bill=PurchaseBill.objects.get(pk=pk)
            #purchase_bill.discount=float(request.data['discount'])
            Cash.load().add_cash(purchase_bill.cash_paid.amount)
            purchase_bill.cash_paid.amount=float(request.data['paid'])
            purchase_bill.cash_paid.save()
            purchase_bill.save()

            data={

                #'discount':purchase_bill.discount,
                'paid': purchase_bill.cash_paid.amount,
                'due':purchase_bill.due(),
                'grand_total': purchase_bill.grand_total()


            }
            dict_response={"error":False,"message":"Successfully Updated Bill Data",'data':data}
        except Exception as  e:
            #print(e)
            dict_response={"error":True,"message":"Error During Updating Bill Data"}

        return Response(dict_response)





class HomeApiViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request):
        #customer_request=CustomerRequest.objects.all()
        #customer_request_serializer=CustomerRequestSerializer(customer_request,many=True,context={"request":request})
        total_product_inventory = (ProductDetail.objects.all().aggregate(total=Sum(F('retail_price')*F('available_item'))))['total']
        total_sim_inventory = (Sim.objects.all().aggregate(total=Sum(F('retail_price')*F('available_item'))))['total']
        if total_sim_inventory is None:
            total_sim_inventory=0
        if total_product_inventory is None:
            total_product_inventory=0
        total_inventory=total_product_inventory+total_sim_inventory##response
        total_inventory=round(total_inventory,2)
        total_cash=Cash.load().amount###response
        customers=Customer.objects.all()
        total_due=0##response
        for customer in customers:
           total_due=total_due+customer.balance()
        
        all_bills=Bill.objects.all()
        #tz=pytz.timezone(settings.TIME_ZONE)
        first_date, last_date=monthFirstAndLastDate(datetime.now())
        month_bills=all_bills.filter(added_on__gte=first_date, added_on__lte=last_date)

        sim_mon_sell=SimSell.objects.filter(created_at__gte=first_date, created_at__lte=last_date).aggregate(total=Sum('price'))['total']
        sim_mon_profit=SimSell.objects.filter(created_at__gte=first_date, created_at__lte=last_date).aggregate(total=Sum('profit'))['total']
        if sim_mon_sell is None:
            sim_mon_sell=0
        if sim_mon_profit is None:
            sim_mon_profit=0
        #print(sim_mon_sell)
        monthly_profit=sim_mon_profit##response
        monthly_bill=sim_mon_sell###response
        for bill in month_bills:
            monthly_profit=monthly_profit+bill.profit()
            monthly_bill=monthly_bill+bill.grand_total()
        monthly_profit=round(monthly_profit,2)
        monthly_bill=round(monthly_bill,2)
        todays_bills=month_bills.filter(added_on__gte=datetime.now().replace(hour=0, minute=0, second=0))
        today_sim_sell=SimSell.objects.filter(created_at__gte=datetime.now().replace(hour=0, minute=0, second=0)).aggregate(total=Sum('price'))['total']
        today_sim_profit=SimSell.objects.filter(created_at__gte=datetime.now().replace(hour=0, minute=0, second=0)).aggregate(total=Sum('profit'))['total']
        if today_sim_sell is None:
           today_sim_sell=0
        if today_sim_profit is None:
           today_sim_profit=0
		
        todays_bill_total=today_sim_sell##response
        todays_profit=today_sim_profit##response
        todays_due=0##response

        for bill in todays_bills:
            todays_bill_total=todays_bill_total+bill.grand_total()
            todays_profit=todays_profit+bill.profit()
            todays_due=todays_due+bill.due()


        todays_bill_total=round(todays_bill_total,2)
        todays_profit=round(todays_profit,2)

        sim_sell=SimSell.objects.all().aggregate(total=Sum('price'))['total']
        sim_profit=SimSell.objects.all().aggregate(total=Sum('profit'))['total']
        if sim_sell is None:
           sim_sell=0
        if sim_profit is None:
           sim_profit=0
        


        bill_total=sim_sell##response
        profit_total=sim_profit##response
        for bill in all_bills:
           bill_total=bill_total+ bill.grand_total()
           profit_total=profit_total+bill.profit()
        bill_total=round(bill_total,2)
        profit_total=round(profit_total,2)


        ac=AccountCategory.objects.all()
        serializer=AccountCategorySerializers(ac,many=True,context={"request":request})

        accounts_data=serializer.data


        bill_dates=BillDetails.objects.order_by().values("added_on__date").distinct()
        profit_chart_list=[]
        sell_chart_list=[]
        #buy_chart_list=[]request.body
        for billdate in bill_dates:
            access_date=billdate["added_on__date"]

            bill_data=Bill.objects.filter(added_on__date=access_date)
            profit_amt_inner=0
            sell_amt_inner=0
            for billsingle in bill_data:
                #buy_amt_inner = float(buy_amt_inner + float(billsingle.medicine_id.buy_price)) * int(billsingle.qty)
                sell_amt_inner = sell_amt_inner+ billsingle.grand_total()

                profit_amt_inner = profit_amt_inner+billsingle.profit()

            profit_chart_list.append({"date":access_date,"amt":profit_amt_inner})
            sell_chart_list.append({"date":access_date,"amt":sell_amt_inner})

        dict_respone={"error":False,"message":"Home Page Data","inventory_total":total_inventory,"total_cash":total_cash,
	    "todays_due":todays_due,"total_due":total_due,"bill_total":bill_total,"monthly_bill":monthly_bill,"todays_bill":todays_bill_total,"accounts_data":accounts_data,
        "todays_profit":todays_profit,"monthly_profit":monthly_profit,"profit_total":profit_total,"sell_chart":sell_chart_list,"profit_chart":profit_chart_list}


        return  Response(dict_respone)

@csrf_exempt
def supplierPayment(request):

    if request.method=="POST":


        try:
            data=json.loads(request.body)
            supplier=Supplier.objects.get(id=data['supplier_id'])
            CashPaid.objects.create(supplier=supplier, amount=float(data['amount']), method=data['method'])
            dict_response={"error":False,"message":"Successfully Added Payment"}
        except:
            dict_response={"error":True,"message":"Error During Adding Supplier Payment"}

        return JsonResponse(dict_response)


@csrf_exempt
def customerPayment(request):

    if request.method=="POST":

        try:
            data=json.loads(request.body)
            customer=Customer.objects.get(id=data['customer_id'])
            CashReceived.objects.create(customer=customer, amount=float(data['amount']), method=data['method'])
            dict_response={"error":False,"message":"Successfully Added Payment"}
        except:
            dict_response={"error":True,"message":"Error During Adding Supplier Payment"}

        return JsonResponse(dict_response)
		
		
		
		
#####views for sim Management####

class SimViewSet(viewsets.ViewSet):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]


	def list(self,request):
		print("here")
		sim=Sim.objects.all()
		serializer=SimSerializer(sim,many=True,context={"request":request})
		response_dict={"error":False,"message":"All Sims Data ","data":serializer.data}
		return Response(response_dict)
    

	def update(self,request,pk=None):
		try:
			print(request.data)
			sim=Sim.objects.get(pk=pk)
			stockin=float(request.data['stockin'])
			retail_price=float(request.data['retail_price'])
			previous_retail_price=sim.available_item*sim.retail_price
			changed_price=(previous_retail_price+retail_price*stockin)/(sim.available_item+stockin)
			
			
			sim.retail_price=round(changed_price,2)
			sim.consumer_price=float(request.data['consumer_price'])
			sim.available_item=sim.available_item+stockin
			sim.purchased_item=sim.purchased_item+stockin
			sim.save()
			
			dict_response={"error":False,"message":"Successfully Updated Sim Data"}
		except Exception as e:
			print(e)
			
			dict_response={"error":True,"message":"Error During Updating Sim Data"}
		return Response(dict_response)
		
@csrf_exempt
def saveSimSell(request):

	if request.method=="POST":
		try:
			sell_data=json.loads(request.body)
			print(sell_data)
			customer=Customer.objects.get(id=sell_data['customer_id'])
			sim=Sim.objects.get(id=sell_data['sim_id'])
			sim_sell=SimSell()
			sim_sell.sim=sim
			sim_sell.customer=customer
			sim_sell.sim_number=sell_data['sim_number']
			sim_sell.notes=sell_data['sim_notes']
			sim_sell.paid_by=sell_data['paid_by']
			sim_sell.price=sim.consumer_price
			sim_sell.profit=sim.consumer_price-sim.retail_price
			sim_sell.save()
			
			sim.available_item=sim.available_item-1
			sim.save()
			dict_response={"error":False,"message":"Successfully Added Payment"}
		except Exception as e:
			print(e)
			dict_response={"error":True,"message":"Error During Adding Supplier Payment"}

		return JsonResponse(dict_response)
		

@csrf_exempt
def getSimMonthlyLedger(request):

	if request.method=="GET":
		
		unique_month_qs=SimSell.objects.all().annotate(date=TruncMonth('created_at'),).values('date').distinct()
		
		response_data=[]
		for item in unique_month_qs:
			month=item['date'].month
			year=item['date'].year
			all_sim_sell_month_qs=SimSell.objects.filter(created_at__year=year,created_at__month=month,paid_by='company')
			for sim_company in SIM_COMPANIES:
				monthly_company_bill=all_sim_sell_month_qs.filter(sim__company=sim_company[0]).aggregate(Sum('price')).get('price__sum', 0)
				if monthly_company_bill is None:
					monthly_company_bill=0;
					
				sell_count=all_sim_sell_month_qs.filter(sim__company=sim_company[0]).count()
				
				payment=SimCompanyPayment.objects.get_or_create(year=year, month=month,company=sim_company[0])[0]
				
			
				#print(sim_company[0])
				#print(monthly_company_bill)
				#print(calendar.month_name[month])
				#print(payment)
				
				rd_inner={
					
					'month_year':calendar.month_name[month]+', '+str(year),
					'month_num':month,
					'year_num':year,
					'company':sim_company[0],
					'total_bill':monthly_company_bill,
					'sell_count':sell_count,
					'paid':payment.paid,
					'due':monthly_company_bill-payment.paid
				
				
				}
				response_data.append(rd_inner)
		#print(response_data)
				
				
			
		
	
			
		dict_response={"error":False,"message":"Successfully Fetched Data",'data':response_data}
		

		return JsonResponse(dict_response)
		
@csrf_exempt
def saveSimCompanyPayment(request):

	if request.method=="POST":
		try:
			data=json.loads(request.body)
			print(data)
			payment=SimCompanyPayment.objects.get(year=data['year'], month=data['month'],company=data['company'])
			Cash.load().add_cash(int(data['amount']))
			payment.paid=payment.paid+int(data['amount'])
			payment.save()

			
			dict_response={"error":False,"message":"Successfully Added Sim Company Payment"}

		except Exception as e:
			print(e)
			dict_response={"error":True,"message":"Error During Adding Sim Company Payment"}

		return JsonResponse(dict_response)
		