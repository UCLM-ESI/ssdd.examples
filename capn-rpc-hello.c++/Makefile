CXX := g++
CXXFLAGS := -std=c++20 -Wall
LIBS := -lcapnp-rpc -lcapnp -lkj -lkj-async

SCHEMA := upper.capnp
SCHEMA_GEN := upper.capnp.c++ upper.capnp.h

SERVER := server
CLIENT := client

all: $(SERVER) $(CLIENT)

$(SCHEMA_GEN): $(SCHEMA)
	@echo "Generating Cap'n Proto C++ sources..."
	capnp compile -oc++ $(SCHEMA)

$(SERVER): server.cpp $(SCHEMA_GEN)
	$(CXX) $(CXXFLAGS) server.cpp upper.capnp.c++ -o $(SERVER) $(LIBS)

$(CLIENT): client.cpp $(SCHEMA_GEN)
	$(CXX) $(CXXFLAGS) client.cpp upper.capnp.c++ -o $(CLIENT) $(LIBS)

run-server: $(SERVER)
	./$(SERVER)

run-client: $(CLIENT)
	./$(CLIENT)

clean:
	rm -f $(SERVER) $(CLIENT) $(SCHEMA_GEN)

.PHONY: all run-server run-client clean
