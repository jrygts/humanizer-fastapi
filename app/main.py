from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import time
from typing import Dict
import re

from .models import HumanizeRequest, HumanizeResponse, BatchHumanizeRequest, ProcessingMode
from .humanizer import HybridHumanizer

# Load environment variables
load_dotenv()

# Global humanizer instance
humanizer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global humanizer
    humanizer = HybridHumanizer()
    print("Humanizer initialized")
    yield
    # Shutdown
    print("Shutting down")

# Create FastAPI app
app = FastAPI(
    title="AI Text Humanizer API",
    description="Advanced text humanization using hybrid regex + OpenAI approach",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "AI Text Humanizer API v2.0",
        "endpoints": {
            "/humanize": "Single text humanization",
            "/batch": "Batch text processing",
            "/health": "Health check",
            "/test": "Test with sample text"
        }
    }

@app.post("/humanize", response_model=HumanizeResponse)
async def humanize_text(request: HumanizeRequest):
    """
    Humanize a single text with configurable processing mode.
    
    - **fast**: Regex patterns only (~5ms)
    - **balanced**: Regex + selective OpenAI (~50ms)
    - **aggressive**: Full OpenAI restructuring (~200ms)
    """
    try:
        result = await humanizer.humanize(request.text, request.mode)
        
        # Check if we met the target detection rate
        if result['ai_detection_estimate'] > request.target_detection_rate:
            # Log for analysis
            print(f"Warning: Detection rate {result['ai_detection_estimate']}% exceeds target {request.target_detection_rate}%")
        
        return HumanizeResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch")
async def batch_humanize(request: BatchHumanizeRequest):
    """
    Process multiple texts in parallel for maximum efficiency.
    """
    try:
        if request.parallel_processing:
            results = await humanizer.batch_humanize(request.texts, request.mode)
        else:
            # Sequential processing if requested
            results = []
            for text in request.texts:
                result = await humanizer.humanize(text, request.mode)
                results.append(result)
        
        return {
            "results": results,
            "total_texts": len(request.texts),
            "average_detection_rate": sum(r['ai_detection_estimate'] for r in results) / len(results)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
async def test_humanization():
    """
    Test the humanizer with sample texts from the research data.
    """
    test_texts = [
        "Climate change impacts are becoming more evident in our world, affecting ecosystems, weather patterns, and human health.",
        "The relationship between social media and mental health is a complex and multifaceted issue that warrants further examination.",
        "Companies are increasingly facing challenges such as supply chain disruptions due to extreme weather events."
    ]
    
    results = {}
    for mode in ProcessingMode:
        mode_results = []
        for text in test_texts:
            result = await humanizer.humanize(text, mode)
            mode_results.append({
                "original": text[:50] + "...",
                "humanized": result['humanized'][:50] + "...",
                "detection_rate": result['ai_detection_estimate'],
                "processing_ms": result['processing_time_ms']
            })
        results[mode.value] = mode_results
    
    return results

@app.get("/health")
async def health_check():
    """Check API health and OpenAI connectivity"""
    health_status = {
        "status": "healthy",
        "regex_engine": "operational",
        "openai_connected": False,
        "environment": os.getenv("ENVIRONMENT", "production")
    }
    
    # Test OpenAI connection
    if os.getenv("OPENAI_API_KEY"):
        try:
            test_result = await humanizer.openai.restructure("Test", aggressive=False)
            health_status["openai_connected"] = 'error' not in test_result
        except:
            health_status["openai_connected"] = False
    
    return health_status

@app.post("/analyze")
async def analyze_text(text: str):
    """
    Analyze text for AI detection indicators without modifying it.
    """
    detection_score = humanizer._estimate_ai_detection(text)
    needs_enhancement = humanizer._needs_openai_enhancement(text)
    
    return {
        "text": text,
        "ai_detection_estimate": detection_score,
        "needs_enhancement": needs_enhancement,
        "indicators": {
            "has_which_clauses": text.count("which") > 0,
            "varied_conjunctions": len(set(re.findall(r'\b(and|together with|as well as|while)\b', text))) > 1,
            "natural_opening": not re.match(r'^(The|An?|This|It) \w+ (is|are|was|were)', text),
            "sentence_variety": len(set([len(s.split()) for s in text.split('.')])) > 2
        }
    }

# Background task for logging
async def log_request(request_data: Dict):
    # Implement logging logic here
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 