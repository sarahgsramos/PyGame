from tela_inicial import tela_inicial
from tela_vitoria import tela_vitoria
from tela_derrota import tela_derrota
from jogo_fase import fase_jogo
import pygame
import sys
pygame.init()
 
 
LARGURA, ALTURA = 1100, 700
tela = pygame.display.set_mode((LARGURA, ALTURA))
estado = "inicio"
 
while True:
    if estado == "inicio":
        estado = tela_inicial(tela)
        if estado == "fase":
            estado = "jogo"
    elif estado == "jogo":
        estado = fase_jogo(tela)
    elif estado == "vitoria":
        estado = tela_vitoria(tela)
    elif estado == "derrota":
        estado = tela_derrota(tela)
    elif estado == "sair":
        break
 
pygame.quit()
sys.exit()
