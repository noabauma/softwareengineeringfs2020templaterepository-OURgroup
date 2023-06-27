#include <iostream>
#include "hospital.h"

/*************************Device*************************/

unsigned Device::nextID = 0;			//static deviceID's

//constructor of Device [0,99]
void Device::construct(std::vector<Nurse> &n, std::vector<Doctor> &dr, std::vector<Ambulance> &a){
    deviceID.value = nextID++;
    deviceID.setAlarm();					//FREQ-16
    blacklist = false;
    nurses = n;
    doctors = dr;
    ambulances = a;
}

void Device::set(std::string deviceDescription, double data){
    deviceID.resetAlarm();
    if		 (deviceDescription == "Heartrate"){heartrate.value = data; heartrate.hasValue = true;}
    else if(deviceDescription == "Bloodsystolic"){ bloodsystolic.value = data; bloodsystolic.hasValue = true;}
    else if(deviceDescription == "Diastolic"){ diastolic.value = data; diastolic.hasValue = true;}
    else if(deviceDescription == "Bodytemperature"){bodytemperature.value = data; bodytemperature.hasValue = true;}
    else if(deviceDescription == "Roomtemperature"){ roomtemperature.value = data; roomtemperature.hasValue = true;}
    else if(deviceDescription == "Sleepingstate"){ sleepingstate.value = data; sleepingstate.hasValue = true;}
    else if(deviceDescription == "Tension"){ tension.value = data; tension.hasValue = true;}
    else if(deviceDescription == "Blacklist"){ blacklist = bool(data);}
    else{std::cout << "error " << deviceDescription << " not found\n"; return;}
}

void Device::check(){
#ifdef DEBUG
    //std::cout << deviceID.value << "\t" << heartrate.value << "\t" << image << "\n";
#endif

    bool case_occured = false;			//FREQ-12

    if(deviceID.isAlarm(12*60*60)){		//FREQ-16
        callnurse();
        deviceID.resetAlarm();
    }

    //FREQ-1 & FREQ-2 & FREQ-3 & FREQ-4
    if(heartrate.hasValue) {
        double heartrate_ = heartrate.value;
        if ((heartrate_ > 40 && heartrate_ < 50) || (heartrate_ > 100 && heartrate_ < 110)){
            heartrate.resetAlarm1();
            heartrate.setAlarm();
        }else if(heartrate_ < 40 || heartrate_ > 110){
            heartrate.setAlarm1();
        }else {
            heartrate.resetAlarm();
            heartrate.resetAlarm1();
        }

        if (heartrate.isAlarm(60)) {
            callnurse();
            case_occured = true;
            heartrate.resetAlarm();
        }if(heartrate.isAlarm1(60)){
            calldoctor();
            case_occured = true;
            heartrate.resetAlarm1();
        }
    }

    //FREQ-9 & FREQ-10 & FREQ-11
    if(bloodsystolic.hasValue){
        if(bloodsystolic.value > 170){				//FREQ-11
            bloodsystolic.setAlarm2();
        }if(bloodsystolic.value > 160){			//FREQ-9
            bloodsystolic.setAlarm1();
        }if(bloodsystolic.value > 150){			//FREQ-10 	(I could set it in range[150,160) but FREQ-10 described it like this)
            bloodsystolic.setAlarm();
        }else {
            bloodsystolic.resetAlarm();
            bloodsystolic.resetAlarm1();
            bloodsystolic.resetAlarm2();
        }

        if (bloodsystolic.isAlarm(600)) {
            callnurse();
            case_occured = true;
            bloodsystolic.resetAlarm();
        }if(bloodsystolic.isAlarm1(600)){
            calldoctor();
            case_occured = true;
            bloodsystolic.resetAlarm1();
        }if(bloodsystolic.isAlarm2(600)){
            callambulance();
            case_occured = true;
            bloodsystolic.resetAlarm2();
        }
    }

    //FREQ-9 & FREQ-10 & FREQ-11
    if(diastolic.hasValue){
        if(diastolic.value > 110){				//FREQ-11
            diastolic.setAlarm2();
        }if(diastolic.value > 100){				//FREQ-9
            diastolic.setAlarm1();
        }if(diastolic.value > 90){				//FREQ-10
            diastolic.setAlarm();
        } else {
            diastolic.resetAlarm();
            diastolic.resetAlarm1();
            diastolic.resetAlarm2();
        }

        if (diastolic.isAlarm(600)) {
            callnurse();
            case_occured = true;
            diastolic.resetAlarm();
        }if(diastolic.isAlarm1(600)){
            calldoctor();
            case_occured = true;
            diastolic.resetAlarm1();
        }if(diastolic.isAlarm2(600)){
            callambulance();
            case_occured = true;
            diastolic.resetAlarm2();
        }
    }


    //FREQ-5 & FREQ-6
    if(bodytemperature.hasValue){
        if(bodytemperature.value < 35 || bodytemperature.value > 40){
            bodytemperature.setAlarm();
        }else{
            bodytemperature.resetAlarm();
        }

        if(bodytemperature.isAlarm(300)){		//300sec = 5min
            callnurse();
            case_occured = true;
            bodytemperature.resetAlarm();
        }
    }

    //FREQ-14
    if(roomtemperature.hasValue){
        if(roomtemperature.value < 20 || roomtemperature.value > 30){
            roomtemperature.setAlarm();
        }else{
            roomtemperature.resetAlarm();
        }

        if(roomtemperature.isAlarm(60)){
            callnurse();

        }if(roomtemperature.isAlarm(600)){
            blacklist = true;
            roomtemperature.resetAlarm();
        }
    }

    //FREQ-7
    if(sleepingstate.hasValue){
        if(bool(sleepingstate.value) == false){		//false means not sleeping
            sleepingstate.setAlarm();
        }else{
            sleepingstate.resetAlarm();
        }

        if(sleepingstate.isAlarm(20*60*60)){			//20*60*60sec = 20hours
            calldoctor();
            case_occured = true;
            sleepingstate.resetAlarm();
        }
    }



    //FREQ-8
    if(tension.hasValue){
        if(tension.value < 9 || tension.value > 11){
            tension.setAlarm();
        }else{
            tension.resetAlarm();
        }

        if(tension.isAlarm(60)){
            callambulance();
            case_occured = true;
            tension.resetAlarm();
        }
    }

    if(case_occured){
        case_occured = false;
        //TODO FREQ-12 && FREQ-13
        std::string report = makeReport();
        //TODO send report to Doctor::reports[]
		
    }

}


void Device::callnurse(){
	
	std::cout <<  "Device: " << deviceID.value << " calling nurse\n";

    bool nurseCalled = false;

    // check if a nurse is free and give him/her the device number
    for (int i = 0; i < nurses.size(); i++) {
        if (!nurses[i].getnurseOccupied()) {

            nurses[i].assign(deviceID.value);

            nurseCalled = true;

            std::cout << "Nurse called!\n";
			break;
        }
    }

    if (!nurseCalled) {
        std::cout << "No nurse available!\n";
    }
}


void Device::calldoctor(){
	
	std::cout <<  "Device: " << deviceID.value << " calling doctor\n";

    bool doctorCalled = false;

    // check if a doctor is free and give him/her the device number
    for (int i = 0; i < doctors.size(); i++) {
        if (!doctors[i].getdoctorOccupied()) {

            doctors[i].assign(deviceID.value);

            doctorCalled = true;

            std::cout << "Doctor called!\n";
			break;
        }
    }

    if (!doctorCalled) {
        std::cout << "No doctor available!\n";
    }
}


void Device::callambulance(){
	
	std::cout <<  "Device: " << deviceID.value << " calling ambulance\n";

    bool ambulanceCalled = false;

    // check if an ambulance is free and give him/her the device number
    for (int i = 0; i < ambulances.size(); i++) {
        if (!ambulances[i].getambulanceOccupied()) {

            ambulances[i].assign(deviceID.value);

            ambulanceCalled = true;

            std::cout << "Ambulance called!\n";
			break;
        }
    }

    if (!ambulanceCalled) {
        std::cout << "No ambulance available!\n";
    }
}


//FREQ-12 && FREQ-13
std::string Device::makeReport(){
	std::string report  = "Device ID: " + std::to_string(deviceID.value) + " \n " +
								"Image: " + image + " \n " + 
								"Heartrate: " + std::to_string(heartrate.value) + " \n " +
								"Bloodsystolic: " + std::to_string(bloodsystolic.value) + " \n " +
								"Diastolic: " + std::to_string(diastolic.value) + " \n " +
								"Bodytemperature: " + std::to_string(bodytemperature.value) + " \n " +
								"Roomtemperature: " + std::to_string(roomtemperature.value) + " \n " +
								"Sleepingstate: " + std::to_string(sleepingstate.value) + " \n " +
								"Tension: " + std::to_string(tension.value) + " \n ";
	
	
	std::cout << "Report for Doctor:\n" << report << "\n\n";			//for debugging
	
	
	return report;
}

/*************************Nurse*************************/
//constructor
unsigned Nurse::nextID = 0;

void Nurse::construct(){
	nurseID = nextID++;
	nurseneededby = std::vector<bool>(Device::maxDevices, false);
	nurseOccupied = false;
}

// assign a device to a nurse
void Nurse::assign(double deviceID) {
    nurseOccupied = true;
    nurseneededby[deviceID] = true;
}


/*************************Doctor*************************/
//constructor
unsigned Doctor::nextID = 0;

void Doctor::construct(){
	doctorID = nextID++;
	doctorneededby = std::vector<bool>(Device::maxDevices, false);
	doctorOccupied = false;
	//TODO Here should be string[] reports being constructed (size maxDevices9
}

// assign a device to a doctor
void Doctor::assign(double deviceID) {
    doctorOccupied = true;
    doctorneededby[deviceID] = true;
}


/*************************Ambulance*************************/
//constructor
unsigned Ambulance::nextID = 0;

void Ambulance::construct(){
    ambulanceID = nextID++;
    ambulanceneededby = std::vector<bool>(Device::maxDevices, false);
    ambulanceOccupied = false;
}

// assign a device to a doctor
void Ambulance::assign(double deviceID) {
    ambulanceOccupied = true;
    ambulanceneededby[deviceID] = true;
}