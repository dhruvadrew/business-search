import { type NextRequest, NextResponse } from "next/server"
import { generateMockData } from "../utils/mockData"

const API_URL = "https://your-api-endpoint.com/search" // Replace with your actual API endpoint

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const query = searchParams.get("q")

  if (!query) {
    return NextResponse.json({ error: "Query parameter is required" }, { status: 400 })
  }

  try {
    const response = await fetch(`${API_URL}?q=${encodeURIComponent(query)}`)
    if (!response.ok) {
      throw new Error("API response was not ok")
    }
    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error("Error fetching data:", error)
    console.log("Falling back to mock data")
    const mockData = generateMockData(query)
    return NextResponse.json(mockData)
  }
}

