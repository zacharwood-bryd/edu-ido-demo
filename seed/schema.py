"""Check every record against the org's real schema before inserting it.

Education Cloud field names and picklist values change between releases, so
the loader never trusts them. For each object we call describe() once, then:
- drop fields the org doesn't have (and log them),
- swap picklist values the org doesn't allow for a valid one (and log it),
- warn about required fields we aren't filling.
"""

import logging

log = logging.getLogger(__name__)


class Schema:
    def __init__(self, sf):
        self.sf = sf
        self._cache: dict[str, dict] = {}

    def describe(self, sobject: str) -> dict:
        if sobject not in self._cache:
            self._cache[sobject] = getattr(self.sf, sobject).describe()
        return self._cache[sobject]

    def has_object(self, sobject: str) -> bool:
        try:
            self.describe(sobject)
            return True
        except Exception:
            return False

    def fields(self, sobject: str) -> dict[str, dict]:
        return {f["name"]: f for f in self.describe(sobject)["fields"]}

    def first_field(self, sobject: str, *candidates: str) -> str | None:
        """Return the first candidate field name that exists on the object."""
        available = self.fields(sobject)
        for name in candidates:
            if name in available:
                return name
        return None

    def picklist_values(self, sobject: str, field: str) -> list[str]:
        meta = self.fields(sobject).get(field, {})
        return [v["value"] for v in meta.get("picklistValues", []) if v.get("active")]

    def clean(self, sobject: str, record: dict) -> dict:
        """Return a copy of record that the org will accept."""
        available = self.fields(sobject)
        cleaned = {}
        for name, value in record.items():
            meta = available.get(name)
            if meta is None or not meta.get("createable"):
                log.debug("%s.%s not in org or not createable, skipped", sobject, name)
                continue
            if meta["type"] == "picklist" and value is not None:
                allowed = self.picklist_values(sobject, name)
                if allowed and value not in allowed:
                    log.warning(
                        "%s.%s: '%s' not allowed, using '%s'", sobject, name, value, allowed[0]
                    )
                    value = allowed[0]
            cleaned[name] = value
        self._warn_missing_required(sobject, cleaned)
        return cleaned

    def _warn_missing_required(self, sobject: str, record: dict) -> None:
        for name, meta in self.fields(sobject).items():
            required = (
                meta.get("createable")
                and not meta.get("nillable")
                and not meta.get("defaultedOnCreate")
                and meta["type"] != "boolean"
            )
            if required and name not in record:
                log.warning("%s.%s is required and not set; insert may fail", sobject, name)
