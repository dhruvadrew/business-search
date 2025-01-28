"use client"

import { useState, useEffect } from "react"

const descriptions = [
  "Find registered businesses in Florida",
  "Verify company information quickly",
  "Access official state records",
  "Streamline your business research",
]

export default function RotatingText() {
  const [index, setIndex] = useState(0)
  const [fade, setFade] = useState(false)

  useEffect(() => {
    const intervalId = setInterval(() => {
      setFade(true)
      setTimeout(() => {
        setIndex((prevIndex) => (prevIndex + 1) % descriptions.length)
        setFade(false)
      }, 500) // Wait for fade out, then change text
    }, 3000) // Change text every 3 seconds

    return () => clearInterval(intervalId)
  }, [])

  return (
    <p
      className={`text-xl text-center text-gray-600 mb-8 h-8 transition-opacity duration-500 ${fade ? "opacity-0" : "opacity-100"}`}
    >
      {descriptions[index]}
    </p>
  )
}

