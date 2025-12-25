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
