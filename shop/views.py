from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import CustomerCreationForm, OrderEnquiryForm
from .models import OrderEnquiry


def home(request):
    return render(request, 'shop/home.html')


def products(request):
    return render(request, 'shop/products.html')


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == 'POST':
        form = OrderEnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            if request.user.is_authenticated:
                enquiry.customer = request.user
            enquiry.save()
            messages.success(request, 'Thank you! Your order enquiry has been received. We will contact you shortly.')
            return redirect(f"{reverse('contact')}#order-form")
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['customer_name'] = request.user.get_full_name() or request.user.get_username()
            initial['email'] = request.user.email
        form = OrderEnquiryForm(initial=initial)
    return render(request, 'shop/contact.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.user.is_authenticated:
        return redirect('account')

    form = CustomerCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Your account has been created.')
        return redirect('account')
    return render(request, 'registration/register.html', {'form': form})


@login_required
def account(request):
    enquiries = OrderEnquiry.objects.filter(customer=request.user)
    return render(request, 'shop/account.html', {'enquiries': enquiries})