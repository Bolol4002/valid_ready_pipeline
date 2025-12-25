import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
import random


async def reset_dut(dut):
    dut.rst.value = 1
    dut.valid_in.value = 0
    dut.data_in.value = 0
    dut.ready_out.value = 0

    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    dut.rst.value = 0
    await RisingEdge(dut.clk)


@cocotb.test()
async def test_simple_flow(dut):
    """
    Producer sends data continuously.
    Consumer always ready.
    """
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    await reset_dut(dut)

    dut.ready_out.value = 1  # consumer always ready

    sent = [1, 0, 1, 1, 0]
    received = []

    async def producer():
        for bit in sent:
            dut.data_in.value = bit
            dut.valid_in.value = 1

            # Wait until accepted
            while True:
                await RisingEdge(dut.clk)
                if dut.ready_in.value == 1:
                    dut.valid_in.value = 0
                    break

    async def consumer():
        while len(received) < len(sent):
            await RisingEdge(dut.clk)
            if dut.valid_out.value == 1 and dut.ready_out.value == 1:
                received.append(int(dut.data_out.value))

    await cocotb.start_soon(producer())
    await cocotb.start_soon(consumer())

    assert received == sent, f"Expected {sent}, got {received}"


@cocotb.test()
async def test_random_backpressure(dut):
    """
    Random ready signal to test stalling behavior.
    """
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    await reset_dut(dut)

    sent = [random.randint(0, 1) for _ in range(20)]
    received = []

    async def producer():
        for bit in sent:
            dut.data_in.value = bit
            dut.valid_in.value = 1
            while True:
                await RisingEdge(dut.clk)
                if dut.ready_in.value == 1:
                    dut.valid_in.value = 0
                    break

    async def consumer():
        while len(received) < len(sent):
            dut.ready_out.value = random.choice([0, 1])
            await RisingEdge(dut.clk)
            if dut.valid_out.value == 1 and dut.ready_out.value == 1:
                received.append(int(dut.data_out.value))

    await cocotb.start_soon(producer())
    await cocotb.start_soon(consumer())

    assert received == sent, f"Mismatch: {received} != {sent}"
