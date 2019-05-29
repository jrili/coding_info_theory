function [correct_pixels_ratio] = simulate_img_transmission(p, input_filename, use_ecc, output_filename)
%SIMULATE_IMG_TRANSMISSION simulate transmission over a binary symmetric
%channel
%   Simulate the transmission of "input_filename" over a binary symmetric
%   channel with error probability "p".
%
%   Activate error-correction by setting "use_ecc" = True
%
%   Optionally save the transmitted
%   image into "output_filename" (set to '' to skip)
%   
rng(277);   

logprint = sprintf('Simulation of "%s" with p=%#1.4f started. Loading image...\n\n',...
                        input_filename,p);                    
fprintf(logprint)
%% image encoder
img_data = imread(input_filename);
dim_size = size(img_data);

img_bits = reshape(img_data,prod(dim_size),1);
img_bits = de2bi(img_bits);
img_bits = reshape(img_bits,1,prod(dim_size)*8);

%% %% %% ECC encoder %% %% %% 
n = 7; % length of encoded block
k = 4; % block size

% Parity Matrix for (7,4) Hamming code:
P = [1, 1, 0;
    0, 1, 1;
    1, 1, 1;
    1, 0, 1];
    
% initialize coded_bits:
coded_bits = zeros(1, n*length(img_bits)/k, 'uint8');

% initialize some stuff for execution time measurement
current_progress_milestone = 10;
tic

if use_ecc
    G = [P, eye(k)];

    % Encode bits per block
    num_blks = (length(img_bits)/k);

    for i=1:num_blks
        % Get 1 block from img_bits and encode
        start_index = (i-1)*k+1;
        end_index = start_index + k-1;
        m = double(img_bits(start_index:end_index));
        c = mod(m*G, 2);

        % Store encoded bit sequence into coded_bits
        start_index = (i-1)*n+1;
        end_index = start_index + n-1;
        coded_bits(start_index:end_index) = c;

        % Calculate progress and print to console during a milestone
        progress = 100*(i/num_blks);
        if progress >= current_progress_milestone
            logstr = sprintf('Image encoding in progress, please wait... %#2.2f percent done.\n',...
                            100*(i/num_blks));
            fprintf(logstr)
            current_progress_milestone = current_progress_milestone + 10;
        end
    end
else
    coded_bits = img_bits;
end

total_elapsed_time = toc;
logstr = sprintf('Image encoding finished after %d mins %f seconds\n\n',...
    uint8(total_elapsed_time/60), mod(total_elapsed_time, 60));
fprintf(logstr);

%% channel transmission
error_pattern = binornd(1,p*ones(1,length(coded_bits)));
recv_bits = uint8(xor(coded_bits,error_pattern));


%% %% %% ECC decoder %% %% %%

if use_ecc
    % parity check matrix
    H = [eye(n-k), P.'];
    H = H.';

    num_codewords = length(recv_bits)/n;
    recovered_img_bits = zeros(1,num_codewords*k);
    current_progress_milestone=0;

    for i=1:num_codewords
        % Get 1 codeword and then compute the syndrome "s"
        start_index = (i-1)*n +1;
        end_index = start_index + n -1;
        current_codeword = double(recv_bits(start_index:end_index));
        s = mod(current_codeword*H, 2);

        % Look-up the error pattern associated with syndrome "s" then add
        % it to the codeword to correct any detected errors
        error_pattern = double(lookup_syndrome_table(s));
        current_codeword = mod(current_codeword + error_pattern, 2);

        % Store the decoded message into "recovered_img_bits"
        start_index = (i-1)*k+1;
        end_index = start_index + k-1;
        recovered_img_bits(start_index:end_index) = current_codeword(k:n);
        
        % Calculate progress and print to console during a milestone
        progress = 100*(i/num_codewords);
        if progress >= current_progress_milestone
            logstr = sprintf('Image decoding in progress, please wait... %#2.2f percent done.\n',...
                            100*(i/num_codewords));
            fprintf(logstr)
            current_progress_milestone = current_progress_milestone + 10;
        end
    end
else
    recovered_img_bits = recv_bits;
end
total_elapsed_time = toc;
logstr = sprintf('Image decoding finished after %d mins %f seconds',...
    uint8(total_elapsed_time/60), mod(total_elapsed_time, 60));
fprintf(logstr);

recovered_img_bits = uint8(recovered_img_bits);

%% image decoders
recovered_img_bits = reshape(recovered_img_bits,size(img_bits));
recv_img = reshape(recovered_img_bits,prod(dim_size),8);
recv_img = bi2de(recv_img);
recv_img = reshape(recv_img,dim_size);

if ~strcmp(output_filename, '')
    imwrite(recv_img, output_filename)
end

correct_pixels_ratio = sum(sum(and(recv_img(:,:,1) == img_data(:,:,1),and(recv_img(:,:,2) == img_data(:,:,2),recv_img(:,:,3) == img_data(:,:,3)))))/(prod(size(recv_img))/3)

end

