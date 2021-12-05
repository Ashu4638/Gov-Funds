import binascii
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5


def sign_transaction(self):
   private_key = self.sender._private_key
   signer = PKCS1_v1_5.new(private_key)
   h = SHA.new(str(self.to_dict()).encode('utf8'))
   return binascii.hexlify(signer.sign(h)).decode('ascii')