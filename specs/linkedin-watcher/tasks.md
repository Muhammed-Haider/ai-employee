# Tasks: LinkedIn Watcher

- [ ] **Task 1: Authentication Script**
    - Create `uv_project/scripts/capture_linkedin_session.py` using Playwright.
    - Instructions: Open headed browser, wait for user login, save `linkedin_session.json` to project root.
    - Test: Run script, log in manually, verify JSON file creation.

- [ ] **Task 2: Watcher Skeleton & Config**
    - Create `uv_project/agent_skills/monitoring/linkedin_watcher.py`.
    - Implement `LinkedInWatcher` class structure with `__init__` loading the session.
    - Test: Verify class initializes and loads session successfully.

- [ ] **Task 3: Notification Scraping Logic**
    - Implement `check_notifications()` method.
    - Navigate to `/notifications`.
    - Parse top 5 notification items (text, link, sender).
    - Test: Print scraped notifications to console.

- [ ] **Task 4: DM Scraping Logic**
    - Implement `check_messages()` method.
    - Navigate to `/messaging`.
    - Detect unread badges or top 3 threads.
    - Test: Print unread message count/snippets.

- [ ] **Task 5: Vault Integration**
    - Implement `save_to_inbox(item)` method.
    - Format item as Markdown with YAML metadata.
    - Write to `AI_Employee_Vault/Inbox/LINKEDIN_{TYPE}_{ID}.md`.
    - Test: Verify file creation in Vault with correct content.

- [ ] **Task 6: Deduplication & Logging**
    - Implement local cache `linkedin_seen.json` to prevent duplicates.
    - Add `write_dashboard_entry` calls for success/failure.
    - Test: Run twice; second run should find 0 new items.

- [ ] **Task 7: Automation Wrapper**
    - Create `run_linkedin_watcher.ps1` (or `.bat`) for easy execution.
    - Test: Run script from CLI, verify full loop completion.
