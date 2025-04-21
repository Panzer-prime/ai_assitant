from src.utils.recoder import listen
from src.utils.ai import AI
from src.skills.search import Search
import datetime


DEV = True


def main():
    if not DEV:
        voice_command = listen()
        if not voice_command: 
            print("couldnt get the voicew")
    
    ai = AI("mistral", "src/system_prompt.md")
    command = input("what is your command? ")

    # response = ai.get_intent(command)

    # if response["action"]["type"] == "search_internet":
    #     pass
 
    search = Search(command)
    print(search.search())

    print(ai.get_ai_response("search in the given data for any information related with the following querry creating a short summary: " + command + " the the data is the following: " ,"".join(search.search())))



main()