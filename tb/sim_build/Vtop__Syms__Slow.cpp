// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vtop__pch.h"

Vtop__Syms::Vtop__Syms(VerilatedContext* contextp, const char* namep, Vtop* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup top module instance
    , TOP{this, namep}
{
    // Check resources
    Verilated::stackCheck(252);
    // Setup sub module instances
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscopep_TOP = new VerilatedScope{this, "TOP", "TOP", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    __Vscopep_valid_ready = new VerilatedScope{this, "valid_ready", "valid_ready", "valid_ready", -9, VerilatedScope::SCOPE_MODULE};
    // Set up scope hierarchy
    __Vhier.add(0, __Vscopep_valid_ready);
    // Setup export functions - final: 0
    // Setup export functions - final: 1
    // Setup public variables
    __Vscopep_TOP->varInsert("clk", &(TOP.clk), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("data_in", &(TOP.data_in), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("data_out", &(TOP.data_out), false, VLVT_UINT8, VLVD_OUT|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("ready_in", &(TOP.ready_in), false, VLVT_UINT8, VLVD_OUT|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("ready_out", &(TOP.ready_out), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("rst", &(TOP.rst), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("valid_in", &(TOP.valid_in), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("valid_out", &(TOP.valid_out), false, VLVT_UINT8, VLVD_OUT|VLVF_PUB_RW, 0, 0);
    __Vscopep_valid_ready->varInsert("clk", &(TOP.valid_ready__DOT__clk), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_valid_ready->varInsert("data_in", &(TOP.valid_ready__DOT__data_in), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_valid_ready->varInsert("data_out", &(TOP.valid_ready__DOT__data_out), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_valid_ready->varInsert("data_reg", &(TOP.valid_ready__DOT__data_reg), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_valid_ready->varInsert("ready_in", &(TOP.valid_ready__DOT__ready_in), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_valid_ready->varInsert("ready_out", &(TOP.valid_ready__DOT__ready_out), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_valid_ready->varInsert("rst", &(TOP.valid_ready__DOT__rst), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_valid_ready->varInsert("valid_in", &(TOP.valid_ready__DOT__valid_in), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_valid_ready->varInsert("valid_out", &(TOP.valid_ready__DOT__valid_out), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_valid_ready->varInsert("valid_reg", &(TOP.valid_ready__DOT__valid_reg), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
}

Vtop__Syms::~Vtop__Syms() {
    // Tear down scope hierarchy
    __Vhier.remove(0, __Vscopep_valid_ready);
    // Clear keys from hierarchy map after values have been removed
    __Vhier.clear();
    // Tear down scopes
    VL_DO_CLEAR(delete __Vscopep_TOP, __Vscopep_TOP = nullptr);
    VL_DO_CLEAR(delete __Vscopep_valid_ready, __Vscopep_valid_ready = nullptr);
    // Tear down sub module instances
}
