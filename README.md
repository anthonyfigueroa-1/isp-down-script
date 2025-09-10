# ISP-Down Script Project Summary

## Project Purpose

The project monitors ISP outages and automates the Freshservice
ticketing workflow and Microsoft Teams Auto Attendant greetings. It
continuously: 1. Detects network alerts from Freshservice. 2. Matches
them to known sites, departments, and service components. 3. Updates
Freshservice tickets and the company status page. 4. Adjusts Microsoft
Teams out-of-office (OOO) greetings to inform callers about outages.

## High-Level Workflow

1.  Fetch Freshservice tickets (`tickets.py`).
2.  Filter and deduplicate tickets (`filter_ticket.py`;
    `used_tickets.py`; `closed_tickets.py`).
3.  Identify affected site and department using regex (`re.py`) and
    fuzzy matching with PolyFuzz (`fuzzy.py`, `resub.py`, and department
    cache in `departments.py`).
4.  Update ticket fields and Freshservice Status Page (`set_fields.py`,
    `status_page.py`).
5.  Write logs and persist open/closed ticket state (`logger.py`,
    `open_tickets.py`).
6.  Generate an OOO greeting summarizing active outages
    (`ooo_script.py`) and write it to a file (`greeting.py`).
7.  Update Microsoft Teams mailbox settings via Graph API if the
    greeting changed (`ms_mail_token.py`).
8.  Run continuously in a loop, sleeping for 30 seconds between cycles
    (`main.py`).

## Key Modules and Functions

### Ticket Handling

-   `get_tickets()` & `put_ticket_updates()`: Interact with
    Freshservice's API to read/update tickets.
-   `check_down_tickets()`: Confirms ticket statuses (open vs closed)
    and updates internal lists.
-   `post_ticket_note()` / `post_private_note()`: Posts solution links
    or custom notes to tickets.
-   `set_fixed()` / `set_priority()` / `set_department()`: Classifies
    tickets (priority 2--4, department ID, network tags).

### Filtering and State Management

-   `filter_ticket()`: Excludes already closed or processed tickets.
-   `used_tickets.py`, `closed_tickets.py`, `open_tickets.py`: Persist
    IDs of tickets in `/req-files/` to avoid reprocessing.
-   `group_filtered()`: Groups filtered tickets for bulk operations.

### Fuzzy Matching

-   Uses PolyFuzz TF-IDF to:
    -   Match site names to service components (`match_componenets`).
    -   Match site names to departments (`match_department`).
    -   Match sites to urgency keywords to set priority (`priority`).
-   `normalize()` maps abbreviations like `ns → northstar` for
    consistent matching.

### Status Page Integration

-   `get_service_components()`: Retrieves service components for mapping
    outages.
-   `post_to_status_page()`: Posts incidents with timestamps and
    component IDs.

### Microsoft Teams OOO Handling

-   `ooo_script()`: Builds phrases like "We are aware that Beaver Creek
    is down..." based on filtered tickets.
-   `write_greeting_to_file()`: Writes new messages only when changes
    occur.
-   `get_bearer_token()` & `patch_ooo()`: Authenticates with Azure AD
    (using MSAL and client credentials) and patches the greeting via
    Microsoft Graph API.

## PowerShell Component

-   `okay.ps1`: Runs in its own container to apply Teams greeting
    updates when the Python script writes to `greeting.txt`. It handles
    certificate-based auth and periodically retries if updates fail.

## Dockerized Deployment

-   `docker-compose.yml`:
    -   `isp-down`: Python 3.12 slim container built from `dockerfile`.
    -   `pwsh`: PowerShell container for Teams greeting updates.
    -   Volumes mount request files (`/req-files`), messages
        (`/message`), and priorities.
    -   Both services restart automatically.
-   `dockerfile`: Installs requirements (`requirement.txt`) and
    registers the entry point `isp-down = root.main:main`.

## Persistent Storage & Config

-   Uses local text and JSON files for:
    -   `used_tickets.txt`, `closed_tickets.txt`, `open_tickets.json`
        for state.
    -   `departments.json` as a cached department list.
    -   `urgent.txt` (volume-mounted) for priority keywords.
-   Relies on environment variables (`ANDREW_API`, `ANTHONY_API`,
    `MAIL_CLIENT`, etc.) for API keys and secrets.

## Overall Flow

1.  Monitor Freshservice for "ISP Down" alerts.
2.  Filter duplicates and closed tickets.
3.  Fuzzy-match sites → departments & components.
4.  Update Freshservice ticket fields, status page, and logs.
5.  Persist ticket state across runs.
6.  Update Teams OOO greeting automatically when outages change.
7.  Repeat indefinitely in a containerized environment.

