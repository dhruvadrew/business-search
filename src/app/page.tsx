import SearchWrapper from "./components/SearchWrapper"

export default function Home() {
  return (
    <main className="container mx-auto p-4 min-h-screen flex flex-col items-center justify-center">
      <h1 className="text-4xl md:text-5xl font-bold mb-4 text-center">Florida Secretary of State Business Search</h1>
      <SearchWrapper />
    </main>
  )
}

