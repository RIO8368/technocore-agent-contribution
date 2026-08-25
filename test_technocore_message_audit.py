from technocore_message_audit import audit_messages


DID = "did:key:test-agent"


def run_test(name, messages, expected_count):
    issues = audit_messages(messages)

    if len(issues) == expected_count:
        print(f"PASS: {name}")
    else:
        print(
            f"FAIL: {name} "
            f"(expected {expected_count}, got {len(issues)})"
        )
        for issue in issues:
            print(f"  - {issue}")

    return len(issues) == expected_count


def main():
    tests = [
        (
            "valid increasing nonces",
            [
                {"seq": 1, "from": DID, "nonce": 100},
                {"seq": 2, "from": DID, "nonce": 101},
                {"seq": 3, "from": DID, "nonce": 102},
            ],
            0,
        ),
        (
            "replayed nonce",
            [
                {"seq": 1, "from": DID, "nonce": 100},
                {"seq": 2, "from": DID, "nonce": 100},
            ],
            2,
        ),
        (
            "older nonce",
            [
                {"seq": 1, "from": DID, "nonce": 200},
                {"seq": 2, "from": DID, "nonce": 199},
            ],
            1,
        ),
        (
            "duplicate sequence",
            [
                {"seq": 10, "from": DID, "nonce": 300},
                {"seq": 10, "from": DID, "nonce": 301},
            ],
            1,
        ),
        (
            "invalid DID",
            [
                {"seq": 1, "from": "not-a-did", "nonce": 400},
            ],
            1,
        ),
        (
            "invalid nonce",
            [
                {"seq": 1, "from": DID, "nonce": "400"},
            ],
            1,
        ),
    ]

    passed = 0

    for name, messages, expected_count in tests:
        if run_test(name, messages, expected_count):
            passed += 1

    print()
    print(f"{passed}/{len(tests)} tests passed")


if __name__ == "__main__":
    main()