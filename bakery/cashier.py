from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.db.models import Sum
from .forms import *
from .models import *
from bakery import *
from school.models import *
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, View, CreateView
from django.views.generic.edit import CreateView, UpdateView
from django.http import JsonResponse
from django.core import serializers
import datetime
from django.contrib.auth.decorators import login_required
from school_management_system.settings import TWILIO_ACCOUNT_SID2, TWILIO_AUTH_TOKEN2, TWILIO_PHONE_NUMBER2
from twilio.rest import Client
from .filters import *
from .thread import *

@login_required
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            today = datetime.datetime.now().date()
            customer = form.save()
            order = Order.objects.create(customer=customer, order_date=today, due_date=customer.due_dates)
            print(customer)
            request.session['id'] = order.id
            if customer.due_dates:
                return redirect('shop:Takeorderitems')
            else:
                return redirect('shop:orderitems')

    else:
        form = CustomerForm()

    template = 'backery/customer.html'
    context = {
        'form': form,
    }
    return render(request, template, context)



class orderitems(CreateView):
    model = Order_Details
    form_class = OrderdetailsForm
    template = 'backery/create_order.html'



    def get(self, *args, **kwargs):
         if self.request.session['id']:
            order_id = self.request.session['id']
            order = Order.objects.get(id=order_id)
            form = self.form_class()
            detail = Order_Details.objects.filter(order_id=order)
            gross_total = detail.aggregate(cc=Sum('gross_price'))

            vat =  0.00
            if not gross_total['cc']:
                total_sum = 0.00
            else:
                total_sum = float(gross_total['cc'])
            if not gross_total['cc']:
                order.gross_price = 0.00
            else:
                order.gross_price = gross_total['cc']
            order.vat = vat
            order.save()
            return render(self.request, self.template, {"form": form, "detail":detail, "vat": vat,"total_sum":total_sum,"order":order})

    def post(self,  *args, **kwargs):
        if self.request.is_ajax and self.request.method =="POST":
            form = self.form_class(self.request.POST)
            if self.request.session['id']:
                order_id = self.request.session['id']
                order = Order.objects.get(id=order_id)
            if form.is_valid():

                instance = form.save(commit=False)
                product = Product.objects.get(name = instance.product)
                product_unit_price = product.unit_price
                instance.order_id = order
                instance.unit_price = product_unit_price
                instance.gross_price = product_unit_price * instance.quantity
                instance.save()
                get_product = Inventory.objects.get(product_id=product.id)
                get_product.outgoing += instance.quantity
                Inventory_records.objects.create(
                    product=product, quantity=instance.quantity, unit_price=product.unit_price, status="Outgoing")
                get_product.save()
                ser_instance = serializers.serialize('json', [instance, ])
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)

    def form_valid(self,form):
        messages.success(self.request, 'Sales item added')
        return super().form_valid(form)


@login_required
def deletes(request,pk):
    pro = Order_Details.objects.get(id=pk)
    product = Product.objects.get(name=pro.product)
    get_product = Inventory.objects.get(product_id=product.id)
    get_product.outgoing -= pro.quantity
    get_product.save()
    Inventory_records.objects.create(
        product=product, quantity=pro.quantity, unit_price=product.unit_price, status="Incoming")
    pro.delete()
    return redirect('shop:orderitems')


@login_required
def checkout(request):
    if request.session['id']:
        order_id = request.session['id']
        order = Order.objects.get(id =order_id)
        detail = Order_Details.objects.filter(order_id=order.id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            today = datetime.datetime.now()
            order.amount_paid = form.cleaned_data['amount_paid']
            order.save()

            try:
                code = Account_code.objects.get(code="Sales")
            except Account_code.DoesNotExist:
                code = Account_code.objects.create(code="Sales")
            company = Company_group.objects.get(name="Party Tree Bakes")

            Revenue.objects.create(
                account_code=code, amount=order.amount_paid, company=company)
            client = Client(TWILIO_ACCOUNT_SID2, TWILIO_AUTH_TOKEN2)
            # ,http_client=proxy_client
            today = datetime.datetime.now().date()
            CheckoutThread(order).start()

    else:
        form = PaymentForm()
    template = 'backery/checkout.html'
    context = {
        'order': order,
        'detail': detail,
        'form': form,
    }
    return render(request,template,context)

@login_required
def checkout_print(request,pk):

    order = Order.objects.get(id=pk)
    detail = Order_Details.objects.filter(order_id=order.id)
    template = 'backery/checkout_print.html'
    context = {
        'order': order,
        'detail': detail,
    }
    return render(request, template, context)

@login_required
def Vew_order(request,pk):

    order = Order.objects.get(id=pk)
    detail = Order_Details.objects.filter(order_id=order.id)
    template = 'backery/view_order.html'
    context = {
        'order': order,
        'detail': detail,
    }
    return render(request, template, context)


@login_required
def close_order(request):
    if request.session['id']:
        try:
            del request.session['id']
            return redirect('shop:manage_order')
        except KeyError:
            return redirect('shop:manage_order')


@login_required
def close(request):
    return redirect('shop:manage_order')

@login_required
def manage_order(request):

    orders = Order.objects.filter(clear=False)
    template = 'backery/manage_orders.html'
    context = {
        'orders': orders,
    }
    return render(request,template,context)


class Takeorderitems(CreateView):
    model = Order_Details
    form_class = TakeOrderdetailsForm
    template = 'backery/create_order_out.html'

    def get(self, *args, **kwargs):
        if self.request.session['id']:
            order_id = self.request.session['id']
            order = Order.objects.get(id=order_id)
            form = self.form_class()
            detail = Order_Details.objects.filter(order_id=order)
            gross_total = detail.aggregate(cc=Sum('gross_price'))

            vat =  0.00
            if not gross_total['cc']:
                total_sum = 0.00
            else:
                total_sum = float(gross_total['cc'])
            if not gross_total['cc']:
                order.gross_price = 0.00
            else:
                order.gross_price = gross_total['cc']
            order.vat = vat
            order.save()
            return render(self.request, self.template, {"form": form, "detail": detail, "vat": vat, "total_sum": total_sum, "order": order})

    def post(self,  *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            form = self.form_class(self.request.POST)
            if self.request.session['id']:
                order_id = self.request.session['id']
                order = Order.objects.get(id=order_id)
            if form.is_valid():

                instance = form.save(commit=False)
                product = Product.objects.get(name=instance.product)
                product_unit_price = product.unit_price
                instance.order_id = order
                instance.unit_price = product_unit_price
                instance.gross_price = product_unit_price * instance.quantity
                instance.save()
                ser_instance = serializers.serialize('json', [instance, ])
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)

    def form_valid(self, form):
        messages.success(self.request, 'Order item added')
        return super().form_valid(form)


@login_required
def makepayment(request,pk):
    order = Order.objects.get(id=pk)
    detail = Order_Details.objects.filter(order_id=order.id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            today = datetime.datetime.now()
            dd = form.cleaned_data['amount_paid']
            order.amount_paid += form.cleaned_data['amount_paid']
            order.save()
            try:
                code = Account_code.objects.get(code="Sales")
            except Account_code.DoesNotExist:
                code = Account_code.objects.create(code="Sales")
            company = Company_group.objects.get(name="Party Tree Bakes")
            Revenue.objects.create(
                account_code=code, amount=dd, company=company)
            PaymentThread(order).start()

            messages.success(request, 'Payment made Sucessfully')
            return redirect('shop:manage_order')
    else:
        form = PaymentForm()
    template = 'backery/check.html'
    context = {
        'order': order,
        'detail': detail,
        'form': form,
    }
    return render(request, template, context)


@login_required
def debt(request):
    ord = Order.objects.filter(balance__gt=0.00)
    total = ord.aggregate(cc=Sum('total_price'))

    myFilter = AccountRecievableFilter(request.GET, queryset=ord)
    ord = myFilter.qs
    total = myFilter.qs.aggregate(cc=Sum('total_price'))

    template = 'backery/accountrecieve.html'
    context = {
        'ord': ord,
        'myFilter': myFilter,
        'total': total,
    }
    return render(request, template, context)
