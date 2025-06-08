import re
import random
from typing import List, Tuple, Callable, Union

class AdvancedPatterns:
    """Pattern engine that mimics NaturalWrite's approach"""
    
    def __init__(self):
        self.sentence_patterns = self._load_sentence_patterns()
        self.word_patterns = self._load_word_patterns()
        self.flow_breakers = self._load_flow_breakers()
        
    def _load_sentence_patterns(self) -> List[Tuple[str, Union[str, Callable]]]:
        return [
            # Opening transformations (highest priority)
            (r'^(.*?) impacts are becoming', lambda m: f'The world shows increasing signs of {m.group(1)} which'),
            (r'^The (.*?) of (.*?) is', lambda m: f'{m.group(2)} requires {m.group(1)} because it'),
            (r'^Analyzing (.*?) reveals', lambda m: f'The analysis of {m.group(1)} shows'),
            (r'^Reflecting on (.*?),', lambda m: f'My personal {m.group(1)} experiences show that'),
            
            # Complete sentence inversions
            (r'Companies are increasingly (.*?)ing', lambda m: f'Businesses encounter challenges because they {m.group(1)}'),
            (r'Research suggests that (.*?)', lambda m: f'Research indicates that people {m.group(1)}'),
            (r'Studies have shown that', r'Research indicates that'),
            (r'It is (crucial|essential|important) to', lambda m: f'People need to'),
            
            # Passive to active voice
            (r'can be (.*?)ed by', lambda m: f'enables {m.group(1)}ing through'),
            (r'is being (.*?)ed', lambda m: f'experiences {m.group(1)}ing'),
        ]
    
    def _load_word_patterns(self) -> List[Tuple[str, Callable]]:
        return [
            # Conjunction sophistication
            (r'\band\b', lambda m: random.choice(['together with', 'as well as', 'while', 'and'])),
            (r'Additionally,', lambda m: random.choice(['The practice also', 'Furthermore,', 'Moreover,', 'Additionally,'])),
            (r'However,', lambda m: random.choice(['Yet', 'Critics argue that', 'Nevertheless,', 'However,'])),
            (r'Furthermore,', lambda m: random.choice(['What\'s more,', 'Beyond that,', 'Furthermore,'])),
            
            # Word replacements that sound more natural
            (r'\bindividuals\b', lambda m: random.choice(['people', 'persons', 'individuals'])),
            (r'\butilize\b', lambda m: random.choice(['use', 'employ', 'utilize'])),
            (r'\bdemonstrate\b', lambda m: random.choice(['show', 'reveal', 'demonstrate'])),
            
            # Subject-verb-object scrambling
            (r'(\w+) provides (\w+) benefits', lambda m: f'{m.group(2)} benefits come from {m.group(1)}'),
            (r'(\w+) helps (\w+) to (\w+)', lambda m: f'{m.group(1)} enables {m.group(2)} to {m.group(3)}'),
            (r'can (\w+) (\w+)', lambda m: f'has the ability to {m.group(1)} {m.group(2)}'),
        ]
    
    def _load_flow_breakers(self) -> List[Tuple[str, Callable]]:
        return [
            # Add "which" clauses strategically
            (r'(benefits|impacts|effects|changes)(?=[ ,.])', lambda m: f'{m.group(1)} which'),
            (r'(research|studies|analysis)(?=[ ,.])', lambda m: f'{m.group(1)} which'),
            
            # Break up perfect sentence flow
            (r'\. ([A-Z])', lambda m: random.choice(['. ', '. The ', '. This ', '. Our ']) + m.group(1)),
            
            # Add human-like interruptions
            (r'(important|crucial|essential)', lambda m: random.choice([m.group(1), f'very {m.group(1)}', f'really {m.group(1)}'])),
        ]
    
    def apply_patterns(self, text: str) -> Tuple[str, List[str]]:
        """Apply patterns in a way that mimics human writing"""
        changes = []
        
        # Split into sentences for better control
        sentences = re.split(r'(?<=[.!?])\s+', text)
        processed_sentences = []
        
        for i, sentence in enumerate(sentences):
            # First sentence gets heavy transformation
            if i == 0:
                for pattern, replacement in self.sentence_patterns[:5]:  # Focus on openings
                    if re.search(pattern, sentence):
                        if callable(replacement):
                            sentence = re.sub(pattern, replacement, sentence)
                        else:
                            sentence = re.sub(pattern, replacement, sentence)
                        changes.append(f"Opening transformation: {pattern}")
                        break
            
            # Apply word-level changes
            for pattern, replacement in self.word_patterns:
                if re.search(pattern, sentence):
                    if callable(replacement):
                        sentence = re.sub(pattern, replacement, sentence)
                    else:
                        sentence = re.sub(pattern, replacement, sentence)
                    changes.append(f"Word replacement: {pattern}")
            
            # Apply flow breakers (30% chance)
            if random.random() < 0.3:
                for pattern, replacement in self.flow_breakers:
                    if re.search(pattern, sentence):
                        if callable(replacement):
                            sentence = re.sub(pattern, replacement, sentence)
                        else:
                            sentence = re.sub(pattern, replacement, sentence)
                        changes.append(f"Flow breaker: {pattern}")
                        break
            
            processed_sentences.append(sentence)
        
        return ' '.join(processed_sentences), changes 