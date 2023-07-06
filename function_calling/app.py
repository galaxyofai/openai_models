import os
import openai
import json 

from dotenv import load_dotenv,find_dotenv
__ = load_dotenv(find_dotenv()) #read local .env file
openai.api_key=os.environ["OPENAI_API_KEY"]







def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "39", # set by us
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)
    


def first_response(user_text):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
       
        {"role": "user", "content": user_text}
    ],
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. bangalore, Delhi",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    ]
    )
    result=completion.choices[0]['message']
    print("Answer>>>>>>",result)
    return result

def second_response(first_res_data,function_args):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        first_res_data,
       {
                "role": "function",
                "name": first_res_data["function_call"]["name"],
                "content": get_current_weather(
            location=function_args.get("location"),
            unit=function_args.get("unit"),),
        }

    ],
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. Gujarat, delhi",
                    },
                    
                },
                "required": ["location"],
            },
        }
    ]
    )
    result2=completion.choices[0]['message']
    print("Answer>>>>>>",result2)
    return result2



if __name__=='__main__':
    question="what is the temprature in mumbai"
    first_response_data=first_response(question)
    function_args = json.loads(first_response_data["function_call"]["arguments"])
    num_addition=second_response(first_response_data,function_args)

