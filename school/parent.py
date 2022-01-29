from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .forms import *
from .models import *
from .filters import *
from .utils import *
import datetime


@login_required
def parentdashboard(request):
    parent = Parents.objects.get(id=request.user.username)
    child = Students.objects.filter(parent_id=parent.id)
    ord = Billing.objects.filter(parent_id=parent.id).order_by('-id')
    children = child.count()
    fees = ord.aggregate(cc=Sum('total'))
    fees_paid = ord.aggregate(ff=Sum('amount_paid'))

    if fees['cc'] and not fees_paid['ff']:
        current_bill = fees['cc']
    elif not fees['cc'] and fees_paid['ff']:
        current_bill= fees_paid['ff']
    elif not fees['cc'] and not fees_paid['ff']:
        current_bill = 0.00
    else:
        current_bill = fees['cc']-fees_paid['ff']

    context={
        'parent':parent,
        'ord': ord,
        'children': children,
        'fees':fees,
        'fees_paid': fees_paid,
        'current_bill': current_bill,
        'child': child,
    }

    template ='hod_template/parentdashboard.html'
    return render(request,template,context)


@login_required
def parentbill(request,pk):
    # studbill = StudentBill.objects.get(id=pk)
    stud = Students.objects.get(id=pk)
    # bb = Bills.objects.get(id=stud.course)
    bill = Bills.objects.filter(
        class_id=stud.course_id)

    context = {
        'bill': bill,
        # 'arres': arres,
        # 'studbill': studbill,
    }

    template='hod_template/manage_bill.html'
    return render(request,template)


@login_required
def child_results(request):
    attendance_list = studenthistory.objects.filter(
        parent_id=request.user.username).order_by('-results')
    context = {
        'academic_term': attendance_list,
    }

    template = 'staff_template/manage_resultss.html'
    return render(request, template, context)


def parentdailyreport(request):
    rep = DailyClassReportDetails.objects.filter(status='approved',
        parent_id=request.user.username).order_by('-id')
    template = 'hod_template/view_dailyreport.html'
    context = {
        'rep': rep,
    }
    return render(request, template, context)
