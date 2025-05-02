import datetime
from src.utils.recoder import listen
from src.utils.ai import AI
from src.skills.search import Search
from src.skills.weather import Weather
DEV = True


def get_user_prompt():
    if DEV:
        return input("What is your command? ")
    else:
        voice_command = listen()
        if not voice_command:
            print("Couldn't get the voice command.")
            return None
        return voice_command

def main():
    prompt = get_user_prompt()
    if not prompt:
        return

    ai = AI("mistral", "src/prompts/system_prompt.txt")
    response = ai.get_intent(prompt)
    print(response)
    functions_list = response.get("function_called", dict())

    print(functions_list)
    result = ""
    
    for action in functions_list:
        for key, value in action.items():
            if "search" in key.lower():
                search = Search()
                content = search.search(value)

                if len(content) > 5000:
                    content = content[:5000]

                result += content

            if "weather" in key.lower():
                weather = Weather()
                result += weather.get_weather(value)


    final_result = f"The result of the action is the following data:\n{result}"

    ai_personality = ""

    user_res = f"""
    memory: {""}
    function response: {final_result}
    """

    print(user_res)

if __name__ == "__main__":
    main()
