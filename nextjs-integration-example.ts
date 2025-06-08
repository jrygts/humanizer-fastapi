// app/api/humanize/route.ts
// Next.js API Route Handler for calling FastAPI Humanizer on Render.com

import { NextRequest, NextResponse } from 'next/server';

// Replace with your actual Render.com URL
const FASTAPI_BASE_URL = process.env.FASTAPI_HUMANIZER_URL || 'https://your-app-name.onrender.com';

export async function POST(request: NextRequest) {
  try {
    // Parse the incoming request
    const body = await request.json();
    const { text, mode = 'balanced' } = body;

    // Validate input
    if (!text || typeof text !== 'string') {
      return NextResponse.json(
        { error: 'Text is required and must be a string' },
        { status: 400 }
      );
    }

    // Call FastAPI humanizer service
    const response = await fetch(`${FASTAPI_BASE_URL}/humanize`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text,
        mode, // fast | balanced | aggressive
        target_detection_rate: 20.0
      }),
    });

    if (!response.ok) {
      throw new Error(`FastAPI responded with status: ${response.status}`);
    }

    const result = await response.json();

    // Return the humanized result
    return NextResponse.json({
      success: true,
      original: result.original,
      humanized: result.humanized,
      ai_detection_estimate: result.ai_detection_estimate,
      processing_time_ms: result.processing_time_ms,
      method_used: result.method_used,
      changes_applied: result.changes_applied
    });

  } catch (error) {
    console.error('Humanizer API Error:', error);
    
    return NextResponse.json(
      { 
        success: false, 
        error: 'Failed to humanize text',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

// Optional: Health check endpoint
export async function GET() {
  try {
    const response = await fetch(`${FASTAPI_BASE_URL}/health`);
    const health = await response.json();
    
    return NextResponse.json({
      service: 'Next.js Humanizer Proxy',
      fastapi_health: health,
      status: response.ok ? 'healthy' : 'degraded'
    });
  } catch (error) {
    return NextResponse.json(
      { 
        service: 'Next.js Humanizer Proxy',
        status: 'unhealthy',
        error: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 503 }
    );
  }
}

/*
Environment Variables to Add to Your Next.js App:

In your .env.local:
FASTAPI_HUMANIZER_URL=https://your-app-name.onrender.com

Or in Vercel/production environment:
FASTAPI_HUMANIZER_URL=https://your-actual-render-app.onrender.com

Usage from your frontend:
```javascript
const response = await fetch('/api/humanize', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: "The effectiveness of AI is becoming evident.",
    mode: "balanced" // or "fast" or "aggressive"
  })
});

const result = await response.json();
if (result.success) {
  console.log('Original:', result.original);
  console.log('Humanized:', result.humanized);
  console.log('AI Detection:', result.ai_detection_estimate + '%');
}
```
*/ 