# 🚀 VERCEL DEPLOYMENT GUIDE (Complete)

Deploy your Django backend to **Vercel FREE TIER** in 10 minutes!

---

## 📋 Prerequisites

✅ **You have:**
- Django backend ready in `c:\Users\ahame\Downloads\backend-drf`
- Neon PostgreSQL connection string (from `NEON_SETUP_GUIDE.md`)
- GitHub account (for pushing code)

---

## 🔧 STEP-BY-STEP DEPLOYMENT

### **PHASE 1: Prepare Your Code**

---

#### **STEP 1: Create GitHub Repository**

1️⃣ Open GitHub: **https://github.com/new**

2️⃣ Fill in the form:
   - **Repository name**: `stock-prediction-backend`
   - **Description**: `Stock prediction API with Django`
   - **Visibility**: `Public` (for free tier)
   - **Initialize with**: Keep unchecked
   - Click **"Create repository"**

   ![Screenshot](https://imgur.com/abc123.png)

3️⃣ You'll see the quick setup page. **Copy the commands** shown.

---

#### **STEP 2: Push Code to GitHub**

1️⃣ Open **PowerShell** or **Git Bash** in your project folder

   ```
   cd c:\Users\ahame\Downloads\backend-drf
   ```

2️⃣ Run these commands (replace `YOUR_USERNAME` with your GitHub username):

   ```bash
   git init
   git add .
   git commit -m "Initial commit: Django backend with stock prediction API"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/stock-prediction-backend.git
   git push -u origin main
   ```

3️⃣ When prompted for password, use your **GitHub Personal Access Token**:
   - Go to: https://github.com/settings/tokens
   - Click **"Generate new token"**
   - Name: `vercel-deploy`
   - Scopes: Select `repo`
   - Create and copy the token
   - Paste in terminal when prompted

4️⃣ Your code is now on GitHub! ✅

   ![GitHub Repo](https://imgur.com/xyz789.png)

---

### **PHASE 2: Configure Vercel**

---

#### **STEP 3: Connect to Vercel**

1️⃣ Go to: **https://vercel.com/new**

2️⃣ Click **"Continue with GitHub"**

   ![Vercel Step 1](https://imgur.com/abc123.png)

3️⃣ Authorize Vercel to access your GitHub account

4️⃣ Select your repository: **`stock-prediction-backend`**

   ![Vercel Step 2](https://imgur.com/def456.png)

5️⃣ Click **"Import"**

---

#### **STEP 4: Configure Build Settings**

On the **Configure Project** page, you'll see several sections:

##### **A. Project Settings**

- **Framework Preset**: Leave as `Other` (Django is already configured)
- **Build Command**: Should auto-fill with:
  ```
  bash build_files.sh
  ```
  *(This is in your `build_files.sh` file)*

- **Output Directory**: Leave empty (Django handles static files)

##### **B. Environment Variables**

1️⃣ In the **Environment Variables** section, click **"Add"**

2️⃣ Add each of these variables:

| Variable Name | Value | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key | `abc123xyz-your-secret` |
| `DEBUG` | `False` | `False` |
| `DATABASE_URL` | Neon connection string | `postgresql://...` |
| `ALLOWED_HOSTS` | Your domains | `*.vercel.app,syedishaq.me` |
| `PRODUCTION_DATABASE` | `True` | `True` |

**Step-by-step for adding variables:**

   ![Vercel Env 1](https://imgur.com/env001.png)

   - Click **"Add"** button
   - Enter name: `SECRET_KEY`
   - Enter value: Your Django secret key
   - Click **"Save"**
   - Repeat for each variable

   ![Vercel Env 2](https://imgur.com/env002.png)

---

**Secret Key Generator:**
If you don't have a SECRET_KEY, generate one:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Run this in PowerShell to generate a key.

---

#### **STEP 5: Review & Deploy**

1️⃣ Scroll down and review all settings

2️⃣ Click **"Deploy"** button

   ![Deploy Button](https://imgur.com/deploy.png)

3️⃣ Watch the deployment progress
   - You'll see build logs in real-time
   - Should take 2-5 minutes

4️⃣ Once complete, you'll see:
   ```
   ✅ Deployment Complete!
   Your app is live at: https://stock-prediction-backend.vercel.app
   ```

   ![Success](https://imgur.com/success.png)

---

### **PHASE 3: Verify & Test**

---

#### **STEP 6: Test Your Deployed API**

1️⃣ Your API is now live at:
   ```
   https://YOUR_PROJECT_NAME.vercel.app/api/v1/
   ```

2️⃣ Test the endpoints:

**Registration Test:**
```bash
curl -X POST https://stock-prediction-backend.vercel.app/api/v1/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123","email":"test@example.com"}'
```

**Expected Response:**
```json
{"username":"testuser","email":"test@example.com"}
```

3️⃣ Or use **Postman** to test:
   - Import the [Postman Collection](#postman-collection)
   - Change URL to your Vercel domain
   - Test each endpoint

---

#### **STEP 7: Update CORS Settings**

If you get CORS errors, update your `.env` on Vercel:

1️⃣ Go to your **Vercel Dashboard**: https://vercel.com/dashboard

2️⃣ Select your project

3️⃣ Click **"Settings"** → **"Environment Variables"**

4️⃣ Add/Update:
   ```
   CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://ishaq019.github.io,https://syedishaq.me,http://localhost:3000
   ```

5️⃣ You need to **redeploy** after changing env vars:
   - Go to **"Deployments"**
   - Click the three dots on the latest deployment
   - Click **"Redeploy"**

   ![Redeploy](https://imgur.com/redeploy.png)

---

## 📊 Monitoring & Logs

### **View Logs:**

1️⃣ **Vercel Dashboard** → Your project → **"Functions"**

2️⃣ Click the function to see real-time logs

3️⃣ See request/response history

### **Database Monitoring:**

1️⃣ Go to **Neon Console**: https://console.neon.tech

2️⃣ Select your project

3️⃣ View:
   - **Resource usage**
   - **Active connections**
   - **Query performance**
   - **Database browser** (manage tables)

---

## 🔗 Postman Collection

Test your API easily with Postman:

### **Import Collection:**

1️⃣ Download: [postman_collection.json](#)

2️⃣ Open **Postman** → **Import** → Select file

3️⃣ Replace `{{BASE_URL}}` with:
   ```
   https://stock-prediction-backend.vercel.app/api/v1
   ```

4️⃣ Run requests!

### **Available Requests:**

```
POST /register/
POST /token/
POST /token/refresh/
GET /protected-view/
POST /predict/
```

---

## ⚙️ Advanced Configuration

### **Custom Domain (Optional)**

1️⃣ Go to **Vercel Dashboard** → Your project → **Settings**

2️⃣ Click **"Domains"**

3️⃣ Add your domain: `api.syedishaq.me`

4️⃣ Follow DNS configuration instructions

5️⃣ Your API is now at: `https://api.syedishaq.me/api/v1/`

---

### **CI/CD Pipeline**

Vercel automatically deploys when you push to GitHub!

```bash
# Make changes locally
git add .
git commit -m "Update prediction model"
git push origin main

# Automatically deploys to Vercel ✅
```

---

## 🐛 Troubleshooting

### **Issue: "502 Bad Gateway"**
- ❓ Problem: Server crashed or not responding
- ✅ Solution:
  1. Check Vercel logs
  2. Verify DATABASE_URL is correct
  3. Check `requirements.txt` is complete
  4. Redeploy

### **Issue: "500 Internal Server Error"**
- ❓ Problem: Code error
- ✅ Solution:
  1. Check function logs in Vercel
  2. Look for error traceback
  3. Fix code locally
  4. Push to GitHub
  5. Auto-redeploy happens

### **Issue: CORS Error in Frontend**
- ❓ Problem: Frontend can't reach API
- ✅ Solution:
  1. Check CORS_ALLOWED_ORIGINS in `.env`
  2. Make sure frontend domain is in the list
  3. Redeploy with new settings

### **Issue: Database Connection Timeout**
- ❓ Problem: Can't connect to Neon
- ✅ Solution:
  1. Verify DATABASE_URL is correct
  2. Check Neon console for active connections
  3. Ensure `sslmode=require` in URL
  4. Try using connection pooling

---

## 📈 Optimization Tips

### **Reduce Cold Start Time:**
1. Keep dependencies minimal (already done ✅)
2. Use `requirements-prod.txt` for production
3. Lazy load heavy modules

### **Monitor Costs:**
- **Neon Free Tier**: 50,000 compute units/month
- **Vercel Free Tier**: 100 deployments/month, 100GB bandwidth
- Both should be **free** for small-to-medium projects

### **Backup Database:**
- Neon provides automatic backups
- Go to **Neon Console** → **Backups**
- Keep 7-day rolling backup

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Vercel project created
- [ ] Environment variables set
- [ ] SECRET_KEY configured
- [ ] DATABASE_URL (Neon) configured
- [ ] Build command working
- [ ] API endpoints responding
- [ ] CORS configured for all frontend origins
- [ ] Database migrations applied
- [ ] Logs checked for errors
- [ ] Frontend can reach API

---

## 🎉 You're Live!

Your Django backend is now deployed on **Vercel** with a **PostgreSQL database on Neon**!

### **Your API URL:**
```
https://stock-prediction-backend.vercel.app/api/v1/
```

### **Next Steps:**
1. Deploy your frontend (React, Vue, etc.)
2. Update frontend to use your API URL
3. Test all endpoints
4. Monitor logs and performance
5. Set up custom domain (optional)

---

## 📞 Support

**Having issues?** Check:
- **Vercel Docs**: https://vercel.com/docs
- **Django Docs**: https://docs.djangoproject.com
- **Neon Docs**: https://neon.tech/docs
- **GitHub Issues**: Link to repo issues

---

**Status**: 🎯 Backend is Production-Ready!
