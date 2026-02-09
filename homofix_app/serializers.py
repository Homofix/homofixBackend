from rest_framework import serializers
from .models import Technician,CustomUser,Task,Booking,Product,Customer,Rebooking,BookingProduct,JobEnquiry,Kyc,SpareParts,Addon,TechnicianLocation,showonline,RechargeHistory,Wallet,WalletHistory,WithdrawRequest,AllTechnicianLocation,Blog,MostViewed,Category,SubCategory,feedback,Offer,HomePageService,ApplicantCarrer,Carrer,Coupon,LegalPage,FAQ,HodSharePercentage,Payment,Settlement,WorkingStateCity

from django.utils.safestring import mark_safe
from django.utils.html import strip_tags
import requests
class LoginSerliazer(serializers.Serializer):
    username = serializers.CharField
    password = serializers.CharField
    class Meta:
       
        fields = ('id','username','password')  
        # fields = ['username', 'email', 'first_name', 'last_name']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','email','first_name']

 
class ExpertSerliazer(serializers.ModelSerializer):
    admin = CustomUserSerializer()
    class Meta:
        model = Technician
        exclude = ['supported_by']
        #fields = "__all__"
        # fields = ['reference_id','created_at','updated_at','admin_id']   
        # depth = 1    



# ------------------ Task ------------------------ 

class ASerializer(serializers.ModelSerializer):
    class Meta:
        model = Addon
        fields = ('id', 'spare_parts_id', 'quantity', 'date', 'description')


class BookingprdSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id')
    addon_set = ASerializer(many=True, read_only=True)
    
    class Meta:
        model = BookingProduct
        fields = ('id', 'product_id','addon_set')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username',"first_name"]

class CustomerSerializer(serializers.ModelSerializer):
    admin = UserSerializer()
    class Meta:
        model = Customer
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
   
    warranty_desc = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = "__all__"

    def get_warranty_desc(self, obj):

        return obj.warranty_desc.replace('\r\n', '').strip().replace('<p>', '').replace('</p>', '')

class techSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technician
        fields = "__all__"



class BookingProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BookingProduct
        fields = ['id','product','quantity']



class BookingSerializer(serializers.ModelSerializer):
    booking_product = BookingProductSerializer(many=True)
    customer = CustomerSerializer()
    products = ProductSerializer(many=True)
    tax_amount = serializers.ReadOnlyField()
    total_amount = serializers.ReadOnlyField()
    final_amount = serializers.ReadOnlyField()
    pay_amt = serializers.ReadOnlyField()
    

    class Meta:
        model = Booking
        fields = "__all__"



class TaskSerializer(serializers.ModelSerializer):
    booking = BookingSerializer()
    # technician = techSerializer()
   

    class Meta:
        model = Task
        fields = "__all__"



# class BokingSerializer(serializers.ModelSerializer):
#     # booking = BookingSerializer()
 

#     class Meta:
#         model = Booking
#         fields = "__all__"


class KycSerializer(serializers.ModelSerializer):

    class Meta:
        model = Kyc
        fields = "__all__"


# ------------------------------- PRODUCT ------------------

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        # depth = 1
    
# ----------------------- Rebooking ------------------------

# class customerSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='admin.username', read_only=True)

#     class Meta:
#         model = Customer
#         fields = ['id', 'username', 'address', 'mobile', 'state']

# class BokingSerializer(serializers.ModelSerializer):
#     customer = customerSerializer()

#     class Meta:
#         model = Booking
#         fields = ['id', 'customer',  'status']        
        
# class BookingProductSerializer(serializers.ModelSerializer):
#     booking = BokingSerializer()
#     product = serializers.StringRelatedField()
    

#     class Meta:
#         model = BookingProduct
#         fields = ['id', 'product', 'quantity', 'total_price']


# class RebookingSerializer(serializers.ModelSerializer):
#     booking_product = BookingProductSerializer()



# class customerSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='admin.username', read_only=True)

#     class Meta:
#         model = Customer
#         fields = ['id', 'username', 'address', 'mobile', 'state']

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'description', 'price']


# class BookingProductSerializer(serializers.ModelSerializer):
#     product = ProductSerializer()

#     class Meta:
#         model = BookingProduct
#         fields = ['id', 'product', 'total_price']


# class BokingSerializer(serializers.ModelSerializer):
#     customer = customerSerializer()
#     products = BookingProductSerializer(source='bookingproduct_set', many=True)

#     class Meta:
#         model = Booking
#         fields = ['id', 'customer', 'booking_date', 'is_verified', 'supported_by', 'status', 'products']


# class RebookingSerializer(serializers.ModelSerializer):
#     booking_product = BookingProductSerializer()
#     # technician = serializers.StringRelatedField()
#     booking_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
#     # booking = BokingSerializer()

#     class Meta:
#         model = Rebooking
#         fields = "__all__"

   
     

#     class Meta:
#         model = Rebooking
#         fields = "__all__"


class customerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='admin.username', read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'username', 'address', 'mobile', 'state']


class ProductSerializerr(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'product_pic']

class BookingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingProduct
        fields = '__all__'

class testingBooking(serializers.ModelSerializer):
    # booking_product = BookingProductSerializer(many=True)
    
    class Meta:
        model = Booking
        fields = ('customer', 'products')


    

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        booking = Booking.objects.create(**validated_data)
        for product_data in products_data:
            BookingProduct.objects.create(booking=booking, **product_data)
        return booking

        

class BokingSerializer(serializers.ModelSerializer):
    # customer = customerSerializer()
    # products = BookingProductSerializer(source='bookingproduct_set', many=True)

    class Meta:
        model = Booking
        fields = "__all__"
        # fields = ['id', 'customer', 'booking_date', 'is_verified', 'supported_by', 'status', 'products']


class BookingProductSerializer(serializers.ModelSerializer):
    product = ProductSerializerr()
    booking = BookingSerializer()
    
    # booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all())

    class Meta:
        model = BookingProduct
        fields = ['id', 'booking', 'product', 'quantity', 'total_price']

class TechnicianSerializer(serializers.ModelSerializer):
    admin_id = serializers.ReadOnlyField(source='admin.id')

    class Meta:
        model = Technician
        # fields = ['admin_id']
        fields = "__all__"



class RebookingSerializer(serializers.ModelSerializer):
    booking_product = BookingProductSerializer()
    
   
    class Meta:
        model = Rebooking
        fields = "__all__"






# --------------------------- JOb ENQUIRY ------------------------------- 

class JobEnquirySerliazer(serializers.ModelSerializer):
    class Meta:
        model = JobEnquiry
        fields = "__all__"



# --------------------------------------- SparePARTS ----------------------         


class SparePartsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SpareParts
        fields = ['id','product','spare_part','price','description']




class PrductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["subcategory"]


class SparePartssubcategorySerializer(serializers.ModelSerializer):
    product = PrductSerializer()

    class Meta:
        model = SpareParts
        fields = ["id", "product", "spare_part", "price", "description"]

# --------------------------------------- SparePARTS ----------------------         

# class AddonsSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Addon
#         fields = "__all__"


class BookingProdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingProduct
        fields = ['id','booking', 'product', 'quantity', 'total_price', 'total_price_with_tax']


# class AddonsSerializer(serializers.ModelSerializer):
#     # booking_prod_id = BookingProdSerializer()
    
#     class Meta:
#         model = Addon
#         # fields = ['id', 'booking_product', 'addon_products', 'quantity', 'date', 'description']
#         fields = "__all__"




class SparPartsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SpareParts
        fields = ['id','product','spare_part','price','description']


class BookingProductAddonSerializer(serializers.ModelSerializer):
    # booking = serializers.IntegerField(source='booking.id')
    booking= BookingSerializer()
    # technician_id = serializers.IntegerField(source='booking.technician.id')
    
    class Meta:
        model = BookingProduct
        fields = ['id','booking', 'product', 'quantity', 'total_price', 'total_price_with_tax']



class AddonsSerializer(serializers.ModelSerializer):
    # booking_prod_id = BookingProductAddonSerializer()
    # addon_products = SparPartsSerializer()

    class Meta:
        model = Addon
        fields = ['id', 'booking_prod_id', 'spare_parts_id', 'quantity', 'date', 'description']




class BookingAddonSerializer(serializers.ModelSerializer):
    # booking_product = BookingProductSerializer(many=True)
    # customer = CustomerSerializer()
    # products = ProductSerializer(many=True)
    tax_amount = serializers.ReadOnlyField()
    total_amount = serializers.ReadOnlyField()
    final_amount = serializers.ReadOnlyField()
    pay_amt = serializers.ReadOnlyField()
    

    class Meta:
        model = Booking
        fields = ['tax_amount','total_amount','final_amount','pay_amt']

class AddongGetBookingProductSerializer(serializers.ModelSerializer):
    # booking = serializers.IntegerField(source='booking.id')
    booking= BookingAddonSerializer()
    # technician_id = serializers.IntegerField(source='booking.technician.id')
    
    class Meta:
        model = BookingProduct
        fields = ['id','booking']


class AddonsGetSerializer(serializers.ModelSerializer):
    booking_prod_id = AddongGetBookingProductSerializer()
    spare_parts_id = SparePartsSerializer()
    booking_id = serializers.ReadOnlyField(source='booking_prod_id.booking.id')
    # total_amount = serializers.SerializerMethodField()

   
   

    class Meta:
        model = Addon
        fields = ['id','booking_id', 'booking_prod_id', 'spare_parts_id', 'quantity', 'date', 'description']
        # depth = 1


# ---------------------------------------- Technician Location ------------- 

class TechnicianLocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=TechnicianLocation
        fields = ['technician_id','booking_id','location']

# ------------------------------ All Technician Location ---------------------- 

class AllTechnicianLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model=AllTechnicianLocation
        fields = "__all__"


# --------------------------- Online Offline -------------------------- 
class TechnicianOnlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = showonline
        # fields = '__all__'
        exclude = ['date']




# ----------------------------------- RechargeHistory ------------------
class TechnicianRechargeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RechargeHistory
        fields = '__all__'
        # exclude = ['date']


# ------------------------- wallet -------------------- 

class TechnicianWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'
        # exclude = ['date']

# --------------------- Wallet History --------------------- 
class TechnicianWalletHistorySerializer(serializers.ModelSerializer):
    # technician_id = serializers.IntegerField(source='wallet.technician_id')
    technician_id = serializers.PrimaryKeyRelatedField(source='wallet.technician_id', read_only=True)
    class Meta:
        model = WalletHistory
        # fields = '__all__'
        fields = ('id', 'technician_id', 'type', 'amount', 'description', 'date')



# ------------------------- WithdrawRequest ------------------------- 

class TechnicianWithdrawRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawRequest
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Blog
        
        fields = '__all__'
    
    

class OfferSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Offer
        
        fields = '__all__'
    
    

   


class MostViewedSerializer(serializers.ModelSerializer):
    subcategory_name = serializers.CharField(source='subccategry_id.name', read_only=True)
    class Meta:
        model = MostViewed
        fields = ['subccategry_id', 'subcategory_name', 'img']


# ----------------------------- Category ------------------- 
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_image', 'name']    

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(source='subcategory_set', many=True)
   
    
    class Meta:
        model = Category
        fields = ['id','icon','category_name','subcategories']



class LegalPageSerializer(serializers.ModelSerializer):
   
    
    class Meta:
        model = LegalPage
        fields = "__all__"

# ----------------------------- Sub-Category ------------------- 

class ProductfilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
    
        fields = ['id', 'product_pic', 'product_title','name','description','warranty','warranty_desc','price','dis_amt','selling_price']    


class SubcategorySerializer(serializers.ModelSerializer):
    Category_name = serializers.CharField(source='Category_id.category_name', read_only=True)    
    products = ProductfilterSerializer(source='product_set', many=True)
    legal_pages = LegalPageSerializer(source='legalpage_set', many=True, read_only=True)  # 👈 LegalPage data add kiya

    class Meta:
        model = SubCategory
        fields = ['id','subcategory_image','name','Category_id','Category_name','products','legal_pages']
        


# ------------------------- Reebooking -------------------------         

# class TechnicianRebookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Rebooking
#         fields = '__all__'




# ---------------------------- Customer Login ------------------------------


class CustomerLoginSerliazer(serializers.Serializer):
    
    phone_number = serializers.CharField
   
    class Meta:
       
        fields = ('phone_number')  
        

class VerifyOtpSerializer(serializers.Serializer):
    OTPP = serializers.CharField
    class Meta:
        fields = ('OTPP')  




class CustSerailizer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='admin.username')
    first_name = serializers.ReadOnlyField(source='admin.first_name')
    class Meta:
        model=Customer
        fields = '__all__'
        ['id', 'admin', 'username','first_name', 'address', 'mobile', 'city', 'state', 'area', 'zipcode']
        
# -------------------- feedback ------------------------- 


class FeedbackSerailizer(serializers.ModelSerializer):
    # username = serializers.ReadOnlyField(source='admin.username')
    class Meta:
        model=feedback
        fields = '__all__'
        # ['id', 'admin', 'username', 'address', 'mobile', 'city', 'state', 'area', 'zipcode']
        


class LoginCustomrSerializers(serializers.Serializer):
    phone_number = serializers.CharField()



# --------------------------------- Home Page Service API ------------ 

class SubcategrySerializer(serializers.ModelSerializer):
    # Category_name = serializers.CharField(source='Category_id.category_name', read_only=True)    

    class Meta:
        model = SubCategory
        fields = ['id','subcategory_image','name']




class HomePageSerailizer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = SubcategrySerializer(many=True, read_only=True, source='category_id.subcategory_set')
    
    
    class Meta:
        model=HomePageService
        
        fields = ['id', 'title', 'category_id', 'subcategory']
        




# ---------------------- Testing ----------------- 


class CustomerLoginn(serializers.Serializer):
    
    phone_number = serializers.CharField()
   
    class Meta:
       
        fields = ('phone_number',)
      

class AddonsDeleteSerailizers(serializers.Serializer):
    
    id = serializers.CharField()
   
    class Meta:
       
        fields = ('id',)


class ApplicantCarrerSerliazer(serializers.ModelSerializer):
    
    class Meta:
        model = ApplicantCarrer
        fields = "__all__"


class CarrerSerliazer(serializers.ModelSerializer):
    
    class Meta:
        model = Carrer
        fields = "__all__"




class BkingProductSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = BookingProduct
        fields = ['product', 'quantity']


# class BkingSerializer(serializers.ModelSerializer):
   

#     class Meta:
#         model = Booking
#         fields = '__all__'        


class ProSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

# class BkingSerializer(serializers.ModelSerializer):
#     booking_products = BkingProductSerializer(many=True)

#     class Meta:
#         model = Booking
#         fields = '__all__'

#         # read_only_fields = ['supported_by']


#     def create(self, validated_data):
        
#         booking_products_data = validated_data.pop('booking_products', [])
#         booking = Booking.objects.create(**validated_data)
#         print("nanooooooo",booking)

#         for product_data in booking_products_data:
#             print("hhhhh")
#             product = product_data.get('product')
            
#             quantity = product_data.get('quantity')
#             total_price = int(100)
#             # if product and product.price is not None:
#             #     total_price = quantity * product.price
#             # total_price = quantity * product.price
#             BookingProduct.objects.create(
#                 booking=booking,
#                 product=product,
#                 quantity=quantity,
#                 total_price=100
#             )

#         return booking    

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_amount', 'validity_period']


class BkingSerializer(serializers.ModelSerializer):
    booking_product = BkingProductSerializer(many=True)
    # coupon = CouponSerializer()

    
    class Meta:
        model = Booking
        fields = "__all__"
        # exclude = ('products',)

    def create(self, validated_data):
        
        product_ids_data = validated_data.pop('booking_product', [])
        
        booking = Booking.objects.create(**validated_data)

        for product_id_data in product_ids_data:
            product_id = product_id_data.get('product')
            quantity = product_id_data.get('quantity')
            
            product = Product.objects.get(name=product_id)
            total_price = quantity * product.price  # Calculate total price based on quantity and product price
            slling_price = product.selling_price
            prce = product.price
            BookingProduct.objects.create(
                booking=booking,
                product=product,
                quantity=quantity,
                total_price=total_price,
                selling_price=slling_price,
                price=prce,
            
            )
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

        return booking

   
# ------------------------ Legal Page --------------- 



class faqSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"




class HodSharPercentageSerliazer(serializers.ModelSerializer):
    
    class Meta:
        model = HodSharePercentage
        fields = ['percentage']



class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ('id', 'code', 'discount_amount')





# ----------------------- testing -------------------         


class AdnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addon
        fields = '__all__'


class kingProductSerializer(serializers.ModelSerializer):
    addons = AdnSerializer(many=True, read_only=True)

    class Meta:
        model = BookingProduct
        fields = '__all__'

class BingSerializer(serializers.ModelSerializer):
    booking_product = kingProductSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

class TskSerializer(serializers.ModelSerializer):
    booking = BingSerializer()

    class Meta:
        model = Task
        fields = '__all__'



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment   
        fields = '__all__'     




# --------------------------- Demo ------------------------- 


class cuSeralizerDemo(serializers.ModelSerializer):
    first_name = serializers.CharField(source='admin.first_name', read_only=True)
    
    class Meta:
        model = Customer
        fields = ['address','mobile','city','state','area','zipcode','first_name','gst_no']


# ------------- Settlement -----------------         


class SettlementSeralizer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Settlement
        fields = "__all__"

# ---------------------- Customer payment --------------------- 


class CustomerPaymentsSerliazer(serializers.ModelSerializer):
   
    class Meta:
        model = Payment
        fields = "__all__"








# ---------------------- Customer Booking ------------------------


# class CustomerBookingProductDetailsSerializer(serializers.ModelSerializer):
   
#     # warranty_desc = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Product
#         fields = "__all__"


# class customerBookingDetailsProduct(serializers.ModelSerializer):
   
#     class Meta:
#         model : BookingProduct
#         fields = '__all__'



class AcusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addon
        fields = ('id', 'spare_parts_id', 'quantity', 'date', 'description')
        # depth = 1
    
class CustomerBookingProductDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price','dis_amt','selling_price','product_pic']  # Add the desired fields from the Product model
    
   

class customerBookingDetailsProduct(serializers.ModelSerializer):
    # addons = AdnSerializer(many=True, read_only=True)
    product = CustomerBookingProductDetailsSerializer()
    # addon_set = ASerializer(many=True, read_only=True)
    addon_set = serializers.SerializerMethodField()

    class Meta:
        model = BookingProduct
        fields = ["id", "product", "quantity", "addon_set", "selling_price", "price"]
    
    def get_addon_set(self, obj):
        addons = obj.addon_set.all()
        addon_data = AcusSerializer(addons, many=True).data

        for addon in addon_data:
            spare_parts_id = addon['spare_parts_id']
            spare_parts = SpareParts.objects.get(pk=spare_parts_id)
            
            addon['spare_part_name'] = spare_parts.spare_part
            addon['spare_part_price'] = spare_parts.price
        
        return addon_data
       



class TechnicianStatusUpdateSerializer(serializers.Serializer):
    status = (
    ('Active','Active'),
    ('Inactive','Inactive'),
    ('New','New'),
    # ('Deactivate','Deactivate'),
    ('Hold','Hold'),
)
    new_status = serializers.ChoiceField(choices=status)
 

class CustomerBookingDetailSerializer(serializers.ModelSerializer):
    tax_amount = serializers.ReadOnlyField()
    total_amount = serializers.ReadOnlyField()
    final_amount = serializers.ReadOnlyField()
    pay_amt = serializers.ReadOnlyField()
    # booking_product = kingProductSerializer(many=True, read_only=True)
    booking_product = customerBookingDetailsProduct(many=True, read_only=True)
    
    
    # products = ProductSerializer(many=True)
    class Meta:
        model = Booking
        fields = "__all__"
        # depth = 1



class WorkingStateCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingStateCity
        fields = ['id', 'state', 'city', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
