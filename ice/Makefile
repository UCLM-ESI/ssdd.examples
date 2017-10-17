#!/usr/bin/make -f
# -*- mode:makefile -*-

all:

run-server:
	./Server.py --Ice.Config=Server.config | tee proxy.out

run-client:
	./Client.py '$(shell head -1 proxy.out)'

clean:
	$(RM) *~ proxy.out
	$(RM) -rf dist
