from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
# Create your models here.
class FoodType(models.Model):
    name=models.CharField(max_length=200)
    image=models.ImageField( upload_to="Images")

    def __str__(self) -> str:
        return f"{self.name}"
class FoodItem(models.Model):
    name=models.CharField(max_length=200)
    image=models.ImageField( upload_to="Foods")
    price=models.IntegerField()
    available=models.BooleanField(default=True)
    category=models.ForeignKey(to=FoodType,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} {self.price}"
class orderDetail(models.Model):
    fooditem=models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    total_price=models.IntegerField(default=0)

    def save(self,*args, **kwargs) :
        self.total_price=int(self.quantity)*int(self.fooditem.price)
        print(self.total_price)
        super(orderDetail, self).save(*args, **kwargs)
    def __str__(self) -> str:
        return f"{self.quantity} {self.fooditem.name}"
class GrandOrder(models.Model):
    orders = models.ManyToManyField(orderDetail,blank=True)
    grand_total = models.IntegerField(default=0)
    table_number = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField( default=timezone.now)

