from django.contrib import admin
from django.http import HttpResponse
import os
from django.urls import reverse
from django.conf import settings
from django.http import FileResponse
from django.utils.html import format_html
from . models import CustomUser,AdminHOD,Technician,Product,Category,SpareParts,Customer,Support,FAQ,Booking,Task,Rebooking,BookingProduct,SubCategory,ContactUs,JobEnquiry,HodSharePercentage,Payment,Addon,Wallet,TechnicianLocation,Kyc,showonline,RechargeHistory,Share,AllTechnicianLocation,WithdrawRequest,Attendance,Blog,Offer,MostViewed,HomePageService,Carrer,ApplicantCarrer,LegalPage,Invoice,Settlement,Coupon,feedback,AutoAssignSetting,Pincode,UniversalCredential,Slot,UniversalSlotTracker,BookingTracker,WalletHistory,WorkingStateCity


# Register your models here.



class ProductAdmin(admin.ModelAdmin):
    list_display=['id','product_pic','product_title','name','subcategory']


# admin.site.register(CustomUser)
admin.site.register(AdminHOD)
admin.site.register(BookingTracker)
# admin.site.register(Technician)
admin.site.register(Product,ProductAdmin)
# admin.site.register(SpareParts)
# admin.site.register(Customer)
# admin.site.register(Support)
admin.site.register(FAQ)
# admin.site.register(Booking)
admin.site.register(Task)
admin.site.register(Rebooking)
# admin.site.register(BookingProduct)
admin.site.register(SubCategory)
admin.site.register(ContactUs)
admin.site.register(HodSharePercentage)
# admin.site.register(Payment)
# admin.site.register(Addon)
# admin.site.register(Wallet)
admin.site.register(TechnicianLocation)
admin.site.register(Kyc)
admin.site.register(showonline)
admin.site.register(RechargeHistory)
admin.site.register(Share)
admin.site.register(AllTechnicianLocation)
admin.site.register(WithdrawRequest)
admin.site.register(Attendance)
admin.site.register(Blog)
admin.site.register(Offer)
admin.site.register(MostViewed)
admin.site.register(HomePageService)
admin.site.register(Carrer)
admin.site.register(ApplicantCarrer)
admin.site.register(LegalPage)
admin.site.register(AutoAssignSetting)
admin.site.register(Pincode)
admin.site.register(UniversalCredential)
admin.site.register(Slot)
# admin.site.register(Invoice)
admin.site.register(UniversalSlotTracker)
admin.site.register(WalletHistory)
admin.site.register(WorkingStateCity)



@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ['id', 'admin', 'display_subcategories']

    def display_subcategories(self, obj):
        return ", ".join([subcategory.name for subcategory in obj.subcategories.all()])
    
    display_subcategories.short_description = 'Subcategories'
    

@admin.register(CustomUser)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['id','username']
    search_fields = ["username"]

@admin.register(BookingProduct)
class BookingProductAdmin(admin.ModelAdmin):
    list_display=['id','booking','product','total_price']

@admin.register(Invoice)
class CustomerInvoice(admin.ModelAdmin):
    
    list_display = ['id', 'booking_id', 'invoice', 'invoice_no']

    # def display_invoice(self, obj):
    #     if obj.invoice:
    #         return format_html('<a href="{}" target="_blank">View Invoice</a>', reverse('new_invoice', args=[obj.pk]))
    #     return "No invoice"

    # display_invoice.short_description = "Invoice"

    # def get_urls(self):
    #     from django.urls import path

    #     urls = super().get_urls()
    #     custom_urls = [
    #         path('<int:invoice_id>/view-invoice/', self.admin_site.admin_view(self.view_invoice),
    #              name='view-invoice'),
    #     ]
    #     return custom_urls + urls

    # def view_invoice(self, request, invoice_id):
    #     invoice = Invoice.objects.get(pk=invoice_id)
    #     if invoice.invoice:
    #         response = HttpResponse(content_type='application/pdf')
    #         response.write(invoice.invoice)
    #         return response
    #     return HttpResponse("Invoice not found")

   
       

       
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=['id','booking_id','payment_mode','amount','date']

@admin.register(Wallet)
class TechnicianAdmin(admin.ModelAdmin):
    list_display=['id','total_share']

@admin.register(SpareParts)
class TechnicianAdmin(admin.ModelAdmin):
    list_display=['id','product','spare_part','price','description']


@admin.register(Booking)
class TechnicianAdmin(admin.ModelAdmin):
    list_display=['id','status','booking_customer','subtotal','total_amount','tax_amount','total_addons','final_amount','pay_amt','coupon_code','coupon_discount_amount','coupon_validity_period','order_id','booking_date']


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display=['id','admin','can_new_booking','can_cancel_booking','can_rebooking','can_assign_task','can_expert_create','can_contact_us_enquiry']

    

@admin.register(Addon)
class SupportAdmin(admin.ModelAdmin):
    list_display=['id','booking_prod_id','spare_parts_id','quantity','description','date']

    


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['id','address','mobile','city']
    search_fields = ["mobile"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','category_name']
    

@admin.register(JobEnquiry)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name','mobile','email','resume','date']
    
    

@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display=['id','amount','settlement','date']
    

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display=['id','code','discount_amount','validity_period']
    
    

@admin.register(feedback)
class feddbackAdmin(admin.ModelAdmin):
    list_display=['id','booking_id','customer_id','technician_id','rating','description']
    
    

