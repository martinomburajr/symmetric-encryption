
# Server / Client Application using sockets and AES Ecryption

## Client application
> Send and receives keys, messages and files to/from server application

> To compile and run Client Using makefile:
  ```
  make 
  make run

  ``` 

## Server application
> Send and receives keys, messages and files to/from client application

> To compile and run server using makefile :
  ```
  make 
  make run

  ```

The server must be executed first to initiate connection between the client/server endpoints.

### To send data between client and server using terminal: 
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