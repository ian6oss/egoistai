#!/usr/bin/env node

/**
 * generate-article.mjs
 *
 * Claude-powered article generation pipeline for EgoistAI.com.
 * Uses a parallel writer + reviewer approach:
 *   1. Writer (Claude Sonnet) generates the article
 *   2. Reviewer (Claude Sonnet) fact-checks and validates
 *   3. If review fails, uses reviewer's fixed version or regenerates
 *
 * Usage:
 *   node scripts/generate-article.mjs          # Generate 1 article (default)
 *   node scripts/generate-article.mjs 4        # Generate 4 articles
 *
 * Environment:
 *   ANTHROPIC_API_KEY - Required. Set in .env or environment.
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import Anthropic from '@anthropic-ai/sdk';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = join(__dirname, '..');
const ARTICLES_DIR = join(PROJECT_ROOT, 'src', 'content', 'articles');
const DRAFTS_DIR = join(PROJECT_ROOT, 'src', 'content', 'drafts');
const CALENDAR_PATH = join(__dirname, 'content-calendar.md');
const LOGS_DIR = join(PROJECT_ROOT, 'logs');
const PROMPTS_DIR = join(__dirname, 'prompts');

// -------------------------------------------------------------------
// Configuration
// -------------------------------------------------------------------
const DAILY_LIMIT = parseInt(process.argv[2] || '1', 10);
const MAX_RETRIES = 2;
const WRITER_MODEL = 'claude-sonnet-4-6';
const REVIEWER_MODEL = 'claude-sonnet-4-6';
const SAVE_TO_DRAFTS = true; // Save to drafts/ instead of articles/

// -------------------------------------------------------------------
// Load .env file (simple parser, no external dependency)
// -------------------------------------------------------------------
function loadEnv() {
  const envPath = join(PROJECT_ROOT, '.env');
  if (!existsSync(envPath)) return;
  const content = readFileSync(envPath, 'utf-8');
  for (const line of content.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eqIndex = trimmed.indexOf('=');
    if (eqIndex === -1) continue;
    const key = trimmed.slice(0, eqIndex).trim();
    const value = trimmed.slice(eqIndex + 1).trim();
    if (!process.env[key]) {
      process.env[key] = value;
    }
  }
}

// -------------------------------------------------------------------
// Category display name mapping
// -------------------------------------------------------------------
const CATEGORY_DISPLAY = {
  'tools': 'Tools',
  'news': 'News',
  'tutorials': 'Tutorials',
  'money': 'Money',
  'people': 'People',
};

// -------------------------------------------------------------------
// Calendar parsing
// -------------------------------------------------------------------
function parseCalendar() {
  const calendar = readFileSync(CALENDAR_PATH, 'utf-8');
  const lines = calendar.split('\n');
  const articles = [];
  let currentCategory = null;

  for (const line of lines) {
    if (line.startsWith('## Category 1:')) currentCategory = 'tools';
    else if (line.startsWith('## Category 2:')) currentCategory = 'news';
    else if (line.startsWith('## Category 3:')) currentCategory = 'tutorials';
    else if (line.startsWith('## Category 4:')) currentCategory = 'money';
    else if (line.startsWith('## Category 5:')) currentCategory = 'people';

    const match = line.match(/^\|\s*\d+\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*(P[123])\s*\|\s*(TODO|DONE)\s*\|/);
    if (match && currentCategory) {
      articles.push({
        slug: match[1].trim(),
        title: match[2].trim(),
        priority: match[3].trim(),
        status: match[4].trim(),
        category: currentCategory,
      });
    }
  }

  return articles;
}

function selectNextArticles(articles, limit) {
  const todos = articles.filter(a => {
    if (a.status !== 'TODO') return false;
    // Skip if file already exists in articles or drafts
    const articlePath = join(ARTICLES_DIR, `${a.slug}.md`);
    const draftPath = join(DRAFTS_DIR, a.category, `${a.slug}.md`);
    return !existsSync(articlePath) && !existsSync(draftPath);
  });

  const priorityOrder = { P1: 0, P2: 1, P3: 2 };
  todos.sort((a, b) => {
    const pDiff = priorityOrder[a.priority] - priorityOrder[b.priority];
    if (pDiff !== 0) return pDiff;
    return a.category.localeCompare(b.category);
  });

  return todos.slice(0, limit);
}

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function updateCalendarStatus(slug) {
  let calendar = readFileSync(CALENDAR_PATH, 'utf-8');
  const regex = new RegExp(`(\\|\\s*${escapeRegex(slug)}\\s*\\|[^|]*\\|[^|]*\\|)\\s*TODO\\s*\\|`, 'g');
  calendar = calendar.replace(regex, '$1 DONE |');
  calendar = updateSummaryCounts(calendar);
  writeFileSync(CALENDAR_PATH, calendar, 'utf-8');
}

function updateSummaryCounts(calendar) {
  const categoryNames = ['Tools', 'News', 'Tutorials', 'Money', 'People'];

  for (const name of categoryNames) {
    const sectionRegex = new RegExp(`## Category \\d+: ${escapeRegex(name)}[\\s\\S]*?(?=## Category|## Summary|$)`);
    const sectionMatch = calendar.match(sectionRegex);
    if (sectionMatch) {
      const doneCount = (sectionMatch[0].match(/\| DONE \|/g) || []).length;
      const totalMatch = sectionMatch[0].match(/^\|\s*\d+\s*\|/gm);
      const totalCount = totalMatch ? totalMatch.length : 0;
      const remaining = totalCount - doneCount;
      const p1Remaining = (sectionMatch[0].match(/\| P1 \| TODO \|/g) || []).length;

      const summaryRowRegex = new RegExp(
        `\\| ${escapeRegex(name)} \\|\\s*\\d+\\s*\\|\\s*\\d+\\s*\\|\\s*\\d+\\s*\\|\\s*\\d+\\s*\\|`
      );
      calendar = calendar.replace(
        summaryRowRegex,
        `| ${name} | ${totalCount} | ${doneCount} | ${remaining} | ${p1Remaining} |`
      );
    }
  }

  const allDone = (calendar.match(/\| DONE \|/g) || []).length;
  const allRows = calendar.match(/^\|\s*\d+\s*\|/gm);
  const totalAll = allRows ? allRows.length : 80;
  const remainingAll = totalAll - allDone;
  const p1RemainingAll = (calendar.match(/\| P1 \| TODO \|/g) || []).length;

  calendar = calendar.replace(
    /\| \*\*Total\*\* \|[^|]*\|[^|]*\|[^|]*\|[^|]*\|/,
    `| **Total** | **${totalAll}** | **${allDone}** | **${remainingAll}** | **${p1RemainingAll}** |`
  );

  return calendar;
}

// -------------------------------------------------------------------
// Claude article generation + review
// -------------------------------------------------------------------
function loadPromptTemplate(filename) {
  return readFileSync(join(PROMPTS_DIR, filename), 'utf-8');
}

function buildPrompt(article) {
  const today = new Date().toISOString().split('T')[0];
  const keyword = article.slug.replace(/-/g, ' ');
  const imagePath = `/images/${article.slug}.webp`;

  let userPrompt = loadPromptTemplate('article-user.txt');
  userPrompt = userPrompt.replace(/__SLUG__/g, article.slug);
  userPrompt = userPrompt.replace(/__TITLE__/g, article.title);
  userPrompt = userPrompt.replace(/__CATEGORY__/g, article.category);
  userPrompt = userPrompt.replace(/__CATEGORY_DISPLAY__/g, CATEGORY_DISPLAY[article.category] || article.category);
  userPrompt = userPrompt.replace(/__KEYWORD__/g, keyword);
  userPrompt = userPrompt.replace(/__DATE__/g, today);
  userPrompt = userPrompt.replace(/__IMAGE_PATH__/g, imagePath);

  return userPrompt;
}

async function writeArticle(client, article) {
  const systemPrompt = loadPromptTemplate('article-system.txt');
  const userPrompt = buildPrompt(article);

  const response = await client.messages.create({
    model: WRITER_MODEL,
    max_tokens: 8000,
    system: systemPrompt,
    messages: [
      { role: 'user', content: userPrompt },
    ],
  });

  let content = response.content[0].text;

  // Clean up: remove any code fence wrapping
  content = content.replace(/^```(?:markdown|md|yaml)?\n?/m, '');
  content = content.replace(/\n?```\s*$/m, '');
  content = content.trim();

  // Ensure it starts with ---
  if (!content.startsWith('---')) {
    const fmStart = content.indexOf('---');
    if (fmStart >= 0) {
      content = content.substring(fmStart);
    }
  }

  return content;
}

async function reviewArticle(client, content, article) {
  const reviewSystem = loadPromptTemplate('review-system.txt');
  const reviewPrompt = `Review this article for EgoistAI.com.

Article slug: ${article.slug}
Category: ${article.category}
Expected title: ${article.title}

---ARTICLE START---
${content}
---ARTICLE END---

Provide your review as a JSON object.`;

  const response = await client.messages.create({
    model: REVIEWER_MODEL,
    max_tokens: 10000,
    system: reviewSystem,
    messages: [
      { role: 'user', content: reviewPrompt },
    ],
  });

  let text = response.content[0].text;

  // Extract JSON from response (Claude might wrap it in markdown)
  const jsonMatch = text.match(/```(?:json)?\s*\n?([\s\S]*?)\n?```/);
  if (jsonMatch) {
    text = jsonMatch[1];
  }

  try {
    return JSON.parse(text);
  } catch {
    return { pass: true, score: 7, issues: [], suggestions: [], fixed_content: null };
  }
}

// -------------------------------------------------------------------
// Logging
// -------------------------------------------------------------------
function log(message) {
  const timestamp = new Date().toISOString();
  const logLine = `[${timestamp}] ${message}`;
  console.log(logLine);
  return logLine;
}

function ensureDir(dir) {
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
}

// -------------------------------------------------------------------
// Main
// -------------------------------------------------------------------
async function main() {
  loadEnv();

  const startTime = Date.now();
  const logLines = [];
  const addLog = (msg) => logLines.push(log(msg));

  addLog('=== EgoistAI Article Generator (Writer + Reviewer) ===');
  addLog(`Target: ${DAILY_LIMIT} article(s)`);
  addLog(`Writer model: ${WRITER_MODEL}`);
  addLog(`Reviewer model: ${REVIEWER_MODEL}`);
  addLog(`Output: ${SAVE_TO_DRAFTS ? 'drafts/' : 'articles/'}`);

  // Check API key
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    addLog('ERROR: ANTHROPIC_API_KEY not set.');
    addLog('  Create .env file with: ANTHROPIC_API_KEY=sk-ant-your-key');
    process.exit(1);
  }

  const client = new Anthropic({ apiKey });

  // Parse calendar and select articles
  const allArticles = parseCalendar();
  const selected = selectNextArticles(allArticles, DAILY_LIMIT);

  if (selected.length === 0) {
    addLog('All articles in content calendar are DONE or files already exist. Nothing to generate.');
    process.exit(0);
  }

  addLog(`Selected ${selected.length} articles to generate:`);
  selected.forEach((a, i) => addLog(`  ${i + 1}. [${a.priority}] ${a.slug} (${a.category})`));

  const results = { success: 0, failed: 0, skipped: 0 };

  for (const article of selected) {
    addLog(`\n--- Generating: ${article.slug} ---`);

    const outputDir = SAVE_TO_DRAFTS
      ? join(DRAFTS_DIR, article.category)
      : ARTICLES_DIR;
    const outputPath = join(outputDir, `${article.slug}.md`);

    if (existsSync(outputPath)) {
      addLog(`  SKIP: File already exists at ${outputPath}`);
      results.skipped++;
      continue;
    }

    ensureDir(outputDir);

    let success = false;

    for (let attempt = 1; attempt <= MAX_RETRIES + 1; attempt++) {
      try {
        // Step 1: Writer generates article
        addLog(`  [Writer] Attempt ${attempt}/${MAX_RETRIES + 1}: Generating with ${WRITER_MODEL}...`);
        let content = await writeArticle(client, article);

        // Basic validation
        if (!content.startsWith('---') || content.indexOf('---', 3) === -1) {
          addLog('  [Writer] FAILED: Missing or malformed frontmatter.');
          if (attempt <= MAX_RETRIES) continue;
          addLog('  FAILED: Max retries exceeded.');
          results.failed++;
          break;
        }

        // Word count
        const body = content.substring(content.indexOf('---', 3) + 3).trim();
        const wordCount = body.split(/\s+/).length;
        addLog(`  [Writer] Word count: ${wordCount}`);

        // Step 2: Reviewer checks the article
        addLog(`  [Reviewer] Reviewing article with ${REVIEWER_MODEL}...`);
        const review = await reviewArticle(client, content, article);

        addLog(`  [Reviewer] Score: ${review.score}/10 | Pass: ${review.pass}`);

        if (review.issues && review.issues.length > 0) {
          for (const issue of review.issues) {
            addLog(`  [Reviewer] ${issue.severity}: ${issue.description}`);
          }
        }

        if (review.suggestions && review.suggestions.length > 0) {
          review.suggestions.forEach(s => addLog(`  [Reviewer] Suggestion: ${s}`));
        }

        // If reviewer provided fixed content, use it
        if (!review.pass && review.fixed_content) {
          addLog(`  [Reviewer] Using reviewer's fixed version.`);
          content = review.fixed_content;

          // Clean up fixed content too
          content = content.replace(/^```(?:markdown|md|yaml)?\n?/m, '');
          content = content.replace(/\n?```\s*$/m, '');
          content = content.trim();
        } else if (!review.pass && !review.fixed_content) {
          // Review failed without fix — retry
          if (attempt <= MAX_RETRIES) {
            addLog(`  [Reviewer] No fix provided, retrying generation...`);
            continue;
          }
          addLog(`  FAILED: Review failed after max retries.`);
          results.failed++;
          break;
        }

        // Save article
        writeFileSync(outputPath, content, 'utf-8');
        addLog(`  SAVED: ${outputPath}`);

        // Update calendar
        updateCalendarStatus(article.slug);
        addLog(`  Calendar updated: ${article.slug} -> DONE`);

        results.success++;
        success = true;
        break;
      } catch (err) {
        addLog(`  ERROR: ${err.message}`);
        if (attempt <= MAX_RETRIES) {
          addLog(`  Retrying in 5 seconds...`);
          await new Promise(r => setTimeout(r, 5000));
        } else {
          addLog(`  FAILED: Max retries exceeded.`);
          results.failed++;
        }
      }
    }
  }

  // Summary
  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
  addLog('\n=== Generation Summary ===');
  addLog(`  Success: ${results.success}`);
  addLog(`  Failed: ${results.failed}`);
  addLog(`  Skipped: ${results.skipped}`);
  addLog(`  Time: ${elapsed}s`);

  // Save log
  ensureDir(LOGS_DIR);
  const logDate = new Date().toISOString().split('T')[0];
  const logTime = new Date().toISOString().split('T')[1].replace(/:/g, '').substring(0, 6);
  const logFile = join(LOGS_DIR, `generate-${logDate}-${logTime}.log`);
  writeFileSync(logFile, logLines.join('\n') + '\n', 'utf-8');
  console.log(`\nLog saved: ${logFile}`);

  // Exit with error if all failed
  if (results.failed > 0 && results.success === 0) {
    process.exit(1);
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
