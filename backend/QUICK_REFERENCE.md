# Quick Reference Guide - GeoBiro Backend API

## 🎯 Essential Commands

### Start Backend
```bash
# With Docker (recommended)
cd /home/unique/projects/geobiro/backend
docker-compose up

# Without Docker
uvicorn main:app --reload
```

### Access Points
- **API Root:** http://localhost:8000
- **API Docs:** http://localhost:8000/api/docs
- **Health Check:** http://localhost:8000/health

---

## 🔐 Authentication

### Register Admin
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@geobiro.ba",
    "password": "YourSecurePassword123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "YourSecurePassword123"
  }'
```

### Use Token in Requests
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/api/admin/contact-submissions
```

---

## 📋 API Endpoints Cheat Sheet

### Public Endpoints (No auth required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/services` | Get all services |
| GET | `/api/services/{id}` | Get service by ID |
| GET | `/api/team` | Get all team members |
| GET | `/api/team/{id}` | Get team member by ID |
| GET | `/api/certificates` | Get all certificates |
| GET | `/api/licenses` | Get all licenses |
| GET | `/api/company-info` | Get company information |
| GET | `/api/statistics` | Get statistics |
| POST | `/api/contact` | Submit contact form |

### Admin Endpoints (Requires token)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/services` | Create service |
| PUT | `/api/services/{id}` | Update service |
| DELETE | `/api/services/{id}` | Delete service |
| POST | `/api/team` | Create team member |
| POST | `/api/team/{id}/upload-image` | Upload team photo |
| PUT | `/api/team/{id}` | Update team member |
| DELETE | `/api/team/{id}` | Delete team member |
| POST | `/api/certificates` | Create certificate |
| POST | `/api/certificates/{id}/upload-image` | Upload cert image |
| PUT | `/api/certificates/{id}` | Update certificate |
| DELETE | `/api/certificates/{id}` | Delete certificate |
| POST | `/api/licenses` | Create license |
| POST | `/api/licenses/{id}/upload-image` | Upload license image |
| PUT | `/api/licenses/{id}` | Update license |
| DELETE | `/api/licenses/{id}` | Delete license |
| GET | `/api/admin/contact-submissions` | Get all submissions |
| GET | `/api/admin/contact-submissions/{id}` | Get submission |
| PATCH | `/api/admin/contact-submissions/{id}/status` | Update status |
| DELETE | `/api/admin/contact-submissions/{id}` | Delete submission |
| PUT | `/api/admin/company-info` | Update company info |
| PUT | `/api/admin/statistics` | Update statistics |

---

## 📝 Request/Response Examples

### GET Services
```bash
curl http://localhost:8000/api/services?category=BIM
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "3D Modeling",
    "description": "Professional 3D modeling...",
    "category": "BIM",
    "image_url": "https://...",
    "software_tools": "Revit, AutoCAD",
    "created_at": "2025-12-25T10:00:00",
    "updated_at": "2025-12-25T10:00:00"
  }
]
```

### POST Contact Form
```bash
curl -X POST http://localhost:8000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "phone": "+1234567890",
    "email": "john@example.com",
    "message": "I would like to know more about your services."
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "phone": "+1234567890",
  "email": "john@example.com",
  "message": "I would like to know more about your services.",
  "status": "new",
  "submitted_at": "2025-12-25T10:00:00"
}
```

### POST Create Service (Admin)
```bash
curl -X POST http://localhost:8000/api/services \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "Laser Scanning",
    "description": "High-precision laser scanning services for surveying and mapping.",
    "category": "Surveying",
    "image_url": "https://example.com/laser.jpg",
    "software_tools": "Leica, Faro"
  }'
```

### Upload Image (Admin)
```bash
curl -X POST http://localhost:8000/api/team/1/upload-image \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/image.jpg"
```

### GET Contact Submissions (Admin)
```bash
curl http://localhost:8000/api/admin/contact-submissions?status=new \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "phone": "+1234567890",
    "email": "john@example.com",
    "message": "Message...",
    "status": "new",
    "ip_address": "192.168.1.1",
    "user_agent": "Mozilla/5.0...",
    "submitted_at": "2025-12-25T10:00:00"
  }
]
```

---

## ⚙️ Environment Variables

### Required
```
DATABASE_URL=postgresql://user:password@localhost:5432/geobiro_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-min-32-characters
```

### Email Configuration
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@geobiro.ba
ADMIN_EMAIL=info@geobiro.ba
```

### Application
```
ENVIRONMENT=development
DEBUG=true
FRONTEND_URL=http://localhost:5173
```

---

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Rebuild images
docker-compose build

# Access database
docker-compose exec postgres psql -U geobiro -d geobiro_db

# Access Redis
docker-compose exec redis redis-cli
```

---

## 🔧 Database Commands

```bash
# Connect to database
psql -U geobiro -d geobiro_db -h localhost

# List tables
\dt

# View specific table
SELECT * FROM services;

# Backup database
pg_dump -U geobiro geobiro_db > backup.sql

# Restore database
psql -U geobiro geobiro_db < backup.sql
```

---

## 📞 Contact Form Flow

1. **Frontend** → `POST /api/contact` with form data
2. **Backend** → Saves to database, sends email to admin
3. **Admin Email** → Receives notification with message
4. **User Email** → Receives confirmation response
5. **Admin Panel** → Can view at `GET /api/admin/contact-submissions`

---

## 🎨 Frontend Integration (Simple)

```javascript
// Get services
const services = await fetch('http://localhost:8000/api/services')
  .then(r => r.json())

// Get team
const team = await fetch('http://localhost:8000/api/team')
  .then(r => r.json())

// Submit contact form
const response = await fetch('http://localhost:8000/api/contact', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'John Doe',
    phone: '+1234567890',
    email: 'john@example.com',
    message: 'Your message'
  })
})
```

---

## 🆘 Common Issues

### "Connection refused"
- PostgreSQL not running
- Redis not running
- Check DATABASE_URL and REDIS_URL

### "401 Unauthorized"
- Token missing or expired
- Add `Authorization: Bearer TOKEN` header
- Re-login to get new token

### "CORS error"
- Frontend URL not in FRONTEND_URL env
- Check browser console for details
- Verify CORS middleware config

### "File upload failed"
- File too large
- Invalid file type
- Check uploads directory permissions

---

## 📊 Useful Redis Commands

```bash
# Connect to Redis
redis-cli

# List all cache keys
KEYS cache:*

# Get specific key
GET cache:services

# Clear cache
FLUSHDB

# Monitor live requests
MONITOR
```

---

## 🔍 Database Schema Summary

```sql
-- 8 Tables created automatically
users                    -- Admin accounts
services                 -- Services (BIM/Surveying)
team_members             -- Team member profiles
certificates             -- Company certificates
licenses                 -- Government licenses
contact_submissions      -- Contact form data
company_info             -- Company information
statistics               -- Key metrics
```

---

## 📈 Performance Tips

1. **Caching** - Redis caches frequently accessed data automatically
2. **Connection Pooling** - PostgreSQL uses 10-20 connections by default
3. **Rate Limiting** - Contact endpoint limited to prevent spam
4. **Async Email** - Emails sent asynchronously (non-blocking)
5. **Indexes** - Database indexes on frequently queried fields

---

## 🔐 Security Checklist

- [ ] Change `SECRET_KEY` in production
- [ ] Use strong database password
- [ ] Enable HTTPS/SSL in production
- [ ] Configure CORS correctly for your domain
- [ ] Regular database backups
- [ ] Monitor logs for suspicious activity
- [ ] Keep dependencies updated
- [ ] Use environment variables for secrets

---

## 📚 Additional Resources

- **API Docs:** http://localhost:8000/api/docs
- **Setup Guide:** See SETUP_GUIDE.md
- **Frontend Integration:** See FRONTEND_INTEGRATION.md
- **Complete Implementation:** See IMPLEMENTATION_COMPLETE.md

---

**Quick Start:** `docker-compose up` → Go to http://localhost:8000/api/docs

Generated: December 25, 2025
