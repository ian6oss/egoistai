---
title: "Build a Complete Website With AI in 30 Minutes"
excerpt: "No coding experience needed. This step-by-step tutorial shows you how to go from zero to a live, professional website using Cursor, Claude Code, and v0 — all in under 30 minutes."
category: "Tutorials"
categorySlug: "tutorials"
image: "/images/build-complete-website-with-ai-30-minutes.webp"
date: "2026-03-24"
readTime: "14 min read"
author: "EgoistAI"
tags: ["ai", "web development", "cursor", "claude code", "v0", "tutorial", "coding", "no code"]
featured: false
---

Two years ago, building a professional website from scratch required either weeks of learning to code or thousands of dollars to hire a developer. Today, AI tools have compressed that timeline to 30 minutes and zero dollars.

This isn't about drag-and-drop website builders with ugly templates. We're building a real, custom website with modern technology — the same tech stack that professional developers use. AI just happens to write the code for us.

By the end of this tutorial, you'll have a live, responsive, professional-looking website that you built yourself. Let's go.

![Building a website with AI tools](/images/ai-website-building-tutorial.webp)

## What We're Building

For this tutorial, we're building a personal portfolio website. It'll include:

- A hero section with your name and tagline
- An "About Me" section
- A project showcase grid
- A skills/services section
- A contact form
- Responsive design (looks good on mobile, tablet, and desktop)
- Clean, modern aesthetics

You can adapt this process to build any type of website: a business landing page, a blog, a SaaS product page, or anything else.

## The Tools We're Using

We'll use three AI tools, each for a different phase of the build:

**Vercel v0** (Free) — For generating the initial UI components and design. Think of it as your AI designer.

**Cursor** (Free tier available) — An AI-powered code editor. This is where we'll assemble and customize the website.

**Claude** (Free tier) — For troubleshooting, explaining code, and handling any customization that v0 and Cursor can't.

You'll also need:
- **Node.js** installed on your computer (free, takes 2 minutes to install)
- **A GitHub account** (free)
- **A Vercel account** (free) — for hosting the live website

Total cost: $0.

## Phase 1: Generate UI Components with v0 (10 Minutes)

### Step 1: Open v0 and describe your hero section

Go to v0.dev and sign in with your Vercel account. In the prompt box, type something like this:

"Create a modern portfolio hero section with a large heading showing the name 'Alex Chen', a subtitle that says 'Full-Stack Developer & Designer', a brief one-paragraph bio, and two CTA buttons: 'View My Work' and 'Get In Touch'. Use a clean, minimal design with a dark color scheme. Include a subtle gradient background."

v0 will generate a React component with Tailwind CSS styling. It usually gives you a few variations to choose from.

### Step 2: Pick the best version and iterate

Look at the options v0 gives you. Pick the one closest to what you want, then refine with follow-up prompts:

- "Make the gradient more subtle"
- "Increase the font size of the heading"
- "Add a profile image placeholder on the right side"
- "Make it responsive — stack vertically on mobile"

Spend 2-3 minutes iterating until the hero section looks right.

### Step 3: Generate the remaining sections

Repeat the process for each section of your website:

**About section:**
"Create an About Me section with a large image on the left and text content on the right. Include a heading, two paragraphs of bio text, and a list of key stats (years of experience, projects completed, clients served). Clean, minimal design matching a dark theme."

**Projects grid:**
"Create a project showcase grid with 6 project cards. Each card should have an image, project title, brief description, and tech stack tags. Use a 3-column grid on desktop, 2 on tablet, 1 on mobile. Add a hover effect that scales the card slightly."

**Skills section:**
"Create a skills/services section with 4 service cards in a grid. Each card has an icon placeholder, service title, and brief description. Use a clean card design with subtle borders."

**Contact section:**
"Create a contact form section with fields for name, email, and message. Include a submit button and contact information (email, location, social links) displayed alongside the form."

**Navigation:**
"Create a fixed top navigation bar with a logo/name on the left and navigation links on the right: Home, About, Projects, Skills, Contact. Include a mobile hamburger menu that opens a full-screen overlay."

**Footer:**
"Create a minimal footer with copyright text, social media icon links, and a 'Back to Top' button."

For each component, v0 gives you the React/Tailwind code. Keep the browser tab open — we'll use this code in the next phase.

![v0 component generation interface](/images/v0-component-generation.webp)

## Phase 2: Assemble in Cursor (15 Minutes)

### Step 4: Set up the project

Open your terminal and run these commands to create a new Next.js project (this is the framework v0's code is designed for):

```
npx create-next-app@latest my-portfolio
```

When it asks you questions during setup, accept the defaults — they'll include TypeScript, Tailwind CSS, and App Router, which is exactly what we need.

Then open the project in Cursor:

```
cd my-portfolio
cursor .
```

### Step 5: Let Cursor assemble the components

Here's where the magic happens. Open Cursor's AI chat (Cmd+L on Mac, Ctrl+L on Windows) and give it a comprehensive prompt:

"I'm building a portfolio website. I have the following sections that need to be assembled into a single-page website: Hero, About, Projects, Skills, Contact, Navigation, and Footer.

Create the following file structure:
- Components for each section in /components/
- A main page that imports and renders all sections in order
- A clean global stylesheet

Here's the code for each component: [paste your v0 components]

Make sure:
- The navigation links scroll smoothly to each section
- The page is fully responsive
- All sections are connected with consistent spacing
- The color scheme is consistent throughout (dark theme)"

Cursor will create the files, write the code, and assemble everything. This is usually the most satisfying moment — watching AI build your website in real-time.

### Step 6: Preview and customize

Start the development server:

```
npm run dev
```

Open your browser to localhost:3000 and you'll see your website. It probably won't be perfect on the first try, and that's fine. Use Cursor's AI to make adjustments.

Common fixes to ask Cursor for:

- "The spacing between sections is too tight. Add more padding."
- "The mobile menu isn't working. Fix the toggle logic."
- "I want the project cards to link to external URLs. Add an href prop."
- "Change the primary accent color from blue to emerald green."
- "Add smooth scroll behavior when clicking navigation links."
- "The contact form needs validation — check for valid email format."

Each request takes Cursor a few seconds to implement. You're essentially having a conversation with your developer, except your developer works at the speed of light and never pushes back on requests.

### Step 7: Add your real content

Replace all placeholder text with your actual content:

- Your real name and title
- Your actual bio
- Real project descriptions and images
- Your genuine skills and services
- Your contact information

You can do this manually in the code (it's just text) or ask Cursor: "Replace all placeholder content with the following real information: [paste your content]."

### Step 8: Add images

Drop your images into the /public/images/ folder. Ask Cursor to update the image references:

"Update all image placeholders to use these files from /public/images/: profile.jpg for the hero and about sections, project1.jpg through project6.jpg for the project cards."

For project screenshots, you can use real images or generate placeholder images with an AI image tool. If you don't have images ready, ask Cursor to add a nice gradient placeholder that looks intentional rather than broken.

![Cursor AI code editing interface](/images/cursor-ai-editing.webp)

## Phase 3: Deploy to the Internet (5 Minutes)

### Step 9: Push to GitHub

If you don't have Git set up, ask Cursor to help:

"Initialize a git repository, create an initial commit with all files, and give me the commands to push to a new GitHub repository."

Cursor will generate the exact commands. Run them in the terminal:

```
git init
git add .
git commit -m "Initial portfolio website"
git remote add origin https://github.com/yourusername/my-portfolio.git
git push -u origin main
```

### Step 10: Deploy on Vercel

Go to vercel.com and sign in. Click "New Project," connect your GitHub account, and select your portfolio repository.

Vercel auto-detects that it's a Next.js project and configures everything automatically. Click "Deploy."

In about 60 seconds, your website is live on the internet with a URL like `my-portfolio.vercel.app`. That's it. A real, professional website, live on the internet, built in under 30 minutes.

### Step 11: Connect a custom domain (optional)

If you have a custom domain (like yourname.com), you can connect it in Vercel's dashboard under Settings > Domains. Add your domain, update your DNS records as instructed, and Vercel handles the rest — including free SSL certificates.

Domain names cost about $10-15/year from providers like Namecheap, Google Domains, or Cloudflare. It's the only cost in this entire process.

## Troubleshooting Common Issues

### "My components look different assembled than they did in v0"

This usually happens because of CSS conflicts. Ask Cursor: "Some sections look different than expected. Check for CSS conflicts and fix any conflicting styles between components."

### "The mobile layout is broken"

Ask Cursor: "The layout breaks on mobile screens. Check all components for responsive design and fix any elements that don't adapt properly to small screens. Use Tailwind's responsive prefixes (sm:, md:, lg:)."

### "The build fails when I try to deploy"

Copy the error message and paste it to Cursor or Claude: "My Next.js build fails with this error: [paste error]. Fix it." Build errors are usually minor issues like missing imports or TypeScript type errors, and AI handles them instantly.

### "The contact form doesn't actually send emails"

A basic HTML form won't send emails on its own. Ask Cursor: "Make the contact form functional. Use Formspree or a similar service so form submissions get sent to my email address." Formspree has a free tier that handles up to 50 submissions per month.

### "I want to add a blog"

This is a bigger addition but still doable with AI. Ask Cursor: "Add a blog section to my portfolio using MDX files for content. Create a /blog route with a list page and individual post pages. Add 2-3 sample blog posts." This might take an extra 15-20 minutes of iteration.

## Going Further: Advanced Customizations

Once your basic site is live, here are some enhancements you can add with AI assistance:

### Animations
"Add subtle scroll-triggered animations using Framer Motion. Fade in each section as the user scrolls to it. Keep it tasteful — no bouncing or spinning."

### Dark/Light Mode Toggle
"Add a dark/light mode toggle to the navigation. Default to dark mode. Save the user's preference in localStorage."

### Analytics
"Add Vercel Analytics and Google Analytics to track page views and visitor behavior."

### Performance Optimization
"Optimize the website for performance. Add next/image optimization for all images, lazy loading for below-the-fold content, and proper meta tags for SEO."

### SEO
"Add comprehensive SEO meta tags, Open Graph tags for social sharing, and a sitemap.xml. Target the keyword 'full stack developer portfolio'."

Each of these can be accomplished in 5-10 minutes with Cursor's AI assistance.

![Final portfolio website preview](/images/ai-built-portfolio-preview.webp)

## What We Just Did

Let's recap. In 30 minutes, we:

1. Designed UI components with v0 (AI generated the visual design)
2. Assembled a complete website with Cursor (AI wrote the code)
3. Troubleshot and customized with Claude (AI fixed issues)
4. Deployed to the internet with Vercel (free hosting)

The result is a professional, responsive, custom website running on the same technology stack (Next.js, React, Tailwind CSS) that companies pay developers $150K+ per year to build.

Is it as good as what a senior developer would produce from scratch? No. A skilled developer would add nuances, performance optimizations, and architectural decisions that AI wouldn't think of unprompted. But it's better than 90% of the portfolio websites on the internet, and it cost you nothing but 30 minutes of your time.

## The Bigger Picture

This tutorial is about more than building a portfolio site. It's about a fundamental shift in who can create software.

The barrier to building on the web used to be technical skill. You needed to learn HTML, CSS, JavaScript, a framework, deployment, hosting — hundreds of hours of learning before you could build anything meaningful.

AI hasn't eliminated the value of that knowledge (skilled developers build much better things with AI than beginners do), but it has dramatically lowered the barrier to getting started. If you can describe what you want in plain English, you can build it.

That's true for portfolio sites, landing pages, web apps, mobile apps, browser extensions, and pretty much any software project. The tools we used today — v0, Cursor, Claude — work for all of them.

The only question is what you want to build next.

---

*This tutorial was tested and verified in March 2026. Tool interfaces and capabilities may have changed since publication. All tools used have free tiers sufficient to complete this project.*
