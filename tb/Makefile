TOPLEVEL_LANG = verilog

# Simulator
SIM = verilator

# Location of RTL
VERILOG_SOURCES += $(PWD)/../../src/valid_ready_single.sv

# Top module name
TOPLEVEL = valid_ready_single

# Python testbench (no .py)
MODULE = test_valid_ready

# Enable waveform output
VERILATOR_TRACE = 1

include $(shell cocotb-config --makefiles)/Makefile.sim