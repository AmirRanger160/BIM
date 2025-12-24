# Frontend Integration Guide for GeoBiro Vue.js

This guide explains how to integrate the FastAPI backend with your existing Vue.js frontend.

## 1. Environment Setup

### Create `.env.local` in your Vue frontend root:

```
VITE_API_URL=http://localhost:8000/api
VITE_API_TIMEOUT=10000
```

For production:
```
VITE_API_URL=https://api.geobiro.ba/api
```

## 2. Create API Client

### Create `src/services/api.js`:

```javascript
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_URL,
  timeout: import.meta.env.VITE_API_TIMEOUT || 10000,
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle responses
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/admin/login'
    }
    return Promise.reject(error)
  }
)

export default api
```

## 3. Update Components to Use API

### Example: Contact Form (Contact.vue)

**Before (hardcoded):**
```vue
<script>
export default {
  data() {
    return {
      form: { name: '', phone: '', email: '', message: '' },
      loading: false
    }
  },
  methods: {
    async submitForm() {
      this.loading = true
      // No backend implementation
      this.loading = false
    }
  }
}
</script>
```

**After (with API):**
```vue
<script>
import api from '@/services/api'

export default {
  data() {
    return {
      form: { name: '', phone: '', email: '', message: '' },
      loading: false,
      submitted: false,
      error: null
    }
  },
  methods: {
    async submitForm() {
      this.loading = true
      this.error = null
      try {
        await api.post('/contact', this.form)
        this.submitted = true
        // Reset form after 3 seconds
        setTimeout(() => {
          this.form = { name: '', phone: '', email: '', message: '' }
          this.submitted = false
        }, 3000)
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error submitting form'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
```

### Example: Services (BimServices.vue)

**Before (hardcoded):**
```vue
<script>
export default {
  data() {
    return {
      services: [
        { id: 1, title: '3D Modeling', description: '...', image: '...' },
        // ... more services
      ]
    }
  }
}
</script>
```

**After (with API):**
```vue
<script>
import api from '@/services/api'

export default {
  data() {
    return {
      services: [],
      loading: true,
      error: null
    }
  },
  async mounted() {
    try {
      // Get BIM services
      this.services = await api.get('/services', {
        params: { category: 'BIM' }
      })
    } catch (err) {
      this.error = 'Failed to load services'
      console.error(err)
    } finally {
      this.loading = false
    }
  }
}
</script>
```

### Example: Team Members (Team.vue)

```vue
<script>
import api from '@/services/api'

export default {
  data() {
    return {
      members: [],
      loading: true
    }
  },
  async mounted() {
    try {
      this.members = await api.get('/team')
    } catch (err) {
      console.error('Failed to load team members:', err)
    } finally {
      this.loading = false
    }
  }
}
</script>
```

### Example: Statistics (Stats.vue)

```vue
<script>
import api from '@/services/api'

export default {
  data() {
    return {
      stats: {
        annual_projects: 1000,
        service_types: 9,
        employees: 90,
        satisfied_clients: 100
      }
    }
  },
  async mounted() {
    try {
      this.stats = await api.get('/statistics')
    } catch (err) {
      console.error('Failed to load statistics:', err)
    }
  }
}
</script>
```

## 4. Admin Panel Integration (Optional)

If you want to add admin functionality to manage content:

### Create Admin Login
```vue
<!-- src/views/AdminLogin.vue -->
<script>
import api from '@/services/api'

export default {
  data() {
    return {
      form: { username: '', password: '' },
      loading: false,
      error: null
    }
  },
  methods: {
    async login() {
      this.loading = true
      this.error = null
      try {
        const response = await api.post('/auth/login', this.form)
        localStorage.setItem('access_token', response.access_token)
        this.$router.push('/admin')
      } catch (err) {
        this.error = 'Invalid credentials'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
```

### Admin Dashboard (to manage content)
```vue
<!-- src/views/AdminDashboard.vue -->
<script>
import api from '@/services/api'

export default {
  data() {
    return {
      submissions: [],
      services: [],
      team: [],
      activeTab: 'submissions'
    }
  },
  async mounted() {
    this.loadSubmissions()
  },
  methods: {
    async loadSubmissions() {
      try {
        this.submissions = await api.get('/admin/contact-submissions')
      } catch (err) {
        console.error('Failed to load submissions:', err)
      }
    },
    async loadServices() {
      try {
        this.services = await api.get('/services')
      } catch (err) {
        console.error('Failed to load services:', err)
      }
    },
    async loadTeam() {
      try {
        this.team = await api.get('/team')
      } catch (err) {
        console.error('Failed to load team:', err)
      }
    },
    async deleteSubmission(id) {
      if (confirm('Delete this submission?')) {
        try {
          await api.delete(`/admin/contact-submissions/${id}`)
          this.loadSubmissions()
        } catch (err) {
          alert('Failed to delete submission')
        }
      }
    }
  }
}
</script>
```

## 5. Update package.json

Add axios if not already installed:

```bash
npm install axios
```

## 6. CORS Configuration (If Frontend & Backend on Different Ports)

Your backend's `.env` should have:
```
FRONTEND_URL=http://localhost:5173
```

The backend is configured to allow CORS from the frontend URL.

## 7. Running Both Frontend & Backend

### Terminal 1 - Backend:
```bash
cd backend
uvicorn main:app --reload
```

### Terminal 2 - Frontend:
```bash
cd .
npm run dev
```

Access at: `http://localhost:5173`

## 8. File Upload Example

For uploading team member photos or certificates:

```javascript
// Multipart form data for image upload
async uploadTeamImage(memberId, file) {
  const formData = new FormData()
  formData.append('file', file)
  
  try {
    const response = await api.post(
      `/team/${memberId}/upload-image`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )
    return response
  } catch (err) {
    console.error('Upload failed:', err)
    throw err
  }
}
```

## 9. Authentication & Token Management

Store token in localStorage or sessionStorage:

```javascript
// Login
const response = await api.post('/auth/login', { username, password })
localStorage.setItem('access_token', response.access_token)

// Use in all requests (automatically added by interceptor)
// Logout
localStorage.removeItem('access_token')
```

## 10. Error Handling

Consistent error handling pattern:

```javascript
try {
  const data = await api.get('/services')
  // Use data
} catch (error) {
  const message = error.response?.data?.detail || error.message
  console.error('API Error:', message)
  // Show user-friendly error message
}
```

---

## Common API Response Formats

### Success Response
```json
{
  "id": 1,
  "title": "Service Name",
  "description": "Service description",
  // ... other fields
}
```

### Error Response
```json
{
  "detail": "Error message explaining what went wrong"
}
```

### List Response
```json
[
  { "id": 1, "title": "Item 1" },
  { "id": 2, "title": "Item 2" }
]
```

---

## Troubleshooting

### CORS Errors
- Ensure `FRONTEND_URL` in backend `.env` matches your frontend URL
- Make sure backend is running on port 8000
- Check browser console for specific CORS errors

### Token Issues
- Verify token is being stored in localStorage
- Check token is being sent in Authorization header
- Token expires after 30 minutes (configurable)

### File Upload Issues
- Ensure `Content-Type` is set to `multipart/form-data`
- Check file size limits
- Verify uploads directory exists on backend

---

## Next Steps

1. **Install axios** in your frontend
2. **Create the api.js** service file
3. **Update component by component** to use the API
4. **Test authentication** by trying admin login
5. **Verify contact form** submission works end-to-end
6. **Deploy** both frontend and backend together

For more details, see the [SETUP_GUIDE.md](./SETUP_GUIDE.md) in the backend directory.
