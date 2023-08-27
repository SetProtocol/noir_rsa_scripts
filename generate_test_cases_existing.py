import random
import rsa

from faker import Faker

fake = Faker()

NUM_EXAMPLES = 1

BITS_PER_LIMB =  56
NUM_LIMBS = 74
BYTES_PER_LIMB = 7 # Number of bytes per limb (BITS_PER_LIMB / 8).
MAX_BITS = 4144 # Maximum number of bits (BITS_PER_LIMB * NUM_LIMBS).
MAX_BYTES = 518 # Maximum number of bytes (NUM_LIMBS * BYTES_PER_LIMB).


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
    pubkey_n = 22678151869562939359899136428859256198402569240680475393086048829021713182010490409724483359945551283969506235489826762257419985891230334120904178414351809046671461143996599803281758436654811035615578092428632166371331342907633917876752170113620966009358291594609542956251740141784694619901495773614035042135465203364073740861194611021551592336450807473519143746970021740067888325723330796836146546417386918505126721680365151889317110944800331756379997471380657912089911948147086686452887197011845657708078311037666769039161141500897109834073427400667740315220146696437513966171590587213846521825862509466370365529359

    pubkey_e_limbs = breakdown_to_limbs(pubkey_e)
    pubkey_n_limbs = breakdown_to_limbs(pubkey_n)

    # 1 - Generate message
    # message = "Hello World! This is Noir-RSA" # fake.text()
    message_bytes = bytes(bytearray([
      116, 111, 58, 101, 109, 97, 105, 108, 119, 97, 108, 108, 101, 116, 46, 114, 101, 108, 97, 121, 101, 114, 64, 103, 109, 97, 105, 108, 46, 99, 111, 109, 13, 10, 115, 117, 98, 106, 101, 99, 116, 58, 69, 109, 97, 105, 108, 32, 87, 97, 108, 108, 101, 116, 32, 77, 97, 110, 105, 112, 117, 108, 97, 116, 105, 111, 110, 32, 73, 68, 32, 49, 13, 10, 109, 101, 115, 115, 97, 103, 101, 45, 105, 100, 58, 60, 67, 65, 74, 55, 89, 54, 106, 100, 119, 71, 97, 71, 80, 77, 109, 48, 87, 98, 52, 116, 116, 95, 65, 122, 107, 114, 102, 71, 114, 67, 61, 71, 50, 88, 61, 90, 52, 105, 80, 83, 116, 115, 61, 77, 80, 87, 114, 70, 85, 43, 81, 64, 109, 97, 105, 108, 46, 103, 109, 97, 105, 108, 46, 99, 111, 109, 62, 13, 10, 100, 97, 116, 101, 58, 77, 111, 110, 44, 32, 49, 55, 32, 65, 112, 114, 32, 50, 48, 50, 51, 32, 49, 56, 58, 50, 56, 58, 51, 54, 32, 43, 48, 57, 48, 48, 13, 10, 102, 114, 111, 109, 58, 115, 117, 101, 103, 97, 109, 105, 115, 111, 114, 97, 64, 103, 109, 97, 105, 108, 46, 99, 111, 109, 13, 10, 109, 105, 109, 101, 45, 118, 101, 114, 115, 105, 111, 110, 58, 49, 46, 48, 13, 10, 100, 107, 105, 109, 45, 115, 105, 103, 110, 97, 116, 117, 114, 101, 58, 118, 61, 49, 59, 32, 97, 61, 114, 115, 97, 45, 115, 104, 97, 50, 53, 54, 59, 32, 99, 61, 114, 101, 108, 97, 120, 101, 100, 47, 114, 101, 108, 97, 120, 101, 100, 59, 32, 100, 61, 103, 109, 97, 105, 108, 46, 99, 111, 109, 59, 32, 115, 61, 50, 48, 50, 50, 49, 50, 48, 56, 59, 32, 116, 61, 49, 54, 56, 49, 55, 50, 51, 55, 50, 55, 59, 32, 120, 61, 49, 54, 56, 52, 51, 49, 53, 55, 50, 55, 59, 32, 104, 61, 116, 111, 58, 115, 117, 98, 106, 101, 99, 116, 58, 109, 101, 115, 115, 97, 103, 101, 45, 105, 100, 58, 100, 97, 116, 101, 58, 102, 114, 111, 109, 58, 109, 105, 109, 101, 45, 118, 101, 114, 115, 105, 111, 110, 58, 102, 114, 111, 109, 58, 116, 111, 58, 99, 99, 58, 115, 117, 98, 106, 101, 99, 116, 32, 58, 100, 97, 116, 101, 58, 109, 101, 115, 115, 97, 103, 101, 45, 105, 100, 58, 114, 101, 112, 108, 121, 45, 116, 111, 59, 32, 98, 104, 61, 71, 120, 77, 108, 103, 119, 76, 105, 121, 112, 110, 86, 114, 69, 50, 67, 48, 83, 102, 52, 121, 122, 104, 99, 87, 84, 107, 65, 104, 83, 90, 53, 43, 87, 69, 82, 104, 75, 104, 88, 116, 108, 85, 61, 59, 32, 98, 61
    ]))

    # 2 - Generate Hashed and Padded Message
    message_hash_bytes = rsa.compute_hash(message_bytes, 'SHA-256')
    message_hash_int = int.from_bytes(message_hash_bytes, 'big')
    message_hash_limbs = breakdown_to_limbs(message_hash_int)

    # 3- Generated Signature
    # signature_bytes = rsa.sign_hash(message_hash_bytes, privkey, 'SHA-256')
    signature_int = 17645329850780954558574263278280755989139741933649874804905625904240788824779409537959003320842059137284621038912229081442542464311522534829338409537194778363345092772799781241784786215026178636444506663186386760319012235997754130358203809144831898380755427701018795084834394681413645045298819506595731418953925458024518837669603047309107713137889378738241430225558301505228357626611135188115571560037658285631825458173889700273470139647938189092783605181725186234089858387244396061743822505837723743339402552894027494289555361742258965096932454109072087074479467374138912599571532331045089082422251527977276501409814
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
