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
from school_management_system.settings import TWILIO_ACCOUNT_SID3, TWILIO_AUTH_TOKEN3, TWILIO_PHONE_NUMBER3
from twilio.rest import Client


@login_required
def create_order(request):
    order = Orders.objects.create()
    return redirect('partytree:orderitemss', order.id)


def orderitemss(request,pk):
    order = Orders.objects.get(id=pk)
    detail = Order_Detailss.objects.filter(order_id=order)
    list_inventory = Inventorys.objects.filter(avialable_stock__gt=0)
    gross_total = detail.aggregate(cc=Sum('gross_price'))
    order.gross_price= gross_total['cc']
    order.save()
    
    template = 'partytree/create_order.html'
    context ={
            "detail": detail,
            "order": order,
            "list_inventory": list_inventory,
        }
    return render(request, template, context)

def adjuest_quantity(request,pk,order_id):
    detail = Order_Detailss.objects.get(id=pk)
    if request.method == 'POST':
        form = QtyForm(request.POST)
       
        if form.is_valid():
            qty = form.cleaned_data.get('quantity')

            get_inventory = Inventorys.objects.get(product_id=detail.product.id)
            if qty >= get_inventory.avialable_stock:
                messages.success(request,"Quantity Cannot be more than Available StocK :"+ " "+ str(get_inventory.avialable_stock) )
                return redirect('partytree:adjuest_quantity',detail.id,detail.order_id)
    
            
            
            get_inventory.outgoing += qty
            detail.quantity+=qty
            detail.save()
            get_inventory.save()
            return redirect('partytree:orderitemss', pk=order_id)

    else:
        form = QtyForm()

    template = 'partytree/qtyad.html'
    context = {
        'form': form,
    }
    return render(request, template, context)

def cancel_order(request,pk):
    order = Orders.objects.get(id=pk)
    details = Order_Detailss.objects.filter(order_id=order.id)
    for a in details:
        get_inventory = Inventorys.objects.get(product_id=a.product)
        get_inventory.outgoing -= a.quantity
        get_inventory.save()
    order.delete()
    messages.success(request,"Order Cancelled")
    return redirect('partytree:manage_order')


def add_items_to_chart(request,pk,order_id):
    
       
    order = Orders.objects.get(id=order_id)
    get_inventory = Inventorys.objects.get(id=pk)
    get_product = Products.objects.get(name=get_inventory.product_id.name)
    details = Order_Detailss.objects.create(
            product=get_product, unit_price=get_product.unit_price, quantity=1, gross_price=get_product.unit_price, order_id =order)
        # get_inventory.instock -= 1
    get_inventory.outgoing += 1
    get_inventory.save()
    print(get_inventory.instock)
    get_product.save()
    Inventory_recordss.objects.create(
        product=get_product, quantity=details.quantity, unit_price=get_product.unit_price, status="Outgoing")
    messages.success(request,"Item Added To Chart")
    return redirect('partytree:orderitemss',pk =order.id)



class orderitems(CreateView):
    model = Order_Details
    form_class = OrderdetailsForm
    template = 'partytree/create_order.html'

    def get(self, *args, **kwargs):
        if self.request.session['id']:
            order_id = self.request.session['id']
            order = Orders.objects.get(id=order_id)
            form = self.form_class()
            detail = Order_Detailss.objects.filter(order_id=order)
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
                order = Orders.objects.get(id=order_id)
            if form.is_valid():

                instance = form.save(commit=False)
                product = Products.objects.get(name=instance.product)
                product_unit_price = product.unit_price
                instance.order_id = order
                instance.unit_price = product_unit_price
                instance.gross_price = product_unit_price * instance.quantity
                instance.save()
                get_product = Inventorys.objects.get(product_id=product.id)
                get_product.instock -= instance.quantity
                get_product.outgoing += instance.quantity
                print(get_product.instock)
                get_product.save()
                Inventory_recordss.objects.create(
                    product=product, quantity=instance.quantity, unit_price=product.unit_price, status="Outgoing")
                # get_product.save()
                ser_instance = serializers.serialize('json', [instance, ])
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)

    def form_valid(self, form):
        messages.success(self.request, 'Sales item added')
        return super().form_valid(form)


@login_required
def deletes(request, pk):
    pro = Order_Detailss.objects.get(id=pk)
    order_id = pro.order_id 
    product = Products.objects.get(name=pro.product)
    get_product = Inventorys.objects.get(product_id=product.id)
    get_product.outgoing -= pro.quantity
    get_product.save()
    Inventory_recordss.objects.create(
        product=product, quantity=pro.quantity, unit_price=product.unit_price, status="Incoming")
    pro.delete()
    messages.success(request, 'Item Removed')
    return redirect('partytree:orderitemss',order_id )


@login_required
def checkout(request,pk):
    
    
    order = Orders.objects.get(id=pk)
    detail = Order_Detailss.objects.filter(order_id=order.id)

    if request.method == 'POST':
        form = paymentForm(request.POST)
        if form.is_valid():
            today = datetime.datetime.now()
            cc = form.cleaned_data['amount']
            if (cc + order.amount_paid) > order.gross_price:
                bb = order.gross_price - order.amount_paid
                messages.success(request,"Amount Entered cannot be more than" + " "+ "GHC"+ " "+ str(bb))
                return redirect('partytree:checkout',order.id)
            else:
                order.amount_paid += form.cleaned_data['amount'] 
                order.save()


            try:
                code = Account_code.objects.get(code="Sales")
            except Account_code.DoesNotExist:
                code = Account_code.objects.create(code="Sales")
            
            try:
                company = Company_group.objects.get(name="Party Tree")
            except Company_group.DoesNotExist:
                company = Company_group.objects.create(name="Party Tree")
            
            Revenue.objects.create(
                account_code=code, amount=cc, company=company)
            # client = Client(TWILIO_ACCOUNT_SID3, TWILIO_AUTH_TOKEN3)
            # ,http_client=proxy_client
            today = datetime.datetime.now().date()

            # try:
            #     message = client.messages.create(
            #         to="+233" + order.customer.phone,
            #         from_=TWILIO_PHONE_NUMBER3,
            #         body="Dear" + " " + order.customer.name + "," + " " + "The total cost of your order with ID" + " "+order.id + " " + "is " + " " + "GHC" + " " + str(order.total_price) + "." + " " + " You have made payment of GHC" + " " + str(order.amount_paid) + " " + ".Thank you for choosing Party Tree, For enquiries and orders, Please contact us on 0302941093 or 0209684691(Whatsapp).")
            # except IOError:
            #     print('fail')
            #     pass


    else:
        form = paymentForm()
    template = 'partytree/checkout.html'
    context = {
        'order': order,
        'detail': detail,
        'form': form,
    }
    return render(request, template, context)


@login_required
def checkout_print(request, pk):

    order = Orders.objects.get(id=pk)
    detail = Order_Detailss.objects.filter(order_id=order.id)
    template = 'partytree/checkout_print.html'
    context = {
        'order': order,
        'detail': detail,
    }
    return render(request, template, context)


@login_required
def Vew_order(request, pk):

    order = Orders.objects.get(id=pk)
    detail = Order_Detailss.objects.filter(order_id=order.id)
    template = 'partytree/view_order.html'
    context = {
        'order': order,
        'detail': detail,
    }
    return render(request, template, context)


@login_required
def close_order(request):
    
    return redirect('partytree:manage_order')
        


@login_required
def close(request):
    return redirect('partytree:manage_order')


@login_required
def manage_order(request):
    today =datetime.date.today()
    list_inventory = Inventorys.objects.filter(avialable_stock__gt=0)
    orders = Orders.objects.filter(gross_price__gt=0.00,order_date=today)
    ord = Orders.objects.filter(gross_price__gt=0.00,order_date=today)
    company = Company_group.objects.get(name="Party Tree")
    to = ord.count()
    grss = Revenue.objects.filter(company=company.id,
        created_date=today).aggregate(cc=Sum('amount'))
    template = 'partytree/manage_orders.html'
    context = {
        'orders': orders,
        'grss':grss,
        'to':to,
        'list_inventory':list_inventory,
    }
    return render(request, template, context)

def search_order(request):
    today =datetime.date.today()
    
    orders = Orders.objects.filter(gross_price__gt=0.00)
    
    to = orders.count()
    grss = orders.aggregate(cc=Sum('gross_price'))
    template = 'partytree/search.html'
    context = {
        'orders': orders,
        'grss':grss,
        'to':to,
    }
    return render(request, template, context)


@login_required
def makepayment(request, pk):
    order = Orders.objects.get(id=pk)
    detail = Order_Detailss.objects.filter(order_id=order.id)

    if request.method == 'POST':
        form = paymentForm(request.POST)
        if form.is_valid():
            cc = form.cleaned_data['amount']
            if (cc + order.amount_paid) > order.gross_price:
                bb = order.gross_price - order.amount_paid
                messages.success(request,"Amount Entered cannot be more than" + " "+ "GHC"+ " "+ str(bb))
                return redirect('partytree:checkout',order.id)
            else:
                order.amount_paid += form.cleaned_data['amount'] 
                order.save()
            
            try:
                code = Account_code.objects.get(code="Sales")
            except Account_code.DoesNotExist:
                code = Account_code.objects.create(code="Sales")
            try:
                company = Company_group.objects.get(name="Party Tree")
            except Company_group.DoesNotExist:
                company = Company_group.objects.create(name="Party Tree")
            
            Revenue.objects.create(
                account_code=code, amount=cc, company=company)
            # try:
            #     message = client.messages.create(
            #         to="+233" + order.customer.phone,
            #         from_=TWILIO_PHONE_NUMBER3,
            #         body="Dear" + " " + order.customer.name + "," + " " + "The total cost of your order with ID" + " "+order.id + " " + "is " + " " + "GHC" + " " + str(order.total_price) + "." + " " + " You have made payment of GHC" + " " + str(order.amount_paid) + " " + ".Thank you for choosing Party Tree, For enquiries and orders, Please contact us on 0302941093 or 0209684691(Whatsapp).")
            # except IOError:
            #     print('fail')
            #     pass

            messages.success(request, 'Payment made Sucessfully')
            return redirect('partytree:manage_order')
    else:
        form = paymentForm()
    template = 'partytree/checkout.html'
    context = {
        'order': order,
        'detail': detail,
        'form': form,
    }
    return render(request, template, context)



def daily_sales(request):
    today = datetime.datetime.now()
    company = Company_group.objects.get(name="Party Tree")
    ord = Revenue.objects.filter(company=company.id,
        created_date=today)
    total = ord.aggregate(cc=Sum('amount'))
    od = Orders.objects.filter(order_date=today).count()
    template = 'partytree/dailysales.html'
    context = {
        'ord': ord,
        'total': total,
        'od': od,
    }
    return render(request, template, context)