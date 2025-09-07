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

public/    # frontend served by GitHub Pages
scripts/   # CI scripts for fetching and processing news
```

## GitHub Actions

The workflow in `.github/workflows/pipeline.yml` runs on a daily schedule. It
fetches current events, updates the vector store, performs deduplication, builds
the daily index, and commits the changes back to the repository.

## Development

The frontend is plain HTML/CSS/JS and can be previewed locally by serving the
`public/` directory with any static file server.

## OpenAI Setup

The automation requires access to OpenAI's **Deep Research** API and the
`text-embedding-3-small` model.  Locally, set the `OPENAI_API_KEY` environment
variable.  For GitHub Actions, create a repository secret named
`OPENAI_API_KEY`.  Ensure that your OpenAI account has browsing and Deep
Research enabled.
