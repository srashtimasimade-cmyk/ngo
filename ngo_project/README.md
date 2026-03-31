# NGO Better Tomorrow - Django Project

A comprehensive Django web application for managing NGO (Non-Governmental Organization) operations, including projects, members, donations, and impact tracking.

## 🎯 Features

### Core Functionality
- **Organization Management**: Create and manage multiple NGO organizations
- **Project Management**: Track projects with budgets, timelines, and beneficiary targets
- **Team Management**: Manage volunteers and staff members with roles and status
- **Donation Tracking**: Record monetary and in-kind donations
- **Impact Reports**: Track project outcomes and beneficiary impact
- **Admin Dashboard**: Beautiful statistics and quick access to key metrics

### Technical Features
- Class-based views for clean, reusable code
- Advanced filtering and search capabilities
- Responsive Bootstrap 5 design
- Crispy Forms for elegant form rendering
- PostgreSQL/SQLite database support
- Admin interface with custom actions
- User authentication and permissions
- Pagination for large datasets

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Virtual environment

### Installation

1. **Clone or extract the project**
```bash
cd ngo_project
```

2. **Create virtual environment**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create environment file** (`.env`)
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=sqlite3
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

Access the application at `http://localhost:8000`

## 📁 Project Structure

```
ngo_project/
├── config/                 # Django configuration
│   ├── settings.py        # Project settings
│   ├── urls.py            # URL configuration
│   └── wsgi.py            # WSGI configuration
├── ngo_app/               # Main Django app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Django forms
│   ├── urls.py            # App URLs
│   ├── admin.py           # Admin configuration
│   └── apps.py            # App configuration
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   └── ngo_app/           # App templates
├── static/                # Static files (CSS, JS)
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## 📊 Database Models

### Organization
- Name, slug, description
- Mission and vision statements
- Contact information (email, phone, website)
- Location details
- Registration number and establishment date

### Member
- First name, last name, email, phone
- Role (Founder, Director, Coordinator, Volunteer, Donor)
- Status (Active, Inactive, On Leave)
- Date of birth, profile picture
- Biography and address

### Project
- Title, slug, description, objective
- Category (Education, Health, Environment, etc.)
- Status (Planning, Active, On Hold, Completed, Cancelled)
- Timeline (start date, end date)
- Budget and target beneficiaries
- Location and lead member

### Donation
- Donor information
- Donation type (Monetary, In-Kind, Service)
- Amount and currency
- Status (Pending, Received, Cancelled)
- Receipt tracking

### Impact
- Actual beneficiaries and families impacted
- Key achievements and challenges
- Completion percentage
- Report document and gallery

## 🎨 Features Highlight

### Admin Interface
- Beautiful styled admin panel with custom badges
- Color-coded status indicators
- Bulk actions for efficient management
- Custom filters and search
- Inline editing

### Dashboard
- Key statistics overview
- Recent projects and donations
- Quick action buttons
- Visual metrics display

### Project Management
- Advanced filtering by category and status
- Search functionality
- Project cards with key metrics
- Budget and beneficiary display
- Status indicators

## 🔐 Security

- CSRF protection enabled
- SQL injection prevention (ORM queries)
- XSS protection
- Secure password hashing
- User authentication required for create/edit/delete operations
- Environment-based configuration

## 🔧 Configuration

### Database

For SQLite (Development):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

For PostgreSQL (Production):
```env
DB_ENGINE=postgresql
DB_NAME=ngo_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Static Files
```bash
python manage.py collectstatic
```

## 📝 Usage Examples

### Create an Organization
1. Navigate to Admin panel
2. Click "Add Organization"
3. Fill in organization details
4. Save

### Add a Project
1. Go to Projects > New Project
2. Fill in project details
3. Select category and status
4. Set timeline and budget
5. Save

### Record a Donation
1. Navigate to Donations
2. Click "New Donation"
3. Enter donor information
4. Select donation type and amount
5. Submit

## 🐛 Troubleshooting

### Migrations Issues
```bash
# Reset migrations (development only)
python manage.py migrate ngo_app zero
python manage.py migrate ngo_app
```

### Missing Dependencies
```bash
# Reinstall all requirements
pip install --upgrade -r requirements.txt
```

### Static Files Not Loading
```bash
# Rebuild static files
python manage.py collectstatic --clear --no-input
```

## 📦 Dependencies

- **Django 4.2.11**: Web framework
- **Crispy Forms 2.1**: Form rendering
- **Bootstrap 5**: Frontend framework
- **Pillow 10.1**: Image handling
- **Django Filter 23.5**: Query filtering
- **PostgreSQL support**: psycopg2-binary

## 🌐 Deployment

### Gunicorn
```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Environment Variables
- `SECRET_KEY`: Django secret key (required for production)
- `DEBUG`: Set to False in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- Database credentials (if using PostgreSQL)

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5](https://getbootstrap.com/)
- [Crispy Forms](https://django-crispy-forms.readthedocs.io/)

## 📄 License

This project is open source and available under the MIT License.

## 👥 Contributing

Contributions are welcome! Please feel free to submit pull requests.

## 📧 Support

For support and questions, please contact: info@ngobettorrow.org

---

**Made with ❤️ for Better Tomorrow**
