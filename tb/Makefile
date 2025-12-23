TOPLEVEL_LANG = verilog

# Simulator
SIM = verilator

# Location of RTL (file is inside src/valid_ready_single/)
VERILOG_SOURCES += $(PWD)/../src/valid_ready.sv

# Top module name (module defined in the SV file is `valid_ready_pipeline`)
TOPLEVEL = valid_ready

# Python testbench (no .py)
MODULE = test_valid_ready

# Enable waveform output
VERILATOR_TRACE = 1

include $(shell cocotb-config --makefiles)/Makefile.sim