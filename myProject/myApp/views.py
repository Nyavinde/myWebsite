from django.views.generic import TemplateView,View, CreateView, FormView
from django.shortcuts import render, redirect
from .forms import FormCheck,CustomerRegistrationForm,CustomerLoginForm
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate, login,logout
from django.http import JsonResponse
from .models import *



# Create your views here.


class HomeView(TemplateView):
    template_name="home.html"


class ProductView(TemplateView):
    template_name="product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list']=Product.objects.all()
        return context

class AddToCartView(TemplateView):
    template_name = "addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Product.objects.get(id=product_id)

        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)

            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()

        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()

        return context

class ManageCartView(View):
    def get(self,request,*args,**kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity +=1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total +=cp_obj.rate
            cart_obj.save()

        elif action == "dcr":
            cp_obj.quantity -=1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -=cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity ==0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("myApp:mycart")

class MyCartView(TemplateView):
    template_name = "mycart.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart']=cart
        return context


class CheckOutView(CreateView):
    template_name = "checkout.html"
    form_class = FormCheck
    success_url = reverse_lazy("myApp:product")

    def dispatch(self,request,*args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("/login?/then=/checkout/")
        return super().dispatch(request,*args,*kwargs)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id",None)

        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self,form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Reeieved"
            del self.request.session["cart_id"]
            pay_m = form.cleaned_data.get("payment_method")
            order = form.save()

            if pay_m=="Khalti":
                return redirect(reverse("myApp:khaltirequest") + "?o_id=" + str(order.id))
            elif pay_m=="PayPal":
                return redirect(reverse("myApp:paypalrequest") + "?o_id=" + str(order.id))
        else:
            return redirect("myApp:home")

        return super().form_valid(form)

class KhaltiRequestView(View):
    def get(self, request, *args, **kwargs):
        o_id = request.GET.get("o_id")
        order = Order.objects.get(id=o_id)
        context = {
            "order":order
        }
        return render(request, "khaltirequest.html",context)




class PayPalRequestView(View):
    def get(self, request, *args, **kwargs):
        o_id = request.GET.get("o_id")
        order = Order.objects.get(id=o_id)
        context = {
            "order":order
        }
        return render(request, "paypal.html",context)



class CustomerRegistrationView(CreateView):
    template_name = "customer_registration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("myApp:home")

    def form_valid(self,form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username,email,password)
        form.instance.user = user
        login(self.request,user)
        return super().form_valid(form)


class CustomerLogoutView(View):

    def get(self,request):
        logout(request)
        return redirect("myApp:home")

class CustomerLoginView(FormView):
    template_name = "customerlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("myApp:home")

    def form_valid(self,form):
        uname = form.cleaned_data.get("username")
        pasword = form.cleaned_data.get("password")
        usr = authenticate(username=uname,password=pasword)

        if usr is not None and usr.customer:
            login(self.request,usr)
        else:
            return render(self.request,self.template_name,{"form":self.form_class,"error":"Invalid credentials"})
        return super().form_valid(form)


class AboutView(TemplateView):
    template_name="about.html"

class ContactView(TemplateView):
    template_name="contact.html"

class TeamView(TemplateView):
    template_name="team.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_list']=Team.objects.all()
        return context
