# Mnka Cleaning Services

A Django platform for booking cleaning services online, with separate
sign-up flows for customers and cleaners, an admin-driven verification
workflow for cleaners, and a booking/status/review pipeline.

## Apps

- **accounts** — custom user model (customer / cleaner / admin roles), auth
- **services** — the service catalog (categories + bookable services)
- **cleaners** — cleaner profiles, verification, service areas, availability
- **bookings** — booking requests and their status workflow
- **reviews** — post-job ratings, feeds into a cleaner's average rating
- **payments** — Paynow (card/bank + EcoCash) payments tied to bookings

## Run locally with Docker (recommended)

```bash
cp .env.example .env
# edit .env and set a real DJANGO_SECRET_KEY and DB_PASSWORD

docker compose up --build
```

The app will be available at http://localhost:8000

Create an admin user and seed the service catalog (from the flyer's
service categories) in a second terminal:

```bash
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py seed_services
```

Then visit http://localhost:8000/admin/ to review cleaner sign-ups,
verify cleaners, and manage bookings and services.

## Run locally without Docker (quick dev loop)

```bash
python -m venv venv
source venv/bin/activate         # venv\Scripts\activate on Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py seed_services
python manage.py runserver
```

Without `DB_NAME` set, settings.py falls back to SQLite automatically,
so no Postgres install is needed for local development.

## Key flows

- `/` — marketing home page
- `/accounts/signup/` — choose customer or cleaner signup
- `/services/` — browse the service catalog
- `/bookings/new/` — logged-in customer requests a booking
- `/bookings/my-bookings/` — customer's booking history + leave reviews
- `/cleaners/onboarding/` — cleaner completes their profile (bio, ID doc, services offered)
- `/cleaners/dashboard/` — cleaner sees upcoming jobs and updates status
- `/admin/` — verify cleaners, manage services/categories, oversee all bookings

## Booking status flow

`pending → confirmed → in_progress → completed`, with `cancelled`
reachable from `pending`, `confirmed`, or `in_progress`. Transitions
are validated in `Booking.set_status()` — invalid jumps raise a
`ValidationError` instead of silently corrupting state.

## Notes on going to production

- Set `DJANGO_DEBUG=False`, a strong `DJANGO_SECRET_KEY`, and real
  `DJANGO_ALLOWED_HOSTS` / `DJANGO_CSRF_TRUSTED_ORIGINS` in `.env`.
- Static files are served by WhiteNoise directly from the `web`
  container — fine at small scale. For higher traffic, put nginx (or
  a CDN) in front of `web` and let it serve `/static/` and `/media/`
  directly from the shared volumes.
- Notifications (SMS/email on booking updates) via Celery + Redis
  aren't wired in yet — models are structured so this slots in cleanly.

## Design

Colors and layout are built from the Mnka flyer: navy `#002b88` and
green `#93c31e`, "Baloo 2" for headlines paired with "Inter" for body
text. All tokens live at the top of `static/css/main.css` — change
them there to re-theme the whole site. Icons are inline SVG, generated
by a small template tag (`mnka_platform/templatetags/icons.py`) so
they inherit color from their container with no extra image requests.

Note: `mnka_platform` (the project package) is deliberately listed in
`INSTALLED_APPS` — that's what makes its `templatetags` discoverable.
It has no models and needs none.

## Payments (Paynow)

Card/bank and EcoCash payments go through [Paynow](https://paynow.co.zw),
Zimbabwe's payment gateway, via the official `paynow` Python SDK.

1. Get an `integration_id` and `integration_key` from your Paynow
   merchant dashboard (they also issue a sandbox pair for testing
   before you go live).
2. Set `PAYNOW_INTEGRATION_ID` and `PAYNOW_INTEGRATION_KEY` in `.env`.
3. That's it — the "Pay now" button on a customer's booking lets them
   choose card/bank (redirects to Paynow's hosted checkout) or EcoCash
   (sends a USSD prompt to their phone). A booking is automatically
   moved from `pending` to `confirmed` once Paynow confirms payment,
   whether that happens via the `payments:result` webhook (Paynow
   calls this server-to-server) or the "check status" fallback button.

The webhook re-verifies status directly against Paynow's API using the
stored poll URL rather than trusting the raw callback body, since that
body can be spoofed.

To add another gateway (Stripe, for card payments outside Zimbabwe),
add a sibling to `payments/paynow_client.py` and a `Method` choice on
`Payment` — the model and views don't assume Paynow specifically.

## Cloud storage for cleaner documents

By default, uploads (cleaner ID documents, profile photos) are stored
on local disk under `media/` — nothing to configure.

To use cloud storage instead (recommended once you're handling real ID
documents in production), set in `.env`:

```
USE_S3=True
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=...
AWS_S3_REGION_NAME=us-east-1
```

This works with real AWS S3. For an S3-compatible provider instead
(DigitalOcean Spaces, Backblaze B2, etc.), also set
`AWS_S3_ENDPOINT_URL` to that provider's endpoint.

Two storage classes are used (`mnka_platform/storage_backends.py`):
- **Public** — profile photos; publicly readable.
- **Private** — cleaner ID documents (`CleanerProfile.id_document`);
  never public. Every `.url` access generates a signed link that
  expires after an hour, and is only reachable to someone Django has
  already authorized (e.g. staff viewing it in `/admin/`).

