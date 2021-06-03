from django.shortcuts import render
from .models import Item, OrderItem, Order, Category


def store(request):
    category = request.GET.get('category')
    if category == None:
        item = Item.objects.all()
    else:
        item = Item.objects.filter(category__name=category)

    category = Category.objects.all()

    context = {
        'category': category,
        'item': item
    }
    return render(request, 'store.html', context)
