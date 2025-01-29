"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ChevronDown, ChevronUp } from "lucide-react"

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

export default function BusinessCard({ business }: { business: BusinessData }) {
  const [isExpanded, setIsExpanded] = useState(false)
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    setIsVisible(true)
  }, [])

  return (
    <Card className={`w-full border-gray-200 transition-opacity duration-500 ease-in-out ${isVisible ? "opacity-100" : "opacity-0"}`}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-lg font-medium">{business.name}</CardTitle>
        <Button variant="ghost" size="sm" onClick={() => setIsExpanded(!isExpanded)}>
          {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          {isExpanded ? "Hide Details" : "View Details"}
        </Button>
      </CardHeader>
      <CardContent>
        <div
          className={`overflow-hidden transition-all duration-500 ease-in-out ${isExpanded ? "max-h-[2000px] opacity-100" : "max-h-0 opacity-0"}`}
        >
          <div className="space-y-2">
            <p><strong>Document Number:</strong> {business.document_number}</p>
            <p><strong>FEI/EIN Number:</strong> {business.fei_ein_number}</p>
            <p><strong>Date Filed:</strong> {business.date_filed}</p>
            <p><strong>State:</strong> {business.state}</p>
            <p><strong>Status:</strong> {business.status}</p>
            <p><strong>Last Event:</strong> {business.last_event}</p>
            <p><strong>Event Date Filed:</strong> {business.event_date_filed}</p>
            <p><strong>Principal Address:</strong> {business.principal_address}</p>
            <p><strong>Principal Changed:</strong> {business.principal_changed}</p>
            <p><strong>Mailing Address:</strong> {business.mailing_address}</p>
            <p><strong>Mailing Changed:</strong> {business.mailing_changed}</p>
            <p><strong>Registered Agent Name:</strong> {business.registered_agent_name}</p>
            <p><strong>Registered Agent Address:</strong> {business.registered_agent_address}</p>
            <p><strong>Name Changed:</strong> {business.name_changed}</p>
            <p><strong>Address Changed:</strong> {business.address_changed}</p>
            <p><strong>Officer Details:</strong> {JSON.stringify(business.officer_details)}</p>
            <p><strong>Annual Reports:</strong> {business.annual_reports.join(", ")}</p>
            <p><strong>Document URLs:</strong></p>
            <ul className="list-disc pl-5">
              {business.document_urls.map((doc) => {
                try {
                  const parsedDoc = JSON.parse(doc);
                  return (
                    <li key={parsedDoc["Document URL"]}>
                      <a href={parsedDoc["Document URL"]} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
                        {parsedDoc["Document Name"]}
                      </a>
                    </li>
                  );
                } catch (error) {
                  return null;
                }
              })}
            </ul>
          </div>
        </div>
        {!isExpanded && <p className="text-sm text-gray-500">Click 'View Details' to see more information.</p>}
      </CardContent>
    </Card>
  )
}
