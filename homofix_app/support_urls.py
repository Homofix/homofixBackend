
from django.urls import path
from homofix_app import views,SupportViews, HodViews


urlpatterns = [
    path('', SupportViews.dashboard,name="support_dashboard"),
    path('Support/Profile', SupportViews.support_profile,name="support_profile"),
    path('Support/Update/Profile', SupportViews.support_profile_update,name="support_profile_update"),
    path('Support/Orders/', SupportViews.support_orders,name="support_orders"),
    path('Support/Orders/Otp', SupportViews.support_otp,name="support_otp"),
    path('Support/Orders/Verify/Otp', SupportViews.support_verify_otp,name="support_verify_otp"),
    path('support_booking/', SupportViews.support_booking, name='support_booking'),
    path('reschedule_booking/', SupportViews.reschedule_booking, name='reschedule_booking'),
    path('cancel_booking/<int:booking_id>', SupportViews.cancel_booking, name='cancel_booking'),
    path('Support/Task/Assign', SupportViews.support_Task_assign, name='support_Task_assign'),
    path('Support/Booking/List_of_expert/<int:id>', SupportViews.support_List_of_expert, name='support_List_of_expert'),
    path('Support/List/Task', SupportViews.support_list_of_task, name='support_list_of_task'),
    path(
        "Support/DeleteTask/<int:id>/",
        SupportViews.delete_of_task,
        name="support_delete_of_task",
    ),
    path('Support/Order/Cancel', SupportViews.order_cancel, name='order_cancel'),
    path('Support/Expert/Order/Cancel', SupportViews.support_expert_order_cancel, name='support_expert_order_cancel'),
    path('Support/Task/Counting/<int:expert_id>/', SupportViews.support_task_counting, name='support_task_counting'),
    path('Support/Booking/Complete/', SupportViews.support_booking_complete, name='support_booking_complete'),
    path('Support/Booking/Rebooking/<int:task_id>', SupportViews.support_rebooking, name='support_rebooking'),
    path('Support/Booking/Rebooking/Details', SupportViews.support_rebooking_list, name='support_rebooking_list'),
    path('Support/Booking/Rebooking/Update/', SupportViews.support_rebooking_update, name='support_rebooking_update'),
    path('Support/Booking/Rebooking/get-subcategories/', SupportViews.support_get_subcategories, name='support_get_subcategories'),
    path('Support/Booking/Rebooking/get-products/', SupportViews.support_get_products, name='support_get_products'),
    path('Support/get_available_slots', SupportViews.get_available_slots, name='support_get_available_slots'),
    path('Support/Expert/get_pincodes', SupportViews.support_get_pincodes, name='support_get_pincodes'),
    path('Support/Task/Reschedule',SupportViews.support_task_reschedule,name="support_task_reschedule"),
    path('Support/Reassign',SupportViews.support_reassign,name="support_reassign"),
#    ------------------------------ EXPERT --------------------- 
    path('Support/Expert/Add', SupportViews.support_expert_add, name='support_expert_add'),
    path('Support/Expert/list_of_expert', SupportViews.support_list_of_expert, name='support_list_of_expert'),
    path('Support/Booking/Cancel/Expert/<int:id>/', SupportViews.cancel_by_expert_support, name='cancel_by_expert_support'),
    path('Support/Expert/add_expert', SupportViews.support_add_expert, name='support_add_expert'),
    path('Support/Expert/Edit/Profile/<int:id>',SupportViews.expert_edit_profile,name="expert_edit_profile"),
    path('Support/Expert/payment_history/<int:id>', SupportViews.support_expert_payment_history, name='support_expert_payment_history'),
    path('Support/Technician/History/<int:id>',SupportViews.technician_history,name="support_technician_history"),

#    ------------------------------ Rebooking Product --------------------- 

    # path('Support/Expert/Rebooking/Product/<int:id>', SupportViews.support_rebooking_product, name='support_rebooking_product'),
    path('Support/Expert/Rebooking/Product/<int:task_id>', SupportViews.support_rebooking_product, name='support_rebooking_product'),




#    ------------------------------ testing for request session --------------------- 

    path('myView/', SupportViews.myView, name='myView'),
    path('another_view/', SupportViews.another_view, name='another_view'),

# --------------------------- Invoice --------------------- 

    path('Invoice/<int:booking_id>', SupportViews.invoice, name='invoice'),

# --------------------------- Contact Us --------------------- 
    path('Support/ContactUs/', SupportViews.support_contact_us, name='support_contact_us'),


# --------------------------- Job Enquiry ---------------------     

    path('Support/Job/Enquiry', SupportViews.support_job_enquiry, name='support_job_enquiry'),
    path('Support/Invoice/<int:id>', SupportViews.index, name='index'),
    path('pdf_view/<int:booking_id>', SupportViews.ViewPDF, name="pdf_view"),
    # path('pdf_view/<int:booking_id>', SupportViews.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/', SupportViews.DownloadPDF.as_view(), name="pdf_download"),
    path('show/Product', SupportViews.showproduct, name="showproduct"),
    path('createPdf',SupportViews.pdf_report_create,name="pdf_report_create")



]
