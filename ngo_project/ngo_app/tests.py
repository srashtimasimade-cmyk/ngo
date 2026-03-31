"""
Tests for NGO Better Tomorrow application.
Run with: python manage.py test
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Organization, Member, Project, Donation
from datetime import date, timedelta


class OrganizationModelTest(TestCase):
    """Test Organization model."""
    
    def setUp(self):
        self.org = Organization.objects.create(
            name='Test NGO',
            slug='test-ngo',
            description='A test organization',
            mission='Our mission',
            vision='Our vision',
            email='test@ngo.org',
            phone='+1234567890',
            address='123 Test St',
            city='Test City',
            state='Test State',
            country='Test Country',
            postal_code='12345',
            registration_number='REG12345',
            established_date=date.today()
        )
    
    def test_organization_creation(self):
        """Test organization is created correctly."""
        self.assertEqual(self.org.name, 'Test NGO')
        self.assertEqual(self.org.status, Organization.Status.ACTIVE)
    
    def test_organization_str(self):
        """Test organization string representation."""
        self.assertEqual(str(self.org), 'Test NGO')
    
    def test_organization_absolute_url(self):
        """Test organization absolute URL."""
        expected_url = reverse('ngo_app:organization-detail', kwargs={'slug': 'test-ngo'})
        self.assertEqual(self.org.get_absolute_url(), expected_url)


class MemberModelTest(TestCase):
    """Test Member model."""
    
    def setUp(self):
        self.org = Organization.objects.create(
            name='Test NGO',
            slug='test-ngo',
            description='Test',
            mission='Test',
            vision='Test',
            email='test@ngo.org',
            phone='+1234567890',
            address='Test',
            city='Test',
            state='Test',
            country='Test',
            postal_code='12345',
            registration_number='REG123',
            established_date=date.today()
        )
        
        self.member = Member.objects.create(
            organization=self.org,
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='+9876543210',
            role=Member.Role.VOLUNTEER,
            status=Member.Status.ACTIVE
        )
    
    def test_member_creation(self):
        """Test member is created correctly."""
        self.assertEqual(self.member.full_name, 'John Doe')
        self.assertEqual(self.member.role, Member.Role.VOLUNTEER)
    
    def test_member_unique_email_per_org(self):
        """Test email must be unique per organization."""
        with self.assertRaises(Exception):
            Member.objects.create(
                organization=self.org,
                first_name='Jane',
                last_name='Doe',
                email='john@example.com',
                phone='+1111111111',
                role=Member.Role.VOLUNTEER,
                status=Member.Status.ACTIVE
            )


class ProjectModelTest(TestCase):
    """Test Project model."""
    
    def setUp(self):
        self.org = Organization.objects.create(
            name='Test NGO',
            slug='test-ngo',
            description='Test',
            mission='Test',
            vision='Test',
            email='test@ngo.org',
            phone='+1234567890',
            address='Test',
            city='Test',
            state='Test',
            country='Test',
            postal_code='12345',
            registration_number='REG123',
            established_date=date.today()
        )
        
        self.project = Project.objects.create(
            organization=self.org,
            title='Test Project',
            slug='test-project',
            description='Test project description',
            objective='Test objective',
            category=Project.Category.EDUCATION,
            status=Project.Status.ACTIVE,
            start_date=date.today(),
            target_beneficiaries=100,
            budget=5000.00,
            location='Test Location'
        )
    
    def test_project_creation(self):
        """Test project is created correctly."""
        self.assertEqual(self.project.title, 'Test Project')
        self.assertTrue(self.project.is_active)
    
    def test_project_absolute_url(self):
        """Test project absolute URL."""
        expected_url = reverse('ngo_app:project-detail', kwargs={'slug': 'test-project'})
        self.assertEqual(self.project.get_absolute_url(), expected_url)


class DonationModelTest(TestCase):
    """Test Donation model."""
    
    def setUp(self):
        self.org = Organization.objects.create(
            name='Test NGO',
            slug='test-ngo',
            description='Test',
            mission='Test',
            vision='Test',
            email='test@ngo.org',
            phone='+1234567890',
            address='Test',
            city='Test',
            state='Test',
            country='Test',
            postal_code='12345',
            registration_number='REG123',
            established_date=date.today()
        )
        
        self.donation = Donation.objects.create(
            organization=self.org,
            donor_name='John Donor',
            donation_type=Donation.DonationType.MONETARY,
            amount=1000.00,
            status=Donation.Status.RECEIVED,
            donation_date=date.today()
        )
    
    def test_donation_creation(self):
        """Test donation is created correctly."""
        self.assertEqual(self.donation.donor_name, 'John Donor')
        self.assertEqual(self.donation.amount, 1000.00)
    
    def test_donation_display_value(self):
        """Test donation display value."""
        expected = 'USD 1000.00'
        self.assertEqual(self.donation.display_value, expected)


class ViewsTest(TestCase):
    """Test application views."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.client.login(username='testuser', password='password')
        self.org = Organization.objects.create(
            name='Test NGO',
            slug='test-ngo',
            description='Test',
            mission='Test',
            vision='Test',
            email='test@ngo.org',
            phone='+1234567890',
            address='Test',
            city='Test',
            state='Test',
            country='Test',
            postal_code='12345',
            registration_number='REG123',
            established_date=date.today()
        )
    
    def test_dashboard_view(self):
        """Test dashboard view redirects to donation list."""
        response = self.client.get(reverse('ngo_app:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('ngo_app:donation-list'))
    
    def test_organization_list_view(self):
        """Test organization list view."""
        response = self.client.get(reverse('ngo_app:organization-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test NGO')
    
    def test_organization_detail_view(self):
        """Test organization detail view."""
        response = self.client.get(reverse('ngo_app:organization-detail', kwargs={'slug': 'test-ngo'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test NGO')
    
    def test_project_list_view(self):
        """Test project list view."""
        response = self.client.get(reverse('ngo_app:project-list'))
        self.assertEqual(response.status_code, 200)


class AdminInterfaceTest(TestCase):
    """Test admin interface."""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'password')
    
    def test_admin_login(self):
        """Test admin login."""
        response = self.client.post(reverse('admin:login'), {
            'username': 'admin',
            'password': 'password'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_organization_admin(self):
        """Test organization admin page."""
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('admin:ngo_app_organization_changelist'))
        self.assertEqual(response.status_code, 200)
