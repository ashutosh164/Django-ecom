from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Size(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, unique=True)

    def __str__(self):
        return self.get_size_display()


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='items/', null=True)
    description = models.CharField(max_length=200, default='', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    sizes = models.ManyToManyField(Size, related_name='items')

    def __str__(self):
        return self.title

    # RESIZE THE IMAGE
    def save(self,*args,**kwargs):
        super(Item, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    # def get_absolutely_url(self):
    #     return reverse('detail', kwargs={'id': self.id})


# ORDER ITEM AFTER ADD IN CART
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total(self):
        return self.quantity * self.item.price

    def get_total_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_save(self):
        return self.get_total() - self.get_total_discount_price()

    # def get_final_price(self):
    #     if self.item.discount_price:
    #         return self.get_total_discount_price()
    #     else:
    #         return self.get_total()

    def get_final_price(self):
        price = self.quantity * self.item.price
        if self.item.discount_price:
            return price - self.item.discount_price
        else:
            price

    def total_item_price_after_discount(self):
        price = self.item.price * self.quantity
        total_discount = price - self.item.discount_price
        return total_discount


# USE ORDER EVERY TIME USER ADD ITEM TO THE CART BUT NOT ORDERED
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(OrderItem)
    created_on = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    # billing_address = models.ForeignKey('ShippingAddress', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.user} -- {self.item}"

    def get_total(self):
        total = 0
        for order_item in self.item.all():
            total += order_item.get_final_price()
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True, null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    dist = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    country = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=15,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}--{self.address}'

