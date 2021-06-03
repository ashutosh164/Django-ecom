from django.db import models
from PIL import Image
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(upload_to='items/', null=True)
    description = models.CharField(max_length=200, default='', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

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


# ORDER ITEM AFTER ADD IN CART
class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


# USE ORDER EVERY TIME USER ADD ITEM TO THE CART BUT NOT ORDERED
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(OrderItem)
    created_on = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user


