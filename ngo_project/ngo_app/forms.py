"""
Django Forms for NGO application using Crispy Forms.
"""

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit, HTML
from .models import Organization, Member, Project, Donation


class OrganizationForm(forms.ModelForm):
    """Form for creating/editing organizations."""
    
    class Meta:
        model = Organization
        fields = [
            'name', 'slug', 'description', 'mission', 'vision',
            'email', 'phone', 'website',
            'address', 'city', 'state', 'country', 'postal_code',
            'registration_number', 'established_date', 'logo'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Basic Information',
                Row(
                    Column('name', css_class='form-group col-md-6'),
                    Column('slug', css_class='form-group col-md-6'),
                ),
                'description',
                'mission',
                'vision',
            ),
            Fieldset(
                'Contact Information',
                Row(
                    Column('email', css_class='form-group col-md-6'),
                    Column('phone', css_class='form-group col-md-6'),
                ),
                'website',
            ),
            Fieldset(
                'Location',
                Row(
                    Column('address', css_class='form-group col-md-12'),
                ),
                Row(
                    Column('city', css_class='form-group col-md-3'),
                    Column('state', css_class='form-group col-md-3'),
                    Column('country', css_class='form-group col-md-3'),
                    Column('postal_code', css_class='form-group col-md-3'),
                ),
            ),
            Fieldset(
                'Organization Details',
                Row(
                    Column('registration_number', css_class='form-group col-md-6'),
                    Column('established_date', css_class='form-group col-md-6'),
                ),
                'logo',
            ),
            Submit('submit', 'Save Organization', css_class='btn btn-primary btn-lg mt-3')
        )


class MemberForm(forms.ModelForm):
    """Form for managing team members."""
    
    class Meta:
        model = Member
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'role', 'status', 'date_of_birth', 'profile_picture',
            'bio', 'address'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Personal Information',
                Row(
                    Column('first_name', css_class='form-group col-md-6'),
                    Column('last_name', css_class='form-group col-md-6'),
                ),
                Row(
                    Column('email', css_class='form-group col-md-6'),
                    Column('phone', css_class='form-group col-md-6'),
                ),
                'bio',
            ),
            Fieldset(
                'Role & Status',
                Row(
                    Column('role', css_class='form-group col-md-6'),
                    Column('status', css_class='form-group col-md-6'),
                ),
            ),
            Fieldset(
                'Additional Details',
                Row(
                    Column('date_of_birth', css_class='form-group col-md-6'),
                    Column('profile_picture', css_class='form-group col-md-6'),
                ),
                'address',
            ),
            Submit('submit', 'Save Member', css_class='btn btn-success btn-lg mt-3')
        )


class ProjectForm(forms.ModelForm):
    """Form for managing projects."""
    
    class Meta:
        model = Project
        fields = [
            'title', 'slug', 'description', 'objective',
            'category', 'status', 'start_date', 'end_date',
            'target_beneficiaries', 'budget', 'location',
            'lead_member', 'image'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'objective': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Project Details',
                Row(
                    Column('title', css_class='form-group col-md-8'),
                    Column('slug', css_class='form-group col-md-4'),
                ),
                'description',
                'objective',
            ),
            Fieldset(
                'Project Classification',
                Row(
                    Column('category', css_class='form-group col-md-6'),
                    Column('status', css_class='form-group col-md-6'),
                ),
            ),
            Fieldset(
                'Timeline & Scope',
                Row(
                    Column('start_date', css_class='form-group col-md-6'),
                    Column('end_date', css_class='form-group col-md-6'),
                ),
                Row(
                    Column('target_beneficiaries', css_class='form-group col-md-6'),
                    Column('location', css_class='form-group col-md-6'),
                ),
            ),
            Fieldset(
                'Resources',
                Row(
                    Column('budget', css_class='form-group col-md-6'),
                    Column('lead_member', css_class='form-group col-md-6'),
                ),
                'image',
            ),
            Submit('submit', 'Save Project', css_class='btn btn-info btn-lg mt-3')
        )


class DonationForm(forms.ModelForm):
    """Form for recording donations."""
    
    class Meta:
        model = Donation
        fields = [
            'organization', 'donor_name', 'donor_email', 'donor_phone',
            'donation_type', 'project',
            'amount', 'currency', 'description',
            'donation_date', 'notes'
        ]
        widgets = {
            'donation_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Organization & Donor Information',
                'organization',
                Row(
                    Column('donor_name', css_class='form-group col-md-6'),
                    Column('donor_email', css_class='form-group col-md-6'),
                ),
                Row(
                    Column('donor_phone', css_class='form-group col-md-6'),
                    Column('donation_type', css_class='form-group col-md-6'),
                ),
            ),
            Fieldset(
                'Donation Details',
                'project',
                Row(
                    Column('amount', css_class='form-group col-md-6'),
                    Column('currency', css_class='form-group col-md-6'),
                ),
                'description',
                Row(
                    Column('donation_date', css_class='form-group col-md-6'),
                ),
                'notes',
            ),
            Submit('submit', 'Record Donation', css_class='btn btn-warning btn-lg mt-3')
        )
