module valid_ready #(
    parameter int WIDTH = 8
) (
    input  wire             clk,
    input  wire             rst,
    // Input (producer side)
    input  wire             valid_in,
    input  wire [WIDTH-1:0] data_in,
    output logic            ready_in,
    // Output (consumer side)
    output logic            valid_out,
    output logic [WIDTH-1:0] data_out,
    input  wire             ready_out
);
    // data_reg holds the actual data
    // valid_reg tells whether data_reg currently holds valid data
    logic [WIDTH-1:0] data_reg;
    logic             valid_reg;
    // We can accept the data if we are empty or the next module is ready to accept 
    // our current data (combinational)
    assign ready_in = ~valid_reg || ready_out;
    // Output signals reflect internal state
    assign valid_out = valid_reg;
    assign data_out  = data_reg;
    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            // Reset clears the pipeline stage
            valid_reg <= 1'b0;
            // data_reg <= 'x;   // optional: can be left unassigned (don't cares)
        end else begin
            // Case 1: Accept new data
            if (valid_in && ready_in) begin
                data_reg  <= data_in;
                valid_reg <= 1'b1;
            end
            // Case 2: Data moves out but no new data comes in
            else if (valid_reg && ready_out) begin
                valid_reg <= 1'b0;
                // data_reg can optionally be cleared, but not required
            end
            // Else: hold state
        end
    end
endmodule