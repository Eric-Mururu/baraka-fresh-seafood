from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import OrderEnquiryForm


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
            form.save()
            messages.success(request, 'Thank you! Your order enquiry has been received. We will contact you shortly.')
            return redirect(f"{reverse('contact')}#order-form")
    else:
        form = OrderEnquiryForm()
    return render(request, 'shop/contact.html', {'form': form})