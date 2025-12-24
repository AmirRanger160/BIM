# GeoBiro FastAPI Backend

A complete FastAPI backend for the GeoBiro website with PostgreSQL database, Redis caching, JWT authentication, and comprehensive API endpoints.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Redis 6+

### Setup in 5 Minutes

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Copy environment file:**
   ```bash
   cp .env.example .env
   # Edit .env with your database and email settings
   ```

3. **Run with Docker (easiest):**
   ```bash
   docker-compose up
   ```

4. **Or run locally:**
   ```bash
   # Make sure PostgreSQL and Redis are running
   uvicorn main:app --reload
   ```

5. **Access the API:**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/api/docs

## 📋 Features

✅ **Complete API** for all GeoBiro content (services, team, certificates, licenses)
✅ **PostgreSQL Database** with optimized schema and indexes
✅ **Redis Caching** with intelligent TTL management
✅ **JWT Authentication** with role-based access control
✅ **Contact Form** with email notifications
✅ **Image Upload** support for team photos, certificates, licenses
✅ **Admin Dashboard** API ready
✅ **CORS Configured** for frontend integration
✅ **Rate Limiting** on public endpoints
✅ **Error Handling** with detailed logging
✅ **Docker Support** for easy deployment
✅ **API Documentation** with Swagger UI

## 📁 Project Structure

```
backend/
├── app/
│   ├── core/              # Configuration, security, settings
│   ├── models/            # SQLAlchemy database models
│   ├── schemas/           # Pydantic request/response schemas
│   ├── routers/           # API route handlers
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── services.py   # Services CRUD
│   │   ├── team.py       # Team members CRUD
│   │   ├── certificates.py # Certificates CRUD
│   │   ├── licenses.py   # Licenses CRUD
│   │   └── contact.py    # Contact form & company info
│   ├── services/          # Business logic
│   │   └── email_service.py
│   ├── cache.py           # Redis caching layer
│   └── database.py        # Database connection
├── uploads/               # User uploaded files
├── main.py               # FastAPI application entry point
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── SETUP_GUIDE.md        # Detailed setup instructions
├── FRONTEND_INTEGRATION.md # Frontend integration guide
└── README.md             # This file
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Services
- `GET /api/services` - Get all services
- `GET /api/services/{id}` - Get service details
- `POST /api/services` - Create (admin)
- `PUT /api/services/{id}` - Update (admin)
- `DELETE /api/services/{id}` - Delete (admin)

### Team Members
- `GET /api/team` - Get all members
- `GET /api/team/{id}` - Get member details
- `POST /api/team` - Create (admin)
- `POST /api/team/{id}/upload-image` - Upload photo (admin)
- `PUT /api/team/{id}` - Update (admin)
- `DELETE /api/team/{id}` - Delete (admin)

### Certificates
- `GET /api/certificates` - Get all certificates
- `POST /api/certificates` - Create (admin)
- `POST /api/certificates/{id}/upload-image` - Upload image (admin)
- `PUT /api/certificates/{id}` - Update (admin)
- `DELETE /api/certificates/{id}` - Delete (admin)

### Licenses
- `GET /api/licenses` - Get all licenses
- `POST /api/licenses` - Create (admin)
- `POST /api/licenses/{id}/upload-image` - Upload image (admin)
- `PUT /api/licenses/{id}` - Update (admin)
- `DELETE /api/licenses/{id}` - Delete (admin)

### Contact & Company
- `POST /api/contact` - Submit contact form
- `GET /api/admin/contact-submissions` - Get submissions (admin)
- `GET /api/company-info` - Get company info
- `PUT /api/admin/company-info` - Update (admin)
- `GET /api/statistics` - Get statistics
- `PUT /api/admin/statistics` - Update (admin)

## 🔐 Authentication

### Register Admin User
1. Go to http://localhost:8000/api/docs
2. POST `/auth/register` with:
   ```json
   {
     "username": "admin",
     "email": "admin@geobiro.ba",
     "password": "your_secure_password"
   }
   ```
3. Save the `access_token`
4. Use token in Authorization header: `Bearer YOUR_TOKEN`

## 💾 Database

Tables created automatically:
- `users` - Admin users
- `services` - BIM and Surveying services
- `team_members` - Team member profiles
- `certificates` - Company certificates
- `licenses` - Government licenses
- `contact_submissions` - Contact form submissions
- `company_info` - Company information
- `statistics` - Key metrics

## ⚡ Caching with Redis

Automatically cached endpoints:
- Services (1 hour)
- Team members (1 hour)
- Certificates (1 hour)
- Licenses (1 hour)
- Company info (2 hours)
- Statistics (2 hours)

Cache is automatically invalidated when data is updated.

## 📧 Email Configuration

### Using Gmail:
1. Enable "App Passwords" in Google Account
2. Set in `.env`:
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   ```

Contact form emails are sent to `ADMIN_EMAIL`.

## 🐳 Docker Deployment

### Using Docker Compose (includes PostgreSQL & Redis):
```bash
docker-compose up
```

### Build custom Docker image:
```bash
docker build -t geobiro-api .
docker run -p 8000:8000 -e DATABASE_URL=postgresql://... geobiro-api
```

## 🔗 Frontend Integration

See [FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md) for detailed integration instructions with your Vue.js frontend.

### Quick Example:
```javascript
// Get services
const services = await fetch('http://localhost:8000/api/services')
  .then(r => r.json())

// Submit contact form
await fetch('http://localhost:8000/api/contact', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'John',
    phone: '+1234567890',
    email: 'john@example.com',
    message: 'Your message'
  })
})
```

## 📚 Documentation

- **API Docs:** http://localhost:8000/api/docs (Swagger UI)
- **Setup Guide:** See [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Frontend Integration:** See [FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md)

## 🛠 Development

### Install dev dependencies:
```bash
pip install -r requirements.txt pytest pytest-asyncio httpx
```

### Run with auto-reload:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Run tests:
```bash
pytest tests/
```

## 📦 Production Deployment

### Using Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Environment for production:
```
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=generate-random-32-chars
DATABASE_URL=postgresql://user:pass@prod-db.com/db
REDIS_URL=redis://prod-redis.com:6379/0
```

## ❓ Troubleshooting

### Database connection failed
```bash
# Check PostgreSQL
sudo systemctl status postgresql
psql -U geobiro -d geobiro_db
```

### Redis connection failed
```bash
# Check Redis
redis-cli ping
# Output: PONG
```

### CORS errors
- Verify `FRONTEND_URL` in `.env`
- Backend must be accessible from frontend URL

### Email not sending
- Check SMTP credentials
- Verify firewall allows SMTP port
- Check server logs for errors

## 📄 License

MIT

## 📞 Support

For issues or questions, refer to:
1. [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup instructions
2. [FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md) - Frontend integration guide
3. API Docs: http://localhost:8000/api/docs

## 🎯 Next Steps

1. ✅ Backend is ready
2. Configure `.env` with your settings
3. Start backend with `docker-compose up` or `uvicorn main:app --reload`
4. Integrate with Vue.js frontend (see FRONTEND_INTEGRATION.md)
5. Create admin user and manage content
6. Deploy to production

---

**Created:** December 25, 2025
**Version:** 1.0.0
**Status:** Production Ready
