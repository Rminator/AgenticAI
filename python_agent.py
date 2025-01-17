from phi.model.groq import Groq
from phi.agent import Agent
from dotenv import load_dotenv
from phi.tools.python import PythonTools


load_dotenv()

agent = Agent(
    model = Groq(id="llama-3.3-70b-versatile"),
    tools =[PythonTools()],
    show_tool_calls = True
)

agent.print_response("write a python code to find the mean of this array and dont use numpy [10,11,12,13,14]")

