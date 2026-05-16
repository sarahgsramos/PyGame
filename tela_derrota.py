import pygame  
import sys
pygame.init()




def tela_derrota(tela):
    LARGURA, ALTURA = 1100, 700
    pygame.display.set_caption("Dora não conseguiu resgar o Botas!")
    clock = pygame.time.Clock()

    # Imagem de fundo
    fundo = pygame.image.load("imagens/fundo_derrota.png")
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

    # Música
    pygame.mixer.music.load("aúdios/musica_dora.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    fonte = pygame.font.SysFont("arial", 50, True)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"

            if evento.type == pygame.KEYDOWN:
                return "inicio"

        
        tela.blit(fundo, (0, 0))
      

        pygame.display.flip()
        clock.tick(60)