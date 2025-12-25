import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


async def reset_dut(dut):
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)


@cocotb.test()
async def basic_smoke(dut):
    """Minimal smoke test: single-item transfer through the stage."""
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)

    # Default idle values
    dut.valid_in.value = 0
    dut.ready_out.value = 1
    await Timer(1, units="ns")

    assert int(dut.valid_out.value) == 0, "valid_out should be 0 after reset"
    assert int(dut.ready_in.value) == 1, "ready_in should be 1 when empty"

    # Send one item
    dut.data_in.value = 0x5A
    dut.valid_in.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    assert int(dut.valid_out.value) == 1, "valid_out should assert when data accepted"
    assert int(dut.data_out.value) == 0x5A, "data_out must match sent data"

    # Consumer accepts it
    dut.ready_out.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    assert int(dut.valid_out.value) == 0, "valid_out should deassert after handshake"
