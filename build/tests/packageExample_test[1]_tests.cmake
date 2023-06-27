add_test( packageExample_tests.dummyClass_test1 /mnt/c/softwareengineeringfs2020templaterepository/build/tests/packageExample_test [==[--gtest_filter=packageExample_tests.dummyClass_test1]==] --gtest_also_run_disabled_tests)
set_tests_properties( packageExample_tests.dummyClass_test1 PROPERTIES WORKING_DIRECTORY .. VS_DEBUGGER_WORKING_DIRECTORY ..)
set( packageExample_test_TESTS packageExample_tests.dummyClass_test1)
