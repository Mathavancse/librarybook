from django.shortcuts import render,redirect,get_object_or_404
from orders_app.models import Order_Tb
from authentication.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.

@login_required(login_url="/loginpage/")
def customer(request,username):
    all_user = Order_Tb.objects.all()

    paginator = Paginator(all_user,1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'customers_app/customer.html',{'username':username,"page_obj":page_obj,"start_index": page_obj.start_index() - 1})

@login_required(login_url="/loginpage/")
def customerdetails(request):
    user=request.user

    return  render(request,'customers_app/customerdetail.html',{'user':user})

@login_required(login_url="/loginpage/")
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

@login_required(login_url="/loginpage/")
def deleteyou(request):
    delmy=request.user
    delmy.delete()
    messages.success(request,f' "{delmy}"  Your Account Deleted Successfully.')
    return redirect ('login')

from orders_app.models import Order_Tb

@login_required(login_url="/loginpage/")
def study(request, id):
    order = Order_Tb.objects.get(id=id)  # Retrieve the order using id
    book_value = order.BOOK  # Get the BOOK field from that order instance
    book_title = order.BOOK_TITLE
    book_author = order.BOOK_AUTHOR
    return render(request, 'customers_app/openbook.html', {'book_value': book_value,'book_title':book_title,'book_author':book_author})



