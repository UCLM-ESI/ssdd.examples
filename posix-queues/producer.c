#include <mqueue.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

#define	MAXBUFFER	10		/* buffer size */
#define	DATA_TO_PRODUCE	100000		/* amount of data to be produced */

mqd_t	store;				/* message queue */


void Producer(){
	int data;
	int i;
	for(i=0;i<DATA_TO_PRODUCE;i++){
		data=i;
		if(mq_send(store,(char*)&data,sizeof(int),0)==-1){
			printf("Error mq_send\n");
			mq_close(store);
			exit(-1);
		}
		printf("Envio dato:%d\n", data);
	}
	return;
}

int main(){
	struct mq_attr attr;
	attr.mq_maxmsg=MAXBUFFER;
	attr.mq_msgsize=sizeof(int);
	store=mq_open("/queue-data", O_CREAT|O_WRONLY, 0700, &attr);
	if (store==-1){
		printf("Error mq_open, errno=%d\n",errno);
		exit(-1);
	}
	Producer();
	mq_close(store);
	exit(0);
} 
