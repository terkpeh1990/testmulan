from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.db.models import Sum
from .forms import *
from .models import *
from school.models import *
from django.contrib.auth.decorators import login_required
# from .filters import *


@login_required
def manage_category(request):
    category = Categorys.objects.all()

    template = 'partytree/manage_category.html'

    context = {
        'category': category,
    }

    return render(request, template, context)


@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('partytree:manage_category')

    else:
        form = CategoryForm()

    template = 'partytree/create_category.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def edit_category(request, pk):
    category = Categorys.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('partytree:manage_category')

    else:
        form = CategoryForm(instance=category)

    template = 'partytree/create_category.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


# @login_required
def manage_product(request):
    product = Products.objects.all().order_by('name')

    template = 'partytree/manage_product.html'

    context = {
        'product': product,
    }

    return render(request, template, context)


@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('partytree:manage_product')

    else:
        form = ProductForm()

    template = 'partytree/create_product.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def edit_product(request, pk):
    product = Products.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('partytree:manage_product')

    else:
        form = ProductForm(instance=product)

    template = 'partytree/create_product.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def create_restock(request):
    if request.method == 'POST':
        form = RestockForm(request.POST)
        if form.is_valid():
            restockform = form.save(commit=False)
            restockform.status = "Incoming"
            product = Products.objects.get(id=restockform.product.id)
            restockform.unit_price = product.unit_price

            try:
                product = Products.objects.get(id=restockform.product.id)
                get_product = Inventorys.objects.get(product_id=product.id)
                get_product.instock += restockform.quantity
                get_product.unit_price = product.unit_price
                get_product.save()

            except Inventorys.DoesNotExist:
                product = Products.objects.get(id=restockform.product.id)
                Inventorys.objects.create(
                    product_id=product, instock=restockform.quantity, unit_price=product.unit_price)
            restockform.save()
            return redirect('partytree:manage_restock')

    else:
        form = RestockForm()

    template = 'partytree/restock.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def manage_restock(request):
    restock = Inventory_recordss.objects.all()

    template = 'partytree/manage_restock.html'

    context = {
        'restock': restock,
    }

    return render(request, template, context)


@login_required
def manage_damages(request):
    damage = Damagess.objects.all()

    template = 'partytree/manage_damages.html'

    context = {
        'damage': damage,
    }

    return render(request, template, context)


@login_required
def create_damage(request):
    if request.method == 'POST':
        form = DamageForm(request.POST)
        if form.is_valid():
            damageform = form.save()

            try:
                product = Products.objects.get(id=damageform.product_id.id)
                get_product = Inventorys.objects.get(product_id=product.id)
                get_product.outgoing += damageform.quantity
                get_product.save()
                cost = product.unit_price * damageform.quantity
                Inventory_recordss.objects.create(
                    product=product, quantity=damageform.quantity, unit_price=product.unit_price, status="Outgoing")
                try:
                    code = Account_code.objects.get(code="Damages")
                except Account_code.DoesNotExist:
                    code = Account_code.objects.create(code="Damages")
                company = Company_group.objects.get(name="Party Tree")
                pv = Pv.objects.create(
                    account_code=code, company=company, description="Cost of Damages From Party Tree", amount=cost, status="approved")
                pv_detail = Pv_details.objects.create(
                    pv=pv, description=pv.description, amount=pv.amount)
                Expenditure.objects.create(
                    account_code=code, amount=cost, damage=damageform, company=company)

            except Inventorys.DoesNotExist:
                pass

            return redirect('partytree:manage_damages')

    else:
        form = DamageForm()

    template = 'partytree/damages.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def manage_inventory(request):
    inventory = Inventorys.objects.all()

    template = 'partytree/manage_inventory.html'

    context = {
        'inventory': inventory,
    }

    return render(request, template, context)


@login_required
def closing_stock(request):
    inventorys = Inventorys.objects.all()
    for inventory in inventorys:
        product = Products.objects.get(id=inventory.product_id.id)
        print(product)
        Closing_stockss.objects.create(
            product=product, closing_stock=inventory.avialable_stock, avialable_stock_cost=inventory.avialable_stock_cost)
    messages.success(request, 'Stock Closed')
    return redirect('partytree:manage_inventory')


@login_required
def closed_stock(request):
    close_stock = Closing_stockss.objects.all().order_by('-id')
    template = 'partytree/closedstock.html'

    context = {
        'close_stock': close_stock,
    }
    return render(request, template, context)

def EditInventory(request, pk):
    product_inventory = Inventorys.objects.get(pk=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data['quantity']
            product_inventory.outgoing += int(qty)
            product_inventory.save()
            messages.success(request, "Inventory Updated")
            return redirect('partytree:EditInventory', pk=product_inventory.id)
    else:
        form = InventoryForm()
    template = 'partytree/updateinventory.html'
    context = {
        'form': form,
        'product_inventory': product_inventory
    }
    return render(request, template, context)

