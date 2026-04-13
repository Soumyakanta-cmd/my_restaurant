from django.db import models

# Create your models here.
class ItemList(models.Model):
    Category_name= models.CharField( max_length=20)

    def __str__(self):
        return self.Category_name

class Items(models.Model):
    Item_name = models.CharField(max_length=50)
    description=models.TextField(blank=False)
    price=models.IntegerField()
    Category=models.ForeignKey(ItemList,related_name='Name',on_delete=models.CASCADE)
    Image=models.ImageField(upload_to='items/', null=True, blank=True)

    def __str__(self):
        return self.Item_name

class AboutUs(models.Model):
    Description=models.TextField(blank=False)

    def __str__(self):
        return self.Description

class FeedBack(models.Model):
    User_name=models.CharField(max_length=20)
    Description=models.TextField(blank=False)
    Ratings=models.IntegerField()
    Image=models.ImageField(upload_to='items/',blank=True)

    def __str__(self):
        return self.User_name
    


class BookTable(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    )
    Name=models.CharField(max_length=100)
    Phone_number=models.IntegerField()
    Email=models.EmailField()
    Total_person=models.IntegerField()
    booking_date=models.DateField()
    items=models.ManyToManyField(Items, through='BookingItem')
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status    = models.CharField(max_length=20, default='Unpaid')
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return self.Name
    
class BookingItem(models.Model):
    booking  = models.ForeignKey(BookTable, on_delete=models.CASCADE, related_name='booking_items')
    item     = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.booking.Name} - {self.item.Item_name} x{self.quantity}"
    

from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='default.png')

    def __str__(self):
        return self.user.username
    
class Offer(models.Model):
    Item_name = models.ForeignKey(Items,related_name='Name',on_delete=models.CASCADE)
    discount=models.IntegerField()
    Image=models.ImageField(upload_to='items/', null=True, blank=True)

    def __str__(self):
        return self.Item_name

