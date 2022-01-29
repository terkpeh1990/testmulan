from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.db.models import Sum
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, View, CreateView
from django.views.generic.edit import CreateView, UpdateView
from django.http import JsonResponse
from django.core import serializers
import datetime
from .forms import *
from .models import *
from school.models import *
from django.contrib.auth.decorators import login_required
from school_management_system.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER2
from twilio.rest import Client
from .filters import *


@login_required
def manage_category(request):
    category = Category.objects.all()

    template = 'backery/manage_category.html'

    context = {
        'category': category,
    }

    return render(request,template,context)


@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Created')
            return redirect('shop:manage_category')

    else:
        form = CategoryForm()

    template = 'backery/create_category.html'
    context = {
        'form': form,
    }
    return render(request,template,context)


@login_required
def edit_category(request,pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Updated')
            return redirect('shop:manage_category')

    else:
        form = CategoryForm(instance=category)

    template = 'backery/create_category.html'
    context = {
        'form': form,
    }
    return render(request,template,context)


@login_required
def manage_product(request):
    product = Product.objects.all()

    template = 'backery/manage_product.html'

    context = {
        'product': product,
    }

    return render(request,template,context)


@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Created')
            return redirect('shop:manage_product')

    else:
        form = ProductForm()

    template = 'backery/create_product.html'
    context = {
        'form': form,
    }
    return render(request,template,context)


@login_required
def edit_product(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Updated')
            return redirect('shop:manage_product')

    else:
        form = ProductForm(instance=product)

    template = 'backery/create_product.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def create_restock(request):
    if request.method == 'POST':
        form = RestockForm(request.POST)
        if form.is_valid():
            restockform=form.save(commit=False)
            restockform.status = "Incoming"
            product = Product.objects.get(id=restockform.product.id)
            restockform.unit_price = product.unit_price
            restockform.approval = "Pending"
            restockform.save()
            messages.success(request, 'Restock Created Waiting For Approval')
            return redirect('shop:manage_restock')

    else:
        form = RestockForm()

    template = 'backery/restock.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def cancel_restock(request, pk):
    restock = Inventory_records.objects.get(pk=pk)
    restock.approval = "Cancelled"
    restock.save()
    messages.success(request, 'Restock Cancelled')
    return redirect('shop:pending_restock')

@login_required
def approve_restock(request,pk):
    restock = Inventory_records.objects.get(pk=pk)
    try:
        product = Product.objects.get(id=restock.product.id)
        get_product = Inventory.objects.get(product_id=product.id)
        get_product.instock += restock.quantity
        get_product.unit_price = product.unit_price
        get_product.save()

    except Inventory.DoesNotExist:
        product = Product.objects.get(id=restock.product.id)
        Inventory.objects.create(product_id=product, instock=restock.quantity, unit_price =product.unit_price)
    restock.approval = "Approved"
    restock.save()
    messages.success(request, 'Restock Approved')
    return redirect('shop:pending_restock')


@login_required
def manage_restock(request):
    restock = Inventory_records.objects.filter(clear=False)

    template = 'backery/manage_restock.html'

    context = {
        'restock': restock,
    }

    return render(request, template, context)


@login_required
def pending_restock(request):
    restock = Inventory_records.objects.filter(approval = 'Pending')

    template = 'backery/manage_restock.html'

    context = {
        'restock': restock,
    }

    return render(request, template, context)


@login_required
def manage_damages(request):
    damage = Damages.objects.filter(clear=False)

    template = 'backery/manage_damages.html'

    context = {
        'damage': damage,
    }

    return render(request, template, context)


@login_required
def pending_damages(request):
    damage = Damages.objects.filter(dastatus = "Pending")

    template = 'backery/manage_damages.html'

    context = {
        'damage': damage,
    }

    return render(request, template, context)

@login_required
def create_damage(request):
    if request.method == 'POST':
        form = DamageForm(request.POST)
        if form.is_valid():
            damageform = form.save(commit=False)
            damageform.dastatus = "Pending"
            damageform.save()
            messages.success(request, 'Damage Recorded Waiting For Approval')
            return redirect('shop:manage_damages')

    else:
        form = DamageForm()

    template = 'backery/damages.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def cancel_damages(request, pk):
    damage = Damages.objects.get(pk=pk)
    damage.dastatus = "Cancelled"
    damage.save()
    messages.success(request, 'Damages Cancelled')
    return redirect('shop:pending_damages')

@login_required
def approve_damage(request,pk):
    damage = Damages.objects.get(pk=pk)
    try:
        product = Product.objects.get(id=damage.product_id.id)
        get_product = Inventory.objects.get(product_id=product.id)
        get_product.outgoing += damage.quantity
        get_product.save()
        cost = product.unit_price * damage.quantity
        Inventory_records.objects.create(
            product=product, quantity=damage.quantity, unit_price=product.unit_price, status="Outgoing")
        try:
            code = Account_code.objects.get(code="Damages")
        except Account_code.DoesNotExist:
            code = Account_code.objects.create(code="Damages")
        company = Company_group.objects.get(name="Party Tree Bakes")
        pv = Pv.objects.create(
                    account_code=code, company=company, description="Cost of Damages From Party Tree Bakes", amount=cost, status="approved")
        pv_detail = Pv_details.objects.create(
                    pv=pv, description=pv.description, amount=pv.amount)
        Expenditure.objects.create(
                account_code=code, amount=cost, damage=damage, company=company)

    except Inventory.DoesNotExist:
        pass
    damage.dastatus = "Approved"
    damage.save()
    messages.success(request,'Damages Proccessed Successfully')
    return redirect('shop:pending_damages')

@login_required
def manage_inventory(request):
    inventory = Inventory.objects.all()

    template = 'backery/manage_inventory.html'

    context = {
        'inventory': inventory,
    }

    return render(request, template, context)


@login_required
def closing_stock(request):
    inventorys = Inventory.objects.all()
    for inventory in inventorys:
        product = Product.objects.get(id = inventory.product_id.id)
        Closing_stocks.objects.create(
            product=product, closing_stock=inventory.avialable_stock, avialable_stock_cost=inventory.avialable_stock_cost, close_status = "Pending")
    messages.success(request, 'Stock Closed')
    return redirect('shop:manage_inventory')

@login_required
def approve_closing_stock(request,pk):
    closed = Closing_stocks.objects.get(pk=pk)
    closed.close_status = "Approved"
    closed.save()
    messages.success(request, 'Closing Stock Approved')
    return redirect('shop:pending_stock')

@login_required
def closed_stock(request):
    close_stock = Closing_stocks.objects.filter(clear = False)
    template = 'backery/closedstock.html'

    context = {
        'close_stock': close_stock,
    }
    return render(request, template, context)

@login_required
def pending_stock(request):
    close_stock = Closing_stocks.objects.filter(close_status = 'Pending')
    template = 'backery/closedstock.html'

    context = {
        'close_stock': close_stock,
    }
    return render(request, template, context)


@login_required
def daily_sales(request):
    today = datetime.datetime.now()
    company = Company_group.objects.get(name="Party Tree Bakes")
    ord = Revenue.objects.filter(company=company.id,
        created_date=today)
    total = ord.aggregate(cc=Sum('amount'))
    template = 'backery/revenueall.html'
    context = {
        'ord': ord,
        'total': total,
    }
    return render(request, template, context)

@login_required
def taxation(request):
    ord = Order.objects.filter(vat__gt=0.00)
    total = ord.aggregate(cc=Sum('vat'))

    myFilter = AccountRecievableFilter(request.GET, queryset=ord)
    ord = myFilter.qs
    total = myFilter.qs.aggregate(cc=Sum('vat'))

    template = 'backery/bakeryvat.html'
    context = {
        'ord': ord,
        'myFilter': myFilter,
        'total': total,
    }
    return render(request, template, context)

def EditInventory(request,pk):
    product_inventory = Inventory.objects.get(pk=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data['quantity']
            product_inventory.outgoing += int(qty)
            product_inventory.save()
            messages.success(request,"Inventory Updated")
            return redirect('shop:EditInventory', pk=product_inventory.id)
    else:
        form = InventoryForm()
    template = 'backery/updateinventory.html'
    context = {
        'form': form,
        'product_inventory': product_inventory
    }
    return render(request, template, context)

def run_to_zero(request):
    cc = Inventory.objects.all()
    for i in cc:
        i.instock = 0
        i.outgoing = 0
        i.save()
    messages.success(request,"Run to Zero Done")
    return redirect('shop:manage_inventory')


def clear_restock(request):
    cc = Inventory_records.objects.all()
    for i in cc:
        i.clear = True
        i.save()
    messages.success(request,"Hidden")
    return redirect('shop:manage_restock')

def clear_damage(request):
    cc = Damages.objects.all()
    for i in cc:
        i.clear = True
        i.save()
    messages.success(request,"Hidden")
    return redirect('shop:manage_damages')


def clear_closing(request):
    cc = Closing_stocks.objects.all()
    for i in cc:
        i.clear = True
        i.save()
    messages.success(request,"Hidden")
    return redirect('shop:closed_stock')

def clear_order(request):
    cc = Order.objects.all()
    for i in cc:
        i.clear = True
        i.save()
    messages.success(request,"Hidden")
    return redirect('shop:manage_order')


def manage_snack(request):
    snack = Snacks.objects.all()
    template = 'backery/manage_snacks.html'
    context = {
        'snack':snack,
        }
    return render(request,template,context)

@login_required
def create_snack(request):
    if request.method == 'POST':
        form = SnackForm(request.POST)
        if form.is_valid():
            cc=form.save()
            if cc.activity == 'CEO':
                cc.status = 'Approved'
                cc.save()
                Snack_detail.objects.create(student_name="CeO MrS.ThErA",snack=cc)
                customer = Customer.objects.create(name="CeO MrS.ThErA",phone="0553946918")
                today = datetime.datetime.now().date()
                order = Order.objects.create(customer=customer, order_date=today,snack=cc)
                print(customer)
                request.session['id'] = order.id
                return redirect('shop:orderitems')
            else:
                cc.status = 'Pending'
                cc.save()
                request.session['id'] = cc.id
                print(cc.id)
                messages.success(request, 'Snack Created')
                return redirect('shop:snack_detail')

    else:
        form = SnackForm()

    template = 'backery/create_snack.html'
    context = {
        'form': form,
    }
    return render(request,template,context)

class snack_detail(CreateView):
    model = Snack_detail
    form_class = SnackDetailForm
    template = 'backery/snack_detail.html'

    def get(self, *args, **kwargs):
        if self.request.session['id']:
            order_id = self.request.session['id']
            order = Snacks.objects.get(id=order_id)
            form = self.form_class()
            detail = Snack_detail.objects.filter(snack=order)

            return render(self.request, self.template, {"form": form, "detail": detail, "order": order})

    def post(self,  *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            form = self.form_class(self.request.POST)
            if self.request.session['id']:
                order_id = self.request.session['id']
                order = Snacks.objects.get(id=order_id)
                print(order)
                details = Snack_detail.objects.filter(snack=order.id)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.snack = order
                instance.save()
                ser_instance = serializers.serialize('json', [instance, ])
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)

    def form_valid(self, form):
        messages.success(self.request, 'Student added')
        return super().form_valid(form)

def View_snack(request,pk):

    order = Snacks.objects.get(id=pk)
    detail = Snack_detail.objects.filter(snack=order.id)


    template = 'backery/view_snack.html'
    context = {
        'order': order,
        'detail': detail,
    }
    return render(request, template, context)

def View_snacked(request,pk):

    order = Snacks.objects.get(id=pk)
    detail = Snack_detail.objects.filter(snack=order.id)

    snack_order = Order.objects.get(snack=order)

    snack_order_detail = Order_Details.objects.filter(order_id=snack_order.id)
    template = 'backery/view_snack.html'
    context = {
        'order': order,
        'detail': detail,
        'snack_order':snack_order,
        'snack_order_detail':snack_order_detail,
    }
    return render(request, template, context)


def cancel_snack(request, pk):
    restock = Snacks.objects.get(pk=pk)
    restock.status = "Cancelled"
    restock.save()
    messages.success(request, 'Snack Request Cancelled')
    return redirect('shop:pending_snack')


def approve_snack(request, pk):
    restock = Snacks.objects.get(pk=pk)
    restock.status = "Approved"
    restock.save()
    messages.success(request, 'Snack Request Approved')
    return redirect('shop:pending_snack')

def pending_snack(request):
    snack = Snacks.objects.filter(status="Pending")
    template = 'backery/manage_snacks.html'
    context = {
        'snack':snack,
        }
    return render(request,template,context)


def deletes_snackitems(request,pk):
    pro = Snack_detail.objects.get(id=pk)
    pro.delete()
    return redirect('shop:snack_detail')


def delete_snack(request,pk):
    pro = Snacks.objects.get(id=pk)
    pro.delete()
    return redirect('shop:manage_snack')


def closesnack(request):
    if request.session['id']:
        try:
            del request.session['id']
            return redirect('shop:manage_snack')
        except KeyError:
            return redirect('shop:manage_snack')


def snackorder(request,pk):
    snack = Snacks.objects.get(id=pk)
    customer = Customer.objects.create(name="Mulan Snacks",phone="0553946918")
    today = datetime.datetime.now().date()
    order = Order.objects.create(customer=customer, order_date=today,snack=snack)
    print(customer)
    request.session['id'] = order.id
    return redirect('shop:orderitems')







