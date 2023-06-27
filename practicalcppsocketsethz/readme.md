# Practical C++ Sockets -- Unix/Windows compatible
From http://cs.ecs.baylor.edu/~donahoo/practical/CSockets/practical/

Originally by Michael J. Donahoo and Kenneth L. Calvert

Edited to comply with c++11 standards.

## From Original Compilation Instructions :

*Note: This is general information and not specific for this project. Proceed below for project specific information*

Linux:  Make sure to include the pthread library when compiling the
threaded server example.

Windows:  When you compile this program on Windows, make sure you add
wsock32.lib to the library module list (Project->Setting->Link under
VC++).

TCPEchoServer-Thread.cpp requires a PThreads library to run under
Windows.  Here's how I got this to work using the pthreads-win32
library in VC++:

1.  Download the latest snapshot of pthread-win32 from
    http://sources.redhat.com/pthreads-win32.  You probably want the
    precompiled version named pthreads-yyyy-mm-dd.exe.
2.  Copy the include files pthread.h and sched.h to some appropriate
    spot. That would be in PracticalSocket folder. 
    If the compiler does not already know this spot, tell it
    about it.
3.  Copy the DLL to the appropriate spot, that would be inside PracticalSocket folder.

## Compilation Instructions for the Software Engineering project

Copy the PracticalSocket folder and add it to your project src folder as you would do for any other package that you implement. Include it in the CMakeLists.txt of your project's root directory by adding these lines inside the file:

```CMakeLists
set(PRACTICAL_SOCKET_DIR PracticalSocket)

add_subdirectory(${PRACTICAL_SOCKET_DIR})
```