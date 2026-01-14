# Writing

This repo is inspired by [goodresearch.dev](https://goodresearch.dev).

## Setup

Recreate the conda environment with:

```bash
conda env create -n cb --file environment.yml
```

## Build website

```bash
conda activate cb && rm -rf docs/* && jupyter-book build source --path-output . && mv _build/html/* docs/ && rm -rf _build
```

This builds from `source/` and outputs HTML directly to `docs/` for GitHub Pages.

## Adding a new post

1. Create a new markdown file in `source/` (e.g., `source/my-new-post.md`)
2. Add it to `source/_toc.yml` under the Posts section:

```yaml
- caption: Posts
  chapters:
    - file: zipf
    - file: my-new-post
```
