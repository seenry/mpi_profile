#!/bin/bash

MPI_HOME=$HOME/mpich/build/install
MPIEXEC=$MPI_HOME/bin/mpiexec
OLD_LD=$LD_LIBRARY_PATH
LD_LIBRARY_PATH=$MPI_HOME/lib:$OLD_LD
OUT_DIR=$PWD/output

rm -rf $OUT_DIR
mkdir -p $OUT_DIR

#     1 256 1kib 16kib 1mib    128mib
MSGS=(1 256 1024 16384 1048576 134217728)

ALGOS=(
    "ring"
    "recursive_doubling"
    "circ_vring"
    "circ_rs_ag"
)

for algo in ${ALGOS[@]}; do
for n in $(seq 5 8); do
for msg in ${MSGS[@]}; do
    echo -n "running $algo-$n-$msg... "
    $MPIEXEC -n $n \
             -ppn $n \
             -genv MPIR_CVAR_DEVICE_COLLECTIVES=none \
             -genv MPIR_CVAR_ALLREDUCE_INTRA_ALGORITHM=$algo \
             ./test $msg >> $OUT_DIR/$algo-$n-$msg.out
    echo done.
done
done
done

LD_LIBRARY_PATH=$OLD_LD

# python ./clean.py

