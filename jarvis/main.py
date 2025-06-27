from src.utils.recoder import listen
from src.utils.ai import AI
from src.utils.utils import create_availble_functions
from src.plugin.load_plugins import fetch_runner_refs
DEV = True



def get_user_prompt():
    if DEV:
        return input("What is your command? ")
    else:
        voice_command = listen()
        if not voice_command:
            print("Couldn't get the voice command.")
            return ""
        return voice_command

def main():
    
    Ai = AI("mistral", "jarvis/src/prompts/system_prompt.txt")    
    prompt = get_user_prompt()
    
    tools = fetch_runner_refs()
    available_functions = create_availble_functions()

    tools_called, content = Ai.get_ai_response(prompt, tools)

    for tool in tools_called:

        function_to_call = available_functions.get(tool.function.name)
        if function_to_call:
            print('Function output:', function_to_call(**tool.function.arguments))
        else:
            print('Function not found:', tool.function.name)
                       


   

    
    user_res = f"""
    memory: {""}
    function response: {final_result}
    """

    print(user_res)

if __name__ == "__main__":
    main()


