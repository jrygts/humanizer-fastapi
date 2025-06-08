"""
Integration Example: Using FastAPI Humanizer with Next.js App

This example shows how to integrate the new FastAPI humanizer 
with your existing sound-real Next.js application.
"""

import httpx
import asyncio
from typing import Dict, List

class FastAPIHumanizerClient:
    """Client for the FastAPI humanizer service"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        
    async def humanize_text(self, text: str, mode: str = "balanced") -> Dict:
        """Humanize a single text"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/humanize",
                json={
                    "text": text,
                    "mode": mode,
                    "target_detection_rate": 20.0
                },
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
    
    async def batch_humanize(self, texts: List[str], mode: str = "balanced") -> Dict:
        """Humanize multiple texts in parallel"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/batch",
                json={
                    "texts": texts,
                    "mode": mode,
                    "parallel_processing": True
                },
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def analyze_text(self, text: str) -> Dict:
        """Analyze text for AI detection indicators"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/analyze",
                params={"text": text},
                timeout=5.0
            )
            response.raise_for_status()
            return response.json()

# Example usage for your Next.js API routes
async def api_route_example():
    """Example of how to use in your Next.js API routes"""
    
    humanizer = FastAPIHumanizerClient("http://localhost:8000")
    
    # Single text processing (for /api/humanize endpoint)
    user_text = "The effectiveness of artificial intelligence in modern applications is becoming increasingly evident."
    
    try:
        # Use balanced mode for good performance/quality tradeoff
        result = await humanizer.humanize_text(user_text, mode="balanced")
        
        print("✅ Humanization Result:")
        print(f"Original: {result['original']}")
        print(f"Humanized: {result['humanized']}")
        print(f"AI Detection: {result['ai_detection_estimate']}%")
        print(f"Processing Time: {result['processing_time_ms']}ms")
        print(f"Method: {result['method_used']}")
        print(f"Changes: {len(result['changes_applied'])}")
        
        return {
            "success": True,
            "humanized_text": result['humanized'],
            "processing_time": result['processing_time_ms'],
            "ai_detection_rate": result['ai_detection_estimate']
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "success": False,
            "error": str(e)
        }

# Example for batch processing
async def batch_processing_example():
    """Example of batch processing for efficiency"""
    
    humanizer = FastAPIHumanizerClient("http://localhost:8000")
    
    texts = [
        "Climate change impacts are becoming more evident globally.",
        "The relationship between technology and productivity is complex.",
        "Companies are facing unprecedented challenges in the market."
    ]
    
    try:
        result = await humanizer.batch_humanize(texts, mode="fast")
        
        print("✅ Batch Processing Results:")
        print(f"Total texts: {result['total_texts']}")
        print(f"Average detection rate: {result['average_detection_rate']:.1f}%")
        
        for i, text_result in enumerate(result['results']):
            print(f"\nText {i+1}:")
            print(f"  Original: {text_result['original'][:50]}...")
            print(f"  Humanized: {text_result['humanized'][:50]}...")
            print(f"  Detection: {text_result['ai_detection_estimate']}%")
            print(f"  Time: {text_result['processing_time_ms']:.2f}ms")
        
        return result
        
    except Exception as e:
        print(f"❌ Batch Error: {e}")
        return None

# Migration from Flask to FastAPI
class MigrationHelper:
    """Helper for migrating from Flask humanizer to FastAPI"""
    
    @staticmethod
    async def migrate_flask_call(text: str) -> Dict:
        """
        Replace your existing Flask humanizer calls with this
        
        OLD Flask code:
            from humanizer import humanize_with_analysis
            result = humanize_with_analysis(text)
            
        NEW FastAPI code:
            result = await MigrationHelper.migrate_flask_call(text)
        """
        humanizer = FastAPIHumanizerClient()
        
        # Map to similar functionality as Flask version
        fastapi_result = await humanizer.humanize_text(text, mode="balanced")
        
        # Convert to Flask-like response format
        return {
            "humanized_text": fastapi_result["humanized"],
            "changes_made": fastapi_result["changes_applied"],
            "stats": {
                "processing_time": fastapi_result["processing_time_ms"],
                "total_changes": len(fastapi_result["changes_applied"]),
                "ai_detection_estimate": fastapi_result["ai_detection_estimate"]
            },
            "original_length": len(fastapi_result["original"]),
            "humanized_length": len(fastapi_result["humanized"]),
            "change_percentage": fastapi_result["word_count_change"]
        }

# Performance comparison
async def performance_comparison():
    """Compare different processing modes"""
    
    humanizer = FastAPIHumanizerClient()
    test_text = "The analysis demonstrates that artificial intelligence technologies are revolutionizing multiple industries through innovative applications and sophisticated algorithms."
    
    modes = ["fast", "balanced", "aggressive"]
    results = {}
    
    for mode in modes:
        try:
            result = await humanizer.humanize_text(test_text, mode=mode)
            results[mode] = {
                "processing_time": result["processing_time_ms"],
                "ai_detection": result["ai_detection_estimate"],
                "method": result["method_used"],
                "changes": len(result["changes_applied"])
            }
            print(f"🚀 {mode.upper()} mode: {result['processing_time_ms']:.2f}ms, {result['ai_detection_estimate']:.1f}% detection")
        except Exception as e:
            print(f"❌ {mode} mode error: {e}")
    
    return results

if __name__ == "__main__":
    print("🧪 FastAPI Humanizer Integration Examples")
    print("=" * 50)
    
    # Run examples
    asyncio.run(api_route_example())
    print("\n" + "="*50)
    asyncio.run(batch_processing_example())
    print("\n" + "="*50)
    asyncio.run(performance_comparison()) 