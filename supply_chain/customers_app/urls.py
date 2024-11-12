"""
URL configuration for supply_chain project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from customers_app import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('customers/<str:username>/',views.customer,name='customers'),
    path('customerdetail/',views.customerdetails,name='customerdetail'),
    path('customerdetailupdate/',views.customerdetailupdate,name='customerdetailupdate'),
    path('customerdeleted/',views.deleteyou,name='deleteaccount'),
    path('openbook/<str:BOOK_TITLE>/', views.openbook, name='openbook'),

]