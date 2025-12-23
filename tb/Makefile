# Simple Makefile to run cocotb tests. Default SIM=icarus
TOPLEVEL_LANG = verilog
SIM ?= icarus
TOPLEVEL = valid_ready_pipeline
MODULE = test_valid_ready
VERILOG_SOURCES = ../src/valid_ready.sv

include $(shell cocotb-config --makefiles)/Makefile.sim
