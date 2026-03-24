---
title: "Prompt Engineering 101: Write Better Prompts, Get Better Results"
excerpt: "Stop getting mediocre AI output. This beginner-friendly guide teaches you the exact techniques to write prompts that get ChatGPT, Claude, and Midjourney to actually do what you want."
category: "Tutorials"
categorySlug: "tutorials"
image: "/images/prompt-engineering-101-write-better-prompts.webp"
date: "2026-03-24"
readTime: "12 min read"
author: "EgoistAI"
tags: ["ai", "prompt engineering", "chatgpt", "claude", "midjourney", "tutorial", "tips"]
featured: false
---

Here's the dirty secret of AI tools: the difference between garbage output and mind-blowing output is almost never the model. It's the prompt. Most people are using AI like they're texting a slightly dumb friend — vague, lazy, and then frustrated when the response is equally vague and lazy.

Prompt engineering sounds intimidating, but it's really just the art of communicating clearly with AI. If you can write a decent email to a coworker, you can write a great prompt. You just need to know the rules.

This guide will take you from "AI is overrated" to "how did I ever work without this" in about 12 minutes.

![Prompt engineering fundamentals](/images/prompt-engineering-fundamentals.webp)

## Why Your Prompts Suck (No Offense)

Let's start with a reality check. Here's how most people prompt AI:

**Bad prompt:** "Write me a blog post about marketing."

That's like walking into a restaurant and saying "give me food." You'll get something, but it probably won't be what you wanted. The AI has no idea about your audience, your tone, the length you want, the angle you're going for, or what makes your perspective unique.

**Better prompt:** "Write a 1,500-word blog post for small business owners about why email marketing still outperforms social media for ROI. Use a casual, slightly contrarian tone. Include 3-4 specific statistics. Structure it with an attention-grabbing intro, 4 main sections with H2 headings, and a practical call-to-action at the end."

See the difference? Same AI model, dramatically different output. The second prompt gives the AI everything it needs to produce something actually useful.

## The 5 Elements of a Perfect Prompt

Every great prompt contains some combination of these five elements. You don't always need all five, but the more you include, the better your results.

### 1. Role

Tell the AI who it should be. This sets the entire frame for the response.

**Without role:** "Explain quantum computing."
**With role:** "You are a physics professor known for making complex topics accessible to complete beginners. Explain quantum computing."

The role primes the AI to adopt a specific knowledge level, tone, and communication style. Some powerful roles to try:

- "You are a senior copywriter at a top ad agency"
- "You are a pediatrician explaining this to a concerned parent"
- "You are a financial advisor speaking to a first-time investor"
- "You are a stand-up comedian writing material about tech"

### 2. Context

Give the AI background information it needs. Don't assume it knows your situation.

**Without context:** "Help me write a cover letter."
**With context:** "I'm a marketing manager with 5 years of experience transitioning from B2C to B2B SaaS. I'm applying for a Head of Content role at a Series B startup. The job description emphasizes SEO strategy and team leadership. Help me write a cover letter."

The more relevant context you provide, the more tailored the output. You can include:

- Your target audience
- Your industry or niche
- Your experience level
- The specific situation or problem
- Previous attempts and why they didn't work

### 3. Task

Be specific about what you want. Vague tasks get vague results.

**Vague:** "Write something about our product launch."
**Specific:** "Write 5 different email subject lines for our product launch that create urgency without feeling spammy. Our product is a project management tool for remote teams. The launch is next Tuesday."

Break complex tasks into specific, actionable instructions. Instead of "write a marketing plan," try "create a 30-day social media content calendar with post topics, suggested platforms, and posting times."

### 4. Format

Tell the AI how to structure its response. This is the element most people forget.

Format instructions you can use:

- "Respond in bullet points"
- "Create a table comparing X, Y, and Z"
- "Write this as a numbered step-by-step guide"
- "Keep each paragraph under 3 sentences"
- "Use H2 and H3 headings"
- "Format as a pros/cons list"
- "Write exactly 280 characters (for a tweet)"
- "Respond in JSON format"

### 5. Constraints

Set boundaries. Tell the AI what NOT to do, and set quality bars.

Useful constraints:

- "Don't use jargon — write for a general audience"
- "Avoid cliches like 'game-changer' and 'leverage'"
- "Keep the total length under 500 words"
- "Don't start sentences with 'I'"
- "Include at least 3 specific examples"
- "Don't use bullet points"
- "Write at a 6th-grade reading level"

## Advanced Techniques That Actually Work

Once you've got the basics down, these techniques will level up your prompting game significantly.

### Chain of Thought Prompting

Instead of asking for a final answer directly, ask the AI to think through the problem step by step.

**Standard prompt:** "What's the best pricing strategy for our SaaS product?"

**Chain of thought prompt:** "I need to determine the best pricing strategy for our SaaS product. Think through this step by step:
1. First, analyze the common SaaS pricing models (freemium, tiered, usage-based, per-seat)
2. Consider the pros and cons of each for a product targeting small businesses
3. Look at how competitors in the project management space typically price
4. Recommend a strategy with specific reasoning for why it fits our situation"

This technique is especially powerful for complex analysis, math problems, strategic decisions, and debugging code.

### Few-Shot Prompting

Give the AI examples of what you want before asking it to generate new content. This is incredibly effective for maintaining a specific style or format.

**Prompt:** "I need you to write product descriptions in a specific style. Here are two examples:

Example 1: 'The Horizon Backpack isn't for weekend warriors. It's for the ones who treat Tuesday like summit day. 30L of organized chaos, waterproof because your ideas shouldn't be the only things that make a splash.'

Example 2: 'Meet the Drift Sunglasses. Born from the radical idea that protecting your eyes shouldn't make you look like a lab technician. Polarized lenses, titanium frames, zero pretension.'

Now write a product description in this same style for: a wireless charging pad made from recycled ocean plastic."

The AI will nail the tone, rhythm, and style because you've shown it exactly what you want instead of trying to describe it.

![Few-shot prompting example](/images/few-shot-prompting-example.webp)

### The Persona Stack

Combine multiple roles for nuanced output.

**Prompt:** "Analyze my business plan from three perspectives:
1. As a venture capitalist looking for reasons NOT to invest
2. As an excited co-founder who believes in the vision
3. As a pragmatic CFO focused on unit economics

After all three perspectives, synthesize the key insights into a balanced assessment."

This gives you a multi-dimensional analysis that's far more valuable than a single perspective.

### Iterative Refinement

Don't try to get perfection in one prompt. Use follow-up prompts to refine.

**Round 1:** "Write a landing page headline for our AI writing tool."
**Round 2:** "Those are good but too generic. Make them more specific to our audience: busy marketing managers at mid-size companies. More urgency, less corporate."
**Round 3:** "Option 3 is closest. Keep that structure but make it shorter — under 8 words — and add a power word."

Each round gets you closer to exactly what you need. The AI remembers the full conversation, so each refinement builds on the last.

### The Mega-Prompt

For complex projects, put everything into one detailed prompt rather than spreading it across multiple messages.

**Mega-prompt example for a blog post:**

"I need you to write a blog post with the following specifications:

**Topic:** Why startups should hire generalists over specialists in their first 10 hires

**Audience:** Startup founders and early-stage CEOs

**Tone:** Conversational, opinionated, slightly contrarian. Think Paul Graham's essays mixed with a group chat.

**Length:** 2,000-2,500 words

**Structure:**
- Hook opening (personal anecdote or surprising stat)
- The conventional wisdom (and why it's wrong)
- 4-5 arguments for generalists, each with a real-world example
- Acknowledge when specialists ARE the right call
- Practical advice for identifying great generalists
- Strong closing that reinforces the main thesis

**Constraints:**
- No corporate jargon
- No phrases like 'in today's fast-paced world' or 'at the end of the day'
- Every claim needs a specific example or data point
- Paragraphs max 4 sentences
- Include at least one counterintuitive insight

**SEO target keyword:** hiring generalists startups

**Examples of writing I like:** Paul Graham, Lenny Rachitsky, Packy McCormick"

That single prompt will generate a substantially better first draft than a dozen vague back-and-forth messages.

## Platform-Specific Tips

### ChatGPT Tips

- **Use Custom Instructions** to set persistent context (your writing style, your audience, your preferences). This saves you from repeating context in every conversation.
- **GPT-4o is better for creative tasks**, while the o-series reasoning models are better for analysis and coding.
- **Use the canvas feature** for long-form writing projects where you want to edit collaboratively.
- **Upload reference files** when you want the AI to match a specific style or work with existing content.

### Claude Tips

- **Claude excels with long context**. Don't be afraid to paste entire documents, style guides, or codebases. It handles massive context better than any other model.
- **Use Claude Projects** to maintain persistent knowledge across conversations. Upload your brand voice document, writing samples, and audience profiles once, and every conversation in that project will reference them.
- **Extended thinking mode** is incredible for complex analysis. Ask Claude to "think carefully" about your problem and it'll show its reasoning process.
- **Claude responds well to direct, honest communication.** Instead of elaborate prompt frameworks, just tell Claude exactly what you want in plain language.

### Midjourney Tips

Midjourney prompting is a different beast entirely. It's more about visual vocabulary than written instructions.

**Basic structure:** Subject + Style + Details + Parameters

**Example:** "A cozy bookshop interior at golden hour, warm lighting, film photography style, shallow depth of field, Kodak Portra 400 --ar 16:9 --v 7 --s 250"

Key Midjourney parameters:
- `--ar` — Aspect ratio (16:9, 1:1, 9:16, etc.)
- `--v` — Model version
- `--s` — Stylization (0-1000, higher = more artistic)
- `--c` — Chaos (0-100, higher = more varied results)
- `--no` — Negative prompting ("--no text, watermark, blurry")
- `--sref` — Style reference (link to an image to match its style)

**Pro tips for Midjourney:**
- Mention specific camera models, film stocks, or photography techniques for realistic images
- Reference specific artists or art movements for stylized images
- Use "editorial photography" or "product photography" for commercial-quality shots
- Keep prompts descriptive but not overly long — Midjourney often performs better with focused prompts

![Midjourney prompting example](/images/midjourney-prompting-tips.webp)

## Common Mistakes to Avoid

### Being too polite
You don't need "Please, if you wouldn't mind, could you perhaps..." Just state what you want. "Write a 500-word blog post about X" is perfectly fine. The AI doesn't have feelings to hurt.

### Not iterating
If the first output isn't right, don't start a new conversation. Tell the AI what to fix. "Make it shorter," "more casual tone," "add specific examples" — each refinement gets you closer.

### Copying prompts blindly from the internet
Those "100 best ChatGPT prompts" articles are mostly useless because they're generic. The best prompt is one tailored to YOUR specific situation, audience, and needs.

### Ignoring the system prompt / custom instructions
Every conversation starts with default behavior unless you change it. Set your custom instructions once and every conversation improves automatically.

### Asking for too many things at once
"Write a blog post AND create social media posts AND suggest an email campaign AND analyze my competitors" in one prompt will give you mediocre everything. Break it up.

### Not providing examples
Showing the AI what you want is almost always more effective than describing what you want. When in doubt, give examples.

## The Prompt Template Library

Here are ready-to-use templates for common tasks. Copy, customize, and use.

### Blog Post
"Write a [LENGTH]-word blog post about [TOPIC] for [AUDIENCE]. Tone: [CASUAL/PROFESSIONAL/ACADEMIC]. Include [NUMBER] specific examples. Structure: attention-grabbing intro, [NUMBER] main sections with H2 headings, practical conclusion. Target keyword: [KEYWORD]. Avoid: [LIST OF THINGS TO AVOID]."

### Email
"Write a [TYPE: cold outreach / follow-up / newsletter] email. Sender: [WHO YOU ARE]. Recipient: [WHO THEY ARE]. Goal: [WHAT YOU WANT THEM TO DO]. Tone: [TONE]. Length: [SHORT/MEDIUM]. Include a clear CTA. Subject line options: give me 5."

### Social Media
"Create [NUMBER] social media posts for [PLATFORM] about [TOPIC]. Audience: [WHO]. Goal: [ENGAGEMENT/TRAFFIC/AWARENESS]. Include relevant hashtags. Tone: [TONE]. Each post should be [LENGTH] and include a hook in the first line."

### Code
"Write [LANGUAGE] code that [WHAT IT DOES]. Requirements: [LIST]. Use [FRAMEWORK/LIBRARY] if applicable. Include error handling. Add comments explaining the logic. Follow [STANDARD] coding conventions."

### Analysis
"Analyze [TOPIC/DOCUMENT/DATA] from the perspective of [ROLE]. Consider: [FACTORS]. Provide: key findings, potential risks, recommended actions. Format as [FORMAT]. Be specific — no generic advice."

## The Bottom Line

Prompt engineering isn't magic. It's communication. The better you communicate what you want, the better the AI delivers. Every minute you spend crafting a good prompt saves you ten minutes of editing bad output.

Start with the five elements (Role, Context, Task, Format, Constraints), experiment with the advanced techniques, and iterate relentlessly. Within a week of conscious practice, you'll be getting output that makes your colleagues think you hired a professional.

The AI is only as good as your instructions. Make them count.

---

*Bookmark this guide and refer back to it as you practice. Prompt engineering is a skill — it improves with repetition.*
