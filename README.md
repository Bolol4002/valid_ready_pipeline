

# valid_ready_pipeline


Files
- `src/valid_ready_single/valid_ready_single.sv`: the SystemVerilog single-stage pipeline DUT.
- `tb/test_valid_ready.py`: cocotb testbench that verifies functionality and back-pressure behavior.
- `tb/Makefile`: run cocotb tests with a simulator (`verilator` in this project).
- `requirements.txt`: Python dependencies for the venv (cocotb pinned to a working PyPI version).

Overview — valid/ready handshake

The valid/ready handshake is a simple flow-control protocol used in hardware streaming interfaces:

- `valid` (from producer): I have valid data on `data`.
- `ready` (from consumer): I can accept data now.
- A transfer happens when both `valid` and `ready` are high on the same clock edge.

This design implements a single pipeline stage that can hold one data word. It supports bubble-through: when the stage's data is accepted by downstream, the stage can accept new input in the same cycle.

How the SystemVerilog DUT works (walkthrough)

The DUT is in `src/valid_ready_single/valid_ready_single.sv`. Here is the full module followed by an explanation.

```verilog
// Single-stage valid/ready pipeline
// Parameterizable data width
module valid_ready_pipeline #(
  parameter int WIDTH = 8
) (
  input  logic                 clk,
  input  logic                 rst_n,

  // Input (producer) side
  input  logic                 in_valid,
  input  logic [WIDTH-1:0]     in_data,
  output logic                 in_ready,

  // Output (consumer) side
  output logic                 out_valid,
  output logic [WIDTH-1:0]     out_data,
  input  logic                 out_ready
);

  logic stage_valid;
  logic [WIDTH-1:0] stage_data;

  // When stage is empty we can accept input. If stage is full
  // but the downstream is ready to accept the data this cycle,
  // we can accept new input in the same cycle (bubble-through).
  assign in_ready  = !stage_valid || (out_ready && stage_valid);
  assign out_valid = stage_valid;
  assign out_data  = stage_data;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      stage_valid <= 1'b0;
      stage_data  <= '0;
    end else begin
      // Capture input when valid and ready
      if (in_valid && in_ready) begin
        stage_data  <= in_data;
        stage_valid <= 1'b1;
      end

      // If downstream accepts data, clear stage_valid
      // (this makes room for the next input - possibly same cycle)
      if (out_ready && stage_valid && !(in_valid && in_ready && stage_valid)) begin
        // If stage was valid and we transfer to downstream, and
        // we did not simultaneously capture new data above, clear
        stage_valid <= 1'b0;
      end
    end
  end

endmodule
```

Signal behavior and why this works
- `stage_valid`: indicates whether the stage currently holds data.
- `stage_data`: the registered data stored in the stage.
- `out_valid` simply reflects `stage_valid` — downstream sees valid when stage holds data.
- `in_ready` is true when the stage is empty (`!stage_valid`) so it can accept data. It is also true when the stage is full but downstream is ready (`out_ready && stage_valid`), allowing bubble-through (the stage will forward the data to downstream and accept new input in the same cycle).

Important detail: capturing new input and clearing the stage are written so a transfer to downstream can happen in the same cycle as accepting new upstream data. This avoids deadlocks and allows the pipeline to move data efficiently.

How the cocotb testbench exercises the DUT

The cocotb test file is `tb/test_valid_ready.py`. Here is the testbench (full file):

```python
import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


async def reset_dut(dut):
  dut.rst_n.value = 0
  await Timer(100, units='ns')
  dut.rst_n.value = 1
  await RisingEdge(dut.clk)


@cocotb.test()
async def test_simple_flow(dut):
  """Producer sends values while consumer is always ready."""
  cocotb.start_soon(Clock(dut.clk, 10, units='ns').start())
  await reset_dut(dut)

  dut.out_ready.value = 1
  dut.in_valid.value = 0

  data_seq = [1, 2, 3, 4, 255]
  received = []

  async def send_values():
    for v in data_seq:
      # drive valid until accepted
      dut.in_data.value = v
      dut.in_valid.value = 1
      while True:
        await RisingEdge(dut.clk)
        if int(dut.in_ready.value) == 1 and int(dut.in_valid.value) == 1:
          # accepted this cycle
          dut.in_valid.value = 0
          break

  async def recv_values():
    while len(received) < len(data_seq):
      await RisingEdge(dut.clk)
      if int(dut.out_valid.value) == 1 and int(dut.out_ready.value) == 1:
        received.append(int(dut.out_data.value))

  send_task = cocotb.start_soon(send_values())
  recv_task = cocotb.start_soon(recv_values())
  await send_task
  await recv_task

  assert received == data_seq


@cocotb.test()
async def test_random_backpressure(dut):
  """Randomly apply back-pressure and ensure ordering is preserved."""
  cocotb.start_soon(Clock(dut.clk, 10, units='ns').start())
  await reset_dut(dut)

  dut.in_valid.value = 0
  dut.out_ready.value = 0

  data_seq = list(range(1, 21))
  received = []

  async def driver():
    for v in data_seq:
      dut.in_data.value = v
      dut.in_valid.value = 1
      # hold until accepted
      while True:
        await RisingEdge(dut.clk)
        if int(dut.in_ready.value) == 1 and int(dut.in_valid.value) == 1:
          dut.in_valid.value = 0
          break

  async def consumer():
    while len(received) < len(data_seq):
      # randomly toggle ready
      dut.out_ready.value = random.choice([0, 1])
      await RisingEdge(dut.clk)
      if int(dut.out_valid.value) == 1 and int(dut.out_ready.value) == 1:
        received.append(int(dut.out_data.value))

  drv = cocotb.start_soon(driver())
  cons = cocotb.start_soon(consumer())
  await drv
  await cons

  assert received == data_seq

```

Testbench explanation (beginner friendly)
- The testbench creates a clock with `Clock(dut.clk, 10, units='ns')` and applies reset via `reset_dut`.
- `test_simple_flow` drives a sequence of values, holding `in_valid` until `in_ready` becomes true. The test sets `out_ready=1` so downstream never back-pressures; the test then checks the sequence received on `out_data`.
- `test_random_backpressure` randomly toggles `out_ready` to simulate downstream stalling. The driver waits for `in_ready` before moving to the next value. The test ensures ordering is preserved.

How the test maps to the DUT
- When `in_valid` and `in_ready` are both true on a rising clock, the DUT captures `in_data` into `stage_data` and sets `stage_valid`.
- When `out_ready` and `out_valid` are both true on a rising clock, the downstream accepts the stage's data; the DUT clears `stage_valid` unless a new value was captured in the same cycle.

Run the tests (Verilator + venv)

1) Create and activate Python venv and install dependencies (from project root):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

2) Ensure `verilator` is installed and available (we recommend a recent Verilator; check with):

```bash
verilator --version
```

3) Run the tests from the `tb` directory (venv activated):

```bash
cd tb
make SIM=verilator
```

If `make` fails, capture the log and share it. Common fixes:
- Ensure the venv is active so `cocotb-config` is found: `source .venv/bin/activate` from repo root before `cd tb`.
- Verify `tb/Makefile` points at the correct RTL path: `VERILOG_SOURCES` should include `../src/valid_ready_single/valid_ready_single.sv` and `TOPLEVEL` should be `valid_ready_pipeline`.

Learning tips
- Step through the RTL with a waveform viewer (the Makefile enables tracing when supported). Use the VCD/FTZ/GLIF produced by Verilator to inspect `stage_valid`, `in_valid`, `in_ready`, `out_ready` and `stage_data`.
- Modify the DUT to add `WIDTH` changes or a second stage to see how bubble-through and back-pressure interact.

If you want, I can also:
- Add a multi-stage example and tests, or
- Add a GitHub Actions workflow to run the cocotb tests on each push.
