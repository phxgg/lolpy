import base64
import zlib

class Decrypt:
    @staticmethod
    def decrypt(encrypted_text) -> str:
        '''
        Decrypts the encrypted text.
        '''
        compressed = base64.b64decode(encrypted_text)
        decompressed = zlib.decompress(compressed, zlib.MAX_WBITS | 16)
        return decompressed.decode('utf-8')