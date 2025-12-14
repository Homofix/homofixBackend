from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
# from django.contrib.auth.decorators import login_required
from .models import CustomUser,Category,Technician,Product,SpareParts,Support,FAQ,Booking,Task,STATE_CHOICES,SubCategory,Rebooking,ContactUs,JobEnquiry,HodSharePercentage,Customer,Share,Payment,Addon,Wallet,WalletHistory,TechnicianLocation,AdminHOD,AllTechnicianLocation,BookingProduct,WithdrawRequest,RechargeHistory,Attendance,Coupon,Kyc,Blog,Offer,MostViewed,HomePageService,Carrer,ApplicantCarrer,LegalPage,Invoice,Payment,Settlement,feedback,Pincode,UniversalCredential,AutoAssignSetting,SLOT_CHOICES,Slot,showonline
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import random
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.utils import timezone
from urllib.parse import urlencode
import datetime
from django.http import Http404
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter,A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER,TA_LEFT,TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph,Image
from django.conf import settings
from decimal import Decimal
from django.db.models import Sum
from reportlab.lib.styles import getSampleStyleSheet

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
import pdfkit
from django.template.loader import render_to_string
from django.db.models import Avg
import requests
from django.utils import timezone

from django.http import JsonResponse
from utils.firebase import send_push_notification
from django.core.paginator import Paginator

# def all_location(request):
#     all_location = AllTechnicianLocation.objects.all()
   
#     context = {
#         'technician':all_location
#     }
   
   
#     return render(request, 'all_loaction.html', context)

def all_location(request):
    all_locations = AllTechnicianLocation.objects.all()

    # Create a list of markers for each technician location
    markers = []
    for location in all_locations:
        marker = f"markers=color:red%7C{location.latitude},{location.longitude}"
        markers.append(marker)

    # Combine the markers into a single string
    markers_str = '&'.join(markers)

    # Generate the Google Map iframe URL with the markers
    map_url = f"https://www.google.com/maps/embed/v1/view?key=YOUR_API_KEY_HERE&center={all_locations[0].latitude},{all_locations[0].longitude}&zoom=10&{markers_str}"

    context = {
        'map_url': map_url
    }

    return render(request, 'all_location.html', context)


    # return render(request,'all_loaction.html')
# @login_required


# def admin_dashboard(request):
   
#     fedback = feedback.objects.all()
#     booking = Booking.objects.filter(status="New").order_by('-id')[:10]

#     new_expert_count = Technician.objects.filter(status="New").count()
#     booking_count = Booking.objects.filter(status = "New").count()
#     booking_complete = Booking.objects.filter(status = "Completed").count()
#     rebooking_count = Rebooking.objects.all().count()
#     customer_count = Customer.objects.all().count()
#     total_hod_share = Share.objects.aggregate(Sum('company_share'))['company_share__sum'] or 0
    
    
#     return render(request,'homofix_app/AdminDashboard/dashboard.html',{'booking_count':booking_count,'new_expert_count':new_expert_count,'rebooking_count':rebooking_count,'customer_count':customer_count,'booking_complete':booking_complete,'total_hod_share':total_hod_share,'booking':booking,'fedback':fedback})


from datetime import datetime, timedelta
from django.db.models import Count, Avg, Sum, Q, Prefetch
from django.db.models.functions import TruncDay
from django.utils.timezone import make_aware

# def admin_dashboard(request):
#     # Current date
#     today = datetime.today()

#     # Calculate the first and last day of the previous month
#     # first_day_of_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
#     # last_day_of_last_month = today.replace(day=1) - timedelta(days=1)
#     first_day_of_last_month = make_aware(datetime(today.year, today.month - 1, 1)) if today.month > 1 else make_aware(datetime(today.year - 1, 12, 1))
#     last_day_of_last_month = make_aware(datetime(today.year, today.month, 1)) - timedelta(seconds=1)

#     print("first day of last month",first_day_of_last_month)
#     print("Last day of last month",last_day_of_last_month)

#     # Filter completed bookings for last month
#     completed_bookings_last_month = Booking.objects.filter(
#         status="Completed",
#         booking_date__gte=first_day_of_last_month,
#         booking_date__lte=last_day_of_last_month
#     )
#     average_completed_bookings = completed_bookings_last_month.aggregate(Avg('id'))['id__avg']


#     # Group by day and count bookings
#     daily_booking_counts = completed_bookings_last_month.annotate(
#         day=TruncDay('booking_date')
#     ).values('day').annotate(
#         daily_count=Count('id')
#     )

   
#     average_daily_count = int(daily_booking_counts.aggregate(
#     avg_count=Avg('daily_count')
#     )['avg_count'] or 0)

#     print("gggggggggoooooooooo",average_daily_count)

#     # Fetch existing data
#     fedback = feedback.objects.all()
#     booking = Booking.objects.filter(status="New").order_by('-id')[:10]
#     new_expert_count = Technician.objects.filter(status="New").count()
#     booking_count = Booking.objects.filter(status="New").count()
#     booking_complete = Booking.objects.filter(status="Completed").count()
#     rebooking_count = Rebooking.objects.all().count()
#     customer_count = Customer.objects.all().count()
#     total_hod_share = Share.objects.aggregate(Sum('company_share'))['company_share__sum'] or 0

    # completed_bookings = Booking.objects.filter(status='Completed')
    # total_gross_amount = sum(booking.final_amount for booking in completed_bookings)
    

#     # Render template with additional data for average count
#     return render(request, 'homofix_app/AdminDashboard/dashboard.html', {
#         'booking_count': booking_count,
#         'new_expert_count': new_expert_count,
#         'rebooking_count': rebooking_count,
#         'customer_count': customer_count,
#         'booking_complete': booking_complete,
#         'total_hod_share': total_hod_share,
#         'booking': booking,
#         'fedback': fedback,
#         'average_daily_count': average_daily_count,
#         'total_gross_amount': total_gross_amount,
#     })





def admin_dashboard(request):
    today = datetime.today()

    # First & Last day of last month
    if today.month > 1:
        first_day = make_aware(datetime(today.year, today.month - 1, 1))
    else:
        first_day = make_aware(datetime(today.year - 1, 12, 1))
    last_day = make_aware(datetime(today.year, today.month, 1)) - timedelta(seconds=1)

    # Filter completed bookings once and reuse it
    completed_qs = Booking.objects.filter(status="Completed", booking_date__range=(first_day, last_day))

    # Daily count average
    daily_counts = completed_qs.annotate(day=TruncDay('booking_date')) \
                               .values('day') \
                               .annotate(daily_count=Count('id'))

    average_daily_count = int(daily_counts.aggregate(avg=Avg('daily_count'))['avg'] or 0)

    # Dashboard metrics
    booking_new_qs = Booking.objects.filter(status="New")
    booking_completed_qs = Booking.objects.filter(status="Completed")

    total_gross_amount = Booking.objects.filter(status='Completed').aggregate(
        total=Sum('final_amount_field')
    )['total'] or 0

    query = request.GET.get('q', '')

    feedback_qs = feedback.objects.all()
    if query:
        feedback_qs = feedback_qs.filter(
            Q(description__icontains=query)
            | Q(customer_id__admin__first_name__icontains=query)
            | Q(technician_id__admin__username__icontains=query)
            | Q(technician_id__expert_id__icontains=query)
            | Q(booking_id__order_id__icontains=query)
        )

    feedback_list = feedback_qs.order_by('-id')
    paginator = Paginator(feedback_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'booking': booking_new_qs.order_by('-id')[:10],
        'booking_count': booking_new_qs.count(),
        'booking_complete': booking_completed_qs.count(),
        'new_expert_count': Technician.objects.filter(status="New").count(),
        'rebooking_count': Rebooking.objects.count(),
        'customer_count': Customer.objects.count(),
        'total_hod_share': Share.objects.aggregate(total=Sum('company_share'))['total'] or 0,
        'average_daily_count': average_daily_count,
        'total_gross_amount': total_gross_amount,
        'page_obj': page_obj,
        'q': query
        
        
    }

    return render(request, 'homofix_app/AdminDashboard/dashboard.html', context)


def admin_profile(request):
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'customer_count':customer_count,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        
    }
    return render(request,'homofix_app/AdminDashboard/profile.html',context)


def add_admin(request):
    if request.method == "POST":
        random_number = random.randint(0, 999)
        unique_number = str(random_number).zfill(3)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        print("email",email)
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        print(first_name,last_name,email,mobile,password)
        # if AdminHOD.objects.filter(mobile = mobile,admin__email=email).exists():
        #     return JsonResponse({'status': 'error', 'message': 'Mobile Number is already Taken'})
          
        # if AdminHOD.objects.filter(Q(mobile=mobile) | Q(admin__email=email)).exists():
        #     if AdminHOD.objects.filter(mobile=mobile).exists():
        #         return JsonResponse({'status': 'error', 'message': 'Mobile Number is already taken'})
        #     else:
        #         return JsonResponse({'status': 'error', 'message': 'Email is already taken'})
        if AdminHOD.objects.filter(Q(mobile=mobile) | Q(admin__email=email)).exists():
            if AdminHOD.objects.filter(mobile=mobile, admin__email=email).exists():
                return JsonResponse({'status': 'error', 'message': 'Mobile Number and Email are already taken'})
            elif AdminHOD.objects.filter(mobile=mobile).exists():
                return JsonResponse({'status': 'error', 'message': 'Mobile Number is already taken'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Email is already taken'})

        user = CustomUser.objects.create(first_name=first_name,last_name=last_name,username=first_name+unique_number,email=email,user_type='1')
        user.set_password(password)
        user.adminhod.mobile = mobile
        user.save()
        return JsonResponse({'status':'Save'})
    # else:
    #     return JsonResponse({'status':'error'})

        
    return render(request,'homofix_app/AdminDashboard/Admin/create_admin.html')

def edit_admin(request,id):
    hod = AdminHOD.objects.get(id=id)
    
    
    
    context = {
        'hod':hod
    }
       
        
        # first_name = request.POST.get('first_name')
        

    return render(request,'homofix_app/AdminDashboard/Admin/edit_admin.html',context)
    
def delete_admin(request,id):
    admin_id = AdminHOD.objects.get(id=id)
    admin_id.delete()
    return redirect('admin_list')
def update_admin(request):

    if request.method == "POST":  
        print("helloo posting")

        hod_id = request.POST.get('hod_id')
        print("hodddid",hod_id)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')

        hod = CustomUser.objects.get(id=hod_id)
        hod.first_name = first_name
        hod.last_name = last_name
        hod.email = email
        hod.adminhod.mobile = mobile
        print("testinggg",first_name,last_name,email,mobile)
        hod.save()
        messages.success(request,'Admin updated successfully')
        return redirect('admin_list')

def admin_list(request):
    hod = AdminHOD.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'hod':hod,
        'new_expert_count':new_expert_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
    }
    return render(request,'homofix_app/AdminDashboard/Admin/list_of_admin.html',context)
def admin_update_profile(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # if CustomUser.objects.filter(username = username).exists():
        #     return JsonResponse({'status': 'error', 'message': 'Username is already Taken'})
          
        id = request.user.id
        user = CustomUser.objects.get(id=id)
        # user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        print("success")
        return JsonResponse({'status':'Save'})
    else:
        print("erorrrrr")
        
    return render(request,'homofix_app/AdminDashboard/profile.html')

def category(request):
    q = request.GET.get('q', '').strip()
    category_qs = Category.objects.all()
    if q:
        category_qs = category_qs.filter(category_name__icontains=q)

    paginator = Paginator(category_qs.order_by('category_name'), 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    new_expert_count = Technician.objects.filter(status="New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()

    context = {
        'page_obj': page_obj,
        'search_query': q,
        'new_expert_count': new_expert_count,
        'rebooking_count': rebooking_count,
        'customer_count': customer_count,
    }
    return render(request,'homofix_app/AdminDashboard/Category/category.html',context)

def add_category(request):
    if request.method == "POST":
        
        category_name = request.POST.get('category_name')
        category_img = request.FILES.get('category_img')
        
        
        
        if Category.objects.filter(category_name = category_name).exists():
            # return JsonResponse({'status': 'error', 'message': 'Category is already Taken'})
            messages.warning(request,f'{category_name} already Exists')
            return redirect('category')
            
        category = Category.objects.create(category_name=category_name,icon=category_img)
        category.save()
        messages.success(request,f'{category_name} Add Successfully')
        return redirect('category')
       
        
        # return JsonResponse({'status':'Save','cat_Data':cat_Data})


def delete_Category(request,id):
    category = Category.objects.get(id=id)
    category.delete()
    messages.success(request,"Records are Successfully Deleted")
    return redirect('category')

def edit_Category(request):
    if request.method == "POST":
        category_id = request.POST.get('category_id')
        category_img = request.FILES.get('category_img')
        
        category_name = request.POST.get('category_name')
        category = Category.objects.get(id=category_id) 
        category.category_name = category_name
        category.icon = category_img
        category.save()
        messages.success(request,"Records are Updated Successfully")
        return redirect('category')

def subcategory(request):
    q = request.GET.get('q', '').strip()
    category = Category.objects.all()
    sub_category_qs = SubCategory.objects.all()
    if q:
        sub_category_qs = sub_category_qs.filter(name__icontains=q)
    paginator = Paginator(sub_category_qs.order_by('name'), 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    if request.method == 'POST':
        category_id = request.POST.get('category_id')

        
        subcategory_image = request.FILES.get('subcategory_image')
        subcategory_names = request.POST.get('subcategory_name')
        ctg_id = Category.objects.get(id=category_id)
        subcategory = SubCategory.objects.create(Category_id=ctg_id, name=subcategory_names,subcategory_image=subcategory_image)
        subcategory.save()
        

        
        # for name in subcategory_names:
        #     subcategory = SubCategory.objects.create(Category_id=ctg_id, name=name)
        #     subcategory.save()
            

    context = {
        'category':category,
        'page_obj': page_obj,
        'search_query': q,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count
    }
    
    return render(request,'homofix_app/AdminDashboard/Subcategory/sub_category.html',context)
def edit_subcategory(request):
    if request.method == "POST":
        category_id = request.POST.get('category_id')
        sub_category_id = request.POST.get('sub_category_id')
        sub_category_image = request.FILES.get('sub_category_image')
        sub_category_name = request.POST.get('sub_category_name')

        category = Category.objects.get(id=category_id)
        
        subcategory = SubCategory.objects.get(id=sub_category_id) 
        subcategory.Category_id= category
        subcategory.name= sub_category_name
        if sub_category_image:
            subcategory.subcategory_image= sub_category_image
        subcategory.save()
        messages.success(request,"Records are Updated Successfully")
        return redirect('subcategory')
def delete_subcategory(request,id):
    subcategory = SubCategory.objects.get(id=id)
    subcategory.delete()
    messages.success(request,"Deleted")
    return redirect('subcategory')



def technician(request):
    category = Category.objects.all()
    technician = Technician.objects.all()
    # user_status = {}
    # for user in technician:
    #     # check if user is logged in by looking at their last login time
    #     if user.admin.last_login is not None and timezone.now() - user.admin.last_login < timezone.timedelta(seconds=1):
    #         # user is online
    #         user_status[user.id] = 'online'
    #     else:
    #         # user is offline
    #         user_status[user.id] = 'offline'
    # print("user status",user_status)
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    if request.method == "POST":
        
        category_id = request.POST.get('category_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

       

        ctg = Category.objects.get(id=category_id)
        
      
        if CustomUser.objects.filter(username = username).exists():
            # return JsonResponse({'status': 'error', 'message': 'Username is already Taken'})
            messages.error(request,'Username is already Taken')
            return redirect('technician')
            
        user = CustomUser.objects.create_user(username=username,password=password,email=email,user_type='2')
        user.technician.category = ctg
        user.save()
        messages.success(request,'Technician Register Successfully')
        # if(user.is_active):
        #     return JsonResponse({'status':'Save'})
            
        # else:
        #     return JsonResponse({'status':0})

    return render(request,'homofix_app/AdminDashboard/Technician/technician.html',{'category':category,'technician':technician,'new_expert_count':new_expert_count,'booking_count':booking_count,'rebooking_count':rebooking_count,'customer_count':customer_count})




# def technician(request):
#     category = Category.objects.all()
#     q = request.GET.get('q', '').strip()
#     technician_qs = Technician.objects.all().order_by('-id')
#     if q:
#         technician_qs = technician_qs.filter(
#             Q(admin__first_name__icontains=q) |
#             Q(admin__last_name__icontains=q) |
#             Q(admin__username__icontains=q) |
#             Q(mobile__icontains=q) |
#             Q(subcategories__name__icontains=q)
#         ).distinct()
#     paginator = Paginator(technician_qs, 10)
#     page = request.GET.get('page')
#     page_obj = paginator.get_page(page)

#     # user_status = {}
#     # for user in technician:
#     #     # check if user is logged in by looking at their last login time
#     #     if user.admin.last_login is not None and timezone.now() - user.admin.last_login < timezone.timedelta(seconds=1):
#     #         # user is online
#     #         user_status[user.id] = 'online'
#     #     else:
#     #         # user is offline
#     #         user_status[user.id] = 'offline'
#     # print("user status",user_status)
#     new_expert_count = Technician.objects.filter(status="New").count()
#     booking_count = Booking.objects.filter(status = "New").count()
#     rebooking_count = Rebooking.objects.all().count()
#     customer_count = Customer.objects.all().count()
#     if request.method == "POST":
        
#         category_id = request.POST.get('category_id')
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')

       

#         ctg = Category.objects.get(id=category_id)
        
      
#         if CustomUser.objects.filter(username = username).exists():
#             # return JsonResponse({'status': 'error', 'message': 'Username is already Taken'})
#             messages.error(request,'Username is already Taken')
#             return redirect('technician')
            
#         user = CustomUser.objects.create_user(username=username,password=password,email=email,user_type='2')
#         user.technician.category = ctg
#         user.save()
#         messages.success(request,'Technician Register Successfully')
#         # if(user.is_active):
#         #     return JsonResponse({'status':'Save'})
            
#         # else:
#         #     return JsonResponse({'status':0})

#     return render(request,'homofix_app/AdminDashboard/Technician/technician.html',{'category':category,'technician':technician,'new_expert_count':new_expert_count,'booking_count':booking_count,'rebooking_count':rebooking_count,'customer_count':customer_count,'page_obj': page_obj,'search_query': q})




def add_technician(request):
    
    category = Category.objects.all()
    subcategory = SubCategory.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    if request.method == "POST":
        random_number = random.randint(0, 999)
        unique_number = str(random_number).zfill(3)
        
        sub_category_id = request.POST.getlist('sub_category_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        subcat = SubCategory.objects.filter(id__in=sub_category_id)
        user = CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=first_name+unique_number,password=password,email=email,user_type='2')
        user.technician.subcategories.set(subcat)
        user.save()
        messages.success(request,'Technician Register Successfully')
        return redirect('technician')
       

    context = {
        'category':category,
        'subcategory':subcategory,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
    }
    return render(request,'homofix_app/AdminDashboard/Technician/add_technician.html',context)

def technician_add_category(request):
    if request.method == "POST":
        
        category_name = request.POST.get('category_name')
        
        
        
        if Category.objects.filter(category_name = category_name).exists():
            # return JsonResponse({'status': 'error', 'message': 'Category is already Taken'})
            messages.warning(request,f'{category_name} already Exists')
            return redirect('technician')
            
        category = Category.objects.create(category_name=category_name)
        category.save()
        messages.success(request,f'{category_name} Add Successfully')
        return redirect('technician')



def technician_edit_profile(request,id):
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    technician = Technician.objects.get(id=id)
    state_choices = STATE_CHOICES
    sub_cat = SubCategory.objects.all()
    unique_states = Pincode.objects.values_list('state', flat=True).distinct()
    average_rating = technician.feedback_set.aggregate(Avg('rating'))['rating__avg']
    formatted_average_rating = "{:.2f}".format(average_rating) if average_rating else None
    
   
    category = Category.objects.all()
    # subcategories = SubCategory.objects.all()
    subcategories = SubCategory.objects.filter(Category_id__id__in=technician.subcategories.values_list('Category_id__id', flat=True))
    # print("subcategory",subcategories)
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()

    selected_state = technician.working_pincode_areas.first().state if technician.working_pincode_areas.exists() else None
    state_pincodes = Pincode.objects.filter(state=selected_state) if selected_state else []

   
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        father_name = request.POST.get('father_name')    
        # category_id = request.POST.get('category_id')
        subcategory_id = request.POST.getlist('sub_category_id')
        mob_no = request.POST.get('mob_no')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')
        permanent_address = request.POST.get('permanent_address')
        id_proof = request.POST.get('id_proof')
        id_nob = request.FILES.get('id_nob')
        rating = request.POST.get('rating')
        serving_area = request.POST.get('serving_area')
        highest_qualification = request.POST.get('highest_qualification')
        state = request.POST.get('state')
        city = request.POST.get('city')
        status = request.POST.get('status')   
        date_of_joining = request.POST.get('date_of_joining')   
        application_form = request.FILES.get('application_form')  

        pincode = request.POST.getlist('pincode')
        onlinstatus = request.POST.getlist('onlinstatus')
        
        try:
            onlinestatus_obj = showonline.objects.get(technician_id=technician)
        except showonline.DoesNotExist:
            # If showonline object doesn't exist, create a new one
            onlinestatus_obj = showonline.objects.create(technician_id=technician)
        
        # Update online status based on checkbox value
        onlinestatus_obj.online = bool(onlinstatus)
        onlinestatus_obj.save()


        technician.admin.username = username
        technician.admin.first_name = first_name
        technician.admin.last_name = last_name
        technician.admin.email = email
        if profile_pic != None:
            technician.profile_pic=profile_pic

        technician.Father_name=father_name
        technician.mobile=mob_no
        technician.present_address=present_address
        technician.permanent_address=permanent_address
        technician.Id_Proof=id_proof

        if id_nob != None:
            technician.id_proof_document=id_nob

        if status == 'Inactive':
            technician.status = "Inactive"
            
        elif status == 'Hold':
            technician.status = 'Hold'
        
        elif status == 'New':
            technician.status = 'New'

        else:
            technician.status = 'Active'

        technician.rating=rating
        technician.serving_area=serving_area
        technician.highest_qualification=highest_qualification
        technician.state=state
        technician.working_pincode_areas.set(pincode)
        technician.subcategories.set(subcategory_id)
       
        if city:
            city = city.lower()
        technician.city=city
        # technician.joining_date=date_of_joining
        if date_of_joining:
            technician.joining_date =date_of_joining
        if application_form != None:
            technician.application_form=application_form
        

        # cat = Category.objects.get(id=category_id)
        # if subcategory_id:
        #     subcategories = SubCategory.objects.filter(id__in=subcategory_id)
        #     technician.subcategories.set(subcategories)
           

        technician.admin.save()
        technician.save()
        messages.success(request,'updated sucessfully')
        return redirect('technician_edit_profile',id=technician.id)
        # return render(request,'homofix_app/AdminDashboard/Technician/technician_profile.html',{'technician':technician,'category':category})
        # return redirect('technician_edit_profile',{'technician_id': technician_id})
    return render(request,'homofix_app/AdminDashboard/Technician/technician_profile.html',{'technician':technician,'category':category,'subcategories': subcategories,'state_choices':state_choices,'new_expert_count':new_expert_count,'booking_count':booking_count,'rebooking_count':rebooking_count,'customer_count':customer_count,'average_rating':formatted_average_rating,'unique_states': unique_states,'selected_pincode_ids': technician.working_pincode_areas.values_list('id', flat=True),'state_pincodes': state_pincodes})


def edit_technician(request):
    if request.method == "POST":
        
        technician_id = request.POST.get('technician_id')
        category_id = request.POST.get('category_id')
        username = request.POST.get('username')
        email = request.POST.get('email')


        technician = Technician.objects.get(id=technician_id)
        technician.admin.username = username
        technician.admin.email = email

        
        technician.category = Category.objects.get(id=category_id)
        technician.admin.save()
        technician.save()
        
        
        messages.success(request,"Records are Updated Successfully")
        return redirect('technician')

def delete_technician(request,id):
    technician = Technician.objects.get(id=id)
    user = technician.admin
    technician.delete()
    user.delete()
    messages.success(request, "Technician deleted successfully.")
    return redirect('technician')


def technician_history(request,id):
    task = Task.objects.filter(technician=id)
    rebooking = Rebooking.objects.filter(technician=id)
    technician = Technician.objects.get(id=id)
    tecnician_location = TechnicianLocation.objects.filter(technician_id=technician)
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'task':task,
        'rebooking':rebooking,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        'tecnician_location':tecnician_location
    }
   
    return render(request,'homofix_app/AdminDashboard/History/task_history.html',context)
   

# def technician_payment_history(request,id):

#     technician = Technician.objects.get(id=id)
#     wallet_history = WalletHistory.objects.filter(wallet__technician=technician)
    
    
#     share = Share.objects.filter(task__technician=technician)
#     new_expert_count = Technician.objects.filter(status="New").count()
#     booking_count = Booking.objects.filter(status = "New").count()
#     rebooking_count = Rebooking.objects.all().count()
#     customer_count = Customer.objects.all().count() 
    
#     wallet = Wallet.objects.get(technician=technician) 
    

#     if request.method == "POST":
        
#         type = request.POST.get('type')
#         amount = int(request.POST.get('amount'))
#         description = request.POST.get('description')

#         history = WalletHistory(wallet=wallet,type=type,amount=amount,description=description)
#         if history.type == 'bonus':
#             wallet.total_share += history.amount
#         else:
#             wallet.total_share -= history.amount
#         wallet.save()
#         history.save()
#         messages.success(request, f"{'Wallet Add  Successfully'}")
#         return redirect('technician_payment_history',technician.id)
        
        
    


#     context = {
        
#         'new_expert_count':new_expert_count,
#         'booking_count':booking_count,
#         'rebooking_count':rebooking_count,
#         'customer_count':customer_count,
#         'share':share,
#         'wallet_history':wallet_history,
#         'wallet':wallet
#     }
   
#     return render(request,'homofix_app/AdminDashboard/History/ExpertPaymentHistory/expert_payment_history.html',context)


def technician_payment_history(request,id):

    technician = Technician.objects.get(id=id)
    
    
    wallet_history = WalletHistory.objects.filter(wallet__technician_id=technician)
    settlement = Settlement.objects.filter(technician_id=technician)
   
    share = Share.objects.filter(task__technician=technician)
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count() 
    
    try:
       
        wallet = Wallet.objects.get(technician_id=technician)
        
    except Wallet.DoesNotExist:
        wallet = None
        messages.warning(request, 'No wallet found for this technician.')
    try:
        kyc = Kyc.objects.filter(technician_id=technician)
    except Kyc.DoesNotExist:
        kyc = None
        messages.warning(request, 'No KYC found for this technician.')

    if request.method == "POST":
        
        type = request.POST.get('type')
        amount = float(request.POST.get('amount'))
        description = request.POST.get('description')

        if wallet:
            history = WalletHistory(wallet=wallet,type=type,amount=amount,description=description)
            if history.type == 'bonus':
                wallet.total_share += Decimal(str(history.amount))
            else:
                wallet.total_share -= Decimal(str(history.amount))
            wallet.save()
            history.save()
            messages.success(request, 'Wallet transaction successfully added.')
        else:
            messages.warning(request, 'No wallet found for this technician.')
        
        return redirect('technician_payment_history',technician.id)
        
        
    


    context = {
        
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        'share':share,
        'wallet_history':wallet_history,
        'wallet':wallet,
        'kyc':kyc,
        'settlement':settlement
    }
   
    return render(request,'homofix_app/AdminDashboard/History/ExpertPaymentHistory/expert_payment_history.html',context)



    # return render(request,'homofix_app/AdminDashboard/History/ExpertPaymentHistory/expert_payment_history.html',context)
    
    # wallet = Wallet.object.get(technician=id)
    # technician = Technician.objects.get(id=wallet)
    # print("technician id",technician)
    # return redirect('technician_payment_history',technician.id)  

def product(request):
    q = request.GET.get('q', '').strip()
    product_qs = Product.objects.all()
    if q:
        product_qs = product_qs.filter(
            Q(name__icontains=q) |
            Q(subcategory__name__icontains=q)
        )
    paginator = Paginator(product_qs.order_by('name'), 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    category = Category.objects.all()
    categories = Category.objects.all()
    subcategory = SubCategory.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status="New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    if request.method == "POST":
        product_pic = request.FILES.get("product_pic")
        product_name = request.POST.get("product_name")
        product_title = request.POST.get("product_title")
        price = int(request.POST.get("price"))
        discount_amt = int(request.POST.get("discount_amt"))
        warranty = request.POST.get("warranty")
        description = request.POST.get("desc")
        warranty_desc = request.POST.get("warranty_desc")
        # category_id = request.POST.get("category_id")
        sub_category_id = request.POST.get("sub_category_id")

        

        if Product.objects.filter(name=product_name).exists():
            messages.warning(request, "Product is already taken")
            return redirect("product")

        # cat = Category.objects.get(id=category_id)
        subcategry = SubCategory.objects.get(id=sub_category_id)
        product = Product.objects.create(
            product_pic=product_pic,
            name=product_name,
            product_title=product_title,
            # category=cat,
            price=price,
            warranty=warranty,
            warranty_desc=warranty_desc,
            description=description,
            subcategory=subcategry,
            dis_amt=discount_amt

            
        )
        messages.success(request, "Product added successfully")
        product.save()
        return redirect("product")

    context = {
        # "product": product,
        'page_obj': page_obj,
        'search_query': q,

        "category": category,
        "new_expert_count": new_expert_count,
        "booking_count": booking_count,
        "subcategory": subcategory,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        'categories':categories
    }
    return render(request, "homofix_app/AdminDashboard/Product/product.html", context)

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    print("category_id",category_id)
    subcategories = SubCategory.objects.filter(Category_id=category_id)
   
    data = list(subcategories.values('id', 'name'))
    return JsonResponse(data, safe=False)




def get_products(request):
    subcategory_id = request.GET.get('subcategory_id')
    if subcategory_id:
        subcategory_id = int(subcategory_id)
        products = Product.objects.filter(subcategory_id=subcategory_id)
        data = [{'id': product.id, 'name': product.name} for product in products]
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse([], safe=False)



def get_products_price(request):
    subcategory_id = request.GET.get('subcategory_id')
    if subcategory_id:
        subcategory_id = int(subcategory_id)
        products = Product.objects.filter(subcategory_id=subcategory_id)
        data = []
        for product in products:
            if product.selling_price is not None:
                price = product.selling_price
            else:
                price = product.price
            data.append({'id': product.id, 'price': price, 'name': product.name})
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse([], safe=False)
# def product(request):
    

#     product = Product.objects.all()
#     category = Category.objects.all()
#     subcategory = SubCategory.objects.all()
#     new_expert_count = Technician.objects.filter(status="New").count()
#     booking_count = Booking.objects.filter(status = "New").count()
#     if request.method == "POST":       
        
#         product_pic = request.FILES.get('product_pic')
#         product_name = request.POST.get('product_name')
#         product_title = request.POST.get('product_title')
#         price = request.POST.get('price')
#         warranty = request.POST.get('warranty')
#         description = request.POST.get('desc')
#         warranty_desc = request.POST.get('warranty_desc')
#         category_id = request.POST.get('category_id')
       
        
        
#         if Product.objects.filter(name = product_name).exists():
#             # return JsonResponse({'status': 'error', 'message': 'Product is already Taken'})
#             messages.warning(request,'Product is already Taken')
#             return redirect('product')
            
#         cat = Category.objects.get(id=category_id)
#         product = Product.objects.create(product_pic=product_pic,name=product_name,product_title=product_title,category=cat,price=price,warranty=warranty,warranty_desc=warranty_desc,description=description)
#         messages.success(request,'Product Add Successfully')
#         product.save()
#         return redirect('product')
        
#         # return JsonResponse({'status':'Save'})
#     return render(request,'homofix_app/AdminDashboard/Product/product.html',{'product':product,'category':category,'new_expert_count':new_expert_count,'booking_count':booking_count,'subcategory':subcategory})


def update_product(request):
    if request.method == "POST":
        
        product_id = request.POST.get('product_id')
        # category_id = request.POST.get('category_id')
        subcategory_id = request.POST.get('subcategory_id')
        product_pic = request.FILES.get('product_pic')

        product_title = request.POST.get('product_title')
        product_name = request.POST.get('product_name')
        price = int(request.POST.get('price'))
        discount_price = int(request.POST.get('discount_price'))
        warranty = request.POST.get('warranty')
        warranty_description = request.POST.get('warranty_description')
        description = request.POST.get('description')

        # print("description",description)

        print("disocunt price",discount_price)
        # cat = Category.objects.get(id=category_id)
        subcat = SubCategory.objects.get(id=subcategory_id)
        product = Product.objects.get(id=product_id)
        
        discountd_price = price - discount_price

        # print("sellling price",discountd_price)
        if product_pic != None:
            product.product_pic = product_pic
        product.subcategory = subcat
        product.product_title = product_title
        product.name = product_name
        product.price = price
        product.dis_amt = discount_price
        product.selling_price = price - discount_price
        product.warranty = warranty
        product.warranty_desc = warranty_description
        product.description = description

        product.save()
        
        
        messages.success(request,"Records are Updated Successfully")
        return redirect('product')



def delete_product(request,id):
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('product')





######################## Addons #####################


def addons(request):
    q = request.GET.get('q', '').strip()
    category = Category.objects.all()
    addons_qs = SpareParts.objects.all()
    if q:
        addons_qs = addons_qs.filter(
            Q(spare_part__icontains=q) |
            Q(product__subcategory__name__icontains=q) |
            Q(product__name__icontains=q)
        )
    paginator = Paginator(addons_qs.order_by('spare_part'), 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    product = Product.objects.all()
    subcategory = SubCategory.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        spare_part = request.POST.get('spare_part')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        prod = Product.objects.get(id=product_id)
        addon = SpareParts.objects.create(product=prod,spare_part=spare_part,price=price,description=desc)
        
        messages.success(request,'Addons Product Add Successfully')
        return redirect('addons')
        

    return render(request,'homofix_app/AdminDashboard/Addons/addon.html',{'addons':addons,'product':product,'new_expert_count':new_expert_count,'booking_count':booking_count,'rebooking_count':rebooking_count,'customer_count':customer_count,'category':category,'subcategory':subcategory,'page_obj': page_obj,'search_query': q})


def edit_addons(request,id):
    
    spare_parts = SpareParts.objects.get(id=id)
    category = Category.objects.all()
    subcategory = SubCategory.objects.all()
    product = Product.objects.all()
    context = {
        'spare_parts':spare_parts,
        'category':category,
        'subcategory':subcategory,
        'product':product
    }
    return render(request,'homofix_app/AdminDashboard/Addons/edit_addons.html',context)

def update_addons(request):

    if request.method == "POST":
        addon_id  = request.POST.get('spare_parts_id')
        print("addon id",addon_id)
        product_id  = request.POST.get('product_id')
        spare_part  = request.POST.get('spare_part')
        price  = request.POST.get('price')
        description  = request.POST.get('desc')
  
        product = Product.objects.get(id=product_id)
        addons_prod = SpareParts.objects.get(id=addon_id)
        
        addons_prod.product = product
        addons_prod.spare_part = spare_part
        addons_prod.price = price
        addons_prod.description =description
        
        addons_prod.save()
        messages.success(request,'SpareParts Updated Successfully')
        return redirect('addons')

    

def delete_addons(request,id):

    addon = SpareParts.objects.get(id=id)
    addon.delete()
    messages.success(request, "Addon deleted successfully.")
    return redirect('addons')

def addons_details(request):
    q = request.GET.get('q', '').strip()

    addon_qs = Addon.objects.all()
    if q:
        addon_qs = addon_qs.filter(
            Q(spare_parts_id__spare_part__icontains=q) |
            Q(booking_prod_id__product__name__icontains=q)
        )
    paginator = Paginator(addon_qs.order_by('description'), 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'search_query': q,
    }
    return render(request,'homofix_app/AdminDashboard/Addons/addons_detail.html',context)


# --------------------- SUPPORT CREATION --------------------- 

def support(request):
    q = request.GET.get('q', '').strip()
    suppt_qs = Support.objects.all()
    if q:
        suppt_qs = suppt_qs.filter(
            Q(admin__first_name__icontains=q) |
            Q(admin__last_name__icontains=q) |
            Q(mobile__icontains=q)
        )
    paginator = Paginator(suppt_qs.order_by('id'), 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    return render(request,'homofix_app/AdminDashboard/Support/support.html',{'page_obj':page_obj,'search_query': q,'new_expert_count':new_expert_count,'booking_count':booking_count,'rebooking_count':rebooking_count,'customer_count':customer_count})

def add_support(request):
    
    if request.method == "POST":
        random_number = random.randint(0, 999)
        unique_number = str(random_number).zfill(3)
        # username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        can_new_booking = request.POST.get('new_booking')
        can_cancel_booking = request.POST.get('can_cancel_booking')
        can_rebooking = request.POST.get('can_rebooking')
        can_assign_task = request.POST.get('can_assign_task')
        can_new_expert = request.POST.get('can_new_expert')
        print("new expert",can_new_expert)
        can_customer_enquiry = request.POST.get('can_customer_enquiry')
        
        # if CustomUser.objects.filter(username=username).exists():
        #     messages.error(request, 'Username is already taken')
        #     return redirect('admin_support')
            
        user = CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=first_name+unique_number, password=password, email=email, user_type='3')
        user.support.can_new_booking = True if can_new_booking == 'on' else False
        user.support.can_cancel_booking = True if can_cancel_booking == 'on' else False
        user.support.can_rebooking = True if can_rebooking == 'on' else False
        user.support.can_assign_task = True if can_assign_task == 'on' else False
        user.support.can_expert_create = True if can_new_expert == 'on' else False
        user.support.can_contact_us_enquiry = True if can_customer_enquiry == 'on' else False
        
        user.save()
        messages.success(request, 'Support registered successfully')
        return redirect('admin_support')
        
    return redirect('admin_support')


def support_profile(request,id):
    
    support = Support.objects.get(id=id)
    new_expert_count = Technician.objects.filter(status="New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    return render(request,'homofix_app/AdminDashboard/Support/edit_profile.html',{'support':support,'new_expert_count':new_expert_count,'rebooking_count':rebooking_count,'customer_count':customer_count})


# def support_update_profile(request):
    
#     if request.method == "POST":
#         support_id = request.POST.get('support_id')
       
#         profile_pic = request.FILES.get('profile_pic') 
#         username = request.POST.get('username')
#         father_name = request.POST.get('father_name')
#         marital_status = request.POST.get('marital_status')
#         dob = request.POST.get('dob')
#         email = request.POST.get('email')
#         mob_no = request.POST.get('mob_no')
#         address = request.POST.get('address')
#         permanent_address = request.POST.get('permanent_address')
#         date_of_joining = request.POST.get('date_of_joining')
#         status = request.POST.get('status')
#         xyzzz = request.POST.get('xyzzz')
#         firstname = request.POST.get('firstname')
#         print("last name",xyzzz)
        
#         application_form = request.FILES.get('application_form')
#         document_form = request.FILES.get('document_form')
#         # print("application form", application_form)


#         # Permission 
#         can_new_booking = request.POST.get('new_booking')
#         can_cancel_booking = request.POST.get('can_cancel_booking')
#         can_rebooking = request.POST.get('can_rebooking')
#         can_assign_task = request.POST.get('can_assign_task')
#         can_new_expert = request.POST.get('can_new_expert')
#         can_customer_enquiry = request.POST.get('can_customer_enquiry')
#         can_job_enquiry = request.POST.get('can_job_enquiry')

#         support = Support.objects.get(id=support_id)
#         print("suppor id ",support)
#         support.admin.last_name = xyzzz
#         support.admin.last_name="dd"
#         support.save()
        
        
#         if profile_pic:
#             support.profile_pic = profile_pic
        
#         if application_form:
#             support.application_form=application_form

#         if document_form:
#             support.document_form=document_form

        
#         # if application_form:
#         #     application_form_str = ','.join(str(file) for file in application_form)
#         #     support.application_form = application_form_str
#         print("helooooo first",support.admin.first_name) 
#         print("helooooo last",support.admin.last_name) 
#         # support.admin.last_name = lastname 
#         # support.admin.username = username 
#         # support.admin.email = email
#         # support.admin.last_name = last_name 
#         support.admin.first_name = firstname 
#         support.address = address 
#         support.permanent_address = permanent_address 
#         support.father_name = father_name 
#         support.marital_status = marital_status 
#         support.d_o_b = dob 
#         support.mobile = mob_no 


#         support.can_new_booking = True if can_new_booking == 'on' else False
#         support.can_cancel_booking = True if can_cancel_booking == 'on' else False
#         support.can_rebooking = True if can_rebooking == 'on' else False
#         support.can_assign_task = True if can_assign_task == 'on' else False
#         support.can_expert_create = True if can_new_expert == 'on' else False
#         support.can_contact_us_enquiry = True if can_customer_enquiry == 'on' else False
#         support.can_job_enquiry = True if can_job_enquiry == 'on' else False


#         if date_of_joining:
#             support.joining_date = date_of_joining 

#         if status == 'Deactivate':
#             support.status = "Deactivate"
#         elif status == 'Hold':
#             support.status = 'Hold'
#         else:
#             support.status = 'Active'

        
#         support.save()
#         messages.success(request, 'Support Updated Succesffully')
#         return HttpResponseRedirect(reverse("support_profile",args=[support_id]))



def support_update_profile(request):
    if request.method == "POST":
        support_id = request.POST.get('support_id')
        support_nw_id = request.POST.get('support_nw_id')
        print("fadsfadsfadsfads",support_nw_id)
       
        profile_pic = request.FILES.get('profile_pic') 
        username = request.POST.get('username')
        father_name = request.POST.get('father_name')
        marital_status = request.POST.get('marital_status')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        mob_no = request.POST.get('mob_no')
        address = request.POST.get('address')
        permanent_address = request.POST.get('permanent_address')
        date_of_joining = request.POST.get('date_of_joining')
        status = request.POST.get('status')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        
        application_form = request.FILES.get('application_form')
        document_form = request.FILES.get('document_form')
        # print("application form", application_form)


        # Permission 
        can_new_booking = request.POST.get('new_booking')
        can_cancel_booking = request.POST.get('can_cancel_booking')
        can_rebooking = request.POST.get('can_rebooking')
        can_assign_task = request.POST.get('can_assign_task')
        can_new_expert = request.POST.get('can_new_expert')
        can_customer_enquiry = request.POST.get('can_customer_enquiry')
        can_job_enquiry = request.POST.get('can_job_enquiry')

        # support = Support.objects.get(id=support_id)
        hod = CustomUser.objects.get(id=support_id)
        
        
        if profile_pic:
            hod.profile_pic = profile_pic
        
        if application_form:
            hod.support.application_form=application_form

        if document_form:
            hod.support.document_form=document_form

        
        # if application_form:
        #     application_form_str = ','.join(str(file) for file in application_form)
        #     support.application_form = application_form_str
        # print("helooooo",support.admin.first_name) 
        # support.admin.last_name = lastname 
        # support.admin.username = username 
        # support.admin.email = email
        hod.first_name = firstname 
        hod.last_name = lastname 
        hod.support.address = address 
        hod.support.permanent_address = permanent_address 
        hod.support.father_name = father_name 
        hod.support.marital_status = marital_status 
        hod.support.d_o_b = dob 
        hod.support.mobile = mob_no 


        hod.support.can_new_booking = True if can_new_booking == 'on' else False
        hod.support.can_cancel_booking = True if can_cancel_booking == 'on' else False
        hod.support.can_rebooking = True if can_rebooking == 'on' else False
        hod.support.can_assign_task = True if can_assign_task == 'on' else False
        hod.support.can_expert_create = True if can_new_expert == 'on' else False
        hod.support.can_contact_us_enquiry = True if can_customer_enquiry == 'on' else False
        hod.support.can_job_enquiry = True if can_job_enquiry == 'on' else False


        if date_of_joining:
            hod.support.joining_date = date_of_joining 

        if status == 'Deactivate':
            hod.support.status = "Deactivate"
        elif status == 'Hold':
            hod.support.status = 'Hold'
        else:
            hod.support.status = 'Active'

        
        hod.save()
        messages.success(request, 'Support Updated Succesffully')
        return HttpResponseRedirect(reverse("admin_support_profile",args=[support_nw_id]))


def delete_support(request,id):
    support = Support.objects.get(id=id)
    user = support.admin
    support.delete()
    user.delete()
    messages.success(request, "Support deleted successfully.")
    return redirect('admin_support')
    
def support_history(request,id):
    support = Support.objects.get(id=id)
    task = Task.objects.filter(supported_by=support,booking__status='Assign')
    technician = Technician.objects.filter(supported_by=support)
    print("ddddd",technician)

    booking = Booking.objects.filter(supported_by=id)    
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        'booking':booking,
        'task':task,
        'technician':technician
        
    }
    return render(request,'homofix_app/AdminDashboard/History/SupportHistory/support_history.html',context)



# --------------------- Pincode --------------------- 

from django.core.paginator import Paginator
from django.db.models import Q  # for flexible filtering

def pincode(request):
    query = request.GET.get('q', '')  # get search input
    pincode_list = Pincode.objects.filter(
        Q(code__icontains=query)  # search by `code` field
    ).order_by('-id')  # Latest first

    paginator = Paginator(pincode_list, 10)  # 10 per page
    page_number = request.GET.get('page')
    pincode_page = paginator.get_page(page_number)

    suppt = Support.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status="New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()

    return render(request, 'homofix_app/AdminDashboard/Pincode/pincode_list.html', {
        'pincode': pincode_page,
        'query': query,
        'suppt': suppt,
        'new_expert_count': new_expert_count,
        'booking_count': booking_count,
        'rebooking_count': rebooking_count,
        'customer_count': customer_count
    })


def add_pincode(request):
    if request.method == "POST":
        state = request.POST.get('state').strip().title()
        pincode = request.POST.get('pincode')
        pin_code = Pincode.objects.create(code=pincode,state=state)
        pin_code.save()
        messages.success(request,'Pincode Added Successfully')
        return redirect('pincode')


def edit_pincode(request,id):
    if request.method == "POST":
        state = request.POST.get('state').strip().title()
        code = request.POST.get('pincode')

        
        
        pin_code = Pincode.objects.get(id=id)
        pin_code.code = code
        pin_code.state = state
        pin_code.save()
        messages.success(request,'Pincode Updated Successfully')
        return redirect('pincode')

def delete_pincode(request,id):
    
    pin_code = Pincode.objects.get(id=id)
    pin_code.delete()
    messages.success(request, "Pincode deleted successfully.")
    return redirect('pincode')

        

# ------------------------------- Universal Slot ------------------------------        

def add_universal_slot(request):
    if request.method == "POST":
        version = request.POST.get('version')
        slot = request.POST.get('slot')
        # forceupdate = request.POST.get('forceupdate')
        forceupdate = request.POST.get('forceupdate') == 'on'
        universal_slot = UniversalCredential.objects.create(app_version=version,universal_slot=slot,force_update=forceupdate)
        universal_slot.save()
        messages.success(request,'Universal Slot Added Successfully')
        return redirect('universal_slot')
    # return render(request,'homofix_app/AdminDashboard/UniversalSlot/universalslot.html')

def universal_slot(request):
    universal_Slot = UniversalCredential.objects.all()
    record_exists = universal_Slot.count() >= 1
    
    context = {
        'universal_slot':universal_Slot,
        'disable_add_button': record_exists
    }
    return render(request,'homofix_app/AdminDashboard/UniversalSlot/universalslot.html',context)


def edit_universal_slot(request, id):
    if request.method == "POST":
        version = request.POST.get('version')
        slot = request.POST.get('slot')
        # forceupdate = request.POST.get('forceupdate')
        forceupdate = request.POST.get('forceupdate') == 'on'
        universal_slot = UniversalCredential.objects.get(id=id)


        universal_slot.app_version = version
        universal_slot.force_update = forceupdate
        universal_slot.universal_slot = slot

        universal_slot.save()
        messages.success(request,'Universal Slot Updated Successfully')
        return redirect('universal_slot')
        


def delete_universal_slot(request,id):
    universal_slot = UniversalCredential.objects.get(id=id)
    universal_slot.delete()
    messages.success(request,'Universal Slot Delete Successfully')
    return redirect('universal_slot')
        
    

# ------------------------------- FAQS ------------------------------        



def add_faq(request):
    q = request.GET.get('q', '').strip()
    product = Product.objects.all()
    category = Category.objects.all()
    subcategory =SubCategory.objects.all()
    faqs_qs = FAQ.objects.all()
    if q:
        faqs_qs = faqs_qs.filter(
            Q(question__icontains=q) |
            Q(product__subcategory__name__icontains=q)
        )
    paginator = Paginator(faqs_qs.order_by('question'), 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
        

    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        question = request.POST.get('question')
        answer = request.POST.get('answer')

        prod_id = Product.objects.get(id=product_id)
        faq = FAQ.objects.create(product=prod_id,question=question,answer=answer)
        faq.save()
        
    context = {
        'product':product,
        # 'faqs':faqs,
        'page_obj': page_obj,
        'search_query': q,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'category':category,
        'customer_count':customer_count,
        'subcategory':subcategory
    }

    return render(request,'homofix_app/AdminDashboard/Faqs/faqs.html',context)

def update_add_faq(request):
    if request.method == "POST":
        faq_id = request.POST.get('faq_id')
        product_id = request.POST.get('product_id')
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        prod_id = Product.objects.get(id=product_id)
        faq = FAQ.objects.get(id=faq_id)
        faq.product = prod_id
        faq.question = question
        faq.answer = answer
        faq.save()
        messages.success(request,'FAQ Updated Successfully')
        return redirect('add_faq')



def delete_faq(request,id):
    faq = FAQ.objects.get(id=id)
    faq.delete()
    messages.success(request, " FAQ deleted successfully.")
    return redirect('add_faq')


# def booking_list(request):
    
#     booking_count = Booking.objects.filter(status="New").count()
#     booking = Booking.objects.all().order_by("-id")
#     bookings = Booking.objects.filter(status="New").order_by("-id")
   

#     technicians = Technician.objects.all()
#     tasks = Task.objects.all()
#     new_expert_count = Technician.objects.filter(status="New").count()
#     rebooking_count = Rebooking.objects.all().count()
#     customer_count = Customer.objects.all().count()
#     if request.method == "POST":
#         otp_number = random.randint(0, 9999)
#         print("otpp number", otp_number)
#         otp_unique = str(otp_number).zfill(3)

#         first_name = request.POST.get("full_name")
#         mob = request.POST.get("mob")
#         request.session["full_name"] = first_name
#         request.session["mob"] = mob
#         request.session["otp"] = otp_unique
#         if Customer.objects.filter(mobile=mob).exists():
           
#             return JsonResponse({'status':'Save'})
#         else:
            
#             return JsonResponse({"status": "Save"})

        
#     context = {
#         "booking": booking,
#         "technicians": technicians,
#         "tasks": tasks,
#         "new_expert_count": new_expert_count,
#         "booking_count": booking_count,
#         "rebooking_count": rebooking_count,
#         "customer_count": customer_count,
#         "bookings": bookings,
#     }

#     return render(
#         request, "homofix_app/AdminDashboard/Booking_list/booking.html", context
#     )



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# def booking_list(request):
#     booking_count = Booking.objects.filter(status="New").count()
#     booking_list = Booking.objects.filter(status="New").order_by("-id")
    
#     paginator = Paginator(booking_list, 5)  # Show 10 bookings per page
#     page = request.GET.get("page")
#     try:
#         bookings = paginator.page(page)
#     except PageNotAnInteger:
#         bookings = paginator.page(1)
#     except EmptyPage:
#         bookings = paginator.page(paginator.num_pages)

#     new_expert_count = Technician.objects.filter(status="New").count()
#     rebooking_count = Rebooking.objects.count()
#     customer_count = Customer.objects.count()

#     if request.method == "POST":
#         otp_number = random.randint(0, 9999)
#         otp_unique = str(otp_number).zfill(4)

#         first_name = request.POST.get("full_name")
#         mob = request.POST.get("mob")

#         request.session["full_name"] = first_name
#         request.session["mob"] = mob
#         request.session["otp"] = otp_unique

#         return JsonResponse({'status': 'Save'})

#     context = {
#         "bookings": bookings,
#         "new_expert_count": new_expert_count,
#         "booking_count": booking_count,
#         "rebooking_count": rebooking_count,
#         "customer_count": customer_count,
#     }

#     return render(
#         request, "homofix_app/AdminDashboard/Booking_list/booking.html", context
#     )


from django.db.models import Q  # Q object for complex queries
from django.utils.dateparse import parse_date
# def booking_list(request):

#     if request.method == "POST":
#         otp_number = random.randint(0, 9999)
#         print("otpp number", otp_number)
#         otp_unique = str(otp_number).zfill(3)

#         first_name = request.POST.get("full_name")
#         mob = request.POST.get("mob")
#         request.session["full_name"] = first_name
#         request.session["mob"] = mob
#         request.session["otp"] = otp_unique
#         if Customer.objects.filter(mobile=mob).exists():
#             return JsonResponse({'status':'Save'})
#         else:
#              return JsonResponse({"status": "Save"})
#     search_query = request.GET.get('q', '')  # Search query from input field

#     bookings_queryset = Booking.objects.filter(status="New").order_by("-id")

#     if search_query:
#         bookings_queryset = bookings_queryset.filter(
#             Q(order_id__icontains=search_query) |
#             Q(booking_customer__icontains=search_query) |
#             Q(city__icontains=search_query) |
#             Q(zipcode__icontains=search_query) |
#             Q(mobile__icontains=search_query)
#         )

#     paginator = Paginator(bookings_queryset, 10)
#     page = request.GET.get("page")
#     try:
#         bookings = paginator.page(page)
#     except PageNotAnInteger:
#         bookings = paginator.page(1)
#     except EmptyPage:
#         bookings = paginator.page(paginator.num_pages)

#     new_expert_count = Technician.objects.filter(status="New").count()
#     rebooking_count = Rebooking.objects.count()
#     customer_count = Customer.objects.count()

#     context = {
#         "bookings": bookings,
#         "new_expert_count": new_expert_count,
#         "booking_count": bookings_queryset.count(),
#         "rebooking_count": rebooking_count,
#         "customer_count": customer_count,
#         "search_query": search_query,
#     }

#     return render(request, "homofix_app/AdminDashboard/Booking_list/booking.html", context)




def booking_list(request):
    if request.method == "POST":
        otp_number = random.randint(0, 9999)
        print("OTP number:", otp_number)
        otp_unique = str(otp_number).zfill(3)

        first_name = request.POST.get("full_name")
        mob = request.POST.get("mob")
        request.session["full_name"] = first_name
        request.session["mob"] = mob
        request.session["otp"] = otp_unique

        if Customer.objects.filter(mobile=mob).exists():
            return JsonResponse({'status': 'Save'})
        else:
            return JsonResponse({"status": "Save"})

    search_query = request.GET.get('q', '')  # Search query from input field
   
    bookings_queryset = Booking.objects.filter(status="New").order_by("-id")

    if search_query:
        try:
            # Try parsing search_query as a date (YYYY-MM-DD)
            parsed_date = parse_date(search_query)
        except ValueError:
            parsed_date = None

        filters = Q(order_id__icontains=search_query) | \
                  Q(booking_customer__icontains=search_query) | \
                  Q(city__icontains=search_query) | \
                  Q(zipcode__icontains=search_query) | \
                  Q(mobile__icontains=search_query)

        if parsed_date:
            filters |= Q(booking_date__icontains=parsed_date)  # Add booking date filter if valid

        bookings_queryset = bookings_queryset.filter(filters)

    paginator = Paginator(bookings_queryset, 10)
    page = request.GET.get("page")
    try:
        bookings = paginator.page(page)
    except PageNotAnInteger:
        bookings = paginator.page(1)
    except EmptyPage:
        bookings = paginator.page(paginator.num_pages)

    new_expert_count = Technician.objects.filter(status="New").count()
    rebooking_count = Rebooking.objects.count()
    customer_count = Customer.objects.count()

    context = {
        "bookings": bookings,
        "new_expert_count": new_expert_count,
        "booking_count": bookings_queryset.count(),
        "rebooking_count": rebooking_count,
        "customer_count": customer_count,
        "search_query": search_query,
    }

    return render(request, "homofix_app/AdminDashboard/Booking_list/booking.html", context)

def admin_verify_otp(request):
    if request.method == "POST":
        
        otp_num = request.session.get('otp', 'Default value if key does not exist')
        
        

        otp = request.POST.get('otp')
        #if otp == otp_num:  
        if otp == "1234":  
            # OTP is correct, redirect to success page
            # return HttpResponse('otp sucess')
            
            random_number = random.randint(0, 999)
            unique_number = str(random_number).zfill(3)
       
            first_name = request.session.get('full_name', 'Default value if key does not exist')
            mob = request.session.get('mob', 'Default value if key does not exist')
            
            
            if Customer.objects.filter(mobile=mob).exists():
                customer = Customer.objects.get(mobile=mob)
                request.session['customer_id'] = customer.id
                # request.session['customer_id'] = Customer.id
                return JsonResponse({'status': 'Save', 'message': 'otp is match'})
                
            else:

                # user = CustomUser.objects.create(username=user.id,first_name=first_name, user_type='4')    
                user = CustomUser.objects.create(first_name=first_name,username=mob, user_type='4')    
                user.set_password(mob)
                user.customer.mobile = mob
                user.save()
                request.session['customer_id'] = user.customer.id

           
            return JsonResponse({'status': 'Save', 'message': 'otp is match'})
            # return redirect('support_orders')
        else:
            print("show error msg here")
            return JsonResponse({'status': 'Error', 'message': 'wrong otp'})
            # OTP is incorrect, show error message and reload the page
            # messages.error(request, 'Invalid OTP. Please try again.')
            
            # return JsonResponse({'status': 'Error', 'message': 'otp is not  valid'})
    


# def admin_booking(request):
   
    
#     user = request.user
#     adminhod = AdminHOD.objects.get(admin=user)
#     admin_by = request.user.adminhod
    
#     prod = Product.objects.all()
#     category = Category.objects.all()
#     state_choices = STATE_CHOICES
    
    

#     if request.method == 'POST':
       
#         customer_id = request.session.get('customer_id','Default value if key does not exist')
#         print("customer id ",customer_id)
        
#         product_ids = request.POST.getlist('product_id')
#         quantities = request.POST.getlist('quantity')

#         print("qunattttiyttt",quantities)
        
#         booking_date_str = request.POST.get('booking_date')
#         state = request.POST.get('state')
#         zip_code = request.POST.get('zip_code')
#         address = request.POST.get('address')
#         city = request.POST.get('city')
#         area = request.POST.get('area')
#         description = request.POST.get('description')
#         total_amount = int(request.POST.get('total_amount'))
#         print("sss",total_amount)
        
#         customer = Customer.objects.get(id=customer_id)
#         if city:
#             city = city.lower()
#         customer.city = city
#         customer.state = state
#         customer.area = area
#         customer.zipcode = zip_code
#         customer.address=address,
#         customer.save()
#         booking_date = timezone.make_aware(datetime.datetime.fromisoformat(booking_date_str))
        
        
#         booking = Booking.objects.create(
#             customer=customer,
#             booking_date=booking_date,   
#             description=description,          
#             admin_by=admin_by
           
#         )



#         for i, product_id in enumerate(product_ids):
#             product = Product.objects.get(id=product_id)
#             print("producttttt",product)
#             # print("producttttt",product)
            
#             quantity = int(quantities[i])
#             print("quaaaaaa",quantity)
#             price = int(request.POST.getlist('price')[i])
            
#             BookingProduct.objects.create(
#                 booking=booking,
#                 product=product,
#                 quantity=quantity,
#                 total_price=total_amount
#                 # price=price
#             )
#             # total_price = sum(price_list)
#             # booking.total_price = total_price
#             booking.save()

#         messages.success(request, 'Booking created successfully.')
#         return redirect('booking_list')

#     context = {
#         'prod': prod,
#         'state_choices':state_choices,
#         'category':category,
#         'support':support
#     }
#     return render(request, 'homofix_app/AdminDashboard/Booking_list/create_booking.html', context)


# def admin_booking(request):
#     user = request.user
#     adminhod = AdminHOD.objects.get(admin=user)
#     admin_by = request.user.adminhod
    
#     prod = Product.objects.all()
#     category = Category.objects.all()
#     state_choices = STATE_CHOICES
    
#     if request.method == 'POST':
#         customer_id = request.session.get('customer_id','Default value if key does not exist')
#         product_ids = request.POST.getlist('product_id')
        
        
#         quantities = request.POST.getlist('quantity')
        
#         # for i in range(len(product_ids)):
#         #     print("Product ID:", product_ids[i])
#         #     print("Quantity:", quantities[i])
#         print("qantityyyyy",quantities)
#         booking_date_str = request.POST.get('booking_date')
#         state = request.POST.get('state')
#         zip_code = request.POST.get('zip_code')
#         address = request.POST.get('address')
#         city = request.POST.get('city')
#         area = request.POST.get('area')
#         description = request.POST.get('description')
#         total_amount = int(request.POST.get('total_amount'))
        
#         customer = Customer.objects.get(id=customer_id)
#         if city:
#             city = city.lower()
#         customer.city = city
#         customer.state = state
#         customer.area = area
#         customer.zipcode = zip_code
#         customer.address=address,
#         customer.save()
#         booking_date = timezone.make_aware(datetime.datetime.fromisoformat(booking_date_str))
        
#         booking = Booking.objects.create(
#             customer=customer,
#             booking_date=booking_date,   
#             description=description,          
#             admin_by=admin_by
#         )

#         for i, product_id in enumerate(product_ids):
#             product = Product.objects.get(id=product_id)
#             quantity = int(quantities[i])
#             print("qunatittt",quantity)
#             price = int(request.POST.getlist('price')[i])
            
#             BookingProduct.objects.create(
#                 booking=booking,
#                 product=product,
#                 quantity=quantity,
#                 total_price=price * quantity
#             )

#         messages.success(request, 'Booking created successfully.')
#         return redirect('booking_list')

#     context = {
#         'prod': prod,
#         'state_choices':state_choices,
#         'category':category,
#         'support':support
#     }
#     return render(request, 'homofix_app/AdminDashboard/Booking_list/create_booking.html', context)


def admin_booking(request):
   
    
    user = request.user
    adminhod = AdminHOD.objects.get(admin=user)
    admin_by = request.user.adminhod
    
    prod = Product.objects.all()
    category = Category.objects.all()
    state_choices = STATE_CHOICES
    mobile = request.session.get("mob", "Default value if key does not exist")
    
    

    if request.method == 'POST':
       
        customer_id = request.session.get('customer_id','Default value if key does not exist')
        print("customer id ",customer_id)
        
        product_ids = request.POST.getlist('product_id')
        quantities = request.POST.getlist('quantity')
        
        booking_date_str = request.POST.get('booking_date')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        address = request.POST.get('address')
        city = request.POST.get('city')
        area = request.POST.get('area')
        description = request.POST.get('description')
        slot = request.POST.get('slot')
        total_amount = int(request.POST.get('total_amount'))
        print("sss",total_amount)
        
        customer = Customer.objects.get(id=customer_id)
        if city:
            city = city.lower()
        customer.city = city
        customer.state = state
        customer.area = area
        customer.zipcode = zip_code
        customer.address=address,
        customer.save()
        # booking_date = timezone.make_aware(datetime.datetime.fromisoformat(booking_date_str))
        booking_date = timezone.make_aware(datetime.fromisoformat(booking_date_str))

        bookingcust = request.session.get(
            "full_name", "Default value if key does not exist"
        )
        
        
        booking = Booking.objects.create(
            customer=customer,
            booking_date=booking_date,   
            description=description,          
            admin_by=admin_by,
            booking_customer=bookingcust,
            booking_address=address,
            mobile=mobile,
            city=city,
            state=state,
            area=area,
            zipcode=zip_code,
            slot = slot
           
        )



        for i, product_id in enumerate(product_ids):
            product = Product.objects.get(id=product_id)
            print("producttttt",product)
            # print("producttttt",product)
            
            quantity = int(quantities[i])
            print("quaaaaaa",quantity)
            price = int(request.POST.getlist('price')[i])
            
            BookingProduct.objects.create(
                booking=booking,
                product=product,
                quantity=quantity,
                total_price=total_amount,
                selling_price=product.selling_price,
                price=product.price,
                
                # price=price
            )
            # total_price = sum(price_list)
            # booking.total_price = total_price
            booking.save()
        
        # Auto assign technician using round-robin logic
        from homofix_app.services.auto_assign import assign_employee_to_booking
        assign_employee_to_booking(booking)
        
        url = "http://sms.webtextsolution.com/sms-panel/api/http/index.php"
        payload = {
            "username": "Homofix",
            "apikey": "21141-B77C6",
            "apirequest": "Text",
            "sender": "HOMOFX",
            "mobile": booking.mobile,
            "message": "Dear Customer,Your service has been successfully booked. Our Service Expert will arrive as scheduled on the agreed date and time. Thank you for choosing HomOfix Company",
            "route": "TRANS",
            "TemplateID": "1407170037761317839",
            "format": "JSON",
        }
        response = requests.get(url, params=payload)
        print(response.json())

        messages.success(request, 'Booking created successfully.')
        return redirect('booking_list')
    
    slot = Slot.objects.all()
    pincode = Pincode.objects.all()
    states = Pincode.objects.values_list("state", flat=True).distinct()

    context = {
        'prod': prod,
        'state_choices':state_choices,
        'category':category,
        'support':support,
        'slot':slot,
        'pincode':pincode,
        'states':states
    }
    return render(request, 'homofix_app/AdminDashboard/Booking_list/create_booking.html', context)



def admin_List_of_expert(request,id):
    # user = request.user
    # support = Support.objects.get(admin=user)  
    
    booking = Booking.objects.get(id=id)
    booking_subcategories = booking.products.values_list("subcategory", flat=True).distinct()
    
   
    expert = (
        Technician.objects
        .filter(
            working_pincode_areas__code=booking.zipcode,
            subcategories__in=booking_subcategories,
            status="Active",
            showonline__online=True
        )
        .distinct()
    )
    tasks = Task.objects.filter(booking=booking)
    
   
    
    # expert = Technician.objects.filter(city=booking.city, serving_area__icontains=booking.area)
    context = {
        'expert':expert,
        'booking':booking,
        'tasks': tasks,
        'support':support
        
        
        
    }
    
    return render(request,'homofix_app/AdminDashboard/Booking_list/list_of_expert.html',context)    

def admin_reschedule(request):
    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        booking_date_str = request.POST.get('booking_date')
        slot = request.POST.get('slot')
        
        # Convert date string to datetime object
        try:
            booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format")
            return redirect('booking_list')
        
        try:
            booking = Booking.objects.get(id=booking_id)
            
            # Get the time from the slot
            if slot:
                slot_int = int(slot)
                slot_time_str = dict(SLOT_CHOICES).get(slot_int, "")
                if slot_time_str:
                    # Extract start time from slot (e.g., "08:00 AM - 09:00 AM" -> "08:00 AM")
                    start_time_str = slot_time_str.split(' - ')[0]
                    
                    # Parse the time
                    try:
                        start_time = datetime.strptime(start_time_str, '%I:%M %p').time()
                        # Combine date and time
                        booking_datetime = datetime.combine(booking_date, start_time)
                        booking_datetime = make_aware(booking_datetime)
                        
                        # Update booking
                        booking.booking_date = booking_datetime
                        booking.slot = slot_int
                        booking.save()
                        
                        messages.success(request, "Your order reschedule success")
                    except ValueError:
                        messages.error(request, "Invalid time format in slot")
                        return redirect('booking_list')
                else:
                    messages.error(request, "Invalid slot selected")
                    return redirect('booking_list')
            else:
                messages.error(request, "No slot selected")
                return redirect('booking_list')
                
        except Booking.DoesNotExist:
            messages.error(request, "Booking not found")
            
        return redirect('booking_list')

def task_reschedule(request):
    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        booking_date_str = request.POST.get('booking_date')
        slot = request.POST.get('slot')
        
        # Convert date string to datetime object
        try:
            booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format")
            return redirect('list_of_task')
        
        try:
            booking = Booking.objects.get(id=booking_id)
            
            # Get the time from the slot
            if slot:
                slot_int = int(slot)
                slot_time_str = dict(SLOT_CHOICES).get(slot_int, "")
                if slot_time_str:
                    # Extract start time from slot (e.g., "08:00 AM - 09:00 AM" -> "08:00 AM")
                    start_time_str = slot_time_str.split(' - ')[0]
                    
                    # Parse the time
                    try:
                        start_time = datetime.strptime(start_time_str, '%I:%M %p').time()
                        # Combine date and time
                        booking_datetime = datetime.combine(booking_date, start_time)
                        booking_datetime = make_aware(booking_datetime)
                        
                        # Update booking
                        booking.booking_date = booking_datetime
                        booking.slot = slot_int
                        booking.save()
                        
                        messages.success(request, "Your order reschedule success")
                    except ValueError:
                        messages.error(request, "Invalid time format in slot")
                        return redirect('list_of_task')
                else:
                    messages.error(request, "Invalid slot selected")
                    return redirect('list_of_task')
            else:
                messages.error(request, "No slot selected")
                return redirect('list_of_task')
                
        except Booking.DoesNotExist:
            messages.error(request, "Booking not found")
            
        return redirect('list_of_task')





def cancel_booking_byadmin(request,booking_id):
    if request.method == "POST":
        cancel_reason = request.POST.get('cancel_reason')
        booking = Booking.objects.get(id=booking_id)
        booking.status = 'Cancelled'
        booking.cancel_reason = cancel_reason
        print("okkkkkk",cancel_reason)
        booking.save()
        messages.success(request, 'Booking has been cancelled.')
        return redirect('booking_list')    


def get_available_slots(request):
    print("helooooooooooo")
    from django.http import JsonResponse
    from datetime import time as dt_time

    date_str = request.GET.get('date')
    pincode = request.GET.get('pincode')

    # subcategory_ids support: either comma-separated 'subcategory_ids' or array 'subcategory_ids[]'
    raw_ids = request.GET.get('subcategory_ids')
    list_ids = request.GET.getlist('subcategory_ids[]')
    try:
        if raw_ids:
            subcategory_ids = [int(x) for x in raw_ids.split(',') if x]
        else:
            subcategory_ids = [int(x) for x in list_ids if x]
    except ValueError:
        subcategory_ids = []

    if not date_str:
        return JsonResponse({'error': 'Date is required'}, status=400)

    try:
        # Convert date string to date object
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        aware_start_dt = timezone.make_aware(datetime.combine(date_obj, dt_time.min))
        aware_end_dt = timezone.make_aware(datetime.combine(date_obj, dt_time.max))

        # Get universal slot limit
        universal_slot_obj = UniversalCredential.objects.first()
        universal_limit = universal_slot_obj.universal_slot if universal_slot_obj and universal_slot_obj.universal_slot is not None else 0

        # Resolve subcategories queryset if provided
        subcategories = SubCategory.objects.filter(id__in=subcategory_ids) if subcategory_ids else SubCategory.objects.none()

        response_slots = []

        # First: check for a null slot (slot=None) with limit=0 => block all slots
        null_slots = Slot.objects.filter(date=date_obj, slot=None)
        if subcategories.exists():
            null_slots = null_slots.filter(subcategories__in=subcategories).distinct()
        else:
            null_slots = null_slots.distinct()

        null_slot_blocks_all = False
        for ns in null_slots:
            # zip match or global
            zip_ok = True
            if ns.pincode.exists():
                try:
                    zip_ok = pincode and ns.pincode.filter(code=int(pincode)).exists()
                except Exception:
                    zip_ok = False
            if zip_ok and ns.limit == 0:
                null_slot_blocks_all = True
                break

        if null_slot_blocks_all:
            for slot_number in range(1, 13):
                response_slots.append({
                    "id": slot_number,
                    "display": SLOT_CHOICES_DICT.get(slot_number, f"Slot {slot_number}"),
                    "status": "unavailable",
                    "limit": 0,
                    "current_bookings": 0,
                    "remaining_slots": 0
                })
            return JsonResponse({'slots': response_slots})

        # Process each slot number with pincode/subcategory aware logic
        for slot_number in range(1, 13):
            limit = universal_limit
            matching_slot = None
            slot_qs = Slot.objects.filter(date=date_obj, slot=slot_number)
            if subcategories.exists():
                slot_qs = slot_qs.filter(subcategories__in=subcategories).distinct()
            else:
                slot_qs = slot_qs.distinct()

            if slot_qs.exists():
                for slot_obj in slot_qs:
                    # match zipcode or global
                    if slot_obj.pincode.exists():
                        try:
                            if pincode and slot_obj.pincode.filter(code=int(pincode)).exists():
                                matching_slot = slot_obj
                                break
                        except Exception:
                            pass
                    else:
                        matching_slot = slot_obj
                        break

            # Determine limit and handle explicit zero limit
            slot_added = False
            if matching_slot and matching_slot.limit is not None:
                if matching_slot.limit == 0:
                    response_slots.append({
                        "id": slot_number,
                        "display": SLOT_CHOICES_DICT.get(slot_number, f"Slot {slot_number}"),
                        "status": "unavailable",
                        "limit": 0,
                        "current_bookings": 0,
                        "remaining_slots": 0
                    })
                    slot_added = True
                else:
                    limit = matching_slot.limit

            if slot_added:
                continue

            # Calculate current bookings for this slot
            booking_filter = {
                'booking_date__range': (aware_start_dt, aware_end_dt),
                'slot': slot_number,
            }
            if pincode:
                booking_filter['zipcode'] = pincode

            current_count = Booking.objects.filter(**booking_filter).count()
            remaining = max(0, (limit or 0) - current_count)

            response_slots.append({
                "id": slot_number,
                "display": SLOT_CHOICES_DICT.get(slot_number, f"Slot {slot_number}"),
                "status": "available" if remaining > 0 and (limit or 0) > 0 else "unavailable",
                "limit": limit or 0,
                "current_bookings": current_count,
                "remaining_slots": remaining
            })

        return JsonResponse({'slots': response_slots})

    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


from utils.firebase import send_push_notification

def task_assign(request):
    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        technician_id = request.POST.get('technician_id')

        booking = Booking.objects.get(id=booking_id)
        technician = Technician.objects.get(id=technician_id)
        
        print("BOOKING ID",booking_id)
        print("technician_id",technician_id)
        task = Task.objects.create(booking=booking,technician=technician)
        task.save()
        booking.status = "Assign"
        booking.save()
        if technician and hasattr(technician, "fcm_token") and technician.fcm_token:
            send_push_notification(
                            token=technician.fcm_token,
                            title="Booking Update",
                            body=f"Booking #{booking.id} status updated to {booking.status}",
                            data={"booking_id": str(booking.id), "status": booking.status}
                        )

        messages.success(request,'Assign Task Successfully')
        return redirect('booking_list')
    # 
    # print("technician id",tect_id)
    return redirect('booking_list')


# def list_of_task(request):
#     task = Task.objects.all().order_by("-id")
#     tech = Technician.objects.all()
    
#     new_expert_count = Technician.objects.filter(status="New").count()
#     booking_count = Booking.objects.filter(status = "New").count()
#     rebooking_count = Rebooking.objects.all().count()
#     customer_count = Customer.objects.all().count()

    

#     context = {
#         'task':task,
#         'new_expert_count':new_expert_count,
#         'booking_count':booking_count,
#         'rebooking_count':rebooking_count,
#         'customer_count':customer_count,
#         # 'tech_in_city_and_subcategory': tech_in_city_and_subcategory,  # Add filtered technicians 
#         'tech':tech
        
#     }
#     return render(request,'homofix_app/AdminDashboard/Booking_list/task.html',context)    


# def list_of_task(request):
#     # task = Task.objects.filter(booking__status="Assign").order_by("-created_at")
#     task = Task.objects.filter(booking__status__in=["Assign", "Inprocess", "Reached", "Proceed"]).order_by("-created_at")
#     tech = Technician.objects.all()
    
#     new_expert_count = Technician.objects.filter(status="New").count()
#     booking_count = Booking.objects.filter(status="New").count()
#     rebooking_count = Rebooking.objects.all().count()
#     customer_count = Customer.objects.all().count()

    
#     context = {
#         'task': task,
#         'new_expert_count': new_expert_count,
#         'booking_count': booking_count,
#         'rebooking_count': rebooking_count,
#         'customer_count': customer_count,
#         'tech': tech
#     }

#     return render(request, 'homofix_app/AdminDashboard/Booking_list/task.html', context)

# def list_of_task(request):
#     # Get the search query for technician's name or number
#     search_query = request.GET.get('search', '')  # Get the search term from the URL

#     # Filter tasks based on the status
#     task = Task.objects.filter(booking__status__in=["Assign", "Inprocess", "Reached", "Proceed"]).order_by("-created_at")
    
#     # Filter tasks by technician name or number if a search query exists
#     if search_query:
#         task = task.filter(
#             technician__admin__username__icontains=search_query  # Search by technician's name
#         ) | task.filter(booking__order_id__icontains=search_query) | task.filter(booking__customer__mobile__icontains=search_query)
#         #| task.filter(
#             #technician__number__icontains=search_query  # Or search by technician's number
#         #)

#     # Paginate the task list
#     paginator = Paginator(task, 10)  # Show 10 tasks per page
#     page_number = request.GET.get('page')  # Get the page number from the URL
#     page_obj = paginator.get_page(page_number)  # Get the page object
    
#     # Other counts
#     tech = Technician.objects.all()
#     new_expert_count = Technician.objects.filter(status="New").count()
#     booking_count = Booking.objects.filter(status="New").count()
#     rebooking_count = Rebooking.objects.all().count()
#     customer_count = Customer.objects.all().count()

#     context = {
#         'task': page_obj,  # Pass the page object to the template
#         'new_expert_count': new_expert_count,
#         'booking_count': booking_count,
#         'rebooking_count': rebooking_count,
#         'customer_count': customer_count,
#         'tech': tech,
#         'search_query': search_query  # Pass the search query to the template
#     }

#     return render(request, 'homofix_app/AdminDashboard/Booking_list/task.html', context)


def list_of_task(request):
    search_query = request.GET.get('q') or request.GET.get('search', '')
    tasks_qs = Task.objects.filter(
        booking__status__in=["Assign", "Inprocess", "Reached", "Proceed"]
    ).order_by("-created_at")

    if search_query:
        tasks_qs = tasks_qs.filter(
            Q(technician__admin__username__icontains=search_query) |
            Q(booking__order_id__icontains=search_query) |
            Q(booking__customer__mobile__icontains=search_query)
        )

    from django.core.paginator import Paginator
    paginator = Paginator(tasks_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Build map of matched technicians per task
    task_technician_map = {}
    all_techs = (
        Technician.objects
        .filter(status="Active", showonline__online=True)
        .prefetch_related('working_pincode_areas', 'subcategories')
        .distinct()
    )

    for task in page_obj:
        matched = []
        booking = task.booking
        zipcode = booking.zipcode
        # get subcategory if exists
        subcategory = None
        bps = booking.booking_product.all()
        if bps.exists():
            subcategory = bps.first().product.subcategory

        if zipcode and subcategory:
            for tech in all_techs:
                # check zipcode match
                if tech.working_pincode_areas.filter(code=zipcode).exists():
                    # check subcategory match
                    if tech.subcategories.filter(id=subcategory.id).exists():
                        matched.append(tech)
        # Add even if matched empty
        task_technician_map[task.id] = matched

    context = {
        'task': page_obj,
        'task_technician_map': task_technician_map,
        'search_query': search_query,
        # ... other context as before
    }
    return render(request, 'homofix_app/AdminDashboard/Booking_list/task.html', context)


def delete_of_task(request, id):
    if request.method == "POST":
        cancel_reason = request.POST.get('cancel_reason')

        task = Task.objects.get(id=id)
        task.booking.status = "Cancelled"
        booking_id_task = task.booking.id
        print("taskkkk", booking_id_task)
        booking = Booking.objects.get(id=booking_id_task)
        booking.status = "Cancelled"
        booking.cancel_reason = cancel_reason
        booking.save()
        # task.delete()
        messages.success(request, 'Booking Cancel Successfully!!')

        return redirect("list_of_task")



# def Listofcancel(request):
#     booking = Booking.objects.filter(status="Cancelled").order_by("-id")
#     new_expert_count = Technician.objects.filter(status="New").count()
#     booking_count = Booking.objects.filter(status = "New").count()
#     rebooking_count = Rebooking.objects.all().count()
#     customer_count = Customer.objects.all().count()
    
    
#     context = {
#         'booking':booking,
#         'new_expert_count':new_expert_count,
#         'booking_count':booking_count,
#         'rebooking_count':rebooking_count,
#         'customer_count':customer_count
#     }
#     return render(request,'homofix_app/AdminDashboard/Booking_list/cancel_booking.html',context)    


# def Listofcancel(request):
#     booking = Booking.objects.filter(status="Cancelled").order_by("-id")
#     new_expert_count = Technician.objects.filter(status="New").count()
#     booking_count = Booking.objects.filter(status = "New").count()
#     rebooking_count = Rebooking.objects.count()

#     customer_count = Customer.objects.count()
    
   
    

#     context = {
#         'booking': booking,
#         'new_expert_count': new_expert_count,
#         'booking_count': booking_count,
#         'rebooking_count': rebooking_count,
#         'customer_count': customer_count,
#     }
#     return render(request, 'homofix_app/AdminDashboard/Booking_list/cancel_booking.html', context)

def Listofcancel(request):
    search_query = request.GET.get('q', '')

    # Base queryset with Cancelled status
    booking_list = Booking.objects.filter(status="Cancelled").order_by("-id")

    if search_query:
        booking_list = booking_list.filter(
            Q(order_id__icontains=search_query) |
            Q(booking_customer__icontains=search_query) |
            Q(mobile__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(booking_list, 10)
    page_number = request.GET.get('page')
    booking = paginator.get_page(page_number)

    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status="New").count()
    rebooking_count = Rebooking.objects.count()
    customer_count = Customer.objects.count()

    context = {
        'booking': booking,
        'search_query': search_query,
        'new_expert_count': new_expert_count,
        'booking_count': booking_count,
        'rebooking_count': rebooking_count,
        'customer_count': customer_count,
    }
    return render(request, 'homofix_app/AdminDashboard/Booking_list/cancel_booking.html', context)




def Listofcancel_expert(request):
    query = request.GET.get('q', '')

    # Filter only Cancelled bookings
    task_list = Task.objects.filter(booking__status="Cancelled").order_by("-id")

    if query:
        task_list = task_list.filter(
            Q(booking__order_id__icontains=query) |
            Q(technician__expert_id__icontains=query) |
            Q(booking__customer__admin__first_name__icontains=query) |
            Q(booking__customer__admin__last_name__icontains=query) |
            Q(booking__customer__mobile__icontains=query)
        )

    paginator = Paginator(task_list, 10)
    page_number = request.GET.get('page')
    booking = paginator.get_page(page_number)

    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status="New").count()
    rebooking_count = Rebooking.objects.count()
    customer_count = Customer.objects.count()

    context = {
        'booking': booking,
        'new_expert_count': new_expert_count,
        'booking_count': booking_count,
        'rebooking_count': rebooking_count,
        'customer_count': customer_count,
        'search_query': query
    }

    return render(request, 'homofix_app/AdminDashboard/Booking_list/cancel_booking_expert.html', context)


def cancel_by_expert(request,id):
    booking = Task.objects.filter(booking__status="Cancelled", technician=id).order_by("-id")

    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
   
    # Fetch tasks related to the bookings
    

    context = {
        'booking': booking,
        'new_expert_count': new_expert_count,
        'booking_count': booking_count,
        'rebooking_count': rebooking_count,
        'customer_count': customer_count,
          # Pass tasks to the template
    }

    return render(request,'homofix_app/AdminDashboard/Booking_list/cancel_booking_expert.html',context)    
    
    
  


def reassign(request):
    if request.method == "POST":
        task_id = request.POST.get('task_id')
        technician_id = request.POST.get('reassign_technician')
        
        try:
            task = Task.objects.get(id=task_id)  
            technician = Technician.objects.get(id=technician_id)  
            
            task.technician = technician  
            task.save()  
            
            messages.success(request, 'Reassign Updated successfully ...')
        except Task.DoesNotExist:
            messages.error(request, 'Task not found.')
        except Technician.DoesNotExist:
            messages.error(request, 'Technician not found.')
        
        return redirect('list_of_task')  


def ListofNewExpert(request):
    q = request.GET.get('q', '').strip()
    category = Category.objects.all().order_by("-id")
    technician_qs = Technician.objects.filter(status="New")
    if q:
        technician_qs = technician_qs.filter(
            Q(admin__first_name__icontains=q) |
            Q(admin__last_name__icontains=q) |
            Q(admin__username__icontains=q) |
            Q(mobile__icontains=q) |
            Q(subcategories__name__icontains=q)
        )
    paginator = Paginator(technician_qs.order_by('admin'), 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    
    context = {
        'category' :category,
        'technician':technician,
        'page_obj': page_obj,
        'search_query': q,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count
    }
    return render(request,'homofix_app/AdminDashboard/Notification/New_expert.html',context)




def Listofrebooking(request):
    search_query = request.GET.get('q', '')

    # If there's a search query, filter the rebookings
    if search_query:
        rebooking_list = Rebooking.objects.filter(
            Q(booking_product__booking__order_id__icontains=search_query) |  # Search by Booking ID
            Q(booking_product__booking__customer__admin__first_name__icontains=search_query) |  # Search by Customer First Name
            Q(booking_product__booking__customer__admin__last_name__icontains=search_query) |  # Search by Customer Last Name
            Q(booking_product__booking__customer__mobile__icontains=search_query) |  # Search by Customer Mobile
            Q(technician__admin__username__icontains=search_query) # Search by Customer Mobile
              
        ).order_by("-id")
    else:
        rebooking_list = Rebooking.objects.all().order_by("-id")

    # Apply pagination (e.g. 10 records per page)
    paginator = Paginator(rebooking_list, 10)
    page_number = request.GET.get('page')
    rebooking = paginator.get_page(page_number)

    # Get counts for various entities
    rebooking_count = Rebooking.objects.count()
    customer_count = Customer.objects.count()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status="New").count()

    context = {
        'rebooking': rebooking,
        'rebooking_count': rebooking_count,
        'customer_count': customer_count,
        'new_expert_count': new_expert_count,
        'booking_count': booking_count,
        'search_query': search_query  # Pass the search query back to the template
    }

    return render(request, 'homofix_app/AdminDashboard/Rebooking/list_of_rebooking.html', context)



# def admin_booking_complete(request):
    
   
#     task = Task.objects.filter(booking__status = "Completed").order_by("-id")
#     context = {
#         'task':task,
        
        
#     }
#     return render(request,'homofix_app/AdminDashboard/Rebooking/booking_complete.html',context)    


# def admin_booking_complete(request):
#     task = Task.objects.filter(booking__status="Completed") \
#                        .select_related('booking', 'technician', 'supported_by') \
#                        .defer('description') \
#                        .order_by("-id")
#     invoices = Invoice.objects.filter(booking_id__in=[t.booking.id for t in task])  
#     addon = Addon.objects.filter(booking_prod_id__booking__in=[b.booking.id for b in task])
    


        
#     # print("addonssss",addon)
   
#     context = {
#         'task': task,
#         'invoices': invoices,
#         'addons': addon, 
#     }
#     return render(request, 'homofix_app/AdminDashboard/Rebooking/booking_complete.html', context)

from django.core.paginator import Paginator
from django.shortcuts import render

def admin_booking_complete(request):
    booking_id = request.GET.get('booking_id', '')  # Search input ka value le rahe hain

    # By default sabhi completed bookings fetch karo
    task_list = Task.objects.filter(booking__status="Completed") \
                            .select_related('booking', 'technician', 'supported_by') \
                            .defer('description') \
                            .order_by("-id")

    # Agar booking_id diya gaya hai toh filter karein
    if booking_id:
        # task_list = task_list.filter(booking__order_id__icontains=booking_id,booking__customer__mobile__icontains=booking_id)
        task_list = task_list.filter(
            Q(booking__order_id__icontains=booking_id) | Q(booking__customer__mobile__icontains=booking_id)
        )

    paginator = Paginator(task_list, 10)  # 10 items per page
    page_number = request.GET.get('page')
    tasks = paginator.get_page(page_number)

    invoices = Invoice.objects.filter(booking_id__in=[t.booking.id for t in tasks])
    addon = Addon.objects.filter(booking_prod_id__booking__in=[b.booking.id for b in tasks])

    context = {
        'task': tasks,
        'invoices': invoices,
        'addons': addon,
        'search_query': booking_id,  # Taki input field me search value rahe
    }
    return render(request, 'homofix_app/AdminDashboard/Rebooking/booking_complete.html', context)


def admin_rebooking(request, task_id):
    
    task = get_object_or_404(Task, id=task_id)
    booking_id = task.booking.id
    
    
    
    # user = request.user
    # support = Support.objects.get(admin=user)
    
    booking_products = BookingProduct.objects.filter(booking_id=booking_id).select_related('booking', 'product')
    
    for booking_product in booking_products:
        rebookings = Rebooking.objects.filter(booking_product_id=booking_product.id).order_by('-id')
        booking_product.rebookings.set(rebookings)

    context = {
        'booking_prod': booking_products,
        'support':support,
        'task':task
        
    }
    return render(request, 'homofix_app/AdminDashboard/Rebooking/rebooking.html', context)


def admin_rebooking_update(request):
    if request.method == 'POST':
        booking_product_id = request.POST.get('booking_prod_id')
        booking_date_str = request.POST.get('booking_date')
        slot = request.POST.get('slot')
        
        try:
            # booking_product = BookingProduct.objects.get(booking_id=booking_product_id)
            booking_product = BookingProduct.objects.filter(booking=booking_product_id).first()
            booking = booking_product.booking
            task = Task.objects.get(booking=booking)
        except (BookingProduct.DoesNotExist, Task.DoesNotExist):
            raise Http404('BookingProduct or Task matching query does not exist.')
        
        if booking_date_str and slot:
            try:
                date_only = datetime.strptime(booking_date_str, '%Y-%m-%d').date()
                slot_int = int(slot)
                slot_time_str = dict(SLOT_CHOICES).get(slot_int, "")
                start_time_str = slot_time_str.split(' - ')[0] if slot_time_str else ""
                start_time = datetime.strptime(start_time_str, '%I:%M %p').time() if start_time_str else None
                if start_time:
                    booking_datetime = make_aware(datetime.combine(date_only, start_time))
                    booking.booking_date = booking_datetime
                    booking.slot = slot_int
                    booking.save()
                else:
                    messages.error(request, "Invalid slot selected")
                    return redirect('admin_booking_complete')
            except ValueError:
                messages.error(request, "Invalid date or slot format")
                return redirect('admin_booking_complete')
        else:
            messages.error(request, "Date and slot are required")
            return redirect('admin_booking_complete')

        # create a new rebooking object with the same booking and assign it to the same technician
        rebooking = Rebooking.objects.create(
            booking_product=booking_product,
            technician=task.technician,
            booking_date=booking.booking_date
        )
        
        # update the status of the original booking to "completed"
        # task.booking.status = "completed"
        # task.booking.save()
        
        rebooking.save()
        print("successsss",rebooking)
        messages.success(request, 'Rebooking successfully created.')
        return redirect('admin_booking_complete')

    context = {}
    return render(request, 'homofix_app/AdminDashboard/Rebooking/booking_complete.html', context)


def contactus(request):
    carrer = Carrer.objects.all().order_by("-id")
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'carrer':carrer,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        
    }

    if request.method == "POST":
        career_title = request.POST.get('career_title')
        carrer_desc = request.POST.get('carrer_desc')
        carer = Carrer.objects.create(title = career_title,description=carrer_desc)
        carer.save()
        messages.success(request,'Carrer Add Successfully')
        return redirect('contact_us')

    return render(request,'homofix_app/AdminDashboard/Contactus/contact_us.html',context)



def carrer_update_Save(request):
    if request.method == "POST":
        
        carrer_id = request.POST.get('carrer_id')
        career_title = request.POST.get('career_title')
        carrer_desc = request.POST.get('carrer_desc')
        career_status = request.POST.get('career_status')
        print("ssss",career_status)

        
        carrer = Carrer.objects.get(id=carrer_id)
        carrer.title = career_title
        carrer.description = carrer_desc
        carrer.status = career_status


        # if career_status == "Open":
        #     career_status = True
        #     carrer.status = career_status
        #     print("cccc",career_status)

        # elif career_status == "Close":
        #     career_status = False
        #     print("statusss",career_status)
        #     carrer.status = career_status
        carrer.save()   
            
        # else:
            
        messages.success(request,'Carrer Updated Successfully')
        return redirect('contact_us')


def applicant_carrer(request,id):
    applicant_Carrer = ApplicantCarrer.objects.filter(carrer_id=id)
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'applicant_Carrer':applicant_Carrer,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        
    }

    return render(request,'homofix_app/AdminDashboard/Contactus/applicant_carrer.html',context)
def admin_job_enquiry(request):
    job_enquiry = JobEnquiry.objects.all().order_by("-id")
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'job_enquiry':job_enquiry,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        
    }

    return render(request,'homofix_app/AdminDashboard/JobEnquiry/job_enquiry.html',context)



def admin_share_percentage(request):
    share_percentage = HodSharePercentage.objects.all().order_by("-id")[:3]
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    if request.method == "POST":
        share_amt = request.POST.get('share_amt')
        share = HodSharePercentage.objects.create(percentage=share_amt)
        share.save()
        messages.success(request,'Share Amt add Successfully...')
        return redirect('admin_share_percentage')
    context = {
        'share_percentage':share_percentage,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
    }
    return render(request,'homofix_app/AdminDashboard/SharePercentage/share_percentage.html',context)

def admin_share_percentage_update(request):
    if request.method == "POST":
        hod_share_percentage_id = request.POST.get('hod_share_percentage_id')
        share_amt = request.POST.get('share_amt')
        percentage_id = HodSharePercentage.objects.get(id=hod_share_percentage_id)
        percentage_id.percentage = share_amt
        percentage_id.save()
        messages.success(request,"Percentage updated successfully")
        return redirect('admin_share_percentage')

        
def admin_share_list(request):
    q = request.GET.get('q', '').strip()
    share_qs = (
        Share.objects.all()
        .select_related('task__booking', 'task__technician__admin')
        .prefetch_related(
            Prefetch(
                'task__booking__booking_product',
                queryset=BookingProduct.objects.select_related('product__subcategory__Category_id')
            )
        )
        .order_by('-id')
    )
    if q:
        share_qs = share_qs.filter(
            Q(task__technician__admin__first_name__icontains=q) |
            Q(task__technician__admin__last_name__icontains=q) |
            Q(task__booking__order_id__icontains=q) |
            Q(task__booking__booking_product__product__subcategory__name__icontains=q)
        )
    paginator = Paginator(share_qs, 25)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)


    testint = Share.objects.aggregate(Sum('company_share'))
    
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    final_sum = share_qs.aggregate(Sum('task__booking__final_amount_field'))['task__booking__final_amount_field__sum'] or 0
    ttl = Decimal(final_sum)
        
    context = {
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        # 'share':share,
        'page_obj': page_obj,
        'search_query': q,
        'ttl':ttl,
        'testint':testint
    }

    return render(request,'homofix_app/AdminDashboard/SharePercentage/list_of_share.html',context)


def admin_share_percentage_delete(request,id):
    share_percentage = HodSharePercentage.objects.get(id=id)
    share_percentage.delete()
    messages.success(request, "Share Percentage deleted successfully.")
    return redirect('admin_share_percentage')


def admin_customer_list(request):
    search_query = request.GET.get('q', '')

    # If there's a search query, filter the customers
    if search_query:
        customer_list = Customer.objects.filter(
            Q(admin__first_name__icontains=search_query) |  # Search by First Name
            Q(admin__last_name__icontains=search_query) |  # Search by Last Name
            Q(mobile__icontains=search_query)  # Search by Mobile Number
        ).order_by('-id')
    else:
        customer_list = Customer.objects.all().order_by('-id')

    # Apply pagination (e.g. 10 records per page)
    paginator = Paginator(customer_list, 10)
    page_number = request.GET.get('page')
    customer = paginator.get_page(page_number)

    # Get counts for various entities
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status="New").count()
    rebooking_count = Rebooking.objects.count()
    customer_count = Customer.objects.count()

    context = {
        'customer': customer,
        'new_expert_count': new_expert_count,
        'booking_count': booking_count,
        'rebooking_count': rebooking_count,
        'customer_count': customer_count,
        'search_query': search_query  # Pass the search query back to the template
    }

    return render(request, 'homofix_app/AdminDashboard/Customer/customer_list.html', context)
    
def admin_customer_edit(request,id):
    state_choices = STATE_CHOICES
    customer = Customer.objects.get(id=id)
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mob_no')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        area = request.POST.get('area')
        zipcode = request.POST.get('zipcode')
        gst_no = request.POST.get('gst_no')
        customer.admin.first_name = first_name
        customer.admin.email = email
        customer.mobile = mobile
        customer.city = city
        customer.state = state
        customer.area = area
        customer.gst_no = gst_no
        if zipcode:
            customer.zipcode = zipcode
        
        customer.address = address
        customer.save()
        messages.success(request,'Customer Updated Successfully..')
        return redirect('admin_customer_edit', id=customer.id)
         
    context = {
        'customer':customer,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        'state_choices':state_choices,

    }

    return render(request,'homofix_app/AdminDashboard/Customer/edit_customer.html',context)    

def admin_customer_history(request,id):
    customer = Customer.objects.get(id=id)
    
    booking = Booking.objects.filter(customer_id=id).order_by("-id")
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    payment = Payment.objects.filter(booking_id__in=booking).order_by("-id")
    
   
    context = {
        'customer':customer,
        'booking':booking,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        'payment':payment
    }


    return render(request,'homofix_app/AdminDashboard/History/CustomerHistory/customer_history.html',context)


# --------------------------- Customer Payment Details -----------------------------    

def admin_customer_payment(request):
    q = request.GET.get('q', '').strip()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    payment_qs = Payment.objects.all().order_by("-id")
    if q:
        payment_qs = payment_qs.filter(
            Q(booking_id__order_id__icontains=q) |
            Q(booking_id__customer__admin__username__icontains=q) |
            Q(booking_id__customer__admin__first_name__icontains=q) |
            Q(booking_id__customer__admin__last_name__icontains=q) |
            Q(booking_id__customer__mobile__icontains=q) 
        )

    paginator = Paginator(payment_qs, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)



    context = {
        # 'payment':payment,
        'page_obj': page_obj,
        'search_query': q,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
    }

    return render(request,'homofix_app/AdminDashboard/CustomerPayment/list_of_payment.html',context)


       

        # if old_psw and new_psw:
        #     if user.check_password(old_psw):
        #         if new_psw == confirm_psw:

        #             user.set_password(new_psw)
        #             messages.success(request,'success: password changed')
        #             return redirect('admin_reset_psw')
        #             # print("success: password changed")
        #         else:
        #             messages.error(request,'password not match')
        #             return redirect('admin_reset_psw')
        #             # print("password not match")
        #     else:
        #         messages.error(request,'old password does not match')
        #         return redirect('admin_reset_psw')
                # print("error: old password does not match")
    # return render(request,'homofix_app/Authentication/reset_psw.html')


# ------------------------------- Withdraw Request ----------------------     

def admin_withdraw_request(request):
    q = request.GET.get('q', '').strip()
    withdraw_req_qs = WithdrawRequest.objects.all()
    if q:
        withdraw_req_qs = withdraw_req_qs.filter(
            Q(technician_id__admin__username__icontains=q) |
            Q(technician_id__admin__first_name__icontains=q) |
            Q(technician_id__admin__last_name__icontains=q) |
            Q(technician_id__admin__email__icontains=q) |
            Q(technician_id__mobile__icontains=q) |
            Q(technician_id__expert_id__icontains=q)
        )

    paginator = Paginator(withdraw_req_qs, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)


    context = {
        'page_obj': page_obj,
        'search_query': q,

    }
    return render(request,'homofix_app/AdminDashboard/Withdraw/withdraw_request.html',context)



    
def expert_cancel_withraw_request(request,withdraw_id):
    withdraw_req=WithdrawRequest.objects.get(id=withdraw_id)
    withdraw_req.status="Cancel"
    withdraw_req.save()
    return HttpResponseRedirect(reverse("admin_withdraw_request"))

    
def expert_accept_withraw_request(request,withdraw_id):
    withdraw_req=WithdrawRequest.objects.get(id=withdraw_id)
    withdraw_req.status="Accept"
    withdraw_req.save()
    return HttpResponseRedirect(reverse("admin_withdraw_request"))



# ------------------------------------------- Recharge ---------------- 

def recharge(request):
    
    q = request.GET.get('q', '').strip()

    recharge_qs = RechargeHistory.objects.all().order_by('-id')
    if q:
        recharge_qs = recharge_qs.filter(
            Q(technician_id__expert_id__icontains=q) |
            Q(technician_id__admin__username__icontains=q) |
            Q(technician_id__admin__first_name__icontains=q) |
            Q(technician_id__admin__last_name__icontains=q) |
            Q(technician_id__mobile__icontains=q)
        ).order_by('-id')
    paginator = Paginator(recharge_qs, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)


    context = {
        'page_obj': page_obj,
        'search_query': q,
    }
    return render(request,'homofix_app/AdminDashboard/Recharge/list_of_recharge.html',context)



# ------------------------------ Attendance ------------------------ 

def attendence(request,id):

    attendence = Attendance.objects.filter(support_id=id)
    context = {
        'attendence':attendence
    }
    return render(request,'homofix_app/AdminDashboard/Attendence/list_of_attendence.html',context)
    
    


def recharge_technicianwise(request,id):
    recharge = RechargeHistory.objects.filter(technician_id=id)

    context = {
        'recharge':recharge
    }
    return render(request,'homofix_app/AdminDashboard/Recharge/list_of_recharge.html',context)



# ------------------------------ Coupon ------------------------ 


def coupon(request):
    
    
    coupon = Coupon.objects.all()
    context = {
        'coupon':coupon
    }
    return render(request,'homofix_app/AdminDashboard/Coupon/coupon.html',context)

def coupon_save(request):
    if request.method == "POST":
        code = request.POST.get('code') 
        discount_amt = request.POST.get('discount_amt') 
        validity_period = request.POST.get('validity_period') 

        code = Coupon.objects.create(code=code,discount_amount=discount_amt,validity_period=validity_period)
        code.save()
        messages.success(request,'Coupon Code Add Succesfull')
        return redirect('coupon')


def coupon_update(request,id):
    if request.method == "POST":
       
        code = request.POST.get("code")
        discount_amt = request.POST.get("discount_amt")
        validity_period = request.POST.get("validity_period")

        coupon = Coupon.objects.get(id=id)
        coupon.code = code
        coupon.discount_amount=discount_amt
        coupon.validity_period=validity_period
        coupon.save()
        messages.success(request,"Coupon code Updated..")
        return redirect('coupon')



def coupon_delete(request,id) :
    coupon = Coupon.objects.get(id=id)
    coupon.delete()
    messages.success(request,"Coupon Deleted..")
    return redirect('coupon')



def add_blog(request):
    if request.method == "POST":
        title = request.POST.get('title')
        feature_img = request.FILES.get('feature_img')
        content = request.POST.get('content')
        print("feature img",feature_img)
        blog = Blog.objects.create(title=title,feature_img=feature_img,content=content)
        messages.success(request,'Blog Add Successfully')
        return redirect('view_blog')
        
    return render(request,'homofix_app/AdminDashboard/Blog/add_blog.html')


def edit_blog(request,id):
    blog = Blog.objects.get(id=id)
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'blog':blog,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count
    }

    return render(request,'homofix_app/AdminDashboard/Blog/edit_blog.html',context)


def blog_update(request):

    if request.method == "POST":
        blog_id = request.POST.get('blog_id')
        title = request.POST.get('title')
        feature_img = request.FILES.get("feature_img")
        content = request.POST.get('content')
        blog = Blog.objects.get(id=blog_id)
        blog.title = title
        if feature_img: 
            blog.feature_img = feature_img
        blog.content = content
        blog.save()
        messages.success(request,"Blog Updated are successfully")
        return redirect('view_blog')
        

def view_blog(request):
    blog = Blog.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    
    context = {
        'blog':blog,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count

    }

    return render(request,'homofix_app/AdminDashboard/Blog/view_blog.html',context)


def delete_blog(request,id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    messages.success(request,"Blog Delete Successfully")
    return redirect('view_blog')






def view_offers(request):
    offer = Offer.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    
    context = {
        'offer':offer,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count

    }

    return render(request,'homofix_app/AdminDashboard/Offers/view_offers.html',context)



def add_offers(request):
    if request.method == "POST":
        offer_name = request.POST.get('offer_name')
        offer_img = request.FILES.get('offer_img')
        offer_url = request.POST.get('offer_url')
        print("feature img",offer_url)
        offer = Offer.objects.create(name=offer_name,offer_pic=offer_img,url=offer_url)
        messages.success(request,'Offer Add Successfully')
        return redirect('view_offers')
        
    return render(request,'homofix_app/AdminDashboard/Offers/add_offer.html')


def edit_offers(request,id):
    offer = Offer.objects.get(id=id)
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'offer':offer,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count
    }

    return render(request,'homofix_app/AdminDashboard/Offers/edit_offer.html',context)




def offer_update(request):

    if request.method == "POST":
        offer_id = request.POST.get('offer_id')
        offer_name = request.POST.get('offer_name')
        offer_img = request.FILES.get('offer_img')
        offer_url = request.POST.get('offer_url')
        offer = Offer.objects.get(id=offer_id)
        offer.name = offer_name
        if offer_img: 
            offer.offer_pic = offer_img
        offer.url = offer_url
        offer.save()
        messages.success(request,"Offer Updated are successfully")
        return redirect('view_offers')
        



def delete_offer(request,id):
    offer = Offer.objects.get(id=id)
    offer.delete()
    messages.success(request,"Offer Delete Successfully")
    return redirect('view_offers')



def ViewPDF(request,booking_id):
    
    import os
        
    if os.path.exists('last_invoice_number.txt'):
        with open('last_invoice_number.txt', 'r') as f:
            last_invoice_number = int(f.read().strip())
    else:
        last_invoice_number = 0

# Increment the last invoice number
    new_invoice_number = f'INV-{last_invoice_number+1:03d}'

# Save the new invoice number to the file
    with open('last_invoice_number.txt', 'w') as f:
        f.write(str(last_invoice_number+1))

# Print the new invoice number
    print("newwwwww",new_invoice_number)
    # print("ggggg")
    book_id = Booking.objects.get(id=booking_id)

    filename  = f"invoice_{book_id.order_id}.pdf"
    my_path = os.path.join(settings.MEDIA_ROOT, filename)
    # my_path = f"F:\\Homofix\\v75\\invoice_{book_id.order_id}.pdf"
    print("my path",my_path)
    # filename = f"invoice_{instance.order_id}.pdf"
    doc = SimpleDocTemplate(my_path, pagesize=letter,topMargin=0)

    
    # Add the title to the document
    para_style2 = ParagraphStyle(
    'title',
    fontSize=15,
    leading=20,
    alignment=TA_CENTER,  # align text to the left
    textColor=colors.black,
    spaceBefore=0,  # no space before the paragraph
    spaceAfter=12,
)

    
    title = Paragraph('LIST OF ITEM', para_style2)
    addon_title = Paragraph('LIST OF Addon', para_style2)
    inv = Paragraph('Invoice',para_style2)
    title.spaceBefore = 0  # set spaceBefore to zero
    addon_title.spaceBefore = 0  # set spaceBefore to zero
     # Create the table for bill to information
    bookingid=Booking.objects.get(id=booking_id)
    # styles = getSampleStyleSheet()
    address_lines = bookingid.customer.address.split('\n')
    bill_to_data = [    ['Bill To:', bookingid.customer.admin.first_name],
        ['Address:', Paragraph(bookingid.customer.address)],
        ['Mobile:', f'+91{bookingid.customer.mobile}' ],
        ['Email:', bookingid.customer.admin.email],
    ]
    
    bill_to_table = Table(bill_to_data, hAlign='LEFT')
    


# Apply the bill to table style
    # bill_to_style = TableStyle([    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),    ('FONTSIZE', (0, 0), (-1, -1), 11),    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),])

    bill_to_style = TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    # ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    
    ('LINEAFTER', (1, 0), (1, -1), 0.5, colors.black),
])

    bill_to_table.setStyle(bill_to_style)

    # Get the last invoice number from a file
    
# Create the table for invoice details
    invoice_data = [    ['Invoice No:', 'INV-001'],
        ['Invoice Date:', '18-Apr-2023'],
        # ['Due Date:', '30-Apr-2023'],
    ]

    invoice_table = Table(invoice_data, colWidths=[150, None], hAlign='LEFT')



    # Apply the invoice table style
    # invoice_style = TableStyle([    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),    ('FONTSIZE', (0, 0), (-1, -1), 11),    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),])
    invoice_style = TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
])

    invoice_table.setStyle(invoice_style)
    
    nested_table_style = TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('BOX', (0, 0), (-1, -1), 1, colors.black),
])

    # Create the nested table with two columns and one row
    nested_table_data = [[bill_to_table, invoice_table]]
    nested_table = Table(nested_table_data, colWidths=[250, 250])
    nested_table.setStyle(nested_table_style)


    # Define the table data
    
    data = [['Product Name', 'Qty','RATE','TAX','AMOUNT'],]
    addon = [['Addon Name', 'Qty','RATE','TAX','AMOUNT'],]
    bookingProd=BookingProduct.objects.filter(booking=booking_id)
    adon = Addon.objects.filter(booking_prod_id__booking=booking_id)
    # stu = Booking.objects.all()
    for bookingprod in bookingProd:

        price = 0
        if bookingprod.product.selling_price != None:
            price = bookingprod.product.selling_price
        else:
            price = bookingprod.product.price
        
        data.append([bookingprod.product.name, bookingprod.quantity,price,'18%',f'{bookingprod.quantity*price*1.18:.2f}'])
        # data.append([bookingprod.product.name, bookingprod.quantity,price,'18%',bookingprod.quantity*price*1.18])
        for i in adon:
            if i.spare_parts_id.product == bookingprod.product:
                # addon.append([i.spare_parts_id.spare_part,i.quantity,i.spare_parts_id.price,'18%',i.quantity*i.spare_parts_id.price*1.18])
                addon.append([i.spare_parts_id.spare_part, i.quantity, i.spare_parts_id.price, '18%', f'{i.quantity * i.spare_parts_id.price * 1.18:.2f}'])


        # if i.spare_parts_id.product ==  bookingprod.product:
        #     addon.append([i.spare_parts_id.spare_part])
            
        
#     data.append(['Ac Repairing', '2','100','18%','200'])
        

    # Create the table
    # col_widths = [100, 100]
    col_widths = [270, 30, 75, 50, 70]
    table = Table(data,colWidths=col_widths)
    addon_col_widths = [270, 30, 75, 50, 70]
    addontable = Table(addon,colWidths=addon_col_widths)

    # Apply the table style
    style = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        # ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        # ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        # ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        # ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
    ])
    table.setStyle(style)
    
    addonstyle = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        # ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        # ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        # ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
    ])
    addontable.setStyle(addonstyle)
    

    # Define the paragraph style
    para_style = ParagraphStyle(
        'title',
        fontSize=18,
        leading=24,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceBefore=12,
        spaceAfter=12,
    )
    
    
    logo_path = os.path.join(settings.MEDIA_ROOT, 'LOGO2.jpeg')

    
    
    logo = Image(logo_path, width=1.5*inch, height=1.5*inch)
    logo.hAlign = 'LEFT'



    
    
    # Create the table for invoice totals
    booking = Booking.objects.get(id=booking_id)
    tax_rate = 0.18
    total_price = total_price = booking.total_amount
    print("ttoaalll",total_price)
    gst = int(total_price * 18)/100
    total = total_price + Decimal(str(gst))
    # print("gsstttt",gst)

    invoice_totals_data = [    ['Subtotal:', f'{total_price:.2f}'],
        ['CGST @9%:', f'{gst/2:.2f}'],
        ['SGST @9%:', f'{gst/2:.2f}'],
        ['Total:', f'{total:.2f}'],
    ]

    invoice_totals_table = Table(invoice_totals_data, colWidths=[90, None], hAlign='RIGHT')

# Apply the invoice totals table style
    # invoice_totals_style = TableStyle([    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),    ('FONTSIZE', (0, 0), (-1, -1), 11),    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),])
    invoice_totals_style = TableStyle([    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),    ('FONTSIZE', (0, 0), (-1, -1), 11),    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),    ('LINEABOVE', (0, 3), (-1, 3), 1, colors.black),('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),])
    invoice_totals_table.setStyle(invoice_totals_style)


    # Create the table for company information
    company_data = [        [''],  # Add an empty row before the company information
        [f'{"Homofix Technologies PVT Ltd":^65}'],
        # [''],
        [f'{"Corporate Office: 2nd Floor, WP-501-D, Unit 209, Shiv Market, Wazirpur Village ,":^50}'],
        [f'{"Ashok Vihar, New Delhi, Central Delhi, Delhi, 110052":^90}'],
        [f'{"Regd Office: 5139, Awas Vikas 3, Kalyanpur,Kanpur,Uttar Pradesh, India,208017":^50}'],
        [f'{"GSTIN:07AAGCH4863F1Z1":^110}'],

        # ['Ashok Vihar Delhi,New Delhi 110052'],
        # [ '+1 (555) 987-6543'],
        # ['info@abccorp.com'],
    ]
    

    # company_table = Table(company_data, colWidths=[90, None])
    company_table = Table(company_data, colWidths=[doc.width, 0])

    # Apply the company table style
 
    # Apply the company table style
    company_style = TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),  # Add line below style to the first row
    ('FONTSIZE', (0, 1), (-1, -1), 20),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
    ('TOPPADDING', (0, 0), (0, 0), 6),  # Add top padding to the first cell of the first row
    ('LEFTPADDING', (0, 0), (0, 0), 50),  # Add left padding to the first cell of the first row
    ('ALIGN', (0, 0), (0, 0), 'CENTER'),  # Align the first cell of the first row to the center
    # ('TEXTCOLOR', (0, 0), (-1, -1), colors.blue),
    # ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid style to all cells
    ('FONTSIZE', (0, 2), (-1, 2), 12),
    ('FONTSIZE', (0, 3), (-1, 3), 12),
    ('TOPPADDING', (0, 3), (-1, 3), -8),
    ('FONTSIZE', (0, 4), (-1, 4), 12),
    ('FONTSIZE', (0, 5), (-1, 5), 12),
    ('TOPPADDING', (0, 5), (-1, 5), -6),
    # ('LINEBELOW', (-1, -1), (-1, -1), 1, colors.black)  # Add line below style to the last row
])
    company_table.setStyle(company_style)

   
    # doc = SimpleDocTemplate(f'invoice{}.pdf', topMargin=0)

    doc.build([inv,logo, nested_table, Spacer(1, 0.*inch),title, table,Spacer(1, 0.1*inch),addon_title,addontable, Spacer(1, 0.5*inch), invoice_totals_table, Spacer(1, 0.5*inch), company_table])
    import os
    if os.path.exists(my_path):
        with open(my_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="invoice.pdf"'
            return response
    # else:
    #     return HttpResponse("The requested file does not exist.")

    return HttpResponse("Invoice generated successfully")        




def most_view_list(request):
    mst_View = MostViewed.objects.all()
    context = {
        'mst_View':mst_View
    }
    return render(request,'homofix_app/AdminDashboard/MostViewed/view_mostViewed.html',context)

def add_mostViewed(request):
    subcategory = SubCategory.objects.all()
    context = {
        'subcategory': subcategory
    }
    if request.method == "POST":
        # product_ids = request.POST.get('product_id')
        subcategory_ids = request.POST.getlist('subcategory_id[]')
        most_view_pics = request.FILES.getlist('most_img[]')

        print("mooss",most_view_pics)
        # prod = Product.objects.get(id=product_ids)
        # print("hello")

        # for name in most_view_pics:
        #     mst = MostViewed.objects.create(proudct=prod, img=name)
        #     mst.save()

        for subcategory_id, image in zip(subcategory_ids, most_view_pics):
            subcat_id = SubCategory.objects.get(id=subcategory_id)

            # Create a new MostViewed object for each product and image
            mst = MostViewed.objects.create(subccategry_id=subcat_id, img=image)
            mst.save()
        messages.success(request,"MostViewed Add Successfully")
        return redirect('most_view_list')
            

        # Limit the number of entries to a maximum of four
        

    
    return render(request, 'homofix_app/AdminDashboard/MostViewed/add_mostViewed.html', context)

        


def edit_mostViewed(request,id):
    mst_view = MostViewed.objects.get(id=id)
    subcategory = SubCategory.objects.all()
    
    context= {
        'mst_view':mst_view,
        'subcategory':subcategory
    }
    return render(request, 'homofix_app/AdminDashboard/MostViewed/edit_most_viewed.html', context)


def update_Save_mostViewed(request):
    if request.method == "POST":
        mst_view_id = request.POST.get('mst_view_id')
        subcategory_id = request.POST.get('subcategory_id')
        mst_view_pic = request.FILES.get('most_img')

        subcat = SubCategory.objects.get(id=subcategory_id)
        most_viewed = MostViewed.objects.get(id=mst_view_id)
        if mst_view_pic:
            most_viewed.img = mst_view_pic
        
        most_viewed.subccategry_id = subcat

        most_viewed.save()
        messages.success(request,"Most Viewed Updted Successfully")
        return redirect('most_view_list')



def homepageservice_view_list(request):
    home_page_Service = HomePageService.objects.all()
    context = {
        'home_page_Service':home_page_Service
    }
    return render(request,'homofix_app/AdminDashboard/HomePageService/view_homepage_service.html',context)



def add_homepage_service(request):
    category = Category.objects.all()
    
    context = {
        'category': category
    }
    if request.method == "POST":
        # product_ids = request.POST.get('product_id')
        category_ids = request.POST.getlist('category_id[]')
        title = request.POST.getlist('title[]')
        print("category idss",category_ids,"title",title)

        # print("mooss",most_view_pics)
        # prod = Product.objects.get(id=product_ids)
        # print("hello")

        # for name in most_view_pics:
        #     mst = MostViewed.objects.create(proudct=prod, img=name)
        #     mst.save()

        for category_id, image in zip(category_ids, title):
            prod = Category.objects.get(id=category_id)

            # Create a new MostViewed object for each product and image
            mst = HomePageService.objects.create(category_id=prod, title=image)
            mst.save()
        messages.success(request,"HomePageService Add Successfully")
        return redirect('homepageservice_view_list')
            

        # Limit the number of entries to a maximum of four
        

    
    return render(request, 'homofix_app/AdminDashboard/HomePageService/add_homepage_service.html', context)




def edit_homepage_service(request,id):
    homepageservice = HomePageService.objects.get(id=id)
    
    category = Category.objects.all()
    print("Category",category)
    context= {
        'homepageservice':homepageservice,
        'category':category
    }
    return render(request, 'homofix_app/AdminDashboard/HomePageService/edit_homepage_service.html', context)




def update_Save_homepageservice(request):
    if request.method == "POST":
        homepageservice_id = request.POST.get('homepageservice_id')
        category_id = request.POST.get('category_id')
        title = request.POST.get('title')

        cat = Category.objects.get(id=category_id)
        homepageservice = HomePageService.objects.get(id=homepageservice_id)
        
        
        homepageservice.category_id = cat
        homepageservice.title = title

        homepageservice.save()
        messages.success(request,"Home Page Service Updted Successfully")
        return redirect('homepageservice_view_list')


# ----------------------------------- PAGE LEGAL ----------------- 

def page_legal_list(request):
    
    
    pagelegal = LegalPage.objects.all()
    entry_count = LegalPage.objects.count()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    booking_complete = Booking.objects.filter(status = "Completed").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'booking_complete':booking_complete,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        'pagelegal':pagelegal,
        'entry_count': entry_count,
        
    }
    return render(request, 'homofix_app/AdminDashboard/PageLegal/page_legal_list.html', context)

# def add_page_legal(request):
#     subcategory = SubCategory.objects.all()
#     new_expert_count = Technician.objects.filter(status="New").count()
#     booking_count = Booking.objects.filter(status = "New").count()
#     booking_complete = Booking.objects.filter(status = "Completed").count()
#     rebooking_count = Rebooking.objects.all().count()
#     customer_count = Customer.objects.all().count()
#     if request.method == "POST":
#         title = request.POST.get('title')
#         content = request.POST.get('content')
#         subcategory_id = request.POST.get('subcategory_id')
#         home = request.POST.get('home')== 'on'
#         can_contact = request.POST.get('can_contact')== 'on'
#         subcat = None
#         if subcategory_id:

#             subcat = SubCategory.objects.get(id=subcategory_id)
#             print(f"subcategory {subcategory_id} contact {can_contact} home {home}")
#         legal_page = LegalPage.objects.create(title=title,content=content,subcategory=subcat,home=home,contact=can_contact )
       
#         legal_page.save()
#         messages.success(request,'Legal Page Add Successfully')
#         return redirect('page_legal_list')

#     context = {
#         'new_expert_count':new_expert_count,
#         'booking_count':booking_count,
#         'booking_complete':booking_complete,
#         'rebooking_count':rebooking_count,
#         'customer_count':customer_count,
#         'subcategory':subcategory,
        
#     }

#     return render(request, 'homofix_app/AdminDashboard/PageLegal/add_page_legal.html', context)


def add_page_legal(request):
    subcategory = SubCategory.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status="New").count()
    booking_complete = Booking.objects.filter(status="Completed").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        subcategory_id = request.POST.get('subcategory_id')
        home = request.POST.get('home') == 'on'
        can_contact = request.POST.get('can_contact') == 'on'

        subcat = None  # Default value set kar diya

        if subcategory_id:
            try:
                subcat = SubCategory.objects.get(id=subcategory_id)
                print(f"subcategory {subcategory_id} contact {can_contact} home {home}")
            except SubCategory.DoesNotExist:
                messages.error(request, "Invalid subcategory selected.")
                return redirect('page_legal_list')

        legal_page = LegalPage.objects.create(
            title=title,
            content=content,
            subcategory=subcat,
            home=home,
            contact=can_contact
        )

        messages.success(request, 'Legal Page Added Successfully')
        return redirect('page_legal_list')

    context = {
        'new_expert_count': new_expert_count,
        'booking_count': booking_count,
        'booking_complete': booking_complete,
        'rebooking_count': rebooking_count,
        'customer_count': customer_count,
        'subcategory': subcategory,
    }

    return render(request, 'homofix_app/AdminDashboard/PageLegal/add_page_legal.html', context)


def edit_page_legal(request,id):

    subcategory = SubCategory.objects.all()
    legalpage = LegalPage.objects.get(id=id)
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    booking_complete = Booking.objects.filter(status = "Completed").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()



    context = {
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'booking_complete':booking_complete,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        'legalpage':legalpage,
        'subcategory':subcategory,
        
    }

    return render(request, 'homofix_app/AdminDashboard/PageLegal/edit_page_legal.html', context)


# def update_page_legal_save(request):
#     if request.method == "POST":
#         print("ehlooooo")
#         legal_page_id = request.POST.get('legalpage_id')    
#         title = request.POST.get('title')    
#         content = request.POST.get('content')
        
#         subcategory_id = request.POST.get('subcategory_id')

#         home = request.POST.get('home')== 'on'
#         can_contact = request.POST.get('can_contact')== 'on'
#         if subcategory_id:
#             subcat = SubCategory.objects.get(id=int(subcategory_id))
#         else:
#             subcat = None
#         subcat = SubCategory.objects.get(id=subcategory_id)    

#         legalpage = LegalPage.objects.get(id=legal_page_id)
#         legalpage.title = title
#         legalpage.content = content
#         legalpage.home = home
#         legalpage.contact = can_contact
#         legalpage.subcategory = subcat
#         legalpage.save()

#         print("id",legal_page_id,"title",title,'content',content,"subcategory",subcat,"home",home,"contact",can_contact)
#         messages.success(request,'Page Legal Updtaed Successfully')
#         return redirect('page_legal_list')



def update_page_legal_save(request):
    if request.method == "POST":
        print("ehlooooo")
        
        legal_page_id = request.POST.get('legalpage_id')    
        title = request.POST.get('title')    
        content = request.POST.get('content')        
        subcategory_id = request.POST.get('subcategory_id')

        home = request.POST.get('home') == 'on'
        can_contact = request.POST.get('can_contact') == 'on'

        # Validate legal_page_id
        if not legal_page_id:
            messages.error(request, "Invalid Legal Page ID")
            return redirect('page_legal_list')

        # Get LegalPage or return 404
        legalpage = get_object_or_404(LegalPage, id=int(legal_page_id))

        # Get SubCategory if exists, otherwise set None
        subcat = None
        if subcategory_id:
            try:
                subcat = SubCategory.objects.get(id=int(subcategory_id))
            except SubCategory.DoesNotExist:
                messages.error(request, "Selected Subcategory does not exist")
                return redirect('page_legal_list')

        # Update LegalPage
        legalpage.title = title
        legalpage.content = content
        legalpage.home = home
        legalpage.contact = can_contact
        legalpage.subcategory = subcat
        legalpage.save()

        print("id", legal_page_id, "title", title, 'content', content, "subcategory", subcat, "home", home, "contact", can_contact)
        
        messages.success(request, 'Page Legal Updated Successfully')
        return redirect('page_legal_list')

    else:
        messages.error(request, "Invalid request method")
        return redirect('page_legal_list')


def delete_page_legal(request,id):
    page_legal = LegalPage.objects.get(id=id)
    page_legal.delete()
    messages.success(request,'Successfull Deleted !!')

    return redirect('page_legal_list')

def test(request):
    category = Category.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context= {
        'category':category,
        'new_expert_count':new_expert_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
    }
    # return render(request,'homofix_app/AdminDashboard/Category/category.html',{'category':category,'new_expert_count':new_expert_count,'rebooking_count':rebooking_count,'customer_count':customer_count})

    return render(request,'test.html',context)



def testing(request):
    return render(request,'test.html')    





def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None







def read_invoice_counter():
    try:
        with open('invoice_counter.txt', 'r') as file:
            counter = int(file.read())
    except FileNotFoundError:
        counter = 1
    return counter


def write_invoice_counter(counter):
    with open('invoice_counter.txt', 'w') as file:
        file.write(str(counter))
    

# def new_invoice(request, booking_id):
#     # Retrieve the Booking object based on the booking_id
#     booking = get_object_or_404(Booking, id=booking_id)

#     # Read the current invoice counter from the file
#     invoice_counter = read_invoice_counter()

#     # Convert the invoice counter to a string
#     invoice_number = str(invoice_counter)
    
#     # Render the template with the booking data
#     html_content = render_to_string('Invoice/invoice.html', {'booking': booking,'invoice_number':invoice_number})

#     input_file = None  # We will pass the HTML content directly
#     output_file = f'file{invoice_number}.pdf'
#     options = {
#         "enable-local-file-access": ""
#     }

#     # Generate the PDF from the HTML content
#     import os
#     if os.path.exists(output_file):
#         with open(output_file, 'rb') as pdf:
#             response = HttpResponse(pdf.read(), content_type='application/pdf')
#             response['Content-Disposition'] = 'inline; filename="invoice.pdf"'
#             return response
#     pdfkit.from_string(html_content, output_file, options=options)
    

#     # Increment the invoice counter for the next invoice
#     invoice_counter += 1

#     # Write the updated invoice counter back to the file
#     write_invoice_counter(invoice_counter)

#     # Return a response or redirect as needed
#     import os
#     if os.path.exists(output_file):
#         with open(output_file, 'rb') as pdf:
#             response = HttpResponse(pdf.read(), content_type='application/pdf')
#             response['Content-Disposition'] = 'inline; filename="invoice.pdf"'
#             return response
#     return HttpResponse("PDF generated successfully")


def invoice_download(request, booking_id):

    try:
        # invoice = Invoice.objects.get(booking_id=booking_id)
        invoice = Invoice.objects.filter(booking_id=booking_id).first()
        invoice_data = invoice.invoice if invoice else None

        if invoice_data:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
            response.write(invoice_data)
            return response
        else:
            return HttpResponse("Invoice not found.")
    except Invoice.DoesNotExist:
        return HttpResponse("Invoice not found.")
    
    # # Retrieve the Booking object based on the booking_id
    # booking = get_object_or_404(Booking, id=booking_id)

    # # Read the current invoice counter from the file
    # invoice_counter = read_invoice_counter()

    # # Convert the invoice counter to a string
    # invoice_number = str(invoice_counter)

    # # Render the template with the booking data
    # html_content = render_to_string('Invoice/invoice.html', {'booking': booking, 'invoice_number': invoice_number})

    # # Define the PDF file path
    # output_file = f'invoice{invoice_number}.pdf'

    # # Check if the PDF file already exists
    # if os.path.isfile(output_file):
       
    #     with open(output_file, 'rb') as pdf:
    #         response = HttpResponse(pdf.read(), content_type='application/pdf')
    #         response['Content-Disposition'] = 'inline; filename="invoice.pdf"'
    #         return response

    # # Generate the PDF from the HTML content
    # options = {
    #     "enable-local-file-access": ""
    # }
    # pdfkit.from_string(html_content, output_file, options=options)

    # # Increment the invoice counter for the next invoice
    # invoice_counter += 1

    # # Write the updated invoice counter back to the file
    # write_invoice_counter(invoice_counter)

    # # Return the generated PDF as a response
    # with open(output_file, 'rb') as pdf:
    #     print("testinggggggggg")
    #     response = HttpResponse(pdf.read(), content_type='application/pdf')
    #     response['Content-Disposition'] = 'inline; filename="invoice.pdf"'
    #     return response

    # Return a response or redirect as needed
    # return HttpResponse("PDF generated successfully")





from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@csrf_exempt  # Disable CSRF for testing (only if needed)
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        image = request.FILES['upload']
        
        # Save the uploaded image in media/uploads/
        file_path = default_storage.save('uploads/' + image.name, ContentFile(image.read()))
        image_url = default_storage.url(file_path)

        return JsonResponse({
            'uploaded': 1,
            'fileName': image.name,
            'url': image_url
        })  # CKEditor requires this JSON format

    return JsonResponse({'uploaded': 0, 'error': {'message': 'Invalid request'}}, status=400)


import pandas as pd
from django.utils.timezone import localtime
def export_to_excel(request):
    booking_id = request.GET.get('booking_id', '')  # Agar search filter hai toh apply karein

    # Filtered data jo table me dikh raha hai, wahi export hoga
    task_list = Task.objects.filter(booking__status="Completed") \
                            .select_related('booking', 'technician', 'supported_by') \
                            .defer('description') \
                            .order_by("-id")

    if booking_id:
        task_list = task_list.filter(booking__order_id__icontains=booking_id)

    # Data ko Pandas DataFrame me convert karein
    data = []
    for task in task_list:
        product = task.booking.products.first()
        category_name = product.subcategory.Category_id.category_name if product else "N/A"
        subcategory_name = product.subcategory.name if product else "N/A"
        product_name = product.name if product else "N/A"
        customer_name = f"{task.booking.customer.admin.first_name} {task.booking.customer.admin.last_name}" if task.booking.customer.admin else "N/A"
        mobile_no = task.booking.customer.mobile  if task.booking.customer.mobile else "N/A"
        city = task.booking.customer.city  if task.booking.customer.city else "N/A"
        state = task.booking.customer.state  if task.booking.customer.state else "N/A"
        area = task.booking.customer.area  if task.booking.customer.area else "N/A"
        zipcode = task.booking.customer.zipcode  if task.booking.customer.zipcode else "N/A"
        gst_no = task.booking.customer.gst_no  if task.booking.customer.gst_no else "N/A"
        total = task.booking.final_amount  if task.booking.final_amount else "N/A"
        booking_date = localtime(task.booking.booking_date).replace(tzinfo=None) if task.booking.booking_date else "N/A"
        expert_by = task.technician.admin.username  if task.technician.admin.username else "N/A"
         
        data.append({
            "Booking ID": task.booking.order_id,
            "Customer Name": task.booking.customer.admin.first_name,
            "Category": category_name,
            "Subcategory": subcategory_name,
            "Product": product_name,
            "Customer": customer_name,
            "Mobile": mobile_no,
            "City": city,
            "State": state,
            "Area": area,
            "Zipcode": zipcode,
            "GST No": gst_no,
            "Total": total,
            "Booking Date": booking_date,
            "Expert By": expert_by,
            # "Technician": task.technician.name if task.technician else "N/A",
            # "Status": task.booking.status,
            # "Date": task.booking.date_created.strftime("%Y-%m-%d %H:%M:%S"),
        })

    df = pd.DataFrame(data)

    # Excel file ka response create karein
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Booking_Data.xlsx'
    df.to_excel(response, index=False, engine='openpyxl')
    
    return response


import json

@csrf_exempt
def toggle_auto_assign(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        is_enabled = data.get('is_enabled', False)

        # Get or create the single record
        setting, created = AutoAssignSetting.objects.get_or_create(id=1)
        setting.is_enabled = is_enabled
        setting.save()

        return JsonResponse({'status': setting.is_enabled})






# ------------------------------- Slot ------------------------------        

def slot(request):
    
    slot = Slot.objects.all().order_by('-id')
    context = {
        'slot':slot
    }
    return render(request,'homofix_app/AdminDashboard/Slot/slot_list.html',context)



def get_pincodes_by_state(request):
    
    state = request.GET.get('state')
    pincodes = Pincode.objects.filter(state=state).values('id', 'code')
    return JsonResponse({'pincodes': list(pincodes)})

    
def add_slot(request):
    # Add None option to slot choices for blocking all slots
    slot_choices = [(None, "All Slots (Block All)")] + list(SLOT_CHOICES)
    unique_states = Pincode.objects.values_list('state', flat=True).distinct()
    subcategory = SubCategory.objects.all()
    if request.method == "POST":
        date = request.POST.get('date')
        slot = request.POST.get('slot')
        state = request.POST.get('state')
        pincode = request.POST.getlist('pincode')
        subcategry = request.POST.getlist('subcategory')
        limit = request.POST.get('limit')

        # Convert slot to integer or None
        if slot == 'None' or slot == '' or slot is None:
            slot_value = None
        else:
            slot_value = int(slot)

        # Create slot with None value if "All Slots" option was selected
        slot_obj = Slot.objects.create(date=date, slot=slot_value, limit=limit)
        slot_obj.pincode.set(pincode)
        slot_obj.subcategories.set(subcategry)
        slot_obj.save()
        messages.success(request, 'Slot Added successfully')
        return redirect('slot')
   
    context = {
        'slot_choices': slot_choices,
        'unique_states': unique_states,
        'subcategory': subcategory,
    }
    return render(request, 'homofix_app/AdminDashboard/Slot/add_slot.html', context)



def edit_slot(request, id):
    slot = Slot.objects.get(id=id)
    # Add None option to slot choices for blocking all slots
    slot_choices = [(None, "All Slots (Block All)")] + list(SLOT_CHOICES)
    unique_states = Pincode.objects.values_list('state', flat=True).distinct()
    subcategory = SubCategory.objects.all()

    # ✨ Get all pincodes of this slot's state
    selected_state = slot.pincode.first().state if slot.pincode.exists() else None
    state_pincodes = Pincode.objects.filter(state=selected_state) if selected_state else []

    if request.method == "POST":
        date = request.POST.get('date')
        selected_time = request.POST.get('slot')
        pincode = request.POST.getlist('pincode')
        subcategry = request.POST.getlist('subcategory')
        limit = request.POST.get('limit')
        
        # Convert slot to integer or None
        if selected_time == 'None' or selected_time == '' or selected_time is None:
            slot_value = None
        else:
            slot_value = int(selected_time)

        slot.date = date
        slot.slot = slot_value
        
        # Only set pincodes if they are selected, otherwise clear them
        if pincode:
            slot.pincode.set(pincode)
        else:
            slot.pincode.clear()  # Allow empty/null pincode selection
            
        slot.subcategories.set(subcategry)
        slot.limit = limit
        slot.save()
        messages.success(request, "Slot updated successfully.")
        return redirect('slot')
   
    context = {
        'slot': slot,
        'slot_choices': slot_choices,
        'unique_states': unique_states,
        'subcategory': subcategory,
        'state_pincodes': state_pincodes,           # ✨ for initial rendering
        'selected_pincode_ids': slot.pincode.values_list('id', flat=True),  # ✨ to mark selected
        'selected_subcategory_ids': slot.subcategories.values_list('id', flat=True),  # 🔥
        'allow_empty_pincode': True,  # Flag to indicate empty pincode selection is allowed
    }

    return render(request, "homofix_app/AdminDashboard/Slot/edit_slot.html", context)



def delete_slot(request,id):
    
    slot = Slot.objects.get(id=id)
    slot.delete()
    messages.success(request, "Slot deleted successfully.")
    return redirect('slot')




# ------------------------- upload csv file ------------------- 

# import pandas as pd
from django.contrib import messages
from django.shortcuts import redirect
from .models import Pincode

# def upload_pincode_csv(request):
#     if request.method == "POST" and request.FILES.get("csv_file"):
#         csv_file = request.FILES["csv_file"]
#         try:
#             df = pd.read_csv(csv_file)
#             added = 0
#             skipped = 0

#             for _, row in df.iterrows():
#                 state = row.get("state")
#                 code = row.get("pincode")

#                 if state and code:
#                     # check for duplicate entry
#                     if not Pincode.objects.filter(state=state, code=code).exists():
#                         Pincode.objects.create(state=state, code=code)
#                         added += 1
#                     else:
#                         skipped += 1

#             messages.success(request, f"Pincode CSV uploaded successfully. Added: {added}, Skipped (duplicates): {skipped}")
#         except Exception as e:
#             messages.error(request, f"Error importing CSV: {e}")
#     else:
#         messages.error(request, "Please upload a valid CSV file.")

#     return redirect('pincode')  # 🔁 replace with your actual URL name



import pandas as pd
import os

def upload_pincode_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]
        file_name = csv_file.name

        try:
            # Check file extension
            if file_name.endswith(".csv"):
                df = pd.read_csv(csv_file)
            elif file_name.endswith((".xls", ".xlsx")):
                df = pd.read_excel(csv_file)
            else:
                messages.error(request, "Unsupported file format. Please upload a CSV or Excel file.")
                return redirect('pincode')

            added = 0
            skipped = 0

            for _, row in df.iterrows():
                state = row.get("state").strip().title()
                code = row.get("pincode")

                if state and code:
                    if not Pincode.objects.filter(state=state, code=code).exists():
                        Pincode.objects.create(state=state, code=code)
                        added += 1
                    else:
                        skipped += 1

            messages.success(request, f"File uploaded. Added: {added}, Skipped (duplicates): {skipped}")
        except Exception as e:
            messages.error(request, f"Error importing file: {e}")
    else:
        messages.error(request, "Please upload a valid CSV or Excel file.")

    return redirect('pincode')




# views.py

def test_notification_view(request):
    # Flutter app se mila hua FCM token
    fcm_token = 'eQUf_sgfGkJ5t56SzVLMbA:APA91bEkiP9for4msQZLSxRy5msdxJD2rvE8GD9ItSq0hEOYKNXeuqVlubt2Txf7fb3uri5s46ZGnlEd7EK8IhSJ8yI1yQ9AVUbP5YDVv5QAbWnTptKhUPY'
    
    # Notification content
    title = 'Test Notification'
    body = 'Yeh ek test message hai Firebase se.'

    # Optional data payload (key-value string map)
    extra_data = {
        'key1': 'value1',
        'key2': 'value2'
    }

    # Send notification
    result = send_push_notification(fcm_token, title, body, data=extra_data)

    return JsonResponse(result)




# views.py


def get_pincode_by_state(request):
    state = request.GET.get("state")
    pincodes = []
    if state:
        pincodes = list(Pincode.objects.filter(state=state).values("id", "code"))
    return JsonResponse(pincodes, safe=False)



# views.py

from django.http import JsonResponse
from rest_framework.decorators import api_view
from datetime import datetime, time as dt_time
from django.utils import timezone
from .models import Slot, Booking, SubCategory, Pincode, UniversalCredential
# from homofix_app.choices import SLOT_CHOICES_DICT  # Adjust import as needed
from homofix_app.models import SLOT_CHOICES_DICT



@api_view(['GET'])
def ajax_check_slot_availability(request):
    """
    AJAX view to check slot availability based on:
    - zipcode
    - date (YYYY-MM-DD)
    - subcategory_ids (comma-separated string of IDs)
    """

    zipcode = request.GET.get("zipcode")
    print("zipcodee",zipcode)
    date_str = request.GET.get("date")
    print("date:",date_str)
    subcategory_ids = request.GET.getlist("subcategory_ids[]")  # from jQuery AJAX
    print("subcategory_ids",subcategory_ids)

    if not zipcode or not date_str or not subcategory_ids:
        return JsonResponse({"error": "Missing required parameters."}, status=400)

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        aware_start_dt = timezone.make_aware(datetime.combine(date_obj, dt_time.min))
        aware_end_dt = timezone.make_aware(datetime.combine(date_obj, dt_time.max))
    except ValueError:
        return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

    subcategories = SubCategory.objects.filter(id__in=subcategory_ids)

    universal_slot_obj = UniversalCredential.objects.first()
    universal_limit = universal_slot_obj.universal_slot if universal_slot_obj and universal_slot_obj.universal_slot is not None else 0

    response_slots = []

    for slot_number in range(1, 13):
        slots = Slot.objects.filter(
            slot=slot_number,
            subcategories__in=subcategories
        ).distinct()

        matching_slot = None
        if slots.exists():
            for slot_obj in slots:
                if slot_obj.pincode.filter(code=int(zipcode)).exists():
                    matching_slot = slot_obj
                    break

        if matching_slot and matching_slot.limit is not None:
            limit = matching_slot.limit
        else:
            limit = universal_limit

        current_count = Booking.objects.filter(
            booking_date__range=(aware_start_dt, aware_end_dt),
            slot=slot_number,
            zipcode=zipcode,
        ).count()

        remaining = limit - current_count

        response_slots.append({
            "slot": slot_number,
            "time": SLOT_CHOICES_DICT.get(slot_number, f"Slot {slot_number}"),
            "available": remaining > 0
        })

    return JsonResponse({"slots": response_slots})
