import pygame 
import random


def fase_jogo(tela):
    """
    Executa a fase principal do jogo "Dora no rio".

    Nesta fase, a personagem Dora deve atravessar pedras sobre um rio,
    evitando obstáculos como peixes e raposos, até alcançar as botas
    no final do percurso.

    Funcionalidades principais:
    - Carrega imagens, sons e sprites de animação;
    - Cria o cenário, pedras, inimigos e personagem;
    - Controla movimentação, pulo e gravidade;
    - Detecta colisões com obstáculos e água;
    - Gerencia vidas, efeitos sonoros e reinício após colisão;
    - Implementa câmera lateral acompanhando a personagem;
    - Verifica condições de vitória e derrota.

    Parâmetros:
        tela (pygame.Surface):
            Superfície principal do pygame onde os elementos do jogo
            serão desenhados.

    Retorno:
        str:
            - "vitoria":quando Dora alcança as botas;
            - "derrota":quando as vidas acabam;
            - "sair": quando o jogador fecha a janela do jogo.
    """
     
    LARGURA, ALTURA = 1100, 700
    clock = pygame.time.Clock()
    pygame.display.set_caption("Dora no rio")
    fundo = pygame.image.load("imagens/fundo_rio.png")
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
    tronco_img = pygame.image.load("imagens/tronco.png")
    tronco_img = pygame.transform.scale(tronco_img, (40, 25))
    tronco_grande_img = pygame.image.load("imagens/tronco.png")
    tronco_grande_img = pygame.transform.scale(tronco_grande_img, (200, 60))
    peixe_img = pygame.image.load("imagens/peixe.png")
    peixe_img = pygame.transform.scale(peixe_img, (30, 20))
    raposo_img = pygame.image.load("imagens/raposo.png")
    raposo_img = pygame.transform.scale(raposo_img, (50, 50))
    botas_img = pygame.image.load("imagens/botas.png")
    botas_img = pygame.transform.scale(botas_img, (60, 60))
    fonte = pygame.font.SysFont("arial", 30, True)
    som_colisao = pygame.mixer.Sound("aúdios/colisao.mp3")
    som_colisao.set_volume(0.7)
    som_mergulho = pygame.mixer.Sound("aúdios/mergulho.mp3")
    som_mergulho.set_volume(0.8)
    som_pulo = som_pulo = pygame.mixer.Sound("aúdios/pulo.mp3")
    som_pulo.set_volume(0.6)
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
        """
    Representa a personagem principal controlada pelo jogador.

    Responsável pela movimentação, animação, física,
    colisões e reposicionamento da personagem.
    """

        def __init__(self, tronco_inicial):
            """
    Inicializa a personagem Dora.

    Define posição inicial, velocidades,
    animações e tronco seguro inicial.

    Parâmetros:
        tronco_inicial:
            Tronco onde Dora começa a fase.
    """
            self.image = parada_img_list[0]
            self.rect = self.image.get_rect()
            self.rect.midbottom = tronco_inicial.rect.midtop
            self.velocidade = 5
            self.velocidade_x = 0
            self.velocidade_y = 0
            self.no_chao = True
            self.ultimo_tronco = tronco_inicial
            self.indice_tronco = 0
            self.img_index = 1
            self.troca = 0

        def animar (self):
            """
    Atualiza a animação da personagem.

    Alterna entre sprites de parada e caminhada
    de acordo com o movimento horizontal.
    """
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
            """
    Move a personagem no cenário.

    Aplica movimentação lateral, pulo,
    gravidade e colisão com os troncos.

    Parâmetros:
        teclas:
            Teclas pressionadas pelo jogador.

        pedras_todas:
            Lista com todas as pedras do cenário.
    """
            self.velocidade_x  = 0
            if teclas [pygame.K_LEFT]:
                self.velocidade_x -= self.velocidade
            if teclas [pygame.K_RIGHT]:
                self.velocidade_x += self.velocidade
            self.rect.x += self.velocidade_x
            if teclas[pygame.K_UP] and self.no_chao:
                self.velocidade_y = forca_pulo
                self.no_chao = False
                som_pulo.play()
            self.velocidade_y += gravidade
            self.rect.y += int(self.velocidade_y)

            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > largura_mundo:
                self.rect.right = largura_mundo
            self.no_chao = False
            if self.velocidade_y >= 0:
                for i, tronco in enumerate(todos_troncos):
                    if self.rect.colliderect(tronco.rect):
                        pes_anteriores = self.rect.bottom - int(self.velocidade_y)
                        if pes_anteriores <= tronco.rect.top + 10:
                            self.rect.bottom = tronco.rect.top
                            self.velocidade_y = 0
                            self.no_chao = True
                            self.ultimo_tronco = tronco
                            self.indice_tronco = i
                            break

            self.animar()

        def caiu_na_agua (self):
            """
    Verifica se Dora caiu na água.

    Retorno:
        bool:
            True se Dora caiu na água.
            False caso contrário.
    """
            return self.rect.bottom > nivel_agua + 100
        
        def voltar_na_agua(self):
            """
    Reposiciona Dora no último tronco seguro
    após cair na água.
    """
            self.rect.bottomleft = self.ultimo_tronco.rect.topleft
            self.velocidade_y = 0
            self.no_chao = True
        def voltar_no_obstaculo (self, todos_troncos):
            """
    Reposiciona Dora após colisão com obstáculo.

    Move a personagem para o tronco anterior seguro.

    Parâmetros:
        todos_troncos:
            Lista de troncos do cenário.
    """
            if self.indice_tronco >0:
                tronco_seguro = todos_troncos[self.indice_tronco - 1]
            else:
                tronco_seguro = self.ultima_pedra
            self.rect.bottomleft = tronco_seguro.rect.topleft
            self.velocidade_y = 0
            self.no_chao = True
        
        def desenhar (self, tela, camera_x):
            """
    Desenha Dora na tela considerando a câmera.

    Parâmetros:
        tela:
            Superfície principal do pygame.

        camera_x:
            Posição horizontal da câmera.
    """
            tela.blit(self.image, (self.rect.x - camera_x, self.rect.y))
            

    class Tronco:
    
        
        def __init__(self, x):
            """
    Cria um tronco em uma posição horizontal.

    Parâmetros:
        x (int):
            Posição horizontal do tronco.
    """
            self.image = tronco_img
            self.rect = self.image.get_rect()
            self.rect.x = x 
            self.rect.top = nivel_agua
        
        def desenhar (self, tela, camera_x):
            """
    Desenha o tronco na tela.

    Parâmetros:
        tela:
            Superfície principal do pygame.

        camera_x:
            Posição horizontal da câmera.
    """
            tela.blit(self.image, (self.rect.x - camera_x, self.rect.y))
            

    class TroncoGrande:
        """
    Representa um tronco grande do cenário.

    Alguns troncos grandes possuem um raposo
    posicionados sobre eles.
    """
        def __init__(self, x):
            """
    Cria um tronco grande em uma posição horizontal.

    Parâmetros:
        x (int):
            Posição horizontal do tronco.
    """
            self.image = tronco_grande_img
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.top = nivel_agua 
        

        def desenhar (self, tela, camera_x):
            """
    Desenha o tronco grande na tela.

    Parâmetros:
        tela:
            Superfície principal do pygame.

        camera_x:
            Posição horizontal da câmera.
    """
            tela.blit(self.image, (self.rect.x - camera_x, self.rect.y))
           
    class Raposo:
        """
    Representa o inimigo raposo.

    O jogador perde vida ao colidir com ele.
    """
        
        def __init__(self, tronco_grande):
            """
    Posiciona o raposo sobre um tronco grande.

    Parâmetros:
        tronco_grande:
            Tronco onde o raposo vai estar.
    """
            self.image = raposo_img
            self.rect = self.image.get_rect()
            self.rect.midbottom = tronco_grande.rect.midtop
        
        def desenhar (self, tela, camera_x):
            """
    Desenha o raposo na tela.

    Parâmetros:
        tela:
            Superfície principal do pygame.

        camera_x:
            Posição horizontal da câmera.
    """
            tela.blit(self.image, (self.rect.x - camera_x, self.rect.y))
            
    class Peixe:
        """
    Representa o peixe que pula da água.

    O peixe funciona como obstáculo móvel.
    """
        def __init__(self, x):
            """
    Inicializa um peixe em determinada posição.

    Parâmetros:
        x (int):
            Posição horizontal inicial do peixe.
    """
            self.image = peixe_img
            self.rect = self.image.get_rect()
            self.x_inicial = x
            self.rect.x = x
            self.rect.y = nivel_agua + 20
            self.velocidade_y = -random.uniform(12,14)
            self.gravidade = 0.35
                
        def mover (self):
            """
    Atualiza o movimento do peixe.

    Aplica gravidade e reinicia o salto
    quando o peixe retorna para a água.
    """
            self.velocidade_y += self.gravidade
            self.rect.y += int(self.velocidade_y)

            if self.rect.top > nivel_agua + 30:
                self.rect.x = self.x_inicial
                self.rect.y = nivel_agua + 20
                self.velocidade_y = -random.uniform(12,14)
        
        def desenhar (self, tela, camera_x):
            """
    Desenha o peixe na tela.

    Parâmetros:
        tela:
            Superfície principal do pygame.

        camera_x:
            Posição horizontal da câmera.
    """
            tela.blit(self.image, (self.rect.x - camera_x, self.rect.y))
            
    posicoes_troncos_grandes = [940, 1740, 2400]  
 
    troncos_normais = []
    x = 40
    while x < 3950:
        perto_de_grande = any(abs(x - pg) < 90 or abs(pg+200 - (x+60)) < 90 for pg in posicoes_troncos_grandes)
        print(x, posicoes_troncos_grandes, perto_de_grande)
        if not perto_de_grande:
            troncos_normais.append(Tronco(x))
        x += 200

    troncos_normais.append(Tronco(3870))
 
    troncos_grandes = [TroncoGrande(pg_x) for pg_x in posicoes_troncos_grandes]

    todos_troncos = sorted(troncos_normais + troncos_grandes, key = lambda p: p.rect.x)

    raposos = [Raposo(troncos_grandes[1]), Raposo(troncos_grandes[2])]

    peixes = [
        Peixe (530),
        Peixe (1130),
        Peixe (1530),
        Peixe (2130),
        Peixe (2950),
        Peixe (3330),
        Peixe (3550)
    ]


    dora = Dora(troncos_normais[0])

    botas = botas_img.get_rect()
    botas.midbottom = troncos_normais[-1].rect.midtop

    vidas = 3

    em_efeito = False
    tipo_efeito = None 
    inicio_efeito = 0
    duracao_efeito = 0
    
    def iniciar_efeito(som, tipo):
        """
    Inicia o efeito de colisão ou queda na água.

    Reproduz o som correspondente, reduz vidas
    e ativa o estado temporário de efeito.

    Parâmetros:
        som:
            Som que será reproduzido.

        tipo (str):
            Tipo do efeito:
            "agua" ou "obstaculo".
    """
        nonlocal em_efeito, inicio_efeito, duracao_efeito, vidas, tipo_efeito
        som.play()
        vidas -= 1
        em_efeito = True
        tipo_efeito = tipo
        inicio_efeito = pygame.time.get_ticks()
        duracao_efeito = max(450, int(som.get_length()*1000))

    while True:
        clock.tick(60)
        # Verifica eventos da janela do jogo
        for evento in pygame.event.get():
            # Fecha o jogo quando o jogador clica no botão de sair
            if evento.type == pygame.QUIT:
                return "sair"
        
        teclas = pygame.key.get_pressed()
        agora = pygame.time.get_ticks()
         # Verifica se algum efeito de colisão está ativo
        if em_efeito :
             # Aguarda o tempo do efeito terminar
            if agora - inicio_efeito >= duracao_efeito:
                # Retorna Dora após cair na água
                if tipo_efeito == "agua":
                    dora.voltar_na_agua()
                # Retorna Dora após colisão com obstáculo
                else:
                    dora.voltar_no_obstaculo(todos_troncos)
                em_efeito = False  # Desativa o efeito atual
               
                if vidas <= 0: #verifica se o jogador perdeu todas as vidas
                    return "derrota"
        # Executa atualizações normais enquanto não há efeitos ativos
        else:
            dora.mover (teclas, todos_troncos)
            # Atualiza o movimento dos peixes
            for f in peixes:
                f.mover()
            # Verifica se Dora caiu na água
            if dora.caiu_na_agua():
                iniciar_efeito(som_mergulho, "agua")
            # Verifica colisão com obstáculos
            else:
                for obs in raposos + peixes:
                     # Inicia efeito de colisão ao tocar em inimigos
                    if dora.rect.colliderect(obs.rect):
                        iniciar_efeito(som_colisao, "obstaculo")
                        break
        
        # Verifica se Dora encontrou o botas
        if dora.rect.colliderect(botas):
            return "vitoria"
        # Centraliza a câmera na posição horizontal de Dora
        camera_x = dora.rect.centerx - LARGURA // 2
        # Impede que a câmera ultrapasse o início do cenário
        if camera_x < 0:
            camera_x = 0
        # Impede que a câmera ultrapasse o final do cenário
        if camera_x > largura_mundo - LARGURA:
            camera_x = largura_mundo - LARGURA

        primeira_tile = (camera_x // LARGURA) * LARGURA
        for i in range(3):
            x_tile = primeira_tile + i * LARGURA - camera_x
            tela.blit(fundo, (x_tile,0))

        for pedra in todos_troncos:
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

        pedra 