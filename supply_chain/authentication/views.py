from django.shortcuts import render,redirect
from authentication.models import User
from django.contrib.auth import authenticate,login,logout
from authentication.models import User
from django.contrib import messages
# Create your views here.
# def one(request):
#     return render(request,'authentication/one.html')

def createaccount(request):

    if request.method == "POST":

        user_check = User.objects.filter(username=request.POST['username'])

        if user_check.exists():

            context = {
                'error':"*Name already exists"
            }

            return render(request,'authentication/createacount.html',context)

        else:

            new_user = User(
            username=request.POST['username'],
            CONTACT=request.POST['contact'],
            AGE=request.POST['age'],
            email=request.POST['email'],
            )

            new_user.set_password(request.POST['password'])

            new_user.save()

            messages.success(request,f' "{new_user}"  Your Account Created Successfully')

            return redirect('login')

    return render(request,'authentication/createacount.html')

def loginpage(request):

    if request.method == "POST":

        user = authenticate(username = request.POST['username'],password = request.POST['password'])

        if user is not None:

            login(request,user)

            request.session['username'] = user.username

            messages.success(request,f' "{user.username}"  Login Successfully')

            return redirect("customers",username=user.username)

        else:
            context={
                "error":"* Incorrect Username or Password *"
            }


            return render(request,'authentication/login.html',context)

    return render(request,'authentication/login.html')

def logoutpage(request):
    username = request.user.username  # Get the username before logging out
    logout(request)
    messages.success(request, f' "{username}"  Logout successfully.')
    return redirect('login')


def adminpage(request):
    if request.method == 'POST':

        admin_username ='admin'   #adminlogin password =admin1 name=admin

        if admin_username == request.POST['username']:

            user_admin = authenticate(username = request.POST['username'],password = request.POST['password'])

            if user_admin is not None:

                login(request,user_admin)

                messages.success(request,' "Admin"  Login Successfully')


                return redirect('order')

        else:
          context={
                "error":"*incorrect username or password"
          }

        return render(request,'authentication/adminlogin.html',context)


    return render(request,'authentication/adminlogin.html')


