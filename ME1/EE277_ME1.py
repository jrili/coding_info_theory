#################################
# EE 277 - Coding and Information Theory
# HOZQ 2s1819
# Machine Exercise 1
# Submitted by: Jessa Rili
#               2008-50620
# Prerequisites
#   Python 3.6.x
#   matplotlib
#   numpy
#   pandas
#
################

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

def init_symbol_freq_dict():
    print('Initializing symbol frequency dictionary...')

    freq_dict = {}

    supported_symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                         'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                         'u', 'v', 'w', 'x', 'y', 'z',
                         '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                         ' ', ',', '.', '?', '!', "'", '"', '-', ':', '\n'
                         ]
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

def get_symbol_freq(input_filename, output_filename=None):
    print('Processing input: %s...' % (input_filename))
    freq_dict, symbols = init_symbol_freq_dict()
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
    with open(output_filename, 'w') as f:
        for key in dict:
            f.write('%s,%s\n' % (key, dict[key]) )

'''
    METHOD NAME: get_huffman_codes
    DESCRIPTION: 
    INPUT: symbol_proba_dict should be a dictionary with the symbols as key and symbol probabilities as values
    
'''
def get_huffman_codes(symbol_proba_dict, output_code_dict=None):
    assert(type(symbol_proba_dict) == dict)

    ''' Exit condition and processing of recursive function'''
    if len(symbol_proba_dict) == 2:
        if output_code_dict:
            for assigned_code, symbol_seq in enumerate(symbol_proba_dict):
                for symbol in str(symbol_seq):
                    if(symbol not in output_code_dict):
                        output_code_dict[symbol] = ""
                    output_code_dict[symbol] += str(assigned_code)
        print('output_code_dict in exit: ', output_code_dict, '\n')
        return output_code_dict

    ''' Initialize output code dictionary'''
    if output_code_dict is None:
        output_code_dict = {}
        for symbol in symbol_proba_dict:
            output_code_dict[symbol] = ""

    ''' Sort probabilities from lowest to highest'''
    sorted_proba = sorted(symbol_proba_dict.values())
    print('Probabilities:\n', sorted_proba)
    ''' Sort symbols according to their probabilities'''
    sorted_keys = sorted(symbol_proba_dict.keys(), key=lambda symbol: symbol_proba_dict[symbol])
    print('Keys:\n', sorted_keys)

    least_prob_symbols = [sorted_keys[0], sorted_keys[1]]
    for i, symbol in enumerate(least_prob_symbols):
        print('\tLeast%d:%s(%f)' % (i, symbol, symbol_proba_dict[symbol]))

    symbol_proba_dict_combine_least = symbol_proba_dict.copy()
    symbol_proba_dict_combine_least[least_prob_symbols[0]+least_prob_symbols[1]] = symbol_proba_dict_combine_least.pop(least_prob_symbols[0]) + \
                                                                                   symbol_proba_dict_combine_least.pop(least_prob_symbols[1])
    print('Updated: dict', symbol_proba_dict_combine_least, '\n')

    output_code_dict = get_huffman_codes(symbol_proba_dict_combine_least, output_code_dict)
    print('symbol_proba_dict: ', symbol_proba_dict)
    print('least_prob_symbols:', least_prob_symbols)
    for assigned_code, symbol_seq in enumerate(least_prob_symbols):
        for symbol in str(symbol_seq):
            output_code_dict[symbol] += str(assigned_code)

    print('output_code_dict: ', output_code_dict, '\n')

    return output_code_dict


def compute_ave_codeword_len(symbol_proba_dict, symbol_code_dict):
    ave_codeword_len = 0

    for symbol in symbol_proba_dict:
        ave_codeword_len = symbol_proba_dict[symbol]*len(symbol_code_dict[symbol])

    print('Average codeword length is: ', ave_codeword_len)
    return ave_codeword_len


def 

if __name__ == '__main__':
    input_sequence_filename = 'EE277_ME1_file2compress.txt'
    output_freqgraph_filename = 'EE277_ME1_frequencyplot.png'

    print('\n\n\n1. Getting symbol probabilities...')
    symbol_freq = get_symbol_freq(input_sequence_filename)#, output_freqgraph_filename)

    output_codeword_file = 'EE277_ME1_codewordassignment.csv'
    print('\n\n\n2. Getting Huffman codes...')
    symbol_codes = get_huffman_codes(symbol_freq)
    write_dict_to_file(symbol_codes, output_codeword_file)
    ave_codeword_len = compute_ave_codeword_len(symbol_freq, symbol_codes)


    print('\n\n\n3. ')



