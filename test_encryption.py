from utilities import encryption
def test_getKey():
    password = "HELLO"
    salt = b'Uz\x8b\xfbJ\x86\xfa\xa5\x8d\x98\x14l\x8f\x02\x8b\xbe'
    key = encryption.getKey(password,salt)
    assert key == b'bjLrZJ3_PmxK-UjA1M8h-egstYILmJHeebMHRNDYk4g='
def test_encryptdecrypt():
    key = b'bjLrZJ3_PmxK-UjA1M8h-egstYILmJHeebMHRNDYk4g='
    string = "HeLLo WoRlD"
    encrypted = encryption.encrypt(key,string)
    decrypted = encryption.decrypt(key, encrypted)
    assert "HeLLo WoRlD" == decrypted 