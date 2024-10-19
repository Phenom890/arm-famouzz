import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from .forms import AddressForm, RefundForm, ContactForm
from .models import Product, OrderItem, Order, Address, Coupon, Refund, Contact


def sold_out_view(request):
    return HttpResponse(
        '<h1> <center> This item is Sold out.<br/> Please Check next time!!!<a href="/">Go '
        'Back</a> </center> </h1>')


def get_ref_code():
    return "".join(random.choices(
        string.ascii_letters +
        string.ascii_uppercase +
        string.ascii_lowercase,
        k=20
    ))


def is_valid_form(values: list[vars]):
    valid = True
    for field in values:
        if field == "":
            valid = False
    return valid


@login_required(login_url='login')
def plus_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    item = OrderItem.objects.filter(owner=request.user, item=product, ordered=False).first()
    item.quantity += 1
    item.save()
    return redirect('product_display', pk=product.id)


@login_required(login_url='login')
def minus_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    item = OrderItem.objects.filter(owner=request.user, item=product, ordered=False).first()
    if item.quantity > 1:
        item.quantity -= 1
    item.save()
    return redirect('product_display', pk=product.id)


@login_required(login_url='login')
def remove_from_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    cart_items = OrderItem.objects.filter(owner=request.user, item=product, ordered=False)
    if cart_items:
        cart_item = cart_items.first()
        cart_item.delete()
    else:
        messages.error(request, 'You Cannot delete this item')
    return redirect('product_display', pk=product.id)


def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(category__icontains=query) |
        Q(tag__icontains=query)
    )

    context = {
        'products': products,
    }

    return render(request, 'core/search.html', context)


class HomeView(ListView):
    model = Product
    context_object_name = "products"
    template_name = 'core/index.html'
    paginate_by = 4


class AboutView(View):
    def get(self, request):
        return render(request, 'core/about.html')


class ContactView(LoginRequiredMixin, View):
    def get(self, request, username):
        form = ContactForm()
        context = {
            'form': form,
        }
        return render(request, 'core/contact.html', context)

    def post(self, request, username):
        user_contact = get_object_or_404(User, username=username)
        form = ContactForm(request.POST or None)
        if form.is_valid():
            msg = form.cleaned_data.get('message')

            contact = Contact()
            contact.contactor = user_contact
            contact.email = user_contact.email
            contact.message = msg
            contact.sent = True
            contact.save()
            messages.success(request,
                             'Thank You for your feedback, we will get back to you soon!')
            return redirect('home')

        messages.error(request, 'Message not sent, please try again!')
        return redirect('contact')


class ProductView(LoginRequiredMixin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        cat = product.category  # get the category of the product
        tag = product.tag  # get the tag of the product
        category_products = Product.objects.filter(category=cat)
        tag_products = Product.objects.filter(tag=tag)
        in_cart = OrderItem.objects.filter(owner=request.user, item=product, ordered=False).exists()
        cart_item = OrderItem.objects.filter(owner=request.user, item=product,
                                             ordered=False).first()

        context = {
            'product': product,
            'category_products': category_products,
            'tag_products': tag_products,
            'in_cart': in_cart,
            'cart_item': cart_item,
            'cat': cat,
            'tag': tag,
        }
        return render(request, 'core/product_description.html', context)

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        cart_item, created = OrderItem.objects.get_or_create(owner=request.user, item=product,
                                                             ordered=False)

        #   create an order
        order, created = Order.objects.get_or_create(
            owner=request.user,
            ordered=False,
        )
        if not created:
            order.items.add(cart_item)
            order.save()

        if created:
            #   add the cart item to the order after it has been created
            order.items.add(cart_item)
            order.ref_code = get_ref_code()
            order.save()

        return redirect('product_display', pk=product.id)


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        order_qs = Order.objects.filter(owner=request.user, ordered=False)
        if order_qs:
            order = order_qs.first()
            cart_items = order.items.all()
        else:

            return HttpResponse(
                '<h1> <center>You have no active order. <br/> Add an item to your cart and check '
                'out later!!!</center> </h1>')

        context = {
            'cart_items': cart_items,
            'order': order,
        }
        if cart_items:  # if the cart is not empty
            return render(request, 'core/cart.html', context)
        else:
            return HttpResponse(
                '<h1> <center>Your cart is empty. <br/> Add items to your cart and check out '
                'later!!!</center> </h1>')


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        order = Order.objects.filter(owner=request.user, ordered=False).first()
        cart = order.items.all()
        default = Address.objects.filter(owner=request.user, default=True).first()

        form = AddressForm()

        context = {
            'cart': cart,
            'order': order,
            'form': form,
            'default': default,
        }
        return render(request, 'core/checkout.html', context)

    def post(self, request):
        order = Order.objects.filter(owner=request.user, ordered=False).first()
        save_default = request.POST.get('save_default', False)
        use_default = request.POST.get('use_default', False)
        default_address = Address.objects.filter(owner=request.user, default=True).first()

        form = AddressForm(request.POST or None)

        if use_default:
            new_address = Address()
            new_address.owner = default_address.owner
            new_address.email = default_address.email
            new_address.locality = default_address.locality
            new_address.street_name = default_address.street_name
            new_address.region = default_address.region
            new_address.house_number = default_address.house_number
            new_address.save()

            order.address = new_address
            order.save()


        else:
            locality = request.POST.get('locality')
            street_name = request.POST.get('street_name')
            region = request.POST.get('region')
            house_number = request.POST.get('house_number')

            if is_valid_form([locality, street_name, region, house_number]):

                address = form.save(commit=False)
                address.owner = request.user
                address.email = request.user.email
                if save_default:
                    address.default = True
                    address.save()
                else:
                    address.save()
                order.address = address
                order.save()
            else:
                messages.error(request, 'Fill in the form or use your default address !!!')
                return redirect('checkout')

        return redirect('payment')


class PaymentView(LoginRequiredMixin, View):
    def get(self, request):
        order = Order.objects.filter(owner=request.user, ordered=False).first()
        cart = order.items.all()

        context = {
            'order': order,
            'cart': cart,
        }
        return render(request, 'core/payment.html', context)

    def post(self, request):
        order = Order.objects.filter(owner=request.user, ordered=False).first()
        order_item_qs = order.items.filter(ordered=False)
        if order_item_qs.exists():
            order_item_qs.update(ordered=True)
            for item in order_item_qs:
                item.save()
            order.ordered = True
            order.save()
            messages.success(request, 'Your Order has been succeffully placed.Check your '
                                      'profile for the status!')
            return redirect('home')

        #   This will only execute if the cart is empty
        messages.error(request, 'You do not have anything in your cart!.Please buy something '
                                'before you can order!')
        return redirect('payment')


class AddCoupon(LoginRequiredMixin, View):
    def post(self, request):
        order = Order.objects.filter(owner=request.user, ordered=False).first()
        promo_code = request.POST.get('promo_code')
        promo_exists = Coupon.objects.filter(name=promo_code)
        if promo_exists:
            promo = promo_exists.first()
            order.coupon = promo
            order.save()
            messages.success(request, f'"{promo_code}" coupon successfully added to your order!')
            return redirect('checkout')
        messages.error(request, 'Invalid Coupon Code!')
        return redirect('checkout')


class RequestRefundView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        form = RefundForm()

        context = {
            'form': form,
            'order': order,
        }
        return render(request, 'core/refund.html', context)

    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        form = RefundForm(request.POST or None)
        if form.is_valid():
            msg = form.cleaned_data.get('reason')

            # create an instance of refund and populate it
            refund = Refund()
            refund.issuer = request.user
            refund.order_ref = order.ref_code
            refund.reason = msg
            refund.save()
            # update the refund_requested field on the order to True
            order.refund_requested = True
            order.save()
            messages.success(request, 'Refund requested successfully! We will get back to you '
                                      'shortly')
            return redirect('orders')

        messages.error(request, 'Refund request was not successful! Try again!!')
        return redirect('request_refund', pk=order.id)
