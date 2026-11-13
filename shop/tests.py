from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import OrderEnquiry


class CustomerAccountTests(TestCase):
    def setUp(self):
        self.registration_data = {
            'username': 'freshbuyer',
            'email': 'fresh@example.com',
            'password1': 'Seafood-strong-715!',
            'password2': 'Seafood-strong-715!',
        }

    def enquiry_data(self, **overrides):
        data = {
            'customer_name': 'Fresh Buyer',
            'phone': '0700000000',
            'email': 'fresh@example.com',
            'customer_type': 'Household',
            'product': 'Red Snapper',
            'quantity_kg': 2,
            'delivery_location': 'Watamu',
            'preferred_date': (timezone.localdate() + timedelta(days=1)).isoformat(),
            'notes': '',
        }
        data.update(overrides)
        return data

    def create_enquiry(self, customer, **overrides):
        data = self.enquiry_data(**overrides)
        return OrderEnquiry.objects.create(customer=customer, **data)

    def test_customer_can_register_log_in_and_log_out(self):
        response = self.client.post(reverse('register'), self.registration_data)

        self.assertRedirects(response, reverse('account'))
        customer = get_user_model().objects.get(username='freshbuyer')
        self.assertEqual(customer.email, 'fresh@example.com')
        self.assertTrue(customer.check_password(self.registration_data['password1']))
        self.assertEqual(int(self.client.session['_auth_user_id']), customer.pk)

        self.client.post(reverse('logout'))
        self.assertNotIn('_auth_user_id', self.client.session)

        response = self.client.post(reverse('login'), {
            'username': 'freshbuyer',
            'password': self.registration_data['password1'],
        })
        self.assertRedirects(response, reverse('account'))

    def test_registration_rejects_an_existing_email_address(self):
        get_user_model().objects.create_user(
            username='existing',
            email='fresh@example.com',
            password='Another-strong-934!',
        )

        response = self.client.post(reverse('register'), self.registration_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'An account with this email address already exists.')
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_account_requires_login_and_only_shows_the_signed_in_customers_enquiries(self):
        response = self.client.get(reverse('account'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('account')}")

        customer = get_user_model().objects.create_user(
            username='customer',
            email='customer@example.com',
            password='Another-strong-934!',
        )
        other_customer = get_user_model().objects.create_user(
            username='another',
            email='another@example.com',
            password='Another-strong-935!',
        )
        self.create_enquiry(customer, product='Red Snapper')
        self.create_enquiry(other_customer, product='Kingfish', customer_name='Private Customer')
        self.client.force_login(customer)

        response = self.client.get(reverse('account'))

        self.assertContains(response, 'Red Snapper')
        self.assertNotContains(response, 'Kingfish')
        self.assertNotContains(response, 'Private Customer')

    def test_signed_in_enquiry_is_saved_to_customer_account(self):
        customer = get_user_model().objects.create_user(
            username='customer',
            email='customer@example.com',
            password='Another-strong-934!',
        )
        self.client.force_login(customer)

        response = self.client.post(reverse('contact'), self.enquiry_data())

        self.assertRedirects(response, f"{reverse('contact')}#order-form")
        enquiry = OrderEnquiry.objects.get()
        self.assertEqual(enquiry.customer, customer)

    def test_guest_enquiry_remains_unlinked_to_an_account(self):
        response = self.client.post(reverse('contact'), self.enquiry_data())

        self.assertRedirects(response, f"{reverse('contact')}#order-form")
        self.assertIsNone(OrderEnquiry.objects.get().customer)


class AdminDashboardTests(TestCase):
    def test_admin_dashboard_uses_project_brand_and_enquiry_summary(self):
        admin_user = get_user_model().objects.create_superuser(
            username='siteadmin',
            email='admin@example.com',
            password='Another-strong-936!',
        )
        OrderEnquiry.objects.create(
            customer_name='Dashboard Customer',
            phone='0700000000',
            customer_type='Household',
            product='Tilapia',
            quantity_kg=2,
            delivery_location='Watamu',
            preferred_date=timezone.localdate() + timedelta(days=1),
        )
        self.client.force_login(admin_user)

        response = self.client.get(reverse('admin:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Operations dashboard')
        self.assertContains(response, 'Dashboard Customer')
        self.assertContains(response, 'Awaiting review')
        self.assertContains(response, 'Baraka Fresh Seafood')
