from phi.agent import Agent
from phi.tools.youtube_tools import YouTubeTools
from phi.model.groq import Groq
from dotenv import load_dotenv


load_dotenv()

agent = Agent(
    model = Groq(id="llama-3.3-70b-versatile"),
    tools =[YouTubeTools()],
    show_tool_calls = True,
    #description="You are a youtube agent, obtain captions of the youtube videos and answer questions..."
    
)

agent.print_response("Summarize this video https://www.youtube.com/watch?v=uzkc-qNVoOk&ab_channel=KhanAcademy", markdown=True)