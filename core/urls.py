from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/<username>/', views.ContactView.as_view(), name='contact'),
    path('product/<int:pk>/', views.ProductView.as_view(), name='product_display'),
    path('sold-out/', views.sold_out_view, name='sold_out'),
    path('search/', views.search, name='search'),

    path('plus/<int:pk>/', views.plus_cart, name='plus_cart'),
    path('minus/<int:pk>/', views.minus_cart, name='minus_cart'),
    path('remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),

    path('cart/', views.CartView.as_view(), name='show_cart'),
    path('add-coupon/', views.AddCoupon.as_view(), name='add_coupon'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('request/refund/<int:pk>/', views.RequestRefundView.as_view(), name='request_refund'),

]


