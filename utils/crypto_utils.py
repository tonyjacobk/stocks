"""
Crypto utilities for MEGA encryption/decryption operations.
Refactored for better readability and Python 3 compatibility.
"""
import sys
import struct
import base64
import binascii
import random
from Crypto.Cipher import AES

# Python 3 compatibility helpers
if sys.version_info < (3,):
    def makebyte(x):
        return x

    def makestring(x):
        return x
else:
    import codecs

    def makebyte(x):
        return codecs.latin_1_encode(x)[0]

    def makestring(x):
        return codecs.latin_1_decode(x)[0]


def aes_cbc_encrypt(data, key):
    """Encrypt data using AES CBC mode with zero IV."""
    aes_cipher = AES.new(key, AES.MODE_CBC, makebyte('\0' * 16))
    return aes_cipher.encrypt(data)


def aes_cbc_decrypt(data, key):
    """Decrypt data using AES CBC mode with zero IV."""
    aes_cipher = AES.new(key, AES.MODE_CBC, makebyte('\0' * 16))
    return aes_cipher.decrypt(data)


def aes_cbc_encrypt_a32(data, key):
    """Encrypt a32 array data using AES CBC mode."""
    return str_to_a32(aes_cbc_encrypt(a32_to_str(data), a32_to_str(key)))


def aes_cbc_decrypt_a32(data, key):
    """Decrypt a32 array data using AES CBC mode."""
    return str_to_a32(aes_cbc_decrypt(a32_to_str(data), a32_to_str(key)))


def stringhash(str_data, aeskey):
    """Generate a hash from string data using AES encryption."""
    s32 = str_to_a32(str_data)
    h32 = [0, 0, 0, 0]
    for i in range(len(s32)):
        h32[i % 4] ^= s32[i]
    for _ in range(0x4000):
        h32 = aes_cbc_encrypt_a32(h32, aeskey)
    return a32_to_base64((h32[0], h32[2]))


def prepare_key(arr):
    """Prepare encryption key from array."""
    pkey = [0x93C467E3, 0x7DB0C7A4, 0xD1BE3F81, 0x0152CB56]
    for _ in range(0x10000):
        for j in range(0, len(arr), 4):
            key = [0, 0, 0, 0]
            for i in range(4):
                if i + j < len(arr):
                    key[i] = arr[i + j]
            pkey = aes_cbc_encrypt_a32(pkey, key)
    return pkey


def encrypt_key(a, key):
    """Encrypt key array using provided key."""
    return sum(
        (aes_cbc_encrypt_a32(a[i:i + 4], key) for i in range(0, len(a), 4)), ()
    )


def decrypt_key(a, key):
    """Decrypt key array using provided key."""
    return sum(
        (aes_cbc_decrypt_a32(a[i:i + 4], key) for i in range(0, len(a), 4)), ()
    )


def encrypt_attr(attr, key):
    """Encrypt attribute dictionary."""
    attr = makebyte('MEGA' + __import__('json').dumps(attr))
    if len(attr) % 16:
        attr += b'\0' * (16 - len(attr) % 16)
    return aes_cbc_encrypt(attr, a32_to_str(key))


def decrypt_attr(attr, key):
    """Decrypt attribute dictionary."""
    attr = aes_cbc_decrypt(attr, a32_to_str(key))
    attr = makestring(attr)
    attr = attr.rstrip('\0')
    return __import__('json').loads(attr[4:]) if attr[:6] == 'MEGA{"' else False


def a32_to_str(a):
    """Convert a32 array to byte string."""
    return struct.pack('>%dI' % len(a), *a)


def str_to_a32(b):
    """Convert byte string to a32 array."""
    if isinstance(b, str):
        b = makebyte(b)
    if len(b) % 4:
        # pad to multiple of 4
        b += b'\0' * (4 - len(b) % 4)
    return struct.unpack('>%dI' % (len(b) / 4), b)


def mpi_to_int(s):
    """
    Convert MPI (Multi-precision integer) to Python int.
    
    An MPI is encoded as bytes in big-endian order with a 2-byte header
    indicating the number of bits in the integer.
    """
    return int(binascii.hexlify(s[2:]), 16)


def extended_gcd(a, b):
    """Extended Euclidean Algorithm."""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modular_inverse(a, m):
    """Calculate modular multiplicative inverse."""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def base64_url_decode(data):
    """Decode URL-safe base64 encoded data."""
    data += '=='[(2 - len(data) * 3) % 4:]
    for search, replace in (('-', '+'), ('_', '/'), (',', '')):
        data = data.replace(search, replace)
    return base64.b64decode(data)


def base64_to_a32(s):
    """Convert base64 string to a32 array."""
    return str_to_a32(base64_url_decode(s))


def base64_url_encode(data):
    """Encode data as URL-safe base64."""
    data = base64.b64encode(data)
    data = makestring(data)
    for search, replace in (('+', '-'), ('/', '_'), ('=', '')):
        data = data.replace(search, replace)
    return data


def a32_to_base64(a):
    """Convert a32 array to base64 string."""
    return base64_url_encode(a32_to_str(a))


def get_chunks(size):
    """Generate chunk offsets and sizes for file processing."""
    p = 0
    s = 0x20000
    while p + s < size:
        yield (p, s)
        p += s
        if s < 0x100000:
            s += 0x20000
    yield (p, size - p)


def make_id(length):
    """Generate a random alphanumeric ID."""
    text = ''
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    for _ in range(length):
        text += random.choice(possible)
    return text
