import openai
import asyncio
from typing import Dict, Optional
import os
import time
from functools import lru_cache

class OpenAIHumanizer:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        self.temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.9'))
        
    @lru_cache(maxsize=1000)
    def _get_cached_prompt(self, text_hash: str) -> Optional[str]:
        """Cache common transformations"""
        return None
    
    async def restructure(self, text: str, aggressive: bool = False) -> Dict:
        """Async OpenAI restructuring with NaturalWrite patterns"""
        start_time = time.time()
        
        # Check cache first
        text_hash = hash(text[:100])  # Hash first 100 chars
        cached = self._get_cached_prompt(text_hash)
        if cached:
            return {
                'text': cached,
                'processing_time': 0.001,
                'from_cache': True
            }
        
        prompt = self._build_prompt(text, aggressive)
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=int(len(text) * 1.5),
                timeout=5.0  # 5 second timeout
            )
            
            restructured = response.choices[0].message.content
            processing_time = time.time() - start_time
            
            return {
                'text': restructured,
                'processing_time': processing_time,
                'from_cache': False,
                'model_used': self.model
            }
            
        except asyncio.TimeoutError:
            return {
                'text': text,
                'processing_time': 5.0,
                'error': 'OpenAI timeout'
            }
        except Exception as e:
            return {
                'text': text,
                'processing_time': time.time() - start_time,
                'error': str(e)
            }
    
    def _get_system_prompt(self) -> str:
        return """You are rewriting text to match natural human writing patterns. Based on extensive research comparing AI and human writing:

CRITICAL PATTERNS TO APPLY:

1. OPENING TRANSFORMATIONS (Most Important):
   - "X impacts are becoming" → "The world shows increasing signs of X which"
   - "The Y of Z is" → "Z requires Y because it"
   - Never start with the original subject

2. STRUCTURAL CHANGES:
   - Break logical flow with "which" clauses
   - Mix sentence lengths dramatically
   - Add conversational interruptions

3. WORD-LEVEL CHANGES:
   - "and" → "together with", "as well as"
   - "individuals" → "people"
   - Scramble word order: "provides benefits" → "benefits come from"

4. HUMAN IMPERFECTIONS:
   - Slightly awkward but clear constructions
   - Mix formal and casual vocabulary
   - Add redundant clarifications

GOAL: Make it sound like someone wrote this quickly without editing, maintaining meaning but breaking AI patterns."""

    def _build_prompt(self, text: str, aggressive: bool) -> str:
        if aggressive:
            return f"""Completely restructure this text using ALL these techniques:

1. MANDATORY: Change the opening completely (don't start with the subject)
2. Add 2-3 "which" clauses that interrupt ideas
3. Replace every "and" with different conjunctions
4. Scramble at least 2 word orders
5. Make 1-2 sentences slightly awkward but understandable
6. Mix formal words with casual expressions

Original: {text}

Rewrite applying ALL changes. The opening MUST be completely different."""
        else:
            return f"""Lightly restructure for human-like writing:

1. Change just the opening phrase
2. Add one "which" clause
3. Use "together with" or "as well as" once
4. Keep the overall meaning intact

Original: {text}

Apply these specific changes naturally.""" 