interface OfficerDetail {
  officer_name: string;  // Name of the officer
  officer_title: string; // Title of the officer (e.g., "President", "CEO", etc.)
  officer_address: string; // Full address of the officer (as a single string)
}

// Interface for the business data structure
interface BusinessData {
  name: string;
  document_number: string;
  fei_ein_number: string;
  date_filed: string;
  state: string;
  status: string;
  last_event: string;
  event_date_filed: string;
  principal_address: string;
  principal_changed: string;
  mailing_address: string;
  mailing_changed: string;
  registered_agent_name: string;
  registered_agent_address: string;
  name_changed: string;
  address_changed: string;
  officer_details: OfficerDetail[]; // Using OfficerDetails interface
  annual_reports: string[]; // List of annual report years as strings
  document_urls: string[]; // List of document URLs
}

// Function to generate mock data
export function generateMockData(query: string): BusinessData[] {
  const mockBusinesses: BusinessData[] = [
    {
      name: `${query} Florida Inc.`,
      document_number: `F${Math.floor(Math.random() * 1000000)}`,
      fei_ein_number: `${Math.floor(Math.random() * 100)}-${Math.floor(Math.random() * 1000000)}`,
      date_filed: new Date(Date.now() - Math.floor(Math.random() * 1000000000000)).toISOString().split("T")[0],
      state: "FL",
      status: "Active",
      last_event: "Annual Report",
      event_date_filed: new Date(Date.now() - Math.floor(Math.random() * 10000000000)).toISOString().split("T")[0],
      principal_address: `${Math.floor(Math.random() * 1000) + 1} Main St, Miami, FL ${Math.floor(Math.random() * 89999) + 10000}`,
      principal_changed: new Date(Date.now() - Math.floor(Math.random() * 100000000000)).toISOString().split("T")[0],
      mailing_address: `PO Box ${Math.floor(Math.random() * 10000)}, Miami, FL ${Math.floor(Math.random() * 89999) + 10000}`,
      mailing_changed: new Date(Date.now() - Math.floor(Math.random() * 100000000000)).toISOString().split("T")[0],
      registered_agent_name: "John Doe",
      registered_agent_address: `${Math.floor(Math.random() * 1000) + 1} Agent St, Miami, FL ${Math.floor(Math.random() * 89999) + 10000}`,
      name_changed: new Date(Date.now() - Math.floor(Math.random() * 1000000000000)).toISOString().split("T")[0],
      address_changed: new Date(Date.now() - Math.floor(Math.random() * 1000000000000)).toISOString().split("T")[0],
      officer_details: [{
        officer_name: "Jane Smith",
        officer_title: "Bob Johnson",
        officer_address: "Alice Brown",
      }],
      annual_reports: [
        new Date(Date.now() - Math.floor(Math.random() * 31536000000)).getFullYear().toString(),
        new Date(Date.now() - Math.floor(Math.random() * 63072000000)).getFullYear().toString(),
        new Date(Date.now() - Math.floor(Math.random() * 94608000000)).getFullYear().toString(),
      ],
      document_urls: [
        `http://example.com/docs/${Math.floor(Math.random() * 1000000)}`,
        `http://example.com/docs/${Math.floor(Math.random() * 1000000)}`,
        `http://example.com/docs/${Math.floor(Math.random() * 1000000)}`,
      ],
    },
    {
      name: `${query} Sunshine LLC`,
      document_number: `L${Math.floor(Math.random() * 1000000)}`,
      fei_ein_number: `${Math.floor(Math.random() * 100)}-${Math.floor(Math.random() * 1000000)}`,
      date_filed: new Date(Date.now() - Math.floor(Math.random() * 1000000000000)).toISOString().split("T")[0],
      state: "FL",
      status: "Active",
      last_event: "Amendment",
      event_date_filed: new Date(Date.now() - Math.floor(Math.random() * 10000000000)).toISOString().split("T")[0],
      principal_address: `${Math.floor(Math.random() * 1000) + 1} Beach Blvd, Orlando, FL ${Math.floor(Math.random() * 89999) + 10000}`,
      principal_changed: new Date(Date.now() - Math.floor(Math.random() * 100000000000)).toISOString().split("T")[0],
      mailing_address: `PO Box ${Math.floor(Math.random() * 10000)}, Orlando, FL ${Math.floor(Math.random() * 89999) + 10000}`,
      mailing_changed: new Date(Date.now() - Math.floor(Math.random() * 100000000000)).toISOString().split("T")[0],
      registered_agent_name: "Sarah Johnson",
      registered_agent_address: `${Math.floor(Math.random() * 1000) + 1} Agent Ave, Orlando, FL ${Math.floor(Math.random() * 89999) + 10000}`,
      name_changed: new Date(Date.now() - Math.floor(Math.random() * 1000000000000)).toISOString().split("T")[0],
      address_changed: new Date(Date.now() - Math.floor(Math.random() * 1000000000000)).toISOString().split("T")[0],
      officer_details: [{
        officer_name: "Jane Smith",
        officer_title: "Bob Johnson",
        officer_address: "Alice Brown",
      }],
      annual_reports: [
        new Date(Date.now() - Math.floor(Math.random() * 31536000000)).getFullYear().toString(),
        new Date(Date.now() - Math.floor(Math.random() * 63072000000)).getFullYear().toString(),
      ],
      document_urls: [
        `http://example.com/docs/${Math.floor(Math.random() * 1000000)}`,
        `http://example.com/docs/${Math.floor(Math.random() * 1000000)}`,
      ],
    },
  ];

  return mockBusinesses;
}