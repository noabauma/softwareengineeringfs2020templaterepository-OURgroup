#ifndef SERVER_H
#define SERVER_H

#include <iostream>
#include "common.hh"
#include "PracticalSocket.h"
#include <string>

#ifndef INPUT_PORT
#define INPUT_PORT 8005
#endif

#ifndef OUTPUT_PORT
#define OUTPUT_PORT 8002
#endif

#define RCVBUFSIZE 100000

// TCP client handling function
void HandleTCPClient(TCPSocket *sock);


int server();



#endif /* SERVER_H */