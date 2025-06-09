import time
import psutil
import pyautogui
from src.utils.recoder import listen
from src.utils.ai import AI

from src.plugin.load_plugins import load_plugins
DEV = True


def dispatch(intent, param):
    plugins = load_plugins()
    value = ""
    for plugin in plugins:
        print(value)
        if plugin.can_run(intent):
           value =  plugin.run(param)
    return value

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

    ai = AI("mistral", "jarvis/src/prompts/system_prompt.txt")
    response = ai.get_intent(prompt)
    print(response)
    functions_list = response.get("function_called", dict())

    print(functions_list)
    result = ""
    
    for action in functions_list:
        for key, value in action.items():
            result = result + str(dispatch(key.lower().strip(), value))
                       


    final_result = f"The result of the action is the following data:\n{result}"

    
    user_res = f"""
    memory: {""}
    function response: {final_result}
    """

    print(user_res)

if __name__ == "__main__":
    main()
