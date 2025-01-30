"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ChevronDown, ChevronUp } from "lucide-react"

// Define an interface for the OfficerDetails
interface OfficerDetail {
  officer_name: string
  officer_title: string
  officer_address: string
}

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
  officer_details: OfficerDetail[] // Specific type instead of 'any'
  annual_reports: string[]  // Stringified JSON array
  document_urls: string[] // Document URLs in stringified JSON format
}

export default function BusinessCard({ business }: { business: BusinessData }) {
  const [isExpanded, setIsExpanded] = useState(false)
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    setIsVisible(true)
  }, [])

  const parseAnnualReport = (report: string) => {
    try {
      // Parse the stringified JSON
      const parsedReport = JSON.parse(report)
      return parsedReport
    } catch (error) {
      console.error("Error parsing report:", error)
      return null
    }
  }

  // Helper function to format addresses
  const formatAddress = (address: string) => {
    const [street, ...rest] = address.split("\n")
    const restOfAddress = rest.join(" ")
    return { street, restOfAddress }
  }

  return (
    <Card className={`w-full border-gray-200 transition-opacity duration-500 ease-in-out ${isVisible ? "opacity-100" : "opacity-0"}`}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-lg font-medium">{business.name}</CardTitle>
        <Button variant="ghost" size="sm" onClick={() => setIsExpanded(!isExpanded)} aria-expanded={isExpanded}>
          {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          {isExpanded ? "Hide Details" : "View Details"}
        </Button>
      </CardHeader>
      <CardContent>
        <div
          className={`overflow-hidden transition-all duration-500 ease-in-out ${isExpanded ? "max-h-[2000px] opacity-100" : "max-h-0 opacity-0"}`}
        >
          <div className="space-y-2">
            { business.document_number && <p><strong>Document Number:</strong> {business.document_number}</p>}
            { business.fei_ein_number && <p><strong>FEI/EIN Number:</strong> {business.fei_ein_number}</p>}
            { business.date_filed && <p><strong>Date Filed:</strong> {business.date_filed}</p>}
            { business.state && <p><strong>State:</strong> {business.state}</p>}
            { business.status && <p><strong>Status:</strong> {business.status}</p>}
            { business.last_event && <p><strong>Last Event:</strong> {business.last_event}</p>}
            { business.event_date_filed && <p><strong>Event Date Filed:</strong> {business.event_date_filed}</p>}
            
            {/* Principal Address */}
            { business.principal_address && (
              <div>
                <strong>Principal Address:</strong>
                {(() => {
                  const { street, restOfAddress } = formatAddress(business.principal_address)
                  return (
                    <div>
                      {street && <p>{street}</p>}
                      {restOfAddress && <p>{restOfAddress}</p>}
                    </div>
                  )
                })()}
              </div>
            )}

            {/* Principal Changed */}
            { business.principal_changed && <p><strong>Principal Address Changed:</strong> {business.principal_changed}</p>}

            {/* Mailing Address */}
            { business.mailing_address && (
              <div>
                <strong>Mailing Address:</strong>
                {(() => {
                  const { street, restOfAddress } = formatAddress(business.mailing_address)
                  return (
                    <div>
                      {street && <p>{street}</p>}
                      {restOfAddress && <p>{restOfAddress}</p>}
                    </div>
                  )
                })()}
              </div>
            )}

            {/* Mailing Changed */}
            { business.mailing_changed && <p><strong>Mailing Address Changed:</strong> {business.mailing_changed}</p>}

            {/* Registered Agent Address */}
            { business.registered_agent_address && (
              <div>
                <strong>Registered Agent Address:</strong>
                {(() => {
                  const { street, restOfAddress } = formatAddress(business.registered_agent_address)
                  return (
                    <div>
                      {street && <p>{street}</p>}
                      {restOfAddress && <p>{restOfAddress}</p>}
                    </div>
                  )
                })()}
              </div>
            )}

            {/* Registered Agent Name */}
            { business.registered_agent_name && <p><strong>Registered Agent Name:</strong> {business.registered_agent_name}</p>}
            
            {/* Other address-related fields */}
            { business.name_changed && <p><strong>Name Changed:</strong> {business.name_changed}</p>}
            { business.address_changed && <p><strong>Address Changed:</strong> {business.address_changed}</p>}

            {/* Officer Details */}
            <p><strong>Officer Details:</strong></p>
            <div className="space-y-2">
              {business.officer_details && business.officer_details.map((officer, index) => {
                const { officer_name, officer_title, officer_address } = officer
                if (!officer_name || !officer_title || !officer_address) return null

                // Split address into street and rest (city, state, zip)
                const { street, restOfAddress } = formatAddress(officer_address)

                return (
                  <div key={index} className="p-4 border-b border-gray-300">
                    <p><strong className="font-bold">Title:</strong> {officer_title}</p>
                    <p><strong className="font-bold">Name:</strong> {officer_name}</p>
                    {street && <p><strong className="font-bold">Address:</strong> {street}</p>}
                    {restOfAddress && <p>{restOfAddress}</p>}
                  </div>
                )
              })}
            </div>

            {/* Annual Reports */}
            <p><strong>Annual Reports:</strong></p>
            <div className="space-y-2">
              {business.annual_reports && business.annual_reports.map((report, index) => {
                const parsedReport = parseAnnualReport(report)
                if (!parsedReport || !parsedReport["Report Year"] || !parsedReport["Filed Date"]) return null // Skip null/empty entries
                
                return (
                  <div key={index} className="p-4 border-b border-gray-300">
                    {parsedReport["Report Year"] && (
                      <p><strong>Report Year:</strong> {parsedReport["Report Year"]}</p>
                    )}
                    {parsedReport["Filed Date"] && (
                      <p><strong>Filed Date:</strong> {parsedReport["Filed Date"]}</p>
                    )}
                  </div>
                )
              })}
            </div>

            {/* Document URLs */}
            <p><strong>Document URLs:</strong></p>
            <ul className="list-disc pl-5">
              {business.document_urls.map((doc, index) => {
                try {
                  const parsedDoc = JSON.parse(doc)
                  return (
                    <li key={index}>
                      <a href={parsedDoc["Document URL"]} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
                        {parsedDoc["Document Name"]}
                      </a>
                    </li>
                  )
                } catch (error) {
                  return null
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
