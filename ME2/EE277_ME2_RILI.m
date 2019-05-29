%% CODE SUBMITTED BY: Jessa Faye M. Rili
clc;
clear all
close all
rng(277);   

%% Generate output:
%       system with ECC and
%       system without ECC for p=0.05, p=0.025, p=0.0125 
input_filename = 'test.jpg';
[path, input_filename_name, input_filename_ext] = fileparts(input_filename);

p = [0.05, 0.025, 0.0125];
correct_pixel_ratios = zeros(size(p));
for i=1:length(p)
    % GENERATE OUTPUT WITHOUT ECC
    use_ecc = false;
    output_filename = sprintf('%s_%#1.4f_noECC%s', input_filename_name, p(i),...
                                input_filename_ext);
    correct_pixel_ratios(i) = simulate_img_transmission(p(i),...
                                input_filename, use_ecc, output_filename);
    
    % GENERATE OUTPUT WITH ECC
    use_ecc = true;
    output_filename = sprintf('%s_%#1.4f_withECC%s', input_filename_name, p(i),...
                                input_filename_ext);
    correct_pixel_ratios(i) = simulate_img_transmission(p(i),...
                                input_filename, use_ecc, output_filename);
end
    

%% PREPARE PLOTTING

input_filename = 'test.jpg';

x = 0.005:0.005:0.05;

correct_pixel_ratios_withecc = zeros(size(x));
use_ecc = true;
for i=1:length(x)
    correct_pixel_ratios_withecc(i) = simulate_img_transmission(x(i), input_filename, use_ecc, '');
end

correct_pixel_ratios_withoutecc = zeros(size(x));
use_ecc = false;
for i=1:length(x)
    correct_pixel_ratios_withoutecc(i) = simulate_img_transmission(x(i), input_filename, use_ecc, '');
end

%% PLOT
figure(1)
title('Ratio of correct pixels transmitted');
axis([min(x), max(x), 0, 1]);
xlabel('p (transmission error probability)');
ylabel('ratio of number of correct pixels');
hold on;
grid on;
plot(x, correct_pixel_ratios_withecc);
plot(x, correct_pixel_ratios_withoutecc);
legend('with ECC', 'without ECC');
hold off;