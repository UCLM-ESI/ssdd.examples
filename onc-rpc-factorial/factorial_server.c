#include "factorial.h"

u_long *factorial_1_svc(int *n, struct svc_req *rqstp) {
    static u_long result=1;

    printf("Received: n=%d \n", *n);

    for (int i=*n; i>0; i--)
        result *= i;

    return &result;
}
