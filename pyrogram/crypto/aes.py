import tgcrypto

def ige256_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    return tgcrypto.ige256_encrypt(data, key, iv)


def ige256_decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    return tgcrypto.ige256_decrypt(data, key, iv)


def ctr256_encrypt(data: bytes, key: bytes, iv: bytearray, state: bytearray = None) -> bytes:
    return tgcrypto.ctr256_encrypt(data, key, iv, state or bytearray(1))


def ctr256_decrypt(data: bytes, key: bytes, iv: bytearray, state: bytearray = None) -> bytes:
    return tgcrypto.ctr256_decrypt(data, key, iv, state or bytearray(1))


def xor(a: bytes, b: bytes) -> bytes:
    return int.to_bytes(
        int.from_bytes(a, "big") ^ int.from_bytes(b, "big"),
        len(a),
        "big",
    )