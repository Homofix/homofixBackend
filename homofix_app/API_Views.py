from rest_framework.generics import GenericAPIView,CreateAPIView
from rest_framework.authentication import BasicAuthentication
from homofix_app.serializers import LoginSerliazer,CustomerLoginSerliazer,ExpertSerliazer,CustomUserSerializer,TaskSerializer,RebookingSerializer,JobEnquirySerliazer,ProductSerializer,BokingSerializer,KycSerializer,SparePartsSerializer,AddonsSerializer,TechnicianLocationSerializer,AddonsGetSerializer,TechnicianOnlineSerializer,TechnicianRechargeHistorySerializer,TechnicianWalletSerializer,TechnicianWalletHistorySerializer,TechnicianWithdrawRequestSerializer,AllTechnicianLocationSerializer,BlogSerializer,MostViewed,MostViewedSerializer,VerifyOtpSerializer,CategorySerializer,SubcategorySerializer,CustSerailizer,LoginCustomrSerializers,FeedbackSerailizer,OfferSerializer,testingBooking,HomePageSerailizer,BookingProductSerializer,CustomerLoginn,AddonsDeleteSerailizers,ApplicantCarrerSerliazer,CarrerSerliazer,BkingProductSerializer,BkingSerializer,LegalPageSerializer,faqSerializer,HodSharPercentageSerliazer,CouponSerializer,TskSerializer,PaymentSerializer,cuSeralizerDemo,SettlementSeralizer,CustomerBookingDetailSerializer,TechnicianStatusUpdateSerializer,SparePartssubcategorySerializer,WorkingStateCitySerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
# from homofix_app.EmailBackEnd import EmailBackEnd
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet,ModelViewSet,ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from .models import CustomUser,Technician,Task,Rebooking,JobEnquiry,Product,Booking,Kyc,SpareParts,Addon,TechnicianLocation,showonline,RechargeHistory,Wallet,WalletHistory,WithdrawRequest,HodSharePercentage,Share,AllTechnicianLocation,Blog,MostViewed,Customer,Category,SubCategory,feedback,Offer,BookingProduct,HomePageService,ApplicantCarrer,Carrer,LegalPage,FAQ,Invoice,Coupon,Payment,Settlement,Pincode,Slot,UniversalCredential,UniversalSlotTracker,WorkingStateCity
from decimal import Decimal
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
import random
import requests
from urllib.parse import urlencode
import urllib
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers
from django.utils import timezone
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import pdfkit
from .helpers import save_pdf
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.urls import reverse
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework_simplejwt.tokens import Token
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import generics
from homofix_app.services.auto_assign import assign_employee_to_booking

from utils.firebase import send_push_notification


class LoginViewSet(CreateAPIView):
    authentication_classes = [BasicAuthentication]
    serializer_class = LoginSerliazer
    def post(self,request,*args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
       
        user=authenticate(request, username=username, password = password)
        
        

        if user!=None:
            login(request,user)
            user_type = user.user_type
            if user_type == '2':
                user_data = {
                    'id': user.technician.id,
                    'username': user.username,
                    
                    # Add any other user fields you want to return
                }
                return Response({'message': 'Logged in successfully.', 'user': user_data}, status=status.HTTP_200_OK)
                # return Response({'message': 'Logged in successfully.'}, status=status.HTTP_200_OK)
           
        else:
            return Response({'message': 'Invalid login credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

      

class ExpertViewSet(ModelViewSet):
    
    authentication_classes = [BasicAuthentication]
    serializer_class = ExpertSerliazer
    queryset = Technician.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data) 
    

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

   
# Helper method to create invoice (this method should already be in your class)
def create_invoice(self, booking):
    try:
        subtotal = booking.subtotal
        tax = Decimal(subtotal) * Decimal(0.18)
        total = tax + subtotal
        total_amt = Decimal(booking.total_amount) + Decimal(booking.tax_amount)
        cgst_sgst = Decimal(total_amt) * Decimal(0.09)
        grandtotal = total_amt + (cgst_sgst * 2)

        invoice = Invoice.objects.filter(booking_id=booking).first()
        if not invoice:
            invoice = Invoice.objects.create(booking_id=booking)
            bookingprod = BookingProduct.objects.filter(booking=booking).first()
            addon = Addon.objects.filter(booking_prod_id=bookingprod)
            
            input_file = render_to_string(
                "Invoice/invoice.html",
                {
                    "booking": invoice,
                    "addon": addon,
                    "total": total,
                    "cgst_sgst": cgst_sgst,
                    "grandtotal": grandtotal,
                },
            )
            options = {"enable-local-file-access": ""}

            pdf_data = pdfkit.from_string(input_file, False, options=options)

            if pdf_data:
                invoice.invoice = pdf_data
                invoice.save()
                print("PDF data saved in invoice successfully.")
    except Exception as e:
        print("Error in creating invoice:", e)


from django.db import transaction


# class TaskViewSet(ModelViewSet):
#     authentication_classes = [BasicAuthentication]
#     serializer_class = TaskSerializer
#     queryset = Task.objects.all()

#     def list(self, request, *args, **kwargs):
#         technician_id = request.query_params.get("technician_id")
#         if technician_id:
#             tasks = self.queryset.filter(technician=technician_id)
#             serializer = self.get_serializer(tasks, many=True)
#             return Response(serializer.data)
#         else:
#             return super().list(request, *args, **kwargs)
    
#     # @action(detail=False, methods=['PATCH'])
#     def put(self, request):
#         booking_id = request.data.get("booking_id")
#         print("bookinggggg idddd",booking_id)
#         status = request.data.get("status")
#         if booking_id and status:
#             print(booking_id)
#             try:
#                 with transaction.atomic():
#                     if booking.status == "Completed":
#                         return Response({"success": False, "message": "Booking already processed."})
#                     booking = Booking.objects.get(id=booking_id)
#                     task = Task.objects.get(booking=booking)
#                     booking.status = status
#                     booking.save()
                
                
#                     # return Response({'success': True})
#                     if booking.status == "Completed" and booking.online == True:
#                         print("okkkkkkkkkkkkkk")
                    
#                         # tax_rate = 0.18
#                         booking_amount = booking.total_amount

#                         tax_amt = booking.tax_amount

#                         hod_share_percentage = HodSharePercentage.objects.latest("id")
#                         hod_share_percentage_value = hod_share_percentage.percentage

#                         hod_share = booking_amount * (hod_share_percentage_value / 100)

#                         print("new hod share0", hod_share)
#                         technician_share = booking_amount - hod_share
#                         print("technicia sare", technician_share)

#                         # hod_share_with_tax = hod_share + tax_amt
#                         hod_share_with_tax = float(str(hod_share)) + tax_amt
#                         print("hod_share_with_tax", hod_share_with_tax)

#                         wallet_tecnician = technician_share
#                         # wallet_tecnician = Decimal(technician_share) - Decimal(tax_amt)
#                         print("wallet technician", wallet_tecnician)

#                         # technician_share = booking_amount - hod_share

#                         share = Share.objects.create(
#                             task=task,
#                             hod_share_percentage=hod_share_percentage,
#                             technician_share=wallet_tecnician,
#                             company_share=hod_share_with_tax,
#                         )
#                         share.save()
#                         technician = task.technician
#                         wallet, created = Wallet.objects.get_or_create(
#                             technician_id=technician
#                         )
#                         wallet.total_share += Decimal(str(wallet_tecnician))

#                         wallet.save()

#                         # --------------------- Settlement --------------------------------

#                         settlement = Settlement.objects.create(
#                             technician_id=technician,
#                             amount=wallet_tecnician,
#                             settlement="Settlement Add",
#                         )
#                         settlement.save()

#                         # ----------------------------------- Invoice Part -----------------------

#                         try:
#                             booking = Booking.objects.get(id=booking_id)
#                             booking.status = status
#                             booking.save()
#                             print("helooooo status", booking.status,"booking id",booking.id)
                
#                             # tax = booking.tax_amount
#                             subtotal = booking.subtotal
#                             tax = Decimal(subtotal) * Decimal(0.18)
#                             total = tax + subtotal
#                             total_amt = Decimal(booking.total_amount) + Decimal(
#                                 booking.tax_amount
#                             )
#                             cgst_sgst = Decimal(total_amt) * Decimal(0.09)
#                             grandtotal = total_amt + (cgst_sgst * 2)

#                             bkng_id = Booking.objects.filter(id=booking_id)
#                             if booking:
#                                 invoice = Invoice.objects.filter(booking_id=booking).first()
#                                 if not invoice:
#                                     invoice = Invoice.objects.create(booking_id=booking)
#                                     bookingprod = BookingProduct.objects.filter(
#                                         booking=booking
#                                     ).first()

#                                     # addon = Addon.objects.filter(booking_prod_id=bookingprod)

#                                     addon = Addon.objects.filter(
#                                         booking_prod_id=bookingprod
#                                     )

#                                     input_file = render_to_string(
#                                         "Invoice/invoice.html",
#                                         {
#                                             "booking": invoice,
#                                             "addon": addon,
#                                             "total": total,
#                                             "cgst_sgst": cgst_sgst,
#                                             "grandtotal": grandtotal,
#                                         },
#                                     )
#                                     options = {"enable-local-file-access": ""}

#                                     pdf_data = pdfkit.from_string(
#                                         input_file, False, options=options
#                                     )

#                                     if pdf_data:
#                                         invoice.invoice = pdf_data
#                                         invoice.save()
#                                         # invoice.save()
#                                         print("PDF data saved in invoice successfully.")

#                                     # return Response({'success': True})
#                                 else:
#                                     pass
#                                     # Booking does not exist
#                                     # return Response({'Error': False, 'error': 'Invoice already created'})
#                         except Exception as e:
#                             print(e)

#                     if booking.status == "Completed" and booking.cash_on_service == True:
                        
#                         booking.satatus = "Completed"
#                         booking.save()
#                         tax_rate = 0.18
#                         booking_amount = booking.total_amount
#                         print("final amount", booking_amount)

#                         tax_amt = booking.tax_amount

#                         hod_share_percentage = HodSharePercentage.objects.latest("id")
#                         hod_share_percentage_value = hod_share_percentage.percentage
#                         hod_share = booking_amount * (hod_share_percentage_value / 100)

#                         acbb = Decimal(hod_share) * Decimal(0.18)
#                         print(round(acbb, 2))
#                         print("eeeeee", hod_share)
#                         wallet_tecnician = Decimal(hod_share) + Decimal(tax_amt)
#                         print("helloooo", wallet_tecnician)

#                         technician_share = booking_amount - hod_share

#                         print("technicia sare", technician_share)

#                         print("eeeeeeeeeeeee", wallet_tecnician)
#                         final_amt = booking.final_amount - wallet_tecnician

#                         hod_share_with_tax = final_amt

#                         share = Share.objects.create(
#                             task=task,
#                             hod_share_percentage=hod_share_percentage,
#                             technician_share=hod_share_with_tax,
#                             company_share=wallet_tecnician,
#                         )
#                         share.save()
#                         technician = task.technician
#                         wallet, created = Wallet.objects.get_or_create(
#                             technician_id=technician
#                         )
#                         wallet.total_share -= Decimal(str(wallet_tecnician))

#                         wallet.save()

#                         settlement = Settlement.objects.create(
#                             technician_id=technician,
#                             amount=wallet_tecnician,
#                             settlement="Settlement Deduction",
#                         )
#                         settlement.save()

#                         try:
#                             booking = Booking.objects.get(id=booking_id)
#                             # tax = booking.tax_amount
#                             subtotal = booking.subtotal
#                             tax = Decimal(subtotal) * Decimal(0.18)
#                             total = tax + subtotal
#                             total_amt = Decimal(booking.total_amount) + Decimal(
#                                 booking.tax_amount
#                             )
#                             cgst_sgst = Decimal(total_amt) * Decimal(0.09)
#                             grandtotal = total_amt + (cgst_sgst * 2)

#                             bkng_id = Booking.objects.filter(id=booking_id)
                            
#                             if booking:
#                                 invoice = Invoice.objects.filter(booking_id=booking).first()
#                                 if not invoice:
#                                     invoice = Invoice.objects.create(booking_id=booking)
#                                     bookingprod = BookingProduct.objects.filter(
#                                         booking=booking
#                                     ).first()

#                                     # addon = Addon.objects.filter(booking_prod_id=bookingprod)

#                                     addon = Addon.objects.filter(
#                                         booking_prod_id=bookingprod
#                                     )

#                                     input_file = render_to_string(
#                                         "Invoice/invoice.html",
#                                         {
#                                             "booking": invoice,
#                                             "addon": addon,
#                                             "total": total,
#                                             "cgst_sgst": cgst_sgst,
#                                             "grandtotal": grandtotal,
#                                         },
#                                     )
#                                     options = {"enable-local-file-access": ""}

#                                     pdf_data = pdfkit.from_string(
#                                         input_file, False, options=options
#                                     )

#                                     if pdf_data:
#                                         invoice.invoice = pdf_data
#                                         invoice.save()
#                                         # invoice.save()
#                                         print("PDF data saved in invoice successfully.")

#                                     # return Response({'success': True})
#                                 else:
#                                     pass
#                                     # Booking does not exist
#                                     # return Response({'Error': False, 'error': 'Invoice already created'})
#                         except Exception as e:
#                             print(e)

#                     return Response({"success": True})
#             except Booking.DoesNotExist:
#                 return Response({"success": False, "message": "Booking not found."})
#         else:
#             return Response(
#                 {"success": False, "message": "Booking id and status are required."}
#             )


class TaskViewSet(ModelViewSet):
    authentication_classes = [BasicAuthentication]
   
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def list(self, request, *args, **kwargs):
        technician_id = request.query_params.get("technician_id")
        if technician_id:
            tasks = self.queryset.filter(technician=technician_id)
            serializer = self.get_serializer(tasks, many=True)
            return Response(serializer.data)
        else:
            return super().list(request, *args, **kwargs)

    # @action(detail=False, methods=['PATCH'])
    def put(self, request):
        booking_id = request.data.get("booking_id")
        print("bookinggggg idddd",booking_id)
        
        status = request.data.get("status")
        if booking_id and status:
            print(booking_id)
            try:
                booking = Booking.objects.get(id=booking_id)
                if booking.status == "Completed":
                    return Response({"success": False, "message": "Booking already processed."})
                task = Task.objects.get(booking=booking)
                booking.status = status
                booking.save()
               
               
                # return Response({'success': True})
                if booking.status == "Completed" and booking.online == True:
                   
                    # tax_rate = 0.18
                    booking_amount = booking.total_amount

                    tax_amt = booking.tax_amount

                    hod_share_percentage = HodSharePercentage.objects.latest("id")
                    hod_share_percentage_value = hod_share_percentage.percentage

                    hod_share = booking_amount * (hod_share_percentage_value / 100)

                    print("new hod share0", hod_share)
                    technician_share = booking_amount - hod_share
                    print("technicia sare", technician_share)

                    # hod_share_with_tax = hod_share + tax_amt
                    hod_share_with_tax = float(str(hod_share)) + tax_amt
                    print("hod_share_with_tax", hod_share_with_tax)

                    wallet_tecnician = technician_share
                    # wallet_tecnician = Decimal(technician_share) - Decimal(tax_amt)
                    print("wallet technician", wallet_tecnician)

                    # technician_share = booking_amount - hod_share

                    share = Share.objects.create(
                        task=task,
                        hod_share_percentage=hod_share_percentage,
                        technician_share=wallet_tecnician,
                        company_share=hod_share_with_tax,
                    )
                    share.save()
                    technician = task.technician
                    wallet, created = Wallet.objects.get_or_create(
                        technician_id=technician
                    )
                    wallet.total_share += Decimal(str(wallet_tecnician))

                    wallet.save()

                    # --------------------- Settlement --------------------------------

                    settlement = Settlement.objects.create(
                        technician_id=technician,
                        amount=wallet_tecnician,
                        settlement="Settlement Add",
                    )
                    settlement.save()

                    

                    # ----------------------------------- Invoice Part -----------------------

                    try:
                        booking = Booking.objects.get(id=booking_id)
                        booking.status = status
                        booking.save()
                        print("helooooo status", booking.status,"booking id",booking.id)
               
                        # tax = booking.tax_amount
                        subtotal = booking.subtotal
                        tax = Decimal(subtotal) * Decimal(0.18)
                        total = tax + subtotal
                        total_amt = Decimal(booking.total_amount) + Decimal(
                            booking.tax_amount
                        )
                        cgst_sgst = Decimal(total_amt) * Decimal(0.09)
                        grandtotal = total_amt + (cgst_sgst * 2)

                        bkng_id = Booking.objects.filter(id=booking_id)
                        if booking:
                            invoice = Invoice.objects.filter(booking_id=booking).first()
                            if not invoice:
                                try:
                                    invoice = Invoice.objects.create(booking_id=booking)
                                    bookingprod = BookingProduct.objects.filter(
                                        booking=booking
                                    ).first()

                                    if not bookingprod:
                                        print("BookingProduct not found for booking ID:", booking.id)
                                        raise Exception("BookingProduct not found")

                                    # addon = Addon.objects.filter(booking_prod_id=bookingprod)

                                    addon = Addon.objects.filter(
                                        booking_prod_id=bookingprod
                                    )

                                    input_file = render_to_string(
                                        "Invoice/invoice.html",
                                        {
                                            "booking": invoice,
                                            "addon": addon,
                                            "total": total,
                                            "cgst_sgst": cgst_sgst,
                                            "grandtotal": grandtotal,
                                        },
                                    )
                                    options = {"enable-local-file-access": ""}

                                    pdf_data = pdfkit.from_string(
                                        input_file, False, options=options
                                    )

                                    if pdf_data:
                                        invoice.invoice = pdf_data
                                        invoice.save()
                                        print("PDF data saved in invoice successfully.")
                                    else:
                                        print("Failed to generate PDF data for invoice")
                                except Exception as inner_e:
                                    print("Error creating invoice:", inner_e)
                            else:
                                print("Invoice already exists for booking ID:", booking.id)
                    except Exception as e:
                        print("Error in invoice creation process:", e)

                if booking.status == "Completed" and booking.cash_on_service == True:
                    
                    booking.status = "Completed"
                    booking.save()
                    tax_rate = 0.18
                    booking_amount = booking.total_amount
                    print("final amount", booking_amount)

                    tax_amt = booking.tax_amount

                    hod_share_percentage = HodSharePercentage.objects.latest("id")
                    hod_share_percentage_value = hod_share_percentage.percentage
                    hod_share = booking_amount * (hod_share_percentage_value / 100)

                    acbb = Decimal(hod_share) * Decimal(0.18)
                    print(round(acbb, 2))
                    print("eeeeee", hod_share)
                    wallet_tecnician = Decimal(hod_share) + Decimal(tax_amt)
                    print("helloooo", wallet_tecnician)

                    technician_share = booking_amount - hod_share

                    print("technicia sare", technician_share)

                    print("eeeeeeeeeeeee", wallet_tecnician)
                    final_amt = booking.final_amount - wallet_tecnician

                    hod_share_with_tax = final_amt

                    share = Share.objects.create(
                        task=task,
                        hod_share_percentage=hod_share_percentage,
                        technician_share=hod_share_with_tax,
                        company_share=wallet_tecnician,
                    )
                    share.save()
                    technician = task.technician
                    wallet, created = Wallet.objects.get_or_create(
                        technician_id=technician
                    )
                    wallet.total_share -= Decimal(str(wallet_tecnician))

                    wallet.save()

                    settlement = Settlement.objects.create(
                        technician_id=technician,
                        amount=wallet_tecnician,
                        settlement="Settlement Deduction",
                    )
                    settlement.save()


                    try:
                        booking = Booking.objects.get(id=booking_id)
                        # tax = booking.tax_amount
                        subtotal = booking.subtotal
                        tax = Decimal(subtotal) * Decimal(0.18)
                        total = tax + subtotal
                        total_amt = Decimal(booking.total_amount) + Decimal(
                            booking.tax_amount
                        )
                        cgst_sgst = Decimal(total_amt) * Decimal(0.09)
                        grandtotal = total_amt + (cgst_sgst * 2)

                        bkng_id = Booking.objects.filter(id=booking_id)
                        
                        if booking:
                            invoice = Invoice.objects.filter(booking_id=booking).first()
                            if not invoice:
                                try:
                                    invoice = Invoice.objects.create(booking_id=booking)
                                    bookingprod = BookingProduct.objects.filter(
                                        booking=booking
                                    ).first()

                                    if not bookingprod:
                                        print("BookingProduct not found for booking ID:", booking.id)
                                        raise Exception("BookingProduct not found")

                                    # addon = Addon.objects.filter(booking_prod_id=bookingprod)

                                    addon = Addon.objects.filter(
                                        booking_prod_id=bookingprod
                                    )

                                    input_file = render_to_string(
                                        "Invoice/invoice.html",
                                        {
                                            "booking": invoice,
                                            "addon": addon,
                                            "total": total,
                                            "cgst_sgst": cgst_sgst,
                                            "grandtotal": grandtotal,
                                        },
                                    )
                                    options = {"enable-local-file-access": ""}

                                    pdf_data = pdfkit.from_string(
                                        input_file, False, options=options
                                    )

                                    if pdf_data:
                                        invoice.invoice = pdf_data
                                        invoice.save()
                                        print("PDF data saved in invoice successfully.")
                                    else:
                                        print("Failed to generate PDF data for invoice")
                                except Exception as inner_e:
                                    print("Error creating invoice:", inner_e)
                            else:
                                print("Invoice already exists for booking ID:", booking.id)
                    except Exception as e:
                        print("Error in invoice creation process:", e)


                
                # ------------------- Notificationssssssssssss 

                 # ---------------- Notification Block ----------------
                try:
                    # Technician ko notification
                    technician = task.technician
                   
                    if technician and hasattr(technician, "fcm_token") and technician.fcm_token:
                        send_push_notification(
                            token=technician.fcm_token,
                            title="Booking Update",
                            body=f"Booking #{booking.id} status updated to {booking.status}",
                            data={"booking_id": str(booking.id), "status": booking.status}
                        )
                        print("sendginnnnnnnnnnn success")

                    # User ko notification
                    booking_user = getattr(booking, "user", None)
                    if booking_user and hasattr(booking_user, "fcm_token") and booking_user.fcm_token:
                        send_push_notification(
                            token=booking_user.fcm_token,
                            title="Booking Update",
                            body=f"Your booking #{booking.id} is now {booking.status}",
                            data={"booking_id": str(booking.id), "status": booking.status}
                        )
                except Exception as e:
                    print("Notification error:", e)

                # --------------------------------

                return Response({"success": True})
            
            except Booking.DoesNotExist:
                return Response({"success": False, "message": "Booking not found."})
        else:
            return Response(
                {"success": False, "message": "Booking id and status are required."}
            )

############### NEW API HERE #####################
class TechniciantaskViewSet(ModelViewSet):
    authentication_classes = [BasicAuthentication]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


    def list(self, request, *args, **kwargs):
        technician_id = request.query_params.get("technician_id")
        status = request.query_params.get("status")

        if not technician_id or not status:
            return Response({"detail": "Both 'technician_id' and 'status' are required."}, status=400)

        status = status.lower()

        # Mapping frontend status values to Booking.status choices
        status_map = {
            "assign": ["Assign", "Reached", "Proceed"],
            "reached": ["Reached","Assign", "Proceed"],
            "proceed": ["Proceed","Reached","Assign"],
            "completed": ["Completed"],
            "cancelled": ["Cancelled"],
        }

        # Check if status is valid
        if status not in status_map:
            return Response({"detail": f"Invalid status '{status}'. Valid options are: assign, completed, cancelled."}, status=400)

        tasks = self.queryset.filter(technician=technician_id, booking__status__in=status_map[status])
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    # def list(self, request, *args, **kwargs):
    #     technician_id = request.query_params.get("technician_id")
    #     status_param = request.query_params.get("status")

    #     if technician_id and status_param:
    #         tasks = self.queryset.filter(technician=technician_id, booking__status=status_param)
    #         serializer = self.get_serializer(tasks, many=True)
    #         return Response(serializer.data)
    #     else:
    #         return Response(
    #             {"detail": "Both 'technician_id' and 'status' are required query parameters."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    # @action(detail=False, methods=['PATCH'])
    def put(self, request):
        booking_id = request.data.get("booking_id")
        print("bookinggggg idddd",booking_id)
        
        status = request.data.get("status")
        if booking_id and status:
            print(booking_id)
            try:
                booking = Booking.objects.get(id=booking_id)
                if booking.status == "Completed":
                    return Response({"success": False, "message": "Booking already processed."})
                task = Task.objects.get(booking=booking)
                booking.status = status
                booking.save()
               
               
                # return Response({'success': True})
                if booking.status == "Completed" and booking.online == True:
                   
                    # tax_rate = 0.18
                    booking_amount = booking.total_amount

                    tax_amt = booking.tax_amount

                    hod_share_percentage = HodSharePercentage.objects.latest("id")
                    hod_share_percentage_value = hod_share_percentage.percentage

                    hod_share = booking_amount * (hod_share_percentage_value / 100)

                    print("new hod share0", hod_share)
                    technician_share = booking_amount - hod_share
                    print("technicia sare", technician_share)

                    # hod_share_with_tax = hod_share + tax_amt
                    hod_share_with_tax = float(str(hod_share)) + tax_amt
                    print("hod_share_with_tax", hod_share_with_tax)

                    wallet_tecnician = technician_share
                    # wallet_tecnician = Decimal(technician_share) - Decimal(tax_amt)
                    print("wallet technician", wallet_tecnician)

                    # technician_share = booking_amount - hod_share

                    share = Share.objects.create(
                        task=task,
                        hod_share_percentage=hod_share_percentage,
                        technician_share=wallet_tecnician,
                        company_share=hod_share_with_tax,
                    )
                    share.save()
                    technician = task.technician
                    wallet, created = Wallet.objects.get_or_create(
                        technician_id=technician
                    )
                    wallet.total_share += Decimal(str(wallet_tecnician))

                    wallet.save()

                    # --------------------- Settlement --------------------------------

                    settlement = Settlement.objects.create(
                        technician_id=technician,
                        amount=wallet_tecnician,
                        settlement="Settlement Add",
                    )
                    settlement.save()

                    # ----------------------------------- Invoice Part -----------------------

                    try:
                        # booking = Booking.objects.get(id=booking_id)
                        # booking.status = status
                        # booking.save()
                        # print("helooooo status", booking.status,"booking id",booking.id)
               
                        # tax = booking.tax_amount
                        subtotal = booking.subtotal
                        tax = Decimal(subtotal) * Decimal(0.18)
                        total = tax + subtotal
                        total_amt = Decimal(booking.total_amount) + Decimal(
                            booking.tax_amount
                        )
                        cgst_sgst = Decimal(total_amt) * Decimal(0.09)
                        grandtotal = total_amt + (cgst_sgst * 2)

                        bkng_id = Booking.objects.filter(id=booking_id)
                        if booking:
                            invoice = Invoice.objects.filter(booking_id=booking).first()
                            if not invoice:
                                invoice = Invoice.objects.create(booking_id=booking)
                                bookingprod = BookingProduct.objects.filter(
                                    booking=booking
                                ).first()

                                # addon = Addon.objects.filter(booking_prod_id=bookingprod)

                                addon = Addon.objects.filter(
                                    booking_prod_id=bookingprod
                                )

                                input_file = render_to_string(
                                    "Invoice/invoice.html",
                                    {
                                        "booking": invoice,
                                        "addon": addon,
                                        "total": total,
                                        "cgst_sgst": cgst_sgst,
                                        "grandtotal": grandtotal,
                                    },
                                )
                                options = {"enable-local-file-access": ""}

                                pdf_data = pdfkit.from_string(
                                    input_file, False, options=options
                                )

                                if pdf_data:
                                    invoice.invoice = pdf_data
                                    invoice.save()
                                    # invoice.save()
                                    print("PDF data saved in invoice successfully.")

                                # return Response({'success': True})
                            else:
                                pass
                                # Booking does not exist
                                # return Response({'Error': False, 'error': 'Invoice already created'})
                    except Exception as e:
                        print(e)

                if booking.status == "Completed" and booking.cash_on_service == True:
                    
                    booking.satatus = "Completed"
                    booking.save()
                    tax_rate = 0.18
                    booking_amount = booking.total_amount
                    print("final amount", booking_amount)

                    tax_amt = booking.tax_amount

                    hod_share_percentage = HodSharePercentage.objects.latest("id")
                    hod_share_percentage_value = hod_share_percentage.percentage
                    hod_share = booking_amount * (hod_share_percentage_value / 100)

                    acbb = Decimal(hod_share) * Decimal(0.18)
                    print(round(acbb, 2))
                    print("eeeeee", hod_share)
                    wallet_tecnician = Decimal(hod_share) + Decimal(tax_amt)
                    print("helloooo", wallet_tecnician)

                    technician_share = booking_amount - hod_share

                    print("technicia sare", technician_share)

                    print("eeeeeeeeeeeee", wallet_tecnician)
                    final_amt = booking.final_amount - wallet_tecnician

                    hod_share_with_tax = final_amt

                    share = Share.objects.create(
                        task=task,
                        hod_share_percentage=hod_share_percentage,
                        technician_share=hod_share_with_tax,
                        company_share=wallet_tecnician,
                    )
                    share.save()
                    technician = task.technician
                    wallet, created = Wallet.objects.get_or_create(
                        technician_id=technician
                    )
                    wallet.total_share -= Decimal(str(wallet_tecnician))

                    wallet.save()

                    settlement = Settlement.objects.create(
                        technician_id=technician,
                        amount=wallet_tecnician,
                        settlement="Settlement Deduction",
                    )
                    settlement.save()

                    try:
                        booking = Booking.objects.get(id=booking_id)
                        # tax = booking.tax_amount
                        subtotal = booking.subtotal
                        tax = Decimal(subtotal) * Decimal(0.18)
                        total = tax + subtotal
                        total_amt = Decimal(booking.total_amount) + Decimal(
                            booking.tax_amount
                        )
                        cgst_sgst = Decimal(total_amt) * Decimal(0.09)
                        grandtotal = total_amt + (cgst_sgst * 2)

                        bkng_id = Booking.objects.filter(id=booking_id)
                        
                        if booking:
                            invoice = Invoice.objects.filter(booking_id=booking).first()
                            if not invoice:
                                invoice = Invoice.objects.create(booking_id=booking)
                                bookingprod = BookingProduct.objects.filter(
                                    booking=booking
                                ).first()

                                # addon = Addon.objects.filter(booking_prod_id=bookingprod)

                                addon = Addon.objects.filter(
                                    booking_prod_id=bookingprod
                                )

                                input_file = render_to_string(
                                    "Invoice/invoice.html",
                                    {
                                        "booking": invoice,
                                        "addon": addon,
                                        "total": total,
                                        "cgst_sgst": cgst_sgst,
                                        "grandtotal": grandtotal,
                                    },
                                )
                                options = {"enable-local-file-access": ""}

                                pdf_data = pdfkit.from_string(
                                    input_file, False, options=options
                                )

                                if pdf_data:
                                    invoice.invoice = pdf_data
                                    invoice.save()
                                    # invoice.save()
                                    print("PDF data saved in invoice successfully.")

                                # return Response({'success': True})
                            else:
                                pass
                                # Booking does not exist
                                # return Response({'Error': False, 'error': 'Invoice already created'})
                    except Exception as e:
                        print(e)

                return Response({"success": True})
            except Booking.DoesNotExist:
                return Response({"success": False, "message": "Booking not found."})
        else:
            return Response(
                {"success": False, "message": "Booking id and status are required."}
            )



    
class TechnicianAddonsGetViewSet(ModelViewSet):
    serializer_class = AddonsGetSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        booking_id = self.request.query_params.get('booking_id')
        if booking_id:
            return Addon.objects.filter(booking_prod_id__booking__id=booking_id)
        return Addon.objects.none()  # 👈 empty if booking_id is not provided

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)



class TechnicianRebookingViewSet(ModelViewSet):
    queryset = Rebooking.objects.all()
    serializer_class = RebookingSerializer

    def list(self, request, *args, **kwargs):
        technician_id = request.query_params.get("technician_id")
        status = request.query_params.get("status")

        if not technician_id or not status:
            return Response({"detail": "Both 'technician_id' and 'status' are required."}, status=400)

        status = status.lower()

        status_map = {
            "assign": ["Assign", "Inprocess"],   
            "inprocess": ["Inprocess","Assign"],
            "completed": ["Completed"],
        }

        if status not in status_map:
            return Response({"detail": f"Invalid status '{status}'. Valid options are: assign, inprocess, completed."}, status=400)

        filtered_qs = self.queryset.filter(technician_id=technician_id, status__in=status_map[status])
        serializer = self.get_serializer(filtered_qs, many=True)
        return Response(serializer.data)





@api_view(['PATCH'])
def technicianRebookingStatusUpdated(request):
    try:
        data = request.data
        rebooking_id = data.get("rebooking_id")
        technician_id = data.get("technician_id")
        status = data.get("status")

        # Validate all required fields
        if not rebooking_id or not technician_id or not status:
            return Response({
                'status': False,
                'message': "rebooking_id, technician_id, and status are required.",
                'data': {}
            })

        # Fetch specific Rebooking by ID and technician
        try:
            obj = Rebooking.objects.get(id=rebooking_id, technician_id=technician_id)
        except Rebooking.DoesNotExist:
            return Response({
                'status': False,
                'message': 'Rebooking not found for given rebooking_id and technician_id',
                'data': {}
            })

        # Update status only
        serializer = RebookingSerializer(obj, data={'status': status}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'message': 'Status updated successfully',
                'data': serializer.data
            })
        else:
            return Response({
                'status': False,
                'message': 'Invalid data',
                'data': serializer.errors
            })

    except Exception as e:
        print("Error:", e)
        return Response({
            'status': False,
            'message': 'An error occurred',
            'data': {}
        })

######### end new api #######################################################

class RebookingViewSet(ModelViewSet):
    
    

    queryset = Rebooking.objects.all()     
    serializer_class  = RebookingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        technician_id = self.request.query_params.get('technician_id')
       
        if technician_id:
            queryset = queryset.filter(technician_id=technician_id)
        return queryset
    
    # def update(self, request, pk=None):
    #     try:
    #         rebooking = self.get_object()
    #         serializer = self.get_serializer(rebooking, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except Rebooking.DoesNotExist:
    #         return Response({"error": "Rebooking not found."}, status=status.HTTP_404_NOT_FOUND)
    # ---------------- Booking --------------------- 


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()     
    serializer_class  = BokingSerializer
     

# class CustomerBookingSet(ModelViewSet):
#     queryset = Booking.objects.all()
#     serializer_class = testingBooking
    
#     def perform_create(self, serializer):
#         booking = serializer.save()
#         product_data = self.request.data.get('products', [])
        
#         for product_item in product_data:
#             product_id = product_item.get('product_id')
#             quantity = product_item.get('quantity')
            
#             product = Product.objects.get(id=product_id)
            
#             BookingProduct.objects.create(
#                 booking=booking,
#                 product=product,
#                 quantity=quantity
#             )
class BkingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BkingSerializer

class BkingProductViewSet(viewsets.ModelViewSet):
    queryset = BookingProduct.objects.all()
    serializer_class = BkingProductSerializer     

@api_view(['POST'])
def create_booking_manually(request):
    data = request.data
    # serializer = BookingCreateManuallySerailizer(data=data)
    print("ggggggggggggggg",data)
    return Response({
        'status':"ok",
        'message':data
    })


# @api_view(['PATCH'])
# def RebookingStatusUpdated(request):
    
#     try:
#         data = request.data
#         print("data",data)
#         if not data.get("technician_id"):
#             return Response({
#                 'status':False,
#                 'message':"Technician id is required",
#                 "data":{}
#             })
#         obj = Rebooking.objects.get(technician = data.get("technician_id"))
        
#         serializer = RebookingSerializer(obj,data=data,partial = True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 'status':True,
#                 'message':'Success Data',
#                 'data':serializer.data
#             })
#         return Response({
#             'status':False,
#             'message':'invalid data',
#             'data':serializer.errors
#         })
#     except Exception as e:
#         print(e)
    
#     return Response({
#         'status':False,
#         'message':'Invalid Technician Id',
#         'data':{}
#     })



# @api_view(['PATCH'])
# def RebookingStatusUpdated(request):
#     try:
#         data = request.data
#         print("data", data)
        
#         # Technician ID validation
#         if not data.get("technician_id"):
#             return Response({
#                 'status': False,
#                 'message': "Technician id is required",
#                 "data": {}
#             })
        
#         # Fetch the first Rebooking object matching the technician_id
#         obj = Rebooking.objects.filter(technician=data.get("technician_id")).first()
        
#         if not obj:
#             return Response({
#                 'status': False,
#                 'message': 'No Rebooking found for the given technician ID',
#                 'data': {}
#             })
        
#         # Serialize and save the data
#         serializer = RebookingSerializer(obj, data=data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 'status': True,
#                 'message': 'Success Data',
#                 'data': serializer.data
#             })
        
#         return Response({
#             'status': False,
#             'message': 'Invalid data',
#             'data': serializer.errors
#         })
    
#     except Exception as e:
#         print("Error:", e)
#         return Response({
#             'status': False,
#             'message': 'An error occurred',
#             'data': {}
#         })


@api_view(['PATCH'])
def RebookingStatusUpdated(request):
    try:
        data = request.data
        print("data", data)
        
        # Technician ID validation
        if not data.get("technician_id"):
            return Response({
                'status': False,
                'message': "Technician id is required",
                "data": {}
            })
        
        # Fetch the first Rebooking object matching the technician_id
        obj = Rebooking.objects.filter(technician=data.get("technician_id")).first()
        
        if not obj:
            return Response({
                'status': False,
                'message': 'No Rebooking found for the given technician ID',
                'data': {}
            })
        
        # Serialize and save the data
        serializer = RebookingSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'message': 'Success Data',
                'data': serializer.data
            })
        
        return Response({
            'status': False,
            'message': 'Invalid data',
            'data': serializer.errors
        })
    
    except Exception as e:
        print("Error:", e)
        return Response({
            'status': False,
            'message': 'An error occurred',
            'data': {}
        })


# @api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def create_booking(request):
   
#     data = request.data
#     booking_products_data = data.pop('booking_products', [])
    
    
#     serializer = BkingSerializer(data=data)
    
#     if serializer.is_valid():
#         # print("gggg",serializer)
#         booking = serializer.save()

#         # Create BookingProduct instances if available
#         for booking_product_data in booking_products_data:
#             booking_product_data['booking'] = booking.id
#             # demo = booking_product_data.booking
#             # print("ssss",demo)
#             testo = booking_product_data['booking']
#             print("demoooo datasaa",booking_product_data['booking']) 
#             booking_product_serializer = BkingProductSerializer(data=booking_product_data)
#             print("demooooo",booking_product_serializer)
#             if booking_product_serializer.is_valid():
#                 print("gggg")
#                 booking_product_serializer.save()
#             else:
#                 # If there are any errors in BookingProduct data, delete the created Booking instance
#                 booking.delete()
#                 return Response({
#                     'status': 'error',
#                     'message': 'Invalid BookingProduct data',
#                     'errors': booking_product_serializer.errors
#                 })

#         return Response({
#             'status': 'ok',
#             'data': serializer.data
#         })
#     else:

#         return Response({
#             'status': 'error',
#             'message': 'Invalid Booking data',
#             'errors': serializer.errors
#         })
        



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_booking(request):
   
    data = request.data.copy()
    booking_products_data = data.pop('booking_products', [])
    
    # अगर स्लॉट नहीं दिया गया है तो booking_date के आधार पर स्लॉट निर्धारित करें
    if 'slot' not in data or not data['slot']:
        if 'booking_date' in data and data['booking_date']:
            try:
                # booking_date को datetime में कन्वर्ट करें
                booking_datetime = datetime.strptime(data['booking_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            except ValueError:
                try:
                    # अगर पहला फॉर्मेट काम नहीं करता, तो दूसरा फॉर्मेट आज़माएं
                    booking_datetime = datetime.strptime(data['booking_date'], '%Y-%m-%dT%H:%M:%S')
                except ValueError:
                    # अगर फिर भी काम नहीं करता, तो अन्य फॉर्मेट आज़माएं
                    try:
                        booking_datetime = datetime.fromisoformat(data['booking_date'].replace('Z', '+00:00'))
                    except ValueError:
                        # अगर कोई भी फॉर्मेट काम नहीं करता, तो एरर रिटर्न करें
                        return Response({
                            'status': 'error',
                            'message': 'Invalid booking_date format',
                        }, status=status.HTTP_400_BAD_REQUEST)
            
            booking_time = booking_datetime.time()
            
            # समय के आधार पर स्लॉट निर्धारित करें
            if booking_time >= datetime.strptime('08:00', '%H:%M').time() and booking_time < datetime.strptime('09:00', '%H:%M').time():
                data['slot'] = 1  # 08:00-09:00 AM
            elif booking_time >= datetime.strptime('09:00', '%H:%M').time() and booking_time < datetime.strptime('10:00', '%H:%M').time():
                data['slot'] = 2  # 09:00-10:00 AM
            elif booking_time >= datetime.strptime('10:00', '%H:%M').time() and booking_time < datetime.strptime('11:00', '%H:%M').time():
                data['slot'] = 3  # 10:00-11:00 AM
            elif booking_time >= datetime.strptime('11:00', '%H:%M').time() and booking_time < datetime.strptime('12:00', '%H:%M').time():
                data['slot'] = 4  # 11:00-12:00 PM
            elif booking_time >= datetime.strptime('12:00', '%H:%M').time() and booking_time < datetime.strptime('13:00', '%H:%M').time():
                data['slot'] = 5  # 12:00-01:00 PM
            elif booking_time >= datetime.strptime('13:00', '%H:%M').time() and booking_time < datetime.strptime('14:00', '%H:%M').time():
                data['slot'] = 6  # 01:00-02:00 PM
            elif booking_time >= datetime.strptime('14:00', '%H:%M').time() and booking_time < datetime.strptime('15:00', '%H:%M').time():
                data['slot'] = 7  # 02:00-03:00 PM
            elif booking_time >= datetime.strptime('15:00', '%H:%M').time() and booking_time < datetime.strptime('16:00', '%H:%M').time():
                data['slot'] = 8  # 03:00-04:00 PM
            elif booking_time >= datetime.strptime('16:00', '%H:%M').time() and booking_time < datetime.strptime('17:00', '%H:%M').time():
                data['slot'] = 9  # 04:00-05:00 PM
            elif booking_time >= datetime.strptime('17:00', '%H:%M').time() and booking_time < datetime.strptime('18:00', '%H:%M').time():
                data['slot'] = 10  # 05:00-06:00 PM
            elif booking_time >= datetime.strptime('18:00', '%H:%M').time() and booking_time < datetime.strptime('19:00', '%H:%M').time():
                data['slot'] = 11  # 06:00-07:00 PM
            elif booking_time >= datetime.strptime('19:00', '%H:%M').time() and booking_time < datetime.strptime('20:00', '%H:%M').time():
                data['slot'] = 12  # 07:00-08:00 PM
            elif booking_time >= datetime.strptime('20:00', '%H:%M').time():
                data['slot'] = 12  # रात 8 बजे के बाद सभी बुकिंग को अंतिम स्लॉट में डालें
    
    serializer = BkingSerializer(data=data)
    
    if serializer.is_valid():
        # print("gggg",serializer)
        booking = serializer.save()
        assign_employee_to_booking(booking)
        
        # Create BookingProduct instances if available
        for booking_product_data in booking_products_data:
            booking_product_data['booking'] = booking.id
            # demo = booking_product_data.booking
            # print("ssss",demo)
            testo = booking_product_data['booking']
            print("demoooo datasaa",booking_product_data['booking']) 
            booking_product_serializer = BkingProductSerializer(data=booking_product_data)
            print("demooooo",booking_product_serializer)
            if booking_product_serializer.is_valid():
                print("gggg")
                booking_product_serializer.save()
            else:
                # If there are any errors in BookingProduct data, delete the created Booking instance
                booking.delete()
                return Response({
                    'status': 'error',
                    'message': 'Invalid BookingProduct data',
                    'errors': booking_product_serializer.errors
                })

        return Response({
            'status': 'ok',
            'data': serializer.data
        })
    else:

        return Response({
            'status': 'error',
            'message': 'Invalid Booking data',
            'errors': serializer.errors
        })


class KycViewSet(ModelViewSet):
    # queryset = Kyc.objects.all()     
    serializer_class  = KycSerializer
    def get_queryset(self):
        technician_id = self.request.query_params.get('technician_id')
        print("techincian id",technician_id)
        if technician_id is not None:
            queryset = Kyc.objects.filter(technician_id=technician_id)
        else:
            queryset = Kyc.objects.all()
        return queryset
    
    # def put(self, request):
        
        
    #     id = request.data.get('id')
    #     # booking_id = request.data.get('booking_id')
    #     technician_id = request.data.get('technician_id')
    #     bank_active = request.data.get('bank_active')
    #     # print("kyc id",id,"technician id",technician_id,'bank active',bank_active)
    #     if id and technician_id:
    #         print(id)
    #         try:
    #             kyc = Kyc.objects.get(id=id)
    #             technician_id = Technician.objects.get(id=technician_id)
    #             kyc.bank_active = bank_active
    #             # booking.save()
    #             kyc.save()
    #             return Response({'success': True,'message':'Kyc updated Successfull'})
    #         except (Booking.DoesNotExist, TechnicianLocation.DoesNotExist):
    #             return Response({'success': False, 'message': 'Something Eror.'})
    #     else:
    #         return Response({'success': False, 'message': 'Kyc id technician_id and bank_active are required.'})
    
    def put(self, request):
        id = request.data.get('id')
        technician_id = request.data.get('technician_id')
        bank_active = request.data.get('bank_active')

        if id and technician_id:
            try:
                kyc = Kyc.objects.get(id=id)
                technician = Technician.objects.get(id=technician_id)

                # Set bank_active=False for all other Kyc instances of the same Technician
                Kyc.objects.filter(technician_id=technician).exclude(id=id).update(bank_active=False)

                kyc.bank_active = bank_active
                kyc.save()

                return Response({'success': True, 'message': 'Kyc updated successfully'})
            except (Kyc.DoesNotExist, Technician.DoesNotExist):
                return Response({'success': False, 'message': 'Something went wrong'})
        else:
            return Response({'success': False, 'message': 'Kyc id, technician_id and bank_active are required.'})


# -------------------------- KYC COUNTING ------------------------------- 


# @api_view(['GET'])
# def ExpertTaskCountViewSet(request):
#     technician_id = request.GET.get('technician') # retrieve the technician_id query parameter
#     print("teccc id",technician_id)

    
#     queryset = Task.objects.filter(
#         technician=technician_id,
#         booking__status="Completed"
#     )
    
#     count = queryset.count()
#     print("couting",count)

   
    
#     return Response({
#         'status': True,
#         'message': 'Task count retrieved successfully',
#         'data': count
#     })



@api_view(['GET'])
def ExpertTaskCountViewSet(request):
    technician_id = request.GET.get('technician_id') # retrieve the technician_id query parameter
    
    queryset = Task.objects.all()
    queryset2 = Task.objects.all()
    rebooking = Rebooking.objects.all()
    # if technician_id is not None:
    booking_completed = Task.objects.filter(technician_id=technician_id,booking__status="Completed").count()
    
    new_booking_count = queryset2.filter(technician=technician_id,booking__status="Assign").count()
    print(queryset)
    rebooking_count = rebooking.filter(technician=technician_id,status="Assign").count()
    print("sss",rebooking_count)
    # serializer=TaskSerializer(queryset,many=True)
    return Response({
        'status':True,
        'message':'Wallet History fetched',
        'Booking_Completed':booking_completed,
        'rebooking_count':rebooking_count,
        'new_booking_count':new_booking_count
    })

# ------------------------------- Job Enquiry --------------------------- 


class JobEnquiryViewSet(ModelViewSet):
    queryset = JobEnquiry.objects.all()     
    serializer_class  = JobEnquirySerliazer
     


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()     
    serializer_class  = ProductSerializer
    


class SparePartsViewSet(ReadOnlyModelViewSet):
    # queryset = SpareParts.objects.all()     
    serializer_class  = SparePartsSerializer
    def get_queryset(self):
        product_id = self.request.data.get('product_id')
        queryset = SpareParts.objects.all()

        if product_id:
            product = get_object_or_404(Product, pk=product_id)
            queryset = queryset.filter(product=product)

        return queryset
      
      

class SparePartsSubctegory(ReadOnlyModelViewSet):
    # queryset = SpareParts.objects.all()
    serializer_class = SparePartssubcategorySerializer

    def get_queryset(self):
        product_id = self.request.data.get("product_id")
        queryset = SpareParts.objects.all()

        if product_id:
            product = get_object_or_404(Product, pk=product_id)
            queryset = queryset.filter(product=product)

        return queryset

  

class AddonsViewSet(ModelViewSet):
    queryset = Addon.objects.all()     
    serializer_class  = AddonsSerializer
     

class AddonsGetViewSet(ModelViewSet):
    queryset = Addon.objects.all()     
    serializer_class  = AddonsGetSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete'] 
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)



# class AddonsGetViewSet(ModelViewSet):
#     serializer_class = AddonsGetSerializer
#     http_method_names = ['get', 'post', 'put', 'patch', 'delete']

#     def get_queryset(self):
#         booking_id = self.request.query_params.get('booking_id')
#         if booking_id:
#             return Addon.objects.filter(booking_prod_id__booking__id=booking_id)
#         return Addon.objects.none()  # 👈 empty if booking_id is not provided

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)


# ----------------- Technician Location -------------------- 


class TechnicianLocationViewSet(ModelViewSet):
    serializer_class = TechnicianLocationSerializer
    queryset = TechnicianLocation.objects.all()
    def post(self, request):
        booking_id = request.data.get('booking_id')
        location = request.data.get('location')
        print("booking id",booking_id)
        if booking_id and location:
            try:
                booking = Booking.objects.get(id=booking_id)
                technician_location = TechnicianLocation.objects.get(
                    technician=booking.technician,
                    booking=booking
                )
                technician_location.location = location
                technician_location.save()
                return Response({'success': True})
            except (Booking.DoesNotExist, TechnicianLocation.DoesNotExist):
                return Response({'success': False, 'message': 'Booking or technician location not found.'})
        else:
            return Response({'success': False, 'message': 'Booking id and location are required.'})

        
# ----------------------- Technician All Location -------------------         

# class TechnicianAllLocationViewSet(ModelViewSet):
#     serializer_class = AllTechnicianLocationSerializer
#     queryset = AllTechnicianLocation.objects.all()

class TechnicianAllLocationViewSet(ModelViewSet):
    serializer_class = AllTechnicianLocationSerializer
    queryset = AllTechnicianLocation.objects.all()

    def create(self, request, *args, **kwargs):
        technician_id = request.data.get('technician_id')
        location = request.data.get('location')

        try:
            all_technician_location = AllTechnicianLocation.objects.get(technician_id=technician_id, location=location)
            serializer = AllTechnicianLocationSerializer(all_technician_location, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except AllTechnicianLocation.DoesNotExist:
            serializer = AllTechnicianLocationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        technician_id = request.data.get('technician_id')
        location = request.data.get('location')

        try:
            all_technician_location = AllTechnicianLocation.objects.get(technician_id=technician_id, location=location)
            serializer = AllTechnicianLocationSerializer(all_technician_location, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except AllTechnicianLocation.DoesNotExist:
            return self.create(request, *args, **kwargs)

# ------------------------------------- show offline online -----------------------



class TechnicianOnlineViewSet(viewsets.ViewSet):
    
    def list(self, request):
        technician_id = request.query_params.get('technician_id')
        if technician_id:
            showonline_objs = showonline.objects.filter(technician_id=technician_id).order_by('-date')
            if showonline_objs.exists():
                serializer = TechnicianOnlineSerializer(showonline_objs.first())
                return Response({
                    'status': True,
                    'message': 'Technician online status fetched',
                    'data': serializer.data
                })
            return Response({
                'status': False,
                'message': f'No online status found for technician {technician_id}',
            })
        showonline_objs = showonline.objects.all()
        serializer = TechnicianOnlineSerializer(showonline_objs, many=True)
        return Response({
            'status': True,
            'message': 'Show Online Offline fetched',
            'data': serializer.data
        })

    def update(self, request, pk=None):
        try:
            instance = showonline.objects.get(pk=pk)
            serializer = TechnicianOnlineSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': True,
                    'message': f'Show Online Offline with id {pk} updated',
                    'data': serializer.data
                })
            else:
                return Response({
                    'status': False,
                    'message': 'Invalid data',
                    'data': serializer.errors
                })
        except showonline.DoesNotExist:
            return Response({
                'status': False,
                'message': f'Show Online Offline with id {pk} does not exist',
            })
    
    # def create(self, request):
    #     serializer = TechnicianOnlineSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({
    #             'status': True,
    #             'message': 'New Show Online Offline created',
    #             'data': serializer.data
    #         })
    #     else:
    #         return Response({
    #             'status': False,
    #             'message': 'Invalid data',
    #             'data': serializer.errors
    #         })
    


# ----------------------------- RechargeHistory ----------------------
# @api_view(['GET'])
# def get_RechargeHistory(request):
#     todo_objs = RechargeHistory.objects.all()
#     serializer=TechnicianRechargeHistorySerializer(todo_objs,many=True)
#     return Response({
#         'status':True,
#         'message':'Recharge History fetched',
#         'data':serializer.data
#     })

@api_view(['GET'])
def get_RechargeHistory(request):
    print("helooooooo")
    technician_id = request.GET.get('technician_id') # retrieve the technician_id query parameter
    queryset = RechargeHistory.objects.all()
    if technician_id is not None:
        queryset = queryset.filter(technician_id=technician_id) # filter queryset by technician_id if it is not None
    serializer = TechnicianRechargeHistorySerializer(queryset, many=True)
    return Response({
        'status': True,
        'message': 'Recharge History fetched',
        'data': serializer.data
    })


@api_view(['POST'])
def post_rechargeHistory(request):
    try:
        data = request.data
        serializer = TechnicianRechargeHistorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # Get the technician ID from the serializer data
            technician_id = serializer.data['technician_id']
            # Get the Wallet object for the technician
            technician_wallet = Wallet.objects.get(technician_id=technician_id)
            # Update the technician's total_share field with the amount from the serializer data
            technician_wallet.total_share += serializer.data['amount']
            technician_wallet.save()
            return Response({
                'status': True,
                'message': "success data",
                'data': serializer.data      
            })
        return Response({
            'status': False,
            'message': "invalid data",
            'data': serializer.errors  
        })
    except Exception as e:
        print(e)
        return Response({
            'status': False,
            'message': "Something went wrong",  
        })



# ------------------------ wallet --------------------------- 

@api_view(['GET'])
def get_Wallet(request):
    technician_id = request.GET.get('technician_id') # retrieve the technician_id query parameter
    print("hellooo",technician_id)
    queryset = Wallet.objects.all()
    if technician_id is not None:
        queryset = queryset.filter(technician_id=technician_id) 
    serializer=TechnicianWalletSerializer(queryset,many=True)
    return Response({
        'status':True,
        'message':'Wallet  fetched',
        'data':serializer.data
    })


# ----------------------------------- Wallet History ----------------------------- 


@api_view(['GET'])
def get_Wallet_History(request):
    technician_id = request.GET.get('technician_id') # retrieve the technician_id query parameter
    
    queryset = WalletHistory.objects.all()
    if technician_id is not None:
        queryset = queryset.filter(wallet__technician_id=technician_id) 
    serializer=TechnicianWalletHistorySerializer(queryset,many=True)
    return Response({
        'status':True,
        'message':'Wallet History fetched',
        'data':serializer.data
    })



# ----------------------------------- Withdraw Request ----------------------------- 


@api_view(['POST'])
def post_withdraw_req(request):
    try:
        data = request.data
        serializer = TechnicianWithdrawRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # Get the technician ID from the serializer data
            # technician_id = serializer.data['technician_id']
            # # Get the Wallet object for the technician
            # technician_wallet = Wallet.objects.get(technician_id=technician_id)
            # # Update the technician's total_share field with the amount from the serializer data
            # technician_wallet.total_share += serializer.data['amount']
            # technician_wallet.save()
            return Response({
                'status': True,
                'message': "success data",
                'data': serializer.data      
            })
        return Response({
            'status': False,
            'message': "invalid data",
            'data': serializer.errors  
        })
    except Exception as e:
        print(e)
        return Response({
            'status': False,
            'message': "Something went wrong",  
        })




@api_view(['GET'])
def get_Withdraw_Req(request):
    technician_id = request.GET.get('technician_id') # retrieve the technician_id query parameter
    
    queryset = WithdrawRequest.objects.all()
    if technician_id is not None:
        queryset = queryset.filter(technician_id=technician_id) 
    serializer=TechnicianWithdrawRequestSerializer(queryset,many=True)
    return Response({
        'status':True,
        'message':'Withdraw Request Send',
        'data':serializer.data
    })



class BlogGetViewSet(ReadOnlyModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'title'

    def retrieve(self, request, *args, **kwargs):
        # Get the title from the URL parameters
        title = self.kwargs['title']

        # Perform the lookup based on the title field
        queryset = self.filter_queryset(self.get_queryset())
        blog = self.get_object()
        
        # You can add any additional logic or filtering here if needed
        
        serializer = self.get_serializer(blog)
        return Response(serializer.data)

class OfferGetViewSet(ReadOnlyModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    lookup_field = 'name'

    def retrieve(self, request, *args, **kwargs):
        # Get the title from the URL parameters
        name = self.kwargs['name']

        # Perform the lookup based on the title field
        queryset = self.filter_queryset(self.get_queryset())
        offer = self.get_object()
        
        # You can add any additional logic or filtering here if needed
        
        serializer = self.get_serializer(offer)
        return Response(serializer.data)



class MostViewedGetViewSet(ReadOnlyModelViewSet):
    queryset = MostViewed.objects.all()
    serializer_class = MostViewedSerializer


# ----------------------Booking Customer Details ---------------- 

class CustomerBookingViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Booking.objects.all()     
    serializer_class  = BokingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            # Filter customers based on the authenticated user
            queryset = Booking.objects.filter(customer__admin=user)
        else:
            # If there is no authenticated user, return an empty queryset
            queryset = Customer.objects.none()

        return queryset
     

# ----------------------- Customer Login --------------------------- 


class CustomerViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Customer.objects.all()
    serializer_class = CustSerailizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            # Filter customers based on the authenticated user
            queryset = Customer.objects.filter(admin=user)
        else:
            # If there is no authenticated user, return an empty queryset
            queryset = Customer.objects.none()

        return queryset
    def partial_update(self, request, *args, **kwargs):
        # Retrieve the customer object to update
        instance = self.get_object()

        # Check if the current user is the owner of the customer object
        if instance.admin == request.user:
            print("useerrrrrrr",request.user)
            # serializer = self.get_serializer(instance, data=request.data, partial=True)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
            serializer = self.get_serializer(instance, data=request.data, partial=True,
                                             fields=['first_name', 'address', 'mobile', 'city', 'state', 'area', 'zipcode'])
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
    # queryset = Customer.objects.all() 
    # print("queryset",queryset)    
    # serializer_class  = CustomerSerailizer
     

    # def get(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data) 
    

    # def put(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)

def verify_otp(otp, user):
    # Implement your OTP verification logic here
    # Compare the provided OTP with the OTP associated with the user

    # For example, assuming you have an OTP field in the CustomUser model:
    if user.otp == otp:
        return True
    else:
        return False


# class CustomerLoginViewSet(CreateAPIView):
#     authentication_classes = [BasicAuthentication]
#     serializer_class = CustomerLoginSerliazer
#     def post(self,request,*args, **kwargs):
#         otp_number = random.randint(0,9999)
#         otp_unique = str(otp_number).zfill(3)
#         phone_number = request.POST.get('phone_number')

#         request.session['phone_number'] = phone_number
#         request.session['otp'] = otp_unique
#         username = "TRYGON"
#         apikey = "E705A-DFEDC"
#         apirequest="Text"
#         sender ="TRYGON"
#         mobile=phone_number
#         message=f"Dear User {otp_unique} is the OTP for your login at Trygon. In case you have not requested this, please contact us at info@trygon.in"
#         TemplateID="1707162192151162124"
#         url = f"https://sms.webtextsolution.com/sms-panel/api/http/index.php?username=TRYGON&apikey=E705A-DFEDC&apirequest=Text&sender={sender}&mobile={mobile}&message={urllib.parse.quote(message)}&route=TRANS&TemplateID=1707162192151162124&format=JSON"

#         response = requests.get(url) 
#         print("response",response)
        
#         # cust = Customer.objects.get(mobile=phone_number)
        
#         return Response({'message': 'Otp is sent your mobile number'}, status=status.HTTP_200_OK)
       


class CustomerLoginViewSet(CreateAPIView):
    authentication_classes = [BasicAuthentication]
    serializer_class = CustomerLoginSerliazer
    
    def post(self, request, *args, **kwargs):
        otp_number = random.randint(0, 9999)
        otp_unique = str(otp_number).zfill(3)
        phone_number = request.data.get('phone_number')
       

        request.session['phone_number'] = phone_number
        request.session['otp'] = otp_unique
        ottt = request.session.get('otp', 'Default value if key does not exist')
        
        
        username = "Homofix"
        apikey = "21141-B77C6"
        apirequest = "Text"
        sender = "HOMOFX"
        mobile = phone_number
        #message = f"Dear User {otp_unique} is the OTP for your login at Trygon. In case you have not requested this, please contact us at info@trygon.in"
        message =f"Your OTP for logging in to HOMOFIX COMPANY account is {otp_unique}. Do not share this OTP with anyone for security reasons. - HOMOFIX COMPANY"
        template_id = "1407169087502258386"
        
        url = f"https://sms.webtextsolution.com/sms-panel/api/http/index.php?username=Homofix&apikey=21141-B77C6&apirequest=Text&sender={sender}&mobile={mobile}&message={urllib.parse.quote(message)}&route=TRANS&TemplateID=1407169087502258386&format=JSON"
        
        response = requests.get(url) 
        
        
        
        return Response({'message': 'OTP is sent to your mobile number','otp_session':ottt}, status=status.HTTP_200_OK)
  
        
class CustomerLoginAPI(APIView):
    def post(self,request):
        try:
            data = request.data
            
            serializer = LoginCustomrSerializers(data = data)
            if serializer.is_valid():
                password = serializer.data['phone_number']
                
                if Customer.objects.filter(mobile=password).exists():
                    cus = Customer.objects.get(mobile=password)
                    username = cus.admin.username
                    

                    user = authenticate(password=password,username=username)
                    if user is None:
                        return Response({
                        'status':400,
                        'message':'Invalid Password',
                        'data':{}
                        })

                    user_type = user.user_type
                    if user_type == '4':
                        user_data = {
                            'id': user.customer.id,
                            'mobile': user.customer.mobile,
                            'message':'Login Success'
                            # 'username': user.username,
                            
                            # Add any other user fields you want to return
                    }
                    refresh = RefreshToken.for_user(user)

                    return Response({
                        # 'refresh': str(refresh),
                        'token': str(refresh.access_token),
                        'Customer': user_data
                    })
                else:
                    last_three_digits = password[-3:]
                    userr = "user"
                    
                    user = CustomUser.objects.create(username=userr+last_three_digits, user_type='4')    
                    user.set_password(password)
                    user.customer.mobile = password
                    user.save()
                    

                    custm = Customer.objects.get(mobile=password)
                    usernme = custm.admin.username
                   
                    usrr=authenticate(request,username=usernme, password = password)
                    if usrr is None:
                        return Response({
                        'status':400,
                        'message':'Invalid Password',
                        'data':{}
                        })
                    user_type = user.user_type
                    if user_type == '4':
                        user_data = {
                            'id': user.customer.id,
                            'username': user.username,
                            
                            # Add any other user fields you want to return
                    }
                    refresh = RefreshToken.for_user(usrr)

                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': user_data
                    })
            return Response({
                'status':400,
                'message':'something went wrong',
                'data':serializer.errors
            })
        except Exception as e:
            print(e)




# class CustomerLoginAPI(APIView):
#     def post(self, request):
#         try:
#             data = request.data
#             serializer = LoginCustomrSerializers(data=data)
#             if serializer.is_valid():
#                 password = serializer.data['phone_number']
#                 if Customer.objects.filter(mobile=password).exists():
#                     cus = Customer.objects.get(mobile=password)
#                     username = cus.admin.username
#                     user = authenticate(password=password, username=username)
#                     if user is None:
#                         return Response({
#                             'status': 400,
#                             'message': 'Invalid Password',
#                             'data': {}
#                         })

#                     user_type = user.user_type
#                     if user_type == '4':
#                         user_data = {
#                             'id': user.customer.id,
#                             'mobile': user.customer.mobile,
#                             'message': 'Login Success'
#                         }
#                         refresh = RefreshToken.for_user(user)

#                         return Response({
#                             'token': str(refresh.access_token),
#                             'Customer': user_data
#                         })
#                 else:
#                     last_three_digits = password[-3:]
#                     userr = "user"
#                     user = CustomUser.objects.create(username=userr+last_three_digits, user_type='4')    
#                     user.set_password(password)
#                     user.customer.mobile = password
#                     user.save()
#                     custm = Customer.objects.get(mobile=password)
#                     usernme = custm.admin.username
#                     usrr = authenticate(request, username=usernme, password=password)
#                     if usrr is None:
#                         return Response({
#                             'status': 400,
#                             'message': 'Invalid Password',
#                             'data': {}
#                         })
#                     user_type = user.user_type
#                     if user_type == '4':
#                         user_data = {
#                             'id': user.customer.id,
#                             'username': user.username
#                         }
#                         refresh = RefreshToken.for_user(usrr)

#                         return Response({
#                             'refresh': str(refresh),
#                             'access': str(refresh.access_token),
#                             'user': user_data
#                         })
#             else:
#                 return Response({
#                     'status': 400,
#                     'message': 'Invalid data',
#                     'data': serializer.errors
#                 })
#         except Exception as e:
#             print(e)
#             return Response({
#                 'status': 500,
#                 'message': 'Internal Server Error',
#                 'data': {}
#             })

# -------------------------------- feedback --------------------------

class FeedbackViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = feedback.objects.all()
    serializer_class = FeedbackSerailizer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        feedback_instances = self.get_queryset()
        serializer = self.get_serializer(feedback_instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user = request.user
        booking_id = request.data.get('booking_id')
        rating = request.data.get('rating')
        description = request.data.get('description')

        if not booking_id:
            return Response({'msg': 'booking_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not rating:
            return Response({'msg': 'rating is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not description:
            return Response({'msg': 'description is required.'}, status=status.HTTP_400_BAD_REQUEST)

        existing_feedback = feedback.objects.filter(booking_id=booking_id).first()
        if existing_feedback:
            return Response({'msg': 'Feedback already exists for the provided booking ID.'})
        
        try:
            task = Task.objects.get(booking=booking_id)
            technician_id = task.technician
            booking_instance = task.booking  # Assuming 'booking' is the ForeignKey field name in the Task model
            customer_instance = Customer.objects.get(admin=user)
            feedback_obj = feedback.objects.create(booking_id=booking_instance, customer_id=customer_instance, technician_id=technician_id, rating=rating, description=description)
            return Response({
                'status':"success",
                'msg':"feedback add successfully..",
                # 'customer_id': customer_instance.id,
                # 'technician_id': technician_id,
                # 'rating': rating,
                # 'description': description
            })
            
        except Task.DoesNotExist:
            return Response({'msg': 'Task not found for the provided booking ID.'})
        
        
        
       
    
                
class CustomerVerifyOtp(CreateAPIView):
    authentication_classes = [BasicAuthentication]
    serializer_class = VerifyOtpSerializer
    
    def post(self, request, *args, **kwargs):
        data = request.data
        Otp = data.get('OTPP')
        print("hellooooo")
        
        otp_nUMB = request.session.get('otp', 'Default value if key does not exist')
        print("OTP from session:", otp_nUMB)
        mobile = request.session.get('phone_number', 'Default value if key does not exist')
        
        return Response({
            'otp_input': Otp,
            'otp_session': otp_nUMB,
        })       # if otp == otp_no:
        #     if Customer.objects.filter(mobile=mobile).exists():
                
        #             cust = Customer.objects.get(mobile=mobile)
        #             username = cust.admin.username
        #             print("usernameeee",username)
                    
        #             user=authenticate(request,username=username, password = mobile)
                    # return Response({'message': 'Logged in successfully.'}, status=status.HTTP_200_OK)

        #             if user!=None:
        #                 login(request,user)
        #                 user_type = user.user_type
        #                 if user_type == '4':
        #                     user_data = {
        #                         'id': user.customer.id,
        #                         'username': user.username,
                                
        #                         # Add any other user fields you want to return
        #                     }
        #                     refresh = RefreshToken.for_user(user)
        #                     return Response({
        #                     # 'refresh': str(refresh),
        #                     'token': str(refresh.access_token),
        #                     'message': 'Logged in successfully.','user': user_data
        #                 })
                    
        #                     # return Response({'message': 'Logged in successfully.','user': user_data}, status=status.HTTP_200_OK)
        #     else:
        #         last_three_digits = mobile[-3:]
        #         userr = "user"
        #         user = CustomUser.objects.create(username=userr+last_three_digits, user_type='4')    
        #         user.set_password(mobile)
        #         user.customer.mobile = mobile
        #         user.save()
                

        #         custm = Customer.objects.get(mobile=mobile)
        #         usernme = custm.admin.username
        #         print("usernammeee",usernme)
        #         usrr=authenticate(request,username=usernme, password = mobile)
        #         if usrr!=None:
        #                 login(request,user)
        #                 user_type = usrr.user_type
        #                 if user_type == '4':
        #                     user_data1 = {
        #                         'id': usrr.customer.id,
        #                         'username': usrr.username,
                                
        #                         # Add any other user fields you want to return
        #                     }
        #                     refresh = RefreshToken.for_user(usrr)
        #                     return Response({
        #                     # 'refresh': str(refresh),
        #                     'token': str(refresh.access_token),
        #                     'message': 'Logged in successfully.','user': user_data1
        #                 })
                    
        #                     # return Response({'message': 'Logged in successfully.','user': user_data1}, status=status.HTTP_200_OK)
        # return Response({'message': 'Invalid Otp.'}, status=status.HTTP_401_UNAUTHORIZED)

        
# class CustomerVerifyOtp(CreateAPIView):
#     authentication_classes = [BasicAuthentication]
#     serializer_class = VerifyOtpSerializer
#     def post(self,request,*args, **kwargs):
#         otp = request.POST.get('otp')
#         otp_no = request.session.get('otp', 'Default value if key does not exist')
#         mobile = request.session.get('phone_number', 'Default value if key does not exist')
#         if otp == otp_no:
#             if Customer.objects.filter(mobile=mobile).exists():
                
#                     cust = Customer.objects.get(mobile=mobile)
#                     username = cust.admin.username
#                     print("usernameeee",username)
                    
#                     user=authenticate(request,username=username, password = mobile)
#                     # return Response({'message': 'Logged in successfully.'}, status=status.HTTP_200_OK)

#                     if user!=None:
#                         login(request,user)
#                         user_type = user.user_type
#                         if user_type == '4':
#                             user_data = {
#                                 'id': user.customer.id,
#                                 'username': user.username,
                                
#                                 # Add any other user fields you want to return
#                             }
#                             refresh = RefreshToken.for_user(user)
#                             return Response({
#                             # 'refresh': str(refresh),
#                             'token': str(refresh.access_token),
#                             'message': 'Logged in successfully.','user': user_data
#                         })
                    
#                             # return Response({'message': 'Logged in successfully.','user': user_data}, status=status.HTTP_200_OK)
#             else:
#                 last_three_digits = mobile[-3:]
#                 userr = "user"
#                 user = CustomUser.objects.create(username=userr+last_three_digits, user_type='4')    
#                 user.set_password(mobile)
#                 user.customer.mobile = mobile
#                 user.save()
                

#                 custm = Customer.objects.get(mobile=mobile)
#                 usernme = custm.admin.username
#                 print("usernammeee",usernme)
#                 usrr=authenticate(request,username=usernme, password = mobile)
#                 if usrr!=None:
#                         login(request,user)
#                         user_type = usrr.user_type
#                         if user_type == '4':
#                             user_data1 = {
#                                 'id': usrr.customer.id,
#                                 'username': usrr.username,
                                
#                                 # Add any other user fields you want to return
#                             }
#                             refresh = RefreshToken.for_user(usrr)
#                             return Response({
#                             # 'refresh': str(refresh),
#                             'token': str(refresh.access_token),
#                             'message': 'Logged in successfully.','user': user_data1
#                         })
                    
#                             # return Response({'message': 'Logged in successfully.','user': user_data1}, status=status.HTTP_200_OK)
#         return Response({'message': 'Invalid Otp.'}, status=status.HTTP_401_UNAUTHORIZED)

        
                
                

            
# ------------------------ Category ------------------------ 



class CategoryGetViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
            

# ------------------------ Subcategory ------------------------ 


# class SubcategoryGetViewSet(ReadOnlyModelViewSet):
#     queryset = SubCategory.objects.all()
#     serializer_class = SubcategorySerializer

class SubcategoryGetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubcategorySerializer
    lookup_field = 'name' 

    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     subcategory_name  = self.request.query_params.get('name')
    #     if subcategory_name  is not None:
    #         queryset = queryset.filter(name=subcategory_name)
    #     return queryset
        

class LoginAPI(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = LoginCustomrSerializers(data = data)
            if serializer.is_valid():
                password = serializer.data['password']
                cus = Customer.objects.get(mobile=password)
                username = cus.admin.username
                print("usernameee",username)

                user = authenticate(password=password,username=username)
                if user is None:
                    return Response({
                    'status':400,
                    'message':'Invalid Password',
                    'data':{}
                    })
                refresh = RefreshToken.for_user(user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })

            return Response({
                'status':400,
                'message':'something went wrong',
                'data':serializer.errors
            })
        except Exception as e:
            print(e)


class BlogByTitleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'title'            





class HomePageServiceViewSet(ModelViewSet):
    queryset = HomePageService.objects.all()     
    serializer_class  = HomePageSerailizer







class CustomerLogin(APIView):
    def post(self,request):
        data = request.data 
        serializer = CustomerLoginn(data = data)
        if serializer.is_valid():
            # return Response(data)
            phone_number = serializer.validated_data.get('phone_number')
            # print("helooo phone",phone_number)
            # return Response({
            #     'phone_number':phone_number
            # })
            
            if Customer.objects.filter(mobile=phone_number).exists():
            
                cust = Customer.objects.get(mobile=phone_number)
                username = cust.admin.username
                print("usernameeee",username)
                
                user=authenticate(request,username=username, password = phone_number)
                # return Response({'message': 'Logged in successfully.'}, status=status.HTTP_200_OK)

                if user!=None:
                    login(request,user)
                    user_type = user.user_type
                    if user_type == '4':
                        user_data = {
                            'id': user.customer.id,
                            'username': user.username,
                            
                            # Add any other user fields you want to return
                        }
                        refresh = RefreshToken.for_user(user)
                        return Response({
                        # 'refresh': str(refresh),
                        'token': str(refresh.access_token),
                        'message': 'Logged in successfully.','user': user_data
                    })
                
                        # return Response({'message': 'Logged in successfully.','user': user_data}, status=status.HTTP_200_OK)
            else:
                print("nooooo")
                last_three_digits = phone_number[-3:]
                userr = "user"
                user = CustomUser.objects.create(username=phone_number, user_type='4')    
                user.set_password(phone_number)
                user.customer.mobile = phone_number
                user.save()

                
                    
                custm = Customer.objects.get(mobile=phone_number)
                usernme = custm.admin.username
                print("usernammeee",usernme)
                usrr=authenticate(request,username=usernme, password = phone_number)
                if usrr!=None:
                    login(request,user)
                    user_type = usrr.user_type
                    if user_type == '4':
                        user_data1 = {
                            'id': usrr.customer.id,
                            'username': usrr.username,
                            
                            # Add any other user fields you want to return
                        }
                        refresh = RefreshToken.for_user(usrr)
                        return Response({
                        # 'refresh': str(refresh),
                        'token': str(refresh.access_token),
                        'message': 'Logged in successfully.','user': user_data1
                    })
        
        # try:
            
            
        #     if serializer.is_valid():
        #         password = serializer.data['password']
        #         cus = Customer.objects.get(mobile=password)
        #         username = cus.admin.username
        #         print("usernameee",username)

        #         user = authenticate(password=password,username=username)
        #         if user is None:
        #             return Response({
        #             'status':400,
        #             'message':'Invalid Password',
        #             'data':{}
        #             })
        #         refresh = RefreshToken.for_user(user)

        #         return Response({
        #             'refresh': str(refresh),
        #             'access': str(refresh.access_token),
        #         })

        #     return Response({
        #         'status':400,
        #         'message':'something went wrong',
        #         'data':serializer.errors
        #     })
        # except Exception as e:
        #     print(e)

class addonsDelete(APIView):
    def delete(self, request):
        data = request.data
        serializer = AddonsDeleteSerailizers(data=data)
        if serializer.is_valid():
            try:
                id = serializer.data['id']
                addon = Addon.objects.get(id=id)
                addon.delete()
                return Response({
                    'message': "Addons Delete Successfully"
                })
            except Addon.DoesNotExist:
                return Response({
                    'message': "Addon not found"
                })
        return Response({
            'message': "Invalid Id"
        })     


class ApplicantCarrerViewSet(ModelViewSet):
    queryset = ApplicantCarrer.objects.all()     
    serializer_class  = ApplicantCarrerSerliazer



class CarrerViewedGetViewSet(ReadOnlyModelViewSet):
    queryset = Carrer.objects.filter(status = True)
    serializer_class = CarrerSerliazer    



# ------------------------- Lega Page ----------------------- 
class LegalPageViewSet(ReadOnlyModelViewSet):
    queryset = LegalPage.objects.all()
    serializer_class = LegalPageSerializer    



# ------------------- generate PDF ------------------     
@api_view(['GET'])
def generate_invoice_pdf(request):
    print("helloooo")
    category_objs = Category.objects.all()
    params = {
        # 'today':datetime
        'category_objs':category_objs
    }
    file_name,status= save_pdf(params)
    if not status:
        return Response({
       'status':400
    })

    # file_path = f'/static/invoice/{file_name}'
    # print("file path",file_path)

    
    return Response({
       'status':200,
       'path':f'/media/{file_name}.pdf'
    })



# @api_view(['GET'])
# def invoice_pdf(request, booking_id):
#     try:
#         invoice = Invoice.objects.get(booking_id=booking_id)
#         invoice_data = invoice.invoice if invoice else None

#         if invoice_data:
#             response = HttpResponse(invoice_data, content_type='application/pdf')
#             response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
#             return response
#         else:
#             return Response({
#                 'status': 404,
#                 'message': 'Invoice not found.'
#             })
#     except Invoice.DoesNotExist:
#         return Response({
#             'status': 404,
#             'message': 'Invoice not found.'
#         })



@api_view(['GET'])
def invoice_pdf(request, booking_id):
    try:
        invoice = Invoice.objects.get(booking_id=booking_id)
        invoice_data = invoice.invoice if invoice else None

        if invoice_data:
            response_data = {
                'status': 200,
                'invoice_url': request.build_absolute_uri(reverse('invoice_download', args=[booking_id])),
            }

            return Response(response_data)
        else:
            return Response({
                'status': 404,
                'message': 'Invoice not found.'
            })
    except Invoice.DoesNotExist:
        return Response({
            'status': 404,
            'message': 'Invoice not found.'
        })



@api_view(['GET'])
def invoice_download(request, booking_id):
    try:
        invoice = Invoice.objects.get(booking_id=booking_id)
        invoice_data = invoice.invoice if invoice else None

        if invoice_data:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename="invoice.pdf"'
            response.write(invoice_data)
            return response
        else:
            return Response({
                'status': 404,
                'message': 'Invoice not found.'
            })
    except Invoice.DoesNotExist:
        return Response({
            'status': 404,
            'message': 'Invoice not found.'
        })





@api_view(['GET'])
def expert_invoice_pdf(request, booking_id):
    try:
        invoice = Invoice.objects.get(booking_id=booking_id)
        invoice_data = invoice.invoice if invoice else None

        if invoice_data:
            download_url = reverse('expert_invoice_download', args=[booking_id])
            # view_url = reverse('invoice_view', args=[booking_id])
            response_data = {
                'status': 200,
                'message': 'Invoice found.',
                'download_url': request.build_absolute_uri(download_url),
                # 'view_url': request.build_absolute_uri(view_url),
            }
            return Response(response_data)
        else:
            return Response({
                'status': 404,
                'message': 'Invoice not found.'
            })
    except Invoice.DoesNotExist:
        return Response({
            'status': 404,
            'message': 'Invoice not found.'
        })  




def expert_invoice_download(request, booking_id):
    try:
        invoice = Invoice.objects.get(booking_id=booking_id)
        invoice_data = invoice.invoice if invoice else None

        if invoice_data:
            response = HttpResponse(invoice_data, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
            return response
        else:
            return HttpResponse("Invoice not found.", status=404)
    except Invoice.DoesNotExist:
        return HttpResponse("Invoice not found.", status=404)              
# class FAQViewSet(ReadOnlyModelViewSet):
#     queryset = FAQ.objects.all()     
#     serializer_class  = faqSerializer
#     lookup_field = 'product'



class FAQViewSet(ReadOnlyModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = faqSerializer
    lookup_field = 'product'

    def retrieve(self, request, *args, **kwargs):
        product = self.kwargs['product']
        queryset = self.filter_queryset(self.get_queryset())
        
        faqs = queryset.filter(product=product)
        if not faqs.exists():
            raise NotFound("No FAQs found for the given product.")
        
        serializer = self.get_serializer(faqs, many=True)
        return Response(serializer.data)




# ------------------------------ HOD PERCENTAGE --------------------------


class HodPercentageViewSet(ReadOnlyModelViewSet):
    queryset = HodSharePercentage.objects.all()
    serializer_class = HodSharPercentageSerliazer
    
   
    
@api_view(['POST'])
def check_coupon_validity(request):
    code = request.data.get('code')  # Assuming the coupon code is sent in the request data

    try:
        coupon = Coupon.objects.get(code=code)
    except Coupon.DoesNotExist:
        return Response({'message': 'Invalid coupon code'}, status=400)

    current_datetime = timezone.now()
    if current_datetime <= coupon.validity_period:
        serializer = CouponSerializer(coupon)
        return Response(serializer.data)
    else:
        return Response({'message': 'Coupon expired'}, status=400)


class TokenExpirationCheckAPIView(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]  # Extract the token from the Authorization header

        try:
            refresh_token = RefreshToken(token)
            expiration_date = refresh_token.current_time + timedelta(seconds=refresh_token.access_token.lifetime)

            if expiration_date <= timezone.now():
                return Response({'expired': True}, status=status.HTTP_200_OK)
            else:
                return Response({'expired': False}, status=status.HTTP_200_OK)

        except TokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)




# ---------------------- Testing ----------------------- 


class TskListAPIView(generics.ListAPIView):
    serializer_class = TskSerializer

    def get_queryset(self):
        technician_id = self.kwargs['technician_id']  # Assumes the technician ID is passed as a URL parameter
        print("tidd",technician_id)
        return Task.objects.filter(technician_id=technician_id)


# ---------------------------- Payment -------------------------- 



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def customerpayments(request):
    user = request.user
    data = request.data
    serializer = PaymentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()

        return Response({
            'status':"success",
            'data':serializer.data
        })
    
    return Response({
            'status':"Error",
            'data':serializer.errors
        })
    


class PaymentViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Payment.objects.all()     
    serializer_class  = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            # Filter customers based on the authenticated user
            queryset = Payment.objects.filter(booking_id__customer__admin=user)
        else:
            # If there is no authenticated user, return an empty queryset
            queryset = Customer.objects.none()

        return queryset
  

# class CustomerBookingViewSet(ModelViewSet):
#     authentication_classes = [JWTAuthentication]
#     queryset = Booking.objects.all()     
#     serializer_class  = BokingSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user

#         if user.is_authenticated:
#             # Filter customers based on the authenticated user
#             queryset = Booking.objects.filter(customer__admin=user)
#         else:
#             # If there is no authenticated user, return an empty queryset
#             queryset = Customer.objects.none()

#         return queryset
     




@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def customerupdateprofile(request):
    user = request.user
    customer = user.customer  # Assuming the customer profile is already created for the user
    data = request.data

    # Update the first_name field of the associated CustomUser model
    user.first_name = data.get('first_name', user.first_name)
    user.save()

    serializer = cuSeralizerDemo(customer, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()

        # Include first_name in the serialized data
        serializer.data['first_name'] = user.first_name

        return Response({
            'status': "success",
            'data': serializer.data
        })

    return Response({
        'status': "Error",
        'data': serializer.errors
    })






class SettlementViewSet(ReadOnlyModelViewSet):
    serializer_class = SettlementSeralizer

    def get_queryset(self):
        technician_id = self.request.query_params.get('technician_id')
        queryset = Settlement.objects.all()
        if technician_id:
            queryset = queryset.filter(technician_id=technician_id)
        return queryset





class CustomerBookingDetailsViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Booking.objects.all()     
    serializer_class  = CustomerBookingDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            # Filter bookings based on the authenticated customer
            queryset = Booking.objects.filter(customer__admin=user)
            print("query set",queryset)
        else:
            # If there is no authenticated user, return an empty queryset
            queryset = Booking.objects.none()

        return queryset
  
  

@api_view(["POST"])
def front_booking_status(request):
    booking_id = request.data.get("booking_id")

    # Check if booking_id is provided
    if not booking_id:
        return Response(
            {"message": "Booking ID is required", "status": "ERROR"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        booking = Booking.objects.get(id=booking_id)
        booking.status = "Cancelled"
        booking.save()
        # If the booking exists, return a success response
        return Response(
            {"message": "Booking Cancelled Successfully...", "status": "OK"},
            status=status.HTTP_200_OK,
        )
    except Booking.DoesNotExist:
        # If the booking does not exist, return an error response
        return Response(
            {"message": "Booking ID does not match", "status": "ERROR"},
            status=status.HTTP_404_NOT_FOUND,
        )


class TechnicianStatusUpdate(APIView):
    def post(self, request, technician_id):
        try:
            technician = Technician.objects.get(pk=technician_id)
        except Technician.DoesNotExist:
            return Response(
                {"message": "Technician not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TechnicianStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            new_status = serializer.validated_data['new_status']
            technician.status = new_status
            technician.save()
            return Response({"message": "Status updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# --------------- SLOT CHECKING -------------------------
from django.utils import timezone
from datetime import datetime, time

# --------------- SLOT CHECKING -------------------------
from datetime import datetime, time as dt_time
# from django.utils import timezone
# from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication

# Slot choices dict
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





# @api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def check_slot_availability(request):
#     """
#     Check all slots availability (1-12) for:
#     - zipcode
#     - date
#     - subcategory_ids (list)
#     """

#     data = request.data

#     zipcode = data.get("zipcode")
#     date_str = data.get("date")
#     subcategory_ids = data.get("subcategory_ids", [])

#     if not zipcode or not date_str or not subcategory_ids:
#         return Response({
#             "status": "error",
#             "message": "zipcode, date, and subcategory_ids are required fields."
#         })

#     # Parse subcategory_ids
#     try:
#         subcategory_ids = list(map(int, subcategory_ids))
#         subcategories = SubCategory.objects.filter(id__in=subcategory_ids)
#         if not subcategories.exists():
#             return Response({
#                 "status": "error",
#                 "message": "No valid subcategories found."
#             })
#     except:
#         return Response({
#             "status": "error",
#             "message": "subcategory_ids must be a list of integers."
#         })

#     # Convert date string to timezone-aware datetime
#     try:
#         date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
#         naive_datetime = datetime.combine(date_obj, dt_time.min)
#         aware_datetime = timezone.make_aware(naive_datetime)
#     except ValueError:
#         return Response({
#             "status": "error",
#             "message": "Invalid date format. Use YYYY-MM-DD."
#         })

#     universal_slot_obj = UniversalCredential.objects.first()
#     universal_limit = universal_slot_obj.universal_slot if universal_slot_obj and universal_slot_obj.universal_slot is not None else 0

#     response_slots = []

#     for slot_number in range(1, 13):
#         slots = Slot.objects.filter(
#             # date=date_obj,  # Uncomment if needed
#             slot=slot_number,
#             subcategories__in=subcategories
#         ).distinct()

#         matching_slot = None
#         if slots.exists():
#             for slot_obj in slots:
#                 if slot_obj.pincode.filter(code=int(zipcode)).exists():
#                     matching_slot = slot_obj
#                     break

#         # ✅ Determine limit
#         if matching_slot and matching_slot.limit is not None:
#             limit = matching_slot.limit
#         else:
#             limit = universal_limit

#         if limit == 0:
#             limit = universal_limit  # fallback

#         # Calculate current assigned bookings
#         aware_start_dt = timezone.make_aware(datetime.combine(date_obj, dt_time.min))
#         aware_end_dt = timezone.make_aware(datetime.combine(date_obj, dt_time.max))
#         current_count = Booking.objects.filter(
#             booking_date__range=(aware_start_dt, aware_end_dt),
#             slot=slot_number,
#             zipcode=zipcode,
#             # status='Assign'
#         ).count()

#         remaining = limit - current_count

#         response_slots.append({
#             "slot": slot_number,
#             "time": SLOT_CHOICES_DICT.get(slot_number, f"Slot {slot_number}"),
#             "status": "available" if remaining > 0 else "unavailable",
#             "limit": limit,
#             "current_bookings": current_count,
#             "remaining_slots": remaining if remaining > 0 else 0
#         })


#     # for slot_number in range(1, 13):
#     #     print("okkkkkkkkkkkkkkkkkkkkkkk")
#     #     # Find matching slots
#     #     slots = Slot.objects.filter(
#     #         # date=date_obj,
#     #         slot=slot_number,
#     #         subcategories__in=subcategories
#     #     ).distinct()
#     #     print("gggggggggoooooooooooooooooooooooo",slots)

#     #     matching_slot = None
#     #     if slots.exists():
#     #         for slot_obj in slots:
#     #             if slot_obj.pincode.filter(code=int(zipcode)).exists():
#     #                 matching_slot = slot_obj
#     #                 break

#     #     # ✅ Determine limit
#     #     if matching_slot and matching_slot.limit is not None:
#     #         # Use specific slot limit if available
#     #         limit = matching_slot.limit
#     #         print(f"✅ Slot {slot_number} → Using Slot limit: {limit}")
#     #     else:
#     #         # Fall back to universal limit
#     #         limit = universal_limit
#     #         print(f"⚠ Slot {slot_number} → No specific slot found. Using Universal limit: {limit}")

#     #     if limit == 0:
#     #         # Skip if limit is 0
#     #         continue

#     #     # Calculate current assigned bookings in this slot
#     #     aware_start_dt = timezone.make_aware(datetime.combine(date_obj, dt_time.min))
#     #     aware_end_dt = timezone.make_aware(datetime.combine(date_obj, dt_time.max))
#     #     current_count = Booking.objects.filter(
#     #         booking_date__range=(aware_start_dt, aware_end_dt),
#     #         slot=slot_number,
#     #         zipcode=zipcode,
#     #         # status='Assign'
#     #     ).count()

#     #     remaining = limit - current_count
#     #     if remaining > 0:
#     #         response_slots.append({
#     #             "slot": slot_number,
#     #             "time": SLOT_CHOICES_DICT.get(slot_number, f"Slot {slot_number}"),
#     #             "status": "available",
#     #             "limit": limit,
#     #             "current_bookings": current_count,
#     #             "remaining_slots": remaining
#     #         })
#     #     else:
#     #         print(f"❌ Slot {slot_number} → Limit reached. Skipping.")



#     return Response({
#         "status": "ok",
#         "slots": response_slots
#     })






@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def check_slot_availability(request):
    """
    Check all slots availability (1-12) for:
    - zipcode
    - date
    - subcategory_ids (list)
    
    Logic:
    1. If a slot with date, null slot, pincode, subcategory exists with limit=0, all slots for that date are unavailable
    2. If a slot with date, specific slot, pincode, subcategory exists with limit=0, that slot is unavailable
    3. If no pincode is provided in the database slot, it applies to all zipcodes
    """

    data = request.data

    zipcode = data.get("zipcode")
    date_str = data.get("date")
    subcategory_ids = data.get("subcategory_ids", [])

    if not date_str or not subcategory_ids:
        return Response({
            "status": "error",
            "message": "date and subcategory_ids are required fields."
        })

    # Parse subcategory_ids
    try:
        subcategory_ids = list(map(int, subcategory_ids))
        subcategories = SubCategory.objects.filter(id__in=subcategory_ids)
        if not subcategories.exists():
            return Response({
                "status": "error",
                "message": "No valid subcategories found."
            })
    except:
        return Response({
            "status": "error",
            "message": "subcategory_ids must be a list of integers."
        })

    # Convert date string to timezone-aware datetime
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        naive_datetime = datetime.combine(date_obj, dt_time.min)
        aware_datetime = timezone.make_aware(naive_datetime)
    except ValueError:
        return Response({
            "status": "error",
            "message": "Invalid date format. Use YYYY-MM-DD."
        })

    universal_slot_obj = UniversalCredential.objects.first()
    universal_limit = universal_slot_obj.universal_slot if universal_slot_obj and universal_slot_obj.universal_slot is not None else 0

    response_slots = []

    # Check for a slot with null slot value for this date and subcategories
    # This means all slots for this date should be unavailable
    null_slot_exists = False
    null_slots = Slot.objects.filter(
        date=date_obj,
        slot=None,
        subcategories__in=subcategories
    ).distinct()
    
    for null_slot in null_slots:
        # Check if zipcode matches or if no pincode restriction exists
        if (zipcode and null_slot.pincode.exists() and null_slot.pincode.filter(code=int(zipcode)).exists()) or \
           (not null_slot.pincode.exists()):
            if null_slot.limit == 0:
                null_slot_exists = True
                break
    
    # If a null slot with limit=0 exists, all slots are unavailable
    if null_slot_exists:
        for slot_number in range(1, 13):
            response_slots.append({
                "slot": slot_number,
                "time": SLOT_CHOICES_DICT.get(slot_number, f"Slot {slot_number}"),
                "status": "unavailable",
                "limit": 0,
                "current_bookings": 0,
                "remaining_slots": 0
            })
        
        return Response({
            "status": "ok",
            "slots": response_slots
        })

    # Process each slot normally if no null slot exists
    for slot_number in range(1, 13):
        # Default values
        limit = universal_limit
        matching_slot = None
        # Flag to track if we've already added this slot to the response
        slot_added = False
        
        # Check for specific slot configurations in the database
        slots = Slot.objects.filter(
            date=date_obj,
            slot=slot_number,
            subcategories__in=subcategories
        ).distinct()

        if slots.exists():
            for slot_obj in slots:
                # Case 1: If zipcode is provided and slot has matching pincode
                if zipcode and slot_obj.pincode.exists() and slot_obj.pincode.filter(code=int(zipcode)).exists():
                    matching_slot = slot_obj
                    break
                # Case 2: If slot has no pincode restrictions (applies to all)
                elif not slot_obj.pincode.exists():
                    matching_slot = slot_obj
                    break

        # Determine limit based on matching slot
        if matching_slot and matching_slot.limit is not None:
            if matching_slot.limit == 0:
                # If limit is 0, slot is unavailable
                response_slots.append({
                    "slot": slot_number,
                    "time": SLOT_CHOICES_DICT.get(slot_number, f"Slot {slot_number}"),
                    "status": "unavailable",
                    "limit": 0,
                    "current_bookings": 0,
                    "remaining_slots": 0
                })
                # Mark this slot as added and skip further processing
                slot_added = True
            else:
                # Use the specific slot's limit
                limit = matching_slot.limit

        # Skip the rest of the processing if we've already added this slot
        if slot_added:
            continue

        # Calculate current assigned bookings
        aware_start_dt = timezone.make_aware(datetime.combine(date_obj, dt_time.min))
        aware_end_dt = timezone.make_aware(datetime.combine(date_obj, dt_time.max))
        
        booking_filter = {
            'booking_date__range': (aware_start_dt, aware_end_dt),
            'slot': slot_number,
        }
        
        if zipcode:
            booking_filter['zipcode'] = zipcode
            
        current_count = Booking.objects.filter(**booking_filter).count()
        remaining = limit - current_count

        # If limit is 0, slot is unavailable
        if limit == 0:
            response_slots.append({
                "slot": slot_number,
                "time": SLOT_CHOICES_DICT.get(slot_number, f"Slot {slot_number}"),
                "status": "unavailable",
                "limit": limit,
                "current_bookings": current_count,
                "remaining_slots": 0
            })
        else:
            response_slots.append({
                "slot": slot_number,
                "time": SLOT_CHOICES_DICT.get(slot_number, f"Slot {slot_number}"),
                "status": "available" if remaining > 0 else "unavailable",
                "limit": limit,
                "current_bookings": current_count,
                "remaining_slots": remaining if remaining > 0 else 0
            })

    return Response({
        "status": "ok",
        "slots": response_slots
    })




@api_view(["POST"])
def save_fcm_token(request):
    tech_id = request.data.get("technician_id")
    token = request.data.get("fcm_token")

    if not tech_id or not token:
        return Response({"success": False, "message": "technician_id and fcm_token required"})

    try:
        technician = Technician.objects.get(id=tech_id)
        technician.fcm_token = token
        technician.save()
        return Response({"success": True, "message": "Token saved successfully"})
    except Technician.DoesNotExist:
        return Response({"success": False, "message": "Technician not found"})



class WorkingStateCityViewSet(ReadOnlyModelViewSet):
    authentication_classes = [BasicAuthentication]
    serializer_class = WorkingStateCitySerializer
    queryset = WorkingStateCity.objects.all()
    http_method_names = ['get']

    def get_queryset(self):
        queryset = super().get_queryset()
        state = self.request.query_params.get('state')
        if state:
            queryset = queryset.filter(state__iexact=state)
        return queryset

# @api_view(["POST"])
# def save_fcm_token(request):
#     tech_id = request.data.get("technician_id")
#     token = request.data.get("fcm_token")

#     if not tech_id or not token:
#         return Response({"success": False, "message": "technician_id and fcm_token required"})

#     try:
#         technician = Technician.objects.get(id=tech_id)

#         if technician.fcm_token == token:
#             return Response({"success": True, "message": "Token already up to date"})
        
#         technician.fcm_token = token
#         technician.save()

#         return Response({"success": True, "message": "Token saved/updated successfully"})
#     except Technician.DoesNotExist:
#         return Response({"success": False, "message": "Technician not found"})
