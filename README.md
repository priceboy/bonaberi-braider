# Phanie Magic Touch

A Next.js portfolio site for Phanie Magic Touch hair studio.

## Deploy to Vercel

1. Push this repository to GitHub, GitLab, or Bitbucket.
2. Import the repository in [Vercel](https://vercel.com/new).
3. Keep the detected **Next.js** framework preset and default build command (`npm run build`).
4. If Supabase is enabled, add the variables from `.env.example` in **Project Settings → Environment Variables** for each required environment.
5. Deploy.

The current site uses bundled mock data, so environment variables are optional until Supabase-backed content is added. Do not commit `.env` files.

## Local development

Use Node.js 20.9 or later.

```bash
npm install
npm run dev
```

Before deploying, run:

```bash
npm run lint
npm run build
```
