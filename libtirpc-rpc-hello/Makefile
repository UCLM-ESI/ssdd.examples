.PHONY: all clean

CLIENT = msg_client
SERVER = msg_server

XDR_SOURCES = msg.x
XDR_HEADER = $(XDR_SOURCES:%.x=%.h)

CLIENT_SRC = $(CLIENT).c
CLIENT_STUB_SRC = msg_clnt.c
CLIENT_OBJECTS = $(CLIENT_SRC:%.c=%.o) $(CLIENT_STUB_SRC:%.c=%.o)

SERVER_SRC  = $(SERVER).c
SERVER_STUB_SRC = msg_svc.c
SERVER_OBJECTS = $(SERVER_SRC:%.c=%.o) $(SERVER_STUB_SRC:%.c=%.o)

RPCGEN_GENFILES = $(XDR_HEADER) $(SERVER_STUB_SRC) $(CLIENT_STUB_SRC)
RPCGEN_OBJECTS = $(RPCGEN_GENFILES:%.c=%.o)

CFLAGS += -g -fPIC $(shell pkg-config --cflags libtirpc)
LDLIBS += $(shell pkg-config --libs libtirpc)
RPCGENFLAGS =

# Targets
all : $(CLIENT) $(SERVER)

$(CLIENT): $(CLIENT_OBJECTS)
	$(LINK.c) $(LDLIBS) -o $@ $^

$(SERVER) : $(SERVER_OBJECTS)
	$(LINK.c) $(LDLIBS) -o $@ $^

$(CLIENT_OBJECTS) $(SERVER_OBJECTS): $(XDR_HEADER)

$(RPCGEN_GENFILES): $(XDR_SOURCES)
	rpcgen $(RPCGENFLAGS) $^

clean:
	 $(RM) core $(CLIENT_OBJECTS) $(SERVER_OBJECTS) $(RPCGEN_GENFILES) $(CLIENT_STUB_SRC) $(SERVER_STUB_SRC) $(CLIENT) $(SERVER) *~
