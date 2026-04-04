import { visit } from 'unist-util-visit';

/**
 * Rehype plugin to add lazy loading, decoding, and sizing hints to all
 * images rendered from markdown/MDX content.
 *
 * - Adds loading="lazy" and decoding="async" to every <img>.
 * - Sets width/height when not already present (defaults to 800x450,
 *   a 16:9 ratio that avoids CLS while CSS handles actual sizing).
 */
export default function rehypeLazyImages() {
  return (tree) => {
    visit(tree, 'element', (node) => {
      if (node.tagName !== 'img') return;

      const props = node.properties || {};

      // Always add lazy loading and async decoding
      if (!props.loading) {
        props.loading = 'lazy';
      }
      if (!props.decoding) {
        props.decoding = 'async';
      }

      // Add default dimensions to prevent CLS if not already set
      if (!props.width) {
        props.width = 800;
      }
      if (!props.height) {
        props.height = 450;
      }

      node.properties = props;
    });
  };
}
