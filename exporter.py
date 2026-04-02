# exporter.py
# Serialises test cases and traceability data to CSV.

import csv
import io
import time


class FileExporter:

    TC_FIELDS = ["id", "requirement_id", "requirement_text", "type",
                 "description", "preconditions", "steps", "expected_result", "priority"]

    TRACE_FIELDS = ["req_id", "requirement", "status", "quality_score",
                    "total_tests", "positive_tests", "negative_tests", "test_ids"]

    # ── Test case CSV ─────────────────────────────────────────────────────────

    def to_csv_bytes(self, test_cases: list) -> bytes:
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=self.TC_FIELDS,
                                extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for tc in test_cases:
            row = dict(tc)
            row["steps"] = (row.get("steps") or "").replace("\n", " | ")
            writer.writerow(row)
        return buf.getvalue().encode("utf-8")

    # ── Traceability matrix CSV ───────────────────────────────────────────────

    def traceability_csv(self, requirements: list, tc_map: dict) -> bytes:
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=self.TRACE_FIELDS,
                                extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for req in requirements:
            tcs  = tc_map.get(req.req_id, [])
            pos  = [t for t in tcs if t.get("type") == "Positive"]
            neg  = [t for t in tcs if t.get("type") == "Negative"]
            ids  = ", ".join(t.get("id", "") for t in tcs) if tcs else "—"
            writer.writerow({
                "req_id":          "REQ-" + str(req.req_id).zfill(3),
                "requirement":     req.description,
                "status":          req.status,
                "quality_score":   req.score if req.score is not None else "—",
                "total_tests":     len(tcs),
                "positive_tests":  len(pos),
                "negative_tests":  len(neg),
                "test_ids":        ids,
            })
        return buf.getvalue().encode("utf-8")
