import React from 'react';
import ReactMarkdown, { Options } from 'react-markdown';
import DOMPurify from 'dompurify';

export interface SanitizedMarkdownProps extends Options {
  children: string;
  className?: string;
}

/**
 * SanitizedMarkdown Component
 * Hardened UI component applying DOMPurify to sanitize input text, stripping
 * XSS vectors, malicious HTML tags, and javascript: protocols before passing to ReactMarkdown.
 */
export const SanitizedMarkdown: React.FC<SanitizedMarkdownProps> = ({
  children,
  className,
  ...props
}) => {
  const rawContent = children || '';

  // Sanitize with DOMPurify against Reflected / Stored XSS vectors
  const cleanContent = DOMPurify.sanitize(rawContent, {
    USE_PROFILES: { html: true },
    ALLOWED_TAGS: [
      'p', 'b', 'i', 'em', 'strong', 'a', 'br', 'ul', 'ol', 'li',
      'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'code', 'pre', 'hr',
      'table', 'thead', 'tbody', 'tr', 'th', 'td', 'span', 'div', 'del'
    ],
    ALLOWED_ATTR: ['href', 'title', 'target', 'rel', 'class', 'className', 'align'],
    ALLOW_DATA_ATTR: false,
  });

  return (
    <div className={className}>
      <ReactMarkdown
        {...props}
        components={{
          a: ({ node, ...rest }) => (
            <a
              {...rest}
              target="_blank"
              rel="noopener noreferrer"
              className="text-teal-600 hover:text-teal-800 underline transition-colors"
            />
          ),
          ...props.components,
        }}
      >
        {cleanContent}
      </ReactMarkdown>
    </div>
  );
};

export default SanitizedMarkdown;
