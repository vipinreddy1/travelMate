export type TripMindPreferenceMetadata = Record<string, string>

export interface TripMindUserMetadata {
  preferences: TripMindPreferenceMetadata
  profileInitializedAt: string
  profileVersion: number
}

export const defaultTripMindMetadata = (): TripMindUserMetadata => ({
  preferences: {
    budget: '$$ (Mid-range)',
    vibe: 'Relaxed',
    pace: 'Slow explorer',
    dietary: 'Vegetarian',
    stay: 'Boutique hotels',
    group: 'Solo',
  },
  profileInitializedAt: new Date().toISOString(),
  profileVersion: 1,
})

export const normalizeTripMindMetadata = (
  candidate: Partial<TripMindUserMetadata> | null | undefined
): TripMindUserMetadata => {
  const defaults = defaultTripMindMetadata()

  return {
    preferences: {
      ...defaults.preferences,
      ...(candidate?.preferences ?? {}),
    },
    profileInitializedAt: candidate?.profileInitializedAt ?? defaults.profileInitializedAt,
    profileVersion: candidate?.profileVersion ?? defaults.profileVersion,
  }
}
