import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const articles = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/articles' }),
  schema: z.object({
    title: z.string(),
    excerpt: z.string(),
    category: z.string(),
    categorySlug: z.enum(['tools', 'news', 'tutorials', 'money', 'people']),
    image: z.string(),
    date: z.string(),
    readTime: z.string(),
    author: z.string().optional(),
    sources: z.array(z.object({
      name: z.string(),
      url: z.string(),
    })).optional(),
    featured: z.boolean().default(false),
    tags: z.array(z.string()).optional(),
  }),
});

export const collections = { articles };
