#include "factorial.h"

void factorial_prog_1(char *host, int n) {
    CLIENT *clnt;
    long *result_1;

#ifndef DEBUG
    clnt = clnt_create (host, FACTORIAL_PROG, FACTORIAL_VERS, "udp");
    if (clnt == NULL) {
	clnt_pcreateerror (host);
	exit (1);
    }
#endif

    result_1 = factorial_1(&n, clnt);
    if (result_1 == NULL)
        clnt_perror(clnt, "call failed");
    else
        printf("factorial(%d): %d", n, *result_1);


#ifndef DEBUG
    clnt_destroy (clnt);
#endif
}

int main(int argc, char *argv[]) {
    char *host;
    int n;

    if (argc < 3) {
	printf ("usage: %s <host> <n>\n", argv[0]);
	return 1;
    }

    host = argv[1];
    n = atoi(argv[2]);
    factorial_prog_1(host, n);

    return 0;
}
