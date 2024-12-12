// Full Adder in Verilog
module full_adder (
    input wire a,       // First input
    input wire b,       // Second input
    input wire cin,     // Carry input
    output wire sum,    // Sum output
    output wire cout     // Carry output
);

// Perform the sum and carry operations
assign sum = a ^ b ^ cin;          // Sum is the XOR of a, b, and cin
assign cout = (a & b) | (cin & (a ^ b)); // Carry is true if any two inputs are true

endmodule