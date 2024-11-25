from django.shortcuts import render,redirect
from orders_app.models import Order_Tb
from authentication.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

@login_required(login_url="/adminpage/")
def order(request):
    all_data = Order_Tb.objects.all()

    paginator = Paginator(all_data,1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'orders_app/order.html',{"page_obj":page_obj,"start_index": page_obj.start_index() - 1})

@login_required(login_url="/adminpage/")
def insertorder(request):

    if request.method == "POST":

        book_title = request.POST['book_title']
        book_author = request.POST['book_author']
        book_isbn = request.POST['book_isbn']
        book_category = request.POST['book_category']
        book_image = request.FILES['book_image']
        book = request.POST['book']

        obj = Order_Tb()
        obj.BOOK_TITLE = book_title
        obj.BOOK_AUTHOR = book_author
        obj.ISBN = book_isbn
        obj.BOOK_CATEGORY = book_category
        obj.BOOK_IMAGE = book_image
        obj.BOOK = book

        obj.save()

        messages.success(request,f' "{obj.BOOK_TITLE}"  Book Successfully Added.')

        return redirect('order')

    return render(request,'orders_app/insert.html')


@login_required(login_url="/adminpage/")
def updateorder(request,id):
    update = Order_Tb.objects.get(id = id)
    if request.method == "POST":
        book_title = request.POST['book_title']
        book_author = request.POST['book_author']
        book_isbn = request.POST['book_isbn']
        book_category = request.POST['book_category']
        book = request.POST['book']

        update.BOOK_TITLE = book_title
        update.BOOK_AUTHOR = book_author
        update.ISBN = book_isbn
        update.BOOK_CATEGORY = book_category
        update.BOOK = book

        if 'book_image' in request.FILES:
            book_image = request.FILES['book_image']
            update.BOOK_IMAGE = book_image

        update.save()

        messages.success(request, f' "{update.BOOK_TITLE}" Book Successfully Updated.')

        return redirect('order')

    return render(request,'orders_app/update.html',{'data':update})

@login_required(login_url="/adminpage/")
def deleteorder(request,id):
    dell = Order_Tb.objects.get(id = id)
    dell.delete()
    messages.success(request,f' "{dell.BOOK_TITLE}"  Book Successfully Deleted.')
    return redirect('order')

@login_required(login_url="/adminpage/")
def customerlist(request):
    alldata=User.objects.all()
    return render (request,'orders_app/customerlist.html',{'data':alldata})

@login_required(login_url="/adminpage/")
def deletecustomer(request,id):
    delcus=User.objects.get(id = id)
    delcus.delete()
    messages.success(request, f' Successfully deleted  "{delcus.username}"  account.')
    return redirect('customerlist')

@login_required(login_url="/adminpage/")
def readbook(request,id):
    order = Order_Tb.objects.get(id=id)  # Retrieve the order using id
    book_value = order.BOOK
    book_title = order.BOOK_TITLE
    book_author = order.BOOK_AUTHOR
    return render(request,'orders_app/book.html',{'book_value':book_value,'book_title':book_title,'book_author':book_author})