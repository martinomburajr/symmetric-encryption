#Daniel Collins CLLDAN008
#18 October 2018
#This program accepts a TCP connection from Task1A and
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
    print("Connection established with: %s:%s.\n" % client_address)
    """Sets up handling for incoming clients."""
    newConnection=Thread(target=key_exchange, args=(client,client_address,))
    newConnection.start()
    newConnection.join()


def key_exchange(client,client_address):  # Takes client socket as argument.
    """Handles a single client connection."""
    #B generates a private and public key
    private_key = rsa.generate_private_key(public_exponent=65537,key_size=1024, backend=default_backend())
    public_key = private_key.public_key()
    pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)
    pem=pem.decode()
    #B sends its public key to A
    client.send(bytes(pem, "utf8"))
    print("B has sent public key to A\n")
    #waiting to receive As public key
    while True:
        try:
            msg = client.recv(BUFSIZ)
            break
        except:
            pass
    print("B has received As public key")
    msg=msg.decode("utf8")
    b64data = '\n'.join(msg.splitlines()[1:-1])
    derdata=base64.b64decode(b64data)
    #saves As public key as a key object
    Akey = load_der_public_key(derdata, backend=default_backend())
    nonceExchange(private_key, public_key, Akey, client)

def nonceExchange(private_key, public_key, Akey, client):
    #waiting for A to send a nonce and identifier
    while True:
        try:
            msg = client.recv(BUFSIZ)
            break
        except:
            print("here")
    print("Got encrypted message with nonce from A\n")
    cipherText=msg
    #decrypts message using private key to read nonce and identifier
    plainText = private_key.decrypt(cipherText,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),     label=None   ) )
    text=plainText.decode()
    ind=text.index(":")
    Anon=text[0:ind]
    Aid=text[ind+1:]
    print("Received As nonce: ",Anon,"and identifier: ",Aid,"\n")
    Bnon=str(random.randrange(100000000000))
    #B creates a random nonce and concatenates this with As nonce and sends this back to A
    sendNons=bytes(Anon+":"+Bnon, "utf8")
    cipherText=Akey.encrypt(sendNons,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None )) 
    client.send(cipherText)
    print("Returned A's nonce encrypted along with a new nonce of %s to tell A that this is indeed B\n" %Bnon)
    print("Now waiting for return of B's nonce to confirm communication is with A \n")
    #waiting for A to return Bs nonce to confirm communication is with A
    while True:
        try:
            msg = client.recv(BUFSIZ)
            break
        except:
            print("waiting")
    cipherText=msg
    plainText = private_key.decrypt(cipherText,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),     label=None   ) )
    text=plainText.decode()
    #check if the nonce is correct and send acknowledgement
    if(text==Bnon):
        print("B has received its nonce of %s, so communication with A is confirmed\n" %Bnon)
        print("Sending acknowledgement")
        client.send(bytes("ack","utf8"))
    else:
        print("B received incorrect nonce, communication terminated")
    secKeyExchange(private_key, public_key, Akey, client)

def secKeyExchange(private_key, public_key, Akey, client):
    #waiting for receipt of encrypted secret key from A
    print("Now waiting for receipt of the encrypted secret key for further communication \n")
    while True:
        try:
            secKey = client.recv(BUFSIZ)
            break
        except:
            print("waiting")
    #decrypt and read secret key sent by A
    secretKey=private_key.decrypt(secKey,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),   label=None) )
    print("Received secret key from A of: %s" %secretKey.decode())
    #send acknowledgement of receipt of secret key
    client.send(bytes("ack","utf8"))
    print("Sent acknowledgement of receipt\nNow waiting for message signed with As private key")
    #wait for receipt of the signed key
    while True:
        try:
            signedKey = client.recv(BUFSIZ)
            break
        except:
            print("waiting")
    print("Received signed secret key from A. Will now verify using As public key")
    #B then uses As public key to verify that the secret message was really signed by A with its private key
    try:
        outerSecret=Akey.verify(signedKey,secKey,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
    except:
        print("Failed to verify signature, communication terminated")
        return 0
    #create a symmetric secret key object to be used for encryption and decryption 
    f=Fernet(secretKey)
    print("Signed message has been verified using A's public key\nSending acknowledgement")
    #send acknowledgement of the receipt of the signed and verified secret key
    client.send(bytes("ack","utf8"))
    a=input("Key Exchange Complete\n\nPress Enter to exit: ")
    return 0
    
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
    print("B is Waiting for a connection request...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
