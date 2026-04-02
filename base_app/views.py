from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from base_app.models import ItemList, Items, AboutUs, FeedBack, BookTable,Offer

def HomeView(request):
    items = Items.objects.all()
    list = ItemList.objects.all()
    review = FeedBack.objects.all()
    return render(request,'home.html',{'items': items, 'list': list, 'review': review})

def AboutView(request):
    data = AboutUs.objects.all()
    return render(request,'about.html',{'data': data})

def MenuView(request):
    items = Items.objects.all()
    list = ItemList.objects.all()
    return render(request,'menu.html',{'items': items, 'list': list})

def OfferView(request):
    offer=Offer.objects.all()
    return render(request,'offer.html',{'offer':offer})

from django.contrib import messages
def BookTableView(request):
    items = Items.objects.all()
    if request.method=='POST':
        name = request.POST.get('user_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('user_email')
        total_person = request.POST.get('total_person')
        booking_date = request.POST.get('booking_date')
        book_items = request.POST.get('items')

        if name != '' and len(phone_number) == 10 and email != '' and total_person != 0 and booking_date != '':
            data = BookTable(Name=name, Phone_number=phone_number,
                             Email=email,Total_person=total_person,
                             booking_date=booking_date)
            
            data.save()
            data.items.set([book_items])
            
            
            messages.success(request ,"✅ Your request is approved and wait for confirmation ")
        else:
            messages.error(request,"❌ Please enter valid details!")
        return redirect('Book_Table')
        
    return render(request, 'book_table.html',{'items':items})

def feedback(request):
    if request.method == 'POST':
        user_name = request.POST.get('User_name')
        description = request.POST.get('Description')
        rating = request.POST.get('Ratings')
        image = request.FILES.get('Image')

        FeedBack.objects.create(
            User_name=user_name,
            Description=description,
            Ratings=rating,
            Image=image
        )

        messages.success(request, "Thank you for your feedback 😊")
        return redirect('feedback')
    return render(request, 'feedback.html')

import random
from django.core.mail import send_mail
from django.contrib.auth.models import User
def generate_otp():
    return str(random.randint(100000,999999))

#admin panel starts here
from django.contrib.auth import authenticate,login,logout
def AdminLoginView(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            otp=generate_otp()
            request.session['otp']=otp
            request.session['temp_user']=user.id

            send_mail(
                'your otp code',
                f'your OTP is {otp}',
                'patisoumyakanta3210@gmail.com',
                [user.email],
                fail_silently=False,
            )

            return redirect('verify_otp')
        else:
            messages.error(request,'Invalid user name and password')
            return redirect('admin_login')
        
    return render(request, 'login.html')

def verifyotp(request):
    if request.method =='POST':
        entered_otp = request.POST['otp']
        saved_otp=request.session.get('otp')
        if entered_otp == saved_otp:
            user_id=request.session.get('temp_user')
            user=User.objects.get(id=user_id)

            login(request,user)

            request.session.pop('otp',None)
            request.session.pop('temp_user',None)

            return redirect('dashboard')
        else:
            messages.error(request,'Invalid otp')
            return redirect('verify_otp')
        
    return render(request,'verifyotp.html')

from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required(login_url='admin_login')
def dashboard(request):
    pending_count   = BookTable.objects.filter(status='Pending').count()
    total_bookings  = BookTable.objects.count()
    total_items     = Items.objects.count()
    total_feedback  = FeedBack.objects.count()
    recent_bookings = BookTable.objects.order_by('-id')[:5]
 
    return render(request, 'dashboard.html', {
        'pending_count':   pending_count,
        'total_bookings':  total_bookings,
        'total_items':     total_items,
        'total_feedback':  total_feedback,
        'recent_bookings': recent_bookings,
    })

def AdminLogoutView(request):
    logout(request)
    return redirect('admin_login')

from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
@staff_member_required(login_url='admin_login')
def update_booking(request, id):
    booking = get_object_or_404(BookTable, id=id)
    if request.method == "POST":
        status = request.POST.get('status')


        return render(request, 'confirm.html', {
            'booking': booking,
            'status': status  
        })

    return redirect('booking')

@staff_member_required(login_url='admin_login')
def confirm_update(request, id):
    booking = get_object_or_404(BookTable, id=id)

    if request.method == "POST":
        status = request.POST.get('status')

        if status:
            if status == "Confirmed":
                html_content = f"""
                            <html>
                            <body style="font-family: Arial, sans-serif; background-color:#f4f4f4; padding:20px;">
                                
                                <div style="max-width:600px; margin:auto; background:white; padding:20px; border-radius:10px;">
                                    
                                    <h2 style="color:#28a745; text-align:center;">Booking Confirmed ✅</h2>
                                    
                                    <p>Hello <b>{booking.Name}</b>,</p>
                                    
                                    <p>
                                        Your booking has been <b style="color:green;">confirmed</b>.
                                        Please wait until our waiter comes and assists you.
                                    </p>
                                    
                                    <p>We hope you have a wonderful time at our restaurant 🍽️</p>

                                    <hr>

                                    <h4>📞 Contact Us</h4>
                                    <p>
                                        Phone: +91 9437742861<br>
                                        Email: support@padmini.com
                                    </p>

                                    <h4>🌐 Follow Us</h4>
                                    <p>
                                        <a href="https://facebook.com">
                                            <img src="https://cdn-icons-png.flaticon.com/24/733/733547.png">
                                        </a>
                                        <a href="https://instagram.com">
                                            <img src="https://cdn-icons-png.flaticon.com/24/733/733558.png">
                                        </a>
                                        <a href="https://twitter.com">
                                            <img src="https://cdn-icons-png.flaticon.com/24/733/733579.png">
                                        </a>
                                    </p>

                                    <hr>

                                    <p style="text-align:center; color:gray;">
                                        Thank you for choosing <b>padmini Restaurant</b> ❤️
                                    </p>

                                </div>

                            </body>
                            </html>
                            """
                email = EmailMultiAlternatives(
                    subject="Booking Confirmed ✅",
                    body="Your booking has been confirmed",
                    from_email=settings.EMAIL_HOST_USER,
                    to=[booking.Email],
                   
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

                booking.status = status
                booking.save()

    return redirect('booking')
    

@staff_member_required(login_url='admin_login')
def allbooking(request):
    status = request.GET.get('status')
    if status:
        booking = BookTable.objects.filter(status=status)
    else:
        booking=BookTable.objects.all()
    return render(request,'booking.html',{'booking':booking})

@staff_member_required(login_url='admin_login')
def itemcategory(request):
    itemlist=ItemList.objects.all()
    return render(request,'itemcategory.html',{'itemlist':itemlist})

from .forms import*
@staff_member_required(login_url='admin_login')
def additemcategory(request):
    form=ItemListForm()
    if request.method == 'POST':
        form=ItemListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('itemcategory')
    return render(request,'additemcategory.html',{'form':form})

@staff_member_required(login_url='admin_login')
def deleteitemcategory(request, id):
    item = get_object_or_404(ItemList, id=id)

    if request.method == "POST":
        item.delete()
        return redirect('itemcategory')

    return render(request, 'deleteitemcategory.html', {'item': item})

@staff_member_required(login_url='admin_login')
def adminprofile(request):
    return render(request, 'adminprofile.html')

from .models import Profile
@staff_member_required(login_url='admin_login')
def editadminprofile(request):
    if request.method == 'POST':
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)

        
        username = request.POST.get('username')
        email = request.POST.get('email')
        image = request.FILES.get('image')
        password = request.POST.get('password')

        
        user.username = username
        user.email = email

        if password and password.strip():
            user.set_password = password
        user.save()
        
        if image:
            profile.image = image
            profile.save()

        return redirect('admin_login')

    return render(request, 'editadminprofile.html')

@staff_member_required(login_url='admin_login')
def allitems(request):
    items=Items.objects.all()
    return render(request,'allitems.html',{'items':items})

@staff_member_required(login_url='admin_login')
def additem(request):
    form=AddItemForm()
    if request.method == 'POST':
        form=AddItemForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('allitems')
    return render(request,'additem.html',{'form':form})

@staff_member_required(login_url='admin_login')
def deleteitem(request,id):
    item = get_object_or_404(Items, id=id)
    if request.method == "POST":
        item.delete()
        return redirect('allitems')

    return render(request, 'deleteitem.html', {'item': item})
@staff_member_required(login_url='admin_login')
def updateitem(request,id):
    item=Items.objects.get(id=id)
    form=AddItemForm(instance=item)
    if request.method=='POST':
        form=AddItemForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            return redirect('allitems')
    return render(request,'updateitem.html',{'form':form})

@staff_member_required(login_url='admin_login')
def feedbackview(request):
    feedback=FeedBack.objects.all()
    return render(request,'feedbackview.html',{'feedback':feedback})

@staff_member_required(login_url='admin_login')
def deletefeedback(request,id):
    feedback=FeedBack.objects.get(id=id)
    if request.method=='POST':
        feedback.delete()
        return redirect('feedbackview')
    return render(request,'deletefeedback.html',{'feedback':feedback})

@staff_member_required(login_url='admin_login')
def aboutus(request):
    about=AboutUs.objects.all()
    return render(request,'aboutus.html',{'about':about})

@staff_member_required(login_url='admin_login')
def editaboutus(request,id):
    about=AboutUs.objects.get(id=id)
    form=EditAbout(instance=about)
    if request.method=='POST':
        form=EditAbout(request.POST,instance=about)
        if form.is_valid():
            form.save()
            return redirect('aboutus')
    return render(request,'editaboutus.html',{'form':form})

@staff_member_required(login_url='admin_login')
def addaboutus(request):
    form=EditAbout()
    if request.method == 'POST':
        form=EditAbout(request.POST)
        if form.is_valid():
            form.save()
            return redirect('aboutus')
    return render(request,'editaboutus.html',{'form':form})

@staff_member_required(login_url='admin_login')
def offerus(request):
    offer=Offer.objects.all()
    return render(request,'offerus.html',{'offer':offer})

@staff_member_required(login_url='admin_login')
def addoffer(request):
    items = Items.objects.all()

    if request.method == "POST":
        item_id = request.POST.get('item')
        discount = request.POST.get('discount')
        image = request.FILES.get('image')

        item = Items.objects.get(id=item_id)

        Offer.objects.create(
            Item_name=item,
            discount=discount,
            Image=image
        )

        return redirect('offerus')

    return render(request, 'addoffer.html', {'items': items})
@staff_member_required(login_url='admin_login')
def deleteoffer(request,id):
    offer=Offer.objects.get(id=id)
    if request.method == 'POST':
        offer.delete()
        return redirect('offerus')
    return render(request,'deleteoffer.html',{'offer':offer})


