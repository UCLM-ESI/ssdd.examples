#

STUBS = sensor_pb2.py sensor_pb2_grpc.py

all: $(STUBS)

%_pb2.py %_pb2_grpc.py: %.proto
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. $<

clean:
	$(RM) *_pb2* *~
	$(RM) -rf __pycache__
