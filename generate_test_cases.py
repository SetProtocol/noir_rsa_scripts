import random
import rsa

from faker import Faker

fake = Faker()

NUM_EXAMPLES = 10

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

# generate a random 512 bit number
max_56_bit_num = 2**56 - 1
a = max_56_bit_num + 1
b = max_56_bit_num + 1
sum = a + b
print("a: ", a)
print("b: ", b)
print("sum: ", sum)

# convert to limbs
a_limbs = breakdown_to_limbs(a)
b_limbs = breakdown_to_limbs(b)
sum_limbs = breakdown_to_limbs(sum)

# print the limbs
print("a_limbs: ", a_limbs)
print("b_limbs: ", b_limbs)
print("sum_limbs: ", sum_limbs)

def __main__():
  for i in range(NUM_EXAMPLES):
    print("Example: ", i)
    (pubkey, privkey) = rsa.newkeys(512)
    pubkey_e_limbs = breakdown_to_limbs(pubkey.e)
    pubkey_n_limbs = breakdown_to_limbs(pubkey.n)

    message_bytes = fake.text().encode('utf-8')
    signature_bytes = rsa.sign(message_bytes, privkey, 'SHA-256')
    signature_int = int.from_bytes(signature_bytes, 'little')
    signature_limbs = breakdown_to_limbs(signature_int)

    message_int = int.from_bytes(message_bytes, 'little')
    message_limbs = breakdown_to_limbs(message_int)


    print("message limbs: ", message_limbs)
    print("signature limbs: ", signature_limbs)
    print("public key e limbs: ", pubkey_e_limbs)
    print("public key n: limbs", pubkey_n_limbs)
    print("--------------------")

__main__()
