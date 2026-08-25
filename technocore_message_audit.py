"""
Technocore Message Audit Tool

Audits Technocore-style messages for:
- duplicate sequence numbers
- invalid DID
- duplicate/replayed nonces
- non-increasing nonces
"""

from typing import Any


def audit_messages(messages: list[dict[str, Any]]) -> list[str]:
    issues: list[str] = []

    seen_sequences: set[int] = set()
    last_nonce_by_did: dict[str, int] = {}
    seen_nonce_by_did: dict[str, set[int]] = {}

    for index, message in enumerate(messages):
        prefix = f"message[{index}]"

        if not isinstance(message, dict):
            issues.append(f"{prefix}: message is not an object")
            continue

        seq = message.get("seq")
        did = message.get("from")
        nonce = message.get("nonce")

        if not isinstance(seq, int):
            issues.append(f"{prefix}: invalid seq")
        elif seq in seen_sequences:
            issues.append(f"{prefix}: duplicate seq {seq}")
        else:
            seen_sequences.add(seq)

        if not isinstance(did, str) or not did.startswith("did:key:"):
            issues.append(f"{prefix}: invalid DID")
            continue

        if not isinstance(nonce, int):
            issues.append(f"{prefix}: invalid nonce")
            continue

        did_nonces = seen_nonce_by_did.setdefault(did, set())

        if nonce in did_nonces:
            issues.append(
                f"{prefix}: replayed nonce {nonce} for {did}"
            )
        else:
            did_nonces.add(nonce)

        previous_nonce = last_nonce_by_did.get(did)

        if previous_nonce is not None and nonce <= previous_nonce:
            issues.append(
                f"{prefix}: nonce not strictly increasing "
                f"for {did}: {nonce} <= {previous_nonce}"
            )

        last_nonce_by_did[did] = nonce

    return issues


def main() -> None:
    print("Technocore Message Audit Tool")
    print("------------------------------")

    messages = [
        {
            "seq": 1,
            "from": "did:key:example-agent",
            "nonce": 100,
            "text": "first message",
        },
        {
            "seq": 2,
            "from": "did:key:example-agent",
            "nonce": 101,
            "text": "second message",
        },
    ]

    issues = audit_messages(messages)

    print(f"Messages audited: {len(messages)}")
    print(f"Issues found: {len(issues)}")

    if issues:
        print("Audit result: FAIL")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("Audit result: PASS")


if __name__ == "__main__":
    main()