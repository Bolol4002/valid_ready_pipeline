# test_valid_ready.py
import cocotb
from cocotb.triggers import Timer, RisingEdge, FallingEdge, Combine
from cocotb.clock import Clock
import random

async def reset_dut(dut):
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)


@cocotb.test()
async def test_basic_flow(dut):
    """Basic smoke test: send one item, receive it"""
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)

    assert dut.valid_out.value == 0, "valid_out should be 0 after reset"
    assert dut.ready_in.value == 1, "ready_in should be 1 after reset (empty)"

    # Send one transaction
    dut.valid_in.value = 1
    dut.data_in.value = 0xA5   # some random pattern

    await RisingEdge(dut.clk)
    await Timer(1, units='ns')  # let comb settle

    assert dut.ready_in.value == 1, "should still be ready (consumer not blocking)"
    assert dut.valid_out.value == 1
    assert dut.data_out.value == 0xA5

    # Consume
    dut.ready_out.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, units='ns')

    assert dut.valid_out.value == 0, "valid should clear after handshake"
    assert dut.ready_in.value == 1, "should be ready again"


@cocotb.test()
async def test_backpressure(dut):
    """Test back-pressure behavior"""
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)

    # Fill the stage
    dut.valid_in.value = 1
    dut.data_in.value = 0x77
    await RisingEdge(dut.clk)

    # Now stage is full → ready_in should go low when consumer not ready
    dut.ready_out.value = 0
    await Timer(1, units='ns')

    assert dut.ready_in.value == 0, "ready_in must be 0 when full and consumer not ready"

    # Try to push new data → should be ignored
    dut.data_in.value = 0xFF
    await RisingEdge(dut.clk)
    await Timer(1, units='ns')

    assert dut.data_out.value == 0x77, "data should NOT change when backpressured"

    # Now let it through
    dut.ready_out.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, units='ns')

    assert dut.valid_out.value == 0
    assert dut.ready_in.value == 1


@cocotb.test()
async def test_stream_random(dut):
    """Randomized streaming test with different stall patterns"""
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    await reset_dut(dut)

    N_TRANSACTIONS = 200

    sent = []
    received = []

    dut.ready_out.value = 0

    for i in range(N_TRANSACTIONS):
        # ----------------------
        # Producer side
        # ----------------------
        if random.random() < 0.85:  # ~85% chance to try send
            data = random.randint(0, 255)
            dut.valid_in.value = 1
            dut.data_in.value = data

            await RisingEdge(dut.clk)

            if dut.ready_in.value == 1:
                sent.append(data)
                # dut._log.info(f"→ sent 0x{data:02x}")
        else:
            dut.valid_in.value = 0
            await RisingEdge(dut.clk)

        # ----------------------
        # Consumer side - random stalls
        # ----------------------
        if len(sent) > len(received) + random.randint(0, 3):  # sometimes allow bubble
            if random.random() < 0.65:  # ~65% chance to accept
                dut.ready_out.value = 1
                await RisingEdge(dut.clk)

                if dut.valid_out.value == 1:
                    received.append(int(dut.data_out.value))
                    # dut._log.info(f"← got  0x{int(dut.data_out.value):02x}")
            else:
                dut.ready_out.value = 0
                await RisingEdge(dut.clk)

    # Drain remaining
    dut.valid_in.value = 0
    dut.ready_out.value = 1

    for _ in range(20):
        await RisingEdge(dut.clk)

    # Final check
    assert len(sent) == len(received), \
        f"Mismatch in transaction count! sent={len(sent)}, received={len(received)}"

    for i, (exp, got) in enumerate(zip(sent, received)):
        assert exp == got, f"Transaction {i} mismatch: expected 0x{exp:02x}, got 0x{got:02x}"

    dut._log.info(f"OK - {len(sent)} transactions passed ✓")


# Optional very simple directed test with long stall
@cocotb.test()
async def test_long_stall(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    dut.valid_in.value = 1
    dut.data_in.value = 0xDE

    await RisingEdge(dut.clk)  # accept first

    dut.ready_out.value = 0

    for _ in range(50):
        await RisingEdge(dut.clk)
        assert dut.ready_in == 0, "should stay not ready during long stall"
        assert dut.data_out == 0xDE, "data should hold"

    dut.ready_out.value = 1
    await RisingEdge(dut.clk)
    assert dut.valid_out == 0, "valid should clear after final handshake"