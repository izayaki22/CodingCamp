from typing import List, Union
import re

class TextPreprocessor:
    @staticmethod
    def preprocess(text: Union[List[str], str]) -> List[str]:
        if isinstance(text, list):
            return [TextPreprocessor._preprocess_sentence(sentence) for sentence in text]
        elif isinstance(text, str):
            return [TextPreprocessor._preprocess_sentence(text)]
        else:
            raise ValueError("Invalid input type. Text should be either List[str] or str.")

    @staticmethod
    def _preprocess_sentence(sentence: str) -> str:
        
        symbols = r"[\"'.,\/#@?!$%»\^&\*;:{}=\-_\`~\(\)\[\]0-9\n]"
        sentence = re.sub(r'(\b\w+)-(\w+\b)', r'\1 \2', sentence)
        final_sentence = re.sub(symbols, lambda x: " " if x.group() == "\n" else "", sentence).strip().lower()

        return final_sentence