from django import template

from core.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        orders = Order.objects.filter(owner=user, ordered=False)
        if orders.exists():
            order = orders.first()
            return order.items.count()
    return 0
