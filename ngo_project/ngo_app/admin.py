"""
Django Admin Configuration for NGO Better Tomorrow.
Provides attractive admin interface for managing all data.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Organization, Member, Project, Donation, Impact


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Admin interface for organizations."""
    
    list_display = ('name', 'status_badge', 'email', 'city', 'created_at')
    list_filter = ('status', 'country', 'created_at')
    search_fields = ('name', 'email', 'registration_number')
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'mission', 'vision', 'logo')
        }),
        ('Contact', {
            'fields': ('email', 'phone', 'website')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code')
        }),
        ('Registration', {
            'fields': ('registration_number', 'established_date', 'status'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'established_date'
    
    def status_badge(self, obj):
        """Display status as colored badge."""
        colors = {
            'active': '#28a745',
            'inactive': '#6c757d',
            'pending': '#ffc107',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """Admin interface for members."""
    
    list_display = ('full_name', 'organization', 'role_badge', 'status', 'email', 'joined_date')
    list_filter = ('status', 'role', 'organization', 'joined_date')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'profile_picture')
        }),
        ('Organization Role', {
            'fields': ('organization', 'role', 'status', 'joined_date')
        }),
        ('Additional Info', {
            'fields': ('bio', 'address'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'joined_date'
    
    def role_badge(self, obj):
        """Display role as styled badge."""
        colors = {
            'founder': '#e83e8c',
            'director': '#007bff',
            'coordinator': '#17a2b8',
            'volunteer': '#28a745',
            'donor': '#ffc107',
        }
        color = colors.get(obj.role, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 12px;">{}</span>',
            color,
            obj.get_role_display()
        )
    role_badge.short_description = 'Role'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin interface for projects."""
    
    list_display = ('title', 'organization', 'category_tag', 'status_badge', 'start_date', 'budget_display')
    list_filter = ('status', 'category', 'organization', 'start_date')
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Project Details', {
            'fields': ('title', 'slug', 'organization', 'description', 'objective', 'image')
        }),
        ('Classification', {
            'fields': ('category', 'status')
        }),
        ('Timeline & Scope', {
            'fields': ('start_date', 'end_date', 'target_beneficiaries', 'location', 'lead_member')
        }),
        ('Budget & Resources', {
            'fields': ('budget',),
        }),
    )
    
    filter_horizontal = ()
    date_hierarchy = 'start_date'
    
    def category_tag(self, obj):
        """Display category as tag."""
        colors = {
            'education': '#007bff',
            'health': '#dc3545',
            'environment': '#28a745',
            'community': '#17a2b8',
            'women': '#e83e8c',
            'disaster': '#fd7e14',
            'other': '#6c757d',
        }
        color = colors.get(obj.category, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 15px; font-size: 12px;">{}</span>',
            color,
            obj.get_category_display()
        )
    category_tag.short_description = 'Category'
    
    def status_badge(self, obj):
        """Display status as badge."""
        colors = {
            'planning': '#6c757d',
            'active': '#28a745',
            'on_hold': '#ffc107',
            'completed': '#007bff',
            'cancelled': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 12px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def budget_display(self, obj):
        """Display budget with currency formatting."""
        return format_html('<strong>${:,.2f}</strong>', obj.budget)
    budget_display.short_description = 'Budget'


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    """Admin interface for donations."""
    
    list_display = ('donor_name', 'organization', 'donation_type_badge', 'amount_display', 'status_badge', 'donation_date')
    list_filter = ('status', 'donation_type', 'organization', 'donation_date')
    search_fields = ('donor_name', 'donor_email', 'donor_phone')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email', 'donor_phone')
        }),
        ('Donation Details', {
            'fields': ('organization', 'project', 'donation_type', 'amount', 'currency', 'description')
        }),
        ('Management', {
            'fields': ('status', 'donation_date', 'receipt_issued', 'notes')
        }),
    )
    
    date_hierarchy = 'donation_date'
    actions = ['mark_as_received', 'issue_receipt']
    
    def donation_type_badge(self, obj):
        """Display donation type as badge."""
        colors = {
            'monetary': '#28a745',
            'in_kind': '#007bff',
            'service': '#17a2b8',
        }
        color = colors.get(obj.donation_type, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 12px;">{}</span>',
            color,
            obj.get_donation_type_display()
        )
    donation_type_badge.short_description = 'Type'
    
    def amount_display(self, obj):
        """Display amount with currency."""
        if obj.donation_type == 'monetary':
            return format_html('<strong>{} {:,.2f}</strong>', obj.currency, obj.amount or 0)
        return obj.description[:30]
    amount_display.short_description = 'Amount/Description'
    
    def status_badge(self, obj):
        """Display status as badge."""
        colors = {
            'pending': '#ffc107',
            'received': '#28a745',
            'cancelled': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 12px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def mark_as_received(self, request, queryset):
        """Mark selected donations as received."""
        updated = queryset.update(status=Donation.Status.RECEIVED)
        self.message_user(request, f'{updated} donation(s) marked as received.')
    mark_as_received.short_description = 'Mark selected donations as received'
    
    def issue_receipt(self, request, queryset):
        """Mark receipts as issued."""
        updated = queryset.filter(donation_type=Donation.DonationType.MONETARY).update(receipt_issued=True)
        self.message_user(request, f'Receipt(s) issued for {updated} donation(s).')
    issue_receipt.short_description = 'Issue receipt'


@admin.register(Impact)
class ImpactAdmin(admin.ModelAdmin):
    """Admin interface for impact reports."""
    
    list_display = ('project_title', 'actual_beneficiaries', 'families_impacted', 'completion_percentage')
    list_filter = ('project',)
    search_fields = ('project__title', 'key_achievements')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Project Reference', {
            'fields': ('project',)
        }),
        ('Impact Metrics', {
            'fields': ('actual_beneficiaries', 'families_impacted', 'children_benefited', 'completion_percentage')
        }),
        ('Report Content', {
            'fields': ('key_achievements', 'challenges_faced', 'lessons_learned')
        }),
        ('Media', {
            'fields': ('report_document', 'gallery_images'),
            'classes': ('collapse',)
        }),
    )
    
    def project_title(self, obj):
        """Display project title."""
        return obj.project.title
    project_title.short_description = 'Project'
