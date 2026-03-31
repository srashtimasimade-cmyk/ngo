# NGO Better Tomorrow - Development Guide

## 🚀 Project Overview

This is a production-ready Django web application for managing NGO operations. It features:
- Comprehensive data models for organizations, projects, members, and donations
- Beautiful responsive UI with Bootstrap 5
- Advanced admin interface with custom styling
- REST-like URLs with semantic slugs
- Full CRUD operations
- Advanced filtering and search

## 📂 Project Structure

```
ngo_project/
│
├── config/                          # Django Configuration
│   ├── __init__.py
│   ├── settings.py                 # Project settings (Database, apps, etc.)
│   ├── urls.py                     # Main URL routing
│   ├── wsgi.py                     # WSGI application
│   └── asgi.py                     # ASGI application
│
├── ngo_app/                         # Main Application
│   ├── migrations/                 # Database migrations
│   ├── __init__.py
│   ├── admin.py                    # Admin interface customization
│   ├── apps.py                     # App configuration
│   ├── forms.py                    # Django forms with Crispy Forms
│   ├── models.py                   # Database models (5 models)
│   ├── tests.py                    # Unit tests
│   ├── urls.py                     # App URL routing
│   └── views.py                    # View classes (16+ views)
│
├── templates/                       # HTML Templates
│   ├── base.html                   # Base template with navigation
│   └── ngo_app/
│       ├── dashboard.html          # Dashboard with statistics
│       ├── organization_list.html   # Organizations listing
│       ├── organization_detail.html # Organization profile
│       ├── organization_form.html   # Organization form
│       ├── project_list.html        # Projects with filtering
│       ├── project_detail.html      # Project profile
│       ├── project_form.html        # Project form
│       ├── member_list.html         # Team members listing
│       ├── member_detail.html       # Member profile
│       ├── member_form.html         # Member form
│       ├── donation_list.html       # Donations tracking
│       ├── donation_detail.html     # Donation profile
│       └── donation_form.html       # Donation form
│
├── static/                          # Static files
│   ├── css/                         # CSS files
│   │   └── style.css               # Custom styles
│   └── js/                          # JavaScript files
│       └── main.js                 # Custom scripts
│
├── manage.py                        # Django management script
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore file
├── README.md                        # README documentation
├── DATABASE_SCHEMA.md               # SQL schema documentation
└── DEVELOPMENT_GUIDE.md             # This file
```

## 🗄️ Database Models

### 1. Organization
Represents an NGO organization with complete information:
```python
- name, slug (unique)
- description, mission, vision
- email, phone, website
- address, city, state, country, postal_code
- registration_number (unique)
- established_date, status (active/inactive/pending)
- logo (image upload)
- timestamps (created_at, updated_at)
```

**Relationships:**
- One-to-Many: Members, Projects, Donations

### 2. Member
Team members, volunteers, and staff:
```python
- organization (FK)
- first_name, last_name, email (unique per org)
- phone, date_of_birth
- role (founder/director/coordinator/volunteer/donor)
- status (active/inactive/on_leave)
- profile_picture, bio, address
- joined_date
- timestamps
```

**Relationships:**
- Many-to-One: Organization
- One-to-Many: Projects (as lead)

### 3. Project
NGO initiatives and programs:
```python
- organization (FK)
- title, slug (unique), description, objective
- category (6 categories)
- status (planning/active/on_hold/completed/cancelled)
- start_date, end_date
- target_beneficiaries, budget, location
- lead_member (FK, optional)
- image
- timestamps
```

**Relationships:**
- Many-to-One: Organization, Member
- One-to-Many: Donations
- One-to-One: Impact

### 4. Donation
Financial and in-kind contributions:
```python
- organization (FK), project (FK, optional)
- donor_name, donor_email, donor_phone
- donation_type (monetary/in_kind/service)
- status (pending/received/cancelled)
- amount, currency (for monetary)
- description (for in-kind)
- donation_date, receipt_issued
- notes
- timestamps
```

**Relationships:**
- Many-to-One: Organization, Project

### 5. Impact
Project outcome and beneficiary tracking:
```python
- project (1:1)
- actual_beneficiaries, families_impacted
- children_benefited
- key_achievements, challenges_faced
- lessons_learned
- completion_percentage
- report_document, gallery_images (JSON)
- timestamps
```

**Relationships:**
- One-to-One: Project

## 🎨 View Structure

### Dashboard Views
- `dashboard()`: Main dashboard with statistics and recent items

### Organization Views
- `OrganizationListView`: List all organizations (paginated, searchable)
- `OrganizationDetailView`: Organization profile with statistics
- `OrganizationCreateView`: Create new organization (requires login)
- `OrganizationUpdateView`: Edit organization (requires login)

### Project Views
- `ProjectListView`: List projects with advanced filtering
- `ProjectDetailView`: Project profile with impact information
- `ProjectCreateView`: Create new project (requires login)
- `ProjectUpdateView`: Edit project (requires login)
- `ProjectDeleteView`: Delete project (requires login)
- `ProjectFilter`: Custom filter class for filtering projects

### Member Views
- `MemberListView`: List team members with role filtering
- `MemberDetailView`: Member profile with led projects
- `MemberCreateView`: Add team member (requires login)
- `MemberUpdateView`: Edit member info (requires login)

### Donation Views
- `DonationListView`: List donations with status/type filtering
- `DonationDetailView`: Donation profile
- `DonationCreateView`: Record new donation (requires login)
- `DonationUpdateView`: Edit donation (requires login)

## 🔐 Authentication & Permissions

- Public views: Dashboard, list views, detail views
- Protected views: Create, update, delete operations (LoginRequiredMixin)
- Admin interface: Full admin access with custom styling

## 🎨 Forms

### OrganizationForm
- All organization fields
- Crispy Forms with Bootstrap 5 layout
- Organized into fieldsets

### MemberForm
- Personal and role information
- Profile picture upload
- Crispy Forms layout

### ProjectForm
- Project details, timeline, budget
- Crispy Forms with organized sections

### DonationForm
- Donor information
- Flexible for different donation types
- Crispy Forms layout

## 📊 URL Patterns

```
/                           → Dashboard
/organizations/             → List organizations
/organizations/<slug>/      → Organization detail
/organizations/create/      → Create organization
/organizations/<slug>/edit/ → Edit organization

/projects/                  → List projects (with filters)
/projects/<slug>/          → Project detail
/projects/create/          → Create project
/projects/<slug>/edit/     → Edit project
/projects/<slug>/delete/   → Delete project

/members/                   → List members
/members/<pk>/             → Member detail
/members/create/           → Add member
/members/<pk>/edit/        → Edit member

/donations/                → List donations
/donations/<pk>/           → Donation detail
/donations/create/         → Record donation
/donations/<pk>/edit/      → Edit donation

/admin/                    → Django admin interface
```

## 🧪 Testing

Run tests with:
```bash
python manage.py test
python manage.py test ngo_app
python manage.py test ngo_app.tests.OrganizationModelTest
```

Test coverage includes:
- Model creation and validation
- Unique constraints
- URL resolution
- View rendering
- Admin interface

## 🔧 Admin Customization

### Organization Admin
- List display: Name, Status, Email, City, Created
- Filters: Status, Country, Date
- Search: Name, Email, Registration
- Fieldsets: Basic, Contact, Location, Registration

### Member Admin
- List display: Name, Organization, Role, Status, Email, Joined
- Filters: Status, Role, Organization
- Search: Name, Email, Phone
- Custom badges for roles

### Project Admin
- List display: Title, Organization, Category, Status, Budget
- Filters: Status, Category, Organization
- Search: Title, Description
- Custom styling with category tags

### Donation Admin
- List display: Donor, Organization, Type, Amount, Status, Date
- Bulk actions: Mark as received, Issue receipt
- Filters: Status, Type, Organization, Date
- Custom badge styling

## 🔍 SQL Queries

### Get Organization Statistics
```sql
SELECT o.name, COUNT(p.id) as projects, COUNT(m.id) as members
FROM ngo_app_organization o
LEFT JOIN ngo_app_project p ON o.id = p.organization_id
LEFT JOIN ngo_app_member m ON o.id = m.organization_id
GROUP BY o.id;
```

### Get Project Performance
```sql
SELECT p.title, p.target_beneficiaries, i.actual_beneficiaries,
       p.budget, SUM(d.amount) as funds_received
FROM ngo_app_project p
LEFT JOIN ngo_app_impact i ON p.id = i.project_id
LEFT JOIN ngo_app_donation d ON p.id = d.project_id
GROUP BY p.id;
```

## 📱 Responsive Design

- Mobile-first approach
- Bootstrap 5 grid system
- Responsive navigation bar
- Mobile-friendly forms
- Optimized for all screen sizes

## 🎨 Styling Features

- Modern gradient backgrounds
- Smooth transitions and hover effects
- Well-organized typography
- Color-coded status badges
- Icon integration with Bootstrap Icons
- Card-based layout

## 🚀 Deployment Checklist

- [ ] Set DEBUG = False
- [ ] Generate secure SECRET_KEY
- [ ] Configure allowed hosts
- [ ] Set up PostgreSQL database
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Configure email backend
- [ ] Set up logging
- [ ] Configure CORS headers if needed
- [ ] Set up SSL/HTTPS
- [ ] Configure domain name
- [ ] Deploy with Gunicorn/uWSGI

## 📦 Performance Optimization

- Database indexes on frequently filtered fields
- Optimized queries with select_related and prefetch_related
- Paginated lists (10-20 items per page)
- Caching ready (can add @cache_page decorator)
- CDN ready for static files

## 🔄 Common Tasks

### Add a new field to a model:
1. Add field to model in `models.py`
2. Run: `python manage.py makemigrations`
3. Run: `python manage.py migrate`
4. Update forms and templates

### Add a new view:
1. Create view class in `views.py`
2. Add URL pattern in `urls.py`
3. Create template
4. Test in Django shell or browser

### Customize admin interface:
1. Edit admin.py
2. Create ModelAdmin class
3. Customize list_display, list_filter, search_fields
4. Add custom actions if needed

## 🐛 Debugging

Enable debug toolbar:
```bash
pip install django-debug-toolbar
# Add to INSTALLED_APPS
# Add middleware in settings
```

View SQL queries:
```python
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as context:
    # Your code here
    print(context.captured_queries)
```

## 📝 Code Style

- PEP 8 compliant
- Docstrings for all classes and complex functions
- Type hints recommended
- 80-character line limit for readability

## 🔗 Useful Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.0/)
- [Django Crispy Forms](https://django-crispy-forms.readthedocs.io/)
- [Bootstrap Icons](https://icons.getbootstrap.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 📞 Support

For issues or questions:
1. Check the README.md
2. Review DATABASE_SCHEMA.md for data structure
3. Check inline code comments
4. Run tests to identify issues
5. Check Django logs for errors

---

**Happy coding! 💚**
