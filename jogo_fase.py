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
        
        def caiu_na_agua (self): 
            return self.rect.bottom > nivel_agua
        
        def voltar_checkpoint (self):
            self.rect.midbottom = self.ultima_pedra.rect.midtop
            self.velocidade_y = 0
            self.no_chao = True
        
        def desenhar (self, tela):
            tela.blit(self.image, self.rect)
    
    class Pedra:
        
        def __init__(self, x, y):
            self.image = pedra_img
            self.rect = self.image.get_rect(topleft=(x,y))
        
        def desenhar (self, tela):
            tela.blit(self.image, self.rect)
    
    class Obstaculo:
        
        def __init__(self, imagem, x, y, velocidade):
            self.image = imagem
            self.rect = self.image.get_rect(topleft = (x,y))
            self.velocidade = velocidade
        
        def mover(self):
            self.rect.x -= self.velocidade
        
        def desenhar (self, tela):
            tela.blit(self.image, self.rect)

    pedras = [
        Pedra(40, 480),
        Pedra(200,450),
        Pedra(360,490),
        Pedra(520,440),
        Pedra(680,480),
        Pedra(820,450),
        Pedra(960,480),
    ]

    dora = Dora(pedras[0])

    vidas = 3

    invencivel = 0

    obstaculos = [
        Obstaculo(peixe_img, 700, 300,6),
        Obstaculo(raposo_img, 1200, 250, 4),
        Obstaculo(peixe_img,1600,320,5),
        Obstaculo(raposo_img, 2000, 280,5),
    ]

    botas = botas_img.get.rect()
    botas.midbottom = pedras[-1].rect.midtop

    while True:
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
        
        teclas = pygame.key.get_pressed()

        dora.mover(teclas,pedras)

        for obstaculo in obstaculos:
            obstaculo.mover()

        if invencivel > 0:
            invencivel -= 1

        if dora.caiu_na_agua():
            if invencivel == 0: 
                vidas  -= 1
                invencivel = 60

            dora.voltar_checkpoint()

            if vidas <= 0:
                return "derrota"
            
        if invencivel == 0:
            for obstaculo in obstaculos:
                if dora.rect.colliderect(obstaculo.rect):
                    vidas -= 1
                    invencivel = 60
                    dora.voltar_checkpoint()

                    if vidas <= 0:
                        return "derrota"
                    break 
        
        if dora.rect.colliderect(botas):
            return "vitoria"
            
        tela.blit(fundo,(0,0))

        for pedra in pedras:
            pedra.desenhar(tela)

        tela.blit(botas_img,botas)

        for obstaculo in obstaculos:
            obstaculo.desenhar(tela)

        dora.desenhar(tela)

        sombra = fonte.render(f"Vidas: {vidas}", True, (0,0,0))
        texto = fonte.render(f"Vidas: {vidas}", True, (255,255,255))
        tela.blit(sombra, (22,22))
        tela.blit(texto,(20,20))

        pygame.display.flip()  
      
        
            
