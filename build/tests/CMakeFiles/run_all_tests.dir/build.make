# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /mnt/c/softwareengineeringfs2020templaterepository

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /mnt/c/softwareengineeringfs2020templaterepository/build

# Utility rule file for run_all_tests.

# Include the progress variables for this target.
include tests/CMakeFiles/run_all_tests.dir/progress.make

tests/CMakeFiles/run_all_tests: tests/packageExample_test
	cd /mnt/c/softwareengineeringfs2020templaterepository/build/tests && ./packageExample_test
	cd /mnt/c/softwareengineeringfs2020templaterepository/build/tests && test

run_all_tests: tests/CMakeFiles/run_all_tests
run_all_tests: tests/CMakeFiles/run_all_tests.dir/build.make

.PHONY : run_all_tests

# Rule to build all files generated by this target.
tests/CMakeFiles/run_all_tests.dir/build: run_all_tests

.PHONY : tests/CMakeFiles/run_all_tests.dir/build

tests/CMakeFiles/run_all_tests.dir/clean:
	cd /mnt/c/softwareengineeringfs2020templaterepository/build/tests && $(CMAKE_COMMAND) -P CMakeFiles/run_all_tests.dir/cmake_clean.cmake
.PHONY : tests/CMakeFiles/run_all_tests.dir/clean

tests/CMakeFiles/run_all_tests.dir/depend:
	cd /mnt/c/softwareengineeringfs2020templaterepository/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /mnt/c/softwareengineeringfs2020templaterepository /mnt/c/softwareengineeringfs2020templaterepository/tests /mnt/c/softwareengineeringfs2020templaterepository/build /mnt/c/softwareengineeringfs2020templaterepository/build/tests /mnt/c/softwareengineeringfs2020templaterepository/build/tests/CMakeFiles/run_all_tests.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : tests/CMakeFiles/run_all_tests.dir/depend

