/** this dumps the content of a bufferedReader to the screen
 * @Author 
 * @Version 17/10/2018
 */

import java.io.DataInputStream;
import java.io.PrintStream;
import java.io.IOException;
import java.net.Socket;
import java.net.ServerSocket;
import java.io.BufferedReader;
import java.io.InputStreamReader;

import java.util.Scanner; 

public class Server
{
	// The server socket.
	private static ServerSocket serverSocket = null;
	// The client socket.
	private static Socket clientSocket = null;

    public static void main(String[] args) 
    {
    	int portNumber = 2016;

        System.out.println("Server Starting ...");
        Socket messageSocket, userSocket;
        Scanner scanner = new Scanner(System.in); 

        try { 
            System.out.println("Please enter the portNumber to listen on: ");
            int socket = Integer.parseInt(scanner.nextLine());
            
            // make a new socket to listen for messages 
      		serverSocket = new ServerSocket(socket); 
            
		    /*  Create a client socket for each connection and pass it to a new client thread. */
		    while (true)
		    { 
			    clientSocket = serverSocket.accept(); 
	            
                if (clientSocket != null)
                {
                    ClientThread clientThread = new ClientThread(clientSocket); // START THE THREAD
                    // Start Thread
                    clientThread.start() ; 
                    clientThread.join();
                    System.out.println("Server connected!");
                    break;
                }
                else
        		{ 
                    System.out.println("not connected!");
                    break;
                }
			}

        } 
        //MODIFIED FROM IOEXCEPTION FOR DEBUG 
		catch (IOException ex) { ex.printStackTrace(); System.out.println("IO Error"); System.exit(0); } 
		catch (Exception ex) { ex.printStackTrace(); System.out.println("IO Error");  System.exit(0);}
    }

}

