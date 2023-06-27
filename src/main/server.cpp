#include "server.h"
#include "parser.h"

// TCP client handling function
void HandleTCPClient(TCPSocket *sock) {
  #ifdef DEBUG
  std::cout << "Handling client ";
  try {
    std::cout << sock->getForeignAddress() << ":";
  } catch (SocketException e) {
    std::cerr << "Unable to get foreign address" << std::endl;
  }
  try {
    std::cout << sock->getForeignPort();
  } catch (SocketException e) {
    std::cerr << "Unable to get foreign port" << std::endl;
  }
  std::cout << std::endl;
  #endif
  // Send received string and receive again until the end of transmission
  char Buffer[RCVBUFSIZE];
  int recvMsgSize;
  while ((recvMsgSize = sock->recv(Buffer, RCVBUFSIZE)) > 0) { // Zero means
                                                         // end of transmission
    #ifdef DEBUG
    std::cout << "Message length: " << recvMsgSize << std::endl;
    std::cout << "Raw Buffer: " << Buffer << std::endl;
    #endif 
    //convert to std::string
    std::string msg = Buffer;
    msg = msg.substr(0, msg.find("}", 0)+1);
    #ifdef DEBUG
    std::cout << "Cut buffer: " << msg << std::endl;
    #endif
    myParser(msg);
    
  }
    delete sock;
}


int server(){
    #ifdef DEBUG
    std::cout << "Recieving on port " << INPUT_PORT << std::endl;
    #endif 
    try
    {
        TCPServerSocket serverSocket(INPUT_PORT);
        HandleTCPClient(serverSocket.accept());            
    }
    catch(const std::exception& e)
    {
        std::cerr << e.what() << '\n';
        return STATUS_BAD;
    }
    return STATUS_OK;
}