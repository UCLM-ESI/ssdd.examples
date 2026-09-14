IDL = math.idl.py
GENERATED = math_client_stub.py math_server_stub.py

.PHONY: generate run-server run-client clean

generate: $(GENERATED)

$(GENERATED): $(IDL) rpcgen.py picorpc.py
	./rpcgen.py $(IDL)

run-server: generate
	./server.py

run-client: generate
	./client.py localhost 5

clean:
	$(RM) *~ $(GENERATED)
