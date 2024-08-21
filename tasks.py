from crewai import Task

from textwrap3 import dedent
from tools import AmadeusTools
flight_offer = AmadeusTools.flight_offers_search




class TravelTasks():
    
    def top_ten_task(self, agent, category, dates):
        return Task(
            description=dedent(f"""\
                **Task**:  Identify the top 10 cities for this trip
                **Description**: You are given a category for a trip and a date range. Based on the time of year this trip falls in, find the top 10 cities for a trip of this category.
                Make sure to account for weather conditions and seasonal/cultural events in the given month/months of the trip (this is given by the date range).

                    
                **Parameters**:                                    
                category: {category}
                date range: {dates}
            """),
            expected_output=dedent(f"""\
                A list of the top 10 cities with the following format for each:  
                **City Name**
                **Brief description of the weather conditions and cultural events during the date range given.**
                **Brief description of why this city would be ideal for the category of the trip.**       
            """),
            agent=agent,
            async_execution=True
        )

    def best_three_task(self, agent, location, category, people, dates, budget):
        return Task(
            description=dedent(f"""\
                **Task**: Given a list of 10 possible cities for this trip, from the output of top_ten_task, identify the best 3 cities.
                **Description**: You will be given a list of 10 possible cities for a trip of the category {category}. 
                

                Do the following:
                - For each of the 10 cities, find the average cost approximation for a round trip flight to this city, considering the starting location as {location} and the number of        people on the trip as {people}, with the start and end dates of the trip defined by {dates}.
                - Then, for each of the 10 cities, find the approximate cost of stay for {people} people at these cities for the number of days of the trip.
                - Make a list of the 10 cities with the cost of flight and the cost of stay, as well as the total costs (flight + stay for all people)
                - Determine if the total costs for each of the cities is within or exceeds the budget given by {budget} in USD.
                - Filter the list and only keep the cities that are within budget.
                - From the remaining cities, select the cheapest three cities which you believe are the best for this trip, taking budget into considerations.

                **Parameters**:
                location: {location}                                    
                category: {category}
                number of people: {people}
                date range: {dates}
                budget: {budget}
            """),
            expected_output=dedent(f"""\
                The best three cities for this trip listed in the following format:
                **City Name**
                **Average cost approximation for flight, determined from before**
                **Average cost approximation for stay, determined from before**
                **Total trip costs at this city (flight + stay)**   
            """),
            agent=agent,
        )
    
    def gather_task(self, agent, category, people, dates):
        return Task(
            description=dedent(f"""\
                **Task**: Your task is to act as a local expert on these the three cities given.
                **Description**: You will be given a list of three cities from the output of best_three_task. 
                These three are potential cities for a {category} trip by {people} number of people during the date range of {dates}.
                
                You are to act as a local expert on all three of these cities and compile an
                in-depth guide for {people} people traveling there and wanting
                to have THE BEST {category} trip ever!
                Gather information about  key attractions, local customs,
                special events, and daily activity recommendations.
                Find the best spots to go to, the kind of place only a
                local would know.
                This guide should provide a thorough overview of what
                each city has to offer, including hidden gems, cultural
                hotspots, must-visit landmarks, weather forecasts, and
                high level costs.

                The final answer must be a comprehensive city guide for all three cities,
                rich in cultural insights and practical tips,
                tailored to enhance the travel experience.

                category: {category}
                number of people: {people}
                date range of trip: {dates}

            """),
            expected_output=dedent(f"""\
                A comprehensive city guide for each city with cultural insights and practical tips, formatted as following:
                **City Name**
                **Comprehensive city guide for that city**
                
            """),
            agent=agent,
            
        )
    
    def budget_allocator_task(self, agent, location, people, dates, budget, flight, hotel, car):
        return Task(
            description=dedent(f"""\
                **Task**: Your task is to allocate the budget given by {budget} for the trip given the various allocation requirements in consideration.
                **Description**: 
                You will be given a list of three cities with a highlevel breakdown of costs for trips to those cities, given by the output of best_three_task.
                These three cities are potential travel destinations for a trip of {people} people starting from the location of {location} during the date range of {dates} with the budget of {budget}.
                You have a budget of {budget} to work with for EACH of these SEPARATE trip possibilities. Consider the budget breakdowns for all three cities as independent of each other.
                This output highlights, for each of these cities, the approximate flight costs for the trip as well as the approximate stay costs for the trip.
                
                If the flight variable is set to Yes, that means you have to consider the flight costs as a category in your budget allocations.
                If the hotel variable is set to Yes, that means you have to consider the accomodation costs as a category in your budget allocations.
                If the car variable is set to Yes, that means you have to consider the car rental costs as a category in your budget allocations.

                Create a budget breakdown of the different categories that the budget needs to be allocated to, depending on which variables are set to yes.
                You can use the cost approximation for flight and stay from the highlevel breakdown of costs as your flight and hotel budget allocation (if those variables are set to yes), but make sure you
                use your own expertise on these numbers to determine what a good budget allocation for all of the categories is, given that all of the categories that are set to yes MUST be accounted for in the budget.
                
                number of people: {people}
                date range of trip: {dates}
                starting location: {location}
                budget: {budget}
                flight variable: {flight}
                hotel variable: {hotel}
                car variable: {car}

            """),
            expected_output=dedent(f"""\
                A budget breakdown for each of the cities in the following format:
                **City Name: City Name**
                **Airport Code: The airport code for the nearest airport to this city**
                **Budget breakdown by allocation category for this city**
                
            """),
            agent=agent,
        )
    
    def flight_task(self, agent, location, people, dates):
        return Task(
            description=dedent(f"""\
                **Task Description**: The flight_search tool is a tool you can use to find round-trip flight details from one location to another.
                The parameters it takes as input are originLocationCode, destinationLocationCode, departureDate, returnDate, adults.
                    
                For each of the three cities from the output of budget_allocator_task, do the following:
                    You must finish all these steps first for one city before moving on to the next city.
                    Use the flight_search tool to return round-trip flight details for a trip to this destination city.
                    The following are what you will use for the tool parameters:

                    originLocationCode: The nearest airport code to the city given by {location},
                    destinationLocationCode: The airport code of the destination city from the budget_allocator_task,
                    departureDate: first date from {dates},
                    returnDate: last date from {dates}
                    adults: {people}

                    If error is encountered:

                        If you get an error like [400], [500], or [429] as output, try the tool again with the same inputs.
                        If you get an list index out of range error, run the tool again but replace the destinationLocationCode with another closest airport to destination not the same one you already used as a parameter.
                        If that still doesn't work, replace the originLocationCode with another airport closest to the {location}.

                    The tool will successfully return a JSON output.
                    Use the JSON output for this city to fill out the flight details in the template given below:

                    **Template**
                    *City Name*
                    Round-trip Total Ticket Price: *data[0].price.total converted from data[0].price.currency to USD*
                    Last date to purchase tickets: *data[0].lastTicketingDateTime*
                    Itinerary:  
                        Outbound: 
                            Departure City: *City and iata code of departure for outbound* 
                            Arrival City: *City and iata code of final arrival for outbound*
                            Departure Date: *Departure date given for outbound*
                            Departure Time: *Departure time for outbound*
                            Arrival Date: *Final arrival date for outbound*
                            Arrival Time: *Final arrival time for outbound*
                            Airline: *carrierCode for the outbound segment*
                            Flight Number: *Flight number for outbound segment*, 
                            Class: *cabin for outbound segment*
                        Return:  
                            Departure City: *City and iata code of departure for return* 
                            Arrival City: *City and iata code of final arrival for return*
                            Departure Date: *Departure date given for return*
                            Departure Time: *Departure time for return*
                            Arrival Date: *Final arrival date for return*
                            Arrival Time: *Final arrival time for return*
                            Airline: *carrierCode for the return segment*
                            Flight Number: *Flight number for return segment*, 
                            Class: *cabin for return segment*              

                Once you have done this process for one city, move on to the next city and do this for all three cities.

            """),
            expected_output=dedent(f"""\
                Consolidate the flight details for all three of the trips and output them together.             
            """),
            tools=[flight_offer],
            agent=agent,
        )
    
    def planner_task(self, agent, category, location, dates):
        return Task(
            description=dedent(f"""\
                **Task**: Create an in-depth start to finish trip itinerary for the three possible trips to the three cities.
                **Description**: 
                The output given from the gather_task is an in-depth city guide for each of the three cities, you will use this mainly in your itinerary.
                The output from flight_task is the flight details for all three cities' trips.
                These three cities are our destination city for each of the three trips respectively.
                Using this context as well as the given parameters, create a travel itinerary for each of the three cities.
                
                The format given below is a general guideline for how the itinerary for each city should be structured. Following the general outline of this format,
                create a more aesthetically pleasing markdown version of this itinerary for each of the three cities.
                
                **Format**               
                Here is your in-depth itinerary for a {category} trip starting from {location} for the dates *the start and end dates of {dates}*:

                City 1: *name of city 1*
                *The comprehensive city guide for city 1 from gather_task output, only include the summary at the top of the city guide, the key attractions, the local customs, and special events*

                Day by day itinerary:

                *start date, given by the first date of {dates}*
                Leave for the airport at *Outbound departure time (for city 1) from flight_task minus 3 hours*.

                Flight details:
                *the flight booking details from flight_task for city 1 INCLUDING the round-trip ticket price (in USD), last date to purchase tickets, and outbound details. Make these indented and italicized.*

                Arrive at *city 1* at *Outbound arrival time for city 1 from flight_task*.

                *Day by day itinerary in-depth at city 1, given by the gather_task output. Be descriptive with this. Label the days according to the consecutive dates after the start date.*
                *Go up till the day before the end date*

                *end date, given by last date of {dates}*
                Leave for the airport at *Return departure time (for city 1) from flight_task minus 3 hours*.

                Flight details:
                *all of the return flight booking details for city 1 from flight_task. Make these indented and italicized.*

                Hope you enjoy an eventful trip to *city 1*!

                
            """),
            expected_output=dedent(f"""\
                Travel itineraries for each of the three cities respectively, one after another. Make this in an organized and aesthetically pleasing markdown format. Make use of indentation, spacing, and layout to make it organized. Separate each city itinerary with a horizontal line.
                
            """),
            agent=agent,
        )

