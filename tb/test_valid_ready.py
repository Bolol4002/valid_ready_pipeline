import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock


@cocotb.test()
async def basic_valid_ready_test(dut):
    """Minimal test for valid-ready handshake"""

    # Start clock
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    # Initialize inputs
    dut.rst.value = 1
    dut.valid_in.value = 0
    dut.data_in.value = 0
    dut.ready_out.value = 0

    # Apply reset
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst.value = 0

    # ---- Test 1: Send one data word ----
    dut.data_in.value = 0xAB
    dut.valid_in.value = 1
    dut.ready_out.value = 1  # downstream ready

    await RisingEdge(dut.clk)

    # Check that data was accepted
    assert dut.valid_out.value == 1, "valid_out should be high after accepting data"
    assert dut.data_out.value == 0xAB, "data_out mismatch"

    # ---- Test 2: Consumer accepts data ----
    await RisingEdge(dut.clk)

    # After transfer, buffer should be empty
    assert dut.valid_out.value == 0, "valid_out should be low after data is consumed"

    # ---- Test 3: Stall scenario ----
    dut.valid_in.value = 1
    dut.data_in.value = 0x55
    dut.ready_out.value = 0  # stall downstream

    await RisingEdge(dut.clk)

    # Data should be stored internally
    assert dut.valid_out.value == 1, "valid_out should remain high during stall"
    assert dut.data_out.value == 0x55, "data should be held stable"

    # Release stall
    dut.ready_out.value = 1
    await RisingEdge(dut.clk)

    assert dut.valid_out.value == 0, "data should have moved out after stall release"

    dut.valid_in.value = 0

    await Timer(20, units="ns")
