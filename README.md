# Static Site Generator

A static site generator built from scratch in Python. It converts Markdown content into a fully functional HTML website using a single HTML template, with support for inline formatting, images, links, code blocks, headings, lists, and blockquotes.

## How it works

1. **Cleans** the output directory (`docs/`)
2. **Copies** all static assets (CSS, images) from `static/` to `docs/`
3. **Recursively walks** the `content/` directory and converts every `.md` file into a corresponding `.html` file, preserving the directory structure
4. **Injects** the generated HTML and the page title into `template.html`

## Project structure

```
.
├── content/            # Markdown source files
│   ├── index.md
│   ├── contact/
│   └── blog/
│       ├── glorfindel/
│       ├── majesty/
│       └── tom/
├── static/             # Static assets copied as-is to docs/
│   ├── index.css
│   └── images/
├── src/                # Python source code
│   ├── main.py
│   ├── gencontent.py   # Page generation and recursive crawling
│   ├── markdown_blocks.py  # Block-level markdown parsing
│   ├── inline_markdown.py  # Inline markdown parsing (bold, italic, code…)
│   ├── extract_markdown.py # Regex extraction of images and links
│   ├── htmlnode.py     # Base HTML node class
│   ├── leafnode.py     # Leaf (no children) HTML node
│   ├── parentnode.py   # Parent (with children) HTML node
│   ├── textnode.py     # Intermediate text representation
│   └── copystatic.py   # Recursive static file copy
├── template.html       # HTML template with {{ Title }} and {{ Content }}
├── main.sh             # Build and serve locally
├── build.sh            # Build only (used for deployment)
└── test.sh             # Run the test suite
```

## Requirements

- Python 3.8+
- No external dependencies — standard library only

## Usage

### Run locally

Builds the site and starts a local server at [http://localhost:8888](http://localhost:8888):

```bash
./main.sh
```

### Build for GitHub Pages

Generates the site with the correct base path for GitHub Pages:

```bash
python3 src/main.py /static-site-generator
```

### Run tests

```bash
./test.sh
```

## Markdown support

| Feature | Syntax |
|---|---|
| Heading | `# H1` … `###### H6` |
| Bold | `**bold**` |
| Italic | `_italic_` |
| Inline code | `` `code` `` |
| Code block | ` ```…``` ` |
| Blockquote | `> quote` |
| Unordered list | `- item` |
| Ordered list | `1. item` |
| Link | `[text](url)` |
| Image | `![alt](url)` |

## Adding content

Create a new `.md` file anywhere inside `content/`. The directory structure is mirrored in the output:

```
content/blog/new-post/index.md  →  docs/blog/new-post/index.html
```

Every Markdown file must have a level-1 heading (`# Title`) — it is used as the HTML `<title>`.

## Template

`template.html` has two placeholders:

- `{{ Title }}` — replaced with the `# H1` heading of the page
- `{{ Content }}` — replaced with the full HTML body generated from Markdown

## Deployment

The site is deployed to GitHub Pages from the `docs/` directory on the `main` branch. After building, commit and push `docs/`:

```bash
python3 src/main.py /static-site-generator
git add docs
git commit -m "build"
git push
```

## License

[MIT](LICENSE)
