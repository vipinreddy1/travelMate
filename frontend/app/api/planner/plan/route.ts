import { NextResponse } from 'next/server'

const getPlannerApiUrl = () =>
  process.env.PLANNER_API_URL?.trim() || process.env.NEXT_PUBLIC_API_URL?.trim()

export async function POST(request: Request) {
  const plannerApiUrl = getPlannerApiUrl()

  if (!plannerApiUrl) {
    return NextResponse.json(
      { detail: 'Planner API URL is not configured on the frontend server.' },
      { status: 500 }
    )
  }

  let body: unknown

  try {
    body = await request.json()
  } catch {
    return NextResponse.json({ detail: 'Invalid JSON payload.' }, { status: 400 })
  }

  try {
    const response = await fetch(`${plannerApiUrl}/api/v1/planner/plan`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      cache: 'no-store',
    })

    const text = await response.text()
    const contentType = response.headers.get('content-type') || 'application/json'

    return new NextResponse(text, {
      status: response.status,
      headers: {
        'Content-Type': contentType,
      },
    })
  } catch (error) {
    const detail =
      error instanceof Error
        ? `Unable to reach planner backend at ${plannerApiUrl}. ${error.message}`
        : `Unable to reach planner backend at ${plannerApiUrl}.`

    return NextResponse.json({ detail }, { status: 502 })
  }
}
