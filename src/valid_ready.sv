module valid_ready(
    input clk, rst;
    input valid_in, data_in, ready_out;
    output ready_in, valid_out, data_out;
);
    reg mem=1'b0;
    always @(posedge clk or posedge rst) begin
        if(rst==1'b1) mem=1'b0;
        else begin
            if(valid_in == 1'b1 && ready_in == 1'b1) begin
                mem<=data_in;
                valid_out=1'b1;
            end
            if(valid_out==1'b1 && ready_out==1'b1) begin
                data_out<=mem;
                mem=1'b0;
            end

        end
    end
endmodule
    