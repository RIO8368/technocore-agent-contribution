import json
from pathlib import Path


REQUIRED_FIELDS = {
    "artifact_url",
    "commit",
    "did",
    "schema",
    "signature",
}

EXPECTED_SCHEMA = "technocore-contribution-proof-v1"


def inspect_proof(path: str) -> list[str]:
    issues = []
    proof_path = Path(path)

    if not proof_path.exists():
        return ["proof file does not exist"]

    try:
        data = json.loads(proof_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ["invalid JSON"]

    if not isinstance(data, dict):
        return ["proof root must be an object"]

    missing = REQUIRED_FIELDS - set(data.keys())

    for field in sorted(missing):
        issues.append(f"missing field: {field}")

    schema = data.get("schema")

    if schema is not None and schema != EXPECTED_SCHEMA:
        issues.append("invalid proof schema")

    did = data.get("did")

    if did is not None:
        if not isinstance(did, str) or not did.startswith("did:key:"):
            issues.append("invalid DID format")

    commit = data.get("commit")

    if commit is not None:
        if (
            not isinstance(commit, str)
            or len(commit) != 40
            or any(c not in "0123456789abcdef" for c in commit.lower())
        ):
            issues.append("invalid commit hash")

    artifact_url = data.get("artifact_url")

    if artifact_url is not None:
        if (
            not isinstance(artifact_url, str)
            or not artifact_url.startswith("https://github.com/")
        ):
            issues.append("invalid GitHub artifact URL")

    signature = data.get("signature")

    if signature is not None:
        if not isinstance(signature, str) or not signature:
            issues.append("invalid signature")

    return issues


def main() -> None:
    print("Technocore Proof Inspector")
    print("--------------------------")
    print("Inspector loaded.")
    print("Schema:", EXPECTED_SCHEMA)


if __name__ == "__main__":
    main()