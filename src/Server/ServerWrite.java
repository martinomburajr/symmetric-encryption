/** this class writes to a printstream
 * @Author: 
 * @Version: 17/10/2018
 */

import java.io.PrintStream;
import java.util.Scanner;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.Socket;
import java.io.FileInputStream;
import java.net.UnknownHostException;
import java.io.IOException;
import java.nio.file.*;
import java.io.File;
import java.lang.Thread; 


public class ServerWrite extends Thread
{
	private Scanner scanner ;
	private String user;
	public static boolean quit;
	public static BufferedReader reader; 
	public static Socket userSocket;
	private PrintStream printStream;

	public ServerWrite(PrintStream p, String user, Socket userSocket, BufferedReader reader)
	{
		this.printStream = p;
		this.scanner = new Scanner(System.in);
		this.user = user;
		this.userSocket = userSocket;
		this.reader = reader;
		this.printStream.println(user); // send the server the name
	}

	public void quit()
	{
		try {
			reader.close();
			printStream.close();
			userSocket.close();
			System.out.println("Quitting client");
			System.exit(0);
		}
		catch(Exception e) {
			e.printStackTrace();
		}
	}

	public void run() 
	{
		String line = "";
		this.quit = false;
		
		// keep looping
        System.out.println( "Enter category followed by message to send: ':K 'key'', ':M 'Message'', ':K 'File'' " ); // print it to the terminal

		while (true) 
		{ 
			line = scanner.nextLine(); // keep reading what the user says

			if(line.equals(":q") || line.equals(":quit")) // To quit
			{ 
				printStream.println(line); // print as normal so that the server can process the quit
				System.out.println("Closing connection, exiting");
				break; // leaves the infinite loop
			}

			// Client request file tranfer, Server starts RUNNING file Receiver Thread, Client Sends file to Server
			else if ( line.toUpperCase().contains(":K") )
			{
				// line.substring( line.lastIndexOf(" ")+1)
				
				printStream.println(line); // print as normal so that the server can process the quit
				// System.out.println("Sending Key ...");
			}

			else if ( line.toUpperCase().contains(":M") )
			{
				// System.out.println(":M  Sending Message ...");
				printStream.println(line) ;
			}
			
			else if ( line.toUpperCase().contains(":F") )
			{
				// System.out.println(":F  Files transfer ...");
				String filename = line.substring( line.lastIndexOf(" ") + 1 ) ;
				// read file into string / object 
				byte[] data = null;

				try {
					File aFile = new File ( filename );

					if ( aFile.exists() & aFile.isFile())
					{
						FileInputStream fis = new FileInputStream ( aFile ); //new File (path.toString()) );
						// File contents of the file stored in memory .. watching out for file size
						data = new byte[(int) aFile.length()];
						fis.read(data);
						fis.close();
					}
					String strData = new String(data, "UTF-8");

					// send data.
					printStream.println( "F: Sending file data " + strData ) ;
					printStream.println( "" ) ;
				}
				catch (IOException ex) { ex.printStackTrace(); System.out.println("IO Error");   System.exit(0); } 
				catch (Exception ex) { ex.printStackTrace(); System.out.println("Error");  System.exit(0); }
			}

			// Send Client connection details to Server to receive file.

			else {
				// Format the user's input.
				printStream.println(line); // write it to the chat
			}
		}
		quit(); // we have left the thread so we can quit
	}


	// public boolean SendFile( String filename, String hostname,int portnumber)
	// {
	// 	String fR_hostname = userSocket.getInetAddress().getHostName();	
	// 	int fR_portnumber = 2021;
	// 	boolean sent = false;

	//     try {
	//         InetAddress address = InetAddress.getByName( hostname );  // this converts the string ip into an InetAddress object
	//         Socket c_socket = new Socket ( address , portnumber);

	//         File aFile = new File ( filename );

	//         if ( aFile.exists() & aFile.isFile())
	//         {
	//           FileInputStream fis = new FileInputStream ( aFile ); //new File (path.toString()) );

	//           byte [] data = Files.readAllBytes( Paths.get(path.toString()) );
	//           byte [] buffer =  data; // new byte [fis.available()];   // available returns number of bytes
	          
	//           fis.read(buffer);
	//           ObjectOutputStream oos = new ObjectOutputStream ( c_socket.getOutputStream());
	//           oos.writeObject(buffer);

	//           System.out.println(">>file sent!");
	//           oos.close();
	// 		  sent = true;
	//         }
	        
	//         else
	//           System.out.println(">>Error file not sent. Please enter correct filepath.!");
	        
	//         c_socket.close();
	//     }
	//     catch(UnknownHostException ex)
	//     {
	//         System.out.println( "\nError - Unknown Host : "+ex.toString() );
	//         // ex.printStackTrace();
	//     }
	// 	catch (ClassNotFoundException ex) { ex.printStackTrace(); }
	//     catch (IOException ex) { ex.printStackTrace(); }  
	// 	catch (Exception ex)   { ex.printStackTrace(); }

	// 	return sent;
	// }

}