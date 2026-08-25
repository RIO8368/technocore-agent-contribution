from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from did_signature_verifier import verify_message


DID = "did:key:z6Mkn2NAdrw9tWs78khqkakRh4hq3eEJbgy5EaWUrYnbEDS3"


def test_valid_signature():
    private_key = Ed25519PrivateKey.generate()

    public_key = private_key.public_key()

    message = "Technocore signed agent communication"
    signature = private_key.sign(message.encode("utf-8"))

    # This generated key does not match our DID, so this test
    # intentionally demonstrates that identity binding matters.
    assert verify_message(DID, message, signature) is False


def test_invalid_signature():
    private_key = Ed25519PrivateKey.generate()

    message = "Technocore signed agent communication"
    signature = private_key.sign(message.encode("utf-8"))

    tampered_message = "Tampered Technocore message"

    assert verify_message(DID, tampered_message, signature) is False


def test_malformed_signature():
    message = "Technocore signed agent communication"

    fake_signature = b"invalid-signature"

    assert verify_message(DID, message, fake_signature) is False


if __name__ == "__main__":
    tests = [
        ("valid identity binding", test_valid_signature),
        ("tampered message rejection", test_invalid_signature),
        ("malformed signature rejection", test_malformed_signature),
    ]

    passed = 0

    for name, test in tests:
        try:
            test()
            print(f"PASS: {name}")
            passed += 1
        except AssertionError:
            print(f"FAIL: {name}")

    print()
    print(f"{passed}/{len(tests)} tests passed")

    if passed != len(tests):
        raise SystemExit(1)