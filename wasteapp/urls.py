from django.urls import path
from . import views
urlpatterns = [

    path('',views.login,name="login"),
    path('login',views.login,name="login"),
    path('logout',views.logout,name="logout"),

    # admin ------------------------------------------------------------------------------------
    path('adminhome',views.admin_home,name="adminhome"),
    path('selectdistrict',views.select_district,name="selectdistrict"),
    path('selecttaluk/<str:id>',views.select_taluk,name="selecttaluk"),
    path('adddistrict', views.add_district, name="adddistrict"),
    path("addtaluk/<str:id>", views.add_taluk, name="addtaluk"),
    path('addpanchayat/<str:id>',views.add_panchayat,name='addpanchayat'),
    path('viewpanchayat',views.view_panchayat,name="viewpanchayat"),
    path('editpanchayat/<str:id>',views.edit_panchayat,name="editpanchayat"),
    path('deletepanchayat/<str:id>', views.delete_panchayat, name="deletepanchayat"),

    path("viewdistrict", views.view_district, name="viewdistrict"),

    path("addcategory", views.add_category, name="addcategory"),
    path('viewcategory',views.view_category,name="viewcategory"),
    path("editcategory/<str:id>", views.edit_category, name="editcategory"),
    path("deletecategory/<str:id>", views.delete_category, name="deletecategory"),
    path('selectcategory',views.select_category,name='selectcategory'),
    path('addrecyclecategory/<str:id>',views.add_recycle_category,name="addrecyclecategory"),
    path('viewrecyclecategory/<str:id>',views.view_recycle_category,name="viewrecyclecategory"),
    path('deleterecyclecategory/<str:id>',views.delete_recycle_category,name="deleterecyclecategory"),
    path('adminrecycleditem',views.admin_recycled_items,name='adminrecycleditem'),

    # user---------------------------------------------------------------------------------------
    path('userhome',views.user_home,name="userhome"),
    path('uselectdistrict', views.user_select_district, name='uselectdistrict'),
    path('uselecttaluk/<str:id>', views.user_select_taluk, name='uselecttaluk'),
    path('uselectpanchayat/<str:id>',views.user_select_panchayat,name="uselectpanchayat"),
    path('userregister/<str:id>',views.user_register,name="userregister"),
    path("uviewcategory",views.user_view_category,name="uviewcategory"),
    path('addbooking/<str:id>',views.add_booking,name="addbooking"),
    path('bookwaste',views.book_waste,name="bookwaste"),
    path('bookingsuccess',views.booking_success_page,name="bookingsuccess"),
    path('panchayatapproved',views.view_panchayat_approved,name="panchayatapproved"),
    path('makepayment/<str:id>',views.make_payment,name="makepayment"),
    path('paymentsuccess',views.payment_success_page,name="paymentsuccess"),
    path('pendingbooking',views.pending_booking,name="pendingbooking"),
    path('deletependingbooking/<str:id>',views.delete_pending_booking,name="deletependingbooking"),
    path('bookeditems',views.booked_items,name="bookeditems"),
    path('addcomplaint',views.add_complaint,name="addcomplaint"),
    path('complaintreply',views.view_complaint_reply,name="complaintreply"),

    # panchayat----------------------------------------------------------------------------------
    path('panchayathome',views.panchayat_home,name="panchayathome"),
    path('viewbookingrequest',views.view_booking_request,name="viewbookingrequest"),
    path('approvebooking/<str:id>',views.approve_booking,name="approvebooking"),
    path("deletebooking/<str:id>",views.delete_booking,name="deletebooking"),
    path('bookeduser',views.booked_user,name="bookeduser"),
    path('viewcomplaint',views.view_complaint,name="viewcomplaint"),
    path('sendreply/<str:id>',views.send_reply,name="sendreply"),
    path('recyleCategory/<str:id>/<str:idw>',views.recyle_Category,name="recyleCategory"),
    path('thankspage',views.thanks_page,name="thankspage"),
    path('recycleditems',views.recycled_items,name="recycleditems"),
    path('addworker',views.add_worker,name="addworker"),
    path('viewworkers',views.view_workers,name="viewworkers"),
    path('deleteworker/<str:id>',views.delete_worker,name="deleteworker"),
    path('viewworkers1',views.view_workers1,name="viewworkers1"),
    path('salaryamount/<str:id>',views.salary_amount,name="salaryamount"),
    path('addworkerpayment',views.add_worker_payment,name="addworkerpayment"),
    path('viewworkerlist',views.view_worker_list,name="viewworkerlist"),
    path('viewworkerleave/<str:id>',views.view_worker_leave,name="viewworkerleave"),

    # worker----------------------------------------------------------------------------------
    path('workerhome',views.worker_home,name='workerhome'),
    path('viewwork',views.view_work,name="viewwork"),
    path('applyleave',views.apply_leave,name="applyleave"),





]
