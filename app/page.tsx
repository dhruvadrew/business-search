"use client"

import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import Search from "./components/Search"

const queryClient = new QueryClient()

export default function Home() {
  return (
    <QueryClientProvider client={queryClient}>
      <main className="container mx-auto p-4 min-h-screen flex flex-col items-center justify-start">
        {/* Title & Rotating Text will stay fixed */}

        {/* Search bar below the fixed title */}
        <Search />
      </main>
    </QueryClientProvider>
  )
}
