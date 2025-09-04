# n8n Workflow Design: Collect Cheapest Google Flights Prices Daily

## 1. Goal
- Automatically run every day at a specified time (e.g., 09:00).  
- Query the **lowest price flight** between specific cities (e.g., Tokyo HND → Shenyang SHE).  
- Record the result in a database or Google Sheet.  
- (Optional) Send notifications with the daily lowest price.  

---

## 2. Requirements
- **SerpApi account** (free plan allows 100 searches/day).  
  - API docs: https://serpapi.com/google-flights-api  
  - Get an API key.  
- A **database (MySQL/Postgres/SQLite)** or **Google Sheet** to store results.  
- n8n installed and connected to the internet.  

---

## 3. Workflow Node Design

### Node 1: `Cron`
- Type: Scheduled trigger  
- Config: Run daily at 09:00  

---

### Node 2: `HTTP Request` (Call SerpApi)
- Method: `GET`  
- URL:  
  ```
  https://serpapi.com/search
  ```  
- Query parameters example:  
  ```
  engine=google_flights
  departure_id=HND
  arrival_id=SHE
  outbound_date=2025-10-01
  currency=JPY
  hl=en
  api_key=YOUR_API_KEY
  ```  
- Notes:  
  - `departure_id` = departure airport code (e.g., HND)  
  - `arrival_id` = arrival airport code (e.g., SHE)  
  - `outbound_date` = travel date  
  - `currency` = price currency  
  - `hl` = language  

The response will be JSON with flight results.  

---

### Node 3: `Function`
- Extract the lowest flight price.  
- Example code:  
  ```javascript
  const data = items[0].json.flights_results;
  if (!data || data.length === 0) {
    return [{json: {price: null, note: "No flight data"}}];
  }

  let minPrice = null;
  let bestFlight = null;
  for (let flight of data) {
    if (flight.price && flight.price.amount) {
      const price = parseFloat(flight.price.amount);
      if (minPrice === null || price < minPrice) {
        minPrice = price;
        bestFlight = flight;
      }
    }
  }

  return [{
    json: {
      date: new Date().toISOString().slice(0,10),
      departure: bestFlight?.departure_airport?.id || "HND",
      arrival: bestFlight?.arrival_airport?.id || "SHE",
      airline: bestFlight?.airline || "Unknown",
      price: minPrice,
      currency: bestFlight?.price?.currency || "JPY"
    }
  }];
  ```  

---

### Node 4: Store Data
Two options:  

1. **Google Sheets node**  
   - Append a new row each run:  
     ```
     Date | Departure | Arrival | Airline | Lowest Price | Currency
     ```  

2. **Database node (MySQL/Postgres)**  
   - Table schema example:  
     ```sql
     CREATE TABLE flight_prices (
       id SERIAL PRIMARY KEY,
       record_date DATE,
       departure VARCHAR(10),
       arrival VARCHAR(10),
       airline VARCHAR(50),
       price NUMERIC,
       currency VARCHAR(10)
     );
     ```  
   - Configure the DB node in n8n to insert Function node output.  

---

### Node 5 (Optional): Notifications
- Use **Telegram / Email / Slack node**.  
- Example message:  
  ```
  Daily Cheapest Flight
  Route: HND → SHE
  Airline: ANA
  Price: 68,000 JPY
  Date: 2025-09-04
  ```  

---

## 4. Extensions
- Query **multiple routes** using `Split In Batches` node.  
- Query **different dates** (e.g., next 7 days) to track price trends.  
- Add statistics in n8n (e.g., weekly average, price difference from yesterday).  
