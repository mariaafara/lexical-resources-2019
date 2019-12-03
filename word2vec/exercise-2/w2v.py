import torch

from utils import Environment, PAD_TOK
from data import compute_vocabulary, iter_examples
from model import Word2VecCBOWModel

def build_env(filename, vector_dim, window_size=5, batch_size=20, lr=.1):
    """
        this function builds a training environment, as definied in the file `utils.py`
        components for handling data are defined in the file `data.py`
        the model itself is defined in the `model.py` file.
    """
    # compute vocabulary
    print("compute vocabulary")
    itos, stoi = compute_vocabulary(filename, pad_token=PAD_TOK)
    # compute data iterator
    print("compute data iterator")
    data_iter = iter_examples(filename, stoi, window_size=window_size,
        batch_size=batch_size)
    # build CBOW model
    
    print("build CBOW")
    model = Word2VecCBOWModel(vocab_size=len(itos), vector_dim=vector_dim, pad_idx=stoi[PAD_TOK])
    # initialize optimization algorithm
    print("compute optimizer")
    optim = torch.optim.SGD(model.parameters(), lr=lr)
    # define loss function
    print("compute criterion")
    criterion = torch.nn.NLLLoss()
    # build full environment
    return Environment(itos, stoi, data_iter, model, optim, criterion)

if __name__ == "__main__":
    """
        main entry point to the program.
    """
    # define command-line arguments
    import argparse
    parser = argparse.ArgumentParser(description="PyTorch W2V training script")
    parser.add_argument("filename", type=str, 
        help="corpus file to compute vectors")
    parser.add_argument("--dim", type=int, default=100, 
        help="vector dimensionality")
    parser.add_argument("--window_size", type=int, default=5, 
        help="window size")
    parser.add_argument("--batch_size", type=int, default=20, 
        help="batch size")
    parser.add_argument("--learning_rate", type=float, default=.1, 
        help="learning rate")
    parser.add_argument("--output_file", type=str, default="",
        help="filename to save W2V model")
    args = parser.parse_args()
      
    # build environment  
    environment = build_env(args.filename, args.dim, 
        window_size=args.window_size, batch_size=args.batch_size, lr=args.learning_rate)
    # train model
    environment.train()
    
    if args.output_file:
        # save model
        environment.save_model(args.output_file)
        
