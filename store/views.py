from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, OrderItem, Order, Category
from .forms import UserRegistrationsForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone


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


def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request, 'Username Or Password is incorrect')
    return render(request, 'login.html')


def signup(request):
    form = UserRegistrationsForm()
    if request.method == 'POST':
        form = UserRegistrationsForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'account was created for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)


def userlogout(request):
    logout(request)
    return redirect('login')


def add_to_cart(request, pk):
    item = get_object_or_404(Item, id=pk)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.item.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.item.add(order_item)
    else:
        # order_date =timezone.now()
        order = Order.objects.create(user=request.user)
        order.item.add(order_item)
    return redirect('store')


def remove_cart(request, pk):
    item = get_object_or_404(Item, id=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.item.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.item.remove(order_item)
        else:
            return redirect('store')
    else:
        return redirect('store')

    return redirect('store')


# def remove_cart(request, pk):
#     item = get_object_or_404(Item, id=pk)
#     order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.item.filter(item__id=item.id).exists():
#             order_item.quantity -= 1
#             order_item.save()
#             if order_item.quantity == 0:
#                 order_item.delete()
#
#         else:
#             order.item.remove(order_item)
#     else:
#         # order_date =timezone.now()
#         order = Order.objects.create(user=request.user)
#         order.item.add(order_item)
#     return redirect('store')
