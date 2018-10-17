import java.io.PrintStream;
import java.io.FileInputStream;
import java.util.Scanner;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.io.UnsupportedEncodingException;
import java.nio.file.*;
import java.io.File;

/** this class writes to a printstream
 * @Author: 
 * @Version: 17/10/2018
 */

public class ClientWrite extends Thread
{
	private Scanner scanner ;
	private String user;
	public static boolean quit;
	public static BufferedReader reader; 
	public static Socket userSocket;
	private PrintStream printStream;

	public static Thread messageTransferer;

	ClientWrite(PrintStream p, String user, Socket userSocket, BufferedReader reader)
	{
		this.printStream = p;
		this.scanner = new Scanner(System.in);
		this.user = user;
		this.userSocket = userSocket;
		this.reader = reader;
		printStream.println(user); // send the server the name
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
        System.out.println( "Type input to send: Key, Message, File " ); // print it to the terminal
        
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
				printStream.println( "" ) ;
			}

			else if ( line.toUpperCase().contains(":M") )
			{
				printStream.println(line) ;
				printStream.println( "" ) ;

			}
			
			else if ( line.toUpperCase().contains(":F") )
			{
				String filename = line.substring( line.lastIndexOf(" ")+1 ) ;
				// read file into string or object 
				byte[] data = null;

				File aFile = new File ( filename );

				try 
				{
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
					printStream.println( "F: " + strData ) ;
				}
				catch (UnsupportedEncodingException encodex) { System.out.println("encode Error!"); }
				catch (FileNotFoundException fex) { System.out.println("file not found!"); }
				catch (IOException ioex) { System.out.println("IO Error!"); }
				
			}

			// Send Client connection details to Server to receive file.

			else {
				// Format the user's input.
				printStream.println(line); // write it to the chat
			}
		}
		quit(); // we have left the thread so we can quit
	}
}

	// public boolean SendFile( String filename, String hostname,int portnumber)
	// {
	// 	String fR_hostname = userSocket.getInetAddress().getHostName();	
	// 	int fR_portnumber = 2021;
	// 	boolean sent = false;

	//     try {
	//         InetAddress address = InetAddress.getByName( hostname );  // this converts the string ip into an InetAddress object
	//         Socket c_socket = new Socket ( address , portnumber);

	//         File aFile = new File ( filePath );

	//         if ( aFile.exists() & aFile.isFile())
	//         {
	//           Path path = Paths.get( filePath );
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
