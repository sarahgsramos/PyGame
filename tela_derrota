import pygame  
import sys
pygame.init()


LARGURA, ALTURA = 1100, 700
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Dora não conseguiu resgar o Botas!")
clock = pygame.time.Clock()

# Imagem de fundo
fundo = pygame.image.load("imagens/fundo_derrota.png")
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

# Música
pygame.mixer.music.load("aúdios/musica_dora.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

def tela_derrota():
    fonte = pygame.font.SysFont("arial", 50, True)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"

            if evento.type == pygame.KEYDOWN:
                return "inicio"

        tela.fill((255, 180, 180))
        texto = fonte.render("Você perdeu!", True, (0, 0, 0))
        tela.blit(texto, (380, 300))

        pygame.display.flip()
        clock.tick(60)