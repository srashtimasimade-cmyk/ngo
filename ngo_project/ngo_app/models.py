"""
Models for NGO Better Tomorrow application.
Defines database schema for managing NGO operations, members, projects, and donations.
"""

from django.db import models
from django.core.validators import URLValidator, MinValueValidator
from django.utils import timezone
from django.urls import reverse


class TimeStampedModel(models.Model):
    """Abstract base model with timestamp fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Organization(TimeStampedModel):
    """Core organization model."""
    
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        PENDING = 'pending', 'Pending Approval'
    
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    mission = models.TextField(help_text="Organization's mission statement")
    vision = models.TextField(help_text="Organization's vision statement")
    
    # Contact Information
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    website = models.URLField(validators=[URLValidator()], blank=True, null=True)
    
    # Location
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    
    # Organization Details
    registration_number = models.CharField(max_length=50, unique=True)
    established_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('ngo_app:organization-detail', kwargs={'slug': self.slug})


class Member(TimeStampedModel):
    """Organization members/volunteers."""
    
    class Role(models.TextChoices):
        FOUNDER = 'founder', 'Founder'
        DIRECTOR = 'director', 'Director'
        COORDINATOR = 'coordinator', 'Coordinator'
        VOLUNTEER = 'volunteer', 'Volunteer'
        DONOR = 'donor', 'Donor'
    
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        ON_LEAVE = 'on_leave', 'On Leave'
    
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='members')
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    role = models.CharField(max_length=20, choices=Role.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='members/', blank=True, null=True)
    bio = models.TextField(blank=True)
    
    joined_date = models.DateField(default=timezone.now)
    address = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['-joined_date']
        unique_together = ['organization', 'email']
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Project(TimeStampedModel):
    """NGO projects/initiatives."""
    
    class Status(models.TextChoices):
        PLANNING = 'planning', 'Planning'
        ACTIVE = 'active', 'Active'
        ON_HOLD = 'on_hold', 'On Hold'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
    
    class Category(models.TextChoices):
        EDUCATION = 'education', 'Education'
        HEALTH = 'health', 'Health'
        ENVIRONMENT = 'environment', 'Environment'
        COMMUNITY = 'community', 'Community Development'
        WOMEN = 'women', 'Women Empowerment'
        DISASTER = 'disaster', 'Disaster Relief'
        OTHER = 'other', 'Other'
    
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='projects')
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    objective = models.TextField(help_text="Project objectives and goals")
    
    category = models.CharField(max_length=50, choices=Category.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNING)
    
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    
    target_beneficiaries = models.IntegerField(validators=[MinValueValidator(0)])
    budget = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    location = models.CharField(max_length=255)
    lead_member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_projects')
    
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    
    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['category']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('ngo_app:project-detail', kwargs={'slug': self.slug})
    
    @property
    def is_active(self):
        return self.status == self.Status.ACTIVE


class Donation(TimeStampedModel):
    """Track donations to the organization."""
    
    class DonationType(models.TextChoices):
        MONETARY = 'monetary', 'Monetary'
        IN_KIND = 'in_kind', 'In-Kind'
        SERVICE = 'service', 'Service'
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        RECEIVED = 'received', 'Received'
        CANCELLED = 'cancelled', 'Cancelled'
    
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='donations')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')
    
    donor_name = models.CharField(max_length=255)
    donor_email = models.EmailField(blank=True)
    donor_phone = models.CharField(max_length=20, blank=True)
    
    donation_type = models.CharField(max_length=20, choices=DonationType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    # For monetary donations
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='USD')
    
    # For in-kind donations
    description = models.TextField(blank=True, help_text="Description of donation")
    
    donation_date = models.DateField(default=timezone.now)
    receipt_issued = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-donation_date']
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['donation_date']),
        ]
    
    def __str__(self):
        return f"Donation from {self.donor_name} - {self.get_donation_type_display()}"
    
    @property
    def display_value(self):
        if self.donation_type == self.DonationType.MONETARY:
            # Ensure 2 decimal places for monetary amounts
            return f"{self.currency} {self.amount:.2f}"
        return self.description


class Impact(TimeStampedModel):
    """Track project impact and outcomes."""
    
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='impact')
    
    # Beneficiaries
    actual_beneficiaries = models.IntegerField(validators=[MinValueValidator(0)])
    families_impacted = models.IntegerField(validators=[MinValueValidator(0)])
    children_benefited = models.IntegerField(validators=[MinValueValidator(0)], blank=True, default=0)
    
    # Outcomes
    key_achievements = models.TextField(help_text="Key achievements and outcomes")
    challenges_faced = models.TextField(blank=True, help_text="Challenges faced during project")
    lessons_learned = models.TextField(blank=True)
    
    # Metrics
    completion_percentage = models.IntegerField(
        validators=[MinValueValidator(0), ],
        default=0,
        help_text="Project completion percentage (0-100)"
    )
    
    # Media
    report_document = models.FileField(upload_to='impact_reports/', blank=True, null=True)
    gallery_images = models.JSONField(default=list, blank=True, help_text="JSON list of image URLs")
    
    class Meta:
        verbose_name = "Impact Report"
        verbose_name_plural = "Impact Reports"
    
    def __str__(self):
        return f"Impact Report - {self.project.title}"
