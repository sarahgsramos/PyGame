import pygame 
import random
from tela_inicial import tela_inicial
from tela_vitoria import tela_vitoria
from tela_derrota import tela_derrota

def fase_jogo(tela):
    LARGURA, ALTURA = 1100, 700
    clock = pygame.time.Clock()
    pygame.display.set_caption("Dora no rio")
    fundo = pygame.image.load("imagens/fundo_rio.png")
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
    dora_img = pygame.image.load("imagens/dora.png")
    dora_img = pygame.transform.scale(dora_img, (80, 80))
    pedra_img = pygame.image.load("imagens/pedras.png")
    pedra_img = pygame.transform.scale(pedra_img, (90, 60))
    peixe_img = pygame.image.load("imagens/peixe.png")
    peixe_img = pygame.transform.scale(peixe_img, (70, 45))
    raposo_img = pygame.image.load("imagens/raposo.png")
    raposo_img = pygame.transform.scale(raposo_img, (90, 90))
    botas_img = pygame.image.load("imagens/botas.png")
    botas_img = pygame.transform.scale(botas_img, (90, 90))
    fonte = pygame.font.SysFont("arial", 30, True)

    class Dora:
        def __init__(self):
            self.image = dora_img
            self.rect = self.image.get_rect()
            self.rect.x = 60
            self.rect.y = 300
            self.velocidade = 5
        def mover(self, teclas):
            if teclas[pygame.K_UP]:
                self.rect.y -= self.velocidade
            
