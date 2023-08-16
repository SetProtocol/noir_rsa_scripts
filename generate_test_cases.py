import random
import rsa

from faker import Faker

fake = Faker()

NUM_EXAMPLES = 1

BITS_PER_LIMB =  56
NUM_LIMBS = 37
BYTES_PER_LIMB = 7 # Number of bytes per limb (BITS_PER_LIMB / 8).
MAX_BITS = 2072 # Maximum number of bits (BITS_PER_LIMB * NUM_LIMBS).
MAX_BYTES = 259 # Maximum number of bytes (NUM_LIMBS * BYTES_PER_LIMB).


def breakdown_to_limbs(num):
  # Breakdown the number into limbs
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

    # Generate Public and Private Keys
    (pubkey, privkey) = rsa.newkeys(2048)

    pubkey_e_limbs = breakdown_to_limbs(pubkey.e)
    pubkey_n_limbs = breakdown_to_limbs(pubkey.n)

    # 1 - Generate message
    message = "Hello World! This is Noir-RSA" # fake.text()
    message_bytes = message.encode()

    # 2 - Generate Hashed and Padded Message
    message_hash_bytes = rsa.compute_hash(message_bytes, 'SHA-256')
    message_hash_int = int.from_bytes(message_hash_bytes, 'big')
    message_hash_limbs = breakdown_to_limbs(message_hash_int)

    # 3- Generated Signature
    signature_bytes = rsa.sign_hash(message_hash_bytes, privkey, 'SHA-256')
    signature_int = int.from_bytes(signature_bytes, 'big')
    signature_limbs = breakdown_to_limbs(signature_int)

    # Print inputs to Verify Function
    print("Original Message Text", message)
    print("message hash limbs: ", message_hash_limbs)
    print("signature limbs: ", signature_limbs)
    print("public key e limbs: ", pubkey_e_limbs)
    print("public key n: limbs", pubkey_n_limbs)
    print("-----------Debugging Lines Below ---------")

    # ----- Below is print for debugging purposes where we print all lines in Little Endean
    # The things that we want to print are 1) Padded Message Hash, 2) Message Hash

    padded_sha256_hash = (signature_int ** pubkey.e) % pubkey.n
    # print("padded 256 num: ", hex(padded_sha256_hash))

    # Print Message Padded Message Hash
    padded_sha256_hash_bytes = padded_sha256_hash.to_bytes(70, 'big') # 8 * 70 = 560 (MAX_BYTES = 70)
    padded_sha256_hash_byte_array = bytearray(padded_sha256_hash_bytes)
    padded_sha256_hash_byte_array.reverse()

    pow_mod_limbs = breakdown_to_limbs(padded_sha256_hash)
    print("pow mod limbs: ", pow_mod_limbs)
    print("padded 256 hash in bytes in little endian: ", [int(el) for el in padded_sha256_hash_byte_array])

    # Print Message Hash in Little Endean
    message_hash_in_bytes_of_size_70 = [int(el) for el in bytearray(message_hash_bytes)]
    message_hash_in_bytes_of_size_70.reverse()
    # while len(message_hash_in_bytes_of_size_70) < 70:
    #   # Add elements to the array
    #   message_hash_in_bytes_of_size_70.append(0)
    print("Message hash", message_hash_in_bytes_of_size_70)

    # integer little endian representation in Noir Code = [32, 4, 0, 5, 1, 2, 4, 3, 101, 1, 72, 134, 96, 9, 6, 13, 48, 49, 48]
    hex_big_endian = "3031300d060960864801650304020105000420"
    int_little_endian = [int(''.join([hex_big_endian[i], hex_big_endian[i+1]]), 16) for i in range(0, len(hex_big_endian), 2)]
    int_little_endian.reverse()
    print("Integer Little Endian", int_little_endian)

__main__()
