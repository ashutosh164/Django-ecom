from django.shortcuts import render, redirect
from .models import Item, OrderItem, Order, Category
from .forms import UserRegistrationsForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate


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


def item_detail(request, pk):
    item = Item.objects.get(id=pk)

    context = {
        'item': item
    }

    return render(request, 'details.html', context)


def signup(request):
    form = UserRegistrationsForm()
    if request.method == 'POST':
        form = UserRegistrationsForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'account was created for ' + username)

    context = {'form': form}
    return render(request, 'register.html', context)







