import base64
import hashlib


def decode_did_key(did):
    prefix = "did:key:z"
    if not did.startswith(prefix):
        raise ValueError("Unsupported DID format")

    encoded = did[len(prefix):]

    # Base58btc decoder
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    number = 0
    for char in encoded:
        number = number * 58 + alphabet.index(char)

    raw = number.to_bytes((number.bit_length() + 7) // 8, "big")

    # Preserve leading zero bytes represented by "1"
    leading_ones = len(encoded) - len(encoded.lstrip("1"))
    raw = b"\x00" * leading_ones + raw

    # did:key Ed25519 multicodec prefix = 0xed01
    if not raw.startswith(b"\xed\x01"):
        raise ValueError("DID does not contain an Ed25519 public key")

    return raw[2:]


def verify_message(did, message, signature):
    """
    Verify an Ed25519 signature associated with a did:key.

    Returns True when the signature is valid.
    """
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import (
            Ed25519PublicKey,
        )

        public_key_bytes = decode_did_key(did)

        if len(public_key_bytes) != 32:
            return False

        public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
        public_key.verify(signature, message.encode("utf-8"))

        return True

    except Exception:
        return False


def fingerprint(did):
    """
    Return a short deterministic fingerprint of the public DID.
    """
    public_key = decode_did_key(did)
    return hashlib.sha256(public_key).hexdigest()[:16]


if __name__ == "__main__":
    DID = "did:key:z6Mkn2NAdrw9tWs78khqkakRh4hq3eEJbgy5EaWUrYnbEDS3"

    message = "Technocore signed agent communication"

    print("DID signature verifier")
    print("----------------------")
    print("DID:", DID)
    print("Public-key fingerprint:", fingerprint(DID))
    print("Message:", message)
    print()
    print("Verifier ready.")