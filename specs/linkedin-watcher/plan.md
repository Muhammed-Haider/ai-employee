# Plan: LinkedIn Watcher

## 1. Architecture
- **Skill Module**: `uv_project/agent_skills/monitoring/linkedin_watcher.py`
- **Session Manager**: `uv_project/scripts/capture_linkedin_session.py`
- **State Storage**: `uv_project/linkedin_session.json`
- **Output**: `AI_Employee_Vault/Inbox/`

## 2. Technical Approach
- Use **Playwright** with the Chromium engine.
- Implement a `LinkedInWatcher` class that:
    1. Loads `storage_state`.
    2. Navigates to `/notifications` and `/messaging`.
    3. Scrapes unread message counts and notification text.
    4. Compares found items with a local `seen_ids.json` cache.
    5. Writes new items to the Vault.

## 3. Interfaces
- **Internal**: Uses `agent_skills.file_skills.write_md` and `write_vault.py`.
- **External**: LinkedIn Web Interface (via Playwright).

## 4. Key Decisions & ADRs
📋 Architectural decision detected: Use Playwright for LinkedIn scraping — Document reasoning and tradeoffs? Run `/sp.adr playwright-for-linkedin`

## 5. Non-Functional Requirements
- **Performance**: Polling cycle < 5 minutes.
- **Reliability**: Graceful handling of login expiration (log to Dashboard).
- **Security**: No credentials stored in code; strictly session-based.

## 6. Verification Strategy
- **Unit Tests**: Test Markdown generation and metadata formatting.
- **Integration Tests**: Verify file creation in `Inbox/` upon mock data match.
- **Manual Test**: Run `capture_linkedin_session.py` and verify successful page load.
