# Spec: LinkedIn Watcher

## 1. Purpose
Automate the monitoring of LinkedIn for new connection requests, direct messages (DMs), and mentions to ensure timely business engagement and lead generation.

## 2. Scope
- **In-Scope**:
    - Polling LinkedIn for notifications and DMs.
    - Categorizing activity (DM, Mention, Request).
    - Generating standardized Markdown files in `AI_Employee_Vault/Inbox/`.
    - Logging activity to `Dashboard.md`.
- **Out-of-Scope**:
    - Automated replies or outbound messaging.
    - Commenting on posts.
    - Profile optimization.

## 3. Inputs & Dependencies
- **Authentication**: Requires a valid `linkedin_session.json` (similar to `x_session.json`).
- **Dependencies**: 
    - `playwright` for browser-based scraping.
    - `AI_Employee_Vault` structure.
    - `ccr` (or current "Brain" implementation) for categorization.

## 4. Process Flow
1. **Trigger**: Scheduled script (every 30 mins).
2. **Auth**: Load storage state from `linkedin_session.json`.
3. **Scrape**: 
    - Navigate to Notifications and Messaging pages.
    - Extract text and metadata for new items.
4. **Format**: Create `LINKEDIN_YYYYMMDD_ID.md` in `Inbox/`.
5. **Log**: Update `Dashboard.md` with a summary of found items.

## 5. Acceptance Criteria
- [ ] Successfully navigates LinkedIn without being blocked.
- [ ] Detects unread messages and new connection requests.
- [ ] Creates unique files for each new interaction to prevent duplicates.
- [ ] Metadata in Markdown files includes `type: linkedin_activity` and `status: new`.
- [ ] Failures (e.g., session expired) are logged clearly to `Dashboard.md`.

## 6. Constraints
- **Stealth**: Must use human-like delays and headless=False (or specific user-agents) to avoid detection.
- **Frequency**: No more than 2-3 polls per hour.
