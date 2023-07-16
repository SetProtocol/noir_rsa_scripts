import random
import rsa

from faker import Faker

fake = Faker()

NUM_EXAMPLES = 1

BITS_PER_LIMB =  56
NUM_LIMBS = 10
BYTES_PER_LIMB = 7
MAX_BITS = 560
MAX_BYTES = 70

def breakdown_to_limbs(num):
  # Breakwdown the number into limbs
  # Limbs are 56 bits long
  # The limbs are in a little endian format
  # The limbs are stored in a list
  # The list is in a little endian format

  # convert the number to a binary string
  num_bin = bin(num)[2:]

  # pad the binary string with zeros
  num_bin = num_bin.zfill(MAX_BITS)

  # convert the binary string to a list of bytes
  num_bytes = []
  for i in range(0, MAX_BITS, 8):
      num_bytes.append(num_bin[i:i+8])

  # convert the list of bytes to a list of limbs
  num_limbs = []
  for i in range(0, MAX_BYTES, BYTES_PER_LIMB):
      num_limbs.append(num_bytes[i:i+BYTES_PER_LIMB])

  # convert the list of limbs to a list of integers
  num_limbs = [int(''.join(limb), 2) for limb in num_limbs]

  # reverse the list of limbs
  num_limbs.reverse()
  return num_limbs

def __main__():
  for i in range(NUM_EXAMPLES):
    print("Example: ", i)
    (pubkey, privkey) = rsa.newkeys(512)
    pubkey_e_limbs = breakdown_to_limbs(pubkey.e)
    pubkey_n_limbs = breakdown_to_limbs(pubkey.n)

    message = fake.text()
    message_bytes = message.encode('utf-8')
    message_hash_bytes = rsa.compute_hash(message_bytes, 'SHA-256')
    signature_bytes = rsa.sign_hash(message_hash_bytes, privkey, 'SHA-256')
    signature_int = int.from_bytes(signature_bytes, 'little')
    signature_limbs = breakdown_to_limbs(signature_int)

    message_hash_int = int.from_bytes(message_hash_bytes, 'little')
    message_hash_limbs = breakdown_to_limbs(message_hash_int)

    # bigint exponentiation of signature_int by pubkey.e
    padded_256_bytes = rsa.pkcs1v15._pad_for_signing(message_hash_bytes, 560)

    # padded_sha256_hash = signature_int ** pubkey.e % pubkey.n
    print("padded 256 hash: ", padded_sha256_hash)

    padded_sha256_hash_bytes = padded_sha256_hash.to_bytes(560, 'little') # 8 * 70 = 560 (MAX_BYTES = 70)

    print("padded 256 hash in bytes: ", padded_sha256_hash_bytes)
    print("message hash bytes", message_hash_bytes)

    # print("message hash limbs: ", message_hash_limbs)
    # print("signature limbs: ", signature_limbs)
    # print("public key e limbs: ", pubkey_e_limbs)
    # print("public key n: limbs", pubkey_n_limbs)
    print("--------------------")

__main__()
