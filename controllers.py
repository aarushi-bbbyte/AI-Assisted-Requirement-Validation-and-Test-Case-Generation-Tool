# controllers.py
# Orchestration layer: wires together domain objects, validators, generators, repos.

from requirement import Requirement
from validator import RequirementValidator
from ai_generator import AITestCaseGenerator
from repository import RequirementRepository, TestCaseRepository
from exporter import FileExporter


class RequirementController:
    def __init__(self, req_repo: RequirementRepository):
        self._repo      = req_repo
        self._validator = RequirementValidator()

    def submit(self, text: str, source: str = "manual") -> Requirement:
        req = Requirement(text, source=source)
        self._repo.save(req)
        return req

    def validate(self, requirement: Requirement) -> dict:
        return self._validator.validate(requirement)


class TestCaseController:
    def __init__(self, tc_repo: TestCaseRepository):
        self._repo      = tc_repo
        self._generator = AITestCaseGenerator()

    def generate(self, requirement: Requirement) -> list:
        if requirement.status != "valid":
            raise ValueError(
                "Cannot generate test cases for requirement REQ-" +
                str(requirement.req_id) + " because it is not valid."
            )
        tcs = self._generator.generateTestCases(requirement)
        self._repo.save_for_req(requirement.req_id, tcs)
        return tcs

    def get_for_req(self, req_id: int) -> list:
        return self._repo.get_for_req(req_id)

    def get_all(self) -> list:
        return self._repo.all()

    def get_all_by_req(self) -> dict:
        return self._repo.all_by_req()


class ExportController:
    def __init__(self, req_repo: RequirementRepository, tc_repo: TestCaseRepository):
        self._req_repo = req_repo
        self._tc_repo  = tc_repo
        self._exporter = FileExporter()

    def export_csv(self, req_id: int = None) -> bytes:
        if req_id is not None:
            tcs = self._tc_repo.get_for_req(req_id)
        else:
            tcs = self._tc_repo.all()
        if not tcs:
            raise ValueError("No test cases to export.")
        return self._exporter.to_csv_bytes(tcs)

    def export_traceability_csv(self) -> bytes:
        reqs   = self._req_repo.all()
        tc_map = self._tc_repo.all_by_req()
        return self._exporter.traceability_csv(reqs, tc_map)
