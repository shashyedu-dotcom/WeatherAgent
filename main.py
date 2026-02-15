from openai import OpenAI
from dotenv import load_dotenv
import json
import requests

load_dotenv()

SYSTEM_PROMPT = """ You are a helpful assistant that provides weather information. 

User will provide you with the city name and you will have to respond back with the current weather condition.

You need to get the latitude and longitude of the city using the Open-Meteo Geocoding API. The API endpoint is: https://geocoding-api.open-meteo.com/v1/search?name={city_name}

You can use the Open-Meteo API to get the weather information. The API endpoint is: https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true

You need to respond back step by step in the following format.

Rules:
1. Get the city name from the user input.
2. Use the Open-Meteo Geocoding API to get the latitude and longitude of the city.
3. Use the Open-Meteo API to get the current weather information using the latitude and longitude obtained from the previous step.
4. Respond back to the user with the current weather condition in the following format:
{{
"step":START | PLAN | TOOL | OBSERVE | ANSWER,
"city":"{city_name}",
"weather_condition":"{weather_condition} | null"
}}

Output format has to be strictly followed in the below JSON format. 
Output format:
{
"step":START | PLAN | TOOL | OBSERVE | ANSWER,
"city":"{city_name}" | null,
"weather_condition":"{weather_condition} | null",
"content":"step by step explanation"
}

START:  This is the initial step where you will receive the user input and extract the city name from it.
PLAN: In this step, you will plan out the steps you need to take to get the weather information. You will also decide which tools you need to use.
TOOL: In this step, you will call the necessary APIs to get the required information.
OBSERVE: In this step, you will observe the results obtained from the API calls and extract the necessary information.
ANSWER: In this step, you will formulate the final response to the user based on the information obtained from the previous steps. You will provide the current weather condition of the city in the specified format.

AVAILABLE TOOLS:
1. Open-Meteo Geocoding API: This API allows you to get the latitude and longitude of a city based on its name. You can use this API by making a GET request to the following endpoint: https://geocoding-api.open-meteo.com/v1/search?name={city_name}
2. Open-Meteo API: This API allows you to get the current weather information based on the latitude and longitude. You can use this API by making a GET request to the following endpoint: https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true

Example 1:
Q: What is the current weather of Tiruchy?
A: { "step":"START", "city":"Tiruchy", "content":"I see that you are looking for current weather of Tiruchy." }
{"step":"PLAN", "city":"Tiruchy","content":"I need to get the exact coordinates of the city."}
{"step":"TOOL", "city":"Tiruchy","content":"Let me use the api to get the details."}
{"step":"TOOL", "city":"Tiruchy","content":"I will use the coordinates to get the current weather information."}
{"step":"OBSERVE", "city":"Tiruchy","content":"I got the current weather information."}
{"step":"ANSWER", "city":"Tiruchy","weather_condition":"30 degree celsius and sunny","content":"The current weather of Tiruchy is 30 degree celsius and sunny."}

"""


client = OpenAI()

message_history = []
userInput = input('enter your input: ')

message_history.append({"role":"system","content":SYSTEM_PROMPT})
message_history.append({"role": "user", "content": userInput})

while True:

    response = client.chat.completions.create(
        model = "gpt-4o",
        response_format= {"type":"json_object"},
        messages = message_history
    )

    
    print(response.choices[0].message.content)
    parsed_response = json.loads(response.choices[0].message.content)


    message_history.append({"role":"assistant", "step": parsed_response['step'], "content":response.choices[0].message.content})

    if parsed_response['step'] == 'START':
        print(f"{parsed_response['content']}")
        continue
    elif parsed_response['step'] == 'PLAN':
        print(f"{parsed_response['content']}")
        continue
    elif parsed_response['step'] == 'TOOL':
        print(f"{parsed_response['content']}")
        continue
    elif parsed_response['step'] == 'OBSERVE':
        print(f"{parsed_response['content']}")
        continue
    elif parsed_response['step'] == 'ANSWER':
        print(f"The current weather of {parsed_response['city']} is {parsed_response['weather_condition']}.")
        break