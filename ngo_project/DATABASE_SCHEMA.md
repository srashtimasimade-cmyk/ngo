# NGO Better Tomorrow - SQL Database Schema

## Database Diagram

```sql
-- Organizations Table
CREATE TABLE ngo_app_organization (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    slug VARCHAR(50) NOT NULL UNIQUE,
    description LONGTEXT NOT NULL,
    mission LONGTEXT NOT NULL,
    vision LONGTEXT NOT NULL,
    
    -- Contact
    email VARCHAR(254) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    website VARCHAR(255),
    
    -- Location
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    
    -- Organization Details
    registration_number VARCHAR(50) NOT NULL UNIQUE,
    established_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    logo VARCHAR(100),
    
    -- Timestamps
    created_at TIMESTAMP AUTO_INCREMENT,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    KEY organization_status_idx (status),
    KEY organization_slug_idx (slug)
);

-- Members Table
CREATE TABLE ngo_app_member (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    organization_id BIGINT NOT NULL,
    
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    
    role VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    
    date_of_birth DATE,
    profile_picture VARCHAR(100),
    bio LONGTEXT,
    
    joined_date DATE NOT NULL,
    address VARCHAR(255),
    
    created_at TIMESTAMP AUTO_INCREMENT,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY member_org_email_idx (organization_id, email),
    KEY member_org_status_idx (organization_id, status),
    KEY member_role_idx (role),
    FOREIGN KEY (organization_id) REFERENCES ngo_app_organization(id) ON DELETE CASCADE
);

-- Projects Table
CREATE TABLE ngo_app_project (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    organization_id BIGINT NOT NULL,
    lead_member_id BIGINT,
    
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE,
    description LONGTEXT NOT NULL,
    objective LONGTEXT NOT NULL,
    
    category VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'planning',
    
    start_date DATE NOT NULL,
    end_date DATE,
    
    target_beneficiaries INT NOT NULL CHECK (target_beneficiaries >= 0),
    budget DECIMAL(12, 2) NOT NULL CHECK (budget >= 0),
    
    location VARCHAR(255) NOT NULL,
    image VARCHAR(100),
    
    created_at TIMESTAMP AUTO_INCREMENT,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    KEY project_org_status_idx (organization_id, status),
    KEY project_category_idx (category),
    KEY project_slug_idx (slug),
    FOREIGN KEY (organization_id) REFERENCES ngo_app_organization(id) ON DELETE CASCADE,
    FOREIGN KEY (lead_member_id) REFERENCES ngo_app_member(id) ON SET NULL
);

-- Donations Table
CREATE TABLE ngo_app_donation (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    organization_id BIGINT NOT NULL,
    project_id BIGINT,
    
    donor_name VARCHAR(255) NOT NULL,
    donor_email VARCHAR(254),
    donor_phone VARCHAR(20),
    
    donation_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    
    -- For monetary donations
    amount DECIMAL(12, 2) CHECK (amount >= 0),
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    
    -- For in-kind donations
    description LONGTEXT,
    
    donation_date DATE NOT NULL,
    receipt_issued BOOLEAN DEFAULT FALSE,
    notes LONGTEXT,
    
    created_at TIMESTAMP AUTO_INCREMENT,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    KEY donation_org_status_idx (organization_id, status),
    KEY donation_date_idx (donation_date),
    FOREIGN KEY (organization_id) REFERENCES ngo_app_organization(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES ngo_app_project(id) ON SET NULL
);

-- Impact Reports Table
CREATE TABLE ngo_app_impact (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    project_id BIGINT NOT NULL UNIQUE,
    
    actual_beneficiaries INT NOT NULL CHECK (actual_beneficiaries >= 0),
    families_impacted INT NOT NULL CHECK (families_impacted >= 0),
    children_benefited INT NOT NULL DEFAULT 0 CHECK (children_benefited >= 0),
    
    key_achievements LONGTEXT NOT NULL,
    challenges_faced LONGTEXT,
    lessons_learned LONGTEXT,
    
    completion_percentage INT NOT NULL DEFAULT 0 CHECK (completion_percentage >= 0 AND completion_percentage <= 100),
    
    report_document VARCHAR(100),
    gallery_images JSON,
    
    created_at TIMESTAMP AUTO_INCREMENT,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES ngo_app_project(id) ON DELETE CASCADE
);
```

## Key Relationships

### Organization ← Members (1:N)
- One organization has many members
- Delete organization cascades to delete all members

### Organization ← Projects (1:N)
- One organization manages many projects
- Delete organization cascades to delete all projects

### Organization ← Donations (1:N)
- One organization receives many donations
- Delete organization cascades to delete all donations

### Project ← Impact (1:1)
- One project has one impact report
- Delete project cascades to delete impact report

### Project ← Donations (1:N)
- One project can receive many donations
- If project is deleted, donations set project_id to NULL

### Member ← Projects (1:N) - Leadership
- One member can lead multiple projects
- If member is deleted, projects' lead_member_id set to NULL

## Database Indexes

- **Organizations**: (status), (slug)
- **Members**: (organization_id, status), (role)
- **Projects**: (organization_id, status), (category), (slug)
- **Donations**: (organization_id, status), (donation_date)

## SQL Queries Examples

### Get total donations by organization
```sql
SELECT 
    o.name,
    SUM(CASE WHEN d.donation_type = 'monetary' THEN d.amount ELSE 0 END) as total_donations,
    COUNT(d.id) as donation_count
FROM ngo_app_organization o
LEFT JOIN ngo_app_donation d ON o.id = d.organization_id AND d.status = 'received'
GROUP BY o.id
ORDER BY total_donations DESC;
```

### Get project performance metrics
```sql
SELECT 
    p.title,
    p.target_beneficiaries,
    i.actual_beneficiaries,
    p.budget,
    SUM(CASE WHEN d.donation_type = 'monetary' THEN d.amount ELSE 0 END) as funds_received,
    i.completion_percentage
FROM ngo_app_project p
LEFT JOIN ngo_app_impact i ON p.id = i.project_id
LEFT JOIN ngo_app_donation d ON p.id = d.project_id AND d.status = 'received'
GROUP BY p.id
ORDER BY p.start_date DESC;
```

### Get active team members by role
```sql
SELECT 
    o.name as organization,
    m.role,
    COUNT(m.id) as member_count,
    GROUP_CONCAT(CONCAT(m.first_name, ' ', m.last_name)) as members
FROM ngo_app_member m
JOIN ngo_app_organization o ON m.organization_id = o.id
WHERE m.status = 'active'
GROUP BY o.id, m.role
ORDER BY o.name, m.role;
```

### Get impact statistics
```sql
SELECT 
    p.title,
    p.category,
    i.actual_beneficiaries,
    i.families_impacted,
    i.children_benefited,
    i.completion_percentage,
    (i.actual_beneficiaries / p.target_beneficiaries * 100) as beneficiary_achievement_rate
FROM ngo_app_project p
JOIN ngo_app_impact i ON p.id = i.project_id
WHERE p.status IN ('active', 'completed')
ORDER BY i.actual_beneficiaries DESC;
```

## Data Constraints & Validation

### Organization
- Name and slug must be unique
- Registration number must be unique
- Email format validation

### Member
- Combination of organization + email must be unique
- Phone must match pattern (stored as VARCHAR for flexibility)
- Status limited to: active, inactive, on_leave
- Role limited to: founder, director, coordinator, volunteer, donor

### Project
- Target beneficiaries must be >= 0
- Budget must be > 0
- Slug must be unique across all projects
- Category limited to: education, health, environment, community, women, disaster, other

### Donation
- Amount must be > 0 for monetary donations
- Currency codes limited to 3 characters (ISO 4217)
- Status limited to: pending, received, cancelled
- Type limited to: monetary, in_kind, service

### Impact
- Completion percentage must be 0-100
- All numeric fields must be non-negative
