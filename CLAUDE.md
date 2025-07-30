# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

**Setup and Dependencies:**
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Running the Application:**
```bash
# Run the main bot locally (requires .env file with GOOGLE_API_KEY and DISCORD_WEBHOOK_URL)
python main.py

# Run comprehensive system tests (recommended before deployment)
python test_system.py

# Test Discord integration (legacy)
python test_discord.py
```

**Environment Setup:**
- Create `.env` file with required secrets:
  - `GOOGLE_API_KEY`: Google Gemini API key
  - `DISCORD_WEBHOOK_URL`: Discord webhook URL for notifications
- Optional environment variables:
  - `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR) - default: INFO
  - `LOG_FILE`: Log file path - default: logs/fundbot.log

**Development and Testing:**
```bash
# Run system validation tests
python test_system.py

# Run with debug logging
LOG_LEVEL=DEBUG python main.py

# Run with custom log file
LOG_FILE=custom.log python main.py
```

## Architecture Overview

FundBot is a Python-based automated funding opportunity scraper and notification system with the following modular architecture:

**Core Flow (main.py):**
1. Initialize SQLite database for tracking processed URLs
2. Scrape funding portals using AI-powered content extraction
3. Classify opportunities for AI/data visualization company relevance
4. Filter out previously notified opportunities
5. Generate AI summaries for new relevant opportunities
6. Send notifications to Discord
7. Store processed URLs to prevent duplicates

**Agent Modules (agents/):**
- `scraper.py`: Web scraping using Gemini 2.0 Flash to extract funding opportunities from HTML
- `classifier.py`: AI classification to filter relevant opportunities for the company profile
- `summarizer.py`: AI-powered summarization of funding opportunities
- `notifier.py`: Discord webhook integration for notifications
- `database.py`: SQLite operations for URL deduplication

**Configuration:**
- `portales.json`: External configuration file containing portal names and URLs to scrape
- `fundbot.db`: SQLite database for tracking processed URLs (auto-created)

**AI Integration:**
- Uses Google Gemini 2.0 Flash via LangChain for all AI operations
- Three separate AI calls with retry logic: content extraction, classification, and summarization
- Temperature set to 0 for consistent results
- Exponential backoff retry mechanism for reliability

**Automation:**
- GitHub Actions workflow (`.github/workflows/daily_scraper.yml`) runs daily at 08:00 UTC
- Improved commit logic that checks for actual changes before committing
- Automatically commits updated database and data files back to repository
- Requires `GOOGLE_API_KEY` and `DISCORD_WEBHOOK_URL` secrets in GitHub

## Key Technical Details

**Enhanced Error Handling:**
- Comprehensive logging system with configurable levels
- Retry mechanisms with exponential backoff for HTTP requests and AI calls
- Robust database operations with connection pooling and transaction handling
- Graceful error recovery and detailed error reporting

**Dependencies:**
- `langchain` + `langchain-google-genai` for AI integration
- `beautifulsoup4` + `requests` for web scraping with retry logic
- `python-dotenv` for environment variable management
- Custom utilities for logging and retry mechanisms

**Data Flow with Validation:**
- Portals → Raw HTML → AI Extraction → AI Classification → Deduplication → AI Summary → Discord Notification
- Each step includes validation, error handling, and logging
- Database operations track titles, sources, and timestamps for better analytics
- Comprehensive metrics logging for monitoring and debugging

**Company Profile Focus:**
The AI classifier uses a detailed company profile for opportunities relevant to:
- Artificial Intelligence and Machine Learning
- Data visualization and dashboards
- Software development and technology
- Data analysis and Business Intelligence
- Technology consulting and digital innovation

**Monitoring and Debugging:**
- Structured logging with execution metrics
- Database statistics tracking
- Discord notification validation and rate limiting
- Comprehensive test suite (`test_system.py`) for validation