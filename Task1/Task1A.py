#Daniel Collins CLLDAN008
#18 October 2018
#This program requests a connection to Task1B,
#And then begins to exchange details
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import os
import base64
import random
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms
from cryptography.hazmat.primitives.asymmetric import rsa, padding, utils
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_der_public_key
#This function is used to receive messages 
def receive(toSend=None):
    """Handles receiving of messages."""
    msg=None
    while True:
        try:
            msg=client_socket.recv(BUFSIZ)
            return msg  
        except:
            print("failed")
            if(toSend!=None):
                client_socket.send(toSend)
            pass

def keySwap():
    #create a private key
    private_key = rsa.generate_private_key(public_exponent=65537,key_size=1024, backend=default_backend())
    #create a public key associated with the private key
    public_key = private_key.public_key()
    pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)
    pem=pem.decode()
    a=input("Press Enter to send A's public key to B: ")
    #send the public key to B
    client_socket.send(bytes(pem, "utf8"))
    #receive Bs public key
    msg=receive()
    msg=msg.decode("utf8")
    b64data = '\n'.join(msg.splitlines()[1:-1])
    #this is done because the library has some errors with loading and saving keys from strings
    derdata=base64.b64decode(b64data)
    #save Bs public key as an object
    Bkey = load_der_public_key(derdata, backend=default_backend())
    print("A received Bs public key, will now use key to encrypt a message to B containing A's chosen nonce and identifier\n")
    nonceSwap(private_key, public_key, Bkey)
    
def nonceSwap(private_key, public_key, Bkey):
    a=input("Press Enter to send encrypted message with nonce and identifier")
    #choose random nonce and identifier
    nonce=str(random.randrange(100000000000)) #this would usually be a bigger range
    identifier=str(random.randrange(100000000000))#this too
    toSend=bytes(nonce+":"+identifier,"utf8")
    print("Sending random nonce of %s and identifier of %s\n" % (nonce ,identifier) )
    cipherText=Bkey.encrypt(toSend,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None )) 
    #send this to B encrypted with Bs public key
    client_socket.send(cipherText)
    #get back As nonce along with Bs chosen nonce
    getNons=receive()
    cipherText = private_key.decrypt(getNons,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),     label=None   ) )
    text=cipherText.decode()
    ind=text.index(":")
    Anon=text[0:ind]
    Bnon=text[ind+1:]
    #check if B sent back the correct nonce
    if(Anon==nonce):
        print("Communication with B confirmed by receipt of A's nonce of: %s \n" %Anon)
    else:
        print("wrong nonce, terminate")
        return
    a=input("Now sending back B's nonce to ensure B that this is A\nPress Enter to send nonce: ")
    #send back Bs nonce to ensure B that this is A
    toSend=bytes(Bnon,"utf8")
    cipherText=Bkey.encrypt(toSend,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None )) 
    client_socket.send(cipherText)
    print("Now waiting for acknowledgement\n")
    ack=receive()
    if(ack.decode()=="ack"):
        print("Acknowledgement of nonce received \n")
    else:
        print("wrong nonce, terminate")
        return
    secKeySwap(Bkey, public_key, private_key)
    
def secKeySwap(Bkey, public_key, private_key):
    a=input("Press Enter to generate and send secret key to B")
    #generate a random secret key
    sKey=Fernet.generate_key() #key for symmetric encryption
    print("The secret key is ")
    print(sKey.decode())
    f=Fernet(sKey) #f is an object that can encrypt and decrypt using the sKey
    innerSecret= Bkey.encrypt(sKey,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None ))
    #send the secret key encrypted with Bs public key to B
    client_socket.send(innerSecret)
    ack=receive()
    #wait for acknowledgement of the secret key
    if(ack.decode()=="ack"):
        a=input("Acknowledgement of Secret key received.\nPress Enter to send signed key: ")
    else:
        print("Something happened")
        return
    #sign the encrypted secret key with As private key and send this to B
    signedSecret=private_key.sign(innerSecret,padding.PSS(mgf=padding.MGF1(algorithm=hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
    client_socket.send(signedSecret)
    ack=receive()
    #wait for acknowledgement of receipt and verification of the signed secret key
    if(ack.decode()=="ack"):
        a=input("Acknowledgement of secret key validation. \nKey exchange complete\nPress Enter to exit: ")
    else:
        print("Something happened")
        return
    #key swapping complete. This secret key can now be used to symmetrically encrypt
    #messages for the remainder of communication


HOST = "127.0.0.1"
PORT = 33000  # Default value.
BUFSIZ = 2048
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
i=input("Press enter to start communication with B")
while True:
    try:
        client_socket.connect(ADDR)
        break
    except:
        pass

receive_thread = Thread(target=keySwap)
receive_thread.start()
