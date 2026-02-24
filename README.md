# Dealguys

Dealguys is a static deals website for posting and browsing affiliate offers, coupon codes, and freebies.

## Run locally

```bash
python3 -m http.server 4173
```

Then open: `http://localhost:4173`

## Deploy on GitHub Pages

This repo includes an automated workflow at `.github/workflows/deploy-pages.yml`.

### 1) Push this repo to GitHub

```bash
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

### 2) Enable GitHub Pages

1. Go to **Settings → Pages** in your GitHub repo.
2. Under **Build and deployment**, set **Source** to **GitHub Actions**.

### 3) Trigger deployment

- Any push to `main` deploys automatically, or
- Run the workflow manually from **Actions → Deploy Dealguys to GitHub Pages**.

After deployment, your site URL will look like:

`https://<your-username>.github.io/<your-repo>/`
