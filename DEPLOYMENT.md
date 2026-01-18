# 🚀 Portfolio Website Deployment Guide

## GitHub Pages Setup (Free Hosting!)

### Step 1: Initialize Git Repository
```bash
cd sales-analytics-dashboard
git init
git add .
git commit -m "Initial commit: Sales Analytics Portfolio"
```

### Step 2: Create GitHub Repository
1. Go to GitHub.com and create a new repository
2. Name it: `product-portfolio` or `sales-analytics-dashboard`
3. Make it **Public** (required for free GitHub Pages)
4. **Don't** initialize with README (we already have one)

### Step 3: Push to GitHub
```bash
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
git branch -M main
git push -u origin main
```

### Step 4: Enable GitHub Pages
1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll to **Pages** section (left sidebar)
4. Under **Source**, select:
   - Branch: `main`
   - Folder: `/docs`
5. Click **Save**

### Step 5: Access Your Live Site
After 2-3 minutes, your site will be live at:
```
https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/
```

---

## 📝 Before You Deploy: Personalize Your Portfolio

### Update These Files:

#### 1. `docs/index.html` (Line 67)
```html
<h1 class="text-5xl md:text-7xl font-bold mb-6 text-slate-900 dark:text-white">
    Your Name  <!-- ⚠️ CHANGE THIS -->
</h1>
```

#### 2. Footer Links (Lines 579-590)
```html
<a href="https://linkedin.com/in/yourprofile" target="_blank">  <!-- ⚠️ CHANGE -->
<a href="https://github.com/yourusername" target="_blank">  <!-- ⚠️ CHANGE -->
<a href="mailto:your.email@example.com">  <!-- ⚠️ CHANGE -->
```

#### 3. `README.md` (Optional)
Update the author section at the bottom with your name.

---

## 🎨 Customization Options

### Change Color Scheme
In `docs/index.html`, find the `tailwind.config` section (line 9):
```javascript
colors: {
    primary: '#3b82f6',  // Change this hex code
    secondary: '#8b5cf6',  // And this one
}
```

**Color Palette Ideas:**
- Professional Blue: `#2563eb` and `#4f46e5`
- Startup Green: `#10b981` and `#059669`
- Bold Purple: `#8b5cf6` and `#7c3aed`
- Corporate Dark: `#1e293b` and `#334155`

### Add Google Analytics (Optional)
Before `</head>` tag, add:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-GA-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR-GA-ID');
</script>
```

---

## 🔗 Adding to Your Application

### Resume/CV
```
Portfolio: https://yourusername.github.io/product-portfolio
```

### LinkedIn Profile
1. Go to **Edit Profile**
2. Add to **Websites** section
3. Label it: "Product Management Portfolio"

### Cover Letters
```
"I've created a comprehensive sales analytics dashboard demonstrating 
my data-driven PM approach. You can view my analysis and insights at:
[your GitHub Pages URL]"
```

---

## 🐛 Troubleshooting

### Site Not Loading?
- Wait 5-10 minutes after enabling Pages
- Check Settings → Pages shows "Your site is published"
- Verify `/docs` folder is selected (not `/root`)

### Visualizations Not Showing?
Make sure the HTML files are in `docs/reports/`:
```
docs/
├── index.html
└── reports/
    ├── sales_trend.html
    ├── regional_performance.html
    └── category_distribution.html
```

### 404 Error on Reports?
Links are case-sensitive! Verify filenames match exactly.

---

## 📊 Tracking Portfolio Views

Add a simple view counter using [hits.sh](https://hits.sh):

In `docs/index.html` footer, add:
```html
<img src="https://hits.sh/github.com/yourusername/yourrepo.svg?style=flat-square&label=Portfolio%20Views" alt="Views">
```

---

## 🎯 Next Steps After Deployment

1. **Share on LinkedIn**: Post about your new portfolio
2. **Include in Applications**: Add the URL to every PM application
3. **Get Feedback**: Share with mentors or PM communities
4. **Keep Updated**: Add new projects as you build them

---

## 🚀 Advanced: Custom Domain (Optional)

Want `www.yourname.com` instead of GitHub's URL?

1. Buy a domain ($10-15/year) from Namecheap or Google Domains
2. In your repo, create file: `docs/CNAME`
3. Add your domain: `www.yourname.com`
4. Configure DNS records (A records pointing to GitHub IPs)
5. Follow [GitHub's custom domain guide](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

---

**Questions?** Open an issue on GitHub or check the [GitHub Pages docs](https://pages.github.com)

**Ready to deploy? Run the commands above and your portfolio will be live in minutes!** 🎉
