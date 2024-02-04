from typing import List, Optional, Union
from .tokenizer import Tokenizer
from .text_preprocessor import TextPreprocessor

class WordTokenizer(Tokenizer):
        
    
    def __init__(self, corpus: Optional[Union[List[str], str]] = None):
        
        super().__init__(corpus)
        
        self.word_tokens = {}
        
    
    def train(self, *args, **kwargs) -> None:

        i = 1
        for sent in self.corpus:
            for word in sent.split():
                if word not in self.word_tokens.keys():
                    self.word_tokens[word] = i
                    i += 1
        
        self.word_tokens['<PAD>'] = 0
                    
    def tokenize(self, text: Union[List[str], str], padding: bool = False, max_length: Optional[int] = None) -> List[List[int]]:
        
        text = TextPreprocessor.preprocess(text)

        if isinstance(text, list) and padding:
            max_len = max(len(token) for token in text)
            tokens = [token + '<PAD>' * (max_len - len(token)) for token in text]

        if max_length is not None:
            if isinstance(text, list):
                tokens = [token[:max_length] for token in tokens]
            else:
                tokens = [tokens[:max_length]]

        indices = []
        for sent in text:
            tokenized_sent =[]
            for word in sent.split():
                if word in self.word_tokens.keys():
                    tokenized_sent.append(self.word_tokens[word])
                else:
                    tokenized_sent.append('-')
            indices.append(tokenized_sent)
            
        return indices


    
