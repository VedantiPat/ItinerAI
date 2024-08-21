from langchain.tools import tool
from amadeus import Client, ResponseError
# Initialize the Amadeus client
amadeus = Client(client_id='mud8SJfItmm2zEXWVNgcQjAAWsACb9ny', client_secret='xHWDBDxjDj5BZHhe')

class CalculatorTools():

    @tool("Make a calculation")
    def calculate(operation):
        """Useful to perform any mathematical calculations,
        like sum, minus, multiplication, division, etc.
        The input to this tool should be a mathematical
        expression, a couple examples are `200*7` or `5000/2*10`
        """
        try:
            return eval(operation)
        except SyntaxError:
            return "Error: Invalid syntax in mathematical expression"
        
class AmadeusTools:
    @staticmethod
    @tool("Find cheapest flight details")
    def flight_offers_search(originLocationCode, destinationLocationCode, departureDate, returnDate, adults):
        "Searches over 400 airlines to find the cheapest round-trip flight for a given itinerary."
        try:
            # Correctly use keyword arguments
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=originLocationCode, 
                destinationLocationCode=destinationLocationCode, 
                departureDate=departureDate,
                returnDate=returnDate, 
                adults=adults
            )

            # Extract the flight offers from the response
            flight_offers = response.data
            # Find the cheapest flight offer
            cheapest_offer = flight_offers[0]
            # Return the cheapest offer
            return cheapest_offer

        except ResponseError as error:
            return str(error)

