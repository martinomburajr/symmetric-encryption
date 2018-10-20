#This program accepts a TCP connection from Task1Sender and
#Then continues the process of exchanging keys
#The code for the sockets and threading was adapted from
#https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import base64
import random
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import load_der_public_key
def accept_incoming_connections():
    client, client_address = SERVER.accept()
    print("Connection request from : %s:%s." % client_address)
    print("Connection established with: %s:%s." % client_address)
    """Sets up handling for incoming clients."""
    newConnection=Thread(target=handle_client, args=(client,client_address,))
    newConnection.start()
    newConnection.join()


def handle_client(client,client_address):  # Takes client socket as argument.
    """Handles a single client connection."""
    private_key = rsa.generate_private_key(public_exponent=65537,key_size=1024, backend=default_backend())
    public_key = private_key.public_key()
    pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)
    pem=pem.decode()
    client.send(bytes(pem, "utf8"))
    print("B has sent public key to A ")
    while True:
        try:
            msg = client.recv(BUFSIZ)
            break
        except:
            pass
    print("Got As public key")
    msg=msg.decode("utf8")
    b64data = '\n'.join(msg.splitlines()[1:-1])
    derdata=base64.b64decode(b64data)
    Akey = load_der_public_key(derdata, backend=default_backend())
    
    while True:
        try:
            msg = client.recv(BUFSIZ)
            break
        except:
            print("here")
    print("Got encrypted message with nonce from A\n")
    cipherText=msg
    plainText = private_key.decrypt(cipherText,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),     label=None   ) )
    print(plainText)
    text=plainText.decode()
    ind=text.index(":")
    Anon=text[0:ind]
    Aid=text[ind+1:]
    print(Anon,"and then",Aid)
    Bnon=str(random.randrange(100000000000))
    sendNons=bytes(Anon+":"+Bnon, "utf8")
    cipherText=Akey.encrypt(sendNons,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None )) 
    print(cipherText)
    client.send(cipherText)
    print("Returned A's nonce encrypted along with a new nonce to tell A that tis is indeed B")
    print("Now waiting for return of B's nonce to confirm communication is with A ")
    while True:
        try:
            msg = client.recv(BUFSIZ)
            break
        except:
            print("waiting")
    cipherText=msg
    plainText = private_key.decrypt(cipherText,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),     label=None   ) )
    print(plainText)
    text=plainText.decode()
    if(text==Bnon):
        print("B has received its nonce, so communication with A is confirmed")
        print("Sending acknowledgement")
        client.send(bytes("ack","utf8"))
    else:
        print("B received incorrect nonce, communication terminated")
    print("Now waiting for receipt of the encrypted secret key for further communication ")
    while True:
        try:
            secKey = client.recv(BUFSIZ)
            break
        except:
            print("waiting")
    print("Received secret key")
    print(msg)
    secretKey=private_key.decrypt(secKey,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),   label=None) )
    print("Received secret key from A")
    print(secretKey)
    client.send(bytes("ack","utf8"))
    print("Now waiting for message signed with As private key")
    while True:
        try:
            signedKey = client.recv(BUFSIZ)
            break
        except:
            print("waiting")
    print("Received signed secret key from A. Will now verify using As public key")
    try:
        outerSecret=Akey.verify(signedKey,secKey,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
    except:
        print("Failed to verify signature, communication terminated")
        return 0
    print(outerSecret)
    f=Fernet(secretKey)
    print("received secsret key of %s " %secretKey.decode())
    client.send(bytes("ack","utf8"))
    a=input("Press Enter to exit: ")
    return 0
    
def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)
    
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 2048
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
