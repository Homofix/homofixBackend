from django.shortcuts import render,redirect
from homofix_app.models import *
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView    
from django.urls import reverse_lazy
# Create your views here.


def admin_reset_psw(request):
   
    id = request.user.id
    print("iddd",id)
    if request.method == "POST":
        old_psw = request.POST.get('old_psw')
        new_psw = request.POST.get('new_psw')
        confirm_psw = request.POST.get('confirm_psw')
        # id = request.user.id
        user = CustomUser.objects.get(id=id)
        
        if old_psw and new_psw:
            if user.check_password(old_psw):
                if new_psw == confirm_psw:
                    if old_psw == new_psw:
                        messages.error(request, 'New password must be different from the old password')
                        return redirect('admin_reset_psw')
                    else:
                        user.set_password(new_psw)
                        user.save()
                        messages.success(request,'Password successfully changed')
                        return redirect('admin_reset_psw')
                else:
                    messages.error(request, 'Passwords do not match')
                    return redirect('admin_reset_psw')
            else:
                messages.error(request, 'Old password is incorrect')
                return redirect('admin_reset_psw')
    return render(request, 'accounts/reset_psw.html')
    # return render(request, 'homofix_app/Authentication/reset_psw.html')
 

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

