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
    message_bytes = message.encode()
    print(message_bytes)
    message_hash_bytes = rsa.compute_hash(message_bytes, 'SHA-256')
    print("message hash bytes", message_hash_bytes)
    message_hash_in_bytes_of_size_70 = [int(el) for el in bytearray(message_hash_bytes)]
    message_hash_in_bytes_of_size_70.reverse()
    while len(message_hash_in_bytes_of_size_70) < 70:
      # Add elements to the array
      message_hash_in_bytes_of_size_70.append(0)
    print(message_hash_in_bytes_of_size_70)

    signature_bytes = rsa.sign_hash(message_hash_bytes, privkey, 'SHA-256')
    print("signature bytes: ", signature_bytes)
    signature_int = int.from_bytes(signature_bytes, 'big')
    signature_limbs = breakdown_to_limbs(signature_int)

    message_hash_int = int.from_bytes(message_hash_bytes, 'big')
    message_hash_limbs = breakdown_to_limbs(message_hash_int)

    padded_sha256_hash = (signature_int ** pubkey.e) % pubkey.n
    print("padded 256 num: ", hex(padded_sha256_hash))


    padded_sha256_hash_bytes = padded_sha256_hash.to_bytes(70, 'big') # 8 * 70 = 560 (MAX_BYTES = 70)
    padded_sha256_hash_byte_array = bytearray(padded_sha256_hash_bytes)
    padded_sha256_hash_byte_array.reverse()
    print("padded 256 hash in bytes in little endian: ", [int(el) for el in padded_sha256_hash_byte_array])

    # print("message hash limbs: ", message_hash_limbs)
    # print("signature limbs: ", signature_limbs)
    # print("public key e limbs: ", pubkey_e_limbs)
    # print("public key n: limbs", pubkey_n_limbs)
    print("--------------------")

__main__()
