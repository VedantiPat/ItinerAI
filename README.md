This is the source code repo for the Travel Concierge Application. This application’s framework is based upon the crewai agentic framework.

The files are as follows:
- agents.py : the agents written for this framework
- tasks.py : the tasks written for this framework
- tools.py : the tools integrated in this framework
- app.py : the main file for the streamlit UI as well as the file making the crew run from the user inputs
- mock_app.py : a mock version of the app for demo purposes, spits out an example output of the full itinerary from a previous run, this is stored in results.txt
- results.txt : stores an example output itinerary from a previous run
- requirements.txt : all of the dependencies required for this application
- test.py : to test the amadeus tool seperately


There are some changes that need to be still implemented to this version to improve it:
- Make sure that the flight agent does not go on a loop. Once it finds a result for each of the three destination cities, it should not make a call to the flight search tool again and should instead just consolidate the result into the flight details output.
- Make sure that the flight ticket price outputed is in USD.
- Currently, the best 3 cities that the best 3 agent is returning are sometimes above the budget requirements, as the approximations might be off. This is resulting in the cheapest flight ticket to be sometimes above the budget. Ensure this does not happen.
  - This agent was previously integrated with the duckduckgosearch tool to be able to get real time cost approximations for flight + stay and make judgements that way, but it would sometimes go on a loop searching for too long so instead the search functionalities were removed. If needed they can be implemented again, ensuring the looping does not happen.
- Currently, the output from the budget allocator is not really useful as it is not able to be used by the flight agent to actually take the budget allocations into consideration. The flight agent by default finds the cheapest itinerary, and sometimes this may not be under the budget allocation.
  - So the budget allocation needs to be actually made useful in this process or removed all together, or maybe even added at the end to make sure all the total costs from the booking details are under the set budget.
- The hotel and car rental APIs are not currently integrated, they can be integrated using a similar process as the flight API. There might be some further customization considering where in the city specifically the user is set to visit based on the itinerary, so a hotel and car plan should be made in consideration with the actual itinerary from the local expert.
