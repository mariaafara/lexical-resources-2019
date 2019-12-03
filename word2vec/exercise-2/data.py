import itertools as it

import torch
import more_itertools as mit

from utils import PAD_TOK

def iter_data(filename, window_size):
    """
        iterates over data 
    """
    with open(filename) as istr:
        # remove trailing blanks
        lines = map(str.strip, istr) 
        # tokenize
        lines = map(str.split, lines)
        for line in lines:
            #iterate over all center positions
            for i, token in enumerate(line):
                yield token, line[i-window_size:i] + line[i+1:i+1+window_size]


def compute_vocabulary(filename, pad_token=PAD_TOK):
    """
        creates vocabulary files for numericalization
    """
    with open(filename) as istr:
        # remove trailing blanks
        lines = map(str.strip, istr) 
        # tokenize
        lines = map(str.split, lines)
        # create itos (cf. `utils.py`)
        itos = list({w for l in lines for w in l} | {PAD_TOK})
        # create stoi (cf. `utils.py`)
        stoi = {w:i for i,w in enumerate(itos)}
        # return itos and stoi
        return itos, stoi

        
def numericalize_example(example, stoi):
    """
        turns a list of strings into a list of integers
    """
    # unpack
    token, context = example
    # map according to stoi
    return stoi[token], list(map(stoi.__getitem__, context))

    
def iter_examples(filename, stoi, window_size=5, batch_size=20):
    """
        reads from file and generates batched tensor examples
    """
    # numericalize
    iter_ex = (numericalize_example(e, stoi) for e in iter_data(filename, window_size))
    # fill-value to pad contexts with
    fv = stoi[PAD_TOK]
    for example in mit.chunked(iter_ex, batch_size):
        #de-tuple
        words, contexts = zip(*example)
        # pad contexts
        contexts = list(zip(*it.zip_longest(*contexts, fillvalue=fv)))
        # create tensors
        word_tensor = torch.tensor(words)
        context_tensor = torch.tensor(contexts)
        yield word_tensor, context_tensor
