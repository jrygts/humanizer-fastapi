// app/api/humanize/route.ts
// Minimal Next.js API Route that forwards requests to FastAPI on Render.com

import { NextRequest, NextResponse } from 'next/server';

const FASTAPI_BASE_URL = process.env.FASTAPI_HUMANIZER_URL || 'https://your-app-name.onrender.com';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Forward request to FastAPI
    const response = await fetch(`${FASTAPI_BASE_URL}/humanize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    const result = await response.json();
    
    // Propagate status code and response
    return NextResponse.json(result, { status: response.status });
    
  } catch (error) {
    return NextResponse.json(
      { error: 'FastAPI service unavailable' },
      { status: 503 }
    );
  }
}

/*
Environment Variables (.env.local):
FASTAPI_HUMANIZER_URL=https://your-render-app.onrender.com

Usage:
```javascript
const response = await fetch('/api/humanize', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: "Your text here",
    mode: "balanced"
  })
});
```
*/ 