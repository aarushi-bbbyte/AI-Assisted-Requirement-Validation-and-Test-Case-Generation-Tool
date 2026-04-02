# ai_generator.py
# Smart rule-based NLP engine that generates deeply requirement-aware test cases.
# No external ML models — pure Python NLP using regex + linguistic patterns.

import re
from requirement import Requirement

# ══════════════════════════════════════════════════════════════════════════════
# NLP helpers
# ══════════════════════════════════════════════════════════════════════════════

# --- Actor extraction --------------------------------------------------------
ACTOR_PATTERNS = [
    r"\b(registered user|unregistered user|guest user|admin(?:istrator)?|"
    r"super[\s-]?admin|manager|operator|customer|client|member|employee|"
    r"student|teacher|owner|the system|the application|the app|the server|"
    r"the database|the api|the module)\b",
    r"\b(user|system|application|app|admin)\b",
]

# --- Action verb extraction --------------------------------------------------
ACTION_PATTERNS = [
    r"\b(?:must|shall|should|will|can|may)\s+([\w\s]+?)(?:\s+(?:the|a|an|in|to|from|with|via|by|through|when|if|after|before|within|using|at)\b|[,;.]|$)",
]

# --- Object extraction -------------------------------------------------------
OBJECT_PATTERNS = [
    r"\b(password|username|email|file|document|report|data|record|form|"
    r"account|profile|message|notification|request|response|token|session|"
    r"link|url|image|video|upload|download|page|dashboard|log|audit|"
    r"payment|invoice|order|product|item|cart|list|entry|field|input|"
    r"output|result|setting|configuration|preference|role|permission)\b",
]

# --- Numeric / boundary extraction ------------------------------------------
NUMERIC_RE = re.compile(
    r"(?P<qualifier>within|at least|at most|more than|less than|greater than|"
    r"fewer than|up to|minimum|maximum|exactly|no more than|no less than|"
    r"equal to|between \d+ and)?\s*(?P<value>[\d,]+(?:\.\d+)?)\s*"
    r"(?P<unit>second|minute|hour|day|week|month|year|ms|millisecond|"
    r"kb|mb|gb|tb|character|char|item|record|attempt|click|step|"
    r"user|request|retry|retry attempt|percent|%|dollar|\$)s?\b",
    re.IGNORECASE,
)

# --- Condition clause extraction ---------------------------------------------
CONDITION_RE = re.compile(
    r"\b(?P<trigger>if|when|whenever|unless|until|after|before|"
    r"provided that|assuming|in case)\b\s+(?P<clause>[^,;.]+)",
    re.IGNORECASE,
)

# --- Format / type mentions --------------------------------------------------
FORMAT_RE = re.compile(
    r"\b(pdf|docx|csv|xlsx|xml|json|png|jpg|jpeg|gif|mp4|mp3|zip|"
    r"html|txt|email address|phone number|date|url|http|https|"
    r"integer|string|boolean|alphanumeric|numeric)\b",
    re.IGNORECASE,
)

# --- Security / auth keywords ------------------------------------------------
AUTH_RE = re.compile(
    r"\b(login|log in|log out|logout|authenticate|authoris|authoriz|"
    r"permission|role|access|password|credential|token|session|"
    r"otp|2fa|two.factor|single sign|sso|captcha)\b",
    re.IGNORECASE,
)

# --- UI interaction keywords -------------------------------------------------
UI_RE = re.compile(
    r"\b(button|form|field|input|dropdown|select|checkbox|radio|modal|"
    r"popup|page|screen|view|dashboard|tab|menu|link|icon|label|"
    r"notification|alert|message|toast|banner)\b",
    re.IGNORECASE,
)

# --- File upload keywords ----------------------------------------------------
UPLOAD_RE = re.compile(r"\b(upload|attach|import|submit file|send file)\b", re.IGNORECASE)

# --- Email keywords ----------------------------------------------------------
EMAIL_RE = re.compile(r"\b(email|e-mail|mail|smtp|inbox|send.*mail)\b", re.IGNORECASE)

# --- Report / export keywords ------------------------------------------------
REPORT_RE = re.compile(r"\b(report|export|download|generate|print|extract)\b", re.IGNORECASE)

# --- Search keywords ---------------------------------------------------------
SEARCH_RE = re.compile(r"\b(search|filter|query|find|look up|lookup|sort)\b", re.IGNORECASE)

# --- Delete / remove keywords ------------------------------------------------
DELETE_RE = re.compile(r"\b(delete|remove|deactivate|disable|archive|purge)\b", re.IGNORECASE)

# --- Concurrent / load keywords ----------------------------------------------
CONCURRENCY_RE = re.compile(
    r"\b(concurrent|simultaneous|parallel|multiple users|load|stress|"
    r"scalab|throughput|performance)\b",
    re.IGNORECASE,
)


# ══════════════════════════════════════════════════════════════════════════════
# Main Generator
# ══════════════════════════════════════════════════════════════════════════════

class AITestCaseGenerator:
    """
    Generates deeply requirement-aware positive and negative test cases
    using smart rule-based NLP.  No external models required.
    """

    def __init__(self):
        self._req   = None
        self._text  = ""
        self._lower = ""

        # Extracted entities
        self._actors     = []
        self._action     = ""
        self._objects    = []
        self._numerics   = []   # list of dicts: {qualifier, value, unit, raw}
        self._conditions = []   # list of dicts: {trigger, clause}
        self._formats    = []

        # Feature flags
        self._has_auth        = False
        self._has_ui          = False
        self._has_upload      = False
        self._has_email       = False
        self._has_report      = False
        self._has_search      = False
        self._has_delete      = False
        self._has_concurrency = False

    # ── Public ────────────────────────────────────────────────────────────────

    def generateTestCases(self, requirement: Requirement) -> list:
        self._req   = requirement
        self._text  = requirement.description
        self._lower = requirement.description.lower()

        self.parseRequirement()

        test_cases = []
        test_cases.extend(self.generatePositiveTests())
        test_cases.extend(self.generateNegativeTests())

        for idx, tc in enumerate(test_cases, start=1):
            tc["id"] = "TC-" + str(idx).zfill(3)

        return test_cases

    # ── Pipeline ──────────────────────────────────────────────────────────────

    def parseRequirement(self):
        """Extract all NLP entities and feature flags from the requirement."""
        self._actors     = self._extract_actors()
        self._objects    = self._extract_objects()
        self._numerics   = self._extract_numerics()
        self._conditions = self.extractConditions()
        self._formats    = FORMAT_RE.findall(self._lower)
        self._action     = self._extract_action()

        self._has_auth        = bool(AUTH_RE.search(self._lower))
        self._has_ui          = bool(UI_RE.search(self._lower))
        self._has_upload      = bool(UPLOAD_RE.search(self._lower))
        self._has_email       = bool(EMAIL_RE.search(self._lower))
        self._has_report      = bool(REPORT_RE.search(self._lower))
        self._has_search      = bool(SEARCH_RE.search(self._lower))
        self._has_delete      = bool(DELETE_RE.search(self._lower))
        self._has_concurrency = bool(CONCURRENCY_RE.search(self._lower))

    def _extract_actors(self) -> list:
        found = []
        for pattern in ACTOR_PATTERNS:
            matches = re.findall(pattern, self._lower)
            found.extend(matches)
        return list(dict.fromkeys(found))   # preserve order, deduplicate

    def _extract_objects(self) -> list:
        found = re.findall(OBJECT_PATTERNS[0], self._lower)
        return list(dict.fromkeys(found))

    def _extract_numerics(self) -> list:
        results = []
        for m in NUMERIC_RE.finditer(self._lower):
            results.append({
                "qualifier": (m.group("qualifier") or "").strip(),
                "value":     m.group("value"),
                "unit":      m.group("unit"),
                "raw":       m.group(0).strip(),
            })
        return results

    def extractConditions(self) -> list:
        results = []
        for m in CONDITION_RE.finditer(self._text):
            results.append({
                "trigger": m.group("trigger"),
                "clause":  m.group("clause").strip().rstrip(".,;"),
            })
        return results

    def _extract_action(self) -> str:
        for pattern in ACTION_PATTERNS:
            m = re.search(pattern, self._lower)
            if m:
                return m.group(1).strip()
        return "perform the described action"

    # ── Positive tests ────────────────────────────────────────────────────────

    def generatePositiveTests(self) -> list:
        cases = []
        req   = self._text
        actor = self._actors[0] if self._actors else "the user"
        obj   = self._objects[0] if self._objects else "the target resource"

        # ── P1: Base happy path (always generated) ────────────────────────────
        cases.append({
            "type":            "Positive",
            "description":     "Verify the core happy-path behaviour of the requirement",
            "preconditions":   "System is running. " + actor.capitalize() + " is logged in (if applicable).",
            "steps":           ("1. Set up valid environment and test data.\n"
                                "2. As " + actor + ", provide all required valid inputs.\n"
                                "3. Execute: " + self._action + ".\n"
                                "4. Observe the system response."),
            "expected_result": "The system performs the action as described. "
                               "No errors occur. The outcome matches the requirement.",
            "priority":        "High",
        })

        # ── P2: Each numeric boundary — valid side ────────────────────────────
        for num in self._numerics:
            q   = num["qualifier"] or "exactly"
            val = num["value"]
            unit= num["unit"]
            cases.append({
                "type":            "Positive",
                "description":     "Verify system accepts a value that satisfies the boundary: " + num["raw"],
                "preconditions":   "Valid environment. " + actor.capitalize() + " is ready to perform the action.",
                "steps":           ("1. Prepare input that is " + q + " " + val + " " + unit + ".\n"
                                    "2. Execute the action as " + actor + ".\n"
                                    "3. Observe result."),
                "expected_result": "System accepts the value (" + num["raw"] + ") and completes the action successfully.",
                "priority":        "High",
            })

        # ── P3: Each conditional clause ───────────────────────────────────────
        for cond in self._conditions:
            cases.append({
                "type":            "Positive",
                "description":     "Verify correct behaviour when condition is met: '" + cond["trigger"] + " " + cond["clause"] + "'",
                "preconditions":   "Condition '" + cond["clause"] + "' is satisfied.",
                "steps":           ("1. Ensure the condition '" + cond["clause"] + "' is true.\n"
                                    "2. As " + actor + ", trigger the functionality.\n"
                                    "3. Observe the outcome."),
                "expected_result": "System responds correctly when the condition '" + cond["clause"] + "' is fulfilled.",
                "priority":        "High",
            })

        # ── P4: Format / file type (if specified) ─────────────────────────────
        if self._formats:
            fmt_list = ", ".join(self._formats[:3])
            cases.append({
                "type":            "Positive",
                "description":     "Verify system correctly handles supported format(s): " + fmt_list,
                "preconditions":   "A valid " + fmt_list + " resource is available.",
                "steps":           ("1. Prepare a valid " + fmt_list + " input or file.\n"
                                    "2. As " + actor + ", submit or select it.\n"
                                    "3. Complete the action and observe the result."),
                "expected_result": "System processes the " + fmt_list + " successfully without errors.",
                "priority":        "Medium",
            })

        # ── P5: Auth / login positive ─────────────────────────────────────────
        if self._has_auth:
            cases.append({
                "type":            "Positive",
                "description":     "Verify successful authentication with valid credentials",
                "preconditions":   "A valid account exists in the system.",
                "steps":           ("1. Navigate to the login/auth screen.\n"
                                    "2. Enter correct, valid credentials.\n"
                                    "3. Submit and observe result."),
                "expected_result": "System grants access. User session is created. User is redirected appropriately.",
                "priority":        "High",
            })

        # ── P6: Upload positive ───────────────────────────────────────────────
        if self._has_upload:
            fmt = self._formats[0] if self._formats else "PDF"
            cases.append({
                "type":            "Positive",
                "description":     "Verify " + actor + " can successfully upload a valid " + fmt.upper() + " file",
                "preconditions":   "A valid " + fmt.upper() + " file within the allowed size limit is available.",
                "steps":           ("1. Navigate to the upload section.\n"
                                    "2. Select a valid " + fmt.upper() + " file.\n"
                                    "3. Click Upload / Submit.\n"
                                    "4. Observe feedback."),
                "expected_result": "File is uploaded successfully. A confirmation message is displayed. File appears in the system.",
                "priority":        "High",
            })

        # ── P7: Email notification positive ───────────────────────────────────
        if self._has_email:
            cases.append({
                "type":            "Positive",
                "description":     "Verify system sends a correctly formatted email to a valid address",
                "preconditions":   "A valid, reachable email address is registered in the system.",
                "steps":           ("1. Trigger the action that initiates an email (e.g., password reset, registration).\n"
                                    "2. Check the inbox of the registered email address.\n"
                                    "3. Open and inspect the received email."),
                "expected_result": "Email is received within the expected time. It contains the correct subject, body, and any required links/tokens.",
                "priority":        "High",
            })

        # ── P8: Report / export positive ──────────────────────────────────────
        if self._has_report:
            cases.append({
                "type":            "Positive",
                "description":     "Verify " + actor + " can successfully generate and download a report",
                "preconditions":   "Sufficient data exists to produce a non-empty report.",
                "steps":           ("1. Navigate to the report/export section.\n"
                                    "2. Apply valid filters or parameters if applicable.\n"
                                    "3. Click Generate / Export.\n"
                                    "4. Download and open the file."),
                "expected_result": "Report is generated with correct data. File downloads in the expected format. No data is missing or corrupted.",
                "priority":        "Medium",
            })

        # ── P9: Search / filter positive ──────────────────────────────────────
        if self._has_search:
            cases.append({
                "type":            "Positive",
                "description":     "Verify search/filter returns accurate results for a valid query",
                "preconditions":   "At least one matching " + obj + " exists in the system.",
                "steps":           ("1. Navigate to the search or filter interface.\n"
                                    "2. Enter a valid, known search term or apply a valid filter.\n"
                                    "3. Submit the query.\n"
                                    "4. Inspect results."),
                "expected_result": "Matching results are returned. Results are accurate and sorted/filtered correctly.",
                "priority":        "Medium",
            })

        # ── P10: Delete positive ──────────────────────────────────────────────
        if self._has_delete:
            cases.append({
                "type":            "Positive",
                "description":     "Verify authorised " + actor + " can successfully delete/remove a " + obj,
                "preconditions":   "At least one " + obj + " exists. " + actor.capitalize() + " has delete permission.",
                "steps":           ("1. Locate an existing " + obj + ".\n"
                                    "2. Select the delete/remove option.\n"
                                    "3. Confirm the deletion if prompted.\n"
                                    "4. Verify the item is removed."),
                "expected_result": obj.capitalize() + " is deleted. It no longer appears in the system. A success message is shown.",
                "priority":        "High",
            })

        # ── P11: Concurrent usage (if mentioned) ──────────────────────────────
        if self._has_concurrency:
            cases.append({
                "type":            "Positive",
                "description":     "Verify system handles multiple concurrent users performing the action simultaneously",
                "preconditions":   "Multiple valid test accounts exist.",
                "steps":           ("1. Simulate 5 (or the specified number of) concurrent users.\n"
                                    "2. Each user performs the described action simultaneously.\n"
                                    "3. Observe system response and data integrity."),
                "expected_result": "All users receive correct responses. No data corruption, deadlocks, or race conditions occur.",
                "priority":        "Medium",
            })

        # ── P12: Boundary repeat / stress (always) ────────────────────────────
        cases.append({
            "type":            "Positive",
            "description":     "Verify system produces consistent results across 10 consecutive executions",
            "preconditions":   "Stable environment. Valid test data prepared.",
            "steps":           ("1. Execute the requirement scenario 10 times consecutively using valid inputs.\n"
                                "2. Record the outcome of each execution."),
            "expected_result": "All 10 executions produce correct and identical results. No degradation or inconsistency.",
            "priority":        "Low",
        })

        return cases

    # ── Negative tests ────────────────────────────────────────────────────────

    def generateNegativeTests(self) -> list:
        cases = []
        actor = self._actors[0] if self._actors else "the user"
        obj   = self._objects[0] if self._objects else "the resource"

        # ── N1: Empty / null input ────────────────────────────────────────────
        cases.append({
            "type":            "Negative",
            "description":     "Verify system rejects empty or null input gracefully",
            "preconditions":   "System is running.",
            "steps":           ("1. Leave all required fields blank (null / empty string).\n"
                                "2. Attempt to trigger the action.\n"
                                "3. Observe the response."),
            "expected_result": "System displays a clear validation error. Action is blocked. No crash occurs.",
            "priority":        "High",
        })

        # ── N2: Each numeric boundary violation ───────────────────────────────
        for num in self._numerics:
            inv = self._invert_numeric(num)
            cases.append({
                "type":            "Negative",
                "description":     "Verify system rejects input violating boundary: " + num["raw"],
                "preconditions":   "System is running. Valid environment set up.",
                "steps":           ("1. Prepare input that " + inv["desc"] + ".\n"
                                    "2. As " + actor + ", submit this value.\n"
                                    "3. Observe the system response."),
                "expected_result": ("System rejects the value. An appropriate error message is shown "
                                    "(boundary violated: " + num["raw"] + "). No action is completed."),
                "priority":        "High",
            })

        # ── N3: Condition NOT met ─────────────────────────────────────────────
        for cond in self._conditions:
            cases.append({
                "type":            "Negative",
                "description":     "Verify system handles case where condition is NOT met: '" + cond["clause"] + "'",
                "preconditions":   "The condition '" + cond["clause"] + "' is deliberately false.",
                "steps":           ("1. Ensure condition '" + cond["clause"] + "' is NOT satisfied.\n"
                                    "2. As " + actor + ", attempt to trigger the action.\n"
                                    "3. Observe the outcome."),
                "expected_result": ("System either blocks the action with a clear message, "
                                    "or handles the unmet condition gracefully."),
                "priority":        "High",
            })

        # ── N4: Invalid format / type ─────────────────────────────────────────
        if self._formats:
            fmt = self._formats[0]
            wrong = "TXT" if fmt.upper() != "TXT" else "MP4"
            cases.append({
                "type":            "Negative",
                "description":     "Verify system rejects an unsupported file/data format (expected: " + fmt.upper() + ")",
                "preconditions":   "An invalid-format file (e.g., " + wrong + " instead of " + fmt.upper() + ") is prepared.",
                "steps":           ("1. As " + actor + ", attempt to submit a " + wrong + " file where " + fmt.upper() + " is expected.\n"
                                    "2. Observe the system response."),
                "expected_result": "System rejects the file. A clear format error message is displayed. No data is processed.",
                "priority":        "High",
            })

        # ── N5: Malformed / special character input ───────────────────────────
        cases.append({
            "type":            "Negative",
            "description":     "Verify system is protected against malformed and malicious input",
            "preconditions":   "System is running.",
            "steps":           ("1. Enter special characters: <script>alert('xss')</script>, "
                                "' OR 1=1 --, ../../../etc/passwd into input fields.\n"
                                "2. Submit and observe."),
            "expected_result": ("System sanitises input. No XSS, SQL injection, or path traversal succeeds. "
                                "Error is displayed or input is safely escaped."),
            "priority":        "High",
        })

        # ── N6: Auth — wrong credentials ──────────────────────────────────────
        if self._has_auth:
            cases.append({
                "type":            "Negative",
                "description":     "Verify system rejects authentication with invalid credentials",
                "preconditions":   "A valid account exists.",
                "steps":           ("1. Enter a valid username but an incorrect password.\n"
                                    "2. Submit credentials.\n"
                                    "3. Observe the response."),
                "expected_result": "Login is denied. An error message is shown (e.g., 'Invalid credentials'). Session is NOT created.",
                "priority":        "High",
            })

            # ── N7: Account lockout after repeated failures ────────────────────
            cases.append({
                "type":            "Negative",
                "description":     "Verify account is locked after repeated failed authentication attempts",
                "preconditions":   "A valid account exists.",
                "steps":           ("1. Enter incorrect credentials 5 times (or the configured limit) in succession.\n"
                                    "2. Attempt to log in a 6th time with valid credentials.\n"
                                    "3. Observe the outcome."),
                "expected_result": ("Account is locked after the allowed number of failures. "
                                    "Access is denied even with correct credentials until unlocked."),
                "priority":        "High",
            })

            # ── N8: Unauthorised role access ──────────────────────────────────
            cases.append({
                "type":            "Negative",
                "description":     "Verify system prevents access by an unauthorised role",
                "preconditions":   "A user with insufficient permissions is logged in.",
                "steps":           ("1. Log in as a low-privilege user (e.g., guest).\n"
                                    "2. Attempt to access a resource/feature requiring higher privileges.\n"
                                    "3. Observe the outcome."),
                "expected_result": ("Access is denied. An 'Unauthorised' or 'Forbidden' message is shown. "
                                    "The protected resource is not exposed."),
                "priority":        "High",
            })

        # ── N9: Upload — oversized file ───────────────────────────────────────
        if self._has_upload:
            size_limit = "10 MB"  # default; look for numeric clue
            for num in self._numerics:
                if num["unit"].lower() in ("mb", "gb", "kb"):
                    size_limit = num["value"] + " " + num["unit"].upper()
                    break
            cases.append({
                "type":            "Negative",
                "description":     "Verify system rejects a file that exceeds the size limit (" + size_limit + ")",
                "preconditions":   "A file larger than " + size_limit + " is available.",
                "steps":           ("1. As " + actor + ", attempt to upload a file larger than " + size_limit + ".\n"
                                    "2. Submit and observe."),
                "expected_result": ("Upload is blocked. Error message states the file exceeds "
                                    "the size limit (" + size_limit + "). No partial data is stored."),
                "priority":        "High",
            })

        # ── N10: Email — invalid address ──────────────────────────────────────
        if self._has_email:
            cases.append({
                "type":            "Negative",
                "description":     "Verify system rejects an invalid email address format",
                "preconditions":   "System is running.",
                "steps":           ("1. Enter malformed email addresses: 'user@', '@domain.com', "
                                    "'userATdomain.com', '' (empty).\n"
                                    "2. Submit and observe."),
                "expected_result": ("System rejects each invalid email. "
                                    "A clear validation error is displayed for each case."),
                "priority":        "High",
            })

        # ── N11: Search — no results ──────────────────────────────────────────
        if self._has_search:
            cases.append({
                "type":            "Negative",
                "description":     "Verify system handles a search query that returns no results",
                "preconditions":   "The search term does not match any existing " + obj + ".",
                "steps":           ("1. Enter a search term known to match nothing (e.g., '###NONEXISTENT###').\n"
                                    "2. Submit the query.\n"
                                    "3. Observe the response."),
                "expected_result": ("A 'No results found' message is displayed gracefully. "
                                    "No error or crash occurs. The UI remains functional."),
                "priority":        "Medium",
            })

        # ── N12: Delete — wrong user / no permission ──────────────────────────
        if self._has_delete:
            cases.append({
                "type":            "Negative",
                "description":     "Verify system blocks deletion by an unauthorised " + actor,
                "preconditions":   "An existing " + obj + " is present. User lacks delete permission.",
                "steps":           ("1. Log in as a user without delete permission.\n"
                                    "2. Attempt to delete the " + obj + " via the UI or API.\n"
                                    "3. Observe the result."),
                "expected_result": ("Deletion is blocked. Error message states insufficient permissions. "
                                    + obj.capitalize() + " remains in the system."),
                "priority":        "High",
            })

        # ── N13: Session expiry / timeout ─────────────────────────────────────
        if self._has_auth or "session" in self._lower or "timeout" in self._lower:
            timeout_val = "30 minutes"
            for num in self._numerics:
                if num["unit"].lower() in ("minute", "second", "hour"):
                    timeout_val = num["value"] + " " + num["unit"]
                    break
            cases.append({
                "type":            "Negative",
                "description":     "Verify system handles session expiry correctly after " + timeout_val + " of inactivity",
                "preconditions":   "User is logged in with an active session.",
                "steps":           ("1. Log in as a valid user.\n"
                                    "2. Leave the session idle for " + timeout_val + " (or simulate timeout).\n"
                                    "3. Attempt to perform an action.\n"
                                    "4. Observe the result."),
                "expected_result": ("Session is expired. User is redirected to login. "
                                    "No sensitive data is accessible without re-authentication."),
                "priority":        "Medium",
            })

        # ── N14: Network / connectivity failure ───────────────────────────────
        cases.append({
            "type":            "Negative",
            "description":     "Verify system responds gracefully when network connectivity is lost",
            "preconditions":   "System is running. Network can be interrupted.",
            "steps":           ("1. As " + actor + ", begin performing the action.\n"
                                "2. Simulate a network interruption mid-action (disconnect internet/VPN).\n"
                                "3. Observe the system behaviour."),
            "expected_result": ("System displays a meaningful connectivity error. "
                                "No data is corrupted or partially saved without user knowledge. "
                                "System recovers or allows retry once connectivity is restored."),
            "priority":        "Medium",
        })

        # ── N15: Duplicate submission ─────────────────────────────────────────
        cases.append({
            "type":            "Negative",
            "description":     "Verify system prevents or handles duplicate submission of the same action",
            "preconditions":   "Valid data is prepared.",
            "steps":           ("1. As " + actor + ", submit the action with valid data.\n"
                                "2. Without refreshing, immediately submit the exact same data again.\n"
                                "3. Observe whether a duplicate is created."),
            "expected_result": ("System either prevents the duplicate (shows a warning) or handles it "
                                "idempotently. No duplicate records are created in the system."),
            "priority":        "Medium",
        })

        return cases

    # ── Boundary inversion helper ─────────────────────────────────────────────

    @staticmethod
    def _invert_numeric(num: dict) -> dict:
        q    = (num["qualifier"] or "").lower().strip()
        val  = num["value"]
        unit = num["unit"]

        if "within" in q or "at most" in q or "no more than" in q or "maximum" in q:
            return {"desc": "exceeds the limit: " + val + " " + unit +
                            " (e.g., value = " + str(int(float(val.replace(",","")) * 2)) + " " + unit + ")"}
        if "at least" in q or "minimum" in q or "no less than" in q:
            return {"desc": "is below the minimum: " + val + " " + unit +
                            " (e.g., value = " + str(max(0, int(float(val.replace(",","")) / 2))) + " " + unit + ")"}
        if "more than" in q or "greater than" in q:
            return {"desc": "is equal to or less than " + val + " " + unit}
        if "less than" in q or "fewer than" in q:
            return {"desc": "is equal to or greater than " + val + " " + unit}
        if "exactly" in q:
            return {"desc": "differs from the exact value of " + val + " " + unit +
                            " (e.g., " + str(int(float(val.replace(",","")) + 1)) + " " + unit + ")"}
        # default: just go over
        return {"desc": "violates the boundary: " + num["raw"] +
                        " (use a value clearly outside the allowed range)"}
