# FastAPI AI Text Humanizer

Advanced text humanization API using hybrid regex patterns + OpenAI integration to achieve 0% AI detection rates.

## Features

- **3 Processing Modes**:
  - `fast`: Regex patterns only (~5ms)
  - `balanced`: Regex + selective OpenAI (~50ms) 
  - `aggressive`: Full OpenAI restructuring (~200ms)

- **NaturalWrite-Style Patterns**:
  - Opening sentence transformations
  - Word order scrambling
  - Strategic "which" clause insertion
  - Conjunction sophistication

- **Async Performance**: Parallel processing with FastAPI
- **Batch Processing**: Handle multiple texts simultaneously
- **AI Detection Estimation**: Built-in scoring system

## Quick Start

### Local Development

```bash
# Clone and setup
cd humanizer-fastapi
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="sk-..."

# Run development server
uvicorn app.main:app --reload

# Access API docs at http://localhost:8000/docs
```

### Render.com Deployment

```bash
# 1. Push your code to GitHub
git add .
git commit -m "Add FastAPI humanizer"
git push origin main

# 2. Connect to Render.com
# - Go to https://render.com and sign in with GitHub
# - Click "New+" → "Web Service"
# - Connect your repository
# - Select the humanizer-fastapi directory as the root

# 3. Render will automatically detect render.yaml and deploy
```

**Environment Variables to Set in Render Dashboard:**
- `OPENAI_API_KEY`: Your OpenAI API key (sk-...)
- `OPENAI_MODEL`: gpt-3.5-turbo (default)
- `OPENAI_TEMPERATURE`: 0.9 (default)
- `ENVIRONMENT`: production (default)

**After Deployment:**
- Your API will be available at: `https://your-app-name.onrender.com`
- Health check: `https://your-app-name.onrender.com/health`
- API docs: `https://your-app-name.onrender.com/docs`

## API Usage

### Single Text Humanization

```bash
curl -X POST "http://localhost:8000/humanize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Climate change impacts are becoming more evident in our world.",
    "mode": "balanced",
    "target_detection_rate": 20.0
  }'
```

### Batch Processing

```bash
curl -X POST "http://localhost:8000/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Companies are increasingly facing challenges.",
      "Research suggests new findings."
    ],
    "mode": "fast",
    "parallel_processing": true
  }'
```

### Text Analysis

```bash
curl -X POST "http://localhost:8000/analyze?text=Research%20demonstrates%20significant%20findings"
```

## Performance Targets

| Mode | Processing Time | AI Detection | Cost/1000 requests |
|------|----------------|--------------|-------------------|
| Fast | ~5ms | 60-80% | $0.01 |
| Balanced | ~50ms | 10-30% | $0.10 |
| Aggressive | ~200ms | 0-10% | $0.50 |

## Testing

```bash
# Run tests
pytest tests/

# Test specific endpoint
curl http://localhost:8000/test
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: Model to use (default: gpt-3.5-turbo)
- `OPENAI_TEMPERATURE`: Generation temperature (default: 0.9)
- `ENVIRONMENT`: production/development

## Integration with Existing Systems

### Next.js Integration

For your `sound-real` Next.js app, copy the code from `nextjs-integration-example.ts` to `app/api/humanize/route.ts`:

```typescript
// Replace your existing Flask API call with:
const FASTAPI_BASE_URL = process.env.FASTAPI_HUMANIZER_URL || 'https://your-app-name.onrender.com';

// In your API route:
const response = await fetch(`${FASTAPI_BASE_URL}/humanize`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text,
    mode: 'balanced', // fast | balanced | aggressive
    target_detection_rate: 20.0
  })
});
```

**Environment Variables for Next.js:**
Add to your `.env.local`:
```
FASTAPI_HUMANIZER_URL=https://your-render-app.onrender.com
```

### Python Integration

```python
import httpx

async def humanize_text(text: str, mode: str = "balanced"):
    # For local development
    # base_url = "http://localhost:8000"
    
    # For production (replace with your Render URL)
    base_url = "https://your-app-name.onrender.com"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/humanize",
            json={"text": text, "mode": mode}
        )
        return response.json()
```

## Monitoring

The API includes built-in health checks and can be monitored with:

- Health endpoint: `/health`
- Metrics: Prometheus-compatible (add `prometheus-fastapi-instrumentator`)
- Logging: Structured JSON logs

## Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   FastAPI App   │ -> │ Hybrid       │ -> │ OpenAI Client   │
│   (Endpoints)   │    │ Humanizer    │    │ (Async)         │
└─────────────────┘    └──────────────┘    └─────────────────┘
                              │
                              v
                       ┌──────────────┐
                       │ Advanced     │
                       │ Patterns     │
                       │ (Regex)      │
                       └──────────────┘
```

## License

MIT License - See LICENSE file for details. 