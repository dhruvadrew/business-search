import { type NextRequest, NextResponse } from "next/server"

function mockCrawler(query: string): any[] {
  const floridaCities = ["Miami", "Orlando", "Tampa", "Jacksonville", "Tallahassee"]
  const mockData = [
    {
      name: `${query} Florida Inc.`,
      address: `${Math.floor(Math.random() * 1000) + 1} Main St, ${floridaCities[Math.floor(Math.random() * floridaCities.length)]}, FL ${Math.floor(Math.random() * 89999) + 10000}`,
      phone: `(${Math.floor(Math.random() * 800) + 200}) ${Math.floor(Math.random() * 900) + 100}-${Math.floor(Math.random() * 9000) + 1000}`,
      website: `www.${query.toLowerCase().replace(" ", "")}-fl.com`,
    },
    {
      name: `${query} Sunshine LLC`,
      address: `${Math.floor(Math.random() * 1000) + 1} Beach Blvd, ${floridaCities[Math.floor(Math.random() * floridaCities.length)]}, FL ${Math.floor(Math.random() * 89999) + 10000}`,
      phone: `(${Math.floor(Math.random() * 800) + 200}) ${Math.floor(Math.random() * 900) + 100}-${Math.floor(Math.random() * 9000) + 1000}`,
      website: `www.${query.toLowerCase().replace(" ", "")}sunshine.com`,
    },
  ]
  return mockData
}

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const query = searchParams.get("q")

  if (!query) {
    return NextResponse.json({ error: "Query parameter is required" }, { status: 400 })
  }

  // Simulate longer processing time (2-4 seconds)
  await new Promise((resolve) => setTimeout(resolve, Math.random() * 2000 + 2000))

  const results = mockCrawler(query)
  return NextResponse.json(results)
}

