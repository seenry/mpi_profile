#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    int rank, size;
    
    // Initialize MPI
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Check command-line argument
    if (argc != 2) {
        if (rank == 0) {
            fprintf(stderr, "Usage: %s <message_size>\n", argv[0]);
        }
        MPI_Finalize();
        return EXIT_FAILURE;
    }

    int message_size = atoi(argv[1]);
    if (message_size <= 0) {
        if (rank == 0) {
            fprintf(stderr, "Message size must be a positive integer.\n");
        }
        MPI_Finalize();
        return EXIT_FAILURE;
    }

    // Allocate and initialize input buffer
    int *sendbuf = (int *)malloc(sizeof(int) * message_size);
    int *recvbuf = (int *)malloc(sizeof(int) * message_size);

    for (int i = 0; i < message_size; i++) {
        sendbuf[i] = rank;
    }

    for (int i = 0; i < 4; i++)
        MPI_Allreduce(sendbuf, recvbuf, message_size, MPI_INT, MPI_SUM, MPI_COMM_WORLD);

    fflush(stdout);
    MPI_Barrier(MPI_COMM_WORLD);

    // Perform all-reduce operation
    MPI_Allreduce(sendbuf, recvbuf, message_size, MPI_INT, MPI_SUM, MPI_COMM_WORLD);

    // Clean up
    free(sendbuf);
    free(recvbuf);
    MPI_Finalize();
    return EXIT_SUCCESS;
}

