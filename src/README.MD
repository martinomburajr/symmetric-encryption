
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

### To send keys and data between client and server using terminal: 
> For Keys, use tag ':K' followed by key.
> e.g.:
```
:K 12alskg4211hgh@$!
```
> For Messages, Use tag ':M'  followed by Message.
> e.g.:
```
:M hello client app
```
> For Files ... Use tag ':F' followed by filename.
> e.g.:
```
:F /filename.txt
```