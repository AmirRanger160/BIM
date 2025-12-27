from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List, Annotated
from datetime import datetime
import re


# ============ Custom Email Validator ============
# This allows .test domain for testing purposes (which EmailStr doesn't accept)
def validate_email(email: str) -> str:
    """Validate email address, allowing .test domain for testing."""
    if not email:
        raise ValueError("Email is required")
    
    # Simple email regex pattern that accepts .test domains
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValueError("Invalid email format")
    
    return email


CustomEmail = Annotated[str, field_validator('email')(lambda cls, v: validate_email(v))]


# ============ Auth Schemas ============

class UserBase(BaseModel):
    username: str
    email: str
    
    @field_validator('email')
    @classmethod
    def validate_email_field(cls, v: str) -> str:
        return validate_email(v)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None
    
    @field_validator('email')
    @classmethod
    def validate_email_field(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        return validate_email(v)


class UserResponse(UserBase):
    id: int
    is_admin: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ============ Service Schemas ============

class ServiceBase(BaseModel):
    title_en: Optional[str] = None
    title_fa: Optional[str] = None
    title: Optional[str] = None  # For backward compatibility
    description_en: Optional[str] = None
    description_fa: Optional[str] = None
    description: Optional[str] = None  # For backward compatibility
    category: str = Field(..., description="BIM or Surveying")
    image_url: Optional[str] = None
    software_tools: Optional[str] = None


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    title_en: Optional[str] = None
    title_fa: Optional[str] = None
    title: Optional[str] = None  # For backward compatibility
    description_en: Optional[str] = None
    description_fa: Optional[str] = None
    description: Optional[str] = None  # For backward compatibility
    category: Optional[str] = None
    image_url: Optional[str] = None
    software_tools: Optional[str] = None


class ServiceResponse(BaseModel):
    id: int
    title_en: Optional[str] = None
    title_fa: Optional[str] = None
    title: Optional[str] = None
    description_en: Optional[str] = None
    description_fa: Optional[str] = None
    description: Optional[str] = None
    category: str
    image_url: Optional[str] = None
    software_tools: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============ Team Member Schemas ============

class TeamMemberBase(BaseModel):
    name_en: str = Field(..., min_length=1)
    name_fa: Optional[str] = None
    position_en: Optional[str] = None
    position_fa: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    image_url: Optional[str] = None
    bio_en: Optional[str] = None
    bio_fa: Optional[str] = None
    
    @field_validator('email')
    @classmethod
    def validate_email_field(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        return validate_email(v)


class TeamMemberCreate(TeamMemberBase):
    pass


class TeamMemberUpdate(BaseModel):
    name_en: Optional[str] = None
    name_fa: Optional[str] = None
    position_en: Optional[str] = None
    position_fa: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    image_url: Optional[str] = None
    bio_en: Optional[str] = None
    bio_fa: Optional[str] = None


class TeamMemberResponse(TeamMemberBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============ Certificate Schemas ============

class CertificateBase(BaseModel):
    title_en: str = Field(..., min_length=1)
    title_fa: Optional[str] = None
    image_url: Optional[str] = None
    description_en: Optional[str] = None
    description_fa: Optional[str] = None
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None


class CertificateCreate(CertificateBase):
    pass


class CertificateUpdate(BaseModel):
    title_en: Optional[str] = None
    title_fa: Optional[str] = None
    image_url: Optional[str] = None
    description_en: Optional[str] = None
    description_fa: Optional[str] = None
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None


class CertificateResponse(CertificateBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============ License Schemas ============

class LicenseBase(BaseModel):
    title_en: str = Field(..., min_length=1)
    title_fa: Optional[str] = None
    image_url: Optional[str] = None
    description_en: Optional[str] = None
    description_fa: Optional[str] = None
    issue_date: Optional[str] = None
    issue_authority: Optional[str] = None


class LicenseCreate(LicenseBase):
    pass


class LicenseUpdate(BaseModel):
    title_en: Optional[str] = None
    title_fa: Optional[str] = None
    image_url: Optional[str] = None
    description_en: Optional[str] = None
    description_fa: Optional[str] = None
    issue_date: Optional[str] = None
    issue_authority: Optional[str] = None


class LicenseResponse(LicenseBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============ Contact Submission Schemas ============

class ContactSubmissionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    phone: str = Field(..., min_length=5, max_length=20)
    email: str
    message: str = Field(..., min_length=10)
    
    @field_validator('email')
    @classmethod
    def validate_email_field(cls, v: str) -> str:
        return validate_email(v)


class ContactSubmissionResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    message: str
    status: str
    submitted_at: datetime
    
    class Config:
        from_attributes = True


class ContactSubmissionDetail(ContactSubmissionResponse):
    ip_address: Optional[str]
    user_agent: Optional[str]


class ContactSubmissionStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(new|read|replied|archived)$")


# ============ Company Info Schemas ============

class CompanyInfoBase(BaseModel):
    name: str = Field(..., min_length=1)
    description_en: str
    description_fa: Optional[str] = None
    founded_year: Optional[int] = None
    headquarters_location: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address_city: Optional[str] = None
    address_country: Optional[str] = None
    total_employees: Optional[int] = None
    
    @field_validator('email')
    @classmethod
    def validate_email_field(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        return validate_email(v)


class CompanyInfoCreate(CompanyInfoBase):
    pass


class CompanyInfoUpdate(BaseModel):
    name: Optional[str] = None
    description_en: Optional[str] = None
    description_fa: Optional[str] = None
    founded_year: Optional[int] = None
    headquarters_location: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address_city: Optional[str] = None
    address_country: Optional[str] = None
    total_employees: Optional[int] = None
    
    @field_validator('email')
    @classmethod
    def validate_email_field(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        return validate_email(v)


class CompanyInfoResponse(CompanyInfoBase):
    id: int
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============ Statistics Schemas ============

class StatisticsBase(BaseModel):
    annual_projects: int = Field(..., ge=0)
    service_types: int = Field(..., ge=0)
    employees: int = Field(..., ge=0)
    satisfied_clients: int = Field(..., ge=0)


class StatisticsCreate(StatisticsBase):
    pass


class StatisticsUpdate(BaseModel):
    annual_projects: Optional[int] = Field(None, ge=0)
    service_types: Optional[int] = Field(None, ge=0)
    employees: Optional[int] = Field(None, ge=0)
    satisfied_clients: Optional[int] = Field(None, ge=0)


class StatisticsResponse(StatisticsBase):
    id: int
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============ Project Schemas ============

class ProjectBase(BaseModel):
    title_en: str = Field(..., min_length=1, max_length=255)
    title_fa: Optional[str] = None
    description_en: str
    description_fa: Optional[str] = None
    image_url: Optional[str] = None
    archive_url: Optional[str] = None
    iframe_url: Optional[str] = None
    category: Optional[str] = None
    order: int = 0
    is_featured: bool = False


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title_en: Optional[str] = None
    title_fa: Optional[str] = None
    description_en: Optional[str] = None
    description_fa: Optional[str] = None
    image_url: Optional[str] = None
    archive_url: Optional[str] = None
    iframe_url: Optional[str] = None
    category: Optional[str] = None
    order: Optional[int] = None
    is_featured: Optional[bool] = None


class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============ Article Schemas ============

class ArticleBase(BaseModel):
    title_en: str = Field(..., min_length=1, max_length=255)
    title_fa: Optional[str] = None
    slug: str = Field(..., min_length=1, max_length=255)
    summary_en: str = Field(..., min_length=1)
    summary_fa: Optional[str] = None
    content_en: str = Field(..., min_length=1)
    content_fa: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None
    is_published: bool = False


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title_en: Optional[str] = None
    title_fa: Optional[str] = None
    slug: Optional[str] = None
    summary_en: Optional[str] = None
    summary_fa: Optional[str] = None
    content_en: Optional[str] = None
    content_fa: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None
    is_published: Optional[bool] = None


# ============ Article Image Schemas ============

class ArticleImageBase(BaseModel):
    image_url: str = Field(..., min_length=1)
    caption_en: Optional[str] = None
    caption_fa: Optional[str] = None
    alt_text_en: Optional[str] = None
    alt_text_fa: Optional[str] = None
    order: int = 0


class ArticleImageCreate(ArticleImageBase):
    pass


class ArticleImageUpdate(BaseModel):
    image_url: Optional[str] = None
    caption_en: Optional[str] = None
    caption_fa: Optional[str] = None
    alt_text_en: Optional[str] = None
    alt_text_fa: Optional[str] = None
    order: Optional[int] = None


class ArticleImageResponse(ArticleImageBase):
    id: int
    article_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ArticleResponse(ArticleBase):
    id: int
    publish_date: datetime
    created_at: datetime
    updated_at: datetime
    images: Optional[List[ArticleImageResponse]] = None
    
    class Config:
        from_attributes = True


# ============ Article Image Schemas ============

class ArticleImageBase(BaseModel):
    image_url: str = Field(..., min_length=1)
    caption_en: Optional[str] = None
    caption_fa: Optional[str] = None
    alt_text_en: Optional[str] = None
    alt_text_fa: Optional[str] = None
    order: int = 0


class ArticleImageCreate(ArticleImageBase):
    pass


class ArticleImageUpdate(BaseModel):
    image_url: Optional[str] = None
    caption_en: Optional[str] = None
    caption_fa: Optional[str] = None
    alt_text_en: Optional[str] = None
    alt_text_fa: Optional[str] = None
    order: Optional[int] = None


class ArticleImageResponse(ArticleImageBase):
    id: int
    article_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
