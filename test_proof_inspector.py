import json
import tempfile
from pathlib import Path

from proof_inspector import inspect_proof


def write_json(data):
    temp = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False,
        encoding="utf-8",
    )

    json.dump(data, temp)
    temp.close()

    return Path(temp.name)


def run_test(name, data, expected_errors):
    path = write_json(data)

    try:
        issues = inspect_proof(str(path))

        if len(issues) == expected_errors:
            print(f"PASS: {name}")
            return True

        print(
            f"FAIL: {name} "
            f"(expected {expected_errors}, got {len(issues)})"
        )

        for issue in issues:
            print(f"  - {issue}")

        return False

    finally:
        path.unlink(missing_ok=True)


def main():
    valid_proof = {
        "artifact_url": (
            "https://github.com/example/repo/blob/main/test.py"
        ),
        "commit": "a" * 40,
        "did": "did:key:test-agent",
        "schema": "technocore-contribution-proof-v1",
        "signature": "test-signature",
    }

    tests = [
        (
            "valid proof",
            valid_proof,
            0,
        ),
        (
            "missing DID",
            {
                "artifact_url": valid_proof["artifact_url"],
                "commit": valid_proof["commit"],
                "schema": valid_proof["schema"],
                "signature": valid_proof["signature"],
            },
            1,
        ),
        (
            "invalid DID",
            {
                **valid_proof,
                "did": "not-a-did",
            },
            1,
        ),
        (
            "invalid commit",
            {
                **valid_proof,
                "commit": "12345",
            },
            1,
        ),
        (
            "invalid GitHub URL",
            {
                **valid_proof,
                "artifact_url": "https://example.com/test",
            },
            1,
        ),
        (
            "invalid schema",
            {
                **valid_proof,
                "schema": "wrong-schema",
            },
            1,
        ),
        (
            "empty signature",
            {
                **valid_proof,
                "signature": "",
            },
            1,
        ),
        (
            "missing multiple fields",
            {
                "did": valid_proof["did"],
            },
            4,
        ),
    ]

    passed = 0

    for name, data, expected_errors in tests:
        if run_test(name, data, expected_errors):
            passed += 1

    print()
    print(f"{passed}/{len(tests)} tests passed")


if __name__ == "__main__":
    main()