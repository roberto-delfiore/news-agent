# GitHub Actions Setup Guide

This guide explains how to set up the automated daily AI news generation workflow.

## Required GitHub Secrets

The workflow needs the following secrets to be configured in your GitHub repository:

### 1. SERPAPI_API_KEY
- **Purpose**: Used to fetch news articles and search for images
- **Get it from**: https://serpapi.com/
- **Required**: Yes

### 2. GOOGLE_API_KEY
- **Purpose**: Used for Google Gemini AI to generate news summaries
- **Get it from**: https://aistudio.google.com/app/apikey
- **Required**: Yes

### 3. LANGSMITH_API_KEY
- **Purpose**: Optional tracing and monitoring for AI calls
- **Get it from**: https://smith.langchain.com/
- **Required**: No (workflow will still work without it)

## How to Add Secrets to GitHub

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with the name and value from above
5. Click **Add secret**

## Enable GitHub Pages

To publish the generated news pages:

1. Go to your repository **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. Save the settings

Your news page will be available at:
`https://roberto-delfiore.github.io/news_agent/`

## Workflow Schedule

The workflow runs:
- **Automatically**: Daily at 6:00 AM UTC
- **Manually**: Click **Actions** → **Daily AI News Generator** → **Run workflow**

## What the Workflow Does

1. Checks out the repository
2. Sets up Python 3.12
3. Installs dependencies
4. Generates a new AI news page with 10 articles
5. Saves the page to `docs/index.html`
6. Creates an archived copy with timestamp
7. Commits and pushes changes
8. Deploys to GitHub Pages

## Customization

To change the topic or number of articles, edit `.github/workflows/daily-ai-news.yml`:

```yaml
python news_agent.py "your topic here" \
  --articles 15 \
  --output docs/index.html
```

To change the schedule, modify the cron expression:
```yaml
# Examples:
- cron: '0 6 * * *'   # Daily at 6 AM UTC
- cron: '0 */6 * * *' # Every 6 hours
- cron: '0 12 * * 1'  # Every Monday at noon UTC
```

## Testing

You can manually trigger the workflow to test it:
1. Go to **Actions** tab
2. Select **Daily AI News Generator**
3. Click **Run workflow**
4. Check the run logs for any errors
