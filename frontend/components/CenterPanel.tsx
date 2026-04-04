'use client'

import { useState, useRef, useEffect } from 'react'
import Image from 'next/image'
import { useAppStore } from '@/store/appStore'
import { CompassIcon, MicIcon, SendIcon, UserIcon } from './Icons'
import { ItineraryCard } from './ItineraryCard'
import { cn } from '@/lib/utils'

export const CenterPanel = () => {
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const messages = useAppStore((state) => state.messages)
  const itinerary = useAppStore((state) => state.itinerary)
  const addMessage = useAppStore((state) => state.addMessage)
  const setTypingStatus = useAppStore((state) => state.setTypingStatus)
  const isRecording = useAppStore((state) => state.isRecording)
  const setRecording = useAppStore((state) => state.setRecording)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Mock initial message
  useEffect(() => {
    if (messages.length === 0) {
      addMessage({
        role: 'agent',
        content:
          "Hello! 👋 I'm your digital curator. I've been looking at your preference for slow exploration and boutique stays. Are you thinking about Tokyo for your next solo retreat? I can help you plan something special based on your memories.",
        timestamp: new Date(),
      })
    }
  }, [])

  const handleSendMessage = async () => {
    if (!input.trim()) return

    // Add user message
    addMessage({
      role: 'user',
      content: input,
      timestamp: new Date(),
    })

    setInput('')
    setIsLoading(true)
    setTypingStatus(true)

    // Simulate agent response
    setTimeout(() => {
      setTypingStatus(false)

      // Mock response with itinerary generation
      addMessage({
        role: 'agent',
        content:
          "Perfect! I've crafted a 3-day itinerary for you focusing on quiet neighborhoods and boutique experiences. Here's what I found based on your preferences and your past visits.",
        timestamp: new Date(),
      })

      // Generate mock itinerary
      if (!itinerary) {
        useAppStore.setState({
          itinerary: {
            destination: 'Tokyo',
            country: 'Japan',
            startDate: '2024-10-12',
            endDate: '2024-10-22',
            flights: {
              airline: 'ANA Airways',
              departure: 'SFO',
              arrival: 'NRT',
              price: 680,
              date: '2024-10-12',
            },
            hotel: {
              name: 'The Hoshinoya Tokyo',
              rating: 5,
              price: 450,
              image:
                'https://images.unsplash.com/photo-1631049307038-da0ec9d70304?w=400&h=300&fit=crop',
            },
            days: [
              {
                dayNumber: 1,
                date: '2024-10-12',
                activities: [
                  {
                    time: '14:00',
                    name: 'Arrival at Narita',
                    location: 'Tokyo Airport',
                    description: 'Check in and settle into your ryokan',
                  },
                  {
                    time: '18:00',
                    name: 'Dinner at Local Izakaya',
                    location: 'Shibuya',
                    description: 'Traditional Japanese dinner',
                  },
                ],
              },
              {
                dayNumber: 2,
                date: '2024-10-13',
                activities: [
                  {
                    time: '08:00',
                    name: 'Tsukiji Market Walk',
                    location: 'Tsukiji',
                    description: 'Fresh sushi breakfast at the market',
                  },
                  {
                    time: '11:00',
                    name: 'Meiji Jingu Shrine',
                    location: 'Meiji',
                    description: 'Peaceful forest temple',
                  },
                  {
                    time: '14:00',
                    name: 'Matcha at Traditional Tea House',
                    location: 'Omotesando',
                    description: 'Authentic tea ceremony experience',
                  },
                ],
              },
              {
                dayNumber: 3,
                date: '2024-10-14',
                activities: [
                  {
                    time: '09:00',
                    name: 'Imperial Palace East Gardens',
                    location: 'Chiyoda',
                    description: 'Serene morning walk',
                  },
                  {
                    time: '13:00',
                    name: 'Lunch at Vegetarian Restaurant',
                    location: 'Shinjuku',
                    description: 'Plant-based Japanese cuisine',
                  },
                  {
                    time: '16:00',
                    name: 'Shopping at Vintage Stores',
                    location: 'Harajuku',
                    description: 'Unique local boutiques',
                  },
                ],
              },
            ],
            heroImage:
              'https://images.unsplash.com/photo-1540959375944-7049f642e9d4?w=1200&h=600&fit=crop',
          },
        })
      }

      setIsLoading(false)
    }, 2000)
  }

  const handleMicToggle = () => {
    setRecording(!isRecording)
    // In production, this would connect to ElevenLabs STT
  }

  return (
    <div className="fixed left-[220px] right-[280px] top-0 h-screen bg-gradient-to-b from-cream to-warm-white flex flex-col overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-100 bg-white/50 backdrop-blur-sm flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-gradient-to-br from-teal to-ocean rounded-lg flex items-center justify-center">
            <CompassIcon size={18} className="text-white" />
          </div>
          <h1 className="text-lg font-bold text-text-primary">TripMind</h1>
        </div>

        <div className="flex items-center gap-4">
          <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
            <UserIcon size={20} className="text-text-primary" />
          </button>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={cn(
              'flex gap-3 message-enter',
              message.role === 'user' && 'justify-end'
            )}
          >
            {message.role === 'agent' && (
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-teal to-ocean flex-shrink-0 flex items-center justify-center">
                <CompassIcon size={16} className="text-white" />
              </div>
            )}

            <div
              className={cn(
                'max-w-md rounded-lg px-4 py-3 transition-all duration-300',
                message.role === 'user'
                  ? 'bg-teal text-white rounded-br-sm'
                  : 'bg-white text-text-primary rounded-bl-sm border border-gray-100 shadow-sm'
              )}
            >
              {message.isTyping ? (
                <div className="typing-dots">
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                </div>
              ) : (
                <p className="text-sm leading-relaxed">{message.content}</p>
              )}
            </div>
          </div>
        ))}

        {/* Itinerary Card */}
        {itinerary && (
          <div className="mt-6 mb-4">
            <ItineraryCard itinerary={itinerary} />
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="px-6 py-4 bg-white border-t border-gray-100">
        <div className="flex items-center gap-3 bg-warm-white rounded-full px-4 py-3 border border-gray-100 focus-within:border-teal focus-within:shadow-md transition-all duration-300">
          <button
            onClick={handleMicToggle}
            className={cn(
              'p-2 rounded-full transition-all duration-300 flex-shrink-0',
              isRecording
                ? 'bg-teal/20 text-teal'
                : 'text-text-muted hover:text-teal'
            )}
          >
            <MicIcon size={20} isActive={isRecording} />
          </button>

          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Where do you want to go?"
            className="flex-1 bg-transparent outline-none text-sm placeholder-text-muted"
          />

          <button
            onClick={handleSendMessage}
            disabled={!input.trim() || isLoading}
            className="p-2 text-teal hover:bg-teal/10 rounded-full transition-colors flex-shrink-0 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <SendIcon size={20} />
          </button>
        </div>

        <p className="text-xs text-text-muted text-center mt-3">
          ✨ Your preferences update in realtime as you chat
        </p>
      </div>
    </div>
  )
}
