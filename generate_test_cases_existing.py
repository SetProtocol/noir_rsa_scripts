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
    # (pubkey, privkey) = rsa.newkeys(1024)

    pubkey_e = 65537
    pubkey_n = 139598662710773664102642358570432516379596390497506043389128172540767324028772581520964403424474152246741976321281477033343057554584876768940078817009169280329895177148247654267175764915213957680957788218951292280263042701588196474802827904145218909739601271419613242891314447770423863871028258561712245284281

    pubkey_e_limbs = breakdown_to_limbs(pubkey_e)
    pubkey_n_limbs = breakdown_to_limbs(pubkey_n)

    # 1 - Generate message
    # message = "Hello World! This is Noir-RSA" # fake.text()
    message_bytes = bytes(bytearray([
      102, 114, 111, 109, 58, 97, 108, 105, 99, 101, 64, 122, 107, 101, 109, 97, 105, 108, 46, 99, 111, 109, 13, 10, 100, 107, 105, 109, 45, 115, 105, 103, 110, 97, 116, 117, 114, 101, 58, 118, 61, 49, 59, 32, 97, 61, 114, 115, 97, 45, 115, 104, 97, 50, 53, 54, 59, 32, 100, 61, 122, 107, 101, 109, 97, 105, 108, 46, 99, 111, 109, 59, 32, 115, 61, 100, 101, 102, 97, 117, 108, 116, 59, 32, 99, 61, 114, 101, 108, 97, 120, 101, 100, 47, 114, 101, 108, 97, 120, 101, 100, 59, 32, 104, 61, 102, 114, 111, 109, 59, 32, 116, 61, 49, 54, 57, 50, 53, 55, 55, 50, 51, 49, 59, 32, 98, 104, 61, 80, 72, 73, 114, 87, 101, 121, 90, 114, 71, 43, 68, 53, 116, 106, 56, 81, 97, 115, 83, 67, 111, 115, 116, 53, 65, 108, 104, 48, 104, 115, 48, 100, 90, 90, 103, 111, 80, 108, 99, 72, 74, 119, 61, 59, 32, 98, 61, 59
    ]))

    # 2 - Generate Hashed and Padded Message
    message_hash_bytes = rsa.compute_hash(message_bytes, 'SHA-256')
    message_hash_int = int.from_bytes(message_hash_bytes, 'big')
    message_hash_limbs = breakdown_to_limbs(message_hash_int)

    # 3- Generated Signature
    # signature_bytes = rsa.sign_hash(message_hash_bytes, privkey, 'SHA-256')
    signature_int = 127626553341335668354120020103133913651773246041262838969858601241458000925973213432623507949465532653326396153790691491129967442028971099085045413476791263956364822503108010926785687893737536831768323602449197160854222146013004152835611064290098157672225578348832162259732062436665772664139295298741587637051
    signature_limbs = breakdown_to_limbs(signature_int)

    # Print inputs to Verify Function
    # print("Original Message Text", message)
    print("message hash limbs: ", message_hash_limbs)
    print("signature limbs: ", signature_limbs)
    print("public key e limbs: ", pubkey_e_limbs)
    print("public key n: limbs", pubkey_n_limbs)
    print("-----------Debugging Lines Below ---------")

    # ----- Below is print for debugging purposes where we print all lines in Little Endean
    # The things that we want to print are 1) Padded Message Hash, 2) Message Hash

    padded_sha256_hash = (signature_int ** pubkey_e) % pubkey_n
    # print("padded 256 num: ", hex(padded_sha256_hash))

    # Print Message Padded Message Hash
    padded_sha256_hash_bytes = padded_sha256_hash.to_bytes(259, 'big') # 8 * 70 = 560 (MAX_BYTES = 70)
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
