#!/usr/bin/make -f

all:

run-server:
	./server.py --Ice.Config=server.config | tee proxy.out

run-client:
	./client.py '$(shell head -1 proxy.out)'

clean:
	$(RM) *~ proxy.out
	$(RM) -rf dist
