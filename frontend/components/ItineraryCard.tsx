'use client'

import { useState } from 'react'
import Image from 'next/image'
import { ChevronDownIcon, ArrowRightIcon, CalendarIcon, PlaneIcon, HotelIcon, MapPinIcon } from './Icons'
import { cn, formatDate } from '@/lib/utils'
import { Itinerary } from '@/store/appStore'

interface ItineraryCardProps {
  itinerary: Itinerary
}

export const ItineraryCard = ({ itinerary }: ItineraryCardProps) => {
  const [expandedDays, setExpandedDays] = useState<Set<number>>(new Set([1]))

  const toggleDayExpanded = (dayNumber: number) => {
    const newExpanded = new Set(expandedDays)
    if (newExpanded.has(dayNumber)) {
      newExpanded.delete(dayNumber)
    } else {
      newExpanded.add(dayNumber)
    }
    setExpandedDays(newExpanded)
  }

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-100 slide-up animate-fade-in max-w-2xl mx-auto">
      {/* Hero Image */}
      <div className="relative h-64 w-full overflow-hidden bg-gray-200">
        <Image
          src={itinerary.heroImage}
          alt={itinerary.destination}
          fill
          className="object-cover"
          priority
          unoptimized
        />
        <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black/50" />
        <div className="absolute bottom-6 left-6">
          <h2 className="text-3xl font-bold text-white mb-1">
            {itinerary.destination}
          </h2>
          <p className="text-sm text-gray-100">{itinerary.country}</p>
        </div>
      </div>

      {/* Trip Details */}
      <div className="p-6 bg-gradient-to-br from-gray-50 to-white border-b border-gray-100">
        <div className="grid grid-cols-2 gap-4 mb-6">
          {/* Flight Info */}
          <div className="bg-white rounded-lg p-4 border border-gray-100">
            <div className="flex items-center gap-2 mb-3">
              <PlaneIcon size={18} className="text-teal" />
              <span className="text-xs font-semibold text-text-muted uppercase tracking-wide">
                Flights
              </span>
            </div>
            <div className="mb-2">
              <div className="text-sm font-semibold text-text-primary mb-1">
                {itinerary.flights.airline}
              </div>
              <div className="flex items-center gap-2 text-xs text-text-muted mb-2">
                <span>{itinerary.flights.departure}</span>
                <ArrowRightIcon size={14} />
                <span>{itinerary.flights.arrival}</span>
              </div>
              <div className="text-lg font-bold text-teal">
                ${itinerary.flights.price}
              </div>
            </div>
            <div className="flex items-center gap-1 text-xs text-text-muted">
              <CalendarIcon size={14} />
              <span>{formatDate(itinerary.flights.date)}</span>
            </div>
          </div>

          {/* Hotel Info */}
          <div className="bg-white rounded-lg p-4 border border-gray-100">
            <div className="flex items-center gap-2 mb-3">
              <HotelIcon size={18} className="text-teal" />
              <span className="text-xs font-semibold text-text-muted uppercase tracking-wide">
                Hotel
              </span>
            </div>
            <div className="mb-2">
              <div className="text-sm font-semibold text-text-primary mb-1">
                {itinerary.hotel.name}
              </div>
              <div className="flex items-center gap-1 mb-2">
                {[...Array(itinerary.hotel.rating)].map((_, i) => (
                  <span key={i} className="text-sm">⭐</span>
                ))}
                <span className="text-xs text-text-muted">
                  ({itinerary.hotel.rating}/5)
                </span>
              </div>
              <div className="text-lg font-bold text-teal">
                ${itinerary.hotel.price}/night
              </div>
            </div>
          </div>
        </div>

        {/* Trip Duration */}
        <div className="text-center text-xs text-text-muted">
          <span>{formatDate(itinerary.startDate)}</span>
          <span className="mx-2">•</span>
          <span>{itinerary.days.length} days</span>
        </div>
      </div>

      {/* Day-by-Day Itinerary */}
      <div className="divide-y divide-gray-100">
        {itinerary.days.map((day) => (
          <div key={day.dayNumber} className="bg-white">
            <button
              onClick={() => toggleDayExpanded(day.dayNumber)}
              className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
            >
              <div className="text-left">
                <h3 className="text-sm font-semibold text-text-primary">
                  Day {day.dayNumber} — {formatDate(day.date)}
                </h3>
              </div>
              <ChevronDownIcon
                size={18}
                className={cn(
                  'text-text-muted transition-transform duration-300',
                  expandedDays.has(day.dayNumber) && 'rotate-180'
                )}
              />
            </button>

            {expandedDays.has(day.dayNumber) && (
              <div className="px-6 pb-4 bg-gray-50 space-y-3">
                {day.activities.map((activity, idx) => (
                  <div
                    key={idx}
                    className="flex gap-4 pb-3 last:pb-0 border-b border-white last:border-b-0"
                  >
                    <div className="text-right min-w-fit">
                      <span className="text-xs font-semibold text-teal">
                        {activity.time}
                      </span>
                    </div>
                    <div className="flex-1">
                      <h4 className="text-sm font-semibold text-text-primary mb-1">
                        {activity.name}
                      </h4>
                      <div className="flex items-center gap-1 mb-1">
                        <MapPinIcon size={14} className="text-text-muted" />
                        <span className="text-xs text-text-muted">
                          {activity.location}
                        </span>
                      </div>
                      {activity.description && (
                        <p className="text-xs text-text-muted italic">
                          {activity.description}
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* CTA */}
      <div className="p-6 bg-teal/5 border-t border-teal/10">
        <button className="w-full px-4 py-3 bg-teal text-white rounded-lg font-medium text-sm hover:bg-teal-light transition-colors">
          Save This Itinerary
        </button>
      </div>
    </div>
  )
}
