#!/usr/bin/env python3
"""
AI News Tracker for EgoistAI.com

Monitors RSS feeds and blog pages of top AI companies for new posts.
When new content is detected, generates a draft analysis article using
Claude CLI (claude --print) and saves it to src/content/drafts/news/.

Usage:
    python scripts/ai-news-tracker.py              # Check all sources
    python scripts/ai-news-tracker.py --dry-run     # Check without generating articles
    python scripts/ai-news-tracker.py --source anthropic  # Check single source
"""

import json
import os
import re
import subprocess
import sys
import hashlib
import logging
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import feedparser
import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
STATE_FILE = SCRIPT_DIR / "tracker-state.json"
DRAFTS_DIR = PROJECT_ROOT / "src" / "content" / "drafts" / "news"
LOGS_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOGS_DIR / "tracker.log"

# Ensure directories exist
DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("ai-news-tracker")

# ---------------------------------------------------------------------------
# HTTP session
# ---------------------------------------------------------------------------
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
})
REQUEST_TIMEOUT = 30

# ---------------------------------------------------------------------------
# Source definitions
# ---------------------------------------------------------------------------
SOURCES = [
    {
        "id": "anthropic",
        "name": "Anthropic",
        "blog_url": "https://www.anthropic.com/news",
        "rss_urls": [
            "https://www.anthropic.com/rss.xml",
            "https://www.anthropic.com/feed.xml",
            "https://www.anthropic.com/news/rss",
        ],
        "priority": True,  # Claude updates get detailed feature analysis
        "scrape_selector": "a[href*='/news/']",
        "link_prefix": "https://www.anthropic.com",
        "min_title_len": 10,
    },
    {
        "id": "openai",
        "name": "OpenAI",
        "blog_url": "https://openai.com/blog",
        "rss_urls": [
            "https://openai.com/blog/rss.xml",
            "https://openai.com/blog/rss",
            "https://openai.com/feed",
        ],
        "scrape_selector": "a[href*='/index/']",
        "link_prefix": "https://openai.com",
    },
    {
        "id": "google_ai",
        "name": "Google AI",
        "blog_url": "https://blog.google/technology/ai/",
        "rss_urls": [
            "https://blog.google/technology/ai/rss/",
            "https://blog.google/rss/",
        ],
        "scrape_selector": "a[href*='/technology/ai/']",
        "link_prefix": "https://blog.google",
    },
    {
        "id": "meta_ai",
        "name": "Meta AI",
        "blog_url": "https://ai.meta.com/blog/",
        "rss_urls": [
            "https://ai.meta.com/blog/rss/",
            "https://ai.meta.com/feed/",
        ],
        "scrape_selector": "a[href*='/blog/']",
        "link_prefix": "https://ai.meta.com",
        "min_title_len": 15,
    },
    {
        "id": "perplexity",
        "name": "Perplexity",
        "blog_url": "https://www.perplexity.ai/hub",
        "rss_urls": [],
        "scrape_selector": "a[href*='/hub/']",
        "link_prefix": "https://www.perplexity.ai",
        "min_title_len": 15,
        "exclude_patterns": ["careers", "login", "signup", "pricing"],
    },
    {
        "id": "midjourney",
        "name": "Midjourney",
        "blog_url": "https://mid-journey.ai/changelog/",
        "rss_urls": [],
        "scrape_selector": "a[href*='changelog']",
        "link_prefix": "",
        "min_title_len": 10,
    },
    {
        "id": "runway",
        "name": "Runway",
        "blog_url": "https://runwayml.com/blog/",
        "rss_urls": [
            "https://runwayml.com/blog/rss/",
            "https://runwayml.com/feed/",
        ],
        "scrape_selector": "a[href*='/blog/']",
        "link_prefix": "https://runwayml.com",
        "min_title_len": 10,
    },
    {
        "id": "deepseek",
        "name": "DeepSeek",
        "blog_url": "https://api-docs.deepseek.com/",
        "rss_urls": [],
        "scrape_selector": "a[href*='deepseek']",
        "link_prefix": "",
        "min_title_len": 10,
        "github_releases": "https://api.github.com/repos/deepseek-ai/DeepSeek-V3/releases",
    },
    {
        "id": "qwen",
        "name": "Qwen (Alibaba)",
        "blog_url": "https://qwenlm.github.io/blog/",
        "rss_urls": [
            "https://qwenlm.github.io/feed.xml",
            "https://qwenlm.github.io/blog/feed.xml",
        ],
        "scrape_selector": "a[href*='/blog/']",
        "link_prefix": "https://qwenlm.github.io",
        "min_title_len": 8,
        "exclude_patterns": ["简体中文", "next", "previous", "»", "«"],
        "github_releases": "https://api.github.com/repos/QwenLM/Qwen3/releases",
    },
    {
        "id": "moonshot",
        "name": "Moonshot AI / Kimi",
        "blog_url": "https://kimi.ai/blog",
        "rss_urls": [],
        "scrape_selector": "a[href*='/blog']",
        "link_prefix": "https://kimi.ai",
        "min_title_len": 10,
    },
    {
        "id": "elevenlabs",
        "name": "ElevenLabs",
        "blog_url": "https://elevenlabs.io/blog",
        "rss_urls": [
            "https://elevenlabs.io/blog/rss/",
            "https://elevenlabs.io/blog/rss",
        ],
        "scrape_selector": "a[href^='/blog/']",
        "link_prefix": "https://elevenlabs.io",
        "min_title_len": 15,
        "exclude_patterns": ["affiliates", "company", "developer", "impact", "product", "research", "careers"],
    },
    {
        "id": "cursor",
        "name": "Cursor",
        "blog_url": "https://www.cursor.com/changelog",
        "rss_urls": [],
        "scrape_selector": "a[href*='/changelog']",
        "link_prefix": "https://www.cursor.com",
        "min_title_len": 5,
    },
    {
        "id": "black_forest_labs",
        "name": "Black Forest Labs / Flux",
        "blog_url": "https://blackforestlabs.ai/blog/",
        "rss_urls": [
            "https://blackforestlabs.ai/feed/",
        ],
        "scrape_selector": "article a, .post a",
        "link_prefix": "https://blackforestlabs.ai",
        "min_title_len": 10,
    },
]

# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------
def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError) as e:
            log.warning("Could not load state file, starting fresh: %s", e)
    return {"seen": {}, "last_run": None}


def save_state(state: dict):
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def post_id(url: str, title: str = "") -> str:
    """Generate a deterministic ID for a post."""
    raw = (url or title).strip().lower()
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Feed / scrape helpers
# ---------------------------------------------------------------------------
def try_rss(source: dict) -> list[dict]:
    """Try to fetch posts from RSS feed URLs."""
    posts = []
    for rss_url in source.get("rss_urls", []):
        try:
            log.debug("Trying RSS: %s", rss_url)
            feed = feedparser.parse(rss_url, agent=SESSION.headers["User-Agent"])
            if feed.bozo and not feed.entries:
                continue
            for entry in feed.entries[:15]:  # last 15 entries
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                summary = entry.get("summary", entry.get("description", "")).strip()
                # Clean HTML from summary
                if summary:
                    summary = BeautifulSoup(summary, "html.parser").get_text(separator=" ")[:500]
                pub_date = ""
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    try:
                        pub_date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
                    except Exception:
                        pass
                if title and link:
                    posts.append({
                        "title": title,
                        "url": link,
                        "summary": summary,
                        "date": pub_date,
                        "source_name": source["name"],
                        "source_id": source["id"],
                        "priority": source.get("priority", False),
                    })
            if posts:
                log.info("RSS success for %s (%s): %d posts", source["name"], rss_url, len(posts))
                return posts
        except Exception as e:
            log.debug("RSS failed for %s: %s", rss_url, e)
    return posts


def scrape_blog(source: dict) -> list[dict]:
    """Fallback: scrape the blog page for post links."""
    posts = []
    blog_url = source.get("blog_url")
    if not blog_url:
        return posts

    try:
        log.debug("Scraping blog page: %s", blog_url)
        resp = SESSION.get(blog_url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        selector = source.get("scrape_selector", "a")
        link_prefix = source.get("link_prefix", "")

        seen_urls = set()
        for a_tag in soup.select(selector)[:30]:
            href = a_tag.get("href", "").strip()
            if not href or href == "/" or href == "#":
                continue

            # Build full URL
            if href.startswith("/"):
                href = link_prefix + href
            elif not href.startswith("http"):
                continue

            # Skip if it's just the blog index itself
            if href.rstrip("/") == blog_url.rstrip("/"):
                continue

            # Deduplicate
            if href in seen_urls:
                continue
            seen_urls.add(href)

            title = a_tag.get_text(strip=True)
            # If the link text is too short, try to find a heading nearby
            if len(title) < 5:
                parent = a_tag.parent
                if parent:
                    heading = parent.find(["h1", "h2", "h3", "h4"])
                    if heading:
                        title = heading.get_text(strip=True)

            if not title or len(title) < 3:
                continue

            # Apply minimum title length filter
            min_len = source.get("min_title_len", 5)
            if len(title) < min_len:
                continue

            # Apply exclude patterns
            exclude_patterns = source.get("exclude_patterns", [])
            title_lower = title.lower().strip()
            if any(pat.lower() in title_lower for pat in exclude_patterns):
                continue

            # Skip obvious navigation links
            nav_words = {"home", "about", "contact", "login", "sign up", "sign in",
                         "pricing", "docs", "documentation", "api", "careers", "jobs",
                         "privacy", "terms", "next", "previous", "back"}
            if title_lower in nav_words:
                continue

            posts.append({
                "title": title,
                "url": href,
                "summary": "",
                "date": "",
                "source_name": source["name"],
                "source_id": source["id"],
                "priority": source.get("priority", False),
            })

        if posts:
            log.info("Scraped %s: %d links found", source["name"], len(posts))
    except Exception as e:
        log.warning("Failed to scrape %s: %s", blog_url, e)

    return posts


def check_github_releases(source: dict) -> list[dict]:
    """Check GitHub releases API for sources that use it."""
    posts = []
    gh_url = source.get("github_releases")
    if not gh_url:
        return posts

    try:
        resp = SESSION.get(gh_url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        releases = resp.json()
        for release in releases[:10]:
            title = release.get("name") or release.get("tag_name", "")
            url = release.get("html_url", "")
            body = release.get("body", "")[:500]
            pub_date = ""
            if release.get("published_at"):
                pub_date = release["published_at"][:10]
            if title and url:
                posts.append({
                    "title": f"{source['name']}: {title}",
                    "url": url,
                    "summary": body,
                    "date": pub_date,
                    "source_name": source["name"],
                    "source_id": source["id"],
                    "priority": source.get("priority", False),
                })
        if posts:
            log.info("GitHub releases for %s: %d found", source["name"], len(posts))
    except Exception as e:
        log.warning("GitHub releases check failed for %s: %s", source["name"], e)

    return posts


def fetch_posts(source: dict) -> list[dict]:
    """Fetch posts from a source, trying RSS first then scraping."""
    posts = try_rss(source)
    if not posts:
        posts = scrape_blog(source)
    # Also check GitHub releases if configured
    gh_posts = check_github_releases(source)
    if gh_posts:
        seen_urls = {p["url"] for p in posts}
        for p in gh_posts:
            if p["url"] not in seen_urls:
                posts.append(p)
    return posts


# ---------------------------------------------------------------------------
# Article generation
# ---------------------------------------------------------------------------
def slugify(text: str) -> str:
    """Create a URL-friendly slug from text."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text[:80].strip('-')


def estimate_read_time(text: str) -> str:
    """Estimate read time based on word count."""
    words = len(text.split())
    minutes = max(3, round(words / 230))
    return f"{minutes} min read"


def generate_article(post: dict) -> Optional[str]:
    """Use claude --print CLI to generate an analysis article."""
    today = datetime.now().strftime("%Y-%m-%d")

    if post.get("priority"):
        # Anthropic/Claude specific: detailed feature analysis + usage guide
        prompt = f"""You are writing for EgoistAI.com, a sharp, opinionated AI news and analysis site. The tone is confident, direct, sometimes irreverent — like a knowledgeable friend who cuts through the hype.

Write a detailed analysis article about this Anthropic/Claude update:

Title: {post['title']}
URL: {post['url']}
Summary: {post['summary']}
Date: {post['date'] or today}

The article MUST include:
1. A compelling opening that explains why this matters
2. A detailed breakdown of the new features or changes
3. A "How to Use It" section with step-by-step instructions where applicable
4. Practical examples and use cases
5. How this compares to competitors (OpenAI, Google, etc.)
6. Your honest take — what's genuinely impressive and what's overhyped
7. A conclusion on what this means for AI users

Write 1200-2000 words. Use markdown formatting with ## headers. Include practical tips.
Do NOT include frontmatter — just the article body in markdown.
Do NOT start with "# Title" — just begin with the opening paragraph.
Be specific and actionable, not vague."""
    else:
        prompt = f"""You are writing for EgoistAI.com, a sharp, opinionated AI news and analysis site. The tone is confident, direct, sometimes irreverent — like a knowledgeable friend who cuts through the hype.

Write an analysis article about this AI news:

Title: {post['title']}
Source: {post['source_name']}
URL: {post['url']}
Summary: {post['summary']}
Date: {post['date'] or today}

The article should:
1. Open with why this matters (or doesn't)
2. Break down what was announced
3. Analyze the implications for users, developers, or the industry
4. Compare to competitors where relevant
5. Give an honest verdict — cut through the marketing

Write 800-1500 words. Use markdown formatting with ## headers.
Do NOT include frontmatter — just the article body in markdown.
Do NOT start with "# Title" — just begin with the opening paragraph.
Be specific, not vague. Have opinions."""

    try:
        log.info("Generating article for: %s", post["title"])
        result = subprocess.run(
            ["claude", "--print", "--model", "sonnet", prompt],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            cwd=str(PROJECT_ROOT),
        )

        if result.returncode != 0:
            log.error("claude --print failed (exit %d): %s", result.returncode, result.stderr[:500])
            return None

        body = result.stdout.strip()
        if len(body) < 200:
            log.warning("Generated article too short (%d chars), skipping", len(body))
            return None

        return body

    except subprocess.TimeoutExpired:
        log.error("claude --print timed out for: %s", post["title"])
        return None
    except FileNotFoundError:
        log.error("claude CLI not found. Make sure 'claude' is in PATH.")
        return None
    except Exception as e:
        log.error("Article generation failed: %s", e)
        return None


def generate_title(post: dict) -> str:
    """Generate a catchy article title based on the post."""
    try:
        prompt = f"""Generate a single catchy, click-worthy article title for an AI news analysis about:
"{post['title']}" from {post['source_name']}.

Rules:
- Make it intriguing but not clickbait
- Keep it under 70 characters
- Use a dash or colon for structure if needed
- Don't use quotes in the title
- Output ONLY the title, nothing else"""

        result = subprocess.run(
            ["claude", "--print", "--model", "sonnet", prompt],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(PROJECT_ROOT),
        )

        if result.returncode == 0 and result.stdout.strip():
            title = result.stdout.strip().strip('"').strip("'")
            # Remove any markdown or extra formatting
            title = re.sub(r'^#+\s*', '', title)
            title = title.split('\n')[0].strip()
            if 10 < len(title) < 100:
                return title

    except Exception as e:
        log.debug("Title generation failed, using original: %s", e)

    # Fallback: use original title with a twist
    return post["title"]


def generate_excerpt(title: str, body: str) -> str:
    """Generate a 140-180 character excerpt."""
    # Take first meaningful paragraph
    paragraphs = [p.strip() for p in body.split('\n\n') if p.strip() and not p.strip().startswith('#')]
    if paragraphs:
        text = paragraphs[0]
        # Strip markdown
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        if len(text) > 180:
            text = text[:177] + "..."
        elif len(text) < 140:
            # Pad with next paragraph
            if len(paragraphs) > 1:
                text = text + " " + paragraphs[1]
                text = text[:177] + "..."
        return text
    return title[:180]


def generate_tags(post: dict) -> list[str]:
    """Generate relevant tags."""
    tags = ["ai", "news"]
    source_tags = {
        "anthropic": ["anthropic", "claude"],
        "openai": ["openai", "chatgpt"],
        "google_ai": ["google", "gemini"],
        "meta_ai": ["meta", "llama"],
        "perplexity": ["perplexity", "search"],
        "midjourney": ["midjourney", "image generation"],
        "runway": ["runway", "video generation"],
        "deepseek": ["deepseek"],
        "qwen": ["qwen", "alibaba"],
        "moonshot": ["moonshot", "kimi"],
        "elevenlabs": ["elevenlabs", "voice ai"],
        "cursor": ["cursor", "coding"],
        "black_forest_labs": ["flux", "image generation"],
    }
    tags.extend(source_tags.get(post["source_id"], []))

    # Add tags based on title keywords
    title_lower = post["title"].lower()
    keyword_tags = {
        "model": "ai models",
        "api": "api",
        "open source": "open source",
        "release": "release",
        "update": "update",
        "safety": "ai safety",
        "agent": "ai agents",
        "multimodal": "multimodal",
        "vision": "computer vision",
        "voice": "voice ai",
        "code": "coding",
        "image": "image generation",
        "video": "video generation",
    }
    for keyword, tag in keyword_tags.items():
        if keyword in title_lower and tag not in tags:
            tags.append(tag)

    return tags


def save_article(post: dict, body: str, title: str):
    """Save the generated article as a markdown file."""
    today = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(title)
    filename = f"{slug}.md"
    filepath = DRAFTS_DIR / filename

    # Don't overwrite existing drafts
    if filepath.exists():
        slug = slug + "-" + post_id(post["url"])[:6]
        filename = f"{slug}.md"
        filepath = DRAFTS_DIR / filename

    excerpt = generate_excerpt(title, body)
    read_time = estimate_read_time(body)
    tags = generate_tags(post)

    frontmatter = f"""---
title: "{title.replace('"', '\\"')}"
excerpt: "{excerpt.replace('"', '\\"')}"
category: "News"
categorySlug: "news"
image: "/images/{slug}.webp"
date: "{today}"
readTime: "{read_time}"
author: "EgoistAI"
featured: false
tags: {json.dumps(tags)}
sources:
  - name: "{post['source_name']} Blog"
    url: "{post['url']}"
---"""

    content = frontmatter + "\n\n" + body + "\n"
    filepath.write_text(content, encoding="utf-8")
    log.info("Saved draft: %s", filepath)
    return filepath


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def process_source(source: dict, state: dict, dry_run: bool = False) -> list[dict]:
    """Process a single source. Returns list of new posts found."""
    source_id = source["id"]
    log.info("Checking %s...", source["name"])

    try:
        posts = fetch_posts(source)
    except Exception as e:
        log.error("Failed to fetch %s: %s", source["name"], e)
        return []

    if not posts:
        log.info("No posts found for %s", source["name"])
        return []

    # Filter to new posts only
    seen = state.get("seen", {})
    new_posts = []
    for p in posts:
        pid = post_id(p["url"], p["title"])
        if pid not in seen:
            new_posts.append(p)
            # Mark as seen immediately
            seen[pid] = {
                "title": p["title"],
                "url": p["url"],
                "source": source_id,
                "first_seen": datetime.now(timezone.utc).isoformat(),
                "article_generated": False,
            }

    if not new_posts:
        log.info("No new posts from %s", source["name"])
        return []

    log.info("Found %d new post(s) from %s", len(new_posts), source["name"])

    if dry_run:
        for p in new_posts:
            log.info("  [DRY RUN] Would process: %s", p["title"])
        return new_posts

    # Generate articles for new posts
    for p in new_posts:
        pid = post_id(p["url"], p["title"])
        try:
            body = generate_article(p)
            if body:
                title = generate_title(p)
                filepath = save_article(p, body, title)
                seen[pid]["article_generated"] = True
                seen[pid]["draft_path"] = str(filepath)
                log.info("Article generated: %s -> %s", p["title"], filepath.name)
            else:
                log.warning("No article generated for: %s", p["title"])
        except Exception as e:
            log.error("Error generating article for '%s': %s", p["title"], e)

    state["seen"] = seen
    return new_posts


def main():
    parser = argparse.ArgumentParser(description="AI News Tracker for EgoistAI.com")
    parser.add_argument("--dry-run", action="store_true", help="Check feeds without generating articles")
    parser.add_argument("--source", type=str, help="Check a single source by ID")
    parser.add_argument("--reset", action="store_true", help="Reset state file and start fresh")
    parser.add_argument("--list-sources", action="store_true", help="List all configured sources")
    args = parser.parse_args()

    if args.list_sources:
        print("Configured sources:")
        for s in SOURCES:
            priority = " [PRIORITY]" if s.get("priority") else ""
            print(f"  {s['id']:20s} {s['name']}{priority}")
        return

    log.info("=" * 60)
    log.info("AI News Tracker starting")
    log.info("=" * 60)

    if args.reset:
        log.info("Resetting state file")
        save_state({"seen": {}, "last_run": None})

    state = load_state()
    total_new = 0
    total_articles = 0

    sources_to_check = SOURCES
    if args.source:
        sources_to_check = [s for s in SOURCES if s["id"] == args.source]
        if not sources_to_check:
            log.error("Unknown source: %s", args.source)
            log.info("Available sources: %s", ", ".join(s["id"] for s in SOURCES))
            sys.exit(1)

    for source in sources_to_check:
        try:
            new_posts = process_source(source, state, dry_run=args.dry_run)
            total_new += len(new_posts)
            total_articles += sum(
                1 for p in new_posts
                if state.get("seen", {}).get(post_id(p["url"], p["title"]), {}).get("article_generated")
            )
        except Exception as e:
            log.error("Unhandled error processing %s: %s", source["name"], e)

        # Save state after each source (in case of crash)
        save_state(state)

    log.info("-" * 60)
    log.info("Run complete: %d new posts found, %d articles generated", total_new, total_articles)
    log.info("Drafts directory: %s", DRAFTS_DIR)
    log.info("=" * 60)


if __name__ == "__main__":
    main()
