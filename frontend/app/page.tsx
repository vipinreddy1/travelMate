import { LeftPanel } from '@/components/LeftPanel'
import { CenterPanel } from '@/components/CenterPanel'
import { RightPanel } from '@/components/RightPanel'

export default function Home() {
  return (
    <main className="w-full h-screen overflow-hidden bg-warm-white">
      <LeftPanel />
      <CenterPanel />
      <RightPanel />
    </main>
  )
}
