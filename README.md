# CareNest 🏠

**A full-stack care management platform built with Python and Django**

CareNest is an end-to-end operational tool that connects families, carers, and administrators through a single platform — handling everything from carer onboarding and compliance tracking to booking management and role-based dashboards.

Built independently as a solo project to demonstrate full-stack data engineering and tool development skills.

---

## What it does

CareNest solves a real operational problem in the care sector: the fragmented, paper-heavy workflows that slow down onboarding, compliance checks, and booking management.

**For administrators:**
- Dashboard showing all carers, compliance status, and document expiry alerts
- Onboarding workflow for new carers with DBS and Right-to-Work document tracking
- Automated alerts when documents are approaching expiry
- Booking management and shift scheduling across multiple clients

**For carers:**
- Personal profile management
- View and manage upcoming bookings
- Upload compliance documents (DBS, Right-to-Work, qualifications)
- Track document expiry dates

**For families / clients:**
- Search for available carers by postcode
- View carer profiles and qualifications
- Submit and manage care booking requests

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Django |
| Database | SQLite (development) |
| Frontend | HTML5, CSS3, JavaScript |
| Auth | Django built-in authentication + role-based access control |
| Version control | Git, GitHub |

---

## Key features

- **Role-based access control** — Three distinct user roles (admin, carer, family) each with their own dashboard and permissions
- **Compliance tracking** — Automated document expiry monitoring with dashboard alerts; DBS and Right-to-Work status visible at a glance
- **Postcode-based search** — Families can search for carers available in their area
- **Booking system** — End-to-end booking workflow from request through confirmation and scheduling
- **Onboarding pipeline** — Structured carer onboarding with document upload, verification status, and admin sign-off
- **Admin reporting** — Aggregate views of carer availability, compliance rates, and booking volumes

---

## Data & compliance design

The platform was designed with data quality and regulatory compliance in mind:

- All compliance documents (DBS, Right-to-Work) have expiry tracking with automated status flags
- Role-based access ensures sensitive data is only visible to authorised users
- Booking records maintain a full audit trail
- Data validation enforced at both form and model level

---

## Project structure

```
carenest/
├── accounts/          # User auth, registration, role management
├── carers/            # Carer profiles, compliance documents, availability
├── bookings/          # Booking requests, confirmation, scheduling
├── admin_portal/      # Admin dashboards, compliance reporting
├── search/            # Postcode-based carer search
├── templates/         # HTML templates for all views
├── static/            # CSS, JavaScript, images
└── carenest/          # Django project settings and URL routing
```

---

## Running locally

```bash
# Clone the repository
git clone https://github.com/anjujose06/carenest.git
cd carenest

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser (admin account)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

Then open `http://127.0.0.1:8000` in your browser.

---

## Skills demonstrated

This project was built to demonstrate end-to-end data tool development skills relevant to data analyst and data engineering roles:

- **Python** — Core application logic, data processing, automation
- **Django** — MVC architecture, ORM for database queries, form validation, authentication
- **SQL** — Underlying relational data model; complex queries via Django ORM
- **Data quality** — Validation checks, status flags, expiry monitoring, audit trails
- **Dashboard development** — Role-specific reporting views with aggregated metrics
- **Clean code practices** — Modular structure, documented functions, version-controlled throughout
- **End-to-end delivery** — Designed, built, and deployed as a complete working system

---

## About the developer

**Anju Jose** — MSc Data Science (Merit), University of Greenwich  
[LinkedIn](https://www.linkedin.com/in/anjujose06/) | [GitHub](https://github.com/anjujose06) | anjujose1106@gmail.com

Currently seeking junior data analyst / data engineer roles in the UK. Open to relocation to London.

---

*Built with Python 3 and Django · SQLite · Role-based access control · Postcode search · Compliance tracking*
