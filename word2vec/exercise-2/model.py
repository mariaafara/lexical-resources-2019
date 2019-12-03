import torch

class Word2VecCBOWModel(torch.nn.Module):
    """
        Pytorch implementation of CBOW architecture
    """
    def __init__(self, vocab_size, vector_dim, pad_idx):
        """
            Constructor. CBOW consists in a simple linear projection, a sum, and
            a log-linear classifier
        """
        super(Word2VecCBOWModel, self).__init__()
        # linear projection.
        self.vocab_size = vocab_size
        self.pad_idx = pad_idx
        self.projection = torch.nn.Linear(vocab_size, vector_dim, bias=False)
        
        #log-linear classifier
        self.classifier = torch.nn.Linear(vector_dim, vocab_size)
        self.log_softmax = torch.nn.LogSoftmax(dim=1)
        
    def forward(self, context):
        """
            defines training over a single example
        """
        # indices to one-hot. y_pred = [BATCH_SIZE x CONTEXT_SIZE x VOCAB_SIZE]
        y_pred = torch.zeros(*context.size(), self.vocab_size)
        y_pred.scatter_(-1, context.unsqueeze(-1), 1)
        # blank out padding
        y_pred[:,:,self.pad_idx] = 0.
        # pass through linear projection. 
        # y_pred = [BATCH_SIZE x CONTEXT_SIZE x DIM]
        y_pred = self.projection(y_pred)
        # average over context. y_pred = [BATCH_SIZE x DIM]
        y_pred = y_pred.mean(dim=1)
        #pass through log-linear classifier
        y_pred = self.classifier(y_pred)
        y_pred = self.log_softmax(y_pred)
        return y_pred
