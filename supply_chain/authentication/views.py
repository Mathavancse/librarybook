from django.shortcuts import render,redirect
from authentication.models import User
from django.contrib.auth import authenticate,login,logout
from authentication.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

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
        username = request.POST['username']
        password = request.POST['password']

        # Check if the username exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, "* User Does Not Exist *")
            return render(request, 'authentication/login.html')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'"{user.username}" Login Successfully')
            return redirect("customers")
        else:
            messages.warning(request, "* Incorrect Password *")
            return render(request, 'authentication/login.html')

    return render(request, 'authentication/login.html')



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

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

def emailpage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print("Email:", email)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            print('User exists')
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            current_site = get_current_site(request) #127.0.0.1:8000
            domain = current_site.domain

            try:
                send_mail(
                    subject="Reset Your Password",
                    message = render_to_string('resetpasswordemail.html',{
                        "domain":domain,
                        "uid" : uid,
                        "token":token
                    }),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False
                )
                print("Email sent successfully!")
                messages.success(request,f'Link Send Your Gmail')
            except Exception as e:
                print(f"Error sending email: {e}")

    return render(request, 'authentication/emailpage.html')


def newpassword(request, uidb64, token):
    try:
        # Decode the user ID from uidb64
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')

            if pass1 == pass2:
                user.set_password(pass1)  # Securely set the new password
                user.save()
                messages.success(request, f"Password changed successfully!")
                return redirect('login')  # Redirect to login page after successful password change
            else:
                messages.error(request, "Passwords do not match. Please try again.")
                return render(request, 'authentication/newpassword.html', {"validlink": True})
        
        # Render form for password reset
        return render(request, 'authentication/newpassword.html', {"validlink": True})
    else:
        # Invalid token or link
        messages.error(request, "The password reset link is invalid, expired, or already used.")
        return render(request, 'authentication/newpassword.html', {"validlink": False})












# only the link exists for five minutes

# from django.utils.timezone import now
# import time

# def emailpage(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         print("Email entered:", email)

#         if User.objects.filter(email=email).exists():
#             user = User.objects.get(email=email)
#             print('User exists')
#             token = default_token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.id))
#             timestamp = int(time.time())  # Current timestamp in seconds
#             current_site = get_current_site(request)
#             domain = current_site.domain

#             try:
#                 send_mail(
#                     subject="Reset Your Password",
#                     message=render_to_string('resetpasswordemail.html', {
#                         "domain": domain,
#                         "uid": uid,
#                         "token": token,
#                         "timestamp": timestamp  # Include the timestamp
#                     }),
#                     from_email=settings.EMAIL_HOST_USER,
#                     recipient_list=[email],
#                     fail_silently=False
#                 )
#                 print("Email sent successfully!")
#                 messages.success(request, f'Password reset link sent to your email.')
#             except Exception as e:
#                 print(f"Error sending email: {e}")
#                 messages.error(request, f"Failed to send email. Please try again later.")

#     return render(request, 'authentication/emailpage.html')




# import time

# def newpassword(request, uidb64, token, timestamp):
#     try:
#         # Decode the user ID from uidb64
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     # Check if the token and timestamp are valid
#     if user is not None and default_token_generator.check_token(user, token):
#         current_time = int(time.time())  # Current timestamp
#         token_age = current_time - int(timestamp)  # Calculate the token age in seconds

#         if token_age > 300:  # 300 seconds = 5 minutes
#             messages.error(request, "The password reset link has expired.")
#             return render(request, 'authentication/newpassword.html', {"validlink": False})

#         if request.method == 'POST':
#             pass1 = request.POST.get('pass1')
#             pass2 = request.POST.get('pass2')

#             if pass1 == pass2:
#                 user.set_password(pass1)  # Securely set the new password
#                 user.save()
#                 messages.success(request, "Password changed successfully!")
#                 return redirect('login')  # Redirect to login page after successful password change
#             else:
#                 messages.error(request, "Passwords do not match. Please try again.")
#                 return render(request, 'authentication/newpassword.html', {"validlink": True})

#         # Render form for password reset
#         return render(request, 'authentication/newpassword.html', {"validlink": True})
#     else:
#         # Invalid token or link
#         messages.error(request, "The password reset link is invalid or already used.")
#         return render(request, 'authentication/newpassword.html', {"validlink": False})


# <p>Click the link below to reset your password. This link is valid for 5 minutes only:</p>
# <a href="http://{{ domain }}/reset-password/{{ uid }}/{{ token }}/{{ timestamp }}">Reset Password</a>

# path('newpasswordpage/<uidb64>/<token>/<timestamp>', views.newpassword, name='newpassword'),

