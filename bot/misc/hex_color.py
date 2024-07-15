import random

def gerar_cor_hex():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))