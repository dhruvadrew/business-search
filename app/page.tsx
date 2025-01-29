"use client"

import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import Search from "./components/Search"
import RotatingText from "./components/RotatingText"

const queryClient = new QueryClient()

export default function Home() {
  return (
    <QueryClientProvider client={queryClient}>
      <main className="container mx-auto p-4 min-h-screen flex flex-col items-center justify-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-4 text-center">Florida Secretary of State Business Search</h1>
        <RotatingText />
        <Search />
      </main>
    </QueryClientProvider>
  )
}

