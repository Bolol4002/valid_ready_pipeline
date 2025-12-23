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
