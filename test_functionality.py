import asyncio
from app.humanizer import HybridHumanizer
from app.models import ProcessingMode

async def test():
    print("🚀 Testing FastAPI Humanizer Functionality")
    print("=" * 50)
    
    humanizer = HybridHumanizer()
    
    # Test cases
    test_texts = [
        "Climate change impacts are becoming more evident in our world.",
        "The relationship between social media and mental health is a complex issue.",
        "Companies are increasingly facing challenges due to supply chain disruptions."
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n🔍 Test {i}:")
        print(f"Original: {text}")
        
        # Test FAST mode (regex only)
        result = await humanizer.humanize(text, ProcessingMode.FAST)
        
        print(f"Humanized: {result['humanized']}")
        print(f"Changes: {len(result['changes_applied'])} - {result['changes_applied'][:2]}")
        print(f"AI Detection: {result['ai_detection_estimate']:.1f}%")
        print(f"Processing: {result['processing_time_ms']:.2f}ms")
        print(f"Method: {result['method_used']}")

if __name__ == "__main__":
    asyncio.run(test()) 