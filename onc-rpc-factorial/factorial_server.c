#include "factorial.h"

u_long *factorial_1_svc(int *n, struct svc_req *rqstp) {
    static u_long result;

    printf("Received: n=%d \n", *n);

    result=1;
    for (int i=*n; i>0; i--)
        result *= i;

    return &result;
}
