'use client'

import { notFound } from 'next/navigation'
import { BlogPostContent } from '@/components/BlogPostContent'
import { getBlogById } from '@/lib/blogData'

interface BlogPageProps {
  params: {
    id: string
  }
}

export default function BlogPage({ params }: BlogPageProps) {
  const blog = getBlogById(params.id)

  if (!blog) {
    notFound()
  }

  return <BlogPostContent blog={blog} />
}
