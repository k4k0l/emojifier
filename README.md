# AI-Powered News Portal

This repository hosts a static news portal generated entirely through automation.
It uses GitHub Pages for hosting and OpenAI APIs to fetch and process daily news
summaries.  GitHub Actions run scheduled scripts that gather headlines, store
them as JSON, de-duplicate related items, and build a daily index used by the
frontend.

## Repository Structure

```
news/      # individual news items in JSON

daily/     # daily index files

src/       # Astro source files
public/    # static assets copied by Astro
scripts/   # CI scripts for fetching and processing news
```

## GitHub Actions

The workflow in `.github/workflows/pipeline.yml` runs on a daily schedule. It
fetches current events, updates the vector store, performs deduplication, builds
the daily index, and commits the changes back to the repository.

## Development

The frontend uses the [Astro](https://astro.build) framework. Build the static
site with:

```
npm ci
npm run build
```

The generated files are written to the `dist/` directory and can be served
locally with any static file server.

## OpenAI Setup

The automation requires access to OpenAI's **Deep Research** API and the
`text-embedding-3-small` model.  Locally, set the `OPENAI_API_KEY` environment
variable.  For GitHub Actions, create a repository secret named
`OPENAI_API_KEY`.  Ensure that your OpenAI account has browsing and Deep
Research enabled.

## Testing

Tests attempt a minimal OpenAI API call when `OPENAI_API_KEY` is present:

```
pytest
```

If the environment variable is not set the tests are skipped.
