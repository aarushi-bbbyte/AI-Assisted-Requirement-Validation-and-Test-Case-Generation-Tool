# repository.py
# In-memory repositories for requirements and test cases.

from requirement import Requirement


class RequirementRepository:
    """Stores Requirement objects in memory, keyed by req_id."""

    def __init__(self):
        self._store = {}  # req_id -> Requirement

    def save(self, requirement: Requirement) -> int:
        self._store[requirement.req_id] = requirement
        return requirement.req_id

    def find_by_id(self, req_id: int):
        return self._store.get(req_id)

    def all(self) -> list:
        return list(self._store.values())

    def clear(self):
        self._store.clear()

    def count(self) -> int:
        return len(self._store)


class TestCaseRepository:
    """Stores test case dicts in memory, grouped by requirement ID."""

    def __init__(self):
        # req_id -> list of test case dicts
        self._store = {}

    def save_for_req(self, req_id: int, test_cases: list):
        self._store[req_id] = list(test_cases)

    def get_for_req(self, req_id: int) -> list:
        return self._store.get(req_id, [])

    def all(self) -> list:
        """Return all test cases across all requirements as a flat list."""
        result = []
        for tcs in self._store.values():
            result.extend(tcs)
        return result

    def all_by_req(self) -> dict:
        """Return dict of req_id -> [test_cases]."""
        return dict(self._store)

    def clear(self):
        self._store.clear()
