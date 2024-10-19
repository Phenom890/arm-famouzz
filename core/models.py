from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

TAG_CHOICES = (
    ('warning', 'New'),
    ('primary', 'Best Seller'),
    ('danger', 'Out Of stock'),
    ('info', 'Discounted'),

)

CATEGORY_CHOICES = (
    ('AW', 'African'),
    ('CW', 'Casual'),
    ('FW', 'Formal'),
    ('WW', 'Foreign')
)

REGION_CHOICES = (
    ('AS', 'Ashanti'),
    ('GA', 'Accra'),
    ('WR', 'Western'),
    ('OR', 'Oti'),
    ('NR', 'Northern'),
    ('UW', 'Upper West'),
    ('UE', 'Upper East')
)


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    tag = models.CharField(max_length=15, choices=TAG_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item}"

    def get_final_price(self):
        if self.item.discount_price:
            return self.item.discount_price
        return self.item.price

    def get_total_price(self):
        return float(self.get_final_price() * self.quantity)

    def get_total(self):
        return self.item.price * self.quantity

    def get_discount_price(self):
        return self.item.discount_price * self.quantity

    def get_saved_amount(self):
        if self.item.discount_price:
            return self.get_total() - self.get_discount_price()


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    ref_code = models.CharField(unique=True, max_length=20)
    items = models.ManyToManyField(OrderItem)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order of {self.owner}"

    def get_final_cost(self):
        total = 0.00
        for item in self.items.all():
            total += item.get_total_price()
        return total

    def get_total_amount(self):
        total = self.get_final_cost()
        if self.coupon:
            total -= (self.coupon.coupon_percentage / 100) * total
        return total


class Address(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    locality = models.CharField(max_length=200)
    street_name = models.CharField(max_length=200)
    region = models.CharField(max_length=2, choices=REGION_CHOICES)
    house_number = models.CharField(max_length=200)
    created = models.DateTimeField(default=timezone.now)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.locality

    class Meta:
        verbose_name_plural = 'Addresses'


class Coupon(models.Model):
    name = models.CharField(max_length=20)
    coupon_percentage = models.IntegerField()

    def __str__(self):
        return self.name


class Refund(models.Model):
    issuer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_ref = models.CharField(max_length=30)
    reason = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.issuer.username
