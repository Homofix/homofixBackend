from django.db import models,transaction
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .utils import generate_ref_code,generate_expert_code,generate_support_code,generate_order_code
from ckeditor.fields import RichTextField
import os
from django.utils import timezone
from django.db.models.functions import Coalesce
from django.db.models import Sum
from decimal import Decimal
import datetime
from django.db.models import Prefetch
from django.core.files.base import ContentFile


# Create your models here.

class CustomUser(AbstractUser):
    user_type_data=(('1',"HOD"),('2',"Technician"),('3',"Support"),('4',"Customer"))
    user_type=models.CharField(default='1',choices=user_type_data,max_length=10)



class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return self.admin.username
    

class Category(models.Model):    
    
    icon = models.ImageField(upload_to='CatogryIcon',null=True,blank=True)
    category_name = models.CharField(max_length=50)
    created_at=models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    objects=models.Manager()

    def delete(self, *args, **kwargs):
        if self.icon:
            if os.path.isfile(self.icon.path):
                os.remove(self.icon.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.category_name
    

    
    
class SubCategory(models.Model):
    Category_id = models.ForeignKey(to=Category,on_delete=models.CASCADE)
    subcategory_image = models.ImageField(upload_to='subcategory-Image',null=True,blank=True)
    name = models.CharField(max_length=100)
    created_at=models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def delete(self, *args, **kwargs):
        if self.subcategory_image:
            if os.path.isfile(self.subcategory_image.path):
                os.remove(self.subcategory_image.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name
    
    

status = (
    ('Active','Active'),
    ('Inactive','Inactive'),
    ('New','New'),
    # ('Deactivate','Deactivate'),
    ('Hold','Hold'),
)

STATE_CHOICES = (
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal', 'Pradesh'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnatka', 'Karnatka'),
        ('Kerala', 'Kerala'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttarakhand', 'Uttarakhand'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('West Bengal', 'West Bengal'),
        ('Delhi', 'Delhi'),
        # add more choices as needed
    )


class Support(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='Support', null=True, blank=True)
    address = models.TextField()
    permanent_address = models.TextField(null=True,blank=True)
    father_name = models.CharField(max_length=100,null=True,blank=True)
    mobile = models.CharField(max_length=50)
    marital_status = models.CharField(max_length=50,null=True,blank=True)
    d_o_b = models.CharField(max_length=50,null=True,blank=True)
    status = models.CharField(choices=status, max_length=50, default='Active')
    bookings = models.ManyToManyField('Booking', blank=True, related_name='supported_by_staff')
    support_id = models.CharField(max_length=12,blank=True)
    joining_date = models.DateField(null=True,blank=True)
    application_form = models.FileField(upload_to='Support/Application Form',null=True,blank=True)
    document_form = models.FileField(upload_to='Support/Document Form',null=True,blank=True)
    can_assign_task = models.BooleanField(default=False)
    can_new_booking = models.BooleanField(default=False)
    can_cancel_booking = models.BooleanField(default=False)
    can_rebooking = models.BooleanField(default=False)
    can_expert_create = models.BooleanField(default=False)
    can_contact_us_enquiry = models.BooleanField(default=False)
    can_job_enquiry = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if not self.support_id:
            last_support = Support.objects.order_by('-id').first()
            if last_support and '-' in last_support.support_id:
                last_id = int(last_support.support_id.split('-')[1])
            else:
                last_id = 2300
            new_id = last_id + 1
            self.support_id = f'HS-{new_id:03}'
        super().save(*args, **kwargs)


    def __str__(self):
        return self.admin.username

class Pincode(models.Model):
    state = models.CharField(max_length=255)
    code = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.code)


class Technician(models.Model):
   
    id = models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    subcategories = models.ManyToManyField(SubCategory, blank=True,null=True)
    profile_pic = models.ImageField(upload_to = 'Technician', null= True, blank=True)
    mobile = models.CharField(max_length=20,blank=True,null=True)
    # expert_id = models.CharField(max_length=12,blank=True)
    expert_id = models.CharField(max_length=12, blank=True)

    # user_id = models.CharField(max_length=12,blank=True)
    Father_name = models.CharField(max_length=100,null=True,blank=True)
    present_address = models.TextField(null=True,blank=True)
    permanent_address = models.TextField(null=True,blank=True)
    Id_Proof = models.CharField(max_length=100,null=True,blank=True)
    id_type = models.CharField(max_length=100,null=True,blank=True)
    id_proof_document = models.ImageField(upload_to='ID Proof',null=True,blank=True)
    application_form = models.ImageField(upload_to='Expert/Application Form',null=True,blank=True)
    rating = models.CharField(max_length=50,null=True,blank=True)
    serving_area = models.CharField(max_length=100,null=True,blank=True)
    highest_qualification = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True,choices=STATE_CHOICES)
    city = models.CharField(max_length=100,null=True,blank=True)
    status = models.CharField(choices=status,max_length=50,default='Active')
    # status_choice = models.CharField(choices=STATUS_CHOICES,max_length=50,default='New')
    supported_by = models.ForeignKey(Support, on_delete=models.SET_NULL, null=True, blank=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    joining_date = models.DateField(null=True,blank=True)
    working_pincode_areas = models.ManyToManyField(Pincode, related_name='technicians')
    fcm_token = models.TextField(null=True, blank=True)
    objects=models.Manager()


    def save(self, *args, **kwargs):
        if not self.expert_id:
            last_technician = Technician.objects.order_by('-id').first()
            if last_technician:
                last_id = int(last_technician.expert_id.split('-')[1])
            else:
                last_id = 0
            new_id = last_id + 1
            self.expert_id = f'HE-{new_id:03}'
        super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if not self.expert_id:
    #         self.expert_id = generate_expert_code()
    #     super().save(*args, **kwargs)


    # def save(self, *args, **kwargs):
    #     if self.user_id == "":
    #         user_id = (generate_ref_code())
    #         self.user_id = user_id
    #     super().save(*args, **kwargs)
   
   
    def delete(self, *args, **kwargs):
        if self.profile_pic:
            if os.path.isfile(self.profile_pic.path):
                os.remove(self.profile_pic.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.id)
 


class Customer(models.Model):
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address = models.CharField(max_length=1000)
    mobile = models.CharField(max_length=50)
    city = models.CharField(max_length=50,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True,choices=STATE_CHOICES)
    area = models.CharField(max_length=1000,null=True,blank=True)
    zipcode = models.IntegerField(null=True,blank=True)
    date = models.DateField(auto_now_add=True,null=True,blank=True)
    gst_no = models.CharField(max_length=40,null=True,blank=True)
    
    # def save(self, *args, **kwargs):
    #     if not self.admin.username:
    #         last_customer = Customer.objects.order_by('-id').first()
    #         if last_customer:
    #             last_id = int(last_customer.admin.username.split('-')[1])
    #         else:
    #             last_id = 0
    #         new_id = last_id + 1
    #         self.admin.username = f'User-{new_id:03}'
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.admin.username
    


class Product(models.Model):
    product_pic = models.ImageField(upload_to = 'Product Image')
    product_title = models.CharField(max_length=50,null=True,blank=True)
    name = models.CharField(max_length=50)
    # category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    price = models.IntegerField()
    dis_amt = models.IntegerField(null=True,blank=True)
    selling_price = models.IntegerField(null=True,blank=True)
    warranty = models.CharField(max_length=50,null=True,blank=True)
    warranty_desc = RichTextField(null=True,blank=True)
    description = RichTextField()
    created_at=models.DateField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    
    def save(self, *args, **kwargs):
        if not self.selling_price:
            self.selling_price=self.price - self.dis_amt
           
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    


class FAQ(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = RichTextField()





class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    validity_period = models.DateTimeField()

    def __str__(self):
        return self.code



# class Booking(models.Model):
#     STATUS_CHOICES = (
#         ('New', 'New'),
#         ('Inprocess', 'Inprocess'),
#         ('Cancelled', 'Cancelled'),
#         ('Completed', 'Completed'),
#         ('Reached', 'Reached'),
#         ('Assign', 'Assign'),
#         ('Proceed', 'Proceed'),
#     )

#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     products = models.ManyToManyField(Product, related_name='bookings', through='BookingProduct')
#     booking_date = models.DateTimeField()
#     supported_by = models.ForeignKey(Support, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings_supported_by')
#     admin_by = models.ForeignKey(AdminHOD, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings_admin_by')
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
#     description = models.TextField(null=True,blank=True) 
#     order_id = models.CharField(max_length=9, unique=True, null=True, blank=True)
#     cash_on_service = models.BooleanField(default=False,null=True,blank=True)
#     online = models.BooleanField(default=True,null=True,blank=True)
#     coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings_used_coupon')



#     def save(self, *args, **kwargs):
#         if not self.order_id:
#             today = datetime.datetime.now()
#             year_month = today.strftime('%Y%m')
#             last_order = Booking.objects.filter(order_id__startswith=year_month).order_by('-id').first()
#             if last_order:
#                 last_id = int(last_order.order_id[-2:])
#             else:
#                 last_id = 0
#             new_id = last_id + 1
#             self.order_id = f'{year_month}{new_id:02}'
#         super().save(*args, **kwargs)




#     @property
#     def total_amount(self):
#         # booking_products_prefetch = Prefetch('bookingproduct_set',
#                                             #  queryset=BookingProduct.objects.select_related('product'))
#         booking_products_prefetch = Prefetch('bookingproduct_set', queryset=BookingProduct.objects.select_related('product'))


                                            
        
#         addons_prefetch = Prefetch('bookingproduct_set__addon_set',
#                            queryset=Addon.objects.select_related('spare_parts_id'))
#         booking = Booking.objects.prefetch_related(booking_products_prefetch, addons_prefetch)\
#                                  .get(id=self.id)
#         # total = sum(booking_product.quantity * booking_product.product.price for booking_product in booking.bookingproduct_set.all())
#         total = sum(booking_product.quantity * 
#             (booking_product.product.selling_price or booking_product.product.price) 
#             for booking_product in booking.bookingproduct_set.all())

#         total += sum(addon.quantity * addon.spare_parts_id.price for booking_product in booking.bookingproduct_set.all() for addon in booking_product.addon_set.all())
#         # tax_rate = 0.18  # replace with your actual tax rate
#         # total_with_tax = total + (total * tax_rate)
#         # return round(total_with_tax, 2)
#         if self.coupon:
#             total -= self.coupon.discount_amount
#         return total

#     @property
#     def tax_amount(self):
#         tax_rate = Decimal('0.18')  # replace with your actual tax rate
#         return round(self.total_amount * tax_rate, 2)

#     @property
#     def total_addons(self):
#         addons_prefetch = Prefetch('bookingproduct_set__addon_set',
#                                    queryset=Addon.objects.select_related('spare_parts_id'))
#         booking = Booking.objects.prefetch_related(addons_prefetch).get(id=self.id)
#         total = sum(addon.quantity * addon.spare_parts_id.price 
#                     for booking_product in booking.bookingproduct_set.all() 
#                     for addon in booking_product.addon_set.all())
#         return total
    
#     @property
#     def subtotal(self):
#         subtl = self.total_amount - self.total_addons

#         return subtl

    

SLOT_CHOICES = [
    (1, "08:00 AM - 09:00 AM"),
    (2, "09:00 AM - 10:00 AM"),
    (3, "10:00 AM - 11:00 AM"),
    (4, "11:00 AM - 12:00 PM"),
    (5, "12:00 PM - 01:00 PM"),
    (6, "01:00 PM - 02:00 PM"),
    (7, "02:00 PM - 03:00 PM"),
    (8, "03:00 PM - 04:00 PM"),
    (9, "04:00 PM - 05:00 PM"),
    (10, "05:00 PM - 06:00 PM"),
    (11, "06:00 PM - 07:00 PM"),
    (12, "07:00 PM - 08:00 PM"),
]

SLOT_CHOICES_DICT = dict(SLOT_CHOICES)
class Booking(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Inprocess', 'Inprocess'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
        ('Reached', 'Reached'),
        ('Assign', 'Assign'),
        ('Proceed', 'Proceed'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='booking_products', through='BookingProduct')
    booking_date = models.DateTimeField()
    supported_by = models.ForeignKey(Support, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings_supported_by')
    admin_by = models.ForeignKey(AdminHOD, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings_admin_by')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    description = models.TextField(null=True, blank=True) 
    order_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    cash_on_service = models.BooleanField(default=True, null=True, blank=True)
    online = models.BooleanField(default=False, null=True, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings_used_coupon')
    New_payment = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    booking_customer = models.CharField(max_length=100,null=True)
    booking_address = models.CharField(max_length=1000,null=True)
    mobile = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    area = models.CharField(max_length=1000, null=True)
    zipcode = models.CharField(max_length=100, null=True)
    cancel_reason = models.CharField(max_length=300,null=True,blank=True)
    final_amount_field = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    slot = models.IntegerField(choices=SLOT_CHOICES, null=True, blank=True)
    
    
    
   

    def save(self, *args, **kwargs):
        if not self.order_id:
            today = datetime.datetime.now()
            year_month = today.strftime('%Y%m')
            last_order = Booking.objects.filter(order_id__startswith=year_month).order_by('-id').first()
            if last_order:
                last_id = int(last_order.order_id[-4:])
            else:
                last_id = 0
            new_id = last_id + 1
            self.order_id = f'{year_month}{new_id:04}'
          # ✅ save calculated value
        super().save(*args, **kwargs)
    def update_totals(self):
        total = sum(bp.quantity * (bp.selling_price or bp.price)
                    for bp in self.booking_product.all())
        total += sum(addon.quantity * addon.spare_parts_id.price
                     for bp in self.booking_product.all()
                     for addon in bp.addon_set.all())
        if self.coupon:
            total -= self.coupon.discount_amount
        hod_share_percentage = HodSharePercentage.objects.latest('id')
        comp_val = float(total * (hod_share_percentage.percentage / 100))
        comp_tax = float(comp_val * (0.18))
        exp_val = float(total * ((1 - hod_share_percentage.percentage/100)))
        exp_tax = float(exp_val * (0.05))
        tax_rate = comp_tax + exp_tax 
        final_amount = Decimal(total) + Decimal(round(tax_rate, 2))
        self.final_amount_field = round(final_amount, 2)
        super(Booking, self).save(update_fields=['final_amount_field'])

    @property
    def total_amount(self):
        total = sum(bp.quantity * (bp.selling_price or bp.price)
                    for bp in self.booking_product.all())
        total += sum(addon.quantity * addon.spare_parts_id.price
                     for bp in self.booking_product.all()
                     for addon in bp.addon_set.all())
        if self.coupon:
            total -= self.coupon.discount_amount
        return total


    @property
    def tax_amount(self):
        hod_share_percentage = HodSharePercentage.objects.latest('id')
        
        
        # tax_rate = Decimal('0.18')  # replace with your actual tax rate
        # return round(self.total_amount * tax_rate, 2)
        # comp_val = float(self.total_amount * (hod_share_percentage/100))
        comp_val = float(self.total_amount * (hod_share_percentage.percentage / 100))

        comp_tax = float(comp_val * (0.18))
        # exp_val = float(self.total_amount * ((1 - hod_share_percentage)/100))
        exp_val = float(self.total_amount * ((1 - hod_share_percentage.percentage/100)))

        exp_tax = float(exp_val * (0.05))
        tax_rate = comp_tax + exp_tax 
        return(round(tax_rate, 2))

    @property
    def total_addons(self):
        addons_prefetch = Prefetch('booking_product__addon_set', queryset=Addon.objects.select_related('spare_parts_id'))
        booking = Booking.objects.prefetch_related(addons_prefetch).get(id=self.id)
        total = sum(addon.quantity * addon.spare_parts_id.price 
                    for booking_product in booking.booking_product.all() 
                    for addon in booking_product.addon_set.all())
        return total

    @property
    def subtotal(self):
        subtotal = self.total_amount - self.total_addons
        return subtotal

    @property
    def final_amount(self):
        final_amount = Decimal(self.total_amount) + Decimal(self.tax_amount)
        return round(final_amount,2)


   
    @property
    def pay_amt(self):
        payments = Payment.objects.filter(booking_id=self)
        total_payment_amount = sum(payment.amount for payment in payments)

        if total_payment_amount > 0:
            remaining_amount = Decimal(self.final_amount) - Decimal(total_payment_amount)
            rounded_amount = round(remaining_amount, 2) if remaining_amount > 0 else Decimal('0.00')
        else:
            rounded_amount = Decimal(self.final_amount)

        return rounded_amount

    @property
    def coupon_code(self):
        if self.coupon:
            return self.coupon.code
        return None

    @property
    def coupon_discount_amount(self):
        if self.coupon:
            return self.coupon.discount_amount
        return None

    @property
    def coupon_validity_period(self):
        if self.coupon:
            return self.coupon.validity_period
        return None

class BookingProduct(models.Model):
    
    # booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booking_product')

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    selling_price = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)  
    total_price = models.IntegerField()
    total_price_with_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    # def save(self, *args, **kwargs):
    #     # Calculate the total price with tax
    #     total_price_with_tax = self.total_price * Decimal('1.18')
    #     # Set the total price with tax for this booking product
    #     self.total_price_with_tax = total_price_with_tax
    #     super(BookingProduct, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Calculate the total price with tax
        total_price_with_tax = self.total_price * Decimal('1.18')
        # Set the total price with tax for this booking product
        self.total_price_with_tax = total_price_with_tax
        super().save(*args, **kwargs)
        if self.booking_id:
            self.booking.update_totals()

    # def __str__(self):
    #     return self.product.name
    
    # def total_price(self):
    #     return self.quantity * self.price
    
    # def multiply(self, *args, **kwargs):
    #     self.total_price = self.quantity * self.price
    #     return self.total_price
        
        # super().save(*args, **kwargs)



class SpareParts(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    spare_part = models.CharField(max_length=100,null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    description = models.TextField()
    created_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.spare_part
    


# class Addon(models.Model):
    
#     booking = models.ForeignKey(Booking,on_delete=models.CASCADE)
#     # addon_product = models.ManyToManyField(AddonsProduct)
#     addon_product = models.ForeignKey(AddonsProduct,on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     date = models.DateField(auto_now_add=True)
#     description = models.TextField(null=True,blank=True)



class Addon(models.Model):
    booking_prod_id = models.ForeignKey(BookingProduct,on_delete=models.CASCADE)
    spare_parts_id = models.ForeignKey(SpareParts,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(null=True,blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        bk = self.booking_prod_id.booking
        bk.update_totals()


class HodSharePercentage(models.Model):
    percentage = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    # percentage = models.IntegerField()
    date = models.DateField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return str(self.percentage)
    

   

class TechnicianLocation(models.Model):
    technician_id = models.ForeignKey(Technician, on_delete=models.CASCADE,null=True,blank=True)
    booking_id = models.ForeignKey(Booking,on_delete=models.CASCADE,null=True,blank=True)
    location = models.CharField(max_length=100,null=True,blank=True)
    date = models.DateField(auto_now_add=True,null=True,blank=True)
    # latitude = models.DecimalField(max_digits=9, decimal_places=6)
    # longitude = models.DecimalField(max_digits=9, decimal_places=6)
    # timestamp = models.DateTimeField(auto_now_add=True)


class AllTechnicianLocation(models.Model):
    technician_id = models.ForeignKey(Technician, on_delete=models.CASCADE,null=True,blank=True)
    location = models.CharField(max_length=100,null=True,blank=True)
    date = models.DateField(auto_now_add=True)
    



class Task(models.Model):

    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    description = models.TextField(null=True,blank=True)
    supported_by = models.ForeignKey(Support, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Assign')

    # def __str__(self):
    #     return f"Task for {self.booking.customer.admin.username} - {self.booking.product.name}"



# class Rebooking(models.Model):
#     STATUS_CHOICES = (
#         ('Assign', 'Assign'),
#         ('Inprocess', 'Inprocess'),
#         ('completed', 'Completed'),
       
#     )
#     booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='rebookings')
#     # new_booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='original_bookings')
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Assign')
#     technician = models.ForeignKey(Technician, on_delete=models.CASCADE,null=True,blank=True)
#     booking_date = models.DateTimeField(null=True, blank=True)
#     date = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
        
#         self.booking.status = 'Assign'
#         self.booking.save()

#         super().save(*args, **kwargs)



class Share(models.Model):
    # booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    hod_share_percentage = models.ForeignKey(HodSharePercentage, on_delete=models.CASCADE)
    technician_share = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
  
    company_share = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    date = models.DateField(auto_now_add=True,null=True,blank=True)



class Wallet(models.Model):
    technician_id = models.ForeignKey(Technician, on_delete=models.CASCADE)
    total_share = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    # total_share = models.IntegerField(default=0)
    
    def add_bonus(self, bonus_amount):
        self.total_share += bonus_amount
        self.save()

    def deduct_amount(self, amount):
        self.total_share -= amount
        self.save()
    
    # def recharge_technician_wallet(self, technician_id, amount):
    #     technician = Technician.objects.get(id=technician_id)
    #     if technician == self.technician:
    #         self.total_share += amount
    #         self.save()
    def update_total_share(self):
        # Get the recharge history for the technician
        recharge_history = RechargeHistory.objects.filter(technician_id=self.technician.id)
        
        # Sum the amounts from all entries in the recharge history and update the total_share field
        total_amount = sum([entry.amount for entry in recharge_history])
        self.total_share = total_amount
        self.save()


    # def __str__(self):
    #     return self.technician_id.admin.username
    


class WalletHistory(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    TYPE_CHOICES = (
        ('bonus', 'Bonus'),
        ('deduction', 'Deduction'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    # amount = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    description = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.wallet.technician_id.admin.username)
    

class Rebooking(models.Model):
    STATUS_CHOICES = (
        ('Assign', 'Assign'),
        ('Inprocess', 'Inprocess'),
        ('Completed', 'Completed'),
    )
    
    booking_product = models.ForeignKey(BookingProduct, on_delete=models.CASCADE, related_name='rebookings')
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE, null=True, blank=True)
    booking_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Assign')
    date = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.technician:
            # get the technician assigned to the original Task
            try:
                task = Task.objects.get(booking=self.booking_product.booking, status='Assign')
                self.technician = task.technician
            except Task.DoesNotExist:
                pass
        super(Rebooking, self).save(*args, **kwargs)


class ContactUs(models.Model):
    name = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Carrer(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField()
    status = models.BooleanField(default=True)

class ApplicantCarrer(models.Model):
    carrer_id = models.ForeignKey(Carrer,on_delete=models.CASCADE)    
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    resume = models.FileField(upload_to='Job/Job Enquiry Form',null=True,blank=True)
    date = models.DateField(auto_now_add=True)


    
class JobEnquiry(models.Model):
    resume = models.FileField(upload_to='Job/Job Enquiry Form',null=True,blank=True)
    name = models.CharField(max_length=50)    
    mobile = models.CharField(max_length=20)
    email = models.EmailField(max_length=100,null=True,blank=True)
    expert_in = models.CharField(max_length=100)
    full_address = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    PAYMENT_CHOICES = (
        ('Online', 'Online'),
        ('Cash On Services', 'Cash On Services'),
        ('Qr', 'Qr'),
    )
    booking_id = models.ForeignKey(Booking,on_delete=models.CASCADE)  
    payment_id = models.CharField(max_length=100)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_CHOICES,default="Online")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True,null=True,blank=True)

    
    def __str__(self):
        return str(self.booking_id)
    

    # def save(self, *args, **kwargs):
    #     if self.booking_id:
    #         self.amount = self.booking_id.final_amount
    #     super().save(*args, **kwargs)

   

    

    
class Kyc(models.Model):
    technician_id = models.ForeignKey(Technician,on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100,null=True,blank=True)
    Ac_no = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    bank_holder_name = models.CharField(max_length=100)
    bank_active = models.BooleanField(default=False)
    def __str__(self):
        return str(self.technician_id)
    

class showonline(models.Model):
    technician_id = models.ForeignKey(Technician,on_delete=models.CASCADE)    
    online = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.technician_id.admin.username

        
    

class RechargeHistory(models.Model):
    payment_id = models.CharField(max_length=50,null=True,blank=True)
    technician_id = models.ForeignKey(Technician,on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10,null=True,blank=True)

    def __str__(self):
        return str(self.technician_id) + ' - ' + str(self.amount)


class WithdrawRequest(models.Model):
        
    status = (
        ('Process','Process'),
        ('Cancel','Cancel'),
        ('Accept','Accept'),
    )
    technician_id = models.ForeignKey(Technician,on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    status = models.CharField(choices=status, max_length=50, default='Process')
    

class Attendance(models.Model):
    support_id = models.ForeignKey(Support, on_delete=models.CASCADE)
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(null=True, blank=True)   


class Blog(models.Model):
    title = models.CharField(max_length=100)
    feature_img = models.ImageField(upload_to='Blog/Feature Image')
    content = RichTextField()
    
    

class Offer(models.Model):
    name = models.CharField(max_length=100)
    offer_pic = models.ImageField(upload_to='Offer')
    url = models.URLField(null=True,blank=True)
    def __str__(self):
        return self.name
    

class feedback(models.Model):

    booking_id  = models.ForeignKey(Booking,on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)    
    technician_id = models.ForeignKey(Technician,on_delete=models.CASCADE)
    rating = models.IntegerField()
    description = models.TextField()



class MostViewed(models.Model):
    subccategry_id = models.ForeignKey(SubCategory,on_delete=models.SET_NULL, null=True, blank=True)
    img = models.ImageField(upload_to='MostViewed',null=True,blank=True)
    

class HomePageService(models.Model):
    category_id = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100)
    

    
class LegalPage(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField()
    subcategory = models.ForeignKey(SubCategory,on_delete=models.SET_NULL, null=True, blank=True)
    home = models.BooleanField(default=False)
    contact = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 
   





class Invoice(models.Model):
    booking_id = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    invoice = models.BinaryField(null=True, blank=True)
    invoice_no =  models.IntegerField(default=1)
    updated_at = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            # New invoice entry, increment the invoice number
            last_invoice = Invoice.objects.order_by('-invoice_no').first()
            if last_invoice:
                self.invoice_no = last_invoice.invoice_no + 1
            else:
                self.invoice_no = 1
        super().save(*args, **kwargs)


    def save_invoice(self, pdf_data):
        self.invoice.save('invoice.pdf', ContentFile(pdf_data), save=True)


class Settlement(models.Model):
    technician_id = models.ForeignKey(Technician,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    settlement = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

class UniversalCredential(models.Model):
    app_version = models.FloatField(null=True, blank=True)
    force_update = models.BooleanField(default=False)
    universal_slot = models.IntegerField(null=True,blank=True)
    
    def __str__(self):
        return f"Universal Slot is {self.universal_slot}"


class Slot(models.Model):
    date = models.DateField(null=True,blank=True)
    slot = models.IntegerField(choices=SLOT_CHOICES, null=True, blank=True)
    pincode = models.ManyToManyField(Pincode, related_name='slot',null=True,blank=True)
    subcategories = models.ManyToManyField(SubCategory, related_name='slots',null=True, blank=True)
    # original_limit = models.IntegerField(null=True, blank=True)
    limit = models.IntegerField(null=True,blank=True)
   
    # def __str__(self):
    #     slot_display = dict(SLOT_CHOICES).get(self.slot, self.slot)
    #     return f"Slot {slot_display} on {self.date} (Used: {self.used_count} of {self.original_limit})"
    def __str__(self):
        slot_display = dict(SLOT_CHOICES).get(self.slot, self.slot)
        return f"Slot {slot_display} on {self.date} with limit {self.limit}"


class AutoAssignSetting(models.Model):
    is_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"Auto Assign is {'ON' if self.is_enabled else 'OFF'}"


class TechnicianAssignmentTracker(models.Model):
    last_assigned_technician = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)

class UniversalSlotTracker(models.Model):
    date = models.DateField()
    slot = models.IntegerField()
    used_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date} - Slot {self.slot} : {self.used_count}"

class BookingTracker(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='tracker')
    date = models.DateField()
    slot = models.IntegerField()
    slot_remaining_limit = models.IntegerField(null=True, blank=True)
    universal_slot_remaining_limit = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"BookingTracker for {self.booking.order_id} (Slot: {self.slot}, Date: {self.date})"


@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type=='1':
            AdminHOD.objects.create(admin=instance)
        if instance.user_type=='2':
            technician = Technician.objects.create(admin=instance, present_address="")
            showonlin = showonline.objects.create(technician_id=technician)
            showonlin.save()
            wallet = Wallet.objects.create(technician_id=technician)
            wallet.save()
            
            technician.subcategories.set([SubCategory.objects.first()])
        if instance.user_type=='3':
            
            Support.objects.create(admin=instance, address="")
            # support.can_assign_task = instance.has_perm('homofix_app.assign_task')
            # support.can_cancel_booking = instance.has_perm('homofix_app.cancel_order')
            # support.save()
        if instance.user_type=='4':
            
            Customer.objects.create(admin=instance,address="")



@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type=='1':
        instance.adminhod.save()
    if instance.user_type=='2':
        instance.technician.save() 
    if instance.user_type=='3':
        instance.support.save()
    if instance.user_type=='4':
        instance.customer.save()






# @receiver(post_save, sender=Addon)
# def update_booking_on_addon_save(sender, instance, **kwargs):
#     booking = instance.booking
#     for addons_product in instance.addon_products.all():
#         booking = Booking.objects.get(id=4)
#         product = Product.objects.get(id=1)
#         booking_product = BookingProduct.objects.create(booking=booking, product=product, quantity=2, total_price=200)
#         booking_product.save()
        # booking.products.add(booking_product)


# @receiver(post_save, sender=Addon)
# def update_booking_on_addon_save(sender, instance, **kwargs):
#     booking = instance.booking
#     booking.products.add(*instance.addon_products.all())
# @receiver(m2m_changed, sender=Addon.addon_products.through)
# def update_booking(sender, instance, **kwargs):
#     """
#     Update the products of the associated booking when an add-on product is added
#     or removed from an Addon instance.
#     """
#     if kwargs['action'] in ('post_add', 'post_remove', 'post_clear'):
#         booking = instance.booking
#         addon_products = instance.addon_products.all()
#         booking.products.set(list(booking.products.all()) + list(addon_products))    

# @receiver(post_save, sender=Booking)
# def update_technician_location(sender, instance, created, **kwargs):
#     if not created and instance.status == 'completed':
#         technicians = instance.task_set.values_list('technician', flat=True).distinct()
#         for technician_id in technicians:
#             latitude, longitude = get_technician_location_from_some_service(technician_id)
#             if latitude and longitude:
#                 location, created = TechnicianLocation.objects.update_or_create(
#                     technician_id=technician_id,
#                     defaults={
#                         'latitude': latitude,
#                         'longitude': longitude,
#                     }
#                 )



