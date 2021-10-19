/*
 * This is sample code generated by rpcgen.
 * These are only templates and you can use them
 * as a guideline for developing your own functions.
 */

#include "msg.h"


void
messageprog_1(char *host, char *printmessage_1_arg )
{
    CLIENT *clnt;
    int  *result_1;

#ifndef	DEBUG
    clnt = clnt_ncreate (host, MESSAGE_PROG, PRINTMESSAGE_VERS, "udp");
    if (clnt == NULL) {
        clnt_pcreateerror (host);
	exit (1);
    }
#endif	/* DEBUG */
    result_1 = printmessage_1(&printmessage_1_arg, clnt);
    if (result_1 == (int *) NULL) {
        clnt_perror (clnt, "call failed");
    }

#ifndef	DEBUG
    clnt_destroy (clnt);
#endif	 /* DEBUG */
}


int
main (int argc, char *argv[]) {
  char *host, *message;

    if (argc < 3) {
      printf ("usage: %s server_host message\n", argv[0]);
      return 1;
    }

    host = argv[1];
    message = argv[2];
    messageprog_1 (host, message);

    return 0;
}
