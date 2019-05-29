function [error_pattern] = lookup_syndrome_table(syndrome)
%LOOKUP_SYNDROME_TABLE Looks up a syndrome value in a (7,4) Hamming Code
%Syndrome Table

% initialize output error_pattern
error_pattern = zeros(1,7);

% convert syndrome value to decimal (case statements do not work on
% vectors)
syndrome = bi2de(syndrome, 'left-msb');
switch syndrome
    case 0 %["0","0","0"]
        error_pattern = [0,0,0,0,0,0,0];
    case 4 % ["1","0","0"]
        error_pattern = [1,0,0,0,0,0,0];
    case 2 % ["0","1","0"]
        error_pattern = [0,1,0,0,0,0,0];
    case 1 % ["0","0","1"]
        error_pattern = [0,0,1,0,0,0,0];
    case 6 % ["1","1","0"]
        error_pattern = [0,0,0,1,0,0,0];
    case 3 % ["0","1","1"]
        error_pattern = [0,0,0,0,1,0,0];
    case 7 % ["1","1","1"]
        error_pattern = [0,0,0,0,0,1,0];
    case 5 % ["1","0","1"]
        error_pattern = [0,0,0,0,0,0,1];
end

end

