# requirement.py
# Domain model for a single software requirement

import time

class Requirement:
    """
    Represents one software requirement.
    Attributes:
        req_id      : unique int ID within a session
        description : raw text
        status      : 'pending' | 'valid' | 'invalid'
        score       : quality score 0-100 (set after validation)
        source      : 'manual' | filename of uploaded doc
        created_at  : epoch timestamp
    """

    _counter = 0  # class-level auto-increment

    def __init__(self, description: str, source: str = "manual"):
        Requirement._counter += 1
        self.req_id      = Requirement._counter
        self.description = description.strip()
        self.status      = "pending"
        self.score       = None       # filled by validator
        self.source      = source
        self.created_at  = time.time()

    def update_status(self, new_status: str):
        allowed = {"pending", "valid", "invalid"}
        if new_status not in allowed:
            raise ValueError("Status must be one of " + str(allowed))
        self.status = new_status

    @classmethod
    def reset_counter(cls):
        cls._counter = 0

    def __repr__(self):
        return ("Requirement(id=" + str(self.req_id) +
                ", status=" + repr(self.status) +
                ", text=" + repr(self.description[:40]) + ")")
