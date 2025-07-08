#!/bin/bash

rm -f test
$HOME/mpich/build/install/bin/mpicc main.c -o test

