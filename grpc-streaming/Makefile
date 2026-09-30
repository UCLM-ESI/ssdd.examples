#
SHELL = /bin/bash
PYTHON = $(if $(VIRTUAL_ENV),python3,$(if $(wildcard .venv),.venv/bin/python3,python3))

STUBS = math_pb2.py math_pb2_grpc.py

all: $(STUBS)

%_pb2.py: %.proto
	$(PYTHON) -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. $<

run-server: $(STUBS)
	./server.py

run-client: $(STUBS)
	./client.py localhost 5

venv: .venv

.venv: pyproject.toml
	uv sync

shell: .venv
	bash --rcfile <(echo '[ -f ~/.bashrc ] && . ~/.bashrc; . .venv/bin/activate') -i

requirements.txt: pyproject.toml
	uv export --no-hashes --no-annotate --no-header --no-dev --no-emit-project -o $@

clean:
	$(RM) *~ $(STUBS)
	$(RM) -r __pycache__

.PHONY: all venv shell run-server run-client clean
