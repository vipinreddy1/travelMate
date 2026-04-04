'use client'

import { useState } from 'react'
import { BrainIcon } from './Icons'
import Image from 'next/image'
import { cn } from '@/lib/utils'

interface Trip {
  id: string
  destination: string
  country: string
  image: string
  date: string
  year: string
  status: 'Completed' | 'Ongoing'
  friendName?: string
  friendAvatar?: string
}

const mockTrips: Trip[] = [
  {
    id: '1',
    destination: 'Tokyo',
    country: 'Japan',
    image: 'https://images.unsplash.com/photo-1540959375944-7049f642e9d4?w=400&h=300&fit=crop',
    date: 'Oct 12 - Oct 22',
    year: '2024',
    status: 'Completed',
  },
  {
    id: '2',
    destination: 'Bali',
    country: 'Indonesia',
    image: 'https://images.unsplash.com/photo-1537225228614-b4fad34a2c4b?w=400&h=300&fit=crop',
    date: 'Jul 5 - Jul 15',
    year: '2023',
    status: 'Completed',
  },
  {
    id: '3',
    destination: 'Paris',
    country: 'France',
    image: 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400&h=300&fit=crop',
    date: 'May 1 - May 10',
    year: '2023',
    status: 'Completed',
  },
  {
    id: '4',
    destination: 'New York',
    country: 'USA',
    image: 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=400&h=300&fit=crop',
    date: 'Mar 15 - Mar 25',
    year: '2024',
    status: 'Completed',
    friendName: 'Sarah',
    friendAvatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah',
  },
]

export const RightPanel = () => {
  const [activeTab, setActiveTab] = useState<'my' | 'friends'>('my')

  const displayTrips = activeTab === 'my' ? mockTrips.slice(0, 3) : [mockTrips[3]]

  return (
    <div className="fixed right-0 top-0 h-screen w-[280px] bg-off-white border-l border-gray-100 flex flex-col overflow-hidden">
      {/* Header */}
      <div className="px-6 pt-6 pb-4 border-b border-gray-100">
        <div className="flex items-center gap-2 mb-4">
          <BrainIcon size={18} className="text-teal" />
          <h2 className="text-sm font-semibold text-text-primary">Trip Memory</h2>
        </div>

        {/* Tabs */}
        <div className="flex gap-2">
          {['my', 'friends'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab as 'my' | 'friends')}
              className={cn(
                'px-3 py-1.5 text-xs font-medium transition-colors rounded-md',
                activeTab === tab
                  ? 'bg-teal text-white'
                  : 'text-text-secondary hover:bg-white'
              )}
            >
              {tab === 'my' ? 'My Trips' : 'Friends'}
            </button>
          ))}
        </div>
      </div>

      {/* Trips List */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-3">
        {displayTrips.length ? (
          displayTrips.map((trip) => (
            <div
              key={trip.id}
              className="group cursor-pointer transition-all duration-300 hover:translate-y-[-2px]"
            >
              <div className="relative rounded-lg overflow-hidden h-40 mb-3 border border-gray-100 group-hover:border-teal group-hover:shadow-md transition-all duration-300">
                <Image
                  src={trip.image}
                  alt={trip.destination}
                  fill
                  className="object-cover group-hover:scale-105 transition-transform duration-300"
                  sizes="(max-width: 768px) 100vw, 280px"
                  unoptimized
                />
                {trip.friendName && (
                  <div className="absolute bottom-2 left-2">
                    <Image
                      src={trip.friendAvatar!}
                      alt={trip.friendName}
                      width={28}
                      height={28}
                      className="rounded-full border-2 border-white"
                      unoptimized
                    />
                  </div>
                )}
              </div>

              <h3 className="text-sm font-semibold text-text-primary group-hover:text-teal transition-colors">
                {trip.destination}
              </h3>
              <p className="text-xs text-text-muted mb-2">{trip.country}</p>

              <div className="flex items-center justify-between text-xs">
                <span className="text-text-muted">{trip.year}</span>
                <span
                  className={cn(
                    'px-2 py-0.5 rounded-full text-xs font-medium',
                    trip.status === 'Completed'
                      ? 'bg-success/10 text-success'
                      : 'bg-blue-100 text-blue-700'
                  )}
                >
                  {trip.status === 'Completed' ? '✓ Completed' : 'Ongoing'}
                </span>
              </div>
            </div>
          ))
        ) : (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <div className="mb-3 text-4xl">🗺️</div>
            <p className="text-xs text-text-muted">
              Your trip memories will appear here
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
