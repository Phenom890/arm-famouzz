from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from core.models import Address, Order
from .forms import (
    UserRegisterForm,
    UserForm,
    ProfileForm,
    AddressForm
)
from .models import Profile


class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        context = {
            'form': form,
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request):
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('login')


class UserLogout(View):
    def get(self, request):
        return render(request, 'accounts/logout.html')

    def post(self, request):
        return LogoutView.as_view(next_page='login')(request)


class UserProfileUpdateView(View):
    def get(self, request):
        profile = Profile.objects.filter(user=request.user).first()
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

        context = {
            'u_form': user_form,
            'p_form': profile_form,
        }
        return render(request, 'accounts/profile_update.html', context)

    def post(self, request):
        profile = Profile.objects.filter(user=request.user).first()
        user_form = UserForm(request.POST or None, instance=request.user)
        profile_form = ProfileForm(request.POST or None, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

        context = {
            'u_form': user_form,
            'p_form': profile_form,
        }
        messages.error(request, 'Check the form correctly and make the necessary corrections!')
        return render(request, 'accounts/profile_update.html', context)


class UserProfileView(View):
    def get(self, request):
        user_profile = Profile.objects.filter(user=request.user).first()

        context = {
            'profile': user_profile,
        }
        return render(request, 'accounts/profile.html', context)


class AddressView(View):
    def get(self, request):
        address = Address.objects.filter(owner=request.user)
        context = {
            'addresses': address,
        }
        return render(request, 'accounts/address.html', context)


class UpdateAddress(View):
    def get(self, request, pk):
        curr_address = get_object_or_404(Address, id=pk)
        form = AddressForm(instance=curr_address)

        context = {
            'form': form,
        }
        return render(request, 'accounts/update_address.html', context)

    def post(self, request, pk):
        curr_address = get_object_or_404(Address, id=pk)
        form = AddressForm(request.POST or None, instance=curr_address)

        if form.is_valid():
            updated_address = form.save(commit=False)
            updated_address.owner = request.user
            updated_address.email = request.user.email
            updated_address.save()
            return redirect('address')

        context = {
            'form': form,
        }
        return render(request, 'accounts/update_address.html', context)


class OrdersView(View):
    def get(self, request):
        all_orders = Order.objects.filter(owner=request.user)

        context = {
            'orders': all_orders,
        }
        return render(request, 'accounts/orders.html', context)


class OrderItemView(View):
    def get(self, request, pk):
        all_orders = Order.objects.filter(owner=request.user)
        curr_order = get_object_or_404(Order, id=pk)
        curr_order_item = curr_order.items.all()

        context = {
            'orders': all_orders,
            'curr_order': curr_order,
            'order_items': curr_order_item,
        }
        return render(request, 'accounts/orders.html', context)


def make_default(request, pk):
    user_addresses = Address.objects.filter(owner=request.user)
    curr_address = get_object_or_404(Address, id=pk)
    user_addresses.update(default=False)
    curr_address.default = True
    curr_address.save()
    return redirect('address')


def delete_address(request, pk):
    curr_address = get_object_or_404(Address, id=pk)
    curr_address.delete()
    return redirect('address')
