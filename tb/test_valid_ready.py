import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


async def reset_dut(dut):
    dut.rst.value = 1
    dut.valid_in.value = 0
    dut.data_in.value = 0
    dut.ready_out.value = 0
    await Timer(20, units="ns")
    dut.rst.value = 0
    await RisingEdge(dut.clk)


@cocotb.test()
async def test_basic_transfer(dut):
    """Simple valid-ready transfer"""

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    await reset_dut(dut)

    # Drive input
    dut.valid_in.value = 1
    dut.data_in.value = 1
    dut.ready_out.value = 1

    await RisingEdge(dut.clk)

    assert dut.valid_out.value == 1, "valid_out should assert"
    assert dut.data_out.value == 1, "data_out mismatch"

    # Consume data
    await RisingEdge(dut.clk)
    assert dut.valid_out.value == 0, "valid_out should clear after transfer"


@cocotb.test()
async def test_backpressure(dut):
    """Test behavior when downstream is not ready"""

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    await reset_dut(dut)

    # Producer sends data
    dut.valid_in.value = 1
    dut.data_in.value = 1
    dut.ready_out.value = 0  # consumer stalls

    await RisingEdge(dut.clk)

    # Data should be stored internally
    assert dut.valid_out.value == 1
    assert dut.data_out.value == 1

    # Hold for several cycles
    for _ in range(3):
        await RisingEdge(dut.clk)
        assert dut.valid_out.value == 1
        assert dut.data_out.value == 1

    # Now consumer ready
    dut.ready_out.value = 1
    await RisingEdge(dut.clk)

    assert dut.valid_out.value == 0


@cocotb.test()
async def test_no_input_no_output(dut):
    """Idle behavior"""

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    await reset_dut(dut)

    dut.valid_in.value = 0
    dut.ready_out.value = 1

    for _ in range(3):
        await RisingEdge(dut.clk)
        assert dut.valid_out.value == 0


@cocotb.test()
async def test_streaming(dut):
    """Continuous data flow"""

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    await reset_dut(dut)

    dut.ready_out.value = 1

    for i in range(5):
        dut.valid_in.value = 1
        dut.data_in.value = i & 1
        await RisingEdge(dut.clk)

        assert dut.valid_out.value == 1
        assert dut.data_out.value == (i & 1)

    # Stop input
    dut.valid_in.value = 0
    await RisingEdge(dut.clk)
    assert dut.valid_out.value == 0
