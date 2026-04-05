'use client'

import { useEffect } from 'react'
import { useAppStore } from '@/store/appStore'
import { SparkleIcon } from './Icons'
import { cn } from '@/lib/utils'

interface LeftPanelProps {
  userId: string
}

const getDisplayIcon = (key: string, label: string, icon: string) => {
  const normalized = `${key} ${label}`.toLowerCase()

  if (normalized.includes('accommodation') || normalized.includes('stay') || normalized.includes('hotel') || normalized.includes('lodging')) {
    return '🏨'
  }

  if (icon && icon !== '•') {
    return icon
  }

  return '✨'
}

export const LeftPanel = ({ userId }: LeftPanelProps) => {
  const ensureWorkspace = useAppStore((state) => state.ensureWorkspace)
  const preferences = useAppStore((state) => state.workspaces[userId]?.preferences ?? [])

  useEffect(() => {
    ensureWorkspace(userId)
  }, [ensureWorkspace, userId])

  return (
    <div className="fixed left-0 top-0 h-screen w-[248px] border-r border-white/60 bg-gradient-to-b from-[#f8f4ee] via-[#f7f4ef] to-[#f3efe8] p-5 flex flex-col overflow-y-auto shadow-[inset_-1px_0_0_rgba(255,255,255,0.7)]">
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
        {preferences.map((pref, index) => (
          <div
            key={pref.key}
            className={cn(
              'section-reveal is-visible min-h-[70px] px-3 py-2 rounded-[22px] bg-white/88 glass-panel border border-white/80 flex items-center gap-3 text-sm transition-all duration-300 hover:-translate-y-0.5',
              pref.updated && 'pref-update border-teal ring-2 ring-teal/10'
            )}
            style={{ transitionDelay: `${index * 45}ms` }}
          >
            <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-[#fff7ea] to-[#f3fbfa] text-lg leading-none shadow-sm">
              {getDisplayIcon(pref.key, pref.label, pref.icon)}
            </span>
            <div className="flex min-w-0 flex-1 flex-col justify-center">
              <div className="text-[10px] uppercase tracking-[0.12em] text-text-muted">
                {pref.label}
              </div>
              <div className="mt-1 text-[12px] font-semibold leading-5 text-text-primary">
                {pref.value}
              </div>
            </div>
            <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[#eef3f1]">
              <div className="h-2 w-2 rounded-full bg-teal/20 shadow-[0_0_0_4px_rgba(13,115,119,0.06)]" />
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
