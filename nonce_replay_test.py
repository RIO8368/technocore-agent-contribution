"""
Reproducible nonce replay-protection test.

A nonce is accepted only when it is strictly greater
than the previously accepted nonce.
"""


def accept_nonce(last_nonce, new_nonce):
    return new_nonce > last_nonce


def run_tests():
    last_nonce = 100

    tests = [
        (100, False, "same nonce must be rejected"),
        (99, False, "older nonce must be rejected"),
        (101, True, "newer nonce must be accepted"),
        (101, False, "replayed nonce must be rejected"),
        (102, True, "next nonce must be accepted"),
    ]

    passed = 0

    for new_nonce, expected, description in tests:
        result = accept_nonce(last_nonce, new_nonce)

        if result == expected:
            print(f"PASS: {description}")
            passed += 1

            # Update state only when the nonce is accepted.
            if result:
                last_nonce = new_nonce
        else:
            print(f"FAIL: {description}")

    print()
    print(f"{passed}/{len(tests)} tests passed")

    if passed != len(tests):
        raise SystemExit(1)


if __name__ == "__main__":
    run_tests()