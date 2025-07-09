# Gemini Prompt File for Nairaxi Django Project

## General Instructions
- **Framework:** Django 5.x
- **Frontend:** Tailwind CSS v3
- **Primary Database:** PostgreSQL (or SQLite for development)
- **Primary UI Library:** None (custom components with Tailwind)
- **JavaScript Libraries:** GSAP for animations
- **Project Structure:**
    - Project config: `config/`
    - Apps directory: `apps/`
    - Main apps: `core`, `accounts`, `vehicles`, `leasing`
    - Templates are namespaced within each app (e.g., `apps/vehicles/templates/vehicles/vehicle_list.html`).
- **Goal:** Create a modern, responsive, and high-performance car leasing web application for a Nigerian audience.


### **SAFETY & WORKFLOW RULES:**
1.  **One Logical Step at a Time:** Each prompt will focus on a single, atomic task. Do not chain unrelated tasks (e.g., do not install a package AND modify templates in the same step).
2.  **No Destructive Operations without Explicit Confirmation:** Never delete files (`rm`, `del`), directories (`rmdir`), or the database (`db.sqlite3`) unless explicitly instructed in the prompt with the phrase "CONFIRMED_DELETE".
3.  **Prioritize Fixing Errors:** If a command fails, the immediate next step must be to analyze the error and propose a direct fix for that error only. Do not attempt to fix the error and then proceed with a new, unrelated task.
4.  **Migrations Require Confirmation:** Do not run `makemigrations` or `migrate` unless the prompt is specifically about a model change. Always ask for confirmation before running a migration that could alter the database schema significantly.
5.  **Always Verify Dependencies First:** Before adding a feature that requires a new library (like `django-allauth`), the first step must be to install the library (`pip install ...`) and add it to `requirements.txt`. Only after that succeeds should code modifications be made.
6.  **Configuration Before Usage:** When introducing a new feature that needs configuration in `settings.py` (e.g., a custom form class), the code for that feature (the form itself) must be created *before* the setting is applied. Propose creating the file first, then updating `settings.py`.
7.  **Explain Your Plan:** Before executing a multi-step solution (like a complex migration fix), briefly outline the plan in plain English first. For example: "Plan: 1. Delete old migration files. 2. Re-run makemigrations. 3. Run migrate."

---
...

---
## 1. Django Model Generation

### @gemini: create_vehicle_model
Create a Django model named `Vehicle` in an app called `vehicles`.
It should have fields for:
- A ForeignKey to `VehicleModel` (which links to `VehicleMake`).
- A ForeignKey to `VehicleCategory`.
- `year` (PositiveIntegerField).
- `color`, `license_plate`, `engine_details` (CharFields).
- `fuel_type` and `transmission` (CharField with choices: Petrol/Diesel/Electric/Hybrid and Automatic/Manual).
- `description` (TextField).
- A ManyToManyField to a `VehicleFeature` model.
- `daily_rate_ngn`, `weekly_rate_ngn`, `monthly_rate_ngn` (DecimalFields).
- `main_image` (ImageField).
- `availability_status` (CharField with choices: Available, Leased, Maintenance).
- `is_published` and `is_featured` (BooleanFields).
- A `slug` field that auto-generates from the make, model, and year.
- Include a `get_absolute_url` method pointing to a `vehicles:vehicle_detail` URL pattern.

### @gemini: create_lease_payment_models
Create two Django models in an app called `leasing`: `LeaseApplication` and `Payment`.
- **`LeaseApplication`** should link to `settings.AUTH_USER_MODEL` and `Vehicle`. It needs fields for `start_date`, `end_date`, `status` (with choices), document uploads (`FileField`), and `initial_payment_due` (`DecimalField`). It should have a `save()` method that calculates the initial payment due upon creation.
- **`Payment`** should link to `LeaseApplication`. It needs fields for `amount`, `email`, a unique `reference` (auto-generated using Python's `secrets` module), `status` (with choices), and optional fields for `paystack_charge_id` and `paid_at`.

---
## 2. Django Form Generation

### @gemini: create_lease_application_form
Create a Django `ModelForm` named `LeaseApplicationForm` for the `Leasing` app.
The form should be based on the `LeaseApplication` model and include the following fields: `start_date`, `end_date`, `drivers_license`, `identification_document`, and `terms_agreed`.
- For `start_date` and `end_date`, use a `DateInput` widget with `type='date'` to enable the browser's native date picker.
- For `drivers_license` and `identification_document`, use a `FileInput` widget.
- For `terms_agreed`, use a `CheckboxInput`.
- Style the widgets with appropriate Tailwind CSS classes.

### @gemini: create_vehicle_filter_form
Create a Django Form named `VehicleFilterForm` for the `vehicles` app.
It should not be a ModelForm.
Include the following fields for filtering:
- `keywords`: A non-required CharField for text search.
- `location`: A non-required `ModelChoiceField` for the `Location` model, with an empty label "All Locations".
- `property_type`: A non-required `ModelChoiceField` for the `VehicleCategory` model, with an empty label "All Types".
- `price_range`: A non-required `ChoiceField` with options for price ranges (e.g., '0-50000000', '50000001-100000000').
- `ordering`: A non-required `ChoiceField` for sorting options like 'Newest First', 'Price: Low to High', 'Price: High to Low'.
Style all fields with appropriate Tailwind CSS classes for form inputs.

---
## 3. Django View Generation

### @gemini: create_vehicle_list_view
Generate a Django function-based view named `vehicle_list_view` for the `vehicles` app.
The view should:
1.  Fetch all `is_published=True` `Vehicle` objects.
2.  Instantiate the `VehicleFilterForm` with `request.GET` data.
3.  If the form is valid, filter the initial queryset based on `keywords` (searching title, description, make, model), `location`, `property_type`, and `price_range`.
4.  Apply ordering to the queryset based on the `ordering` form field, defaulting to newest first.
5.  Implement Django's `Paginator` with 9 items per page.
6.  Handle `PageNotAnInteger` and `EmptyPage` exceptions.
7.  Pass the paginated `vehicles`, the `filter_form`, and any applied filter values to the `vehicles/vehicle_list.html` template.

### @gemini: create_paystack_payment_views
Generate a complete set of Django function-based views in `apps/leasing/views.py` to handle Paystack payments using the `requests` library.
This should include:
1.  **`initiate_payment` view:**
    - Requires login and takes a `LeaseApplication` ID.
    - Fetches the application, checks if it's approved.
    - Creates or gets a pending `Payment` record with a unique reference.
    - Renders a `make_payment.html` template, passing the payment object and `PAYSTACK_PUBLIC_KEY` in the context.
2.  **`verify_payment` view:**
    - Requires login and takes a `reference` string from the URL.
    - Makes a server-to-server API call to Paystack's transaction verification endpoint.
    - Securely checks if the transaction status is `success` and if the amount paid matches the amount in the database.
    - If verification passes, update the status of the `Payment`, `LeaseApplication`, and `Vehicle` models.
    - Uses Django's messages framework for success or failure feedback and redirects appropriately.
    - Includes robust error handling for API connection issues or failed payments.
3. **`payment_success` and `payment_failed` views:** Simple views that render static confirmation pages.

---
## 4. Template & UI Generation

### @gemini: create_hero_with_video_bg
Generate the HTML and CSS for a hero section using Tailwind CSS for the Nairaxi homepage.
The hero section should:
- Have a full-screen video background that autoplays, is muted, and loops. The video should cover the entire area.
- Include a dark gradient overlay on top of the video to ensure text readability.
- Display a left-aligned content block with:
  - A large, multi-line headline (e.g., "Premium Car Leasing Solutions").
  - A smaller sub-headline.
  - A descriptive paragraph.
  - A prominent call-to-action button (e.g., "Explore Our Fleet").
- Use placeholder classes like `gsap-h-line`, `gsap-hero-subheadline` for GSAP animation targets.

### @gemini: create_vehicle_card_partial
Generate the HTML for a reusable Django template partial named `partials/vehicle_card_nairaxi.html`.
It should render a single vehicle card using a `vehicle` object passed in the context.
The card should be responsive and styled with Tailwind CSS, including:
- An image with a 16:9 aspect ratio that zooms slightly on hover (using `group` and `group-hover`).
- A category badge.
- The vehicle title (Make, Model, Year) as a link to the detail page.
- A truncated description.
- The daily lease rate.
- A "Lease Now" or "View Details" button.

### @gemini: create_paystack_payment_template
Generate the HTML for a `make_payment.html` template. It should:
- Display a summary of the payment, including the vehicle name, amount, and reference, using context variables from a `payment` object.
- Include a "Pay Now" button.
- Contain the necessary JavaScript to trigger the Paystack Inline Popup using `PaystackPop.setup()`.
- The JavaScript should use the `paystack_public_key`, `payment.email`, `payment.amount`, and `payment.reference` from the Django context.
- After a successful transaction, it should use the `callback` function to redirect the user to a `leasing:verify_payment` URL, passing the transaction reference.

---
## 5. JavaScript & Animation

### @gemini: create_gsap_hero_animation
Generate a JavaScript snippet that uses GSAP to create an intro animation for the hero section text.
The script should be wrapped in a `DOMContentLoaded` event listener.
It must:
1.  Create a GSAP timeline.
2.  Animate the headline (targeting `.gsap-h-line`), sub-headline (`.gsap-hero-subheadline`), description (`.gsap-hero-description`), and CTA button (`.gsap-hero-cta`).
3.  The animations should be a "fade in and slide up" effect (`from({ opacity: 0, y: ... })`).
4.  The animations should be staggered and sequenced for a smooth, professional reveal.

---
## 6. Project Maintenance & Troubleshooting

### @gemini: fix_allauth_migration_conflict
My Django project server is broken after attempting to add `django-allauth`. I have an `InconsistentMigrationHistory` error, and other modules may be missing or misconfigured. I want to reset the database and migrations to fix this.

**SAFETY RULE:** This prompt includes "CONFIRMED_DELETE" which authorizes database and migration file deletion for this specific task.

**Execution Plan:**
1.  Ensure the `django-allauth` library and its dependencies (`cryptography`, `PyJWT`) are installed.
2.  In `config/settings.py`, fix any deprecated `django-allauth` settings and ensure `'allauth'`, `'allauth.account'`, `'allauth.socialaccount'`, and `'allauth.socialaccount.providers.google'` are in `INSTALLED_APPS`. Also ensure `'django.contrib.sites'` is present and `SITE_ID = 1`.
3.  Comment out the `ACCOUNT_SIGNUP_FORM_CLASS` setting in `settings.py` for now to allow initial migrations to run with defaults.
4.  **CONFIRMED_DELETE:** Delete the `db.sqlite3` database file.
5.  **CONFIRMED_DELETE:** Delete the `migrations` directory inside *all* of my custom apps (`core`, `accounts`, `vehicles`, `leasing`).
6.  Run `python manage.py makemigrations` for all apps to create a fresh set of migration files.
7.  Run `python manage.py migrate` to create a new database with a clean, consistent migration history.
8.  Create a new superuser when prompted.
9.  After migrations succeed, create a new `CustomSignupForm` in `apps/accounts/forms.py` that inherits from `allauth.account.forms.SignupForm` and properly handles saving the user's email.
10. Finally, uncomment and verify the `ACCOUNT_SIGNUP_FORM_CLASS` setting in `settings.py` to point to the new custom form.