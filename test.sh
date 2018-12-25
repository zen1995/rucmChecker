#!/bin/bash
for FILENAME in TestError_default17.rucm   TestError_default24.rucm     TestError_default8.rucm      test_3.rucm  TestError_default1.rucm      TestError_default18.rucm     TestError_default25.rucm     test.rucm                    test_4.rucm   TestError_default10.rucm     TestError_default19.rucm     TestError_default26.rucm   test_5.rucm    TestError_default11.rucm     TestError_default20.rucm     TestError_default3.rucm      testNormal.rucm              test_6.rucm TestError_default12.rucm     TestError_default21.rucm     TestError_default4.rucm      test_1.rucm                  test_7.rucm  TestError_default14.rucm     TestError_default22.rucm     TestError_default4_2.rucm    test_10.rucm                 test_8.rucm   TestError_default15.rucm     TestError_default23.rucm     TestError_default5.rucm      test_2.rucm                  test_9.rucm
do
    python3  main.py --rule rule-template.txt test/$FILENAME
    if (($? != 0))
    then
        echo $FILENAME
        exit
    fi
done