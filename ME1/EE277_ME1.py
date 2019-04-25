'''
EE 277 - Coding and Information Theory
HOZQ 2s1819
Machine Exercise 1
Submitted by: Jessa Rili
              2008-50620
Prerequisites
  Python 3.6.x
  matplotlib
  numpy
  pandas

Note: Start of script processing is after the line "if __name__ == '__main__':"
'''

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

supported_symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                     'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                     'u', 'v', 'w', 'x', 'y', 'z',
                     '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                     ' ', ',', '.', '?', '!', "'", '"', '-', ':', '\n'
                     ]

def init_symbol_freq_dict():
    print('Initializing symbol frequency dictionary...')

    freq_dict = {}

    print('\tNumber of supported symbols: ', len(supported_symbols))
    for symbol in supported_symbols:
        freq_dict[symbol] = 0

    return freq_dict, supported_symbols

def plot_bar_proba(symbols, symbol_probs, output_filename=None):
    df = pd.DataFrame({'symbols': symbols, 'proba': symbol_probs})
    # df = df.set_index('symbols', drop=False)
    df = df.sort_values(by='proba', ascending=False)
    df = df.replace(to_replace=' ', value='<SPC>')
    df = df.replace(to_replace='\n', value='<NL>')
    print(df.to_string())

    df.plot.bar(x='symbols', y='proba')
    plt.grid()

    if output_filename:
        plt.savefig(output_filename)
        print('Please close the plot to continue...')
        plt.show()

'''
    METHOD NAME: get_symbol_freq
    DESCRIPTION:
        Produces a dictionary of symbols and their corresponding probabilities of occurence
        in a given text file
        NOTE: only symbols defined in "supported_symbols" will be included
    INPUT:
        input_filename : input text file
        output_filename : optional graph filename
'''
def get_symbol_freq(input_filename, output_filename=None):
    freq_dict, symbols = init_symbol_freq_dict()

    if os.path.isfile(input_filename) == False:
        print('ERR: Input file "%s" does not exist!') % (input_filename)
    else:
        print('Processing input: %s...' % (input_filename))
        with open(input_filename) as file:
            data = file.read().lower()
            for symbol in data:
                if symbol in freq_dict:
                    freq_dict[symbol] += 1

        symbol_probs = np.array(list(freq_dict.values()))
        symbol_probs = symbol_probs/np.sum(symbol_probs)

        freq_dict = dict(zip(symbols, symbol_probs))

        plot_bar_proba(symbols, symbol_probs, output_filename)

    return freq_dict

def write_dict_to_file(dict, output_filename):
    dict_for_writing = dict.copy()
    print('Writing to file: %s' % (output_filename))
    with open(output_filename, 'w') as f:
        ''' Change white space symbols to a human-readable form '''
        if ' ' in dict:
            dict_for_writing['<SPC>'] = dict_for_writing[' ']
            dict_for_writing.pop(' ')

        if '\n' in dict:
            dict_for_writing['<NL>'] = dict_for_writing['\n']
            dict_for_writing.pop('\n')

        for key in dict_for_writing:
            f.write('%s,%s\n' % (key, dict_for_writing[key]))

def compute_ave_codeword_len(symbol_proba_dict, symbol_code_dict):
    ave_codeword_len = 0

    for symbol in symbol_proba_dict:
        ave_codeword_len = symbol_proba_dict[symbol] * len(symbol_code_dict[symbol])

    print('\tAverage codeword length is: ', ave_codeword_len)
    return ave_codeword_len

'''
    METHOD NAME: get_huffman_codes
    DESCRIPTION:
        Assigns codewords to symbols according to Huffman's algorithm
        Note: This is a recursive function!
    INPUT:
        symbol_proba_dict : dictionary with the symbols as key and symbol probabilities as values
        output_code_dict : omit this (only used in internally during recursion)
'''
def get_huffman_codes(symbol_proba_dict, output_code_dict=None):
    assert(type(symbol_proba_dict) == dict)

    ''' Exit condition and processing of recursion'''
    if len(symbol_proba_dict) == 2:
        if output_code_dict:
            for assigned_code, symbol_seq in enumerate(symbol_proba_dict):
                for symbol in str(symbol_seq):
                    if(symbol not in output_code_dict):
                        output_code_dict[symbol] = ""
                    output_code_dict[symbol] += str(assigned_code)
        #print('output_code_dict in exit: ', output_code_dict, '\n')
        return output_code_dict

    ''' Initialize output code dictionary'''
    if output_code_dict is None:
        output_code_dict = {}
        for symbol in symbol_proba_dict:
            output_code_dict[symbol] = ""

    ''' Sort probabilities from lowest to highest'''
    sorted_proba = sorted(symbol_proba_dict.values())
    #print('Probabilities:\n', sorted_proba)
    ''' Sort symbols according to their probabilities'''
    sorted_keys = sorted(symbol_proba_dict.keys(), key=lambda symbol: symbol_proba_dict[symbol])
    #print('Keys:\n', sorted_keys)

    least_prob_symbols = [sorted_keys[0], sorted_keys[1]]
    #for i, symbol in enumerate(least_prob_symbols):
    #    print('\tLeast%d:%s(%f)' % (i, symbol, symbol_proba_dict[symbol]))

    symbol_proba_dict_combine_least = symbol_proba_dict.copy()
    symbol_proba_dict_combine_least[least_prob_symbols[0]+least_prob_symbols[1]] = symbol_proba_dict_combine_least.pop(least_prob_symbols[0]) + \
                                                                                   symbol_proba_dict_combine_least.pop(least_prob_symbols[1])
    #print('Updated: dict', symbol_proba_dict_combine_least, '\n')

    ''' Call method recursively with each new updated symbol probability dictionary '''
    output_code_dict = get_huffman_codes(symbol_proba_dict_combine_least, output_code_dict)

    #print('symbol_proba_dict: ', symbol_proba_dict)
    #print('least_prob_symbols:', least_prob_symbols)
    for assigned_code, symbol_seq in enumerate(least_prob_symbols):
        for symbol in str(symbol_seq):
            output_code_dict[symbol] += str(assigned_code)

    #print('output_code_dict: ', output_code_dict, '\n')

    return output_code_dict

'''
    METHOD NAME: encode_file
    DESCRIPTION:
        Encodes file given symbol-to-codeword assignments
    INPUT:
        _____
'''
def encode_file(input_filename, symbol_codes, output_filename):
    assert(os.path.isfile(input_filename))
    assert(type(symbol_codes) == dict)

    with open(input_filename) as infile:
        with open(output_filename, 'w') as outfile:
            for symbol in infile.read().lower():
                if symbol in supported_symbols and symbol in symbol_codes:
                    outfile.write(symbol_codes[symbol])
                else:
                    print("\tWARNING: Encountered symbol '%c' in input file '%s' not in supported symbols. Ignoring..."
                          % (symbol, input_filename))

def decode_file(input_filename, symbol_codes, output_filename):
    assert (os.path.isfile(input_filename))
    assert (type(symbol_codes) == dict)
    # asserts that the codewords are unique
    assert (len(set(symbol_codes.values())) == len(symbol_codes))

    # create a code-to-symbol dictionary from the given symbol-to-code dictionary
    code_symbols = {}
    for symbol in symbol_codes:
        code_symbols[symbol_codes[symbol]] = symbol

    with open(input_filename) as infile:
        with open(output_filename, 'w') as outfile:
            current_codeword = ''
            for bit in infile.read():
                #print('\tbit:', bit)

                if current_codeword not in code_symbols:
                    current_codeword += bit
                    #print('\tcurrent_codeword:', current_codeword)

                if current_codeword in code_symbols:
                    outfile.write(code_symbols[current_codeword])
                    current_codeword = ''


if __name__ == '__main__':
    output_dir = 'output'
    if os.path.isdir(output_dir) == False:
        os.mkdir(output_dir)
    '''
        #1
    '''
    input_sequence_filename = 'EE277_ME1_file2compress.txt'
    output_freqgraph_filename = os.path.join(output_dir, 'EE277_ME1_frequencyplot.png')
    print('\n\n\n1. Getting symbol probabilities...',)
    symbol_freq = get_symbol_freq(input_sequence_filename, output_freqgraph_filename)
    print("Done!")

    '''
        #2
    '''
    output_codeword_file = os.path.join(output_dir, 'EE277_ME1_codewordassignment.csv')
    print('\n\n\n2. Getting Huffman codes...',)
    symbol_codes = get_huffman_codes(symbol_freq)
    print("Done!")
    print("\tSANITY CHECK: # of symbols=", len(symbol_codes), " ; # of unique codes=", len(set(symbol_codes.values())))
    ave_codeword_len = compute_ave_codeword_len(symbol_freq, symbol_codes)
    write_dict_to_file(symbol_codes, output_codeword_file)

    '''
        #3
    '''
    encoded_output_filename = os.path.join(output_dir, 'EE277_ME1_encoder_out.txt')
    print('\n\n\n3. Encoding file "%s"' % (input_sequence_filename))
    encode_file(input_sequence_filename, symbol_codes, encoded_output_filename)
    print("Done!")


    '''
        #4
    '''
    decoded_output_filename = os.path.join(output_dir, 'EE277_ME1_decoder_out.txt')
    print('\n\n\n4. Decoding file "%s"' % (encoded_output_filename))
    decode_file(encoded_output_filename, symbol_codes, decoded_output_filename)

