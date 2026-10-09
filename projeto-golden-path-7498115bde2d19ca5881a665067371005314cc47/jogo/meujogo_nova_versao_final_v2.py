import pygame
import sys
import os
import math

# =========================================================
# INICIALIZAÇÃO
# =========================================================

pygame.init()

# =========================================================
# CONFIGURAÇÃO DE DIRETÓRIOS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJETO_DIR = os.path.dirname(BASE_DIR)
AVATARES_DIR = os.path.join(PROJETO_DIR, "avatares")

# =========================================================
# TELA
# =========================================================

info = pygame.display.Info()

LARGURA = info.current_w
ALTURA = info.current_h

tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
pygame.display.set_caption("Jogo com Escolha de Avatar")

relogio = pygame.time.Clock()

TAMANHO = 100

# =========================================================
# FUNÇÃO PARA CARREGAR AVATAR
# =========================================================

def carregar_avatar(prefixo, inverter_original=False):

    frames_walk_base = []

    # =====================================================
    # CARREGAR FRAMES DE CAMINHADA
    # =====================================================

    try:
        arquivos = sorted(os.listdir(AVATARES_DIR))
    except:
        arquivos = []

    for nome in arquivos:

        if (
            nome.lower().startswith(
                prefixo.lower() + "frame"
            )
            and nome.lower().endswith(".png")
        ):

            try:
                caminho = os.path.join(
                    AVATARES_DIR,
                    nome
                )

                img = pygame.image.load(
                    caminho
                ).convert_alpha()

                img = pygame.transform.scale(
                    img,
                    (TAMANHO, TAMANHO)
                )

                frames_walk_base.append(img)

            except:
                continue

    # =====================================================
    # CASO NÃO ENCONTRE OS FRAMES
    # =====================================================

    if not frames_walk_base:

        try:
            caminho = os.path.join(
                AVATARES_DIR,
                prefixo + "frame0.png"
            )

            img = pygame.image.load(
                caminho
            ).convert_alpha()

            img = pygame.transform.scale(
                img,
                (TAMANHO, TAMANHO)
            )

            frames_walk_base = [img]

        except:

            fallback = pygame.Surface(
                (TAMANHO, TAMANHO),
                pygame.SRCALPHA
            )

            fallback.fill(
                (255, 0, 0, 255)
            )

            frames_walk_base = [fallback]

    # =====================================================
    # CARREGAR UMA IMAGEM INDIVIDUAL
    # =====================================================

    def carregar_unico(nome_arquivo):

        try:
            caminho = os.path.join(
                AVATARES_DIR,
                nome_arquivo + ".png"
            )

            img = pygame.image.load(
                caminho
            ).convert_alpha()

            return pygame.transform.scale(
                img,
                (TAMANHO, TAMANHO)
            )

        except:
            return frames_walk_base[0]

    # =====================================================
    # IMAGENS BASE
    # =====================================================

    idle_base = carregar_unico(
        prefixo + "frame0"
    )

    pulo_base = carregar_unico(
        prefixo + "pulo"
    )

    caindo_base = carregar_unico(
        prefixo + "caindo"
    )

    caida_base = carregar_unico(
        prefixo + "caida"
    )

    preparar_base = carregar_unico(
        prefixo + "preparandopulo"
    )

    # =====================================================
    # AGACHADO
    #
    # Avatar 2:
    # avatar2agachado.png
    #
    # Outros:
    # avatar1abaixado.png
    # avatar3abaixado.png
    # avatar4abaixado.png
    # =====================================================

    if prefixo.lower() == "avatar2":

        abaixado_base = carregar_unico(
            prefixo + "agachado"
        )

    else:

        abaixado_base = carregar_unico(
            prefixo + "abaixado"
        )


    
    # =====================================================
    # AUMENTAR PULO E AGACHAMENTO DO AVATAR 2
    # =====================================================

    if prefixo.lower() == "avatar2":
        TAMANHO_ESPECIAL = 130

        # Aumenta somente o frame de pulo
        pulo_base = pygame.transform.scale(
            pulo_base,
            (TAMANHO_ESPECIAL, TAMANHO_ESPECIAL)
        )

        # Aumenta somente o frame de agachamento
        abaixado_base = pygame.transform.scale(
            abaixado_base,
            (TAMANHO_ESPECIAL, TAMANHO_ESPECIAL)
        )

    # =====================================================
    # DIREÇÃO DO AVATAR
    # =====================================================

    if inverter_original:

        frames_walk_dir = frames_walk_base

        frames_walk_esq = [
            pygame.transform.flip(
                frame,
                True,
                False
            )
            for frame in frames_walk_base
        ]

    else:

        frames_walk_esq = frames_walk_base

        frames_walk_dir = [
            pygame.transform.flip(
                frame,
                True,
                False
            )
            for frame in frames_walk_base
        ]

    # =====================================================
    # RETORNAR TODAS AS IMAGENS
    # =====================================================

    return {

        # -------------------------------------------------
        # WALK
        # -------------------------------------------------

        "walk_esq": frames_walk_esq,
        "walk_dir": frames_walk_dir,

        # -------------------------------------------------
        # IDLE
        # -------------------------------------------------

        "idle_esq": (
            pygame.transform.flip(
                idle_base,
                True,
                False
            )
            if inverter_original
            else idle_base
        ),

        "idle_dir": (
            idle_base
            if inverter_original
            else pygame.transform.flip(
                idle_base,
                True,
                False
            )
        ),

        # -------------------------------------------------
        # PULO
        # -------------------------------------------------

        "pulo_esq": (
            pygame.transform.flip(
                pulo_base,
                True,
                False
            )
            if inverter_original
            else pulo_base
        ),

        "pulo_dir": (
            pulo_base
            if inverter_original
            else pygame.transform.flip(
                pulo_base,
                True,
                False
            )
        ),

        # -------------------------------------------------
        # CAINDO
        # -------------------------------------------------

        "caindo_esq": (
            pygame.transform.flip(
                caindo_base,
                True,
                False
            )
            if inverter_original
            else caindo_base
        ),

        "caindo_dir": (
            caindo_base
            if inverter_original
            else pygame.transform.flip(
                caindo_base,
                True,
                False
            )
        ),

        # -------------------------------------------------
        # CAÍDA
        # -------------------------------------------------

        "caida_esq": (
            pygame.transform.flip(
                caida_base,
                True,
                False
            )
            if inverter_original
            else caida_base
        ),

        "caida_dir": (
            caida_base
            if inverter_original
            else pygame.transform.flip(
                caida_base,
                True,
                False
            )
        ),

        # -------------------------------------------------
        # PREPARANDO PULO
        # -------------------------------------------------

        "preparar_esq": (
            pygame.transform.flip(
                preparar_base,
                True,
                False
            )
            if inverter_original
            else preparar_base
        ),

        "preparar_dir": (
            preparar_base
            if inverter_original
            else pygame.transform.flip(
                preparar_base,
                True,
                False
            )
        ),

        # -------------------------------------------------
        # AGACHADO
        # -------------------------------------------------

        "abaixado_esq": (
            pygame.transform.flip(
                abaixado_base,
                True,
                False
            )
            if inverter_original
            else abaixado_base
        ),

        "abaixado_dir": (
            abaixado_base
            if inverter_original
            else pygame.transform.flip(
                abaixado_base,
                True,
                False
            )
        )
    }


# =========================================================
# CARREGAMENTO DOS AVATARES
# =========================================================

avatar1 = carregar_avatar(
    "avatar1",
    inverter_original=True
)

avatar2 = carregar_avatar(
    "avatar2",
    inverter_original=False
)

avatar3 = carregar_avatar(
    "avatar3",
    inverter_original=False
)

avatar4 = carregar_avatar(
    "avatar4",
    inverter_original=False
)

lista_avatares = [
    avatar1,
    avatar2,
    avatar3,
    avatar4
]

# =========================================================
# CARREGAR CENÁRIO
# =========================================================

def carregar_fundo(nome):

    # Primeiro tenta dentro da pasta do jogo

    caminho = os.path.join(
        BASE_DIR,
        nome
    )

    # Se não encontrar, tenta na pasta principal

    if not os.path.exists(caminho):

        caminho = os.path.join(
            PROJETO_DIR,
            nome
        )

    try:

        fundo = pygame.image.load(
            caminho
        ).convert()

        fundo = pygame.transform.scale(
            fundo,
            (
                LARGURA,
                ALTURA
            )
        )

        return fundo

    except:

        fundo = pygame.Surface(
            (
                LARGURA,
                ALTURA
            )
        )

        fundo.fill(
            (255, 192, 203)
        )

        return fundo


fundo = carregar_fundo(
    "cenario1.png"
)


# =========================================================
# CONFIGURAÇÃO DO MENU DE AVATARES
# =========================================================

# ---------------------------------------------------------
# FUNDO DO MENU — menos desfoque
# ---------------------------------------------------------

fundo_menu = pygame.image.load(
    os.path.join(
        PROJETO_DIR,
        "fundos",
        "fundo_menu.png"
    )
).convert()

fundo_menu = pygame.transform.scale(
    fundo_menu,
    (LARGURA, ALTURA)
)

# Desfoque bem leve, mantendo o cenário reconhecível.
fundo_pequeno = pygame.transform.smoothscale(
    fundo_menu,
    (
        max(1, LARGURA // 18),
        max(1, ALTURA // 18)
    )
)

fundo_menu_blur = pygame.transform.smoothscale(
    fundo_pequeno,
    (LARGURA, ALTURA)
)


# =========================================================
# FONTE COM ESTÉTICA PIXEL
# =========================================================

# Procura uma fonte pixel instalada no computador.
# Se não existir, usa Consolas sem antialias.
fontes_pixel = [
    "pressstart2p",
    "silkscreen",
    "04b03",
    "joystix",
    "visitor",
    "arcade",
    "munro",
    "pixel",
    "consolas"
]

nome_fonte_pixel = "consolas"

for nome_fonte in fontes_pixel:
    if pygame.font.match_font(nome_fonte):
        nome_fonte_pixel = nome_fonte
        break

tamanho_fonte_titulo = max(
    22,
    int(ALTURA * 0.030)
)

fonte_titulo = pygame.font.SysFont(
    nome_fonte_pixel,
    tamanho_fonte_titulo,
    bold=True
)

fonte_menu = pygame.font.SysFont(
    nome_fonte_pixel,
    max(14, int(ALTURA * 0.019)),
    bold=True
)

fonte_pequena = pygame.font.SysFont(
    nome_fonte_pixel,
    max(11, int(ALTURA * 0.015)),
    bold=True
)


# =========================================================
# CORES DA ESTÉTICA
# =========================================================

DOURADO = (218, 170, 55)
DOURADO_CLARO = (255, 220, 110)

MADEIRA_ESCURO = (67, 39, 22)
MADEIRA = (104, 62, 32)
MADEIRA_CLARO = (139, 87, 43)

FOLHA_ESCURA = (42, 82, 38)
FOLHA = (73, 118, 52)
FOLHA_CLARA = (117, 151, 62)

CREME = (247, 230, 178)


# =========================================================
# DESENHAR FOLHA PIXEL
# =========================================================

def desenhar_folha_pixel(superficie, x, y, tamanho, cor=FOLHA):

    tamanho = max(4, int(tamanho))

    # Haste
    pygame.draw.rect(
        superficie,
        FOLHA_ESCURA,
        (
            int(x + tamanho * 0.45),
            int(y + tamanho * 0.45),
            max(2, tamanho // 5),
            max(3, tamanho)
        )
    )

    # Corpo da folha
    pontos = [
        (int(x + tamanho * 0.50), int(y)),
        (int(x + tamanho), int(y + tamanho * 0.25)),
        (int(x + tamanho * 0.82), int(y + tamanho * 0.75)),
        (int(x + tamanho * 0.30), int(y + tamanho * 0.65)),
        (int(x), int(y + tamanho * 0.30))
    ]

    pygame.draw.polygon(
        superficie,
        cor,
        pontos
    )

    # Brilho pixelado
    pygame.draw.rect(
        superficie,
        FOLHA_CLARA,
        (
            int(x + tamanho * 0.30),
            int(y + tamanho * 0.25),
            max(2, tamanho // 5),
            max(2, tamanho // 5)
        )
    )


# =========================================================
# MOLDURA DE MADEIRA
# =========================================================

def desenhar_moldura_madeira(superficie, rect, dourada=False):

    pygame.draw.rect(
        superficie,
        MADEIRA_ESCURO,
        rect
    )

    margem = max(4, rect.height // 16)

    pygame.draw.rect(
        superficie,
        MADEIRA,
        rect.inflate(
            -margem * 2,
            -margem * 2
        )
    )

    # Linhas das tábuas
    for deslocamento in range(18, rect.height, 28):

        pygame.draw.line(
            superficie,
            MADEIRA_CLARO,
            (
                rect.left + 10,
                rect.top + deslocamento
            ),
            (
                rect.right - 10,
                rect.top + deslocamento
            ),
            2
        )

    if dourada:

        pygame.draw.rect(
            superficie,
            DOURADO,
            rect,
            width=5
        )

        pygame.draw.rect(
            superficie,
            DOURADO_CLARO,
            rect.inflate(-8, -8),
            width=2
        )

    else:

        pygame.draw.rect(
            superficie,
            (44, 29, 19),
            rect,
            width=4
        )


# =========================================================
# PAINEL DE MADEIRA
# =========================================================

def desenhar_painel_madeira(superficie, rect):

    desenhar_moldura_madeira(
        superficie,
        rect,
        dourada=False
    )

    canto = max(5, rect.height // 18)

    cantos = [
        (
            rect.left + 8,
            rect.top + 8
        ),
        (
            rect.right - 8 - canto,
            rect.top + 8
        ),
        (
            rect.left + 8,
            rect.bottom - 8 - canto
        ),
        (
            rect.right - 8 - canto,
            rect.bottom - 8 - canto
        )
    ]

    for px, py in cantos:

        pygame.draw.rect(
            superficie,
            DOURADO,
            (
                px,
                py,
                canto,
                canto
            )
        )


# =========================================================
# TEXTO PIXELADO
# =========================================================

def desenhar_texto_pixel(
    superficie,
    texto,
    fonte,
    centro,
    cor=CREME,
    sombra=True
):

    if sombra:

        sombra_img = fonte.render(
            texto,
            False,
            (28, 18, 10)
        )

        sombra_rect = sombra_img.get_rect(
            center=(
                centro[0] + 3,
                centro[1] + 3
            )
        )

        superficie.blit(
            sombra_img,
            sombra_rect
        )

    texto_img = fonte.render(
        texto,
        False,
        cor
    )

    texto_rect = texto_img.get_rect(
        center=centro
    )

    superficie.blit(
        texto_img,
        texto_rect
    )


# =========================================================
# FOLHAS CAINDO — REMOVIDAS
# =========================================================
# As folhas agora são apenas elementos decorativos presos às madeiras.
# Não existe mais animação de folhas caindo pela tela.

def atualizar_folhas_menu(tempo_atual):
    pass


def desenhar_folhas_menu(superficie):
    pass


# =========================================================
# POSIÇÃO DOS QUATRO AVATARES
# =========================================================

tamanho_botao = int(
    ALTURA * 0.155
)

espaco_botoes = int(
    ALTURA * 0.022
)

inicio_x = int(
    LARGURA * 0.56
)

inicio_y = int(
    ALTURA * 0.30
)

posicoes_botoes = [
    (
        inicio_x,
        inicio_y
    ),
    (
        inicio_x + tamanho_botao + espaco_botoes,
        inicio_y
    ),
    (
        inicio_x,
        inicio_y + tamanho_botao + espaco_botoes
    ),
    (
        inicio_x + tamanho_botao + espaco_botoes,
        inicio_y + tamanho_botao + espaco_botoes
    )
]

botoes = []

for x, y in posicoes_botoes:

    botoes.append(
        pygame.Rect(
            x,
            y,
            tamanho_botao,
            tamanho_botao
        )
    )


# =========================================================
# AVATAR PRINCIPAL
# =========================================================

# Menor e mais próximo do canto inferior esquerdo.
tamanho_avatar_grande = int(
    ALTURA * 0.43
)

avatar_escolhido = lista_avatares[3]

escolhendo_avatar = True


# =========================================================
# CONTROLES DA ANIMAÇÃO
# =========================================================

tempo_inicio_oi = pygame.time.get_ticks()
duracao_oi = 1800

tempo_ultimo_piscar = pygame.time.get_ticks()
intervalo_piscar = 3500
duracao_piscada = 180

esta_piscando = False
inicio_piscada = 0


# =========================================================
# MENSAGEM DE BLOQUEIO
# =========================================================

mensagem_bloqueado = ""

tempo_mensagem_bloqueado = 0

duracao_mensagem_bloqueado = 1800


# =========================================================
# FUNÇÕES DOS AVATARES
# =========================================================

def pegar_imagem_avatar(
    avatar,
    piscando=False
):

    if (
        piscando
        and "blink_dir" in avatar
    ):

        return avatar["blink_dir"]

    return avatar["idle_dir"]


def pegar_frame_oi(
    avatar,
    tempo
):

    if "wave_dir" in avatar:

        frames_oi = avatar["wave_dir"]

        if len(frames_oi) > 0:

            velocidade = 160

            indice = int(
                tempo / velocidade
            ) % len(frames_oi)

            return frames_oi[indice]

    return avatar["idle_dir"]



# =========================================================
# CONFIGURAÇÕES FINAIS DO MENU
# =========================================================

avatar_escolhido = lista_avatares[3]
modo_menu = True


# =========================================================
# MENU — ESTILO PIXEL ART DA REFERÊNCIA
# =========================================================

# A referência usa uma composição bem definida:
#   • cenário desfocado ocupando toda a tela;
#   • personagem grande no canto inferior esquerdo;
#   • placa de título centralizada no alto;
#   • grande painel de madeira no lado direito;
#   • quatro placas penduradas dentro do painel;
#   • botão CONTINUAR no canto inferior direito.
# Todas as medidas abaixo são proporcionais à tela para manter a aparência
# mesmo quando o jogo for executado em outra resolução.

DOURADO = (214, 164, 70)
DOURADO_CLARO = (255, 219, 128)
DOURADO_SOMBRA = (125, 76, 30)

MADEIRA_QUASE_PRETA = (38, 20, 11)
MADEIRA_ESCURO = (67, 34, 16)
MADEIRA = (112, 61, 28)
MADEIRA_CLARA = (151, 86, 39)
MADEIRA_LUZ = (183, 109, 52)

FOLHA_ESCURA = (25, 54, 20)
FOLHA = (58, 108, 40)
FOLHA_CLARA = (111, 155, 61)
CREME = (250, 232, 177)
PRETO_PIXEL = (31, 17, 8)


def desenhar_retangulo_pixel(superficie, rect, cor, borda=None, largura=0, sombra=True):
    """Retângulo em camadas, imitando UI pixel-art sem antialias."""
    if sombra:
        pygame.draw.rect(superficie, (22, 12, 6), rect.move(6, 7))

    pygame.draw.rect(superficie, cor, rect)

    if borda:
        pygame.draw.rect(superficie, borda, rect, width=max(1, largura))


def desenhar_folha_pixel(superficie, x, y, tamanho, cor=FOLHA):
    """Folha decorativa mais orgânica, porém ainda totalmente pixel-art."""
    tamanho = max(8, int(tamanho))
    w = max(6, tamanho)
    h = max(8, int(tamanho * 1.55))
    x = int(x)
    y = int(y)

    # Contorno escuro em formato de folha pontuda.
    contorno = [
        (x + w//2, y),
        (x + w - 2, y + h//3),
        (x + w - 5, y + h*2//3),
        (x + w//2 + 2, y + h),
        (x + w//2 - 2, y + h - 3),
        (x + 4, y + h*2//3),
        (x + 1, y + h//3),
    ]
    pygame.draw.polygon(superficie, (13, 28, 9), contorno)

    corpo = [
        (x + w//2, y + 2),
        (x + w - 4, y + h//3),
        (x + w - 7, y + h*2//3 - 2),
        (x + w//2 + 1, y + h - 4),
        (x + 6, y + h*2//3 - 2),
        (x + 3, y + h//3),
    ]
    pygame.draw.polygon(superficie, cor, corpo)

    # Nervura central e dois brilhos em degraus.
    cx = x + w//2
    pygame.draw.line(superficie, FOLHA_ESCURA,
                     (cx, y + 4), (cx, y + h - 5), max(1, w//9))
    pygame.draw.rect(superficie, FOLHA_CLARA,
                     (x + max(3, w//4), y + max(4, h//4), max(2, w//5), max(2, h//7)))
    pygame.draw.rect(superficie, (143, 181, 78),
                     (x + max(4, w//3), y + max(3, h//5), max(2, w//7), max(2, h//9)))

    # Pequeno talo para a folha parecer presa à madeira.
    pygame.draw.rect(superficie, (54, 39, 16),
                     (cx - 1, y + h - 1, max(2, w//7), max(4, w//4)))


def desenhar_texto_pixel(superficie, texto, fonte, centro,
                         cor=CREME, sombra=True):
    if sombra:
        sombra_img = fonte.render(texto, False, PRETO_PIXEL)
        superficie.blit(sombra_img, sombra_img.get_rect(
            center=(centro[0] + 3, centro[1] + 3)))

    img = fonte.render(texto, False, cor)
    superficie.blit(img, img.get_rect(center=centro))


def desenhar_painel_madeira_referencia(superficie):
    """Grande tronco/painel em pixel-art, com casca rica em camadas."""
    # Painel menor e mais compacto, deixando espaço visual para o CONTINUAR.
    px = int(LARGURA * 0.475)
    py = int(ALTURA * 0.245)
    pw = int(LARGURA * 0.475)
    ph = int(ALTURA * 0.475)
    painel = pygame.Rect(px, py, pw, ph)

    # ---------------------------------------------------------
    # SOMBRA E SILHUETA EXTERNA
    # ---------------------------------------------------------
    pygame.draw.rect(superficie, (14, 7, 3), painel.move(9, 11))
    pygame.draw.rect(superficie, (25, 12, 5), painel.move(3, 4))

    # Moldura de casca, em várias camadas.
    pygame.draw.rect(superficie, (55, 27, 11), painel)
    pygame.draw.rect(superficie, (116, 62, 25), painel.inflate(-5, -5))
    pygame.draw.rect(superficie, (177, 100, 41), painel.inflate(-10, -10), width=4)
    pygame.draw.rect(superficie, (67, 31, 12), painel.inflate(-17, -17), width=4)

    interior = painel.inflate(-29, -29)

    # ---------------------------------------------------------
    # CORPO DA ÁRVORE — base escura e variações verticais
    # ---------------------------------------------------------
    pygame.draw.rect(superficie, (72, 34, 14), interior)

    # Grandes faixas da casca: cada uma tem sombra, corpo e brilho.
    faixas = [
        (-0.02, .10, (51, 23, 9), (94, 43, 16)),
        (.075, .14, (59, 27, 10), (121, 57, 21)),
        (.205, .09, (45, 20, 8), (104, 47, 17)),
        (.285, .16, (65, 29, 11), (132, 64, 24)),
        (.445, .10, (48, 21, 8), (108, 50, 18)),
        (.535, .16, (63, 28, 10), (128, 60, 21)),
        (.695, .09, (44, 19, 7), (101, 45, 16)),
        (.775, .14, (58, 25, 9), (124, 57, 20)),
        (.915, .11, (47, 20, 8), (99, 43, 15)),
    ]
    for frac, width_frac, sombra, luz in faixas:
        x = interior.left + int(interior.width * frac)
        w = max(9, int(interior.width * width_frac))
        pygame.draw.rect(superficie, sombra,
                         (x, interior.top + 2, w, interior.height - 4))
        pygame.draw.rect(superficie, luz,
                         (x + max(5, w//5), interior.top + 5,
                          max(3, w//9), interior.height - 10))

    # Fendas verticais profundas, quebradas em degraus para parecer pixel-art.
    fendas = [
        (.10, .03, [(0,.00),(-5,.10),(2,.18),(-3,.31),(1,.48),(-6,.64),(0,.82)]),
        (.245, .025, [(0,.08),(6,.16),(2,.28),(-4,.40),(0,.57),(5,.73),(-1,.94)]),
        (.39, .032, [(0,.02),(-6,.14),(-2,.25),(4,.37),(0,.52),(-5,.68),(1,.88)]),
        (.57, .026, [(0,.11),(5,.23),(1,.34),(-5,.48),(-1,.63),(5,.76),(0,.91)]),
        (.72, .034, [(0,.03),(-5,.12),(-1,.29),(5,.42),(0,.58),(-4,.71),(2,.86)]),
        (.865, .024, [(0,.15),(5,.26),(0,.39),(-4,.54),(1,.69),(-2,.83)]),
    ]
    for frac, width_frac, pontos in fendas:
        x0 = interior.left + int(interior.width * frac)
        largura = max(3, int(interior.width * width_frac))
        for j in range(len(pontos)-1):
            ox1, yy1 = pontos[j]
            ox2, yy2 = pontos[j+1]
            y1 = interior.top + int(interior.height * yy1)
            y2 = interior.top + int(interior.height * yy2)
            pygame.draw.line(superficie, (39, 17, 6),
                             (x0 + ox1, y1), (x0 + ox2, y2), largura)
            pygame.draw.line(superficie, (122, 57, 20),
                             (x0 + ox1 + largura + 2, y1),
                             (x0 + ox2 + largura + 2, y2), max(1, largura//2))

    # ---------------------------------------------------------
    # VEIOS HORIZONTAIS — pequenos segmentos, não linhas contínuas
    # ---------------------------------------------------------
    veios = [
        (.07,.14,.08),(.13,.30,.12),(.21,.20,.06),(.28,.43,.16),
        (.36,.13,.10),(.44,.36,.09),(.52,.23,.18),(.61,.49,.12),
        (.69,.17,.08),(.76,.39,.16),(.84,.25,.10),(.91,.52,.07)
    ]
    for i, (fy, fx, fw) in enumerate(veios):
        y = interior.top + int(interior.height * fy)
        x = interior.left + int(interior.width * fx)
        w = max(14, int(interior.width * fw))
        cor_s = (46, 20, 7) if i % 2 else (54, 23, 8)
        cor_l = (135, 63, 22)
        # desenho em três blocos, com uma quebra no meio
        pygame.draw.rect(superficie, cor_s, (x, y, w, 4))
        if w > 32:
            pygame.draw.rect(superficie, cor_s, (x + w//3, y-4, max(4,w//7), 4))
        pygame.draw.rect(superficie, cor_l, (x+7, y-2, max(4,w//5), 2))

    # ---------------------------------------------------------
    # NÓS DA MADEIRA — anéis quadrados e rachaduras radiais
    # ---------------------------------------------------------
    nos = [
        (0.17, 0.17, 24),
        (0.78, 0.31, 31),
        (0.36, 0.67, 19),
        (0.88, 0.82, 25),
    ]
    for nx_f, ny_f, raio in nos:
        nx = interior.left + int(interior.width * nx_f)
        ny = interior.top + int(interior.height * ny_f)
        r = max(10, int(raio * min(LARGURA/896, ALTURA/1190)))
        pygame.draw.rect(superficie, (42, 18, 6), (nx-r, ny-r//2, r*2, r))
        pygame.draw.rect(superficie, (116, 51, 17), (nx-r+5, ny-r//2+4, r*2-10, r-8))
        pygame.draw.rect(superficie, (52, 22, 7), (nx-r//2, ny-r//3, r, max(5,r//3)))
        pygame.draw.rect(superficie, (145, 66, 24), (nx-r//3, ny-r//4, max(5,r//3), max(3,r//6)))
        # rachaduras saindo do nó
        for dx, dy, ln in [(-1,0,20),(1,0,25),(0,-1,18),(0,1,23)]:
            if dx:
                pygame.draw.rect(superficie, (43,19,7),
                                 (nx + dx*r, ny-2, dx*ln if dx>0 else ln, 4))
            else:
                pygame.draw.rect(superficie, (43,19,7),
                                 (nx-2, ny + dy*r, 4, dy*ln if dy>0 else ln))

    # ---------------------------------------------------------
    # BORDA INTERNA — casca irregular e pequenos pixels
    # ---------------------------------------------------------
    pygame.draw.rect(superficie, (31, 13, 5), interior, width=5)
    pygame.draw.rect(superficie, (143, 70, 25), interior.inflate(-7, -7), width=3)

    # Pequenos fragmentos claros da casca.
    detalhes = [
        (.06,.10,18,4),(.18,.07,25,3),(.31,.13,14,4),(.48,.06,28,3),
        (.62,.10,17,4),(.79,.08,25,3),(.91,.14,14,4),
        (.12,.88,20,3),(.29,.92,14,4),(.53,.84,23,3),(.71,.91,18,4),
    ]
    for fx, fy, w, h in detalhes:
        x = interior.left + int(interior.width*fx)
        y = interior.top + int(interior.height*fy)
        pygame.draw.rect(superficie, (160, 76, 27), (x,y,w,h))
        pygame.draw.rect(superficie, (66, 27, 9), (x+w//3,y+h+2,max(3,w//2),2))

    # ---------------------------------------------------------
    # FOLHAGEM NOS QUATRO CANTOS
    # ---------------------------------------------------------
    fs = max(13, int(min(LARGURA, ALTURA) * .022))
    folhagem = [
        (interior.left-8, interior.top-5, fs+4, FOLHA_CLARA),
        (interior.left+7, interior.top+17, fs+7, FOLHA),
        (interior.left+26, interior.top+1, fs, FOLHA_ESCURA),
        (interior.right-fs-2, interior.top-4, fs+7, FOLHA_CLARA),
        (interior.right-fs-23, interior.top+18, fs+3, FOLHA),
        (interior.right-fs-4, interior.top+38, fs, FOLHA_ESCURA),
        (interior.left-5, interior.bottom-fs-7, fs+7, FOLHA),
        (interior.left+17, interior.bottom-fs-2, fs+4, FOLHA_CLARA),
        (interior.left+39, interior.bottom-fs+14, fs, FOLHA_ESCURA),
        (interior.right-fs-1, interior.bottom-fs-8, fs+8, FOLHA),
        (interior.right-fs-24, interior.bottom-fs+12, fs+4, FOLHA_CLARA),
        (interior.right-fs-45, interior.bottom-fs+20, fs, FOLHA_ESCURA),
    ]
    for fx, fy, fsize, cor in folhagem:
        desenhar_folha_pixel(superficie, fx, fy, fsize, cor)

    return painel, interior


def desenhar_corda_placa(superficie, rect, hover=False):
    """Duas cordas formando o V característico da imagem."""
    topo = rect.top
    cx = rect.centerx
    gancho_y = max(0, topo - int(rect.height * .28))
    esp = int(rect.width * .31)

    pygame.draw.line(superficie, (36, 20, 10),
                     (cx, gancho_y), (rect.left + esp, topo), 7)
    pygame.draw.line(superficie, (151, 92, 43),
                     (cx, gancho_y), (rect.left + esp, topo), 3)
    pygame.draw.line(superficie, (36, 20, 10),
                     (cx, gancho_y), (rect.right - esp, topo), 7)
    pygame.draw.line(superficie, (151, 92, 43),
                     (cx, gancho_y), (rect.right - esp, topo), 3)

    pygame.draw.rect(superficie, (22, 12, 6), (cx-6, gancho_y-5, 12, 12))
    pygame.draw.rect(superficie,
                     DOURADO_CLARO if hover else (181, 132, 48),
                     (cx-3, gancho_y-5, 6, 8))


def desenhar_placa_avatar_referencia(superficie, rect, bloqueada=False,
                                      hover=False, avatar=None):
    """Placa quadrada: todas as opções usam exatamente o mesmo tamanho."""
    desenhar_corda_placa(superficie, rect, hover)

    # Sombra grossa e recortada, mantendo o visual pixelado.
    pygame.draw.rect(superficie, (18, 8, 3), rect.move(7, 9))
    pygame.draw.rect(superficie, (39, 17, 6), rect)

    # Madeira escura, no mesmo estilo do tronco principal.
    interior = rect.inflate(-11, -11)
    pygame.draw.rect(superficie, (72, 30, 10), interior)

    # Linhas verticais da casca — principal mudança solicitada.
    passo = max(18, interior.width // 6)
    for i in range(-1, 8):
        x = interior.left + i * passo
        pygame.draw.rect(superficie, (43, 17, 5),
                         (x, interior.top, max(5, passo//7), interior.height))
        pygame.draw.rect(superficie, (111, 45, 14),
                         (x + max(7, passo//4), interior.top + 5,
                          max(3, passo//13), interior.height - 10))

    # Veios curtos e quebrados.
    for i in range(5):
        y = interior.top + 16 + i * max(18, interior.height//5)
        x = interior.left + 9 + (i % 2)*13
        w = max(16, interior.width - 35 - (i%3)*18)
        pygame.draw.rect(superficie, (48, 19, 6), (x, y, w, 3))
        pygame.draw.rect(superficie, (133, 54, 17),
                         (x+7, y-2, max(5,w//5), 2))

    # Pequenas rachaduras verticais para casar com o tronco.
    rachaduras = [(.22,.08,.18),(.47,.26,.25),(.73,.10,.20),(.88,.42,.29)]
    for fx, fy, comprimento in rachaduras:
        x = interior.left + int(interior.width*fx)
        y = interior.top + int(interior.height*fy)
        h = int(interior.height*comprimento)
        pygame.draw.rect(superficie, (37, 14, 4), (x, y, 4, h))
        pygame.draw.rect(superficie, (119, 47, 14), (x+6, y+8, 2, max(5,h-20)))

    # Moldura dourada fina, como na referência.
    pygame.draw.rect(superficie, DOURADO, rect, width=5)
    pygame.draw.rect(superficie, DOURADO_CLARO,
                     rect.inflate(-9, -9), width=2)

    # Folhas pequenas apenas nos cantos, sem esconder a textura.
    fs = max(9, int(min(LARGURA, ALTURA)*.012))
    desenhar_folha_pixel(superficie, rect.left-3, rect.top-2, fs, FOLHA)
    desenhar_folha_pixel(superficie, rect.right-fs-3, rect.bottom-fs-5, fs, FOLHA_CLARA)

    if hover:
        pygame.draw.rect(superficie, (255, 223, 108), rect.inflate(7, 7), width=3)

    if bloqueada:
        # Escurecimento leve, deixando a madeira ainda visível.
        camada = pygame.Surface(rect.size, pygame.SRCALPHA)
        camada.fill((10, 5, 2, 74))
        superficie.blit(camada, rect.topleft)

        # Texto central em duas linhas, com mais respiro dentro do quadrado.
        desenhar_texto_pixel(
            superficie, "DESBLOQUEIE", fonte_pequena,
            (rect.centerx, rect.centery - int(rect.height*.10)), DOURADO_CLARO
        )
        desenhar_texto_pixel(
            superficie, "EM BREVE", fonte_pequena,
            (rect.centerx, rect.centery + int(rect.height*.11)), CREME
        )
    elif avatar is not None:
        imagem = avatar["idle_dir"]
        margem = int(rect.width * .10)
        tam = min(rect.width - margem*2, rect.height - margem*2)
        imagem = pygame.transform.scale(imagem, (tam, tam))
        superficie.blit(imagem, imagem.get_rect(center=rect.center))


def desenhar_botao_jogo_referencia(superficie, rect, texto,
                                   hover=False, seta=False):
    """Botão compacto; para CONTINUAR recebe destaque visual maior."""
    sombra = rect.move(6, 8)
    pygame.draw.rect(superficie, (14, 24, 7), sombra)

    # Base verde-musgo inspirada no botão da referência.
    pygame.draw.rect(superficie, (39, 69, 22), rect)
    interior = rect.inflate(-10, -10)
    pygame.draw.rect(superficie, (72, 105, 42), interior)

    # Faixas de madeira/folhagem muito discretas, todas contidas na placa.
    passo = max(22, interior.width // 7)
    for i in range(0, 8):
        bx = interior.left + i * passo
        pygame.draw.rect(
            superficie, (48, 76, 26),
            (bx, interior.top + 4, max(4, passo // 9),
             max(4, interior.height - 8))
        )
        pygame.draw.rect(
            superficie, (96, 130, 51),
            (bx + max(5, passo // 4), interior.top + 6,
             max(2, passo // 14), max(4, interior.height - 12))
        )

    pygame.draw.rect(superficie, (27, 50, 15), interior, width=3)
    pygame.draw.rect(superficie, (111, 147, 59), rect, width=4)
    pygame.draw.rect(superficie, (158, 184, 82),
                     rect.inflate(-8, -8), width=2)

    centro_x = rect.left + int(rect.width*.40) if seta else rect.centerx
    desenhar_texto_pixel(
        superficie, texto, fonte_menu,
        (centro_x, rect.centery), DOURADO_CLARO
    )

    if seta:
        cx = rect.right - int(rect.width*.13)
        cy = rect.centery
        pts = [
            (cx-16,cy-8),(cx,cy-8),(cx,cy-15),(cx+20,cy),
            (cx,cy+15),(cx,cy+8),(cx-16,cy+8)
        ]
        pygame.draw.polygon(superficie, (20, 39, 8),
                            [(x+2,y+3) for x,y in pts])
        pygame.draw.polygon(superficie, (137, 197, 57), pts)
        pygame.draw.rect(superficie, (181, 224, 87),
                         (cx-10, cy-4, 10, 3))

    if hover:
        pygame.draw.rect(superficie, (214, 239, 126),
                         rect.inflate(6, 6), width=3)


# Folhas móveis removidas: a decoração vegetal fica somente nas madeiras.
def atualizar_folhas_menu(tempo_atual):
    pass


def desenhar_folhas_menu(superficie):
    pass


# ---------------------------------------------------------
# POSIÇÕES EXATAS — baseadas na composição da referência
# ---------------------------------------------------------

painel_menu_rect = pygame.Rect(
    int(LARGURA * .475),
    int(ALTURA * .245),
    int(LARGURA * .475),
    int(ALTURA * .475)
)

# Quatro quadrados iguais, posicionados nos quatro cantos internos
# do painel, como na referência enviada.
slot_side = int(min(LARGURA * .125, ALTURA * .145))

margem_x = max(18, int(painel_menu_rect.width * .075))
margem_y = max(18, int(painel_menu_rect.height * .095))

posicoes_placas = [
    (painel_menu_rect.left + margem_x,
     painel_menu_rect.top + margem_y),
    (painel_menu_rect.right - margem_x - slot_side,
     painel_menu_rect.top + margem_y),
    (painel_menu_rect.left + margem_x,
     painel_menu_rect.bottom - margem_y - slot_side),
    (painel_menu_rect.right - margem_x - slot_side,
     painel_menu_rect.bottom - margem_y - slot_side),
]

botoes = [
    pygame.Rect(x, y, slot_side, slot_side)
    for x, y in posicoes_placas
]

# Personagem grande à esquerda, agora totalmente estática.
tamanho_avatar_grande = int(ALTURA * .38)
avatar_escolhido = lista_avatares[3]

# Placa do título: somente o espaço necessário para a frase.
titulo_texto = "ESCOLHA SEU AVATAR!"
titulo_texto_w, titulo_texto_h = fonte_titulo.size(titulo_texto)
placa_titulo_w = min(
    int(LARGURA * .43),
    titulo_texto_w + int(LARGURA * .055)
)
placa_titulo_h = max(
    int(ALTURA * .075),
    titulo_texto_h + int(ALTURA * .025)
)
placa_titulo = pygame.Rect(
    (LARGURA - placa_titulo_w) // 2,
    int(ALTURA * .065),
    placa_titulo_w,
    placa_titulo_h
)

# CONTINUAR maior e com mais destaque, sem madeira sobrando dos lados.
continuar_texto_w, continuar_texto_h = fonte_menu.size("CONTINUAR")
botao_continuar_w = max(
    int(LARGURA * .27),
    continuar_texto_w + int(LARGURA * .085)
)
botao_continuar_h = max(
    int(ALTURA * .09),
    continuar_texto_h + int(ALTURA * .035)
)
botao_continuar_menu = pygame.Rect(
    int(LARGURA * .69),
    int(ALTURA * .84),
    botao_continuar_w,
    botao_continuar_h
)

# Animações do menu
tempo_inicio_oi = pygame.time.get_ticks()
duracao_oi = 1800
tempo_ultimo_piscar = pygame.time.get_ticks()
intervalo_piscar = 3500
duracao_piscada = 180
esta_piscando = False
inicio_piscada = 0
mensagem_bloqueado = False
tempo_mensagem_bloqueado = 0
duracao_mensagem_bloqueado = 1800


def pegar_imagem_avatar(avatar, piscando=False):
    if piscando and "blink_dir" in avatar:
        return avatar["blink_dir"]
    return avatar["idle_dir"]


def pegar_frame_oi(avatar, tempo):
    if "wave_dir" in avatar and len(avatar["wave_dir"]) > 0:
        frames_oi = avatar["wave_dir"]
        indice = int(tempo / 160) % len(frames_oi)
        return frames_oi[indice]
    return avatar["idle_dir"]

# =========================================================
# ESTADO DO GAMEPLAY
# =========================================================

def iniciar_gameplay():

    TAMANHO = 100

    chao = int(
        ALTURA * (500 / 600)
        - TAMANHO
    )

    x = LARGURA // 2
    y = chao

    vel_x = 5
    vel_y = 0

    gravidade = 0.5
    forca_pulo = -12

    no_chao = True
    olhando_direita = True

    tempo_animacao = 0
    vel_animacao = 0.2

    tempo_pouso = 0

    return {
        "TAMANHO": TAMANHO,
        "chao": chao,
        "x": x,
        "y": y,
        "vel_x": vel_x,
        "vel_y": vel_y,
        "gravidade": gravidade,
        "forca_pulo": forca_pulo,
        "no_chao": no_chao,
        "olhando_direita": olhando_direita,
        "tempo_animacao": tempo_animacao,
        "vel_animacao": vel_animacao,
        "tempo_pouso": tempo_pouso
    }



# =========================================================
# LOOP GERAL
# =========================================================

while True:

    # =====================================================
    # MENU DE ESCOLHA
    # =====================================================

    escolhendo_avatar = True

    while escolhendo_avatar:

        tempo_atual = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()

        # -------------------------------------------------
        # FUNDO — blur forte como na referência
        # -------------------------------------------------
        tela.blit(fundo_menu_blur, (0, 0))

        # leve vinheta/escurecimento para destacar a UI
        camada_escura = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        camada_escura.fill((8, 10, 5, 38))
        tela.blit(camada_escura, (0, 0))

        # -------------------------------------------------
        # TÍTULO — placa compacta, sem madeira sobrando
        # -------------------------------------------------
        pygame.draw.rect(tela, (18, 8, 3), placa_titulo.move(5, 7))
        pygame.draw.rect(tela, (48, 20, 7), placa_titulo)
        titulo_interior = placa_titulo.inflate(-10, -10)
        pygame.draw.rect(tela, (83, 35, 11), titulo_interior)

        # Veios verticais curtos, contidos dentro da própria placa.
        passo_titulo = max(18, titulo_interior.width // 7)
        for i in range(0, 8):
            tx = titulo_interior.left + i * passo_titulo
            pygame.draw.rect(
                tela, (48, 18, 5),
                (tx, titulo_interior.top + 4, max(4, passo_titulo // 8),
                 max(4, titulo_interior.height - 8))
            )
            pygame.draw.rect(
                tela, (125, 57, 17),
                (tx + max(5, passo_titulo // 4), titulo_interior.top + 7,
                 max(2, passo_titulo // 14), max(4, titulo_interior.height - 14))
            )

        pygame.draw.rect(tela, DOURADO, placa_titulo, width=4)
        pygame.draw.rect(tela, DOURADO_CLARO,
                         placa_titulo.inflate(-8, -8), width=2)
        desenhar_texto_pixel(
            tela, titulo_texto, fonte_titulo, placa_titulo.center, DOURADO_CLARO
        )

        # -------------------------------------------------
        # GRANDE QUADRO DE MADEIRA
        # -------------------------------------------------
        desenhar_painel_madeira_referencia(tela)

        # -------------------------------------------------
        # AVATAR GRANDE À ESQUERDA — TOTALMENTE PARADO
        # -------------------------------------------------
        # Uma única imagem idle: sem balanço, sem piscada e sem animação de entrada.
        mensagem_bloqueado = False
        avatar_principal = avatar_escolhido["idle_dir"]
        avatar_principal = pygame.transform.scale(
            avatar_principal, (tamanho_avatar_grande, tamanho_avatar_grande)
        )
        avatar_principal_rect = avatar_principal.get_rect(
            midbottom=(int(LARGURA*.205), int(ALTURA*.84))
        )
        tela.blit(avatar_principal, avatar_principal_rect)

        # -------------------------------------------------
        # QUATRO CARTÕES
        # -------------------------------------------------
        for i, botao in enumerate(botoes):
            hover = botao.collidepoint(mouse_pos)
            rect = botao.inflate(int(botao.width*.045), int(botao.height*.045)) if hover else botao
            if hover:
                rect.center = botao.center

            desenhar_placa_avatar_referencia(
                tela, rect,
                bloqueada=(i != 3),
                hover=hover,
                avatar=lista_avatares[3] if i == 3 else None
            )

        # -------------------------------------------------
        # CONTINUAR
        # -------------------------------------------------
        hover_continuar = botao_continuar_menu.collidepoint(mouse_pos)
        desenhar_botao_jogo_referencia(
            tela, botao_continuar_menu, "CONTINUAR",
            hover=hover_continuar, seta=True
        )

        # -------------------------------------------------
        # EVENTOS DO MENU
        # -------------------------------------------------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for i, botao in enumerate(botoes):
                    if botao.collidepoint(evento.pos):
                        if i == 3:
                            avatar_escolhido = lista_avatares[3]
                            mensagem_bloqueado = False
                        else:
                            mensagem_bloqueado = True
                            tempo_mensagem_bloqueado = pygame.time.get_ticks()

                if botao_continuar_menu.collidepoint(evento.pos):
                    if avatar_escolhido == lista_avatares[3]:
                        escolhendo_avatar = False

        pygame.display.flip()
        relogio.tick(60)


    # =====================================================
    # INICIAR GAMEPLAY
    # =====================================================

    estado_jogo = iniciar_gameplay()

    TAMANHO = estado_jogo["TAMANHO"]

    chao = estado_jogo["chao"]

    x = estado_jogo["x"]
    y = estado_jogo["y"]

    vel_x = estado_jogo["vel_x"]
    vel_y = estado_jogo["vel_y"]

    gravidade = estado_jogo["gravidade"]
    forca_pulo = estado_jogo["forca_pulo"]

    no_chao = estado_jogo["no_chao"]
    olhando_direita = estado_jogo[
        "olhando_direita"
    ]

    tempo_animacao = estado_jogo[
        "tempo_animacao"
    ]

    vel_animacao = estado_jogo[
        "vel_animacao"
    ]

    tempo_pouso = estado_jogo[
        "tempo_pouso"
    ]


    # =====================================================
    # BOTÃO VOLTAR — SOMENTE NO GAMEPLAY
    # =====================================================

    botao_voltar = pygame.Rect(
        int(LARGURA * 0.035),
        int(ALTURA * 0.045),
        int(LARGURA * 0.16),
        int(ALTURA * 0.075)
    )

    # =====================================================
    # LOOP PRINCIPAL DO JOGO
    # =====================================================

    voltar_para_menu = False

    while not voltar_para_menu:

        tempo_atual = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()

        # -------------------------------------------------
        # FUNDO
        # -------------------------------------------------

        tela.blit(
            fundo,
            (0, 0)
        )

        # -------------------------------------------------
        # FOLHAS PIXELADAS
        # -------------------------------------------------

        # -------------------------------------------------
        # BOTÃO VOLTAR COM HOVER
        # -------------------------------------------------

        hover_voltar = (
            botao_voltar.collidepoint(
                mouse_pos
            )
        )

        desenhar_botao_jogo_referencia(
            tela,
            botao_voltar,
            "VOLTAR",
            hover=hover_voltar,
            seta=False
        )

        # -------------------------------------------------
        # EVENTOS
        # -------------------------------------------------

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()

                if evento.key in [
                    pygame.K_SPACE,
                    pygame.K_UP
                ]:

                    if no_chao:

                        vel_y = forca_pulo
                        no_chao = False

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if evento.button == 1:

                    if botao_voltar.collidepoint(
                        evento.pos
                    ):

                        voltar_para_menu = True

                        tempo_inicio_oi = (
                            pygame.time.get_ticks()
                        )

                        mensagem_bloqueado = False

        # -------------------------------------------------
        # TECLAS
        # -------------------------------------------------

        teclas = pygame.key.get_pressed()

        movendo = False

        abaixado = teclas[
            pygame.K_DOWN
        ]

        # -------------------------------------------------
        # MOVIMENTO
        # -------------------------------------------------

        if not abaixado:

            if teclas[pygame.K_LEFT]:

                if x > 0:

                    x -= vel_x

                    movendo = True

                    olhando_direita = False

            if teclas[pygame.K_RIGHT]:

                if x < LARGURA - TAMANHO:

                    x += vel_x

                    movendo = True

                    olhando_direita = True

        # -------------------------------------------------
        # FÍSICA
        # -------------------------------------------------

        vel_y += gravidade
        y += vel_y

        # -------------------------------------------------
        # CHÃO
        # -------------------------------------------------

        if y >= chao:

            if not no_chao:

                tempo_pouso = 10

            y = chao

            vel_y = 0

            no_chao = True

        # -------------------------------------------------
        # ESTADO
        # -------------------------------------------------

        if abaixado and no_chao:

            estado = "abaixado"

        elif not no_chao:

            if vel_y < -2:

                estado = "pulo"

            elif vel_y > 2:

                estado = "caindo"

            else:

                estado = "preparar"

        else:

            if tempo_pouso > 0:

                estado = "caida"

                tempo_pouso -= 1

            elif movendo:

                estado = "walk"

            else:

                estado = "idle"

        # -------------------------------------------------
        # DIREÇÃO
        # -------------------------------------------------

        if olhando_direita:

            sufixo = "_dir"

        else:

            sufixo = "_esq"

        # -------------------------------------------------
        # IMAGEM
        # -------------------------------------------------

        if estado == "walk":

            tempo_animacao += vel_animacao

            frames = avatar_escolhido[
                "walk" + sufixo
            ]

            quantidade_frames = len(frames)

            if quantidade_frames <= 0:

                quantidade_frames = 1

            if tempo_animacao >= quantidade_frames:

                tempo_animacao = 0

            imagem = frames[
                int(tempo_animacao)
            ]

        else:

            imagem = avatar_escolhido[
                estado + sufixo
            ]

        # -------------------------------------------------
        # PERSONAGEM
        # -------------------------------------------------

        tamanho_imagem = (
            imagem.get_height()
        )

        rect = imagem.get_rect(
            midbottom=(
                x + TAMANHO // 2,
                y + tamanho_imagem
            )
        )

        tela.blit(
            imagem,
            rect
        )

        # -------------------------------------------------
        # ATUALIZAR TELA
        # -------------------------------------------------

        pygame.display.flip()

        relogio.tick(60)

