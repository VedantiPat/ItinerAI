# Travel Concierge Application

## Overview
This repository contains the source code for the **Travel Concierge Application**, built using the **CrewAI agentic framework**. The application provides AI-driven travel planning, generating end-to-end itineraries based on user preferences.

## Repository Structure
- **agents.py** – Defines the AI agents for the framework.
- **tasks.py** – Outlines the tasks assigned to agents.
- **tools.py** – Integrates external tools used within the framework.
- **app.py** – The main file for the **Streamlit UI**, handling user inputs and agent execution.
- **mock_app.py** – A mock version for demo purposes, generating example itineraries stored in `results.txt`.
- **results.txt** – Stores a sample output itinerary from a previous run.
- **requirements.txt** – Lists dependencies required for the application.
- **test.py** – Used to test the **Amadeus API tool** separately.

## Pending Improvements
### 🛠 Flight Agent Enhancements
- Ensure the **flight agent does not loop**. Once results for the three destination cities are found, the agent should **stop searching** and consolidate the output.
- Convert **flight ticket prices to USD** for consistency.
- Improve budget handling so that the **selected cities align with budget constraints**, preventing expensive flight selections.

### 💡 Budget Allocation Adjustments
- The **budget allocator** currently does not influence the flight agent’s decisions effectively. Options:
  - Make it actively constrain flight selection.
  - Integrate it **at the final stage** to ensure total costs stay within budget.
  - Remove it if it proves unnecessary.

### 🔍 Search Functionality Optimization
- The **DuckDuckGo search tool** was previously integrated for real-time cost approximations but was removed due to looping issues.
- If reintroduced, ensure **looping does not occur** while retrieving pricing data.

### 🏨 Hotel & Car Rental API Integration
- **Hotels and car rentals are not yet integrated**. These should:
  - Consider **itinerary-specific locations** rather than generic city-wide searches.
  - Align with recommendations from the **local expert agent** to ensure convenient accommodations.

---
This application continues to evolve, and these improvements will enhance its functionality for **seamless AI-driven travel planning**. 🚀

