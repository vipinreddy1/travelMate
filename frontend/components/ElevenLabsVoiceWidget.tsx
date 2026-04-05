'use client'

import { useEffect } from 'react'
import React from 'react'

interface ElevenLabsVoiceWidgetProps {
  agentId: string
}

/**
 * ElevenLabs Voice Widget Component
 * 
 * Renders the ElevenLabs conversational AI voice agent widget
 * in an embedded container on the page.
 * 
 * Note: The widget requires the @elevenlabs/convai-widget-embed
 * script to be loaded globally (in app/layout.tsx or via next/script).
 * 
 * The custom HTML element <elevenlabs-convai> becomes available
 * once the script is loaded, enabling voice conversation capabilities.
 */
export default function ElevenLabsVoiceWidget({ agentId }: ElevenLabsVoiceWidgetProps) {
  useEffect(() => {
    // Ensure the widget script is available
    // This runs after the component mounts to handle dynamic loading
    if (typeof window !== 'undefined') {
      // The script should be loaded globally, but this ensures it's available
      // if the widget element exists but the script hasn't fully executed yet
      const checkAndLoadScript = () => {
        // @ts-ignore - elevenlabs-convai is a custom element defined by the script
        if (!customElements.get('elevenlabs-convai')) {
          // Script not yet loaded, the global script tag will handle it
          console.debug('Waiting for ElevenLabs widget script to load...')
        }
      }
      
      checkAndLoadScript()
    }
  }, [])

  return (
    <div className="py-8 px-6 border-t border-gray-100 bg-white">
      <div className="max-w-2xl mx-auto">
        {/* Widget Header */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-text-primary mb-2">Have questions about this trip?</h3>
          <p className="text-sm text-text-muted">
            Chat with our AI assistant to learn more about destinations, activities, and travel tips.
          </p>
        </div>

        {/* ElevenLabs Widget Container */}
        <div className="bg-gray-50 rounded-lg border border-gray-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow">
          {React.createElement('elevenlabs-convai', { 'agent-id': agentId })}
        </div>

        {/* Widget Info */}
        <p className="text-xs text-text-muted mt-4 text-center">
          Powered by TravelMate&apos;s AI assistant
        </p>
      </div>
    </div>
  )
}
