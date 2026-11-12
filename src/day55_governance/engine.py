"""Audit, consent, retention, storage and access control."""

import hashlib
import json
import os
import tempfile

from datetime import datetime, timezone, timedelta
from pathlib import Path

from .config import RETENTION_POLICIES, ROLES, ALLOWED_DATA_CATEGORIES


class GovernanceError(Exception):
    """Raised when a governance or security rule is violated."""


class GovernanceEngine:

    def __init__(self, base_directory="secure_storage"):

        self.base = Path(base_directory)
        self.transcript_dir = self.base / "transcripts"
        self.report_dir = self.base / "reports"
        self.audit_file = self.base / "audit" / "audit_log.jsonl"
        self.consent_file = self.base / "consent" / "consent_records.json"

        for directory in (
            self.transcript_dir,
            self.report_dir,
            self.audit_file.parent,
            self.consent_file.parent
        ):
            directory.mkdir(parents=True, exist_ok=True)

        if not self.consent_file.exists():
            self._write_json(self.consent_file, {})

    # ------------------------------------------------------
    # COMMON HELPERS
    # ------------------------------------------------------

    def _now(self):
        return datetime.now(timezone.utc)

    def _timestamp(self):
        return self._now().isoformat()

    def _write_json(self, path, data):

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            delete=False,
            suffix=".tmp"
        ) as temporary:

            json.dump(
                data,
                temporary,
                indent=4,
                ensure_ascii=False
            )

            temporary_path = Path(temporary.name)

        os.replace(temporary_path, path)

    def _read_json(self, path):

        path = Path(path)

        if not path.exists():
            return {}

        with path.open("r", encoding="utf-8-sig") as file:
            return json.load(file)

    def _validate_identifier(self, value):

        if not isinstance(value, str) or not value.strip():
            raise GovernanceError("A valid identifier is required.")

        if len(value) > 100:
            raise GovernanceError("Identifier is too long.")

        return value.strip()

    # ------------------------------------------------------
    # ACCESS CONTROL
    # ------------------------------------------------------

    def authorize(self, role, permission):

        if role not in ROLES:
            raise GovernanceError("Unknown user role.")

        if permission not in ROLES[role]:
            raise GovernanceError(
                f"Access denied: role '{role}' cannot perform '{permission}'."
            )

        return True

    # ------------------------------------------------------
    # AUDIT TRAIL WITH HASH CHAIN
    # ------------------------------------------------------

    def _read_audit_records(self):

        if not self.audit_file.exists():
            return []

        records = []

        with self.audit_file.open("r", encoding="utf-8-sig") as file:

            for line in file:

                if line.strip():
                    records.append(json.loads(line))

        return records

    def log_event(
        self,
        actor,
        event_type,
        resource_type,
        resource_id,
        details=None
    ):

        actor = self._validate_identifier(actor)
        resource_id = self._validate_identifier(resource_id)

        if not isinstance(event_type, str) or not event_type.strip():
            raise GovernanceError("Event type is required.")

        if not isinstance(resource_type, str) or not resource_type.strip():
            raise GovernanceError("Resource type is required.")

        records = self._read_audit_records()

        previous_hash = (
            records[-1]["record_hash"]
            if records else "GENESIS"
        )

        record = {
            "timestamp": self._timestamp(),
            "actor": actor,
            "event_type": event_type,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "details": details or {},
            "previous_hash": previous_hash
        }

        canonical = json.dumps(
            record,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False
        )

        record["record_hash"] = hashlib.sha256(
            canonical.encode("utf-8")
        ).hexdigest()

        with self.audit_file.open("a", encoding="utf-8") as file:

            file.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

        return record

    def verify_audit_trail(self, role):

        self.authorize(role, "audit.verify")

        records = self._read_audit_records()
        previous_hash = "GENESIS"

        for index, record in enumerate(records):

            if record.get("previous_hash") != previous_hash:
                return {
                    "valid": False,
                    "failed_record": index,
                    "reason": "Previous hash mismatch."
                }

            supplied_hash = record.get("record_hash")

            content = {
                key: value
                for key, value in record.items()
                if key != "record_hash"
            }

            canonical = json.dumps(
                content,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False
            )

            expected_hash = hashlib.sha256(
                canonical.encode("utf-8")
            ).hexdigest()

            if supplied_hash != expected_hash:
                return {
                    "valid": False,
                    "failed_record": index,
                    "reason": "Record hash mismatch."
                }

            previous_hash = supplied_hash

        return {
            "valid": True,
            "records_checked": len(records),
            "reason": "Audit chain integrity verified."
        }

    # ------------------------------------------------------
    # SCORE AND DECISION LOGGING
    # ------------------------------------------------------

    def log_score(
        self,
        actor,
        candidate_id,
        score,
        scoring_model,
        role="admin"
    ):

        self.authorize(role, "audit.read")

        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise GovernanceError("Score must be numeric.")

        if not 0 <= score <= 100:
            raise GovernanceError("Score must be between 0 and 100.")

        if not isinstance(scoring_model, str) or not scoring_model.strip():
            raise GovernanceError("Scoring model name is required.")

        return self.log_event(
            actor,
            "SCORE_GENERATED",
            "candidate_score",
            candidate_id,
            {
                "score": score,
                "scoring_model": scoring_model
            }
        )

    def log_decision(
        self,
        actor,
        candidate_id,
        decision,
        reason,
        role="admin"
    ):

        self.authorize(role, "audit.read")

        if not isinstance(decision, str) or not decision.strip():
            raise GovernanceError("Decision is required.")

        if not isinstance(reason, str) or not reason.strip():
            raise GovernanceError("Decision reason is required.")

        return self.log_event(
            actor,
            "HIRING_DECISION",
            "candidate_decision",
            candidate_id,
            {
                "decision": decision,
                "reason": reason,
                "human_review_required": True
            }
        )

    # ------------------------------------------------------
    # CONSENT MANAGEMENT
    # ------------------------------------------------------

    def record_consent(
        self,
        candidate_id,
        purpose,
        granted,
        actor="admin"
    ):

        candidate_id = self._validate_identifier(candidate_id)

        if not isinstance(purpose, str) or not purpose.strip():
            raise GovernanceError("Consent purpose is required.")

        if not isinstance(granted, bool):
            raise GovernanceError("Consent must be True or False.")

        records = self._read_json(self.consent_file)

        candidate_records = records.setdefault(candidate_id, [])

        entry = {
            "purpose": purpose,
            "granted": granted,
            "timestamp": self._timestamp(),
            "actor": actor
        }

        candidate_records.append(entry)

        self._write_json(self.consent_file, records)

        self.log_event(
            actor,
            "CONSENT_GRANTED" if granted else "CONSENT_DENIED",
            "consent",
            candidate_id,
            {"purpose": purpose}
        )

        return entry

    def has_consent(self, candidate_id, purpose):

        candidate_id = self._validate_identifier(candidate_id)

        records = self._read_json(self.consent_file)

        entries = records.get(candidate_id, [])

        matching = [
            item for item in entries
            if item["purpose"] == purpose
        ]

        if not matching:
            return False

        # Latest consent record controls current consent status.
        latest = max(
            matching,
            key=lambda item: item["timestamp"]
        )

        return latest["granted"] is True

    # ------------------------------------------------------
    # SECURE TRANSCRIPT AND REPORT STORAGE
    # ------------------------------------------------------

    def store_data(
        self,
        role,
        category,
        record_id,
        candidate_id,
        content,
        purpose,
        actor
    ):

        if category not in ALLOWED_DATA_CATEGORIES:
            raise GovernanceError("Unsupported storage category.")

        permission = (
            "transcript.write"
            if category == "transcripts"
            else "report.write"
        )

        self.authorize(role, permission)

        record_id = self._validate_identifier(record_id)
        candidate_id = self._validate_identifier(candidate_id)

        if not self.has_consent(candidate_id, purpose):
            raise GovernanceError(
                "Data cannot be stored without valid consent."
            )

        if not isinstance(content, dict):
            raise GovernanceError("Content must be a dictionary.")

        directory = (
            self.transcript_dir
            if category == "transcripts"
            else self.report_dir
        )

        path = directory / f"{record_id}.json"

        if path.exists():
            raise GovernanceError("Record already exists.")

        record = {
            "record_id": record_id,
            "candidate_id": candidate_id,
            "category": category,
            "purpose": purpose,
            "created_at": self._timestamp(),
            "content": content
        }

        self._write_json(path, record)

        self.log_event(
            actor,
            "DATA_STORED",
            category,
            record_id,
            {
                "candidate_id": candidate_id,
                "purpose": purpose
            }
        )

        return {
            "status": "stored",
            "record_id": record_id,
            "category": category
        }

    def read_data(self, role, category, record_id, actor):

        if category == "transcripts":
            self.authorize(role, "transcript.read")
            directory = self.transcript_dir

        elif category == "reports":
            self.authorize(role, "report.read")
            directory = self.report_dir

        else:
            raise GovernanceError("Unsupported storage category.")

        record_id = self._validate_identifier(record_id)

        path = directory / f"{record_id}.json"

        if not path.exists():
            raise GovernanceError("Requested record does not exist.")

        record = self._read_json(path)

        if not self.has_consent(
            record["candidate_id"],
            record["purpose"]
        ):
            raise GovernanceError(
                "Access denied because consent is no longer valid."
            )

        self.log_event(
            actor,
            "DATA_ACCESSED",
            category,
            record_id
        )

        return record

    def delete_data(self, role, category, record_id, actor):

        if category == "transcripts":
            self.authorize(role, "transcript.delete")
            directory = self.transcript_dir

        elif category == "reports":
            self.authorize(role, "report.delete")
            directory = self.report_dir

        else:
            raise GovernanceError("Unsupported storage category.")

        record_id = self._validate_identifier(record_id)
        path = directory / f"{record_id}.json"

        if not path.exists():
            raise GovernanceError("Record does not exist.")

        path.unlink()

        self.log_event(
            actor,
            "DATA_DELETED",
            category,
            record_id
        )

        return {"status": "deleted", "record_id": record_id}

    # ------------------------------------------------------
    # DATA RETENTION
    # ------------------------------------------------------

    def apply_retention(
        self,
        role="admin",
        now=None
    ):

        self.authorize(role, "retention.manage")

        now = now or self._now()

        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)

        deleted = {
            "transcripts": [],
            "reports": []
        }

        directories = {
            "transcripts": self.transcript_dir,
            "reports": self.report_dir
        }

        for category, directory in directories.items():

            retention_days = RETENTION_POLICIES[category]

            cutoff = now - timedelta(days=retention_days)

            for path in directory.glob("*.json"):

                record = self._read_json(path)

                created_at = datetime.fromisoformat(
                    record["created_at"]
                )

                if created_at.tzinfo is None:
                    created_at = created_at.replace(
                        tzinfo=timezone.utc
                    )

                if created_at < cutoff:

                    record_id = record["record_id"]

                    path.unlink()

                    deleted[category].append(record_id)

                    self.log_event(
                        "retention_service",
                        "RETENTION_DELETION",
                        category,
                        record_id,
                        {"retention_days": retention_days}
                    )

        return {
            "status": "completed",
            "deleted_records": deleted,
            "retention_policies": RETENTION_POLICIES
        }

    # ------------------------------------------------------
    # GOVERNANCE SUMMARY
    # ------------------------------------------------------

    def governance_summary(self):

        audit_records = self._read_audit_records()

        return {
            "audit_record_count": len(audit_records),
            "transcript_count": len(
                list(self.transcript_dir.glob("*.json"))
            ),
            "report_count": len(
                list(self.report_dir.glob("*.json"))
            ),
            "retention_policies": RETENTION_POLICIES,
            "access_roles": list(ROLES.keys()),
            "consent_required": True
        }
