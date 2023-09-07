from .title import title
from .transcribe import transcribe_speech as ts
from colorama import Fore
from .overview import Overview
import os
from prettytable import PrettyTable
from .conversation import Conversation

class Menu:
    invalid = f"{Fore.RED} Invalid input. Please try again.{Fore.GREEN}"
    options1 = f"""
    1. Transcribe Conversation
    2. View Conversations
    3. Reset Conversations
    4. Exit
    """
    user_input = ''
 
    def run(self):
        os.system('clear')
        print(title)
        self.main_menu()

    def main_menu(self):
        while True:
            possible_inputs = {
                "1": self.transcribe,
                "2": self.view,
                "3": self.reset,
                "4": self.exit
            }
            print(self.options1)
            self.user_input = input(">>> ")

            if self.user_input in possible_inputs:
                possible_inputs[self.user_input]()
            else:
                print(self.invalid)

            if self.user_input == '4':
                break

    def transcribe(self):
        os.system('clear')
        ts()

    def view(self):
        overview_table = PrettyTable()
        col_names = ["ID","Title","Summary", "Timestamp"]
        overview_table.field_names = col_names
        overview_table.max_width["Summary"] = 75
        overviews = Overview.fetch_overviews()
        for overview in overviews:
            overview_table.add_row(overview)
        print(overview_table)

        while True:
            print("Type X to go back, the convsation ID for more details or delete {id} to delete the conversation")
            self.user_input = input(">>> ")

            if("delete" in self.user_input.lower()):
                try:
                    id = self.user_input.split(" ")[1]
                    Conversation.delete_convo(id)
                
                except:
                    print("Invalid Input")


            elif("export" in self.user_input.lower()):
                # TODO export convos as files

                try:
                    id = self.user_input.split(" ")[1]
                    
                
                except:
                    print("Invalid Input")

            elif(self.user_input != 'x'):
                convo_table = PrettyTable()
                convo_table.field_names = ["Timestamp", "Text"]
                convo = Overview.fetch_conversation(int(self.user_input))
                for row in convo:
                    convo_table.add_row([row[1],row[3]])
                print(convo_table)

            elif(self.user_input.lower() == 'x'):
                self.user_input = 1
                break
            else:
                print(self.invalid)



    def reset(self):
        pass

    def exit(self):
        pass

    





