CXX := g++
CXXFLAGS := -std=c++20 -Wall
LIBS := -lcapnp-rpc -lcapnp -lkj -lkj-async

SCHEMA := hello.capnp
SCHEMA_GEN := hello.capnp.c++ hello.capnp.h

SERVER := server
CLIENT := client

all: $(SERVER) $(CLIENT)

$(SCHEMA_GEN): $(SCHEMA)
	@echo "Generating Cap'n Proto C++ sources..."
	capnp compile -oc++ $(SCHEMA)

$(SERVER): server.cpp $(SCHEMA_GEN)
	$(CXX) $(CXXFLAGS) server.cpp hello.capnp.c++ -o $(SERVER) $(LIBS)

$(CLIENT): client.cpp $(SCHEMA_GEN)
	$(CXX) $(CXXFLAGS) client.cpp hello.capnp.c++ -o $(CLIENT) $(LIBS)

run-server: $(SERVER)
	./$(SERVER)

run-client: $(CLIENT)
	./$(CLIENT)

clean:
	rm -f $(SERVER) $(CLIENT) $(SCHEMA_GEN)

.PHONY: all run-server run-client clean
