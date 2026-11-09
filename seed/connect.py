"""Log in to the org.

Two options, tried in this order:
1. Salesforce CLI: if you've run `sf org login web --alias edu-ido`, we borrow
   that session. No password is stored anywhere. (Recommended.)
2. Username, password and security token from a .env file.
"""

import json
import os
import shutil
import subprocess

from simple_salesforce import Salesforce

API_VERSION = "65.0"


def connect_with_cli(target_org: str) -> Salesforce:
    """Use the access token from an org the Salesforce CLI is logged in to."""
    if shutil.which("sf") is None:
        raise RuntimeError("The Salesforce CLI (sf) is not installed or not on PATH.")

    result = subprocess.run(
        ["sf", "org", "display", "--target-org", target_org, "--json"],
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout or "{}")
    if payload.get("status") != 0:
        message = payload.get("message", result.stderr.strip())
        raise RuntimeError(f"sf org display failed for '{target_org}': {message}")

    org = payload["result"]
    return Salesforce(
        instance_url=org["instanceUrl"],
        session_id=org["accessToken"],
        version=API_VERSION,
    )


def connect_with_password() -> Salesforce:
    """Use SF_USERNAME, SF_PASSWORD and SF_SECURITY_TOKEN from the environment."""
    from dotenv import load_dotenv

    load_dotenv()
    missing = [k for k in ("SF_USERNAME", "SF_PASSWORD") if not os.getenv(k)]
    if missing:
        raise RuntimeError(f"Missing in .env: {', '.join(missing)}")

    return Salesforce(
        username=os.environ["SF_USERNAME"],
        password=os.environ["SF_PASSWORD"],
        security_token=os.getenv("SF_SECURITY_TOKEN", ""),
        domain=os.getenv("SF_DOMAIN", "login"),
        version=API_VERSION,
    )


def connect(target_org: str | None) -> Salesforce:
    if target_org:
        return connect_with_cli(target_org)
    return connect_with_password()
