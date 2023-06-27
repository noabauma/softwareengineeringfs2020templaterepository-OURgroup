#include <iostream>
#include <vector>
#include <chrono>
#include <thread>				//std::this_thread::sleep_for

//jsonxx important includes
#include <cassert>
#include <sstream>
#include <string>
#include <fstream>

#include "parser.h"
#include "hospital.h"
#include "jsonxx.h"
#include "common.hh"

using namespace jsonxx;


//has to be globali defined for deviceChecker
std::vector<Device> d(Device::maxDevices, Device());

//constructs all the classes in a vector with there intended sizes
void initDevices() {

    //constructing 30 nurses
    std::vector<Nurse> n(Nurse::maxNurses, Nurse());
    for(unsigned i = 0; i < Nurse::maxNurses; ++i){
        n[i].construct();
    }

    //constructing 20 doctors
    std::vector<Doctor> dr(Doctor::maxDoctors, Doctor());
    for(unsigned i = 0; i < Doctor::maxDoctors; ++i){
        dr[i].construct();
    }

    //constructing 5 ambulances
    std::vector<Ambulance> a(Ambulance::maxAmbulances, Ambulance());
    for(unsigned i = 0; i < Ambulance::maxAmbulances; ++i){
        a[i].construct();
    }

    //constructing 100 devices with there deviceID and blacklist=false
	for(unsigned i = 0; i < Device::maxDevices; ++i){
		d[i].construct(n, dr, a);
	}
	

}

//master thread checks json string and if correct loads data into specific device
void myParser(std::string str) {
	Object o;
	assert(o.parse(str));
	
	//can only be a real message if deviceId is known
	if(!o.has<Number>("deviceId") || !o.has<String>("deviceDescription") || !o.has<Number>("data") ){
		std::cout << "Message not correct\n";
		return;
	}
	
	unsigned deviceID = o.get<Number>("deviceId");
	if(deviceID >= Device::maxDevices){
		std::cout << "No such deviceID exist\n";
		return;
	}
	
	std::string deviceDescription = o.get<String>("deviceDescription");
	
	if(deviceDescription == "Image"){
		/*
		std::ostream out;
		std::stringstream ss;
		out << o.get<std::string>("data");
		ss << out.rdbuf();							//doesn't work out.rdbuf(); is protected
		std::string image = ss.str();
		
		d[deviceID].setimage(image);
		*/
	}else{
		Number data = o.get<Number>("data");
		d[deviceID].set(deviceDescription, double(data));
	}
	
	
}

//second thread only reads what master threads writes
void deviceChecker(){
	while(true){
		for(unsigned i = 0; i < d.size(); ++i){
			if(!d[i].isblacklist()){
				d[i].check();
			}
		}
		#ifdef DEBUG
		std::this_thread::sleep_for(std::chrono::seconds(1));		//good for debugging but for NFREQ-2 will be removed
		#endif 
	}
}
