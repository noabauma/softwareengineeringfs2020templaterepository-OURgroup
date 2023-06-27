# Test Summary Report

## Introduction

The overall verdict in brief.

## Scenarios tested

### Scenario 1 (PASSED)

Should store 3 values a,b & c. c is mult. from a*b.
At the end typing exit, programm should output CSV with the 3 values.

Result:

> Pass

### Scenario 2 (PASSED)

The user wants to know the results of nested expressions with
parentheses.

> Pass

### Scenario 3 (PASSED)

The user wants to know the result of a trigonometric expression.

> Pass

### Scenario 4 (FAILED)

The user enters an illegal expression which leads to an error.

> Fails, how to reproduce:  
enter log(0), throws an out_of_range instance and crashes. (should return "ERROR...")

## Other concerns and comments

### Noah: 
Very good! I like it, works like wanted! 
Two things bother me:
1. "=" has to be right at Letter. A space between doesn't work.
2. (Scenario 1)c=a*b=0 while C=A*B=7.5
But that is not a big deal! :)

### Leonard:
Looks good to me, only failed scenario is number 4, which seems like an uncatched exception.  
One thing that could be better is the return when entering an empty expression ("") (just returns a number), but this was not asked for. 
