// Single-stage valid/ready pipeline
// Parameterizable data width
module valid_ready_pipeline #(
    parameter int WIDTH = 8
) (
    input  logic                 clk,
    input  logic                 rst_n,

    // Input (producer) side
    input  logic                 in_valid,
    input  logic [WIDTH-1:0]     in_data,
    output logic                 in_ready,

    // Output (consumer) side
    output logic                 out_valid,
    output logic [WIDTH-1:0]     out_data,
    input  logic                 out_ready
);

    logic stage_valid;
    logic [WIDTH-1:0] stage_data;

    // When stage is empty we can accept input. If stage is full
    // but the downstream is ready to accept the data this cycle,
    // we can accept new input in the same cycle (bubble-through).
    assign in_ready  = !stage_valid || (out_ready && stage_valid);
    assign out_valid = stage_valid;
    assign out_data  = stage_data;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            stage_valid <= 1'b0;
            stage_data  <= '0;
        end else begin
            // Capture input when valid and ready
            if (in_valid && in_ready) begin
                stage_data  <= in_data;
                stage_valid <= 1'b1;
            end

            // If downstream accepts data, clear stage_valid
            // (this makes room for the next input - possibly same cycle)
            if (out_ready && stage_valid && !(in_valid && in_ready && stage_valid)) begin
                // If stage was valid and we transfer to downstream, and
                // we did not simultaneously capture new data above, clear
                stage_valid <= 1'b0;
            end
        end
    end

endmodule
