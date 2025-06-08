#!/usr/bin/env python3
"""
Test FastAPI grammar fixes
"""

from app.humanizer import HybridHumanizer
import asyncio

async def test_fastapi_grammar():
    humanizer = HybridHumanizer()
    
    test_text = 'Persons has the ability while while working together with development.'
    print(f'Original: {test_text}')
    
    result = await humanizer.humanize(test_text, 'fast')
    print(f'Fixed: {result["humanized"]}')
    
    grammar_fixes = [c for c in result['changes_applied'] if 'Grammar fix' in c]
    print(f'Grammar fixes applied: {len(grammar_fixes)}')
    for fix in grammar_fixes:
        print(f'  - {fix}')

if __name__ == "__main__":
    asyncio.run(test_fastapi_grammar()) 