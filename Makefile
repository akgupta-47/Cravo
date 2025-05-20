# Makefile

PROTO_DIR=protobuf
OUT_DIR=fastapi/proto

PROTOC=protoc
PY_OUT_FLAG=--python_out=$(OUT_DIR)

PROTO_FILES=$(wildcard $(PROTO_DIR)/*.proto)

all: compile

compile:
	@echo "Compiling .proto files..."
	@mkdir -p $(OUT_DIR)
	@for file in $(PROTO_FILES); do \
		echo "Compiling $$file..."; \
		$(PROTOC) $(PY_OUT_FLAG) $$file; \
	done
	@echo "Done."

clean:
	@echo "Cleaning generated .py files..."
	@rm -f $(OUT_DIR)/*_pb2.py
	@echo "Clean complete."
