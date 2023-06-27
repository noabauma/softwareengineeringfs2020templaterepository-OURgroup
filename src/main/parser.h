#ifndef PARSER_H
#define PARSER_H

//master thread checks json string and if correct loads data into meant device
void myParser(std::string str);

void initDevices();

//second thread only reads what master threads writes
void deviceChecker();

#endif