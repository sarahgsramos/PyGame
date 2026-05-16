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
            if teclas[pygame.K_DOWN]:
                self.rect.y += self.velocidade
            if teclas[pygame.K_LEFT]:
                self.rect.x -= self.velocidade
            if teclas[pygame.K_RIGHT]:
                self.rect.x += self.velocidade
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > LARGURA:
                self.rect.right = LARGURA
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > ALTURA:
                self.rect.bottom = ALTURA

        def desenhar(self, tela):
            tela.blit(self.image, self.rect)
        
    class Obstaculo:
        def __init__(self, imagem, x, y, velocidade):
            self.image = imagem
            self.rect = self.image.get_rect(topleft=(x, y))
            self.velocidade = velocidade

        def mover(self):
            self.rect.x -= self.velocidade
            if self.rect.right < 0:
                self.rect.x = LARGURA + random.randint(100, 400)
                self.rect.y = random.randint(180, 600)
        
        def desenhar(self, tela):
            tela.blit(self.image, self.rect)

    dora = Dora()
    vidas = 3
    invencivel = 0
    obstaculos = [
        Obstaculo(pedra_img, 500, 500, 4),
        Obstaculo(peixe_img, 800, 300, 6),
        Obstaculo(pedra_img, 1100, 430, 5),
        Obstaculo(raposo_img, 1400, 450, 4),
    ]

    botas = botas_img.get_rect()
    botas.x = 1900
    botas.y = 500

    while True:
        clock.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
        teclas = pygame.key.get_pressed()
        dora.mover(teclas)
        for obstaculo in obstaculos:
            obstaculo.mover()
        if invencivel > 0:
            invencivel -= 1
        
            
