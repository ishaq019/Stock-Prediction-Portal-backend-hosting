# 🗄️ Neon PostgreSQL Setup Guide (FREE)

**Neon** is a **serverless PostgreSQL database** perfect for Vercel hosting. It's FREE with generous limits!

---

## 📊 Neon Free Tier Benefits
- **50,000 compute units/month** (plenty for small projects)
- **100 databases** 
- **Unlimited connections**
- **Automatic backups**
- **PostgreSQL 14+** (fully compatible)
- **REST API** built-in

---

## 🖥️ STEP-BY-STEP SETUP (GUI)

### **STEP 1: Create Neon Account**

1️⃣ Open your browser and go to: **https://console.neon.tech/auth/signup**

2️⃣ Click **"Sign up"** button

   ![Step 1](https://imgur.com/rKx5Z8z.png)

3️⃣ Choose **"Sign up with Google"** (easiest option)
   - Or use email to register
   
   ![Step 2](https://imgur.com/8cK5hQJ.png)

4️⃣ Click "Allow" to grant access to your Google account

5️⃣ You'll see the **Welcome page** - click **"Create project"**

   ![Step 3](https://imgur.com/TzBlzCN.png)

---

### **STEP 2: Create Your Database**

1️⃣ On the **Create project** page:
   - **Project name**: `stock-prediction` (or any name)
   - **Database name**: `neondb` (default is fine)
   - **Region**: Select closest to you (e.g., "US East - N. Virginia")
   - Click **"Create project"**

   ![Step 4](https://imgur.com/w8tN3Sc.png)

2️⃣ Wait 30-60 seconds for the database to be created

3️⃣ Once created, you'll see the **Connection details page**

   ![Step 5](https://imgur.com/L9bH7Xq.png)

---

### **STEP 3: Get Your Connection String**

1️⃣ On the connection details page, look for:
   - **Connection String** section
   - You'll see something like:
   ```
   postgresql://user:password@ep-xxxxx.region.aws.neon.tech/neondb?sslmode=require
   ```

2️⃣ **Click the copy icon** next to the connection string
   
   ![Step 6](https://imgur.com/KpQxYZL.png)

3️⃣ It's now copied to your clipboard! ✅

---

### **STEP 4: Update Your .env File**

1️⃣ Open the `.env` file in your project

   **Location**: `c:\Users\ahame\Downloads\backend-drf\.env`

2️⃣ Replace the `DATABASE_URL` line:
   ```
   OLD:
   DATABASE_URL=sqlite:///db.sqlite3
   
   NEW:
   DATABASE_URL=postgresql://user:password@ep-xxxxx.region.aws.neon.tech/neondb?sslmode=require
   ```

3️⃣ Paste the connection string you copied from Neon

4️⃣ Save the file (Ctrl+S)

**Example .env file:**
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://user:password@ep-xxxxx.region.aws.neon.tech/neondb?sslmode=require
CORS_ALLOW_ALL=False
```

---

### **STEP 5: Test Local Connection (Optional)**

Run this in your terminal to test the connection:

```bash
python manage.py migrate
```

If successful, you'll see:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

✅ Your database is working!

---

## 🚀 Next: Vercel Deployment

Once your `.env` is updated with the Neon connection string, follow the **VERCEL_DEPLOYMENT_GUIDE.md**

---

## 🔗 Useful Neon Links

- **Console**: https://console.neon.tech
- **Documentation**: https://neon.tech/docs
- **Support**: support@neon.tech

---

## ❓ Troubleshooting

**Q: Connection times out?**
- A: Make sure SSL is enabled (`sslmode=require`)
- Check if your IP is whitelisted (Neon allows all by default)

**Q: "too many connections" error?**
- A: Vercel serverless creates many connections
- Use **connection pooling** (Neon provides this automatically on paid plans, or use pgBouncer)

**Q: Want to manage data manually?**
- A: Use Neon's **SQL Editor** in the console
- Go to **SQL Editor** → Write queries → Execute

---

**Status**: ✅ Database ready for Vercel deployment!
