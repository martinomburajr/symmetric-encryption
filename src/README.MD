
# Server / Client Application using sockets and AES Ecryption

##Client application
> Send and receives keys, messages and files to/from server application
 To Run Using makefile: compile and run:
  ```
  make 
  make client

  ``` 

##Server application
> Send and receives keys, messages and files to/from client application
To Run Using makefile: compile and run:
  ```
  make 
  make server

  ```

###The server must be executed first

###To send data between client and server using terminal: 
- Use tag ":K 'key'" for keys 
eg.:
```
:K 12alskg4211hgh@$!
```
- Use tag ":M 'Message'" for messages
eg.:
```
:M hello client app
```
- Use tag ":F 'file'" for files
eg.:
```
:F /filename.txt
```