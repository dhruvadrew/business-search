"use client"

import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { SearchIcon } from "lucide-react"
import BusinessCard from "./BusinessCard"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { AlertCircle } from "lucide-react"
import { generateMockData } from "../utils/mockData"

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

const fetchBusinesses = async (query: string): Promise<BusinessData[]> => {
  //const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`)
  //if (!response.ok) {
  //  throw new Error("Network response was not ok")
  //}
  //return response.json()
  return generateMockData(query)
}

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
    <div className="w-full max-w-3xl space-y-4">
      <div className="relative">
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
      {isLoading && (
        <div className="flex justify-center items-center py-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
        </div>
      )}
      {isMockData && (
        <Alert variant="warning">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Note</AlertTitle>
          <AlertDescription>Displaying mock data. The actual API may be unavailable.</AlertDescription>
        </Alert>
      )}
      {isError && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error.message}</AlertDescription>
        </Alert>
      )}
      {data && (
        <div className="space-y-4">
          {data.map((business, index) => (
            <div
              key={index}
              className="transition-all duration-500 ease-in-out"
              style={{ transitionDelay: `${index * 100}ms` }}
            >
              <BusinessCard business={business} />
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

