from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """Admin user model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Service(Base):
    """Service model for BIM and Surveying services."""
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, index=True)  # "BIM" or "Surveying"
    image_url = Column(String(500), nullable=True)
    software_tools = Column(String(500), nullable=True)  # Comma-separated list
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TeamMember(Base):
    """Team member model."""
    __tablename__ = "team_members"
    
    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=True)
    position_en = Column(String(255), nullable=True)
    position_fa = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(20), nullable=True)
    image_url = Column(String(500), nullable=True)
    bio_en = Column(Text, nullable=True)
    bio_fa = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Certificate(Base):
    """Certificate model."""
    __tablename__ = "certificates"
    
    id = Column(Integer, primary_key=True, index=True)
    title_en = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=True)
    image_url = Column(String(500), nullable=True)
    description_en = Column(Text, nullable=True)
    description_fa = Column(Text, nullable=True)
    issue_date = Column(String(50), nullable=True)
    expiry_date = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class License(Base):
    """License model."""
    __tablename__ = "licenses"
    
    id = Column(Integer, primary_key=True, index=True)
    title_en = Column(String(255), nullable=False)
    title_fa = Column(String(255), nullable=True)
    image_url = Column(String(500), nullable=True)
    description_en = Column(Text, nullable=True)
    description_fa = Column(Text, nullable=True)
    issue_date = Column(String(50), nullable=True)
    issue_authority = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ContactSubmission(Base):
    """Contact form submission model."""
    __tablename__ = "contact_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    message = Column(Text, nullable=False)
    status = Column(String(50), default="new", index=True)  # new, read, replied
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow, index=True)


class CompanyInfo(Base):
    """Company information model."""
    __tablename__ = "company_info"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description_en = Column(Text, nullable=False)
    description_fa = Column(Text, nullable=True)
    founded_year = Column(Integer, nullable=True)
    headquarters_location = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    address_city = Column(String(100), nullable=True)
    address_country = Column(String(100), nullable=True)
    total_employees = Column(Integer, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Statistics(Base):
    """Statistics/metrics model."""
    __tablename__ = "statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    annual_projects = Column(Integer, default=1000)
    service_types = Column(Integer, default=9)
    employees = Column(Integer, default=90)
    satisfied_clients = Column(Integer, default=100)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
