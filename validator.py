# validator.py
# Validates requirements for ambiguity, completeness, and produces a quality score 0-100.

import re
from requirement import Requirement

# ── Word lists ────────────────────────────────────────────────────────────────

AMBIGUOUS_WORDS = [
    "etc", "and/or", "some", "maybe", "probably", "might", "often",
    "usually", "generally", "various", "several", "many", "few",
    "appropriate", "adequate", "good", "fast", "easy", "user-friendly",
    "flexible", "robust", "efficient", "effective", "simple", "better",
    "quickly", "soon", "as needed", "if necessary", "as appropriate",
    "reasonable", "whenever possible", "nice", "smooth", "seamless",
]

OBLIGATION_KEYWORDS = [
    "must", "shall", "should", "will", "can", "may",
    "is required", "is able to", "is capable of",
]

# Actor nouns — at least one improves score
ACTOR_WORDS = [
    "user", "admin", "administrator", "system", "application", "app",
    "client", "server", "manager", "operator", "guest", "member",
    "customer", "employee", "student", "teacher", "owner",
]

# Measurable quantifiers improve score
MEASURABLE_PATTERNS = [
    r"\d+\s*(second|minute|hour|day|week|month|year|ms|kb|mb|gb|%|percent|character|char|item|record|attempt|click|step)s?\b",
    r"\b(within|at least|at most|no more than|no less than|maximum|minimum|exactly|up to)\s+\d+",
]

# Condition keywords
CONDITION_KEYWORDS = ["if", "when", "while", "after", "before", "unless", "until"]

# Error/exception handling keywords
ERROR_KEYWORDS = ["error", "fail", "invalid", "exception", "timeout", "reject", "deny", "block"]

MIN_WORD_COUNT = 6
IDEAL_WORD_COUNT = 15   # requirements shorter than this lose some score


# ── Scoring weights ───────────────────────────────────────────────────────────
# Each criterion either adds or deducts from 100

WEIGHTS = {
    "obligation_present":   20,   # +20 if obligation keyword found
    "actor_present":        10,   # +10 if actor/subject found
    "measurable":           15,   # +15 if has measurable criteria
    "adequate_length":      10,   # +10 if >= IDEAL_WORD_COUNT words
    "condition_present":     5,   # +5  if has condition clause
    "error_handling":        5,   # +5  if mentions failure/error
    # deductions
    "ambiguous_word":       -8,   # -8 per ambiguous word (capped at -40)
    "too_short":           -20,   # -20 if below MIN_WORD_COUNT
}


# ── Validator ─────────────────────────────────────────────────────────────────

class RequirementValidator:
    """
    Validates a Requirement and returns:
    {
        "valid": bool,
        "score": int (0-100),
        "grade": str ("A"/"B"/"C"/"D"/"F"),
        "issues": [str],
        "suggestions": [str],
        "details": {criterion: bool/int},
    }
    """

    def __init__(self):
        self._req  = None
        self._text = ""
        self._words = []

    # ── Public ────────────────────────────────────────────────────────────────

    def validate(self, requirement: Requirement) -> dict:
        self._req   = requirement
        self._text  = requirement.description.lower()
        self._words = re.findall(r"\b\w+\b", self._text)

        issues      = []
        suggestions = []
        details     = {}
        score       = 0

        # ── 1. Obligation keyword ─────────────────────────────────────────────
        has_obligation = any(
            re.search(r"\b" + re.escape(kw) + r"\b", self._text)
            for kw in OBLIGATION_KEYWORDS
        )
        details["obligation_present"] = has_obligation
        if has_obligation:
            score += WEIGHTS["obligation_present"]
        else:
            issues.append(
                "Missing obligation keyword — requirements must contain "
                "'must', 'shall', 'should', 'will', 'can', or 'may'."
            )
            suggestions.append(
                "Add an obligation word. Example: change 'The system allows login' "
                "to 'The system must allow login'."
            )

        # ── 2. Actor / subject ────────────────────────────────────────────────
        has_actor = any(
            re.search(r"\b" + re.escape(a) + r"\b", self._text)
            for a in ACTOR_WORDS
        )
        details["actor_present"] = has_actor
        if has_actor:
            score += WEIGHTS["actor_present"]
        else:
            suggestions.append(
                "Specify who or what performs the action "
                "(e.g., 'The user', 'The system', 'An administrator')."
            )

        # ── 3. Measurable criteria ────────────────────────────────────────────
        has_measurable = any(
            re.search(p, self._text) for p in MEASURABLE_PATTERNS
        )
        details["measurable"] = has_measurable
        if has_measurable:
            score += WEIGHTS["measurable"]
        else:
            suggestions.append(
                "Add measurable criteria — e.g., 'within 3 seconds', "
                "'at least 8 characters', 'no more than 3 attempts'."
            )

        # ── 4. Length ─────────────────────────────────────────────────────────
        word_count = len(self._words)
        details["word_count"] = word_count
        if word_count < MIN_WORD_COUNT:
            score += WEIGHTS["too_short"]   # deduct
            issues.append(
                "Requirement is too short (" + str(word_count) + " words). "
                "Minimum is " + str(MIN_WORD_COUNT) + " words."
            )
            suggestions.append(
                "Expand the requirement to describe the actor, action, object, "
                "and any constraints or conditions."
            )
        elif word_count >= IDEAL_WORD_COUNT:
            score += WEIGHTS["adequate_length"]
        details["adequate_length"] = word_count >= IDEAL_WORD_COUNT

        # ── 5. Condition clause ───────────────────────────────────────────────
        has_condition = any(
            re.search(r"\b" + kw + r"\b", self._text)
            for kw in CONDITION_KEYWORDS
        )
        details["condition_present"] = has_condition
        if has_condition:
            score += WEIGHTS["condition_present"]

        # ── 6. Error / exception handling ─────────────────────────────────────
        has_error = any(
            re.search(r"\b" + kw + r"\b", self._text)
            for kw in ERROR_KEYWORDS
        )
        details["error_handling"] = has_error
        if has_error:
            score += WEIGHTS["error_handling"]

        # ── 7. Ambiguous words ────────────────────────────────────────────────
        found_vague = [
            w for w in AMBIGUOUS_WORDS
            if re.search(r"\b" + re.escape(w) + r"\b", self._text)
        ]
        details["ambiguous_words"] = found_vague
        if found_vague:
            deduction = min(len(found_vague) * abs(WEIGHTS["ambiguous_word"]), 40)
            score -= deduction
            quoted = ", ".join('"' + w + '"' for w in found_vague)
            issues.append("Ambiguous language detected: " + quoted + ".")
            suggestions.append(
                "Replace vague terms with precise, measurable language. "
                "E.g., replace 'fast' with 'within 2 seconds', 'good' with "
                "'achieving a success rate of at least 95%'."
            )

        # ── Clamp and grade ───────────────────────────────────────────────────
        score = max(0, min(100, score))
        grade = self._grade(score)

        is_valid = len(issues) == 0
        requirement.update_status("valid" if is_valid else "invalid")
        requirement.score = score

        return {
            "valid":       is_valid,
            "score":       score,
            "grade":       grade,
            "issues":      issues,
            "suggestions": suggestions,
            "details":     details,
        }

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _grade(score: int) -> str:
        if score >= 85: return "A"
        if score >= 70: return "B"
        if score >= 55: return "C"
        if score >= 40: return "D"
        return "F"
