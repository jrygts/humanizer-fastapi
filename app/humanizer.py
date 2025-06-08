import asyncio
from typing import Dict, List
import time
import re
from .patterns import AdvancedPatterns, TYPO_RULES
from .openai_client import OpenAIHumanizer
from .models import ProcessingMode

class HybridHumanizer:
    def __init__(self):
        self.patterns = AdvancedPatterns()
        self.openai = OpenAIHumanizer()
        
    async def humanize(self, text: str, mode: ProcessingMode = ProcessingMode.BALANCED) -> Dict:
        """Main humanization method with async processing"""
        start_time = time.time()
        
        if mode == ProcessingMode.FAST:
            # Regex only - no OpenAI
            result_text, changes = self.patterns.apply_patterns(text)
            return self._build_response(text, result_text, changes, time.time() - start_time, "regex_only")
        
        # Run regex patterns first (always)
        regex_task = asyncio.create_task(self._apply_regex_async(text))
        
        if mode == ProcessingMode.BALANCED:
            # Selective OpenAI - only for problematic sentences
            regex_result = await regex_task
            needs_openai = self._needs_openai_enhancement(regex_result['text'])
            
            if needs_openai:
                openai_result = await self.openai.restructure(regex_result['text'], aggressive=False)
                final_text = openai_result.get('text', regex_result['text'])
                return self._build_response(
                    text, final_text, 
                    regex_result['changes'] + ['OpenAI restructuring'],
                    time.time() - start_time, "hybrid"
                )
            else:
                return self._build_response(
                    text, regex_result['text'], 
                    regex_result['changes'],
                    time.time() - start_time, "regex_only"
                )
        
        else:  # AGGRESSIVE mode
            # Parallel processing for maximum speed
            regex_task = asyncio.create_task(self._apply_regex_async(text))
            openai_task = asyncio.create_task(self.openai.restructure(text, aggressive=True))
            
            regex_result, openai_result = await asyncio.gather(regex_task, openai_task)
            
            # Use OpenAI result if successful, otherwise fallback to regex
            if 'error' not in openai_result:
                final_text = openai_result['text']
                method = "openai_aggressive"
            else:
                final_text = regex_result['text']
                method = "regex_fallback"
            
            return self._build_response(
                text, final_text,
                regex_result['changes'] + [f"OpenAI: {openai_result.get('error', 'success')}"],
                time.time() - start_time, method
            )
    
    async def _apply_regex_async(self, text: str) -> Dict:
        """Apply regex patterns asynchronously"""
        # Run in executor to not block event loop
        loop = asyncio.get_event_loop()
        result_text, changes = await loop.run_in_executor(
            None, self.patterns.apply_patterns, text
        )
        return {'text': result_text, 'changes': changes}
    
    def _needs_openai_enhancement(self, text: str) -> bool:
        """Determine if text needs OpenAI enhancement"""
        # Check for AI detection indicators
        indicators = {
            'perfect_sentences': len(re.findall(r'[.!?]\s+[A-Z]\w+\s+\w+ly\s+', text)),
            'repetitive_structure': self._check_repetitive_structure(text),
            'lacks_which_clauses': text.count('which') < 1,
            'formal_tone': len(re.findall(r'(utilize|implement|demonstrate|facilitate)', text)) > 2
        }
        
        score = sum([
            indicators['perfect_sentences'] > 1,
            indicators['repetitive_structure'],
            indicators['lacks_which_clauses'],
            indicators['formal_tone']
        ])
        
        return score >= 2  # Needs enhancement if 2+ indicators present
    
    def _check_repetitive_structure(self, text: str) -> bool:
        """Check if sentences have similar structure"""
        sentences = re.split(r'[.!?]+', text)
        if len(sentences) < 3:
            return False
        
        # Check first 3 words of each sentence
        structures = []
        for sent in sentences[:3]:
            words = sent.strip().split()[:3]
            if words:
                structures.append(' '.join(words))
        
        return len(set(structures)) < len(structures) * 0.7
    
    def _build_response(self, original: str, humanized: str, changes: List[str], 
                       processing_time: float, method: str) -> Dict:
        """Build standardized response"""
        
        # Apply grammar and typo fixes before finalizing
        fixed_text, grammar_fixes = self._fix_grammar_and_typos(humanized)
        all_changes = changes + grammar_fixes
        
        return {
            'original': original,
            'humanized': fixed_text,
            'processing_time_ms': processing_time * 1000,
            'ai_detection_estimate': self._estimate_ai_detection(fixed_text),
            'method_used': method,
            'changes_applied': all_changes,
            'word_count_change': len(fixed_text.split()) - len(original.split())
        }
    
    def _estimate_ai_detection(self, text: str) -> float:
        """Estimate AI detection probability based on patterns"""
        score = 100  # Start with 100% (definitely AI)
        
        # Reduce score for human-like patterns
        score -= len(re.findall(r'which', text)) * 15
        score -= len(re.findall(r'together with|as well as', text)) * 10
        score -= 20 if not re.match(r'^(The|An?|I|We|My)', text) else 0
        score -= len(re.findall(r'enables \w+ to|benefits come from', text)) * 10
        score -= 10 if re.search(r'people|persons', text) else 0
        
        # Check for natural flow breaks
        sentences = text.split('.')
        if any(len(s.split()) > 25 for s in sentences):  # Long, winding sentences
            score -= 15
        
        return max(0, min(100, score))

    async def batch_humanize(self, texts: List[str], mode: ProcessingMode = ProcessingMode.BALANCED) -> List[Dict]:
        """Process multiple texts in parallel"""
        tasks = [self.humanize(text, mode) for text in texts]
        return await asyncio.gather(*tasks)

    def _fix_grammar_and_typos(self, text: str) -> tuple[str, List[str]]:
        """Fix common grammatical errors and typos introduced by transformations."""
        modified_text = text
        fixes_applied = []
        
        for pattern, replacement in TYPO_RULES:
            old_text = modified_text
            modified_text = re.sub(pattern, replacement, modified_text, flags=re.IGNORECASE)
            
            if old_text != modified_text:
                fixes_applied.append(f"Grammar fix: {pattern} → {replacement}")
        
        return modified_text, fixes_applied 