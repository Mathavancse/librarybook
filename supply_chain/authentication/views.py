from django.shortcuts import render,redirect
from authentication.models import User
from django.contrib.auth import authenticate,login,logout
from authentication.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required


# Create your views here.
# def one(request):
#     return render(request,'authentication/one.html')
def createaccount(request):
    if request.method == "POST":
        user_mail = User.objects.filter(email=request.POST['email'])
        user_name = User.objects.filter(username=request.POST['username'])

        if user_mail.exists():
            context = {
                'err': "*Email already exists"
            }
            return render(request, 'authentication/createacount.html', context)

        elif user_name.exists():
            context = {
                'error': "*Username already exists"
            }
            return render(request, 'authentication/createacount.html', context)

        else:
            new_user = User(
                username=request.POST['username'],
                CONTACT=request.POST['contact'],
                AGE=request.POST['age'],
                email=request.POST['email'],
            )

            new_user.set_password(request.POST['password'])
            new_user.save()

            messages.success(request, f'"{new_user.username}" Your Account Created Successfully')

            return redirect('login')

    return render(request, 'authentication/createacount.html')

def loginpage(request):

    if request.method == "POST":

        user = authenticate(username = request.POST['username'],password = request.POST['password'])

        if user is not None:

            login(request,user)

            messages.success(request,f' "{user.username}"  Login Successfully')

            return redirect("customers")

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


def emailpage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print("Email:", email)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            print('User exists')

            try:
                send_mail(
                    subject="Reset Your Password",
                    message = f"Hello {user.username}, To reset your password, click on the given link: http://127.0.0.1:8000/newpasswordpage/{user.username}/",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False
                )
                print("Email sent successfully!")
                messages.success(request,f' "{user.username}"  Link Send Your Email Successfully')
            except Exception as e:
                print(f"Error sending email: {e}")

    return render(request, 'authentication/emailpage.html')


def newpassword(request,name):
    username=User.objects.get(username=name)
    print("userid",username)
    if request.method == 'POST':
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        print("pass1 and pass2", pass1 ,"and" ,pass2)

        if pass1 == pass2:
            username.set_password(pass1)  # This method securely sets the password
            username.save()  # Save the user with the new password
            messages.success(request,f' "{username}" Password Changed Successfully')
            return redirect('login') 

        else:
            return render(request, 'authentication/newpassword.html')

    return render (request,'authentication/newpassword.html')