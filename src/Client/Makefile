JAVAC = javac
JFLAGS = -g 

SOURCES = Client.java ClientRead.java ClientWrite.java 

.SUFFIXES: .java .class

.java.class:
	$(JAVAC) $(JFLAGS) $<

client.class: ClientRead.class ClientWrite.class Client.java
	
clean:
	@rm –f $(SOURCES:.java=.class)

run:
	java -ea Client
