#include <thread>

#include "common.hh"
#include "server.h"
#include "parser.h"

int main(int argc, char *argv[]){
	#ifdef DEBUG
	std::cout <<  "Debug mode activated\n";
	#else
	std::cout << "No Debug mode\n";
	#endif 
	//initializes all the devices/nurses/doctors & ambulance
	initDevices();
	
	//A thread that only reads all the devices
	std::thread deviceMonitor (deviceChecker);
	
	//Leonards Server loading string 
    int status = server();
	
	//sync threads
	deviceMonitor.join();
	
	return status;
}