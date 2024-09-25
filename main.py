from bot import *
import inquirer
from bot.varas_dict import varas
from clear import clear
from datetime import datetime
from termcolor import colored
import pytz
clear()


def set_prompt():

    choices = list(varas())
    choices.append("Todas")
    question_juiz = [
        inquirer.List(
            'vara',
            carousel=True,
            message=colored("Escolha a Vara", "green",
                            attrs=["bold", "underline"]),
            choices=choices,
        )
    ]
    answer_vara = inquirer.prompt(question_juiz)

    clear()

    credential = None
    questions_loadpw = None

    credentials = os.path.join(os.getcwd(), "credentials.json")
    if os.path.exists(credentials):
        with open(credentials, "rb") as f:
            credential = json.load(f)
        questions_loadpw = [
            inquirer.Confirm(
                "loadpw", message="Carregar senha salva?", default=False)
        ]

    questions_date = [
        inquirer.Text(
            "data_inicio", message="Informe a data inicial (separado por '/')"),
        inquirer.Text(
            "data_fim", message="Informe a data final (separado por '/')"
        )
    ]

    dates = inquirer.prompt(questions_date)

    clear()
    questions_pw = [
        inquirer.Text(
            "usuario", message="Usuário"),
        inquirer.Text(
            "senha", message="Senha"
        )]
    questions_savepw = [
            inquirer.Confirm(
                "savecred", message="Salvar senha?", default=False),
        ]
    
    if not questions_loadpw:

        creds = inquirer.prompt(questions_pw)
        savecreds = inquirer.prompt(questions_savepw)
        if savecreds.get("savecred") is True:
            with open(credentials, 'w', encoding='utf-8') as file:
                json.dump(creds, file, ensure_ascii=False, indent=4)
                
    elif questions_loadpw:

        loadpw = inquirer.prompt(questions_loadpw)
        if loadpw is True:
            usuario = credential.get("usuario")
            senha = credential.get("senha")
            
        elif loadpw is False:
            creds = inquirer.prompt(questions_pw)
            usuario = creds.get("usuario")
            senha = creds.get("senha")
            savecreds = inquirer.prompt(questions_savepw)
            if savecreds.get("savecred") is True:
                with open(credentials, 'w', encoding='utf-8') as file:
                    json.dump(creds, file, ensure_ascii=False, indent=4)

    data_inicio = datetime.now(pytz.timezone('Etc/GMT+4'))
    if dates.get("data_inicio", None):
        data_inicio = datetime.strptime(dates.get("data_inicio").replace(" ", "").replace("/", "-"), '%d-%m-%Y')
    
    if not dates.get("data_fim", None):
        
        print(colored("Informe a data final!", "red"))
        return    
    
    data_fim = datetime.strptime(dates.get("data_fim").replace(" ", "").replace("/", "-"), '%d-%m-%Y')
    
    escolha = str(answer_vara.get("vara"))

    start = ExtractPauta(answer_vara.get(
        "vara"), data_inicio, data_fim, usuario, senha)

    if escolha == "Todas":

        start.execution2()

    else:
        start.execution()
    

    pass


set_prompt()
