IDL = counter.idl.py
GENERATED = counter_client_stub.py counter_server_stub.py

.PHONY: generate run-server run-client clean

generate: $(GENERATED)

$(GENERATED): $(IDL) rmigen.py picormi.py
	./rmigen.py $(IDL)

run-server: generate
	./server.py

run-client: generate
	./client.py localhost c1

clean:
	$(RM) *~ $(GENERATED)
