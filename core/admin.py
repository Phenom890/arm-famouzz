from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext

from .models import Product, Order, OrderItem, Address, Coupon, Refund, Contact


class OrderItemPanel(admin.ModelAdmin):
    list_display = ['owner', 'item', 'quantity', 'ordered']


class ContactPanel(admin.ModelAdmin):
    list_display = ['contactor', 'email', 'date_sent', 'seen']

    @admin.action(description="Mark as seen")
    def make_seen_true(self, request, queryset):
        queryset.update(seen=True)
        self.message_user(request, ngettext(
            '%d contact was successfully marked as seen.',
            '%d contacts were successfully marked as seen',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    actions = [make_seen_true]


class OrderPanel(admin.ModelAdmin):
    list_display = ['owner', 'ref_code', 'address', 'refund_requested', 'refund_granted', 'ordered']
    search_fields = ['ref_code', 'owner__username']

    @admin.action(description='Mark selected orders as refund granted')
    def make_refund_granted(self, request, queryset):
        queryset.update(refund_granted=True)
        self.message_user(request, ngettext(
            '%d order was successfully marked as refund granted.',
            '%d orders were successfully marked as refund granted.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    @admin.action(description='Mark selected orders as refund not granted')
    def make_refund_not_granted(self, request, queryset):
        queryset.update(refund_granted=False)
        self.message_user(request, ngettext(
            '%d order was successfully marked as refund not granted.',
            '%d orders were successfully marked as refund not granted.',
            queryset.count(),
        ) % queryset.count(), messages.SUCCESS)

    actions = [make_refund_granted, make_refund_not_granted]


class CouponPanel(admin.ModelAdmin):
    list_display = ['name', 'coupon_percentage']


class RefundPanel(admin.ModelAdmin):
    list_display = ['issuer', 'order_ref', 'reason', 'created']


class AddressPanel(admin.ModelAdmin):
    list_display = ['owner', 'locality', 'street_name', 'created', 'default']


admin.site.register(Product)
admin.site.register(Contact, ContactPanel)
admin.site.register(Refund, RefundPanel)
admin.site.register(Address, AddressPanel)
admin.site.register(OrderItem, OrderItemPanel)
admin.site.register(Order, OrderPanel)
admin.site.register(Coupon, CouponPanel)

admin.site.site_header = 'Armfamouzz'
admin.site.site_title = 'Armfamouzz'
admin.site.site_index_title = 'Welcome To Armfamouzz'
