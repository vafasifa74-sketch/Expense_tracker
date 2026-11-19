"""
URL configuration for spendwise project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from accounts.views import SignUpView
from rest_framework.authtoken.views import ObtainAuthToken
from accounts.views import AuthDetailView

from transactions.views import ExpenseListCreateView
from transactions.views import ExpenseRetriveUpdateDeleteView

from transactions.views import ExpenseSummaryView
from transactions.views import ScanBillView

urlpatterns = [

    #accounts
    path('admin/', admin.site.urls),
    path("accounts/register/",SignUpView.as_view()),
    path("accounts/token/",ObtainAuthToken.as_view()),
    path("accounts/me/",AuthDetailView.as_view()),

    #transactions , Expense
    path("expense/",ExpenseListCreateView.as_view()),
    path("expense/<int:pk>/",ExpenseRetriveUpdateDeleteView.as_view()),
    path("expense/summary/",ExpenseSummaryView.as_view()),

    path("bill/scan/",ScanBillView.as_view()),
]
