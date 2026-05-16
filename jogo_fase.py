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

    nivel_agua = 520
    gravidade = 0.8
    forca_pulo = -15
    class Dora:
        def __init__(self, pedra_inicial):
            self.image = dora_img
            self.rect = self.image.get_rect()
            self.rect.mindbottom = pedra_inicial.rect.midtop
            self.velocidade = 5
            self.velocidade_y = 0
            self.no_chao = True
            self.ultima_pedra = pedra_inicial
        def mover (self, teclas, pedras):
            if teclas [pygame.K_LEFT]:
                self.rect.x -= self.velocidade
            if teclas [pygame.K_RIGHT]:
                self.rect.x += self.velocidade
            if teclas[pygame.K_UP] and self.no_chao:
                self.velocidade_y = forca_pulo
                self.no_chao = False
            self.velocidade_y += gravidade
            self.rect.y += int(self.velocidade_y)

            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > LARGURA:
                self.rect.right = LARGURA
            self.no_chao = False
            if self.velocidade_y >= 0:
                for pedra in pedras:
                    if self.rect.colliderect(pedra.rect):
                        pes_anteriores = self.rect.bottom - int(self.velocidade_y)
                        if pes_anteriores <= pedra.rect.top + 10:
                            self.rect.bottom = pedra.rect.top
                            self.velocidade_y = 0
                            self.no_chao = True
                            self.ultima_pedra = pedra
                            break    
        
            
