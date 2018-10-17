/** this dumps the content of a bufferedReader to the screen
 * @Author 
 * @Version 17/10/2018
 */

import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.file.*;
import java.net.Socket;

public class ClientRead extends Thread {
    private BufferedReader reader;

    ClientRead(BufferedReader r) {
        reader = r;
    }

    // Receive keys - Cipher / plain
    public void getKeys(String portNum, String ip) {

    }

    // Receive message - Cipher / plain
    public void getMessage(String portNum, String ip) {

    }

    public void run() {
        String line = "";
        try 
        {
            while (true) 
            {
                synchronized(this) 
                {
                    while (!reader.ready()) {
                        wait(1000);
                    } // spin until we can print to the screen

                    if (reader.ready()) 
                    {
                        // line - input from other clients
                        line = reader.readLine(); // read data received from the other endpoint
                     
                        String userFormatColor = (char) 27 + "[36m";
                        String clearColor = (char) 27 + "[37m";
                       
                        // String username = line.substring(0, line.indexOf(":"));

                        // 'username-optional' 'message type' 'message text'

                        // username :K key-text
                        if (line.toUpperCase().contains(":K")) 
                        { 
                            String key = line.substring(3);
                            System.out.println( "Recieved Key = " + key ); // print it to the terminal
                        }

                        // username :M Message-text
                        else if (line.toUpperCase().contains(":M")) 
                        {
                            String message = userFormatColor + line.substring(3) + clearColor; 
                            System.out.println( "Recieved Message = " + message ); // print it to the terminal
                        }

                        // username :F File-Data text
                        else if (line.toUpperCase().contains(":F")) 
                        { 
                            String data = line.substring(3);
                            System.out.println( "Recieved File data = "+ data ); // print it to the terminal
                            // Write received message bytes to file
                        }

                        else { }
                    }
                }
                // System.out.println(line);
                if (line.equals("q")) {
                    break;
                }
            }
        } catch (Exception e) {
            System.out.println(e);
        }
    }

}