# GeoBiro FastAPI Backend Setup Guide

## Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Redis 6+

### Installation Steps

#### 1. Install Python Dependencies
```bash
cd /home/unique/projects/geobiro/backend
pip install -r requirements.txt
```

#### 2. Set Up Environment Variables
```bash
# Copy example to .env
cp .env.example .env

# Edit .env with your values:
nano .env
```

**Important environment variables to configure:**
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: A secure random key (min 32 chars)
- `SMTP_HOST`, `SMTP_USER`, `SMTP_PASSWORD`: Email configuration
- `FRONTEND_URL`: Your frontend URL for CORS

#### 3. Initialize PostgreSQL Database
```bash
# Create a new database
sudo -u postgres createdb geobiro_db

# Or create user first (if needed)
sudo -u postgres psql -c "CREATE USER geobiro WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "ALTER ROLE geobiro CREATEDB;"

# Update DATABASE_URL in .env to match
```

#### 4. Start Redis Server
```bash
# If using Docker:
docker run -d -p 6379:6379 redis:latest

# Or if Redis is installed locally:
redis-server
```

#### 5. Run the Backend
```bash
cd /home/unique/projects/geobiro/backend

# With auto-reload (development):
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production:
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at: `http://localhost:8000`

### Initial Admin Setup

Once the backend is running, you need to create an admin user:

1. Go to `http://localhost:8000/api/docs` (Swagger UI)
2. Click on POST `/auth/register`
3. Submit credentials:
   ```json
   {
     "username": "admin",
     "email": "admin@geobiro.ba",
     "password": "secure_password_min_8_chars"
   }
   ```
4. Save the returned `access_token`
5. Subsequent users can be registered via the same endpoint (they won't be admins)

---

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Services
- `GET /api/services` - Get all services (with optional category filter)
- `GET /api/services/{id}` - Get service by ID
- `POST /api/services` - Create service (admin only)
- `PUT /api/services/{id}` - Update service (admin only)
- `DELETE /api/services/{id}` - Delete service (admin only)

### Team Members
- `GET /api/team` - Get all team members
- `GET /api/team/{id}` - Get team member by ID
- `POST /api/team` - Create team member (admin only)
- `POST /api/team/{id}/upload-image` - Upload team member photo (admin only)
- `PUT /api/team/{id}` - Update team member (admin only)
- `DELETE /api/team/{id}` - Delete team member (admin only)

### Certificates
- `GET /api/certificates` - Get all certificates
- `GET /api/certificates/{id}` - Get certificate by ID
- `POST /api/certificates` - Create certificate (admin only)
- `POST /api/certificates/{id}/upload-image` - Upload certificate image (admin only)
- `PUT /api/certificates/{id}` - Update certificate (admin only)
- `DELETE /api/certificates/{id}` - Delete certificate (admin only)

### Licenses
- `GET /api/licenses` - Get all licenses
- `GET /api/licenses/{id}` - Get license by ID
- `POST /api/licenses` - Create license (admin only)
- `POST /api/licenses/{id}/upload-image` - Upload license image (admin only)
- `PUT /api/licenses/{id}` - Update license (admin only)
- `DELETE /api/licenses/{id}` - Delete license (admin only)

### Contact & Company
- `POST /api/contact` - Submit contact form (public)
- `GET /api/admin/contact-submissions` - Get all contact submissions (admin only)
- `GET /api/admin/contact-submissions/{id}` - Get submission by ID (admin only)
- `PATCH /api/admin/contact-submissions/{id}/status` - Update submission status (admin only)
- `DELETE /api/admin/contact-submissions/{id}` - Delete submission (admin only)
- `GET /api/company-info` - Get company information
- `PUT /api/admin/company-info` - Update company info (admin only)
- `GET /api/statistics` - Get statistics
- `PUT /api/admin/statistics` - Update statistics (admin only)

### Health & Info
- `GET /health` - Health check
- `GET /` - API info

---

## Caching System (Redis)

The backend implements intelligent caching:

**Cached Endpoints:**
- Services (1 hour TTL)
- Team members (1 hour TTL)
- Certificates (1 hour TTL)
- Licenses (1 hour TTL)
- Company info (2 hours TTL)
- Statistics (2 hours TTL)

**Cache Invalidation:**
- Automatically invalidated when admin updates data
- Cache keys follow pattern: `cache:entity_type:*`
- Uses Redis KEYS pattern matching for bulk invalidation

---

## Database Schema

### Users Table
```
id (PK), username, email, hashed_password, is_admin, is_active, created_at, updated_at
```

### Services Table
```
id (PK), title, description, category (BIM/Surveying), image_url, software_tools, created_at, updated_at
```

### Team Members Table
```
id (PK), name_en, name_fa, position_en, position_fa, email, phone, image_url, bio_en, bio_fa, created_at, updated_at
```

### Certificates Table
```
id (PK), title_en, title_fa, image_url, description_en, description_fa, issue_date, expiry_date, created_at, updated_at
```

### Licenses Table
```
id (PK), title_en, title_fa, image_url, description_en, description_fa, issue_date, issue_authority, created_at, updated_at
```

### Contact Submissions Table
```
id (PK), name, phone, email, message, status (new/read/replied), ip_address, user_agent, submitted_at
```

### Company Info Table
```
id (PK), name, description_en, description_fa, founded_year, headquarters_location, phone, email, address_city, address_country, total_employees, updated_at
```

### Statistics Table
```
id (PK), annual_projects, service_types, employees, satisfied_clients, updated_at
```

---

## Frontend Integration

### Update Frontend API Base URL

In your Vue frontend (`src/main.js` or API client):

```javascript
const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api'
```

### Example API Calls from Frontend

```javascript
// Get services
const services = await fetch(`${API_BASE_URL}/services`)
  .then(r => r.json())

// Submit contact form
const response = await fetch(`${API_BASE_URL}/contact`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'John Doe',
    phone: '+1234567890',
    email: 'john@example.com',
    message: 'Your message here'
  })
})

// Get team members
const team = await fetch(`${API_BASE_URL}/team`)
  .then(r => r.json())

// Login (admin)
const login = await fetch(`${API_BASE_URL}/auth/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'admin',
    password: 'password'
  })
})
const { access_token } = await login.json()

// Create service (with token)
const newService = await fetch(`${API_BASE_URL}/services`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${access_token}`
  },
  body: JSON.stringify({
    title: 'New Service',
    description: 'Service description',
    category: 'BIM',
    image_url: 'https://...'
  })
})
```

---

## Email Configuration

### Using Gmail
1. Enable "Less secure app access" or use App Password
2. Set in .env:
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   ```

### Using Other Email Providers
- Outlook: `smtp.outlook.com:587`
- SendGrid: See their SMTP relay settings
- Custom SMTP: Configure accordingly

---

## Deployment

### Using Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using Gunicorn (Production)
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Environment Variables for Production
```
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=generate-a-random-32-char-key
DATABASE_URL=postgresql://user:pass@prod-db.com/db
REDIS_URL=redis://prod-redis.com:6379/0
```

---

## Troubleshooting

### PostgreSQL Connection Failed
- Check `DATABASE_URL` in `.env`
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check connection: `psql $DATABASE_URL`

### Redis Connection Failed
- Verify Redis is running: `redis-cli ping`
- Check `REDIS_URL` in `.env`
- Start Redis: `redis-server` or `docker run -p 6379:6379 redis`

### Email Not Sending
- Check SMTP credentials in `.env`
- Verify email address/password are correct
- Check firewall/network access to SMTP server
- Review error logs in console

### CORS Errors from Frontend
- Add your frontend URL to `FRONTEND_URL` in `.env`
- Check the CORS middleware in `main.py`
- Ensure `Allow-Origin` header is in response

---

## Development Tips

### Database Migrations (with Alembic)
```bash
# Initialize Alembic (if needed)
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Running Tests
```bash
# Install pytest
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/
```

### API Documentation
Access interactive docs at: `http://localhost:8000/api/docs`

---

## Support & Next Steps

1. **Create sample data** via API or admin dashboard
2. **Configure frontend** to use API endpoints
3. **Set up SSL/HTTPS** for production
4. **Implement admin dashboard** UI for content management
5. **Add image optimization** for uploads
6. **Set up monitoring** (logs, metrics, alerts)

---

Generated: 2025-12-25
Version: 1.0.0
