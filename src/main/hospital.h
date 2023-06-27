#include <string>
#include <chrono>
#include <vector>

#define NOW_MILLIS std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count()

#include "common.hh"

#ifndef HOSPITAL_H
#define HOSPITAL_H

class Meas;
class Device;
class Nurse;
class Doctor;
class Ambulance;

//This class is used to save the value of the numer, i
//if it has been used
//and current time which it got activated
class Meas {
	public:
	double value =  0.0;
	bool hasValue = false;
	long alarmSince = 0L;
	long alarmSince1 = 0L;
	long alarmSince2 = 0L;
	
	void setAlarm() {
		if (alarmSince == 0L) {
			alarmSince = NOW_MILLIS;
		}
	}
	
	void setAlarm1() {
		if (alarmSince1 == 0L) {
			alarmSince1 = NOW_MILLIS;
		}
	}
	
	
	void setAlarm2() {
		if (alarmSince2 == 0L) {
			alarmSince2 = NOW_MILLIS;
		}
	}
	
	void resetAlarm() {
		alarmSince = 0L;
	}
	void resetAlarm1() {
		alarmSince1 = 0L;
	}
	void resetAlarm2() {
		alarmSince2 = 0L;
	}
	
	bool isAlarm(unsigned seconds) {
		if (hasValue && alarmSince != 0L) {
			return NOW_MILLIS - alarmSince > 1000 * seconds;
		}
		
		return false;
	}
	bool isAlarm1(unsigned seconds) {
		if (hasValue && alarmSince1 != 0L) {
			return NOW_MILLIS - alarmSince1 > 1000 * seconds;
		}
		
		return false;
	}
	bool isAlarm2(unsigned seconds) {
		if (hasValue && alarmSince2 != 0L) {
			return NOW_MILLIS - alarmSince2 > 1000 * seconds;
		}
		
		return false;
	}
};

class Device{
	public:
		static unsigned nextID;
		
		#ifdef DEBUG
		static const unsigned maxDevices = 4;						//make it 4 for debugging (default 100)
		#else
		static const unsigned maxDevices = 100;
		#endif 
		
		Meas getdeviceID(){return deviceID;}
		Meas getheartrate(){return heartrate;}
		Meas getbloodsystolic(){return bloodsystolic;}
		Meas getdiastolic(){return diastolic;}
		Meas getbodytemperature(){return bodytemperature;}
		Meas getroomtemperature(){return roomtemperature;}
		Meas getsleepingstate(){return sleepingstate;}
		Meas gettension(){return tension;}
		std::string getimage(){return image;}
		void setimage(std::string img){image = img;}
		bool isblacklist(){return blacklist;}
		void setblacklist(){blacklist = true;}
		
		void construct(std::vector<Nurse> &n, std::vector<Doctor> &dr, std::vector<Ambulance> &a);															//construct the devices
		void set(std::string deviceDescription, double data);			//defined in cpp file
		void check();																//defined in cpp file
		void callambulance();													//defined in cpp file
		void calldoctor();															//defined in cpp file		
		void callnurse();															//defined in cpp file
		std::string makeReport();												//defined in cpp file
	
	private:
		Meas deviceID;
		Meas heartrate;
		Meas bloodsystolic;
		Meas diastolic;
		Meas bodytemperature;
		Meas roomtemperature;
		Meas tension;
		Meas sleepingstate;
		std::string image;
		bool blacklist;
        std::vector<Nurse> nurses;
        std::vector<Doctor> doctors;
        std::vector<Ambulance> ambulances;
};


class Nurse{
	public:
		static unsigned nextID;
		static const unsigned maxNurses = 30;
	
		unsigned getnurseID(){return nurseID;}
		bool getnurseOccupied(){return nurseOccupied;}
		void setnurseOccupied(){nurseOccupied = true;}
		std::vector<bool> getnurseneededby(){return nurseneededby;}
		void setnurseneededby(double idx){nurseneededby[int(idx)] = true;}
		void construct();
        void assign(double deviceID);
		
	private:
		unsigned nurseID;
		bool nurseOccupied;
		std::vector<bool> nurseneededby;
};


class Doctor{
	public:
		static unsigned nextID;
		static const unsigned maxDoctors  = 20;
	
		unsigned getdoctorID(){return doctorID;}
		bool getdoctorOccupied(){return doctorOccupied;}
		std::vector<bool> getdoctorneededby(){return doctorneededby;}
		std::string getreports(){return reports;}
		void setreports(std::string rpt){reports = rpt;}				//not right
		void construct();
        void assign(double deviceID);
	
	private:
		unsigned doctorID;
		bool doctorOccupied;
		std::vector<bool> doctorneededby;
		std::string reports;					//this should be std::string[] of size maxDevices
};


class Ambulance{
	public:
		static unsigned nextID;
        static const unsigned maxAmbulances  = 5;

		bool getambulanceOccupied(){return ambulanceOccupied;}
		std::vector<bool> getambulanceneededby(){return ambulanceneededby;}
        void construct();
        void assign(double deviceID);
		
	private:
        unsigned ambulanceID;
		bool ambulanceOccupied;
		std::vector<bool> ambulanceneededby;
};

#endif