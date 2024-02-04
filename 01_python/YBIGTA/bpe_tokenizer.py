import re
from typing import List, Optional, Union
from .tokenizer import Tokenizer
from .text_preprocessor import TextPreprocessor
from collections import defaultdict

class BPETokenizer(Tokenizer):
    def __init__(self, corpus: Optional[Union[List[str], str]] = None):
        
        super().__init__(corpus)
        
        self.word_freqs = defaultdict(int)      # 각 단어마다 frequency가 대응된 dict {word : freq}
        self.vocab = defaultdict(int)           # 각 pair마다 frequency가 대응된 dict {pair : freq}
        self.alphabet = []                      # token을 담는 list (alphabet과 merge 된 pair 포함)
        self.splits = {}                        # 각 단어와 단어의 merged 된 형태가 대응된 dict {word : ['w', 'or', 'd']}
        self.merges = {}                        # pair와 merge 된 string이 대응된 dict {('t', 'h') : 'th'}
        
    def compute_word_freqs(self) -> None:           # 각 단어마다 frequency를 계산하는 함수
                                                    # self.word_freqs, self.alphabet, self.splits를 만든다
        
        for sent in self.corpus:
            
            for word in sent.split():
                
                if word in self.word_freqs:
                    self.word_freqs[word] += 1
                else:
                    self.word_freqs[word] = 1
                    
                    for letter in word:                        
                        
                        if letter not in self.alphabet:     
                            self.alphabet.append(letter)
                    
                self.splits[word] = ' '.join(word)
        
    def get_stats(self) -> None:     # 각 pair 마다 frequency를 계산하는 함수. (self.vocab를 만든다)
  
        for word, freq in self.word_freqs.items():
            
            split = self.splits[word].split()
            
            if len(split) == 1:
                continue
            
            for i in range(len(split) - 1):
                
                pair = (split[i], split[i + 1])
                
                self.vocab[pair] += freq

                           
    def merge_vocab(self, pair: List[tuple[str, str]]) -> None:   # 인수로 들어온 pair에 대해 merge 하는 과정
                                                                  # merge 한 후 새로운 token에 대한 pair를 self.vocab에 저장
         
        bigram = re.escape(' '.join(pair))
        pattern = re.compile(r'\b' + bigram + r'\b')
        
        for word in self.word_freqs:

            if len(word) == 1:
                continue
            
            if ' '.join(pair) not in self.splits[word]:         # pair가 word에 없는 경우 - no merge, no self.vocab update
                continue
            
            else:

                self.splits[word] = pattern.sub(''.join(pair), self.splits[word])   # self.splits에서 pair를 합친다
              
                list_split = self.splits[word].split()
                
                if(''.join(pair) not in list_split): 
                    continue
                else: 
                    idx = list_split.index(''.join(pair))           # split된 word에서 pair의 index 찾기
                
                if(idx >= 1):
                    self.vocab[(list_split[idx - 1], list_split[idx])] += self.word_freqs[word]
                
                if idx < len(list_split) - 1:
                    self.vocab[(list_split[idx], list_split[idx + 1])] += self.word_freqs[word]
        
    def train(self, n_iter: int) -> None:

        self.compute_word_freqs()
        self.get_stats()
        
        for _ in range(n_iter):
            
            best = max(self.vocab, key=self.vocab.get)     # self.vocab에서 freq가 제일 높은 key 값(pair) 찾기
            self.merges[best] = ''.join(best)              # self.merges에 추가
            self.merge_vocab(best)                         # merge_vocab 함수를 통해 self.splits 변경, self.vocab 업데이트
            self.alphabet.append(''.join(best))            # self.alphabet에 새로운 token 추가
            self.vocab[best] = 0                           # 각 loop 마다 best 값이 달라져야 하므로 best의 freq를 0으로 변경
        
        
    def tokenize(self, text: Union[List[str], str], padding: bool = False, max_length: Optional[int] = None) -> List[List[int]]:
       
        text = TextPreprocessor.preprocess(text)
        tokens = []

        
        for sent in text:
            tokenized_sent = []
            
            for word in sent.split():
                
                if word in self.splits:
                    tokenized_sent.append(self.splits[word])
                else:
                    
                    word = ' '.join(word)
                    
                    for pair, merge in self.merges.items():
                        
                        if ' '.join(pair) not in word:
                            continue
                        else:
                            pattern = re.compile(r'\b' + ' '.join(pair) + r'\b')
                            word = pattern.sub(merge, word)
                    
                    tokenized_sent.append(word)
            
            tokens.append(tokenized_sent)

        char_to_index = {'<PAD>': 0, **{c: idx + 1 for idx, c in enumerate(self.alphabet)}}
        
        if isinstance(text, list) and padding:
            max_len = max(len(token) for token in tokens)
            tokens = [token + ['<PAD>'] * (max_len - len(token)) for token in tokens]

        if max_length is not None:
            tokens = [token[:max_length] for token in tokens]

        indices = []                # token_index로 출력하기

        for sent in tokens: 
            idx_sent = []
            for token in sent:
                idx_to_str = ''
                for i in range(len(token.split())):
                    c = token.split()[i]
                    if(c not in char_to_index.keys()):
                        idx_to_str += '-'
                    else: 
                        idx_to_str += str(char_to_index[c])
                    idx_to_str += ' '
                
                idx_sent.append(idx_to_str.strip())
                
            indices.append(idx_sent)
         

        return indices
