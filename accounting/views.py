from datetime import datetime, timedelta
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


from accounting.models import AccountCategory, Account, Transaction

from accounting.serializers import AccountCategorySerializers, AccountSerializers, TransactionSerializers

# Create your views here.


class TransactionViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request):
        transactions=Transaction.objects.all().order_by('-id')
        serializer=TransactionSerializers(transactions,many=True,context={"request":request})
        #print(serializer.data)
        response_dict={"error":False,"message":"All Company List Data","data":serializer.data}
        return Response(response_dict)


    def create(self,request):
        try:
            #serializer=SupplierSerliazer(data=request.data,context={"request":request})
            #serializer.is_valid(raise_exception=True)
            #serializer.save()
            print("here")
            transactions=request.data
            print(request.data)
            for tnx in transactions:
                transaction=Transaction()
                account=Account.objects.get(id=tnx['account_id'])
                transaction.account=account


                transaction.tnx_type=tnx['transaction_type']
                transaction.amount=tnx['transaction_amount']
                transaction.tnx_description=tnx['transaction_description']
                transaction.save()


            dict_response={"error":False,"message":"Transaction Data Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Transaction Data"}
        return Response(dict_response)




class AccountViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request):
        accounts=Account.objects.all()
        serializer=AccountSerializers(accounts,many=True,context={"request":request})
        #print(serializer.data)
        response_dict={"error":False,"message":"All Account List Data","data":serializer.data}
        return Response(response_dict)


class AccountCategoryViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request):
        ac=AccountCategory.objects.all()
        serializer=AccountCategorySerializers(ac,many=True,context={"request":request})
        print(serializer.data)
        response_dict={"error":False,"message":"All Account List Data","data":serializer.data}
        return Response(response_dict)
