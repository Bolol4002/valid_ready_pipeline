

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
module valid_ready #(
    parameter int WIDTH = 8
) (
    input  wire             clk,
    input  wire             rst,
    // Input (producer side)
    input  wire             valid_in,
    input  wire [WIDTH-1:0] data_in,
    output logic            ready_in,
    // Output (consumer side)
    output logic            valid_out,
    output logic [WIDTH-1:0] data_out,
    input  wire             ready_out
);
    // data_reg holds the actual data
    // valid_reg tells whether data_reg currently holds valid data
    logic [WIDTH-1:0] data_reg;
    logic             valid_reg;
    // We can accept the data if we are empty or the next module is ready to accept 
    // our current data (combinational)
    assign ready_in = ~valid_reg || ready_out;
    // Output signals reflect internal state
    assign valid_out = valid_reg;
    assign data_out  = data_reg;
    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            // Reset clears the pipeline stage
            valid_reg <= 1'b0;
            // data_reg <= 'x;   // optional: can be left unassigned (don't cares)
        end else begin
            // Case 1: Accept new data
            if (valid_in && ready_in) begin
                data_reg  <= data_in;
                valid_reg <= 1'b1;
            end
            // Case 2: Data moves out but no new data comes in
            else if (valid_reg && ready_out) begin
                valid_reg <= 1'b0;
                // data_reg can optionally be cleared, but not required
            end
            // Else: hold state
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
import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock


@cocotb.test()
async def valid_ready_test(dut):

    # Start clock
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    # Reset
    dut.rst.value = 1
    dut.valid_in.value = 0
    dut.data_in.value = 0
    dut.ready_out.value = 0
    await RisingEdge(dut.clk)

    dut.rst.value = 0
    await RisingEdge(dut.clk)

    # Test vectors
    valid_in  = [0, 1, 1, 0, 1]
    ready_out = [1, 1, 0, 1, 1]
    data_in   = [10, 20, 30, 40, 50]

    expected_valid = []
    expected_data  = []

    for i in range(len(valid_in)):
        dut.valid_in.value = valid_in[i]
        dut.data_in.value  = data_in[i]
        dut.ready_out.value = ready_out[i]

        await RisingEdge(dut.clk)

        expected_valid.append(int(dut.valid_out.value))
        expected_data.append(int(dut.data_out.value))

        print(f"Cycle {i}: "
              f"valid_out={dut.valid_out.value}, "
              f"data_out={dut.data_out.value}")

    # Simple sanity checks
    for i in range(len(expected_valid)):
        if expected_valid[i]:
            assert expected_data[i] != 0, f"Data invalid at cycle {i}"

```



