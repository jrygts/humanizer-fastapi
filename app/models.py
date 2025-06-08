from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from enum import Enum

class ProcessingMode(str, Enum):
    FAST = "fast"           # Regex only (~5ms)
    BALANCED = "balanced"   # Regex + selective OpenAI (~50ms)
    AGGRESSIVE = "aggressive" # Full restructuring (~200ms)

class HumanizeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)
    mode: ProcessingMode = ProcessingMode.BALANCED
    max_processing_time: Optional[int] = Field(500, description="Max time in ms")
    target_detection_rate: Optional[float] = Field(20.0, description="Target AI detection %")
    
    class Config:
        schema_extra = {
            "example": {
                "text": "Climate change impacts are becoming more evident in our world.",
                "mode": "balanced",
                "max_processing_time": 500,
                "target_detection_rate": 20.0
            }
        }

class HumanizeResponse(BaseModel):
    original: str
    humanized: str
    processing_time_ms: float
    ai_detection_estimate: float
    method_used: str
    changes_applied: List[str]
    word_count_change: int
    
class BatchHumanizeRequest(BaseModel):
    texts: List[str] = Field(..., min_items=1, max_items=100)
    mode: ProcessingMode = ProcessingMode.BALANCED
    parallel_processing: bool = True 