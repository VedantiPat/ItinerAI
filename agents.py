from crewai import Agent
from textwrap3 import dedent
from tools import CalculatorTools, AmadeusTools
from langchain_community.tools import DuckDuckGoSearchRun# Initialize the tool
search_tool = DuckDuckGoSearchRun()
calculator = CalculatorTools.calculate
flight_offer = AmadeusTools.flight_offers_search

class TravelAgents(): 
  
  def city_selection_expert(self):
    return Agent(
        role="City Selection Expert",
        backstory=dedent(
            f"""Expert at analyzing travel data to pick ideal destinations"""),
        goal=dedent(
            f"""Select the best cities based on category of trip, weather, season, prices."""),
        verbose=True,
        max_iter=30, # Default value for maximum iterations
        allow_delegation=False,
        max_execution_time = None,
        tools=[search_tool],
    )
  
  def best_three_agent(self):
    return Agent(
        role="Travel Agent Expert",
        backstory=dedent(
            f"""Expert at analyzing travel data and costs to pick ideal destinations based on budget limitations"""),
        goal=dedent(
            f"""Select the best 3 cities out of a list of 10 cities based on the the approximate costs for a trip there for the given number of people, given budget limitations."""),
        verbose=True,
        max_iter=50, # Default value for maximum iterations
        allow_delegation=False,
        max_execution_time = None,
    )
  
  def local_expert(self):
        return Agent(
            role='Local Expert at the given cities',
            goal='Provide the BEST insights about the selected cities',
            backstory="""A knowledgeable local guide with extensive information
            about the city, it's attractions and customs""",
            verbose=True,
            max_iter=50, # Default value for maximum iterations
            allow_delegation=False,
            max_execution_time = None,
            tools=[search_tool],
        )
  
  def budget_allocator(self):
        return Agent(
            role='Expert Budget Allocator',
            goal='Given the requirements for a trip, using your expertise, carefully allocate the given budget to the specific spending needs, ensuring that the total allocation does not pass given budget.',
            backstory="An experienced financial planner with a knack for optimizing travel budgets to maximize value and experience.",
            verbose=True,
            max_iter=50, # Default value for maximum iterations
            allow_delegation=False,
            max_execution_time = None,
        )
  
  def flight_expert(self):
        return Agent(
            role='Flight Booking Expert',
            goal='Find roundtrip flight booking details for the given number of people from start location to end destination for the start and end dates defined.',
            backstory="""You are an experienced flight booking expert, with the ability to find the round trip flight details given the dates and the number of people.""",
            verbose=True,
            max_iter=50, # Default value for maximum iterations
            allow_delegation=False,
            max_execution_time = None,
        )
  
  def planner_agent(self):
        return Agent(
            role='Itinerary Planner Expert',
            goal='Using the information you are given from the city tour guide, the budget allocation, and the flight booking details, create a consolidated an in-depth travel itinerary for the three cities given.',
            backstory="Expert in travel planning and logistics. I have decades of expereince making travel iteneraries.",
            verbose=True,
            max_iter=25, # Default value for maximum iterations
            allow_delegation=False,
            max_execution_time = None,
        )
       
