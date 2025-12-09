from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,logout, login as auth_login
from django.contrib import messages
from homofix_app import views
from django.utils import timezone
from .models import Attendance
from datetime import datetime
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView    
from django.urls import reverse_lazy
# from django.views.generic import ListView
# Create your views here.


# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             if user.user_type == "1":
#                 auth_login(request, user)
#                 return redirect('admin_dashboard')
#             elif user.user_type == "2" and user.technician.status == 'Active':
#                 if not request.user.is_authenticated:
#                     auth_login(request, user)
                
#                 return redirect("technician_dashboard")
#             elif user.user_type == "3" and user.support.status == 'Active':
#                 if not request.user.is_authenticated:
#                     auth_login(request, user)

#                 return redirect("support_dashboard")
#             elif user.user_type == "4":
#                 if not request.user.is_authenticated:
#                     auth_login(request, user)
#                 return HttpResponse("Hello, Customer")
#             else:
                
#                 messages.error(request, "Your account is not active.")
#                 return redirect('login')
#         else:
#             # print('Invalid username or password')
#             messages.error(request, "Invalid username or password.")
#             return redirect('login')

#     if request.user.is_authenticated:
#         if request.user.user_type == "1":
#             return redirect('admin_dashboard')
#         elif request.user.user_type == "2":
#             if request.user.technician.status == 'Active':
#                 return redirect('technician_dashboard')
        
#         elif request.user.user_type == "3":
#             if request.user.support.status == 'Active':
#                 return redirect("support_dashboard")
#         else:
#             return HttpResponse('Customer Dashboard')

#     return render(request, 'homofix_app/Authentication/login.html')



# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             if user.user_type == "1":
#                 auth_login(request, user)
#                 return redirect('admin_dashboard')
#             elif user.user_type == "2" and user.technician.status == 'Active':
#                 if not request.user.is_authenticated:
#                     auth_login(request, user)
                
#                 return redirect("technician_dashboard")
#             elif user.user_type == "3" and user.support.status == 'Active':
#                 if not request.user.is_authenticated:
#                     auth_login(request, user)
                
#                 # create and save an Attendance object for the user who logs in
#                 support = user.support
#                 attendance = Attendance.objects.create(support_id=support, login_time=datetime.now())
#                 attendance.save()
                
#                 return redirect("support_dashboard")
#             elif user.user_type == "4":
#                 if not request.user.is_authenticated:
#                     auth_login(request, user)
#                 return HttpResponse("Hello, Customer")
#             else:
#                 messages.error(request, "Your account is not active.")
#                 return redirect('login')
#         else:
#             messages.error(request, "Invalid username or password.")
#             return redirect('login')

#     if request.user.is_authenticated:
#         if request.user.user_type == "1":
#             return redirect('admin_dashboard')
#         elif request.user.user_type == "2":
#             if request.user.technician.status == 'Active':
#                 return redirect('technician_dashboard')
#         elif request.user.user_type == "3":
#             if request.user.support.status == 'Active':
#                 # update the logout_time of the Attendance object for the user who logs out
#                 support = user.support
#                 attendance = Attendance.objects.filter(support_id=support).order_by('-id').first()
#                 if attendance and not attendance.logout_time:
#                     attendance.logout_time = datetime.now()
#                     attendance.save()
                
#                 return redirect("support_dashboard")
#         else:
#             return HttpResponse('Customer Dashboard')

#     return render(request, 'homofix_app/Authentication/login.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.user_type == "1":
                auth_login(request, user)
                return redirect('admin_dashboard')
            elif user.user_type == "2" and user.technician.status == 'Active':
                if not request.user.is_authenticated:
                    auth_login(request, user)
                
                return redirect("technician_dashboard")
            elif user.user_type == "3" and user.support.status == 'Active':
                if not request.user.is_authenticated:
                    auth_login(request, user)
                
                # create and save an Attendance object for the user who logs in
                support = user.support
                attendance = Attendance.objects.create(support_id=support, login_time=datetime.now())
                attendance.save()
                
                return redirect("support_dashboard")
            elif user.user_type == "4":
                if not request.user.is_authenticated:
                    auth_login(request, user)
                return HttpResponse("Hello, Customer")
            else:
                messages.error(request, "Your account is not active.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    if request.user.is_authenticated:
        if request.user.user_type == "1":
            return redirect('admin_dashboard')
        elif request.user.user_type == "2":
            if request.user.technician.status == 'Active':
                return redirect('technician_dashboard')
        elif request.user.user_type == "3":
            if request.user.support.status == 'Active':
                # update the logout_time of the Attendance object for the user who logs out
                support = request.user.support
                attendance = Attendance.objects.filter(support_id=support).order_by('-id').first()
                if attendance and not attendance.logout_time:
                    attendance.logout_time = datetime.now()
                    attendance.save()
                
                return redirect("support_dashboard")
        else:
            return HttpResponse('Customer Dashboard')

    return render(request, 'homofix_app/Authentication/login.html')

# def logout_user(request):
#     logout(request)
#     return redirect("login")



def logout_user(request):
    if request.user.is_authenticated and request.user.user_type == "3":
        try:
            support = request.user.support
            
            attendance_queryset = Attendance.objects.filter(support_id=support, logout_time=None)
            for attendance in attendance_queryset:
                attendance.logout_time = timezone.now()
                attendance.save()

            
        except Attendance.DoesNotExist:
            pass

    logout(request)
    return redirect("login")



class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'password_reset_form.html'

    


class CustomPasswordResetDoneView(PasswordResetDoneView):
   
    template_name = 'password_reset_done.html'



class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'password_reset_confirm.html'



class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'



def Error404(request, exception):
    return render(request,'homofix_app/AdminDashboard/Error/error-404-error.html')