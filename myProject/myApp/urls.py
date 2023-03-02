from django.urls import path
from .views import *
from myApp import views

app_name = "myApp"

urlpatterns = [
path("", HomeView.as_view(), name="home"),
path("about/",AboutView.as_view(), name="about"),
path("team/",TeamView.as_view(), name="team"),
path("product/",ProductView.as_view(), name="product"),
path("add-to-cart-<int:pro_id>/",AddToCartView.as_view(),name="addtocart"),
path("my-cart/",MyCartView.as_view(),name="mycart"),
path("manage-cart/<int:cp_id>/",ManageCartView.as_view(),name="managecart"),
path("checkout/",CheckOutView.as_view(),name="checkout"),
path("khalti-request/",KhaltiRequestView.as_view(),name="khaltirequest"),

path("paypal-request/",PayPalRequestView.as_view(),name="paypalrequest"),

path("register/",CustomerRegistrationView.as_view(),name="customerregistration"),
path("logout/",CustomerLogoutView.as_view(),name="customerlogout"),
path("login/",CustomerLoginView.as_view(),name="customerlogin"),

]
