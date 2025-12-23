// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Tracing implementation internals

#include "verilated_vcd_c.h"
#include "Vtop__Syms.h"


void Vtop___024root__trace_chg_0_sub_0(Vtop___024root* vlSelf, VerilatedVcd::Buffer* bufp);

void Vtop___024root__trace_chg_0(void* voidSelf, VerilatedVcd::Buffer* bufp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root__trace_chg_0\n"); );
    // Body
    Vtop___024root* const __restrict vlSelf VL_ATTR_UNUSED = static_cast<Vtop___024root*>(voidSelf);
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    if (VL_UNLIKELY(!vlSymsp->__Vm_activity)) return;
    Vtop___024root__trace_chg_0_sub_0((&vlSymsp->TOP), bufp);
}

void Vtop___024root__trace_chg_0_sub_0(Vtop___024root* vlSelf, VerilatedVcd::Buffer* bufp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root__trace_chg_0_sub_0\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    uint32_t* const oldp VL_ATTR_UNUSED = bufp->oldp(vlSymsp->__Vm_baseCode + 1);
    bufp->chgBit(oldp+0,(vlSelfRef.clk));
    bufp->chgBit(oldp+1,(vlSelfRef.rst_n));
    bufp->chgBit(oldp+2,(vlSelfRef.in_valid));
    bufp->chgCData(oldp+3,(vlSelfRef.in_data),8);
    bufp->chgBit(oldp+4,(vlSelfRef.in_ready));
    bufp->chgBit(oldp+5,(vlSelfRef.out_valid));
    bufp->chgCData(oldp+6,(vlSelfRef.out_data),8);
    bufp->chgBit(oldp+7,(vlSelfRef.out_ready));
    bufp->chgBit(oldp+8,(vlSelfRef.valid_ready__DOT__clk));
    bufp->chgBit(oldp+9,(vlSelfRef.valid_ready__DOT__rst_n));
    bufp->chgBit(oldp+10,(vlSelfRef.valid_ready__DOT__in_valid));
    bufp->chgCData(oldp+11,(vlSelfRef.valid_ready__DOT__in_data),8);
    bufp->chgBit(oldp+12,(vlSelfRef.valid_ready__DOT__in_ready));
    bufp->chgBit(oldp+13,(vlSelfRef.valid_ready__DOT__out_valid));
    bufp->chgCData(oldp+14,(vlSelfRef.valid_ready__DOT__out_data),8);
    bufp->chgBit(oldp+15,(vlSelfRef.valid_ready__DOT__out_ready));
    bufp->chgBit(oldp+16,(vlSelfRef.valid_ready__DOT__stage_valid));
    bufp->chgCData(oldp+17,(vlSelfRef.valid_ready__DOT__stage_data),8);
}

void Vtop___024root__trace_cleanup(void* voidSelf, VerilatedVcd* /*unused*/) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root__trace_cleanup\n"); );
    // Locals
    VlUnpacked<CData/*0:0*/, 1> __Vm_traceActivity;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        __Vm_traceActivity[__Vi0] = 0;
    }
    // Body
    Vtop___024root* const __restrict vlSelf VL_ATTR_UNUSED = static_cast<Vtop___024root*>(voidSelf);
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    vlSymsp->__Vm_activity = false;
    __Vm_traceActivity[0U] = 0U;
}
