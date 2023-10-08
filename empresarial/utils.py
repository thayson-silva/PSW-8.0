from random import choice, shuffle
import string
import os
from django.conf import settings
from django.template.loader import render_to_string
from io import BytesIO
from weasyprint import HTML

def gerar_senha_aleatoria(tamanho):

    caracteres_especiais = string.punctuation   
    caracteres = string.ascii_letters
    numeros_list = string.digits

    
    qtd = tamanho // 3
    sobra = tamanho % 3

    # letras = ''
    # for i in range(0, qtd + sobra):
    #     letras += choice(caracteres)
    letras = [choice(caracteres) for i in range(0, qtd + sobra)]
    numeros = [choice(numeros_list) for i in range(0, qtd)]
    especiais = [choice(caracteres_especiais) for i in range(0, qtd)]
    
    senha = list(letras + numeros + especiais)
    shuffle(senha)

    return ''.join(senha)


def gerar_pdf_exames(exame, paciente, senha):

    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/senha_exame.html')
    template_render = render_to_string(path_template, {'exame': exame, 'paciente': paciente, 'senha': senha})

    path_output = BytesIO()

    HTML(string=template_render).write_pdf(path_output)
    path_output.seek(0)
    
    return path_output

if __name__ == '__main__':
    print(gerar_senha_aleatoria(5))