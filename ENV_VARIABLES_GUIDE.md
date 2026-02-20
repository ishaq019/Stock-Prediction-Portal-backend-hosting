# ⚙️ ENVIRONMENT VARIABLES GUIDE

Complete reference for all configuration variables needed for local development and Vercel deployment.

---

## 📝 .env File Template

Create a `.env` file in your project root with these variables:

```env
# ============================================
# DJANGO CONFIGURATION
# ============================================

# Secret key for Django (MUST be unique and secure!)
# Generate: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY=your-super-secret-key-here-generate-new-one

# Debug mode (FALSE for production, TRUE for development)
DEBUG=False

# ============================================
# DATABASE CONFIGURATION
# ============================================

# For LOCAL development (SQLite):
# DATABASE_URL=sqlite:///db.sqlite3

# For PRODUCTION (Neon PostgreSQL):
# Get this from: https://console.neon.tech
# Format: postgresql://username:password@host/database?sslmode=require
DATABASE_URL=postgresql://neon_user:neon_password@ep-xxxxx-xxxxx.region.aws.neon.tech/neondb?sslmode=require

# ============================================
# CORS CONFIGURATION
# ============================================

# Allow all origins (use sparingly, set to False in production)
CORS_ALLOW_ALL=False

# Specific allowed origins are defined in settings.py
# Includes: localhost, syedishaq.me, GitHub Pages, and Vercel domains

# ============================================
# VERCEL/PRODUCTION SETTINGS
# ============================================

# Set to True when deployed on Vercel
PRODUCTION_DATABASE=False

# Allowed hosts (comma-separated, no spaces)
ALLOWED_HOSTS=127.0.0.1,localhost,*.vercel.app,syedishaq.me,www.syedishaq.me

# ============================================
# OPTIONAL: API KEYS (add as needed)
# ============================================

# Example: If you use external services
# STRIPE_KEY=sk_test_...
# SENDGRID_API_KEY=...
```

---

## 🔄 Variable Reference

### **DJANGO CORE VARIABLES**

| Variable | Local Value | Production Value | Description |
|----------|---|---|---|
| `SECRET_KEY` | Generate unique | Generate unique | Django security key |
| `DEBUG` | `True` | `False` | Error details visibility |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | `*.vercel.app,syedishaq.me` | Allowed domains |

### **DATABASE VARIABLES**

| Variable | Value | Notes |
|----------|-------|-------|
| `DATABASE_URL` | SQLite (local) | Format: `sqlite:///db.sqlite3` |
| `DATABASE_URL` | PostgreSQL (prod) | Format: `postgresql://user:pass@host/db` |
| `PRODUCTION_DATABASE` | `True`/`False` | Tells Django which DB config to use |

### **SECURITY VARIABLES**

| Variable | Local | Production | Description |
|----------|-------|-----------|---|
| `CORS_ALLOW_ALL` | `True` | `False` | Allow all origins (dev only!) |
| `SECRET_KEY` | Generate | Generate | Creates secure sessions |

### **OPTIONAL VARIABLES**

Add only if you use these services:

```env
# Stripe (payment processing)
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# SendGrid (email)
SENDGRID_API_KEY=SG.xxx...

# AWS S3 (file storage)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=...

# Google OAuth
GOOGLE_OAUTH_CLIENT_ID=...
GOOGLE_OAUTH_CLIENT_SECRET=...
```

---

## 📋 Setup Instructions

### **STEP 1: Local Development Setup**

1️⃣ **Create `.env` file in project root:**
```
c:\Users\ahame\Downloads\backend-drf\.env
```

2️⃣ **Add these variables:**
```env
SECRET_KEY=generate-with-django-command
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOW_ALL=True
ALLOWED_HOSTS=127.0.0.1,localhost,*.localhost
```

3️⃣ **Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

4️⃣ **Copy output and paste as SECRET_KEY value**

5️⃣ **Test locally:**
```bash
python manage.py runserver
```

✅ If no errors, variables are correct!

---

### **STEP 2: Production Setup (Vercel)**

1️⃣ **Get Neon PostgreSQL connection string:**
   - Go to: https://console.neon.tech
   - Select your project
   - Copy connection string
   - Format: `postgresql://user:password@host/database?sslmode=require`

2️⃣ **Generate new SECRET_KEY:**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3️⃣ **Update Vercel environment variables:**
   - Go to: https://vercel.com/dashboard
   - Select your project
   - **Settings** → **Environment Variables**
   - Add each variable:

| Key | Value |
|---|---|
| `SECRET_KEY` | Generated key |
| `DEBUG` | `False` |
| `DATABASE_URL` | Neon connection string |
| `CORS_ALLOW_ALL` | `False` |
| `ALLOWED_HOSTS` | `your-domain.vercel.app,syedishaq.me,ishaq019.github.io` |
| `PRODUCTION_DATABASE` | `True` |

4️⃣ **Redeploy after adding variables:**
   - Go to **Deployments**
   - Click three-dots on latest
   - Click **"Redeploy"**

---

## 🔐 Security Best Practices

### **✅ DO:**
- ✅ Generate unique SECRET_KEY for each environment
- ✅ Use environment variables for all secrets
- ✅ Set `DEBUG=False` in production
- ✅ Use HTTPS only (Vercel handles this)
- ✅ Restrict CORS to specific domains
- ✅ Rotate API keys regularly

### **❌ DON'T:**
- ❌ Commit `.env` file to GitHub
- ❌ Use weak SECRET_KEY
- ❌ Set `DEBUG=True` in production
- ❌ Use `CORS_ALLOW_ALL=True` in production
- ❌ Share API keys or database URLs
- ❌ Hardcode secrets in code

---

## 🛡️ .gitignore (Already Configured)

Your `.gitignore` should include:
```
.env
.env.local
.env.*.local
*.pyc
__pycache__/
venv/
.venv/
*.db
db.sqlite3
.DS_Store
/media/
/staticfiles/
```

---

## 🔍 Verifying Configuration

### **Check LOCAL variables are loaded:**
```bash
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DEBUG)
>>> print(settings.DATABASES['default']['ENGINE'])
```

### **Check Vercel deployment:**
1. Go to: https://your-project.vercel.app/api/v1/
2. Should return API response (not 500 error)
3. Check **Function** logs for error messages

---

## 🚀 Quick Reference

**For Local Development:**
```env
SECRET_KEY=dev-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOW_ALL=True
```

**For Vercel Production:**
```env
SECRET_KEY=prod-key-here
DEBUG=False
DATABASE_URL=postgresql://...neon.tech...
CORS_ALLOW_ALL=False
ALLOWED_HOSTS=*.vercel.app,syedishaq.me
```

---

## 📞 Need Help?

- **Django Docs**: https://docs.djangoproject.com/en/stable/ref/settings/
- **python-decouple Docs**: https://github.com/henriquebastos/python-decouple
- **Neon Docs**: https://neon.tech/docs
- **Vercel Docs**: https://vercel.com/docs

---

**Status**: ✅ Configuration guide complete!
