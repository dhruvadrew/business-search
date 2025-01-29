"use client"

import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { SearchIcon } from "lucide-react"
import BusinessCard from "./BusinessCard"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { AlertCircle } from "lucide-react"
import RotatingText from "./RotatingText"

interface BusinessData {
  name: string
  document_number: string
  fei_ein_number: string
  date_filed: string
  state: string
  status: string
  last_event: string
  event_date_filed: string
  principal_address: string
  principal_changed: string
  mailing_address: string
  mailing_changed: string
  registered_agent_name: string
  registered_agent_address: string
  name_changed: string
  address_changed: string
  officer_details: any
  annual_reports: string[]
  document_urls: string[]
}

const getBusinessesFromDatabase = async (names: string[]): Promise<BusinessData[]> => {
  try {
    const response = await fetch("http://localhost:8000/businesses", {
      method: "POST", 
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ names }), 
    });

    if (!response.ok) {
      throw new Error(`Error fetching business data: ${response.status} - ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Failed to fetch business data from database:", error);
    return [];
  }
};

const fetchBusinesses = async (query: string): Promise<BusinessData[]> => {
  try {
    const response = await fetch("http://localhost:8000/crawl", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ user_input: query }),
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status} - ${response.statusText}`);
    }

    const data = await response.json();
    console.log("Crawl response:", data);

    const names = data.names || [];

    if (names.length === 0) {
      console.warn("No business names found after crawling.");
      return [];
    }

    return await getBusinessesFromDatabase(names);
  } catch (error) {
    console.error("Failed to fetch businesses:", error);
    return [];
  }
};

export default function Search() {
  const [query, setQuery] = useState("")
  const [isMockData, setIsMockData] = useState(false)
  const { data, isLoading, isError, error, refetch } = useQuery<BusinessData[], Error>({
    queryKey: ["businesses", query],
    queryFn: () => fetchBusinesses(query),
    enabled: false,
    onSuccess: (data) => {
      setIsMockData(data.length > 0 && data[0].name.includes(query))
    },
  })

  const handleSearch = () => {
    setIsMockData(false)
    refetch()
  }

  return (
    <div className="w-full max-w-3xl space-y-4 overflow-hidden"> {/* Prevent main page scroll */}
      {/* Sticky header with title, rotating text, and search bar */}
      <div className="sticky top-0 z-10 w-full p-4"> {/* Set background to blue */}
        <h1 className="text-4xl md:text-5xl font-bold mb-4 text-center text-black">Florida Secretary of State Business Search</h1>
        <RotatingText />
        <div className="relative mb-4"> {/* Search bar with margin */}
          <Input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter business name"
            className="pr-20"
            onKeyPress={(e) => e.key === "Enter" && handleSearch()}
          />
          <Button onClick={handleSearch} disabled={isLoading} className="absolute right-0 top-0 bottom-0 rounded-l-none">
            {isLoading ? "Searching..." : <SearchIcon size={20} />}
          </Button>
        </div>
      </div>

      {/* Loading spinner */}
      {isLoading && (
        <div className="flex justify-center items-center py-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
        </div>
      )}

      {/* Mock data warning */}
      {isMockData && (
        <Alert variant="warning">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Note</AlertTitle>
          <AlertDescription>Displaying mock data. The actual API may be unavailable.</AlertDescription>
        </Alert>
      )}

      {/* Error handling */}
      {isError && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error.message}</AlertDescription>
        </Alert>
      )}

      {/* Light Blue div for business cards */}
      {data && (
        <div className="bg-white-100 p-4 space-y-4 mt-10 overflow-y-auto max-h-[80vh]"> {/* Enable scrolling inside this div */}
          <div className="space-y-4">
            {data.map((business, index) => (
              <div
                key={index}
                className="transition-all duration-500 ease-in-out"
                style={{
                  transitionDelay: `${index * 100}ms`,
                  padding: "10px",  // Ensure there is space between the cards and the container
                  boxSizing: "border-box",  // Ensure padding is inside the width/height of the card
                }}
              >
                <BusinessCard business={business} />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
