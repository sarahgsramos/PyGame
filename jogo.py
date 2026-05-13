from telas import tela_inicial
from tela_vitoria import tela_vitoria

estado = "inicio"
while True:
    if estado == "inicio":
        estado = tela_inicial()
    elif estado == "jogo":
        print("jogo rodando")
        break
    elif estado == "sair":
        break
