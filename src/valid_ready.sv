module valid_ready (
    input  wire clk,
    input  wire rst,

    // Input (producer side)
    input  wire valid_in,
    input  wire data_in,
    output wire ready_in,

    // Output (consumer side)
    output wire valid_out,
    output wire data_out,
    input  wire ready_out
);

    // data_reg holds the actual data
    // valid_reg tells whether data_reg currently holds valid data
    reg data_reg;
    reg valid_reg;

    // We can acccept the data if we are empty or the next module is ready to accept 
    // our curr data(combinational)
    assign ready_in = ~valid_reg || ready_out;

    // Output signals reflect internal state
    assign valid_out = valid_reg;
    assign data_out  = data_reg;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            // Reset clears the pipeline stage
            valid_reg <= 1'b0;
        end else begin
            // Case 1: Accept new data
            if (valid_in && ready_in) begin
                data_reg  <= data_in;
                valid_reg <= 1'b1;
            end
            // Case 2: Data moves out but no new data comes in
            else if (valid_reg && ready_out) begin
                valid_reg <= 1'b0;
            end
            // Else: hold state
        end
    end

endmodule
