# Writing

This repo is inspired by [goodresearch.dev](https://goodresearch.dev).

## Setup

Recreate the conda environment with:

```bash
conda env create -n cb --file environment.yml
```

## Build website

```bash
source build.sh
```

## Adding a new post

1. Create a new markdown file in `docs/` (e.g., `docs/my-new-post.md`)
2. Add it to `docs/_toc.yml` under the Posts section:

```yaml
- caption: Posts
  chapters:
    - file: zipf
    - file: my-new-post
```
