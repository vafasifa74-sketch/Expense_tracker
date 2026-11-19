from django.shortcuts import render,get_object_or_404

# Create your views here.
from rest_framework.views import APIView
from rest_framework import authentication,permissions
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView

from transactions.models import Expense
from transactions.serializers import ExpenseSerializer
from accounts.permissions import Isowner

from datetime import datetime
from django.db.models import Sum
from transactions.aiengine import scan_bill
class ExpenseListCreateView(ListCreateAPIView):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes =[permissions.IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user)

    """def get(self,request):

        qs = Expense.objects.filter(owner = request.user) # fetching current user Expenses (get all expenses)

        serializer_instance = ExpenseSerializer(qs,many=True)

        return Response(serializer_instance.data)"""

    def post(self,request):

        form_data =request.data

        serializer_instance = ExpenseSerializer(data = form_data)

        if serializer_instance.is_valid():

            serializer_instance.save(owner=request.user)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

class ExpenseRetriveUpdateDeleteView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [Isowner]

    def get(self,request,pk=None):
      

        qs = get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,qs)

        serializer_instance = ExpenseSerializer(qs)

        return Response(data=serializer_instance.data)

    def put(self,request,pk=None):

        form_data = request.data

        expense_object= get_object_or_404(Expense,id =pk)

        self.check_object_permissions(request,expense_object)

        serializer_instance = ExpenseSerializer(data=form_data,instance=expense_object)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)

        else:
            return Response(data=serializer_instance.errors)
            
    def delete (self,request,pk=None):
         
        expense_object = get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,expense_object)

        expense_object.delete()

        response_data = {"message":"deleted...."}

        return Response(data=response_data)

           

class ExpenseSummaryView(APIView):

    authentication_classes =[authentication.TokenAuthentication]
    
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        auth_user_expenses = Expense.objects.filter(owner=request.user)

        response_data = {
            "monthly_total":0,
            "todays_total":0
        }

        cur_month = datetime.now().month

        cur_yearr = datetime.now().year

        monthly_total = auth_user_expenses.filter(created_at__month =cur_month
                                  , created_at__year = cur_yearr).values("amount").aggregate(total = Sum("amount")).get("total")

        
        response_data ["monthly_total"] = monthly_total

        category_summary = auth_user_expenses.filter(created_at__month = cur_month,
                                                     created_at__year=cur_yearr).values("category").annotate(total=Sum("amount"))

        response_data["monthly_category_summary"]=category_summary
        

        # today 
        
        today = datetime.now().date()

        print(today)

        today_total = auth_user_expenses.filter(created_at__date = today).values("amount").aggregate(total=Sum("amount")).get("total")

        response_data ["todays_total"] =today_total

        return Response(response_data)


class ScanBillView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes =[permissions.IsAuthenticated]

    def post(self,request):

        bill_image = request.FILES.get("bill_image")

        if not bill_image:

            return Response({"message":" bill_image is not found.."})

        else:
           
           try:
                data = scan_bill(bill_image)
                """
                           {"amount":5770.0,"category":"Shopping","payment_method":null,"title":"NARAYANI READYMADE STORES"}
                """
                Expense.objects.create(title=data.get("title"),
                category=data.get("category"),
                               amount=data.get("amount"),
                               owner=request.user
                           )
               
                           
                return Response(data)
           
           except Exception as e:

               return Response ({"message":e})
               



            
        
        


            


       
    


