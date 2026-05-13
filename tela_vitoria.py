import pygame  
import sys



def tela_vitoria (tela):
    pygame.display.set_caption("Dora resgatou o Botas!")
    LARGURA, ALTURA = 1100, 700
    clock = pygame.time.Clock()

    # Música
    pygame.mixer.music.load("aúdios/musica_dora.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # Imagem de fundo
    fundo = pygame.image.load("imagens/fundo_vitoria.png")
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

    fonte = pygame.font.SysFont("arial",50,True)
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            if evento.type == pygame.KEYDOWN:
                return "inicio"
        tela.fill((200,255,200))
        tela.blit(fundo, (0, 0))
       
        pygame.display.flip()
        clock.tick(60)