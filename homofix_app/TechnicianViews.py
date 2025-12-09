from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Technician,Task,Booking,Rebooking,Share, HodSharePercentage,BookingProduct,Wallet,SpareParts,Addon
from django.contrib import messages
from django.http import JsonResponse



@login_required(login_url='/')
def dashboard(request):
    return render(request,'Technician_templates/Dashboard/dashboard.html')




def expert_task_assign(request):

    user = request.user
    

    technician=Technician.objects.get(admin=user)
    task = Task.objects.filter(technician=technician)
    
    context = {
        'task':task

    }
    
    return render(request,'Technician_templates/Task/task.html',context)



def update_booking_status(request,booking_id):
    booking = Booking.objects.get(id=booking_id)
    task = Task.objects.get(booking=booking)
    # booking_product = BookingProduct.objects.filter(booking=booking)
   
    if request.method == 'POST':
        status = request.POST['status']
        
        # print("testingggggggggggg",xyzz.technician.status_choice)
        booking.status = status
        booking.save()
        return redirect('expert_task_assign')
        # if status == 'completed':
        #     booking_amount = booking.total_amount
        #     hod_share_percentage = HodSharePercentage.objects.latest('id')
        #     hod_share_percentage_value = hod_share_percentage.percentage
        #     hod_share = booking_amount * (hod_share_percentage_value / 100)
        #     tax_rate = 0.18  # replace with your actual tax rate
        #     hod_share = hod_share+(hod_share*tax_rate)
        
        #     technician_share = booking_amount - hod_share
            
            
            # share = Share.objects.create(
            #     task=task,
               
            #     hod_share_percentage=hod_share_percentage,
            #     technician_share=technician_share,
            #     hod_share=hod_share
            # )
            # share.save()
            # # Update the technician's wallet with their share
            # technician = task.technician
            # wallet, created = Wallet.objects.get_or_create(technician=technician)
            # wallet.total_share += technician_share
            # wallet.save()
        #     messages.success(request, f"Booking status updated to {status}. Share data created.")
        #     return redirect('expert_task_assign')
        # else:
        #     messages.success(request, f"Booking status updated to {status}")
        # # messages.success(request, f"Booking status updated to {status}")
        #     return redirect('expert_task_assign')
   

def expert_task_proceed(request,booking_id):
   
   
    addon = SpareParts.objects.all()
    # testing = BookingProduct.objects.get(id=booking_id)
    adon = Addon.objects.all()
    # print("hellooo",adon)
    # print("testinnggg",testing)

    # booking = Booking.objects.get(id=booking_id)
    bookingProd=BookingProduct.objects.filter(booking=booking_id)
    # adon = Addon.objects.filter(booking_prod_id=bookingProd)
    # print("addoon",adon)

    # print(bookingProd)
    # task = Task.objects.get(booking=booking)

    
    context = {
        # 'task':task,
        'addons':addon,
        'bookingProd':bookingProd,
        'adon':adon
        
        
    }
    return render(request,'Technician_templates/Task/Proceed/proceed.html',context)
def expert_rebooking_Task(request):
    user = request.user
    

    technician=Technician.objects.get(admin=user)
    rebooking = Rebooking.objects.filter(technician=technician)
    
    context = {
        'rebooking':rebooking

    }
    return render(request,'Technician_templates/Rebooking/rebooking_Details.html',context)   



def expert_task_addon(request, booking_id):
   
    # get booking object or return 404 if not found
    booking = get_object_or_404(BookingProduct, id=booking_id)
    # addons_product = AddonsProduct.objects.get(id=)

    if request.method == 'POST':
        
        # get addon data from request POST data
        addon_name = request.POST.get('addon')
        spare_part_id = SpareParts.objects.get(id=addon_name)
        
        addon_description = request.POST.get('notes')
        
        quantity = int(request.POST.get('quantity'))

        # create addon object
        addon = Addon.objects.create(
            booking_prod_id=booking,
            spare_parts_id=spare_part_id,
            description=addon_description,           
            quantity=quantity
        )
        
        # addon.addon_products.set([addon_name])
        addon.save()
        return redirect('expert_task_proceed',booking.booking.id)
    

        # # calculate and update invoice totals
        # # booking.calculate_totals()
        # booking.save()

        # # return JSON response with addon and totals data
        # return JsonResponse({
            
        #     'description': addon.description,
        #     # 'addon_product':addon.addon_product.set([addon_name]),
        #     'addon_product': addon.addon_product.first().spare_part, # assuming addon_product is a ManyToManyField to Product model
        #     'quantity': addon.quantity,
        #     # 'addon_total': addon.get_total(),
        #     # 'subtotal': booking.subtotal,
        #     # 'tax': booking.tax,
        #     # 'grand_total': booking.grand_total,
        # })

    # if not a POST request, render addon form template
    # return render(request, 'expert_task_addon.html', {'booking': booking})


def update_rebooking_status(request,booking_id):
    print("heloooooo")
    task = Rebooking.objects.get(id=booking_id)
    
    # user = request.user.id
    # tech = Technician.objects.get(admin=user)
    # print("demoooooooooooooooooo",tech)

    # tec = Technician.objects.get(id=request.user.id)
    # print("technician id",tec)
    
    if request.method == 'POST':
        status = request.POST['status']
        
        # print("testingggggggggggg",xyzz.technician.status_choice)
        task.status = status
        task.save()
        messages.success(request, f"Booking status updated to {status}")
        return redirect('expert_task_assign')
 