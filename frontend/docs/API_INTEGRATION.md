# TripMind Frontend — API Integration & Services Guide

## Overview

This guide covers integrating external APIs and services with the TripMind frontend. Currently, the app uses **mock data**. This document outlines how to connect real services.

---

## Current Architecture

```
┌─────────────────────────────────────────────────────┐
│          REACT COMPONENTS (UI Layer)                 │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│      ZUSTAND STORE (State Management)                │
│  - Preferences, Messages, Itinerary, UI State       │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│    FUTURE: API SERVICE LAYER (To Build)             │
│  - Backend integration                              │
│  - ElevenLabs integration                           │
│  - Google Maps integration                          │
│  - Auth0 integration                                │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│           EXTERNAL APIs & Services                   │
└─────────────────────────────────────────────────────┘
```

---

## Backend API Integration

### Environment Configuration

**File**: `.env.local`

```env
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1

# For production
# NEXT_PUBLIC_API_URL=https://api.tripMind.com
```

### Creating API Service Layer

**Location**: `lib/api.ts` (create new file)

```typescript
// lib/api.ts

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = {
  // Trip Planning
  async generateItinerary(preferences: any) {
    const response = await fetch(`${API_URL}/api/v1/itinerary/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAuthToken()}`
      },
      body: JSON.stringify(preferences)
    })
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }
    
    return response.json()
  },

  // User Preferences
  async updatePreferences(userId: string, preferences: any) {
    const response = await fetch(`${API_URL}/api/v1/users/${userId}/preferences`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAuthToken()}`
      },
      body: JSON.stringify(preferences)
    })
    
    return response.json()
  },

  // Messages/Chat
  async sendMessage(message: string) {
    const response = await fetch(`${API_URL}/api/v1/chat/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAuthToken()}`
      },
      body: JSON.stringify({ content: message })
    })
    
    return response.json()
  },

  // Trip History
  async getTrips(userId: string) {
    const response = await fetch(`${API_URL}/api/v1/users/${userId}/trips`, {
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`
      }
    })
    
    return response.json()
  }
}

function getAuthToken() {
  // Future: Get token from Auth0 session or localStorage
  return localStorage.getItem('authToken') || ''
}
```

### Backend Endpoints (To Implement)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/itinerary/generate` | Generate itinerary from preferences |
| PUT | `/api/v1/users/:id/preferences` | Update user preferences |
| POST | `/api/v1/chat/messages` | Send message to AI |
| GET | `/api/v1/users/:id/trips` | Fetch user's trips |
| POST | `/api/v1/auth/signin` | Login user |
| POST | `/api/v1/auth/logout` | Logout user |

---

## ElevenLabs Voice Integration

### Setup

1. **Get API Key**
   - Visit https://elevenlabs.io
   - Sign up for account
   - Copy API key

2. **Add to `.env.local`**
   ```env
   NEXT_PUBLIC_ELEVENLABS_API_KEY=sk_...
   ```

### Voice Service

**Location**: `lib/voice.ts` (create new file)

```typescript
// lib/voice.ts

import { ElevenLabsClient } from "elevenlabs"

const client = new ElevenLabsClient({
  apiKey: process.env.NEXT_PUBLIC_ELEVENLABS_API_KEY
})

export const voice = {
  // Text to Speech
  async textToSpeech(text: string) {
    try {
      const audio = await client.generate({
        voice: "Bella",  // Voice name
        text: text,
        model_id: "eleven_monolingual_v1"
      })
      
      return audio
    } catch (error) {
      console.error('Text-to-speech error:', error)
      throw error
    }
  },

  // Speech to Text
  async speechToText(audioBlob: Blob) {
    try {
      const formData = new FormData()
      formData.append('audio', audioBlob)
      
      const response = await fetch('https://api.elevenlabs.io/v1/speech-to-text', {
        method: 'POST',
        headers: {
          'xi-api-key': process.env.NEXT_PUBLIC_ELEVENLABS_API_KEY || ''
        },
        body: formData
      })
      
      return response.json()
    } catch (error) {
      console.error('Speech-to-text error:', error)
      throw error
    }
  },

  // Play audio
  async playAudio(audioStream: ReadableStream<Uint8Array>) {
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
    
    const response = new Response(audioStream)
    const arrayBuffer = await response.arrayBuffer()
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer)
    
    const source = audioContext.createBufferSource()
    source.buffer = audioBuffer
    source.connect(audioContext.destination)
    source.start()
  }
}
```

### Using Voice in Components

```typescript
// In CenterPanel.tsx

import { voice } from '@/lib/voice'

export const CenterPanel = () => {
  const [isRecording, setIsRecording] = useState(false)

  const handleMicClick = async () => {
    if (!isRecording) {
      // Start recording
      const mediaRecorder = new MediaRecorder(await navigator.mediaDevices.getUserMedia({ audio: true }))
      setIsRecording(true)

      mediaRecorder.ondataavailable = async (event) => {
        const audioBlob = event.data
        
        // Convert speech to text
        const result = await voice.speechToText(audioBlob)
        
        // Add as user message
        addMessage({
          role: 'user',
          content: result.text,
          timestamp: new Date()
        })
        
        // Get AI response
        const response = await getAIResponse(result.text)
        
        // Play audio response
        await voice.textToSpeech(response.text)
      }

      mediaRecorder.start()
    } else {
      // Stop recording
      setIsRecording(false)
    }
  }

  return (
    // ... rest of component with mic button handler
  )
}
```

---

## Google Maps Integration

### Setup

1. **Get API Key**
   - Visit https://cloud.google.com
   - Create project
   - Enable Maps API
   - Generate API key

2. **Add to `.env.local`**
   ```env
   NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=AIza...
   ```

### Maps Service

**Location**: `lib/maps.ts` (create new file)

```typescript
// lib/maps.ts

export const maps = {
  // Geocode location name to coordinates
  async getCoordinates(locationName: string) {
    const response = await fetch(
      `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(locationName)}&key=${process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY}`
    )
    
    const data = await response.json()
    return data.results[0]?.geometry.location
  },

  // Get place details
  async getPlaceDetails(placeId: string) {
    const response = await fetch(
      `https://maps.googleapis.com/maps/api/place/details/json?place_id=${placeId}&key=${process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY}`
    )
    
    return response.json()
  },

  // Search nearby places
  async searchNearby(lat: number, lng: number, type: string) {
    const response = await fetch(
      `https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=${lat},${lng}&type=${type}&key=${process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY}`
    )
    
    return response.json()
  }
}
```

### Embedding Map in Components

```typescript
// In ItineraryCard.tsx

import { useEffect } from 'react'

export const ItineraryCard = ({ itinerary }: Props) => {
  useEffect(() => {
    // Load Google Maps API
    const script = document.createElement('script')
    script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY}`
    document.head.appendChild(script)

    script.onload = () => {
      // Initialize map
      const map = new window.google.maps.Map(document.getElementById('map'), {
        zoom: 12,
        center: { lat: 35.6762, lng: 139.6503 } // Tokyo coordinates
      })

      // Add markers for activities
      itinerary.days.forEach(day => {
        day.activities.forEach(activity => {
          new window.google.maps.Marker({
            position: activity.coordinates,
            map: map,
            title: activity.name
          })
        })
      })
    }
  }, [itinerary])

  return (
    <div>
      {/* ... existing itinerary UI ... */}
      <div id="map" style={{ width: '100%', height: '400px' }} />
    </div>
  )
}
```

---

## Auth0 Integration

### Setup

1. **Create Auth0 Account**
   - Visit https://auth0.com
   - Create tenant
   - Create application

2. **Install SDK**
   ```bash
   npm install @auth0/nextjs-auth0
   ```

3. **Add to `.env.local`**
   ```env
   AUTH0_SECRET=your-secret
   AUTH0_BASE_URL=http://localhost:3000
   AUTH0_ISSUER_BASE_URL=https://your-tenant.auth0.com
   AUTH0_CLIENT_ID=your-client-id
   AUTH0_CLIENT_SECRET=your-client-secret
   ```

### Setup Auth Routes

**File**: `app/api/auth/[auth0]/route.ts`

```typescript
// app/api/auth/[auth0]/route.ts

import { handleAuth } from '@auth0/nextjs-auth0'

export const GET = handleAuth()
```

### Login/Logout Buttons

```typescript
// In LeftPanel.tsx

import Link from 'next/link'
import { useUser } from '@auth0/nextjs-auth0/client'

export const LeftPanel = () => {
  const { user, isLoading } = useUser()

  if (isLoading) return <div>Loading...</div>

  return (
    <nav>
      {/* ... existing preferences UI ... */}
      
      {user ? (
        <>
          <p>Welcome, {user.name}!</p>
          <Link href="/api/auth/logout">Logout</Link>
        </>
      ) : (
        <Link href="/api/auth/login">Login</Link>
      )}
    </nav>
  )
}
```

---

## Error Handling & Retries

### Retry Logic

**Location**: `lib/api-client.ts`

```typescript
// lib/api-client.ts

export async function fetchWithRetry(
  url: string,
  options: RequestInit = {},
  maxRetries: number = 3
) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch(url, options)
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      
      return response
    } catch (error) {
      console.warn(`Attempt ${i + 1} failed:`, error)
      
      if (i === maxRetries - 1) {
        throw error
      }
      
      // Exponential backoff
      await new Promise(resolve => 
        setTimeout(resolve, Math.pow(2, i) * 1000)
      )
    }
  }
}
```

### Error Boundary

**Location**: `components/ErrorBoundary.tsx`

```typescript
// components/ErrorBoundary.tsx

import React from 'react'

interface Props {
  children: React.ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-6 bg-error-light rounded-lg border border-error">
          <h2 className="text-error font-semibold mb-2">Something went wrong</h2>
          <p className="text-sm text-text-secondary">{this.state.error?.message}</p>
          <button 
            onClick={() => window.location.reload()}
            className="mt-4 px-4 py-2 bg-error text-white rounded-md"
          >
            Reload Page
          </button>
        </div>
      )
    }

    return this.props.children
  }
}
```

---

## Real-Time Client (Future)

### WebSocket Integration

```typescript
// lib/websocket.ts

let socket: WebSocket

export function initializeWebSocket(userId: string) {
  socket = new WebSocket(`wss://api.tripMind.com/ws/${userId}`)

  socket.onopen = () => {
    console.log('WebSocket connected')
  }

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data)
    handleWebSocketMessage(data)
  }

  socket.onerror = (error) => {
    console.error('WebSocket error:', error)
  }
}

export function sendWebSocketMessage(data: any) {
  socket.send(JSON.stringify(data))
}

function handleWebSocketMessage(data: any) {
  // Route message to appropriate handler
  switch (data.type) {
    case 'ai-response':
      useAppStore.setState(state => ({
        messages: [...state.messages, data.message]
      }))
      break
    case 'itinerary-generated':
      useAppStore.setState({ itinerary: data.itinerary })
      break
  }
}
```

---

## Testing API Integration

### Mock API Responses

**Location**: `lib/__mocks__/api.ts`

```typescript
// lib/__mocks__/api.ts

export const mockItinerary = {
  destination: 'Tokyo',
  country: 'Japan',
  startDate: '2024-10-12',
  endDate: '2024-10-22',
  // ... full itinerary object
}

export const api = {
  generateItinerary: jest.fn().mockResolvedValue(mockItinerary),
  updatePreferences: jest.fn().mockResolvedValue({ success: true }),
  sendMessage: jest.fn().mockResolvedValue({ message: 'AI response' })
}
```

### Testing API Calls

```typescript
// __tests__/api.test.ts

import { api } from '@/lib/api'

describe('API Integration', () => {
  it('should generate itinerary', async () => {
    const itinerary = await api.generateItinerary({
      destination: 'Tokyo',
      budget: '$$ (Mid-range)'
    })

    expect(itinerary.destination).toBe('Tokyo')
    expect(itinerary.days).toBeDefined()
  })
})
```

---

## Rate Limiting & Throttling

```typescript
// lib/rate-limiter.ts

export class RateLimiter {
  private calls: number[] = []
  private maxCalls: number
  private timeWindow: number

  constructor(maxCalls: number, timeWindow: number) {
    this.maxCalls = maxCalls
    this.timeWindow = timeWindow
  }

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    const now = Date.now()
    this.calls = this.calls.filter(time => now - time < this.timeWindow)

    if (this.calls.length >= this.maxCalls) {
      await new Promise(resolve => 
        setTimeout(resolve, this.timeWindow - (now - this.calls[0]))
      )
    }

    this.calls.push(now)
    return fn()
  }
}

// Usage
const limiter = new RateLimiter(10, 60000) // 10 requests per minute

await limiter.execute(() => api.generateItinerary(preferences))
```

---

## Monitoring & Analytics

### Track API Calls

```typescript
// lib/analytics.ts

export function trackAPICall(endpoint: string, status: number, duration: number) {
  const event = {
    type: 'api_call',
    endpoint,
    status,
    duration,
    timestamp: new Date().toISOString()
  }

  // Send to analytics service
  fetch('/api/analytics', {
    method: 'POST',
    body: JSON.stringify(event)
  })
}
```

---

## Security Best Practices

1. ✅ **Never expose API keys in client code**
   - Use `.env.local` with NEXT_PUBLIC_ prefix only for public keys
   - Sensitive keys go in .env without prefix (server-side only)

2. ✅ **Validate inputs on backend**
   - Never trust client data

3. ✅ **Use CORS properly**
   - Restrict origins in backend

4. ✅ **Implement rate limiting**
   - Prevent abuse and DDoS attacks

5. ✅ **Use HTTPS in production**
   - Always encrypted communication

6. ❌ **Don't store tokens in localStorage**
   - Use httpOnly cookies instead

---

## Summary

This integration guide provides templates and patterns for connecting:
- Backend API
- ElevenLabs voice services
- Google Maps
- Auth0 authentication

Start by implementing the API service layer, then progressively add other integrations. Mock data ensures the UI works while services are being built.

