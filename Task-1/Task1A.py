#This program requests a connection to the receiver,
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
def receive(toSend=None):
    """Handles receiving of messages."""
    print("A waiting for response... \n")
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

def start():
    private_key = rsa.generate_private_key(public_exponent=65537,key_size=1024, backend=default_backend())
    public_key = private_key.public_key()
    pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)
    pem=pem.decode()
    client_socket.send(bytes(pem, "utf8"))
    msg=receive()
    msg=msg.decode("utf8")
    #print(msg)
    b64data = '\n'.join(msg.splitlines()[1:-1])
    #print("thing is"+b64data)
    derdata=base64.b64decode(b64data)
    Bkey = load_der_public_key(derdata, backend=default_backend())
    print("A got Bs public key, will now use key to encrypt a message to B containing A's chosen nonce and identifier\n\n")
    a=input("Press Enter to send encrypted message with nonce and identifier")
    nonce=str(random.randrange(100000000000)) #this would usually be a bigger range
    identifier=str(random.randrange(100000000000))#this too
    toSend=bytes(nonce+":"+identifier,"utf8")
    print("Sending random nonce of %s and identifier of %s\n\n" % (nonce ,identifier) )
    cipherText=Bkey.encrypt(toSend,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None )) 
    client_socket.send(cipherText)

    getNons=receive()
    cipherText = private_key.decrypt(getNons,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),     label=None   ) )
    text=cipherText.decode()
    ind=text.index(":")
    Anon=text[0:ind]
    Bnon=text[ind+1:]
    if(Anon==nonce):
        print("Communication with B confirmed by receipt of A's nonce of: %s " %Anon)
    else:
        print("wrong nonce, terminate")
        return
    a=input("Now sending back B's nonce to ensure B that this is A\nPress Enter to send nonce: ")
    toSend=bytes(Bnon,"utf8")
    cipherText=Bkey.encrypt(toSend,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None )) 
    client_socket.send(cipherText)
    print("Now waiting for acknowledgement")
    ack=receive()
    if(ack.decode()=="ack"):
        print("Acknowledgement of nonce received ")
    else:
        print("wrong nonce, terminate")
        return
    a=input("Press Enter to generate and send secret key to B")
    sKey=Fernet.generate_key() #key for symmetric encryption
    print("The secret key is ")
    print(sKey.decode())
    f=Fernet(sKey) #f is an object that can encrypt and decrypt using the sKey
    innerSecret= Bkey.encrypt(sKey,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None ))
    client_socket.send(innerSecret)
    ack=receive()
    if(ack.decode()=="ack"):
        a=input("Acknowledgement of Secret key received.\nPress Enter to send signed key: ")
    else:
        print("Something happened")
        return
    print(innerSecret)
    signedSecret=private_key.sign(innerSecret,padding.PSS(mgf=padding.MGF1(algorithm=hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
    client_socket.send(signedSecret)
    ack=receive()
    if(ack.decode()=="ack"):
        a=input("Acknowledgement of secret key validation. \nPress Enter to exit: ")
    else:
        print("Something happened")
        return
    

    
HOST = "127.0.0.1"
PORT = 33000  # Default value.
BUFSIZ = 2048
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
i=input("Press enter to start communication ")
while True:
    try:
        client_socket.connect(ADDR)
        break
    except:
        pass

receive_thread = Thread(target=start)
receive_thread.start()
