

# Create your models here.
from django.db import models
from accounts.models import User
# Create your models here.
#Expense [title,amount,descritpion,category,priority,payment_method,owner FK (User)]
"""
  CATEGORY_CHOICES = [
        ('FOOD', 'Food'),
        ('TRAVEL', 'Travel'),
        ('SHOPPING', 'Shopping'),
        ('BILLS', 'Bills & Utilities'),
        ('HEALTH', 'Health'),
        ('EDUCATION', 'Education'),
        ('ENTERTAINMENT', 'Entertainment'),
        ('GROCERIES', 'Groceries'),
        ('OTHERS', 'Others'),
    ]
"""


class Expense(models.Model):

    title = models.CharField(max_length=200)

    amount = models.FloatField()

    description = models.TextField(null=True)

    CATEGORY_CHOICES = [
        ('Food', 'food'),
        ('Travel', 'Travel'),
        ('Shopping', 'Shopping'),
        ('Bills', 'Bills'),
        ('Health', 'Health'),
        ('Education', 'Education'),
        ('Entertainment', 'Entertainment'),
        ('Groceries', 'Groceries'),
        ('Others', 'Others'),
    ]

    PRIORITY_CHOICES=[
        ("Need","Need"),
        ("Want","Want")
    ]

    PAYMENT_METHOD_CHOICES=[
        ("Cash","Cash"),
        ("Upi","Upi")
    ]

    category = models.CharField(max_length=200,choices=CATEGORY_CHOICES,default="Others")

    priority = models.CharField(max_length=120,choices=PRIORITY_CHOICES,default="Need")

    payment_method = models.CharField(max_length=120,choices=PAYMENT_METHOD_CHOICES,default="upi")

    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="expenses")
    
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):

        return self.title