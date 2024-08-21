from crewai import Crew, Process
from agents import TravelAgents
from tasks import TravelTasks
import streamlit as st
import datetime
import os

os.environ["OPENAI_API_KEY"] = "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"
os.environ["OPENAI_MODEL_NAME"]="gpt-4o-mini"


st.set_page_config("Travel Concierge", page_icon="✈️", layout="wide")


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


class TravelCrew:

    def __init__(self, location, category, people, date_range, budget, flight, hotel, car):
        self.location = location
        self.category = category
        self.people = people
        self.date_range = date_range
        self.budget = budget
        self.flight = flight
        self.hotel = hotel
        self.car = car
        self.output_placeholder = st.empty()

    
    def run(self):
        agents = TravelAgents()
        tasks = TravelTasks()

        city_selector_agent = agents.city_selection_expert()
        best_three_agent = agents.best_three_agent()
        local_expert = agents.local_expert()
        budget_allocator = agents.budget_allocator()
        flight_expert = agents.flight_expert()
        planner_agent = agents.planner_agent()

        top_ten_task = tasks.top_ten_task(
            city_selector_agent,
            self.category,
            self.date_range,
        )

        best_three_task = tasks.best_three_task(
            best_three_agent,
            self.location,
            self.category,
            self.people,
            self.date_range,
            self.budget,
        )

        gather_task = tasks.gather_task(
            local_expert,
            self.category,
            self.people,
            self.date_range,
        )

        budget_allocator_task = tasks.budget_allocator_task(
            budget_allocator,
            self.location,
            self.people,
            self.date_range,
            self.budget,
            self.flight,
            self.hotel,
            self.car,
        )

        flight_task = tasks.flight_task(
            flight_expert,
            self.location,
            self.people,
            self.date_range,
        )

        planner_task = tasks.planner_task(
            planner_agent,
            self.category,
            self.location,
            self.date_range,
        )

        best_three_task.context=[top_ten_task]
        gather_task.context = [best_three_task]
        budget_allocator_task.context = [best_three_task]
        flight_task.context = [budget_allocator_task]
        planner_task.context = [gather_task, budget_allocator_task, flight_task]

        crew = Crew(
            agents=[
                city_selector_agent,
                best_three_agent,
                local_expert,
                budget_allocator,
                flight_expert,
                planner_agent,
            ],
            tasks=[
                top_ten_task, 
                best_three_task,
                gather_task,
                budget_allocator_task,
                flight_task,
                planner_task,
            ],
            process=Process.sequential,
        )

        result = crew.kickoff()

        return result
    


if __name__ == "__main__":
    st.title("🏖️ Travel Concierge")

    st.subheader("Plan your next trip with Amadeus!",
                 divider="orange", anchor=False)

    import datetime

    today = datetime.datetime.now().date()
    next_year = today.year + 1
    jan_16_next_year = datetime.date(next_year, 1, 10)
    categories=["Wellness Retreat", "Vacation", "Honeymoon"]
    checklist = {
        'Flights': 'Yes',
        'Hotels': 'No',
        'Car rentals': 'No'
    }

    with st.sidebar:
        st.header("👇 Enter your trip details")
        with st.form("my_form"):
            location = st.text_input(
                "📍 Where are you currently located?", placeholder="San Mateo, CA")
            category = st.selectbox(
                "🗺️  What kind of trip are you looking for?", options=categories, index=None, placeholder="Vacation"
            )
            people = st.number_input(
                "👥 How many people are traveling?", min_value=1, max_value=50
            )
            date_range = st.date_input(
                "📆 Date range you are interested in traveling?",
                min_value=today,
                value=(today, jan_16_next_year + datetime.timedelta(days=6)),
                format="MM/DD/YYYY",
            )
            budget = st.number_input(
                "💲 What is your budget (USD)?"
            )
            st.write("✈️ Which arrangements would you like to be included in your plan?")
            flight = st.checkbox("Flights")
            hotel = st.checkbox("Hotels")
            car = st.checkbox("Car rentals")


            if flight:
                checklist['Flights'] = 'Yes'

            
            if hotel:
                checklist['Hotels'] = 'Yes'

            if car:
                checklist['Car rentals'] = 'Yes'

            

            submitted = st.form_submit_button("Submit")


if submitted:
    
    if location == '' or category == None or budget == 0.00:
        st.write ("Please fill out all required fields!")

    file_name = 'results.txt'

    # Open the file in read mode
    with open(file_name, 'r') as file:
    # Read the contents of the file
        contents = file.read()
    
    with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
        with st.container(height=500, border=False):
            st.markdown(contents)
        status.update(label="✅ Trip Plan Ready!")


     



