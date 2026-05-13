import pygame
import sys

pygame.init()

# Tela
LARGURA, ALTURA = 1100, 700
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Dora Aventureira: Resgatando o Botas")
clock = pygame.time.Clock()

# Imagem de fundo
fundo = pygame.image.load("imagens/fundo_inicio.png")
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

# Música
pygame.mixer.music.load("aúdios/musica_dora.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  

def tela_inicial():

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return "inicio"

        tela.blit(fundo, (0, 0))

        pygame.display.flip()
        clock.tick(60)

# chama a tela inicial
