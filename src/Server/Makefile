JAVAC = javac
JFLAGS = -g

SOURCES = Server.java ServerRead.java ServerWrite.java ClientThread.java

.SUFFIXES:  .java  .class

.java.class:
	$(JAVAC) *.java  $<

Server.class:  ServerRead.class ServerWrite.class ClientThread.class Server.java

clean: 
	@rm –f $(SOURCES:.java=.class)

run:
	java Server