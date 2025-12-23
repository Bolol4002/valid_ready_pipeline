# valid_ready_pipeline

This repository contains a minimal, self-contained example of a single-stage valid/ready pipeline implemented in SystemVerilog along with a cocotb-based testbench.

Audience: this document teaches the valid/ready handshake, shows a simple RTL implementation, and gives step-by-step instructions to run the cocotb tests from scratch.

Contents
- `src/valid_ready.sv`: SystemVerilog implementation of a single-stage valid/ready pipeline.
- `tb/test_valid_ready.py`: cocotb testbench that verifies functional and flow-control behavior.
- `tb/Makefile`: Makefile to run cocotb tests with a simulator (Icarus by default).
- `requirements.txt`: Python dependencies for running the tests.

Concepts: valid/ready handshake

The valid/ready handshake is a popular streaming interface used to transfer data between producers and consumers while allowing either side to stall the transfer without losing data:

- `valid`: asserted by the sender when data is available.
- `ready`: asserted by the receiver when it can accept data.
- A transfer occurs when both `valid` and `ready` are high on the same clock edge. The sender may keep `valid` asserted until the transfer completes; the receiver may deassert `ready` to apply back-pressure.

Single-stage pipeline behavior

This example implements a single pipeline stage. The stage holds one item of data and exposes the usual streaming interface on both sides:

- Inputs: `in_valid`, `in_data`, `clk`, `rst_n`, `out_ready` (downstream back-pressure).
- Outputs: `in_ready`, `out_valid`, `out_data`.

The stage accepts new input when it is empty or when the current data will be transferred to downstream in the same cycle (i.e., when `out_ready` is true). This lets producers and consumers bubble through the stage efficiently.

Quickstart (Ubuntu / Debian-like)

Prerequisites:

1. System packages (install a simulator and Python):

```bash
sudo apt update
sudo apt install -y verilator iverilog make python3 python3-pip
```

2. Python dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the cocotb test (from repository root):

```bash
cd tb
make SIM=icarus
```

The Makefile uses `cocotb-config --makefiles` to include the standard cocotb simulation Makefile. You can switch `SIM` to another supported simulator (like `verilator`) if you have it installed and configured.

Files and what's inside

- `src/valid_ready.sv` — a compact, synthesizable single-stage pipeline. The module parameters and ports are documented inside the file.
- `tb/test_valid_ready.py` — cocotb tests:
  - `test_simple_flow`: verifies basic transfer when consumer is always ready.
  - `test_random_backpressure`: randomly applies back-pressure to validate flow-control correctness and ordering.

Design notes and rationale

- The stage stores data in a register and uses a `stage_valid` flag to indicate presence of data.
- `in_ready` is asserted when the stage is empty or when the stage will be freed by a simultaneous transfer to downstream (when `out_ready` and `stage_valid` are true).

Extending the example

- Add width, depth, or multi-stage pipelines by chaining instances of the provided module or converting into FIFO-like structures.
- Replace the Makefile SIM with `verilator` or another simulator in environments where Icarus is not desired.

If you want, I can also:
- Run or adapt the tests to target `verilator` instead of Icarus.
- Add a small harness showing multiple pipelined stages.
# Valid Ready Pipeline
2025-12-23

## What is a valid ready pipeline mean??

valid - i have the data
ready - i can accept the data
Transfer only happens when both are set bits

valid ready pipeline solves backpressure like 
- what if stage 2 stalls?
- what if downstream can't accept data?
- What if upstream produces faster than downstream consumes?


so basically if iam full i can only accept the data if i can pass my data to someone else and someone can only accept the data if they dont have any data stored within them.

---
