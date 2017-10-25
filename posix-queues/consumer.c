#include <mqueue.h>
#include <stdio.h>
#include <stdlib.h>

#define	MAXBUFFER	10		/* buffer size */
#define	DATA_TO_RECEIVE	100000		/* amount of data to be produced */

mqd_t	store;				/* message queue */


void Consumer(){
	int data;
	int i;
	for(i=0;i<DATA_TO_RECEIVE;i++){
		if(mq_receive(store,(char*)&data,sizeof(int),0)==-1){
			printf("Error mq_receive\n");
			mq_close(store);
			exit(-1);
		}
		printf("Recibo dato:%d\n", data);
	}
	return;
}
int main(){
	store=mq_open("/queue-data", O_RDONLY);
	if (store==-1){
		printf("Error mq_open\n");
		exit(-1);
	}
	Consumer();
	mq_close(store);
	exit(0);
} 
