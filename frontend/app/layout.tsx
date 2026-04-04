import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'TripMind - Your Intelligent Travel Companion',
  description: 'Plan smarter trips by learning from your memories and your friends\' experiences.',
  viewport: 'width=device-width, initial-scale=1.0',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}
