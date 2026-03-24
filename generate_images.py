#!/usr/bin/env python3
"""Generate all article images using Google Gemini Flash Image API."""

import json
import base64
import time
import os
import sys
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO

API_KEY = Path(os.path.expanduser("~/.config/mogulfeed/.google-api-key")).read_text().strip()
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
OUTPUT_DIR = Path("/Users/ian/egoistai/public/images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STYLE = "modern tech editorial illustration, clean digital art, vibrant colors, sleek and professional, dark theme friendly, NO text NO letters NO words NO writing in the image"

# All images with descriptive prompts
IMAGES = {
    # Article hero images
    "10-ai-tools-replace-marketing-team.webp": "a futuristic AI robot managing multiple marketing screens and dashboards simultaneously, holographic displays showing social media analytics and content creation",
    "ai-marketing-tools-overview.webp": "an overhead view of a modern desk with floating holographic AI tool interfaces for marketing, copywriting, video editing, and design",
    "runway-video-generation.webp": "AI-powered video generation interface with a film reel transforming into digital particles, cinematic lighting",
    "copy-ai-sales-workflow.webp": "automated sales pipeline visualization with AI nodes connecting email, chat, and CRM systems, glowing data streams",
    "zapier-ai-marketing-automation.webp": "interconnected automation workflow with glowing nodes and pathways, representing AI-powered marketing automation",

    "7-free-ai-tools-you-should-be-using.webp": "seven glowing free tool icons floating in space, each representing a different AI capability like search, code, art, and writing",
    "free-ai-tools-overview.webp": "a treasure chest opening to reveal glowing AI tool icons, zero dollar signs floating around, vibrant neon colors",
    "hugging-face-spaces.webp": "a friendly robot face surrounded by open-source code and machine learning model cards floating in space",
    "suno-ai-music-generation.webp": "AI-generated music visualization with sound waves transforming into colorful musical notes and instruments",
    "ollama-local-ai-setup.webp": "a personal computer glowing with AI power, running a local language model, private and secure atmosphere",

    "ai-coming-for-these-jobs-creating-new-ones.webp": "a balanced scale with traditional job icons on one side and futuristic AI-enhanced job icons on the other, transformation theme",
    "ai-jobs-impact-landscape.webp": "a panoramic cityscape where half shows traditional offices and the other half shows futuristic AI-enhanced workplaces",
    "ai-jobs-at-risk.webp": "fading silhouettes of traditional workers being replaced by glowing AI automation processes, somber but hopeful mood",
    "new-ai-careers.webp": "emerging new career roles depicted as glowing avatars with AI tools, prompt engineers, AI trainers, and data curators",
    "ai-resistant-skills.webp": "a shield made of human creativity, empathy, and leadership icons protecting against a wave of automation",

    "ai-image-generator-war-midjourney-dalle-flux-imagen.webp": "four AI warriors representing different image generators facing off in an epic battle arena, each with unique visual style",
    "ai-image-generators-comparison.webp": "four floating screens each showing a different AI-generated art style, side by side comparison layout",
    "midjourney-sample-output.webp": "a stunning fantasy landscape with impossible architecture, showcasing peak AI image generation quality",
    "flux-image-sample.webp": "a hyperrealistic portrait with perfect lighting and detail, showcasing photorealistic AI image generation",
    "image-generator-test-results.webp": "a futuristic scorecard hologram comparing four AI systems with bar charts and radar charts floating in space",

    "build-complete-website-with-ai-30-minutes.webp": "a laptop screen showing a website being built in real-time by AI, code and design elements assembling themselves",
    "ai-website-building-tutorial.webp": "step by step floating panels showing website creation progress from blank screen to finished professional site",
    "v0-component-generation.webp": "UI components materializing from a glowing AI prompt input field, buttons and cards assembling themselves",
    "cursor-ai-editing.webp": "a code editor with AI suggestions highlighting and autocompleting code in real-time, purple and blue glow",
    "ai-built-portfolio-preview.webp": "a beautiful finished portfolio website displayed on multiple devices, phone tablet and laptop, modern design",

    "chatgpt-vs-claude-vs-gemini-ultimate-ai-showdown-2026.webp": "three AI titans represented as abstract digital entities facing each other in a triangular standoff, energy crackling between them",
    "chatgpt-vs-claude-vs-gemini-banner.webp": "three distinct AI brain visualizations side by side, one green, one orange, one blue, each with unique neural patterns",
    "ai-pricing-comparison-2026.webp": "floating price tags and subscription tiers for AI services displayed as a futuristic comparison hologram",
    "ai-reasoning-comparison.webp": "three AI systems solving the same complex puzzle simultaneously, each approaching it differently, split screen view",
    "ai-showdown-final-verdict.webp": "a podium with three positions showing abstract AI entities, trophy and medals, competition finale atmosphere",

    "claude-code-review.webp": "a glowing terminal interface with AI-powered code suggestions flowing across the screen, purple and green accent colors",

    "how-i-made-5000-per-month-using-ai.webp": "a person at a modern desk with AI tools generating income streams visualized as flowing golden data streams",
    "making-money-ai-tools.webp": "a dashboard showing multiple AI-powered revenue streams with growing charts and dollar amounts, optimistic vibe",
    "ai-freelance-writing-workflow.webp": "a writer's workspace with AI assistant helping create content, documents flowing from screen to clients",
    "ai-automation-consulting.webp": "a consultant presenting AI automation workflows to business clients, holographic process diagrams",
    "ai-side-hustle-timeline.webp": "a timeline visualization showing growth from zero to five thousand dollars over six months, milestone markers",

    "openai-raised-40-billion-what-it-means.webp": "a massive vault door opening to reveal forty billion dollars worth of AI computing infrastructure, epic scale",
    "openai-40b-funding.webp": "stacks of money transforming into GPU chips and data centers, representing massive AI investment",
    "openai-spending-breakdown.webp": "a pie chart made of futuristic holographic segments showing spending on compute, research, and operations",
    "ai-industry-impact.webp": "a ripple effect visualization showing how one company's funding impacts the entire AI ecosystem, concentric waves",

    "prompt-engineering-101-write-better-prompts.webp": "a craftsperson carefully sculpting a glowing prompt into a perfect AI instruction, workshop atmosphere",
    "prompt-engineering-fundamentals.webp": "building blocks of a perfect prompt stacking together, each block labeled with abstract icons for context and structure",
    "few-shot-prompting-example.webp": "a teacher showing examples to an AI student, three sample inputs leading to the perfect output pattern",
    "midjourney-prompting-tips.webp": "an artist's palette where each color represents a different prompting technique, creating a masterpiece",

    "sam-altman-most-dangerous-man-silicon-valley.webp": "a silhouette of a tech leader standing before a massive glowing AI neural network, casting a long shadow over Silicon Valley skyline",
    "sam-altman-portrait.webp": "an abstract portrait of a tech visionary composed of circuit board patterns and neural network nodes, dramatic lighting",
    "openai-headquarters.webp": "a futuristic tech company headquarters building at night, glowing with AI energy, sleek modern architecture",
    "openai-evolution-timeline.webp": "a timeline showing transformation from a small nonprofit lab to a massive tech corporation, growing scale",
    "sam-altman-conference.webp": "a tech leader on a grand stage addressing thousands, massive AI visualization projected behind them",
}

def generate_image(filename, prompt):
    """Generate a single image using Gemini Flash Image API."""
    filepath = OUTPUT_DIR / filename
    if filepath.exists():
        print(f"  SKIP (exists): {filename}")
        return True

    full_prompt = f"Generate this image: {prompt}, {STYLE}"
    payload = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}
    }

    try:
        resp = requests.post(ENDPOINT, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        # Find inlineData in response
        for candidate in data.get("candidates", []):
            for part in candidate.get("content", {}).get("parts", []):
                if "inlineData" in part:
                    img_data = base64.b64decode(part["inlineData"]["data"])
                    img = Image.open(BytesIO(img_data))

                    # Resize if wider than 1200px
                    if img.width > 1200:
                        ratio = 1200 / img.width
                        new_height = int(img.height * ratio)
                        img = img.resize((1200, new_height), Image.LANCZOS)

                    # Convert to RGB if needed (for WebP)
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')

                    img.save(filepath, 'WEBP', quality=80)
                    print(f"  OK: {filename} ({img.width}x{img.height})")
                    return True

        print(f"  FAIL (no image in response): {filename}")
        return False

    except Exception as e:
        print(f"  FAIL ({e}): {filename}")
        return False


def main():
    total = len(IMAGES)
    success = 0
    failed = []

    print(f"Generating {total} images...\n")

    for i, (filename, prompt) in enumerate(IMAGES.items(), 1):
        print(f"[{i}/{total}] {filename}")
        if generate_image(filename, prompt):
            success += 1
        else:
            failed.append(filename)

        if i < total:
            time.sleep(2)

    print(f"\nDone: {success}/{total} succeeded")
    if failed:
        print(f"Failed: {', '.join(failed)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
