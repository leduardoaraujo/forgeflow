# ForgeFlow Documentation

This directory contains the documentation for ForgeFlow.

## Building Documentation Locally

### Install MkDocs

```bash
pip install mkdocs-material mkdocs-autorefs
```

### Serve Documentation

```bash
cd docs
mkdocs serve
```

Then open http://127.0.0.1:8000 in your browser.

### Build Documentation

```bash
cd docs
mkdocs build
```

Static site will be generated in `site/` directory.

## Documentation Structure

```
docs/
├── index.md              # Homepage
├── guides/               # User guides
│   ├── getting-started.md
│   ├── core-concepts.md
│   ├── configuration.md
│   └── extending.md
├── examples/             # Examples and tutorials
│   └── index.md
├── api/                  # API reference
│   └── index.md
└── assets/               # Images, diagrams, etc.
```

## Contributing to Documentation

1. Edit Markdown files in `docs/`
2. Test locally with `mkdocs serve`
3. Submit a PR with your changes

See [CONTRIBUTING.md](../CONTRIBUTING.md) for more details.
