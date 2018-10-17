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
import java.lang.Thread;

import java.util.Scanner; 


public class ClientThread extends Thread
{
	private String clientName = null;
  	private InputStreamReader is = null;
  	private PrintStream os = null;
  	private Socket clientSocket = null; 
	
	public static PrintStream printStream;
	public static BufferedReader reader;

	public ClientThread(Socket clientSocket)
	{
		this.clientSocket = clientSocket;
	}

    public void run() 
	{
		try
	    {
	        /* Create input and output streams for this client. */
	        // is = new DataInputStream(clientSocket.getInputStream());
	        is = new InputStreamReader(clientSocket.getInputStream());
	        os = new PrintStream(clientSocket.getOutputStream());
	        String username;
	        
			reader = new BufferedReader( is );

	        System.out.println("Enter username.");
	        username = reader.readLine().trim();

			// create and start threads to read what the user types and write messages to std.out printStream
			ServerWrite w = new ServerWrite(os, username, clientSocket, reader);
			ServerRead r = new ServerRead(reader);
			w.start();
			r.start();

			w.join();
			r.join();

	        /* Start the conversation. */
	        // while (true) 
	        // {
	        //     String line = is.readLine();
	        //     if (line.startsWith("/quit"))
	        //         break; 
	        //     /* The message*/
	        //     if (line.startsWith(":K")) 
	        //     {
	        //         os.println("@" + username + "> " + line);
	        //     }
	        //     else if (line.startsWith(":M")) 
	        //     {
	        //         os.println("@" + username + "> " + line);
	        //     }
	        //     else if (line.startsWith(":F")) 
	        //     {
	        //         os.println("@" + username + "> " + line);
	        //     }
	        // }
	        /* Close the output stream, close the input stream, close the socket. */
	        is.close();
	        os.close();
	        clientSocket.close();
	    } 
		catch (IOException ex) { ex.printStackTrace(); System.out.println("IO Error"); System.exit(0); } 
		catch (Exception ex) { ex.printStackTrace(); System.out.println("IO Error"); System.exit(0);}
	}

}