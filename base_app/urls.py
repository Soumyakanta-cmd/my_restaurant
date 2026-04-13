from base_app import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static  
from base_app.views import *


urlpatterns=[

    path('',HomeView,name="Home"),
    path('book_table',BookTableView,name="Book_Table"),
    path('menu',MenuView,name="Menu"),
    path('offer',OfferView,name="offer"),
    path('about',AboutView,name="About"),
    path('feedback',feedback,name="feedback"),
    path('admin/',AdminLoginView, name='admin_login'),
    path('verifyotp/',verifyotp, name='verify_otp'),
    path('dashboard/', dashboard, name='dashboard'),
    path('admin-logout/', AdminLogoutView, name='admin_logout'),
    path('confirm-update/<int:id>/', confirm_update, name='confirm-update'),
    path('update/<int:id>/', update_booking, name='update_booking'),
    path('booking/', allbooking, name='booking'),
    path('itemcategory/', itemcategory, name='itemcategory'),
    path('itemcategory/add/',additemcategory, name='add-itemcategory'),
    path('itemcategory/delete/<int:id>/', deleteitemcategory, name='delete-itemcategory'),
    path('admin-profile/', adminprofile, name='admin-profile'),
    path('edit-profile/', editadminprofile, name='edit-profile'),
    path('allitems/', allitems, name='allitems'),
    path('additem/', additem, name='additem'),
    path('deleteitem/<int:id>/', deleteitem, name='deleteitem'),
    path('updateitem/<int:id>/', updateitem, name='updateitem'),
    path('feedbackview/', feedbackview, name='feedbackview'),
    path('feedbackdelete/<int:id>/', deletefeedback, name='feedbackdelete'),
    path('aboutus/', aboutus, name='aboutus'),
    path('editaboutus/<int:id>', editaboutus, name='editabout'),
    path('addaboutus/', addaboutus, name='addabout'),
    path('offerus/', offerus, name='offerus'),
    path('addoffer/', addoffer, name='addoffer'),
    path('deleteoffer/<int:id>', deleteoffer, name='deleteoffer'),
    path('pay/<int:booking_id>/', pay_booking, name='pay_booking'),
    path('payment-success/', payment_success, name='payment_success'),
    path('bill/<int:booking_id>/', download_bill, name='download_bill'),

]   
if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

