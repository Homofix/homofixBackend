from django.urls import path
from homofix_app import views,HodViews
from homofix_app import views
from django.conf import settings
from django.conf.urls.static import static
from homofix_app import views
from django.views.static import serve
from django.urls import re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    re_path('media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path('static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('All/Location',HodViews.all_location,name="all_location"),
    path('',views.login,name="login"),
    path('user/logout',views.logout_user,name="user_logout"),

    

    path("Accounts/Admin/Dashboard/",HodViews.admin_dashboard,name="admin_dashboard"),
    path('Accounts/Admin/Add',HodViews.add_admin,name="add_admin"),
    path('Accounts/Admin/Edit/<int:id>',HodViews.edit_admin,name="edit_admin"),
    path('Accounts/Admin/Update/',HodViews.update_admin,name="update_admin"),
    path('Accounts/Admin/Delete/<int:id>',HodViews.delete_admin,name="delete_admin"),
    path('Accounts/Admin/List',HodViews.admin_list,name="admin_list"),
    path('Accounts/Admin/Profile',HodViews.admin_profile,name="admin_profile"),
    path('Accounts/Admin/Updata/Profile',HodViews.admin_update_profile,name="admin_update_profile"),
    path('Accounts/Admin/Category/',HodViews.category,name="category"),
    path('Add/Category',HodViews.add_category,name="add_category"),
    path('Category/Delete/<int:id>',HodViews.delete_Category,name="delete_Category"),
    path('Category/Edit/',HodViews.edit_Category,name="edit_Category"),

    path('Accounts/Admin/SubCategory/',HodViews.subcategory,name="subcategory"),
    path('Accounts/Admin/SubCategory/Edit',HodViews.edit_subcategory,name="edit_subcategory"),
    path('Accounts/Admin/SubCategory/Delete/<int:id>',HodViews.delete_subcategory,name="delete_subcategory"),
    path('get-subcategories/', HodViews.get_subcategories, name='get_subcategories'),
    path('get-products/', HodViews.get_products, name='get_products'),
    path('get-products/Price', HodViews.get_products_price, name='get_products_price'),


# ----------------------------------------- Technician ------------------------- 

    path('Accounts/Admin/Technician',HodViews.technician,name="technician"),
    path('Accounts/Admin/ADD/Technician',HodViews.add_technician,name="add_technician"),
    path('Accounts/Admin/Technician/AddCategory',HodViews.technician_add_category,name="technician_add_category"),
    path('Accounts/Admin/Technician/Profile/<int:id>',HodViews.technician_edit_profile,name="technician_edit_profile"),
    path('Accounts/Admin/Technician/Edit',HodViews.edit_technician,name="edit_technician"),
    path('Accounts/Technician/Delete/<int:id>',HodViews.delete_technician,name="delete_technician"),
    path('Accounts/Technician/History/<int:id>',HodViews.technician_history,name="technician_history"),
    path('Accounts/Technician/Payment/History/<int:id>',HodViews.technician_payment_history,name="technician_payment_history"),
    # path('Accounts/Technician/ADD/Payment/History',HodViews.technician_add_payment_history,name="technician_add_payment_history"),
    path('Accounts/Admin/Product',HodViews.product,name="product"),
    path('Accounts/Admin/Product/Update',HodViews.update_product,name="update_product"),
    path('Accounts/Admin/Product/Delete/<int:id>',HodViews.delete_product,name="delete_product"),


    ########################## Addons ##################################
    
    path('Accounts/Admin/Addons',HodViews.addons,name="addons"),
    path('Accounts/Admin/Addons/Edit/<int:id>',HodViews.edit_addons,name="edit_addons"),
    path('Accounts/Admin/Addons/Update',HodViews.update_addons,name="update_addons"),
    path('Accounts/Admin/Addons/Delete/<int:id>',HodViews.delete_addons,name="delete_addons"),
    path('Accounts/Admin/Addons/Details/',HodViews.addons_details,name="addons_details"),



    ########################## Support ##################################

    path('Accounts/Admin/Support',HodViews.support,name="admin_support"),
    path('Accounts/Admin/Add/Support',HodViews.add_support,name="add_support"),
    path('Accounts/Admin/Support/Profile/<int:id>',HodViews.support_profile,name="admin_support_profile"),
    path('Accounts/Admin/Support/Profile/Update/',HodViews.support_update_profile,name="admin_support_update_profile"),
    path('Accounts/Admin/Support/Delete/<int:id>/',HodViews.delete_support,name="delete_support"),
    path('Accounts/Admin/Support/History/<int:id>/',HodViews.support_history,name="support_history"),
    

    ########################## FAQS ##################################
    path('Accounts/Admin/FAQ', HodViews.add_faq, name='add_faq'),
    path('Accounts/Admin/FAQ/Update', HodViews.update_add_faq, name='update_add_faq'),
    path('Accounts/Admin/FAQ/Delete/<int:id>/', HodViews.delete_faq, name='delete_faq'),

    ########################## Booking List ##################################
     path('Accounts/Admin/BookingList', HodViews.booking_list, name='booking_list'),
     path('Accounts/Admin/Verify/Otp', HodViews.admin_verify_otp,name="admin_verify_otp"),
     path('Accounts/Admin/Booking', HodViews.admin_booking, name='admin_booking'),
     path('Accounts/Booking/List_of_expert/<int:id>', HodViews.admin_List_of_expert, name='admin_List_of_expert'),
    #  path('Accounts/Task/Assign', HodViews.ad_Task_assign, name='support_Task_assign'),
     path('Accounts/Admin/Reschudule', HodViews.admin_reschedule, name='admin_reschedule'),
     path('Accounts/Admin/get_available_slots', HodViews.get_available_slots, name='get_available_slots'),
     path('Accounts/Admin/cancel_booking/<int:booking_id>', HodViews.cancel_booking_byadmin, name='cancel_booking_byadmin'),
     path('Accounts/Admin/taskAssign/', HodViews.task_assign, name='task_assign'),
     path('Accounts/Admin/ListofTask/', HodViews.list_of_task, name='list_of_task'),
     path('Accounts/Admin/DeleteTask/<int:id>/', HodViews.delete_of_task, name='delete_of_task'),
     path('Accounts/Admin/Booking/Listofcancel', HodViews.Listofcancel, name='Listofcancel'),
     path('Accounts/Admin/Booking/Listofcancel/Expert', HodViews.Listofcancel_expert, name='Listofcancel_expert'),
     path('Accounts/Admin/Booking/Cancel/Expert/<int:id>/', HodViews.cancel_by_expert, name='cancel_by_expert'),



    # ---------------------------------- Reschedule and Reassign technician ---------------------------
    
    path('Accounts/Admin/Booking/Reschedule',HodViews.admin_reschedule,name="admin_reschedule"),
    path('Accounts/Admin/Task/Reschedule',HodViews.task_reschedule,name="task_reschedule"),
    path('Accounts/Admin/Reassign',HodViews.reassign,name="reassign"),

    ########################## Notification ##################################

    path('Accounts/Admin/Notification/NewExpert', HodViews.ListofNewExpert, name='ListofNewExpert'),
    
    ########################## Rebooking ##################################

    path('Accounts/Admin/Rebooking/', HodViews.Listofrebooking, name='Listofrebooking'),
    path('Accounts/Admin/Booking-Complete/', HodViews.admin_booking_complete, name='admin_booking_complete'),
    path('Accounts/Admin/Rebooking/<int:task_id>', HodViews.admin_rebooking, name='admin_rebooking'),
    path('Accounts/Admin/Rebooking/Update/', HodViews.admin_rebooking_update, name='admin_rebooking_update'),

    ########################## Contact Us ##################################
    path('Accounts/Admin/ContactUs/', HodViews.contactus, name='contact_us'),
    path('Accounts/Admin/Carrer/Update', HodViews.carrer_update_Save, name='carrer_update_Save'),
    path('Accounts/Admin/ApplicantCarrer/<int:id>', HodViews.applicant_carrer, name='applicant_carrer'),



    ########################## Page Legal ###################################
    path('Accounts/Page/Legal',HodViews.page_legal_list,name="page_legal_list"),
    path('Accounts/Add/Page/Legal/',HodViews.add_page_legal,name="add_page_legal"),
    path('Accounts/Edit/Page/Legal/<int:id>/',HodViews.edit_page_legal,name="edit_page_legal"),
    path('Accounts/Update/Page/Legal/Save/',HodViews.update_page_legal_save,name="update_page_legal_save"),
    path('Accounts/Edit/Page/Legal/Delete/<int:id>/',HodViews.delete_page_legal,name="delete_page_legal"),
    ########################## Job Enquiry ##################################
    path('Accounts/Admin/Job/Enquiry', HodViews.admin_job_enquiry, name='admin_job_enquiry'),

    ########################## Job Enquiry ##################################
    path('Accounts/Admin/Share/Percantage', HodViews.admin_share_percentage, name='admin_share_percentage'),
    path('Accounts/Admin/Share/Percantage/update', HodViews.admin_share_percentage_update, name='admin_share_percentage_update'),
    path('Accounts/Admin/Share/Percantage/Delete/<int:id>', HodViews.admin_share_percentage_delete, name='admin_share_percentage_delete'),
    path('Accounts/Admin/Share/List', HodViews.admin_share_list, name='admin_share_list'),


    ########################## Customer ##################################

    path('Accounts/Admin/Customer/List', HodViews.admin_customer_list, name='admin_customer_list'),
    path('Accounts/Admin/Customer/Edit/<int:id>', HodViews.admin_customer_edit, name='admin_customer_edit'),
    path('Accounts/Admin/Customer/History/<int:id>', HodViews.admin_customer_history, name='admin_customer_history'),

    ########################## Customer Payment Details ##################################
    path('Accounts/Admin/Customer/Payment/Details', HodViews.admin_customer_payment, name='admin_customer_payment'),
    



    # ------------------------------------- table amount total show dummy --------------- 
    # path('Accounts/Admin/Customer/Payment/Details', HodViews.admin_customer_payment, name='admin_customer_payment'),



    ########################## Withdraw Request ##################################
    path('Accounts/Admin/Withdraw/Request/', HodViews.admin_withdraw_request, name='admin_withdraw_request'),
    path('Accounts/Admin/Withdraw/Cancel/<str:withdraw_id>/', HodViews.expert_cancel_withraw_request, name='expert_cancel_withraw_request'),
    path('Accounts/Admin/Withdraw/Accept/<str:withdraw_id>/', HodViews.expert_accept_withraw_request, name='expert_accept_withraw_request'),

    ########################## Recharge ##################################
    path('Accounts/Admin/Recharge/', HodViews.recharge, name='recharge'),
    path('Accounts/Admin/Recharge/Technician/Wise/<int:id>/', HodViews.recharge_technicianwise, name='recharge_technicianwise'),
    
    ########################## Attendence #######################################

    path('Accounts/Admin/Support/Attendence/<int:id>', HodViews.attendence, name='attendence'),
    
    
    ########################## Coupon Code #######################################

    path('Accounts/Admin/Coupon/', HodViews.coupon, name='coupon'),
    path('Accounts/Admin/Coupon/Save', HodViews.coupon_save, name='coupon_save'),
    path("Accounts/Admin/Coupon/Update/<int:id>/", HodViews.coupon_update, name="coupon_update"),
    path("Accounts/Admin/Coupon/Delete/<int:id>/", HodViews.coupon_delete, name="coupon_delete"),
    


    ########################## Blog #######################################

    path('Accounts/Admin/Blog/Add', HodViews.add_blog, name='add_blog'),
    path('Accounts/Admin/Blog/Edit/<int:id>', HodViews.edit_blog, name='edit_blog'),
    path('Accounts/Admin/Blog/Update', HodViews.blog_update, name='blog_update'),
    path('Accounts/Admin/View/Blog/', HodViews.view_blog, name='view_blog'),
    path('Accounts/Admin/Delete/<int:id>/', HodViews.delete_blog, name='delete_blog'),


    ########################## Offers #######################################

     path('Accounts/Admin/View/Offers', HodViews.view_offers, name='view_offers'),
     path('Accounts/Admin/Add/Offers', HodViews.add_offers, name='add_offers'),
     path('Accounts/Admin/Edit/Offers/<int:id>', HodViews.edit_offers, name='edit_offers'),
     path('Accounts/Admin/Offers/Update', HodViews.offer_update, name='offer_update'),
     path('Accounts/Admin/Offers/Delete/<int:id>/', HodViews.delete_offer, name='delete_offer'),
    



    ########################## Most Viewed #######################################

    path('Accounts/Admin/MostViewed/List', HodViews.most_view_list, name='most_view_list'),
    path('Accounts/Admin/MostViewed/Add', HodViews.add_mostViewed, name='add_mostViewed'),
    path('Accounts/Admin/MostViewed/Edit/<int:id>', HodViews.edit_mostViewed, name='edit_mostViewed'),
    path('Accounts/Admin/MostViewed/Update/Save', HodViews.update_Save_mostViewed, name='update_Save_mostViewed'),


    # ------------------------------------- homepageserive --------------------

    path('Accounts/Admin/HomePageService/List', HodViews.homepageservice_view_list, name='homepageservice_view_list'),
    path('Accounts/Admin/HomePageService/Add', HodViews.add_homepage_service, name='add_homepage_service'),
    path('Accounts/Admin/HomePageService/Edit/<int:id>', HodViews.edit_homepage_service, name='edit_homepage_service'),
    path('Accounts/Admin/HomePageService/Update/Save', HodViews.update_Save_homepageservice, name='update_Save_homepageservice'),
    # ------------------------------------ Invoice ------------------------------ 
    path("testing",HodViews.testing,name="testing"),

    path('Accounts/Admin/Booking/Invoice/<int:booking_id>', HodViews.ViewPDF, name="admin_pdf_view"),
    path('Accounts/Admin/Booking/New/Invoice/<int:booking_id>', HodViews.invoice_download, name="new_invoice"),

    path('upload/', HodViews.upload_image, name='ckeditor_upload'),

    path('export-excel/', HodViews.export_to_excel, name='export_to_excel'),


    ########################## Pincode ##################################

    path('Accounts/Admin/Pincode',HodViews.pincode,name="pincode"),
    path('Accounts/Add/Pincode',HodViews.add_pincode,name="add_pincode"),
    path('Accounts/Edit/Pincode/<int:id>',HodViews.edit_pincode,name="edit_pincode"),
    path('Accounts/Delete/Pincode/<int:id>',HodViews.delete_pincode,name="delete_pincode"),


    
    ########################## Universal Slot ##################################

    path('Accounts/Admin/AddUniversalSlot',HodViews.add_universal_slot,name="add_universal_slot"),
    path('Accounts/Admin/UniversalSlot',HodViews.universal_slot,name="universal_slot"),
    path('Accounts/Admin/EditUniversalSlot/<int:id>/',HodViews.edit_universal_slot,name="edit_universal_slot"),
    path('Accounts/Admin/Delete/UniversalSlot/<int:id>/',HodViews.delete_universal_slot,name="delete_universal_slot"),
    path('toggle-auto-assign/', HodViews.toggle_auto_assign, name='toggle_auto_assign'),


    
    ##########################  Slot ##################################

    path('Accounts/Admin/Slot',HodViews.slot,name="slot"),
    path('Accounts/Admin/Add/Slot',HodViews.add_slot,name="add_slot"),
    path('get-pincodes/', HodViews.get_pincodes_by_state, name='get_pincodes_by_state'),
    path('Accounts/Admin/Edit/Slot/<int:id>', HodViews.edit_slot, name='edit_slot'),
    path('Accounts/Admin/Delete/Slot/<int:id>', HodViews.delete_slot, name='delete_slot'),
    path('Accounts/Admin/get_available_slots', HodViews.get_available_slots, name='get_available_slots'),

    path('Accounts/Admin/WorkingState/',HodViews.working_state,name="working_state"),
    path('WorkingState/Delete/<int:id>',HodViews.delete_working_state,name="delete_working_state"),
    path('WorkingState/Edit/',HodViews.edit_working_State,name="edit_working_State"),
    
    ##########################  upload csv file pincode ##################################

    
    path("upload-pincode-csv/", HodViews.upload_pincode_csv, name="upload_pincode_csv"),
    path("notification/", HodViews.test_notification_view, name="notification"),
    path("get-pincode-by-state/", HodViews.get_pincode_by_state, name="get_pincode_by_state"),
    path('ajax/check-slot-availability/', HodViews.ajax_check_slot_availability, name='ajax_check_slot_availability'),
    




    


    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





urlpatterns += staticfiles_urlpatterns()