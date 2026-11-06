import math
import os
import sys

import pygame

# CONFIGURAÇÃO

pygame.init()

LARGURA = 960
ALTURA = 540
FPS = 60

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Meu Jogo")

clock = pygame.time.Clock()


# TELAS


MENU = "menu"
OPCOES = "opcoes"
JOGO = "jogo"

tela_atual = MENU

# CORES

MADEIRA = (174, 96, 45)
MADEIRA_HOVER = (190, 110, 55)
MADEIRA_BORDA = (91, 48, 25)
MADEIRA_DETALHE = (111, 57, 27)

CREME = (255, 238, 202)
SOMBRA_TEXTO = (72, 38, 20)

PAINEL = (36, 28, 21)
PAINEL_BORDA = (184, 113, 62)

BRANCO = (255, 255, 255)
CORDA = (101, 71, 39)

# FONTES


def carregar_fonte(tamanho):
    caminho = pygame.font.match_font("dejavusans", bold=True)

    if caminho:
        return pygame.font.Font(caminho, tamanho)

    return pygame.font.Font(None, tamanho)


fonte_botao = carregar_fonte(36)
fonte_titulo = carregar_fonte(48)
fonte_texto = carregar_fonte(28)


# ARQUIVOS


PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))


def encontrar_arquivo(nome):
    caminhos = (
        os.path.join(PASTA_PROJETO, nome),
        os.path.join(PASTA_PROJETO, "assets", nome),
    )

    for caminho in caminhos:
        if os.path.exists(caminho):
            return caminho

    return None


def carregar_imagem(nome, tamanho, alpha=False):
    caminho = encontrar_arquivo(nome)

    if caminho is None:
        print(f"ERRO: {nome} não encontrado!")
        print("Coloque o arquivo na pasta do projeto ou em assets.")
        pygame.quit()
        sys.exit()

    imagem = pygame.image.load(caminho)

    if alpha:
        imagem = imagem.convert_alpha()
    else:
        imagem = imagem.convert()

    return pygame.transform.smoothscale(imagem, tamanho)


cenario = carregar_imagem(
    "cenario.png",
    (LARGURA, ALTURA)
)

personagem = carregar_imagem(
    "personagem.png",
    (72, 72),
    alpha=True
)

# BOTÕES


botao_start = pygame.Rect(605, 190, 250, 65)
botao_opcoes = pygame.Rect(605, 275, 250, 65)

botao_som = pygame.Rect(305, 195, 350, 65)
botao_fullscreen = pygame.Rect(305, 275, 350, 65)
botao_voltar = pygame.Rect(305, 355, 350, 65)

# CONFIGURAÇÕES


som_ativado = True
fullscreen = False



# BALANÇO


PONTO_ESQUERDO = (402, 128)
PONTO_DIREITO = (481, 128)

COMPRIMENTO_CORDA = 176

ASSENTO_LARGURA = 82
ASSENTO_ALTURA = 13

ANGULO_MAXIMO = 3.2
VELOCIDADE_BALANCO = 1.15

tempo_inicio = pygame.time.get_ticks()


def calcular_balanco():
    tempo = (
        pygame.time.get_ticks() - tempo_inicio
    ) / 1000

    angulo = math.sin(
        tempo * VELOCIDADE_BALANCO
    ) * ANGULO_MAXIMO

    radianos = math.radians(angulo)

    deslocamento_x = (
        math.sin(radianos) * COMPRIMENTO_CORDA
    )

    deslocamento_y = (
        COMPRIMENTO_CORDA
        * (1 - math.cos(radianos))
    )

    esquerda = (
        PONTO_ESQUERDO[0] + deslocamento_x,
        PONTO_ESQUERDO[1]
        + COMPRIMENTO_CORDA
        - deslocamento_y
    )

    direita = (
        PONTO_DIREITO[0] + deslocamento_x,
        PONTO_DIREITO[1]
        + COMPRIMENTO_CORDA
        - deslocamento_y
    )

    centro = (
        (esquerda[0] + direita[0]) / 2,
        (esquerda[1] + direita[1]) / 2
    )

    return angulo, esquerda, direita, centro


def desenhar_balanco():
    angulo, esquerda, direita, centro = calcular_balanco()

    pygame.draw.line(
        tela,
        CORDA,
        PONTO_ESQUERDO,
        (int(esquerda[0]), int(esquerda[1])),
        2
    )

    pygame.draw.line(
        tela,
        CORDA,
        PONTO_DIREITO,
        (int(direita[0]), int(direita[1])),
        2
    )

    personagem_girado = pygame.transform.rotate(
        personagem,
        -angulo
    )

    personagem_rect = personagem_girado.get_rect(
        center=(
            int(centro[0]),
            int(centro[1] - 38)
        )
    )

    tela.blit(
        personagem_girado,
        personagem_rect
    )

    desenhar_assento(
        angulo,
        centro
    )


def desenhar_assento(angulo, centro):
    assento = pygame.Surface(
        (ASSENTO_LARGURA, ASSENTO_ALTURA),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        assento,
        (151, 82, 37),
        (0, 2, ASSENTO_LARGURA, ASSENTO_ALTURA - 2),
        border_radius=3
    )

    pygame.draw.line(
        assento,
        (205, 123, 63),
        (4, 3),
        (ASSENTO_LARGURA - 4, 3),
        2
    )

    pygame.draw.line(
        assento,
        MADEIRA_BORDA,
        (4, ASSENTO_ALTURA - 1),
        (ASSENTO_LARGURA - 4, ASSENTO_ALTURA - 1),
        2
    )

    assento = pygame.transform.rotate(
        assento,
        -angulo
    )

    rect = assento.get_rect(
        center=(int(centro[0]), int(centro[1]))
    )

    tela.blit(assento, rect)


# DESENHO

def desenhar_cenario():
    tela.blit(cenario, (0, 0))


def desenhar_texto(texto, fonte, cor, centro):
    imagem = fonte.render(
        texto,
        True,
        cor
    )

    tela.blit(
        imagem,
        imagem.get_rect(center=centro)
    )


def desenhar_botao(rect, texto, fonte=fonte_botao):
    hover = rect.collidepoint(pygame.mouse.get_pos())

    cor = MADEIRA_HOVER if hover else MADEIRA

    desenho = rect.copy()

    if hover:
        desenho.inflate_ip(6, 4)
        desenho.y -= 2

    pygame.draw.rect(
        tela,
        MADEIRA_BORDA,
        desenho.move(0, 6),
        border_radius=18
    )

    pygame.draw.rect(
        tela,
        cor,
        desenho,
        border_radius=18
    )

    pygame.draw.rect(
        tela,
        MADEIRA_BORDA,
        desenho,
        width=4,
        border_radius=18
    )

    pygame.draw.circle(
        tela,
        MADEIRA_DETALHE,
        (desenho.x + 15, desenho.centery),
        6
    )

    pygame.draw.circle(
        tela,
        MADEIRA_DETALHE,
        (desenho.right - 15, desenho.centery),
        6
    )

    pygame.draw.line(
        tela,
        MADEIRA_DETALHE,
        (desenho.x + 20, desenho.y + 18),
        (desenho.x + 70, desenho.y + 18),
        2
    )

    pygame.draw.line(
        tela,
        MADEIRA_DETALHE,
        (desenho.right - 70, desenho.bottom - 18),
        (desenho.right - 20, desenho.bottom - 18),
        2
    )

    desenhar_texto(
        texto,
        fonte,
        SOMBRA_TEXTO,
        (
            desenho.centerx + 2,
            desenho.centery + 3
        )
    )

    desenhar_texto(
        texto,
        fonte,
        CREME,
        desenho.center
    )


def desenhar_overlay(opacidade):
    overlay = pygame.Surface(
        (LARGURA, ALTURA),
        pygame.SRCALPHA
    )

    overlay.fill((0, 0, 0, opacidade))

    tela.blit(overlay, (0, 0))


# MENU

def desenhar_menu():
    desenhar_cenario()
    desenhar_balanco()

    desenhar_botao(
        botao_start,
        "START"
    )

    desenhar_botao(
        botao_opcoes,
        "OPÇÕES"
    )


# OPÇÕES


def desenhar_opcoes():
    desenhar_cenario()
    desenhar_overlay(115)

    painel = pygame.Rect(
        250,
        80,
        460,
        380
    )

    pygame.draw.rect(
        tela,
        PAINEL,
        painel,
        border_radius=24
    )

    pygame.draw.rect(
        tela,
        PAINEL_BORDA,
        painel,
        width=5,
        border_radius=24
    )

    desenhar_texto(
        "OPÇÕES",
        fonte_titulo,
        CREME,
        (painel.centerx, painel.y + 55)
    )

    texto_som = (
        "SOM: LIGADO"
        if som_ativado
        else "SOM: DESLIGADO"
    )

    texto_fullscreen = (
        "JANELA"
        if fullscreen
        else "TELA CHEIA"
    )

    desenhar_botao(
        botao_som,
        texto_som,
        fonte_texto
    )

    desenhar_botao(
        botao_fullscreen,
        texto_fullscreen,
        fonte_texto
    )

    desenhar_botao(
        botao_voltar,
        "VOLTAR",
        fonte_texto
    )

# JOGO

def desenhar_jogo():
    desenhar_cenario()
    desenhar_overlay(65)

    desenhar_texto(
        "JOGO INICIADO",
        fonte_titulo,
        CREME,
        (LARGURA // 2, 100)
    )

    desenhar_texto(
        "ESC para voltar ao menu",
        fonte_texto,
        BRANCO,
        (LARGURA // 2, ALTURA - 55)
    )

# CONTROLES

def alternar_fullscreen():
    global tela
    global fullscreen

    fullscreen = not fullscreen

    flags = pygame.FULLSCREEN if fullscreen else 0

    tela = pygame.display.set_mode(
        (LARGURA, ALTURA),
        flags
    )


def voltar_ao_menu():
    global tela_atual
    tela_atual = MENU


def tratar_tecla(tecla):
    global rodando

    if tecla == pygame.K_ESCAPE:

        if tela_atual == MENU:
            rodando = False
        else:
            voltar_ao_menu()

    elif tecla == pygame.K_F11:
        alternar_fullscreen()


def tratar_clique_menu(pos):
    global tela_atual

    if botao_start.collidepoint(pos):
        tela_atual = JOGO

    elif botao_opcoes.collidepoint(pos):
        tela_atual = OPCOES


def tratar_clique_opcoes(pos):
    global som_ativado

    if botao_som.collidepoint(pos):
        som_ativado = not som_ativado

    elif botao_fullscreen.collidepoint(pos):
        alternar_fullscreen()

    elif botao_voltar.collidepoint(pos):
        voltar_ao_menu()


def tratar_clique(pos):
    if tela_atual == MENU:
        tratar_clique_menu(pos)

    elif tela_atual == OPCOES:
        tratar_clique_opcoes(pos)


def tratar_eventos():
    global rodando

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        elif evento.type == pygame.KEYDOWN:
            tratar_tecla(evento.key)

        elif (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
        ):
            tratar_clique(evento.pos)

# TELA ATUAL


def desenhar_tela():
    telas = {
        MENU: desenhar_menu,
        OPCOES: desenhar_opcoes,
        JOGO: desenhar_jogo,
    }

    telas[tela_atual]()

# LOOP PRINCIPAL

rodando = True

while rodando:
    tratar_eventos()
    desenhar_tela()

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
sys.exit()