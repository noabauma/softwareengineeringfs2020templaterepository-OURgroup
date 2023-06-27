#
#   A wrapper for C++ sockets on Unix and Windows
#   Copyright (C) 2002
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

CXX = g++
CXXFLAGS = -Wall -ansi -pedantic -g -I../PracticalSocket

LIBS = ../build/PracticalSocket/libPRACTICAL_CPP_SOCKETS.a

ifeq ($(shell uname),SunOS)
  LIBS += -lsocket -lnsl
endif

all: TCPEchoClient TCPEchoServer UDPEchoClient UDPEchoServer TCPEchoServer-Thread \
BroadcastSender BroadcastReceiver MulticastSender MulticastReceiver

TCPEchoClient: TCPEchoClient.cpp
	$(CXX) $(CXXFLAGS) -o TCPEchoClient TCPEchoClient.cpp $(LIBS)

TCPEchoServer: TCPEchoServer.cpp
	$(CXX) $(CXXFLAGS) -o TCPEchoServer TCPEchoServer.cpp $(LIBS)

UDPEchoClient: UDPEchoClient.cpp
	$(CXX) $(CXXFLAGS) -o UDPEchoClient UDPEchoClient.cpp $(LIBS)

UDPEchoServer: UDPEchoServer.cpp
	$(CXX) $(CXXFLAGS) -o UDPEchoServer UDPEchoServer.cpp $(LIBS)

TCPEchoServer-Thread: TCPEchoServer-Thread.cpp
	$(CXX) -D_GNU_SOURCE -o TCPEchoServer-Thread TCPEchoServer-Thread.cpp $(LIBS) -lpthread

BroadcastSender: BroadcastSender.cpp
	$(CXX) $(CXXFLAGS) -o BroadcastSender BroadcastSender.cpp $(LIBS)

BroadcastReceiver: BroadcastReceiver.cpp
	$(CXX) $(CXXFLAGS) -o BroadcastReceiver BroadcastReceiver.cpp $(LIBS)

MulticastSender: MulticastSender.cpp
	$(CXX) $(CXXFLAGS) -o MulticastSender MulticastSender.cpp $(LIBS)

MulticastReceiver: MulticastReceiver.cpp
	$(CXX) $(CXXFLAGS) -o MulticastReceiver MulticastReceiver.cpp $(LIBS)

clean:
	$(RM) TCPEchoClient TCPEchoServer UDPEchoClient UDPEchoServer TCPEchoServer-Thread \
        BroadcastSender BroadcastReceiver MulticastSender MulticastReceiver
