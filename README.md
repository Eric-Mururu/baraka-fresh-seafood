# Baraka Fresh Seafood

A Django website for a fictional seafood supplier in Watamu, Kenya, built with HTML, CSS and Bootstrap. All business details and prices are sample content.

## Set up locally

1. Create and activate a Python virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Apply database migrations with `python manage.py migrate`.
4. Create an administrator with `python manage.py createsuperuser`.
5. Start the development server with `python manage.py runserver`.

Open the site at `http://127.0.0.1:8000/`. The admin dashboard is at `http://127.0.0.1:8000/admin/` and requires an administrator account.

## Creating a manager account

The public registration form creates customer accounts only. To give someone access to manage enquiries:

1. Create an initial administrator with `python manage.py createsuperuser` if you have not already done so.
2. Sign in to `http://127.0.0.1:8000/admin/` with that administrator account.
3. Under **Groups**, create a group (for example, `Managers`) and grant it the **view** and **change** permissions for **Shop | order enquiry**.
4. Under **Users**, add the manager's account, mark it **Active** and **Staff status**, leave **Superuser status** unchecked, and assign the `Managers` group.
5. The manager can then sign in at `http://127.0.0.1:8000/admin/` with the username and password you created.

Use the customer-facing `/account/login/` page for customer accounts; manager access to the admin dashboard is through `/admin/`.

## Customer features

- Register an account, log in, and log out from the main navigation.
- Submit an order enquiry as a guest or while signed in.
- Signed-in customers can review their own enquiries and whether each has been reviewed.
- Administrators can search, filter, and update enquiries in the branded admin dashboard.

Run the automated checks with `python manage.py check` and `python manage.py test`.