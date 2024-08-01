from bot import *
import inquirer
from bot.varas_dict import varas
from clear import clear
from datetime import datetime
from termcolor import colored

clear()

def set_prompt():
    
    choices = list(varas())
    choices.append("Todas")
    question_juiz = [
    inquirer.List(
            'vara',
            carousel=True,
            message=colored("Escolha a Vara", "green", attrs=["bold", "underline"]),
            choices=choices,
        )
    ]
    answer_vara = inquirer.prompt(question_juiz)
    
    clear()
    
    answer_data_inicio = input(colored("Informe a data inicial (separado por '/'): ", attrs=["bold", "underline"], color="blue"))
    answer_data_fim = input(colored("Informe a data final (separado por '/'): ", attrs=["bold", "underline"], color="blue"))
    
    answer_data_inicio = datetime.strptime(answer_data_inicio.replace(" ", "").replace("/", "-"), '%d-%m-%Y')
    answer_data_fim = datetime.strptime(answer_data_fim.replace(" ", "").replace("/", "-"), '%d-%m-%Y')
    
    escolha = str(answer_vara.get("vara"))
    
    start = ExtractPauta(answer_vara.get("vara"), answer_data_inicio, answer_data_fim)
    
    if escolha == "Todas":
    
        start.execution2()
    
    else:
        start.execution()
    
    
set_prompt()

