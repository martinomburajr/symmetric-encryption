/** class send messages
 *
 * @Author: 
 * @Version: 17/10/2018
 */

import java.util.Scanner;
import java.io.PrintStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.Socket;

public class Client {

	private static String publicKey;
	private static String privateKey;
	private static String sessionKey;
	private static String user;

	public static Socket userConnectSocket;
	public static PrintStream printStream;
	public static BufferedReader reader;

	public static void main (String [] args) {
		try{ 
			System.out.println("Proprietary Relay Network");

			Scanner scanner = new Scanner(System.in);
			
			System.out.println("Please enter username: ");
			// user = scanner.nextLine();
			user = "user1";
			System.out.println("username : user1");
			
			// prompt IP in string format
			System.out.println("Please enter the server IP: n.n.n.n");				

			// note: 127.0.0.1 connect to this machine (or localhost)
			// String ip = scanner.nextLine();
			String ip = "127.0.0.1";
			
			System.out.println("server IP: 127.0.0.1");
			
			System.out.println("Please enter the server Socket (Port Number)):");  // 2016
			// int socket = Integer.parseInt(scanner.nextLine());
			int socket = Integer.parseInt(scanner.nextLine());
			
			// Convert the string ip into an InetAddress object
			InetAddress address = InetAddress.getByName(ip);						
			// this opens a Socket on port 2017 with the specified ip address
			userConnectSocket = new Socket(address, socket);					
			
			System.out.println("Connection open");
			
			// Allows the user to write to the socket
			printStream = new PrintStream(userConnectSocket.getOutputStream());				
			// reads everything that the is written to the socket
			reader = new BufferedReader(new InputStreamReader(userConnectSocket.getInputStream()));	

			// create and start threads to read what the user types and write messages to std.out printStream
			ClientWrite w = new ClientWrite(printStream, user, userConnectSocket, reader);
			ClientRead r = new ClientRead(reader);
			w.start(); 
			r.start();			

			w.join(); 
			r.join();
		}
		catch (Exception e) {
			System.out.println(e);
			e.printStackTrace();
		}
		
	}

}