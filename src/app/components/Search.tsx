"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { SearchIcon } from "lucide-react"

interface BusinessData {
  name: string
  address: string
  phone: string
  website: string
}

export default function Search() {
  const [query, setQuery] = useState("")
  const [results, setResults] = useState<BusinessData[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [showResults, setShowResults] = useState(false)
  const router = useRouter()

  const handleSearch = async () => {
    setIsLoading(true)
    setShowResults(false)
    setResults([])
    try {
      const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`)
      const data = await response.json()
      setResults(data)
      router.push(`/?q=${encodeURIComponent(query)}`, { scroll: false })
      setTimeout(() => setShowResults(true), 100) // Delay to trigger fade-in effect
    } catch (error) {
      console.error("Error fetching data:", error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="w-full max-w-2xl space-y-4">
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
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-900"></div>
        </div>
      )}
      {results.length > 0 && (
        <div className={`transition-opacity duration-500 ease-in-out ${showResults ? "opacity-100" : "opacity-0"}`}>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Address</TableHead>
                <TableHead>Phone</TableHead>
                <TableHead>Website</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {results.map((business, index) => (
                <TableRow key={index}>
                  <TableCell>{business.name}</TableCell>
                  <TableCell>{business.address}</TableCell>
                  <TableCell>{business.phone}</TableCell>
                  <TableCell>{business.website}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  )
}

