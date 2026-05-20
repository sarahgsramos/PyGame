import pygame 
import random


def fase_jogo(tela):
    LARGURA, ALTURA = 1100, 700
    clock = pygame.time.Clock()
    pygame.display.set_caption("Dora no rio")
    fundo = pygame.image.load("imagens/fundo_rio.png")
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
    dora_img = pygame.image.load("imagens/dora.png")
    dora_img = pygame.transform.scale_by(dora_img, 0.07)
    pedra_img = pygame.image.load("imagens/pedras.png")
    pedra_img = pygame.transform.scale(pedra_img, (60, 50))
    pedra_grande_img = pygame.image.load("imagens/pedras.png")
    pedra_grande_img = pygame.transform.scale(pedra_grande_img, (200, 120))
    peixe_img = pygame.image.load("imagens/peixe.png")
    peixe_img = pygame.transform.scale(peixe_img, (40, 25))
    raposo_img = pygame.image.load("imagens/raposo.png")
    raposo_img = pygame.transform.scale(raposo_img, (60, 60))
    botas_img = pygame.image.load("imagens/botas.png")
    botas_img = pygame.transform.scale(botas_img, (90, 90))
    fonte = pygame.font.SysFont("arial", 30, True)
    sprite_parada = pygame.image.load("imagens/parada.png").convert()
    sprite_parada.set_colorkey((73,182,182))
    sprite_andando = pygame.image.load("imagens/andando.png").convert()
    sprite_andando.set_colorkey((73,182,182))

    FRAME_W_AND, FRAME_H_AND = sprite_andando.get_width()//12, 55
    andando_img_list = [sprite_andando.subsurface((i*FRAME_W_AND, 0, FRAME_W_AND, FRAME_H_AND)) for i in range(12)]
    FRAME_W_PAR, FRAME_H_PAR = sprite_parada.get_width()//3, 55
    parada_img_list = [sprite_parada.subsurface((i*FRAME_W_PAR,0,FRAME_W_PAR, FRAME_H_PAR)) for i in range(3)]
    
    largura_mundo = 4000
    nivel_agua = 550
    gravidade = 0.8
    forca_pulo = -16

    class Dora:

        def __init__(self, pedra_inicial):
            self.image = parada_img_list[0]
            self.rect = self.image.get_rect()
            self.rect.midbottom = pedra_inicial.rect.midtop
            self.velocidade = 5
            self.velocidade_x = 0
            self.velocidade_y = 0
            self.no_chao = True
            self.ultima_pedra = pedra_inicial
            self.img_index = 1
            self.troca = 0

        def animar (self):
            if self.velocidade_x != 0:
                frames = andando_img_list
            else:
                frames = parada_img_list
            self.troca +=1
            if self.troca >= 16:
                self.troca = 0
                self.img_index += 1
            if self.img_index >= len(frames):
                self.img_index = 0
            self.image = frames [self.img_index]
            

        def mover (self, teclas, pedras_todas):
            self.velocidade_x  = 0
            if teclas [pygame.K_LEFT]:
                self.velocidade_x -= self.velocidade
            if teclas [pygame.K_RIGHT]:
                self.velocidade_x += self.velocidade
            self.rect.x += self.velocidade_x
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
                pes_rect = self.rect
                for pedra in pedras_todas:
                    topo_pedra = pedra.rect
                    if pes_rect.colliderect(topo_pedra) and self.rect.bottom < topo_pedra.bottom:
                            self.rect.bottom = topo_pedra.top 
                            self.velocidade_y = 0
                            self.no_chao = True
                            self.ultima_pedra = pedra
                            break 
            self.animar()

        def caiu_na_agua (self): 
            return self.rect.bottom > nivel_agua + 100
        
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
            tela.blit(self.image, (self.rect.x - camera_x, self.rect.y))
           
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
            self.velocidade_y = -random.uniform(7,10)
            self.gravidade = 0.35
                
        def mover (self):
            self.velocidade_y += self.gravidade
            self.rect.y += int(self.velocidade_y)

            if self.rect.top > nivel_agua + 30:
                self.rect.x = self.x_inicial
                self.rect.y = nivel_agua + 20
                self.velocidade_y = -random.uniform(6,8)
        
        def desenhar (self, tela, camera_x):
            tela.blit(self.image, (self.rect.x - camera_x, self.rect.y))
            
    posicoes_pedras_grandes = [940, 1740, 2700]  
 
    pedras_normais = []
    x = 40
    while x < 3950:
        perto_de_grande = any(abs(x - pg) < 90 or abs(pg+200 - (x+60)) < 90 for pg in posicoes_pedras_grandes)
        print(x, posicoes_pedras_grandes, perto_de_grande)
        if not perto_de_grande:
            pedras_normais.append(Pedra(x))
        x += 200

    pedras_normais.append(Pedra(3870))
 
    pedras_grandes = [PedraGrande(pg_x) for pg_x in posicoes_pedras_grandes]

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
        print(f"dora.top={dora.rect.top} | nivel_agua={nivel_agua} | no_chao={dora.no_chao} | vidas={vidas}")
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
        
        teclas = pygame.key.get_pressed()

        dora.mover(teclas, todas_pedras)

        for f in peixes :
            f.mover()
        if invencivel >0:
            invencivel -= 1
        if dora.caiu_na_agua():
            if invencivel == 0:
                vidas -= 1
                invencivel = 60
            dora.voltar_checkpoint()
            if vidas <= 0:
                return "derrota"
        if invencivel == 0:
            for obs in raposos + peixes:
                if dora.rect.colliderect(obs.rect):
                    vidas -= 1
                    invencivel = 60
                    dora.voltar_checkpoint()
                    if vidas <= 0:
                        return "derrota"
                    break

        if dora.rect.colliderect(botas):
            return "vitoria"
        
        camera_x = dora.rect.centerx - LARGURA // 2
        if camera_x < 0:
            camera_x = 0
        if camera_x > largura_mundo - LARGURA:
            camera_x = largura_mundo - LARGURA

        primeira_tile = (camera_x // LARGURA) * LARGURA
        for i in range(3):
            x_tile = primeira_tile + i * LARGURA - camera_x
            tela.blit(fundo, (x_tile,0))

        for pedra in todas_pedras:
            pedra.desenhar(tela,camera_x)

        tela.blit(botas_img, (botas.x - camera_x, botas.y))

        for f in peixes:
            f.desenhar(tela,camera_x)
        
        for r in raposos:
            r.desenhar(tela, camera_x)

        dora.desenhar(tela, camera_x)

        sombra = fonte.render(f"Vidas: {vidas}", True, (0,0,0))
        texto = fonte.render(f"Vidas: {vidas}", True, (255,255,255))

        tela.blit(sombra, (22,22))
        tela.blit(texto,(20,20))

        pygame.display.flip()