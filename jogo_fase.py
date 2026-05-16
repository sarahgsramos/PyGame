import pygame 
import random


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
    pedra_grande_img = pygame.image.load("imagens/pedras.png")
    pedra_grande_immg = pygame.transform.scale(pedra_grande_img, (200,90))
    peixe_img = pygame.image.load("imagens/peixe.png")
    peixe_img = pygame.transform.scale(peixe_img, (70, 45))
    raposo_img = pygame.image.load("imagens/raposo.png")
    raposo_img = pygame.transform.scale(raposo_img, (90, 90))
    botas_img = pygame.image.load("imagens/botas.png")
    botas_img = pygame.transform.scale(botas_img, (90, 90))
    fonte = pygame.font.SysFont("arial", 30, True)
    largura_mundo = 4000
    nivel_agua = 520
    gravidade = 0.8
    forca_pulo = -16

    class Dora:

        def __init__(self, pedra_inicial):
            self.image = dora_img
            self.rect = self.image.get_rect()
            self.rect.midbottom = pedra_inicial.rect.midtop
            self.velocidade = 5
            self.velocidade_y = 0
            self.no_chao = True
            self.ultima_pedra = pedra_inicial

        def mover (self, teclas, pedras_todas):
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
            if self.rect.right > largura_mundo:
                self.rect.right = largura_mundo
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
            return self.rect.top > nivel_agua
        
        def voltar_checkpoint (self):
            self.rect.midbottom = self.ultima_pedra.rect.midtop
            self.velocidade_y = 0
            self.no_chao = True
        
        def desenhar (self, tela, camera_x):
            tela.blit(self.image, (self.rect.x - camera_x, self.rect.y))
    
    class Pedra:
        
        def __init__(self, x):
            self.image = pedra_img
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.top = nivel_agua
        
        def desenhar (self, tela, camera_x):
            tela.blit(self.image, (self.rect.x - camera_x, self.rect.y))

    class PedraGrande:
        def __init__(self, x):
            self.image = pedra_grande_img
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.top = nivel_agua
        

        def desenhar (self, tela, camera_x):
            tela.blit(self.image, (self.rect.x -camera_x, self.rect.y))
    
    
    class Raposo:
        
        def __init__(self, pedra_grande):
            self.image = raposo_img
            self.rect = self.image.get_rect()
            self.rect.midbottom = pedra_grande.rect.midtop
        
        def desenhar (self, tela, camera_x):
            tela.blit(self.image, (self.rect.x - camera_x, self.rect.y))
        
    class Peixe:
        def __init__(self, x):
            self.image = peixe_img
            self.rect = self.image.get_rect()
            self.x_inicial = x
            self.rect.x = x
            self.rect.y = nivel_agua + 20
            self.velocidade_y = -random.uniform(11,14)
            self.gravidade = 0.45
            self.velocidade_x = - random.uniform(0.5, 1.5)
        
        def mover (self):
            self.rect.x += self.velocidade_x
            self.velocidade_y += self.gravidade
            self.rect.y += int(self.velocidade_y)

            if self.rect.top > nivel_agua + 30:
                self.rect.x = self.x_inicial
                self.rect.y = nivel_agua + 20
                self.velocidade_y = -random.uniform(11,14)
                self.velocidade_x = -random.uniform (0.5, 1.5)
        def desenhar (self, tela, camera_x):
            tela.blit(self.image, (self.rect.x - camera_x, self.rect.y))

    pedras_normais = [
        Pedra(40),
        Pedra (220),
        Pedra (400),
        Pedra (580),
        Pedra (760), 
        Pedra (1180), 
        Pedra (1360),
        Pedra (1540),
        Pedra(1980),
        Pedra(2160),
        Pedra(2340),
        Pedra(2520),
        Pedra(2960),
        Pedra(3140),
        Pedra(3320),
        Pedra(3500),
        Pedra(3680),
        Pedra(3870),
    ]

    pedras_grandes = [
        PedraGrande(940),
        Pedra(1740), 
        PedraGrande(2720)
    ]

    todas_pedras = pedras_normais + pedras_grandes
    raposos = [Raposo(pg) for pg in pedras_grandes]
    peixes = [
        Peixe (500),
        Peixe (1100),
        Peixe (1500),
        Peixe (2100),
        Peixe(2500),
        Peixe(3000),
        Peixe (3400),
        Peixe (3700)
    ]


    dora = Dora(pedras_normais[0])

    botas = botas_img.get_rect()
    botas.midbottom = pedras_normais[-1].rect.midtop

    vidas = 3
    invencivel = 0


    while True:
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
        
        teclas = pygame.key.get_pressed()

        dora.mover(teclas, todas_pedras)

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
      
        
            
