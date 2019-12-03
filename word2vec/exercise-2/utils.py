import itertools as it
import pickle as pk

# token used for padding contexts
PAD_TOK = "<PAD>"

class Environment(object):
    """
        Object describing a training session for a Word2Vec model
    """
    def __init__(self, itos, stoi, data_iter, model, optim, criterion):
        """
            constructor
        """
        self.itos = itos # integer-to-string : transform row index into str word
        self.stoi = stoi # string-to-integer : transform str word into row index
        self._data_iter = data_iter # data iterator
        self.model = model # model to train
        self.optim = optim # optimization algorithm
        self.criterion = criterion # loss function
        
    @property
    def data_iter(self):
        """
            small python hack to avoid deplating the generator
        """
        return it.tee(self._data_iter)[-1]
        
    def __getitem__(self, key):
        """
            small python hack for user-friendly syntax
        """
        if type(key) is str:
            key = self.stoi[key]
        return self.model.projection.weight[:,key]
        
        
    def train_epoch(self):
        """
            perform one training iteration
        """
        # standard training loop
        
        # set model to training mode
        self.model.train()
        summed_loss = 0.
        # iterate over data
        for i, (target_word, source_context) in enumerate(self.data_iter, start=1):
            # reinitialize gradient 
            self.optim.zero_grad()
            # generate a prediction
            output_prediction = self.model(source_context)
            # compute loss
            loss = self.criterion(output_prediction, target_word)
            # compute gradient by back-propagation
            loss.backward()
            # optionally: print current loss, loss should decrease over training 
            summed_loss += loss.item()
            if i % 100 == 0:
                print(summed_loss / i)
            # optimize model: apply gradient to weights
            self.optim.step()
        # set model to evaluation mode
        self.model.eval()
    
    def train(self, epochs=6):
        """
            perform full training.
        """
        for epoch in range(1, epochs+1):
            self.train_epoch()
            
    def save_model(self, output_file):
        """
            save this environment as a pickle file
        """
        with open(output_file, 'wb') as f:
            pk.dump(self.__dict__, f, 2)
        
    @staticmethod
    def from_file(save_file):
        """
            load environment from pickle file
        """
        with open(save_file, 'rb') as f:
            return pk.load(f)
