from __future__ import annotations

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from cocotb_tools.runner import get_runner

LANGUAGE = os.getenv("HDL_TOPLEVEL_LANG", "verilog").lower().strip()

@cocotb.test()
async def dff_simple_test(dut):
    """Test that d propagates to q"""

    dut.rst_n.value = 1
    dut.d.value = 0

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk)

    expected_val = 0

    for i in range(10):
        val = random.randint(0, 1)

        dut.d.value = val

        await RisingEdge(dut.clk)

        assert dut.q.value == expected_val, \
            f"output q was incorrect on the {i}th cycle"

        expected_val = val

    await RisingEdge(dut.clk)

    assert dut.q.value == expected_val, \
        "output q was incorrect on the last cycle"


def test_simple_dff_hidden_runner():

    sim = os.getenv("SIM", "icarus")

    proj_path = Path(__file__).resolve().parent.parent

    sources = [
        proj_path / "sources/dff.sv"
    ]

    runner = get_runner(sim)

    runner.build(
        sources=sources,
        hdl_toplevel="dff",
        always=True,
    )

    runner.test(
        hdl_toplevel="dff",
        test_module="test_simple_dff_hidden",
    )
