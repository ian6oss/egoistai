import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { getCollection } from 'astro:content';

export async function GET(context: APIContext) {
  const articles = await getCollection('articles');
  const sortedArticles = articles.sort(
    (a, b) => new Date(b.data.date).getTime() - new Date(a.data.date).getTime()
  );

  return rss({
    title: 'EgoistAI — AI Tools, News & Insights',
    description: 'Curated AI tools, news, tutorials, and insights for builders, creators, and power users.',
    site: context.site!.toString(),
    items: sortedArticles.map(article => ({
      title: article.data.title,
      pubDate: new Date(article.data.date),
      description: article.data.excerpt,
      link: `/articles/${article.id}`,
      categories: [article.data.category],
    })),
    customData: `<language>en-us</language>`,
  });
}
