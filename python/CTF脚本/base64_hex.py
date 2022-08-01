import binascii
import base64
print(base64.b64encode(base64.b64encode(binascii.b2a_hex(b'index.php'))))