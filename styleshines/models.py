from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator

from datetime import date

# Create your models here.

#----------------------User Model for authentication---------------------

class User(AbstractUser):
    phone=models.CharField(max_length=200,unique=True)
    address=models.CharField(max_length=200)

class Category(models.Model):
    category=models.CharField(max_length=200,unique=True)
    is_active=models.BooleanField(default=True)

# ----------------------Category Model----------------------------------

    def __str__(self):
        return self.category
    
# ----------------------jewellery Model----------------------------------------

class Jewellery(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    options=(
        ('gold','gold'),
        ('rose gold ','rose gold'),
        ('white gold','white gold'),
        ('silver','silver'),
        ('oxidized silver','oxidized silver'),
        ('german silver','german silver'),
        ('pearl','pearl')
    )
    type=models.CharField(max_length=200,choices=options,default="gold")
    image=models.ImageField(upload_to='images')

    @property
    def varients(self):
        qs=self.jewelleryvarients_set.all()
        return qs
    @property
    def reviews(self):
        qs=self.review_set.all()
        return qs
    
    @property
    def avg_rating(self):
        ratings=self.review_set.all().values_list("rating",flat=True)
        return sum(ratings)/len(ratings) if ratings else 0


    def __str__(self):
        return self.name
    
# ----------------------jewellery Varient Model--------------------------------

class JewelleryVarients(models.Model):
    jewel=models.ForeignKey(Jewellery,on_delete=models.CASCADE)
    price=models.PositiveIntegerField()
    description=models.CharField(max_length=200)

    @property
    def offers(self):
        current_date=date.today()
        qs=self.offers_set.all()
        qs=qs.filter(end_date__gte=current_date)
        return qs
    

    def __str__(self):
        return self.jewel.name
    
# ----------------------Offer Model---------------------------------------

class Offers(models.Model):
    jewel_varient=models.ForeignKey(JewelleryVarients,on_delete=models.CASCADE)
    discount_price=models.PositiveIntegerField()
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()


# ----------------------Cart Model----------------------------------------

class Cart(models.Model):
    jewel_varient=models.ForeignKey(JewelleryVarients,on_delete=models.DO_NOTHING)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    options=(
        ('in-cart','in-cart'),
        ('order-placed','order-placed'),
        ('cancelled','cancelled')
    )
    status=models.CharField(max_length=200,choices=options,default='in-cart')
    date=models.DateTimeField(auto_now_add=True)


# ----------------------Order Model---------------------------------------

class Orders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    jewel_varient=models.ForeignKey(JewelleryVarients,on_delete=models.CASCADE)
    options=(
        ('order-placed','order-placed'),
        ('cancelled','cancelled'),
        ('packed','packed'),
        ('in-transit','in-transit'),
        ('delivered','delivered')
    )
    status=models.CharField(max_length=200,choices=options,default='order-placed')
    ordered_date=models.DateTimeField(auto_now_add=True)
    expected_date=models.DateField(null=True)
    address=models.CharField(max_length=200)


# -----------------------Review Model-------------------------------------

class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    jewel=models.ForeignKey(Jewellery,null=True,on_delete=models.SET_NULL)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.CharField(max_length=200)
    
