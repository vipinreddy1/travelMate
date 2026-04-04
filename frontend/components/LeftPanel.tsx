'use client'

import { useAppStore } from '@/store/appStore'
import { SparkleIcon } from './Icons'
import { cn } from '@/lib/utils'

export const LeftPanel = () => {
  const preferences = useAppStore((state) => state.preferences)

  return (
    <div className="fixed left-0 top-0 h-screen w-[220px] bg-off-white border-r border-gray-100 p-6 flex flex-col overflow-y-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-1">
          <SparkleIcon size={16} />
          <h2 className="text-sm font-semibold text-text-primary tracking-tight">
            Your Travel DNA
          </h2>
        </div>
        <p className="text-xs text-text-muted mt-2">
          Your AI learns your style as we chat
        </p>
      </div>

      {/* Preferences */}
      <div className="space-y-3 flex-1">
        {preferences.map((pref) => (
          <div
            key={pref.key}
            className={cn(
              'px-3 py-2 rounded-full bg-white border border-gray-100 flex items-center gap-2 text-sm transition-all duration-300',
              pref.updated && 'pref-update border-teal ring-2 ring-teal/10'
            )}
          >
            <span className="text-base leading-none">{pref.icon}</span>
            <div className="flex-1">
              <div className="text-xs text-text-muted">{pref.label}</div>
              <div className="text-xs font-medium text-text-primary truncate">
                {pref.value}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="pt-6 border-t border-gray-100">
        <div className="flex items-center gap-2 text-xs text-text-muted">
          <span className="w-2 h-2 rounded-full bg-teal-light pulse-soft"></span>
          <span>Updating as you chat...</span>
        </div>
      </div>
    </div>
  )
}
