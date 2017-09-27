#

sensor_pb2.py: sensor.proto
	protoc -I . --python_out=. sensor.proto

clean:
	$(RM) *_pb2* *~
	$(RM) -rf __pycache__
