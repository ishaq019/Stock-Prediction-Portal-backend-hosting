# 📖 QUICK START GUIDE - Complete Deployment in 30 Minutes

This guide will take you from **local development to production on Vercel** using Neon PostgreSQL.

---

## 🎯 What You'll Accomplish

By the end of this guide:
- ✅ Setup free PostgreSQL database (Neon)
- ✅ Configure CORS for your domains
- ✅ Deploy Django backend to Vercel
- ✅ Test all API endpoints
- ✅ Monitor your application

**Time Required**: ~30 minutes (one-time setup)

---

## 🗺️ Part 1: Database Setup (5 minutes)

### Skip this if you already have a Neon database!

1. **Follow**: [NEON_SETUP_GUIDE.md](./NEON_SETUP_GUIDE.md)
2. **You'll get**: A connection string like:
   ```
   postgresql://user:password@ep-xxxxx.region.aws.neon.tech/neondb?sslmode=require
   ```
3. **Keep this safe** - you'll need it in the next step!

---

## ⚙️ Part 2: Configure Application (10 minutes)

### STEP 1: Update .env File

1. Open `c:\Users\ahame\Downloads\backend-drf\.env`

2. Update with your Neon connection string:
   ```env
   SECRET_KEY=abc123xyz-your-secret-key-here
   DEBUG=False
   DATABASE_URL=postgresql://user:password@ep-xxxxx.neon.tech/neondb?sslmode=require
   CORS_ALLOW_ALL=False
   ALLOWED_HOSTS=localhost,127.0.0.1,*.vercel.app,syedishaq.me,ishaq019.github.io
   ```

3. **Don't have a SECRET_KEY?** Run this in PowerShell:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Copy the output and paste as your SECRET_KEY value.

4. **Save the file** (Ctrl+S)

### STEP 2: Verify Settings File (ALREADY DONE ✅)

The CORS settings have been updated to include:
- ✅ localhost (all ports)
- ✅ 127.0.0.1 (all ports)
- ✅ syedishaq.me (with www)
- ✅ ishaq019.github.io (GitHub Pages)

---

## 🚀 Part 3: Deploy to Vercel (15 minutes)

### Follow: [VERCEL_DEPLOYMENT_GUIDE.md](./VERCEL_DEPLOYMENT_GUIDE.md)

**Quick Summary:**

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Stock prediction backend"
   git push -u origin main
   ```

2. **Connect to Vercel**
   - Go to: https://vercel.com/new
   - Import your GitHub repository
   - Click "Import"

3. **Add Environment Variables** (in Vercel dashboard)
   - `SECRET_KEY` = Your generated key
   - `DEBUG` = `False`
   - `DATABASE_URL` = Your Neon connection string
   - `ALLOWED_HOSTS` = `*.vercel.app,syedishaq.me,ishaq019.github.io`

4. **Deploy**
   - Click "Deploy"
   - Wait 2-5 minutes
   - ✅ Your API is live!

---

## ✅ Part 4: Test Your API (5 minutes)

### Option A: Using cURL

```bash
# Test registration
curl -X POST https://your-project.vercel.app/api/v1/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123","email":"test@example.com"}'

# Test login
curl -X POST https://your-project.vercel.app/api/v1/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123"}'
```

### Option B: Using Postman

1. Download Postman: https://www.postman.com/downloads/
2. Import collection (we'll provide this)
3. Replace URL with your Vercel domain
4. Run each request

### Option C: Using Browser

Visit these URLs:
- Registration: `https://your-project.vercel.app/api/v1/register/` (POST with JSON)
- Protected view: `https://your-project.vercel.app/api/v1/protected-view/` (should return 401)

---

## 🔍 Monitoring & Troubleshooting

### Check Logs

**Vercel Logs:**
- Go to: https://vercel.com/dashboard
- Select your project
- Click "Functions"
- Click the function to see logs

**Neon Logs:**
- Go to: https://console.neon.tech
- Select your project
- View connection usage and query logs

### Common Issues

| Issue | Solution |
|-------|----------|
| 502 Bad Gateway | Check Vercel logs, verify DATABASE_URL |
| 500 Error | Check error traceback in Vercel logs |
| CORS Error | Make sure frontend domain is in ALLOWED_HOSTS |
| Connection Timeout | Verify Neon database is running |

---

## 📊 CORS Configuration Breakdown

Your application now accepts requests from:

```
✅ Local Development:
   - http://localhost:3000
   - http://localhost:5173
   - http://localhost:8000
   - http://127.0.0.1:3000
   - http://127.0.0.1:5173
   - http://127.0.0.1:8000

✅ Your Domains:
   - https://syedishaq.me
   - https://www.syedishaq.me
   - https://ishaq019.github.io

✅ Vercel:
   - https://your-project.vercel.app (and all subdomains)
```

If you need to add more domains, update `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    # Add your domain here
    'https://your-newdomain.com',
]
```

Then redeploy to Vercel.

---

## 📚 Documentation Files

We've created comprehensive guides:

| File | Purpose |
|------|---------|
| [NEON_SETUP_GUIDE.md](./NEON_SETUP_GUIDE.md) | PostgreSQL database setup |
| [ENV_VARIABLES_GUIDE.md](./ENV_VARIABLES_GUIDE.md) | Environment configuration reference |
| [VERCEL_DEPLOYMENT_GUIDE.md](./VERCEL_DEPLOYMENT_GUIDE.md) | Complete deployment steps |
| [TESTING_SUMMARY.md](./TESTING_SUMMARY.md) | API testing results |

---

## 🎓 Learning Resources

- **Django Official Docs**: https://docs.djangoproject.com/
- **Vercel Python Support**: https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python
- **Neon PostgreSQL**: https://neon.tech/docs
- **REST Framework**: https://www.django-rest-framework.org/

---

## 🔐 Security Checklist

Before deploying:
- [ ] SECRET_KEY is unique and strong
- [ ] DEBUG is set to False
- [ ] Database password is secure
- [ ] CORS is restricted to needed domains
- [ ] ALLOWED_HOSTS doesn't include wildcards except *.vercel.app
- [ ] .env file is in .gitignore
- [ ] No secrets committed to GitHub

---

## 📞 Need Help?

1. **Check error logs** in Vercel dashboard (Functions tab)
2. **Verify environment variables** match your .env file
3. **Test locally** before deploying: `python manage.py runserver`
4. **Check file sizes** - ensure under Vercel limits
5. **Review this guide** - one section may match your issue

---

## 🎉 You're Ready!

Your Django + PostgreSQL + Vercel stack is ready for deployment!

### Next Steps:
1. ✅ Setup Neon database
2. ✅ Configure environment variables
3. ✅ Deploy to Vercel
4. ✅ Test all endpoints
5. ✅ Setup custom domain (optional)
6. ✅ Deploy your frontend

---

**Estimated Cost**: $0 (completely free tier) 🎊

**Go live in 30 minutes!** 🚀
