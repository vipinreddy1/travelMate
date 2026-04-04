import { BlogPostPage } from '@/components/BlogPostPage'

export default function TripPage({ params }: { params: { id: string } }) {
  return <BlogPostPage params={params} />
}
