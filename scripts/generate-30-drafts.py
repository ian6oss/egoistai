#!/usr/bin/env python3
"""Generate 30 draft articles for EgoistAI using Gemini 2.5 Flash API."""

import json
import time
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

API_KEY = open("/Users/ian/.config/mogulfeed/.google-api-key").read().strip()
DRAFTS_DIR = "/Users/ian/egoistai/src/content/drafts"

def generate_article(prompt, attempt=0):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 8192, "temperature": 0.8}
    }).encode()
    req = Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        resp = urlopen(req, timeout=120)
        data = json.loads(resp.read())
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (HTTPError, URLError, KeyError, Exception) as e:
        if attempt < 2:
            print(f"  Retry {attempt+1} after error: {e}")
            time.sleep(5)
            return generate_article(prompt, attempt+1)
        raise

# 30 articles: 6 per category, prioritizing TODO items from content calendar
ARTICLES = [
    # === TOOLS (6) ===
    {
        "slug": "ai-design-tools-figma-alternatives",
        "title": "AI Design Tools: Figma AI vs Canva AI vs Framer AI — Which One Actually Delivers?",
        "category": "Tools",
        "categorySlug": "tools",
        "tags": ["AI design", "Figma AI", "Canva AI", "Framer AI", "design tools"],
        "topic": "Compare Figma AI, Canva AI, and Framer AI design tools. Cover features, pricing, real-world performance, who each tool is best for. Include comparison table."
    },
    {
        "slug": "ai-email-tools-superhuman-alternatives",
        "title": "AI Email Tools: Superhuman vs Spark AI vs Gmail AI — Your Inbox Deserves Better",
        "category": "Tools",
        "categorySlug": "tools",
        "tags": ["AI email", "Superhuman", "Spark AI", "Gmail AI", "productivity"],
        "topic": "Compare AI email tools: Superhuman, Spark AI, Gmail AI features. Cover AI summarization, smart replies, scheduling, pricing. Include comparison table."
    },
    {
        "slug": "ai-meeting-assistants",
        "title": "AI Meeting Assistants: Otter vs Fireflies vs Granola — Never Take Notes Again",
        "category": "Tools",
        "categorySlug": "tools",
        "tags": ["AI meetings", "Otter AI", "Fireflies", "Granola", "meeting notes"],
        "topic": "Compare AI meeting assistants: Otter.ai, Fireflies.ai, Granola. Cover transcription accuracy, integrations, pricing, action items, real user experiences."
    },
    {
        "slug": "ai-data-analysis-tools",
        "title": "AI Data Analysis Tools: ChatGPT vs Julius vs Hex — Which Crunches Numbers Best?",
        "category": "Tools",
        "categorySlug": "tools",
        "tags": ["AI data analysis", "ChatGPT", "Julius AI", "Hex", "data science"],
        "topic": "Compare AI data analysis tools: ChatGPT Advanced Data Analysis, Julius, Hex. Cover capabilities, accuracy, visualization, pricing."
    },
    {
        "slug": "ai-customer-support-tools",
        "title": "AI Customer Support Tools: Intercom vs Zendesk AI vs Ada — The Bot Battle",
        "category": "Tools",
        "categorySlug": "tools",
        "tags": ["AI support", "Intercom", "Zendesk AI", "Ada", "customer service"],
        "topic": "Compare AI customer support tools: Intercom Fin, Zendesk AI, Ada. Cover resolution rates, setup complexity, pricing, integration capabilities."
    },
    {
        "slug": "ai-translation-tools",
        "title": "AI Translation Tools: DeepL vs Google Translate vs Claude — Who Wins the Language War?",
        "category": "Tools",
        "categorySlug": "tools",
        "tags": ["AI translation", "DeepL", "Google Translate", "Claude", "language tools"],
        "topic": "Compare AI translation tools: DeepL, Google Translate, Claude for translation. Cover accuracy across languages, document translation, API pricing, nuance handling."
    },

    # === NEWS (6) ===
    {
        "slug": "apple-intelligence-2026-update",
        "title": "Apple Intelligence 2026: What Actually Changed (And What's Still Missing)",
        "category": "News",
        "categorySlug": "news",
        "tags": ["Apple Intelligence", "iOS AI", "Siri AI", "Apple 2026", "on-device AI"],
        "topic": "Cover Apple Intelligence updates in 2026: Siri improvements, on-device AI capabilities, image generation, writing tools, what's improved vs still lacking. Be critical but fair."
    },
    {
        "slug": "openai-gpt5-rumors",
        "title": "GPT-5 Rumors: Everything We Know So Far (And Why It Matters)",
        "category": "News",
        "categorySlug": "news",
        "tags": ["GPT-5", "OpenAI", "AI models", "large language models", "AI news"],
        "topic": "Cover all known GPT-5 rumors, leaks, and confirmed info. Discuss expected capabilities, timeline, pricing speculation, and what it means for the AI ecosystem."
    },
    {
        "slug": "anthropic-claude-5-predictions",
        "title": "Claude 5 Predictions: What Anthropic Is Building Next Will Change Everything",
        "category": "News",
        "categorySlug": "news",
        "tags": ["Claude 5", "Anthropic", "AI safety", "AI predictions", "AI models"],
        "topic": "Cover predictions and known information about Claude 5 / next Anthropic model. Discuss Anthropic's safety approach, expected capabilities, competitive positioning."
    },
    {
        "slug": "ai-regulation-2026-global-overview",
        "title": "AI Regulation in 2026: The Global Crackdown Has Arrived",
        "category": "News",
        "categorySlug": "news",
        "tags": ["AI regulation", "EU AI Act", "AI policy", "AI governance", "tech regulation"],
        "topic": "Cover global AI regulation landscape in 2026: EU AI Act enforcement, US executive orders, China regulations, UK approach. What developers and businesses need to know."
    },
    {
        "slug": "ai-copyright-lawsuits-2026",
        "title": "AI Copyright Lawsuits: Where Things Stand in 2026 (It's a Mess)",
        "category": "News",
        "categorySlug": "news",
        "tags": ["AI copyright", "AI lawsuits", "fair use", "AI legal", "content creators"],
        "topic": "Cover the state of AI copyright lawsuits in 2026: major cases, rulings, implications for creators and AI companies. NYT vs OpenAI, Getty, music industry cases."
    },
    {
        "slug": "ai-chip-wars-nvidia-amd-intel",
        "title": "AI Chip Wars: NVIDIA vs AMD vs Intel vs Custom Silicon — Who's Actually Winning?",
        "category": "News",
        "categorySlug": "news",
        "tags": ["AI chips", "NVIDIA", "AMD", "Intel", "AI hardware"],
        "topic": "Cover the AI chip competition: NVIDIA dominance, AMD MI300X, Intel Gaudi, Google TPUs, custom silicon from Amazon/Microsoft. Market share, performance, pricing."
    },

    # === TUTORIALS (6) ===
    {
        "slug": "langchain-tutorial-beginners",
        "title": "LangChain Tutorial for Beginners: Build AI Agents That Actually Work",
        "category": "Tutorials",
        "categorySlug": "tutorials",
        "tags": ["LangChain", "AI agents", "Python tutorial", "LLM development", "AI programming"],
        "topic": "Step-by-step LangChain tutorial for beginners. Cover installation, chains, agents, tools, memory. Build a practical project. Include code examples."
    },
    {
        "slug": "ai-agents-tutorial-crew-ai",
        "title": "AI Agents Tutorial: Build Multi-Agent Systems with CrewAI That Do Real Work",
        "category": "Tutorials",
        "categorySlug": "tutorials",
        "tags": ["CrewAI", "AI agents", "multi-agent", "Python", "automation"],
        "topic": "Tutorial on building multi-agent systems with CrewAI. Cover agent roles, tasks, crews, tools. Build a practical multi-agent project step-by-step."
    },
    {
        "slug": "deploy-llm-on-aws",
        "title": "Deploy Your Own LLM on AWS: The Complete No-BS Guide",
        "category": "Tutorials",
        "categorySlug": "tutorials",
        "tags": ["LLM deployment", "AWS", "SageMaker", "cloud AI", "self-hosted AI"],
        "topic": "Complete guide to deploying an LLM on AWS. Cover SageMaker, EC2 options, cost optimization, model selection, scaling. Include practical commands and configs."
    },
    {
        "slug": "ai-automation-zapier-make",
        "title": "AI Automation with Zapier and Make: The No-Code Guide That Actually Works",
        "category": "Tutorials",
        "categorySlug": "tutorials",
        "tags": ["Zapier", "Make", "AI automation", "no-code", "workflow automation"],
        "topic": "Guide to building AI automations with Zapier and Make.com. Cover connecting AI APIs, building workflows, practical examples, pricing comparison."
    },
    {
        "slug": "vector-databases-explained",
        "title": "Vector Databases Explained: Pinecone vs Weaviate vs Chroma — Pick the Right One",
        "category": "Tutorials",
        "categorySlug": "tutorials",
        "tags": ["vector databases", "Pinecone", "Weaviate", "Chroma", "RAG"],
        "topic": "Explain vector databases and compare Pinecone, Weaviate, Chroma. Cover how embeddings work, use cases, performance, pricing, when to use each."
    },
    {
        "slug": "build-ai-content-pipeline",
        "title": "Build an AI Content Pipeline: Automate Blog Writing Without Losing Your Soul",
        "category": "Tutorials",
        "categorySlug": "tutorials",
        "tags": ["AI content", "content automation", "blog automation", "AI writing", "content pipeline"],
        "topic": "Tutorial on building an automated AI content pipeline. Cover research, outline generation, drafting, editing, publishing workflow. Tools and code examples."
    },

    # === MONEY (6) ===
    {
        "slug": "ai-affiliate-marketing-strategy",
        "title": "AI Affiliate Marketing: How Smart Marketers Are Automating Passive Income",
        "category": "Money",
        "categorySlug": "money",
        "tags": ["AI affiliate", "passive income", "affiliate marketing", "AI automation", "online income"],
        "topic": "Cover AI affiliate marketing strategies using verified case studies from third parties. Tools, automation workflows, realistic income expectations. Use documented case studies only."
    },
    {
        "slug": "ai-consulting-business",
        "title": "Start an AI Consulting Business: The Complete Playbook for 2026",
        "category": "Money",
        "categorySlug": "money",
        "tags": ["AI consulting", "AI business", "freelancing", "consulting", "AI career"],
        "topic": "Complete guide to starting an AI consulting business. Cover service offerings, pricing, finding clients, scaling. Use verified third-party case studies and market data."
    },
    {
        "slug": "ai-dropshipping-2026",
        "title": "AI Dropshipping in 2026: Does It Still Work? (The Honest Answer)",
        "category": "Money",
        "categorySlug": "money",
        "tags": ["AI dropshipping", "ecommerce", "AI business", "dropshipping 2026", "online store"],
        "topic": "Honest analysis of AI dropshipping in 2026. Cover what works, what doesn't, tools available, realistic expectations. Use third-party data and documented case studies only."
    },
    {
        "slug": "build-ai-agency-2026",
        "title": "Build an AI Agency in 2026: The Business Model That's Actually Working",
        "category": "Money",
        "categorySlug": "money",
        "tags": ["AI agency", "AI business", "consulting", "agency model", "AI services"],
        "topic": "Guide to building an AI agency in 2026. Cover service models, pricing, team structure, client acquisition, scaling. Use verified third-party examples and market data."
    },
    {
        "slug": "ai-newsletter-monetization",
        "title": "AI Newsletter Monetization: From Zero Subscribers to $10K/Month Revenue",
        "category": "Money",
        "categorySlug": "money",
        "tags": ["AI newsletter", "newsletter monetization", "email marketing", "AI income", "content business"],
        "topic": "Guide to monetizing an AI newsletter. Cover growth strategies, monetization models (ads, sponsorships, paid tiers), tools. Use verified third-party case studies like The Rundown AI, Ben's Bites."
    },
    {
        "slug": "create-ai-course-sell-online",
        "title": "Create an AI Course and Sell It Online: The Educator's Goldmine",
        "category": "Money",
        "categorySlug": "money",
        "tags": ["AI course", "online education", "course creation", "AI teaching", "passive income"],
        "topic": "Guide to creating and selling AI courses online. Cover platforms, pricing, content creation, marketing. Use verified third-party success stories and market data."
    },

    # === PEOPLE (6) ===
    {
        "slug": "demis-hassabis-deepmind-genius",
        "title": "Demis Hassabis: The DeepMind Genius Who Solved Protein Folding (And Isn't Done Yet)",
        "category": "People",
        "categorySlug": "people",
        "tags": ["Demis Hassabis", "DeepMind", "AlphaFold", "Google AI", "AI pioneers"],
        "topic": "Profile of Demis Hassabis: chess prodigy, game designer, neuroscientist, DeepMind founder. Cover AlphaFold breakthrough, Nobel Prize, Google DeepMind leadership, future vision."
    },
    {
        "slug": "elon-musk-xai-grok",
        "title": "Elon Musk and xAI: Why Grok Matters More Than You Think",
        "category": "People",
        "categorySlug": "people",
        "tags": ["Elon Musk", "xAI", "Grok", "AI competition", "tech billionaires"],
        "topic": "Profile of Elon Musk's AI ambitions through xAI and Grok. Cover the OpenAI split, xAI founding, Grok capabilities, Memphis supercomputer, competitive positioning."
    },
    {
        "slug": "mark-zuckerberg-meta-ai",
        "title": "Mark Zuckerberg's AI Pivot: Inside Meta's Open Source Gamble",
        "category": "People",
        "categorySlug": "people",
        "tags": ["Mark Zuckerberg", "Meta AI", "Llama", "open source AI", "tech leadership"],
        "topic": "Profile of Zuckerberg's AI strategy at Meta. Cover the pivot from metaverse, Llama open source strategy, Meta AI assistant, competitive positioning against OpenAI/Google."
    },
    {
        "slug": "fei-fei-li-world-labs",
        "title": "Fei-Fei Li: From ImageNet to World Labs — The Godmother of AI's Next Chapter",
        "category": "People",
        "categorySlug": "people",
        "tags": ["Fei-Fei Li", "World Labs", "ImageNet", "AI pioneers", "spatial intelligence"],
        "topic": "Profile of Fei-Fei Li: ImageNet creator, Stanford professor, World Labs founder. Cover her journey, contributions to computer vision, spatial intelligence vision, diversity advocacy."
    },
    {
        "slug": "ai-influencers-worth-following",
        "title": "AI Influencers Actually Worth Following in 2026 (No Hype Bros Allowed)",
        "category": "People",
        "categorySlug": "people",
        "tags": ["AI influencers", "AI Twitter", "AI YouTube", "AI community", "AI education"],
        "topic": "Curated list of AI influencers worth following in 2026. Cover researchers, builders, educators, commentators. Include their platforms, why they matter, what makes them credible."
    },
    {
        "slug": "andrej-karpathy-ai-education",
        "title": "Andrej Karpathy: The Man Making AI Education Actually Accessible",
        "category": "People",
        "categorySlug": "people",
        "tags": ["Andrej Karpathy", "AI education", "Tesla AI", "OpenAI", "AI YouTube"],
        "topic": "Profile of Andrej Karpathy: Stanford, OpenAI, Tesla Autopilot, AI educator. Cover his YouTube channel, Eureka Labs, teaching philosophy, impact on AI education."
    },
]

PROMPT_TEMPLATE = """You are a senior tech writer for EgoistAI, a bold, direct, slightly irreverent AI-focused tech blog. Write a complete article with the following specifications:

**Title:** {title}
**Topic:** {topic}
**Category:** {category}

**STRICT REQUIREMENTS:**
1. Word count: 1500-3000 words
2. Tone: Bold, direct, slightly irreverent. No corporate fluff. Talk to readers like smart adults.
3. AEO-optimized structure:
   - Use question-based H2 and H3 headings (e.g., "## What Makes X Different?" or "## Is X Worth the Price?")
   - Include at least one comparison table (markdown table format)
   - End with a ## Frequently Asked Questions section (4-6 Q&As)
4. Use real, verifiable information. Cite specific features, prices, and capabilities.
5. Include practical takeaways and actionable advice.
6. For any money/income topics: Use ONLY verified third-party case studies. NEVER use first-person income claims or "I made $X" framing.

**OUTPUT FORMAT:**
Start with YAML frontmatter, then the article in markdown. Use this EXACT frontmatter format:

---
title: "{title}"
excerpt: "{excerpt_instruction}"
category: "{category}"
categorySlug: "{categorySlug}"
image: "/images/{slug}.webp"
date: "2026-04-03"
readTime: "X min read"
author: "EgoistAI"
featured: false
tags: {tags}
sources:
  - name: "Source Name"
    url: "https://real-url"
  - name: "Another Source"
    url: "https://another-real-url"
---

For the excerpt, write a compelling 140-180 character hook that makes people want to click.
For readTime, estimate based on word count (avg 250 words/min).
For sources, include 3-5 REAL, verifiable source URLs relevant to the topic.

Write the complete article now. Do NOT include ```markdown or ``` code fences around the output."""

def main():
    total = len(ARTICLES)
    print(f"Generating {total} articles...")

    for i, article in enumerate(ARTICLES):
        slug = article["slug"]
        cat_slug = article["categorySlug"]
        out_dir = os.path.join(DRAFTS_DIR, cat_slug)
        out_path = os.path.join(out_dir, f"{slug}.md")

        if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
            print(f"[{i+1}/{total}] SKIP (exists): {slug}")
            continue

        print(f"[{i+1}/{total}] Generating: {slug} ({cat_slug})...")

        prompt = PROMPT_TEMPLATE.format(
            title=article["title"],
            topic=article["topic"],
            category=article["category"],
            categorySlug=cat_slug,
            slug=slug,
            tags=json.dumps(article["tags"]),
            excerpt_instruction="Write a compelling 140-180 char hook"
        )

        try:
            content = generate_article(prompt)
            # Strip any markdown code fences if present
            if content.startswith("```"):
                lines = content.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                content = "\n".join(lines)

            with open(out_path, "w") as f:
                f.write(content)

            word_count = len(content.split())
            print(f"  Done: {word_count} words -> {out_path}")
        except Exception as e:
            print(f"  ERROR: {e}")

        # Delay between API calls
        if i < total - 1:
            time.sleep(4)

    print("\nAll done!")

if __name__ == "__main__":
    main()
