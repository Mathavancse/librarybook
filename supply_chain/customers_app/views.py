from django.shortcuts import render,redirect,get_object_or_404
from orders_app.models import Order_Tb
from authentication.models import User
from django.contrib import messages

# Create your views here.
def customer(request,username):
    user = Order_Tb.objects.all()
    return render(request,'customers_app/customer.html',{'username':username,"user":user})

def customerdetails(request):
    user=request.user

    return  render(request,'customers_app/customerdetail.html',{'user':user})

def customerdetailupdate(request):
    update=request.user

    if request.method == "POST":
        username=request.POST['username']
        age= request.POST['age']
        email=request.POST['email']
        contact=request.POST['contact']

        update.username=username
        update.AGE = age
        update.email = email
        update.CONTACT = contact
        
        update.save()

        messages.success(request,f' "{update.username}"  Successfully Updated.')
        
        return redirect('customerdetail')

    return render(request,'customers_app/customerdetailupdate.html',{'user':update})

def deleteyou(request):
    delmy=request.user
    delmy.delete()
    messages.success(request,f' "{delmy}"  Your Account Deleted Successfully.')
    return redirect ('login')

from orders_app.models import Order_Tb

def study(request, BOOK_TITLE):
    order = Order_Tb.objects.get(BOOK_TITLE=BOOK_TITLE)  # Retrieve the order using id
    book_value = order.BOOK  # Get the BOOK field from that order instance
    book_title = order.BOOK_TITLE
    return render(request, 'customers_app/openbook.html', {'book_value': book_value,'book_title':book_title})



