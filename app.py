import base64
import json
from collections import Counter
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

BASE_DIR = Path(__file__).parent

st.set_page_config(
    page_title="AWS Game 🎮",
    page_icon="☁️",
    layout="centered"
)

# Mesma técnica do app-live: mantém o <header> no DOM porque é dentro do
# stToolbar que o Streamlit renderiza a seta de expandir a sidebar
# (stExpandSidebarButton). Esconder o header inteiro trava a sidebar fechada.
st.markdown("""
<style>
    header[data-testid="stHeader"] {
        background: transparent !important;
        box-shadow: none !important;
    }
    [data-testid="stToolbarActions"],
    [data-testid="stAppDeployButton"],
    [data-testid="stMainMenu"],
    [data-testid="stStatusWidget"],
    [data-testid="stDecoration"],
    #MainMenu,
    footer { display: none !important; }

    /* O padding-top padrão do bloco principal é 96px e comia a área útil acima
       do jogo. O Streamlit renomeou esse contêiner (era stAppViewBlockContainer),
       então miramos nos dois nomes + na classe .block-container, estável entre
       versões. Mesma abordagem do app-live.

       NÃO zerar padding/margin do h1/h4: o Streamlit reserva o espaço do bloco
       via flex-basis fixado no mount, e encolher os headings faz o conteúdo
       transbordar o container — o jogo sobe por cima do subtítulo. */
    [data-testid="stMainBlockContainer"],
    [data-testid="stAppViewBlockContainer"],
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0 !important;
    }
    div[data-testid="stVerticalBlock"] { gap: 0 !important; }
    .element-container { margin-top: 0 !important; margin-bottom: 0 !important; }

    /* Aproxima o subtítulo do título: são 24px de vão (padding-bottom do h1 +
       padding-top do h4). O padding-BOTTOM do h4 fica intacto de propósito —
       ele é o colchão que impede o jogo de encostar no texto. */
    .stMarkdown h1 { padding-bottom: 0 !important; }
    .stMarkdown h4 { padding-top: 0 !important; }

    /* O injetor de tema roda num components.html de altura 0. Sem isto, esse
       iframe invisível ainda reserva espaço e abre um vão no topo da página. */
    iframe[height="0"] { display: none !important; margin: 0 !important; padding: 0 !important; }
    .element-container:has(iframe[height="0"]) {
        margin: 0 !important;
        padding: 0 !important;
        min-height: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# Barra de status (mobile) e barra de rolagem — mesma técnica do AryRoot
# --------------------------------------------------------------------------

# O azul-marinho do próprio jogo: é o tom médio do degradê do canvas e do card.
NAVY = "#003366"
SCROLL_TRACK = "#E6EAF0"

# O <meta theme-color> via st.markdown NÃO funciona sozinho: o Streamlit renderiza
# o markdown dentro de um contêiner, e o navegador só lê essa meta no <head> do
# documento de topo. Por isso o injetor abaixo roda num iframe e escreve no
# parent/top document. O st.markdown aqui é só um reforço para o caso simples.
st.markdown(f'<meta name="theme-color" content="{NAVY}">', unsafe_allow_html=True)

components.html(f"""
<script>
(function() {{
    const doc = window.parent.document;

    // theme-color em TODOS os níveis: o iframe, o pai e o topo. Qual deles o
    // navegador móvel lê depende de como a página está embutida.
    function aplicarThemeColor(d) {{
        try {{
            d.querySelectorAll('meta[name="theme-color"]').forEach(el => el.remove());
            const meta = d.createElement('meta');
            meta.name = 'theme-color';
            meta.content = '{NAVY}';
            d.head.insertBefore(meta, d.head.firstChild);
        }} catch (e) {{}}
    }}
    [document, doc].forEach(aplicarThemeColor);
    try {{
        const topDoc = window.top.document;
        if (topDoc !== doc && topDoc !== document) aplicarThemeColor(topDoc);
    }} catch (e) {{}}

    // Barra de rolagem: as duas sintaxes cobrem todos os navegadores —
    // ::-webkit-scrollbar (Chrome, Edge, Safari, Android) e scrollbar-color /
    // scrollbar-width (Firefox, padrão CSS). Desktop e móvel.
    if (!doc.getElementById('aws-game-scrollbar')) {{
        const style = doc.createElement('style');
        style.id = 'aws-game-scrollbar';
        style.textContent = `
            * {{
                scrollbar-color: {NAVY} {SCROLL_TRACK} !important;
                scrollbar-width: thin !important;
            }}
            *::-webkit-scrollbar {{ width: 9px !important; height: 9px !important; }}
            *::-webkit-scrollbar-thumb {{
                background-color: {NAVY} !important;
                border-radius: 5px !important;
            }}
            *::-webkit-scrollbar-thumb:hover {{ background-color: #004488 !important; }}
            *::-webkit-scrollbar-track {{
                background: {SCROLL_TRACK} !important;
                border-radius: 5px !important;
            }}
        `;
        doc.head.appendChild(style);
    }}
}})();
</script>
""", height=0)

st.markdown("""
<div style="text-align: center;">
    <h1>☁️ AWS Game 🎮</h1>
    <h4>S3 Climbing Adventure</h4>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# Categorias e cores — fonte única da verdade (Python injeta no JS)
# --------------------------------------------------------------------------

# Categorias oficiais AWS 2026. Os slugs vêm do aws-tetris-pro e são a chave
# canônica no servicos.json; a tradução abaixo é só para exibir na legenda.
#
# A paleta é a oficial da AWS, com uma ressalva: a AWS reusa o mesmo hex em até
# 3 categorias (Analytics/Networking/Games são todas #8C4FFF). Como aqui a cor
# da plataforma É o sinal da categoria, as colisões foram desfeitas deslocando a
# luminosidade — mesmo matiz, tom distinto. O hex oficial fica com a categoria
# mais populosa de cada grupo.
CATEGORY_COLORS = {
    "Analytics": "#8C4FFF",
    "App-Integration": "#F05DA5",
    "Artificial-Intelligence": "#01A88D",
    "Blockchain": "#EF924D",
    "Business-Applications": "#C7131F",
    "Cloud-Financial-Management": "#3FB523",
    "Compute": "#ED7100",
    "Containers": "#FF9B40",
    "Customer-Enablement": "#5A30B5",
    "Database": "#527FFF",
    "Developer-Tools": "#437ABA",
    "End-User-Computing": "#01F9D1",
    "Front-End-Web-Mobile": "#ED3F4B",
    "Games": "#5700FC",
    "General-Icons": "#232F3E",
    "Internet-of-Things": "#1B660F",
    "Management-Governance": "#E7157B",
    "Media-Services": "#D86613",
    "Migration-Modernization": "#2EAD19",
    "Networking-Content-Delivery": "#B68FFF",
    "Quantum-Technologies": "#9B4A00",
    "Satellite": "#1A3C6E",
    "Security-Identity-Compliance": "#DD344C",
    "Storage": "#277116",
    # A plataforma-chão. Não confundir com a plataforma FINAL, que também era
    # dourada, mas é pintada por outro caminho (Platform.style, isFinal).
    "Start": "#000000",
}

CATEGORY_LABELS = {
    "Analytics": "Análise",
    "App-Integration": "Integração de Aplicações",
    "Artificial-Intelligence": "Inteligência Artificial",
    "Blockchain": "Blockchain",
    "Business-Applications": "Aplicações Empresariais",
    "Cloud-Financial-Management": "Gestão Financeira na Nuvem",
    "Compute": "Computação",
    "Containers": "Contêineres",
    "Customer-Enablement": "Capacitação do Cliente",
    "Database": "Banco de Dados",
    "Developer-Tools": "Ferramentas de Desenvolvedor",
    "End-User-Computing": "Computação do Usuário Final",
    "Front-End-Web-Mobile": "Front-End Web e Mobile",
    "Games": "Jogos",
    "General-Icons": "Geral",
    "Internet-of-Things": "Internet das Coisas",
    "Management-Governance": "Gerenciamento e Governança",
    "Media-Services": "Serviços de Mídia",
    "Migration-Modernization": "Migração e Modernização",
    "Networking-Content-Delivery": "Redes e Entrega de Conteúdo",
    "Quantum-Technologies": "Tecnologias Quânticas",
    "Satellite": "Satélite",
    "Security-Identity-Compliance": "Segurança, Identidade e Conformidade",
    "Storage": "Armazenamento",
}

FALLBACK_COLOR = "#666666"

# Altura do card de descrição. É fixa de propósito: se acompanhasse o tamanho do
# texto, o layout pularia a cada plataforma. O valor foi medido para caber a mais
# longa das 374 descrições (VPC, 560 caracteres) — ver o teste em curadoria/.
GAME_HEIGHT = 650
CARD_HEIGHT = 200
CARD_GAP = 12

# TTL do cache em memória. O dataset e os assets são estáticos, então 8 horas de
# retenção evitam reler o disco e remontar os ~2,9 MB de HTML a cada sessão nova.
CACHE_TTL = 8 * 60 * 60  # 8 horas


def _darken(hex_color, amount=50):
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02X%02X%02X" % (max(0, r - amount), max(0, g - amount), max(0, b - amount))


# Bordas pré-calculadas: o JS não precisa mais parsear hex a cada quadro.
CATEGORY_STYLES = {
    name: {"color": color, "border": _darken(color)}
    for name, color in CATEGORY_COLORS.items()
}


# --------------------------------------------------------------------------
# Carregamento
# --------------------------------------------------------------------------

def load_asset_b64(relative_path):
    """Sem @st.cache_data de propósito: só o build_game_html() chama isto, e ele
    já é cacheado — então esta função roda uma vez a cada 8 horas. Cacheá-la
    duplicaria ~1 MB de base64 na memória (os mesmos bytes já vivem dentro do
    HTML cacheado) para poupar 6 ms a cada 8 horas."""
    try:
        return base64.b64encode((BASE_DIR / relative_path).read_bytes()).decode()
    except FileNotFoundError:
        return None


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def load_aws_services():
    try:
        data = json.loads((BASE_DIR / "servicos.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        st.error("Arquivo servicos.json não encontrado na raiz do projeto!")
        return []
    except json.JSONDecodeError as exc:
        st.error(f"Erro ao decodificar servicos.json: {exc}")
        return []

    services, seen = [], set()
    for node in data.get("nodes", []):
        name = (node.get("name") or "").strip()
        if not name or name in seen:
            continue  # a base traz 3 serviços repetidos
        seen.add(name)

        services.append({
            "name": name,
            "description": (node.get("Description") or node.get("description") or "").strip(),
            "category": (node.get("Category") or "General-Icons").strip(),
        })
    return services


def to_js(value):
    """json.dumps seguro para injetar dentro de <script>."""
    return json.dumps(value, ensure_ascii=True).replace("</", "<\\/")


aws_services = load_aws_services()
if not aws_services:
    st.stop()

# A legenda sai dos dados, não de uma lista paralela que envelhece sozinha.
category_counts = Counter(s["category"] for s in aws_services)

# Os assets NÃO são carregados aqui: só o build_game_html() precisa deles, e ele
# é cacheado. Carregá-los no módulo faria os ~1 MB de base64 serem despicklados
# do cache a cada rerun sem necessidade — e duplicados na memória, já que os
# mesmos bytes já estão dentro do HTML cacheado.


# --------------------------------------------------------------------------
# Jogo
# --------------------------------------------------------------------------

@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def build_game_html():
    """Monta o HTML do jogo (1,3 MB) e guarda em memória.

    SEM ARGUMENTOS de propósito. O @st.cache_data hasheia todos os argumentos
    para montar a chave do cache — e passar aqui o ~1 MB de base64 dos assets
    custava 23 ms por chamada, contra 7 ms para simplesmente remontar o HTML do
    zero. O cache ficava 3,5x mais lento que não ter cache. Sem argumentos, a
    chave é trivial e o acerto sai por ~2 ms (só o unpickle do resultado).

    Os dados vêm dos carregadores, chamados aqui dentro — então na maior parte
    das vezes nem são executados: este cache acerta antes.
    """
    services = load_aws_services()
    styles = CATEGORY_STYLES
    fallback_color = FALLBACK_COLOR
    mascot = load_asset_b64("static/mascote.png")
    audio = {
        "aplausos": load_asset_b64("static/aplausos.mp3"),
        "pulo": load_asset_b64("static/pulo.mp3"),
        "gameover": load_asset_b64("static/gameover.mp3"),
        "sonora": load_asset_b64("static/sonora.mp3"),
    }
    return f'''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>S3 Climbing Adventure</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            padding: 0;
            background: transparent;
            font-family: 'Arial', sans-serif;
            overflow: hidden;
        }}
        #gameContainer {{
            position: relative;
            width: 700px;
            height: 650px;
            max-width: 100%;
            margin: 0 auto;
            border: 3px solid #2E8B57;
            border-radius: 10px;
            overflow: hidden;
        }}
        canvas {{
            display: block;
            background: transparent;
            outline: none;
            max-width: 100%;
        }}
        #ui {{
            position: absolute;
            top: 12px;
            left: 10px;
            color: white;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            z-index: 100;
            font-size: 18px;
            pointer-events: none;
        }}
        #gameOver, #gameWin, #startOverlay {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.9);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            z-index: 200;
            border: 3px solid #FFD700;
        }}
        #gameOver, #gameWin {{ display: none; }}
        #startOverlay p {{ font-size: 14px; color: #CFCFCF; }}
        button {{
            background: #228B22;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
        }}
        button:hover {{ background: #32CD32; }}

        /* Card da descrição do serviço da plataforma atual. Altura FIXA: se ele
           crescesse conforme o texto, o layout pularia a cada plataforma. */
        #serviceCard {{
            width: 700px;
            max-width: 100%;
            height: {CARD_HEIGHT}px;
            margin: {CARD_GAP}px auto 0;
            padding: 14px 22px;
            /* Mesmas cores do degradê do canvas (#001122 -> #003366 -> #004488),
               para o card ler como continuação do jogo. Não vai até o #87CEEB do
               fundo da tela — sobre aquele azul claro o texto branco cairia para
               2,5:1 de contraste. Nesta faixa fica em ~10:1. */
            background: linear-gradient(180deg, #001122 0%, #003366 45%, #004488 100%);
            border: 3px solid #2E8B57;
            border-radius: 14px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.25);
            overflow: hidden;
            /* Centraliza nos dois eixos. A altura é fixa para caber a maior
               descrição (VPC, 560 chars); as curtas sobrariam espaço embaixo e a
               caixa pareceria cortada. Centralizada, a sobra fica simétrica. */
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        #cardDescription {{
            color: #FFFFFF;
            font-size: 15px;
            line-height: 1.55;
            text-align: center;
            margin: 0;
        }}
    </style>
</head>
<body>
    <div id="gameContainer">
        <canvas id="gameCanvas" width="700" height="650" tabindex="0"></canvas>

        <div id="ui">
            <div>Pontos: <span id="score">0</span></div>
            <div>Vidas: <span id="lives">5</span></div>
            <div>Altura: <span id="height">0</span>m</div>
        </div>

        <div id="startOverlay">
            <h2>☁️ S3 Climbing Adventure</h2>
            <p>← → mover &nbsp;•&nbsp; ↑ ou espaço para pular</p>
            <button id="startBtn">▶ Clique para jogar</button>
        </div>

        <div id="gameOver">
            <h2>💀 Game Over!</h2>
            <p>Você parou no: <span id="finalService">Início</span></p>
            <p>Altura alcançada: <span id="finalHeight">0</span>m</p>
            <p>Pontuação Final: <span id="finalScore">0</span></p>
            <button onclick="restartGame()">🔄 Jogar Novamente</button>
        </div>

        <div id="gameWin">
            <h2>🏆 PARABÉNS!</h2>
            <p>Você escalou os {len(services)} serviços AWS!</p>
            <p>Pontuação Final: <span id="winScore">0</span></p>
            <button onclick="restartGame()">🔄 Jogar Novamente</button>
        </div>
    </div>

    <div id="serviceCard">
        <p id="cardDescription">Comece sua aventura pelos serviços AWS! A cada plataforma que você pisar, a descrição do serviço correspondente aparece aqui.</p>
    </div>

    <script>
        const awsServices = {to_js(services)};
        const CATEGORY_STYLES = {to_js(styles)};
        const FALLBACK_STYLE = {{ color: {to_js(fallback_color)}, border: '#444444' }};
        const audioSources = {to_js(audio)};
        const mascotB64 = {to_js(mascot)};

        const TOTAL_SERVICES = awsServices.length;
        const PLATFORM_SPACING = 220;
        const GROUND_HEIGHT = 60;
        const WORLD_HEIGHT = TOTAL_SERVICES * PLATFORM_SPACING;
        const GROUND_TOP = WORLD_HEIGHT - GROUND_HEIGHT;

        // --- Passo fixo -----------------------------------------------------
        // A física conta TICKS, nunca quadros. requestAnimationFrame dispara na
        // taxa do monitor (60/120/144Hz), então amarrar a física a ele fazia o
        // jogo acelerar junto com o refresh rate. 1 tick == 1 quadro dos 60fps
        // originais, o que mantém todas as constantes de ajuste válidas.
        const TICK_MS = 1000 / 60;
        const MAX_FRAME_MS = 250;   // teto após aba em segundo plano
        const MAX_TICKS_PER_FRAME = 5;
        let accumulator = 0;
        let lastFrameTime = null;

        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        const audioElements = {{}};
        function initAudio() {{
            for (const [key, b64] of Object.entries(audioSources)) {{
                if (!b64) continue;
                audioElements[key] = new Audio('data:audio/mp3;base64,' + b64);
                if (key === 'sonora') {{
                    audioElements[key].loop = true;
                    audioElements[key].volume = 0.3;
                }}
            }}
        }}

        function playAudio(key) {{
            const el = audioElements[key];
            if (!el) return;
            el.currentTime = 0;
            el.play().catch(e => console.log('Audio play failed:', e));
        }}

        function stopAllAudio() {{
            for (const el of Object.values(audioElements)) {{
                el.pause();
                el.currentTime = 0;
            }}
        }}

        let mascotImage = null;
        if (mascotB64) {{
            mascotImage = new Image();
            mascotImage.src = 'data:image/png;base64,' + mascotB64;
        }}

        function newGameState() {{
            return {{
                score: 0,
                lives: 5,
                currentPlatform: 0,
                started: false,
                gameRunning: true,
                keys: {{}},
                cameraY: 0
            }};
        }}
        let gameState = newGameState();

        class Player {{
            constructor(x, y) {{
                this.x = x;
                this.y = y;
                this.width = 40;
                this.height = 50;
                this.velocityX = 0;
                this.velocityY = 0;
                this.speed = 6;
                this.jumpPower = 25;
                this.onGround = false;
                this.standingOn = null;
                this.direction = 1;
                this.invulnerable = false;
                this.invulnerabilityTimer = 0;
                this.maxFallDistance = 700;
                this.lastGroundY = y;
            }}

            update() {{
                if (gameState.keys['ArrowLeft']) {{
                    this.velocityX = -this.speed;
                    this.direction = -1;
                }}
                if (gameState.keys['ArrowRight']) {{
                    this.velocityX = this.speed;
                    this.direction = 1;
                }}
                if ((gameState.keys['ArrowUp'] || gameState.keys[' ']) && this.onGround) {{
                    this.velocityY = -this.jumpPower;
                    this.onGround = false;
                    playAudio('pulo');
                }}

                this.velocityY += 0.8;
                this.x += this.velocityX;
                this.y += this.velocityY;
                this.velocityX *= 0.85;

                if (this.x < -this.width) this.x = canvas.width;
                if (this.x > canvas.width) this.x = -this.width;

                // Consome o estado de "no chão": checkPlatformCollisions() o
                // restaura ainda neste tick se ainda houver plataforma embaixo.
                // Sem isso, andar para fora da borda dava um pulo grátis no ar.
                this.onGround = false;
                this.standingOn = null;

                if (this.y > this.lastGroundY + this.maxFallDistance) {{
                    this.takeDamage();
                }}

                if (this.invulnerable && --this.invulnerabilityTimer <= 0) {{
                    this.invulnerable = false;
                }}

                centerCameraOnPlayer();
            }}

            draw() {{
                ctx.save();
                ctx.translate(0, -gameState.cameraY);

                if (this.invulnerable && Math.floor(this.invulnerabilityTimer / 10) % 2) {{
                    ctx.globalAlpha = 0.5;
                }}

                if (mascotImage && mascotImage.complete) {{
                    ctx.save();
                    if (this.direction === -1) {{
                        ctx.scale(-1, 1);
                        ctx.drawImage(mascotImage, -(this.x + this.width), this.y, this.width, this.height);
                    }} else {{
                        ctx.drawImage(mascotImage, this.x, this.y, this.width, this.height);
                    }}
                    ctx.restore();
                }} else {{
                    ctx.fillStyle = '#228B22';
                    ctx.fillRect(this.x, this.y, this.width, this.height);
                    ctx.fillStyle = 'white';
                    ctx.fillRect(this.x + 8, this.y + 10, 6, 6);
                    ctx.fillRect(this.x + 26, this.y + 10, 6, 6);
                    ctx.fillStyle = 'black';
                    ctx.fillRect(this.x + 10, this.y + 12, 2, 2);
                    ctx.fillRect(this.x + 28, this.y + 12, 2, 2);
                    ctx.fillRect(this.x + 18, this.y + 20, 4, 2);
                }}

                ctx.restore();
            }}

            takeDamage() {{
                if (this.invulnerable) return;

                gameState.lives--;
                this.invulnerable = true;
                this.invulnerabilityTimer = 180;

                if (gameState.lives <= 0) {{
                    gameOver();
                }} else {{
                    this.respawn();
                }}
            }}

            respawn() {{
                let target = null;
                let highest = Infinity;
                for (const platform of platforms) {{
                    if (platform.number <= gameState.currentPlatform && platform.y < highest) {{
                        highest = platform.y;
                        target = platform;
                    }}
                }}

                if (target) {{
                    this.x = target.x + target.width / 2 - this.width / 2;
                    this.y = target.y - this.height;
                    this.lastGroundY = target.y;
                }} else {{
                    this.x = 150;
                    this.y = GROUND_TOP - this.height;
                    this.lastGroundY = GROUND_TOP;
                }}

                this.velocityX = 0;
                this.velocityY = 0;
                this.onGround = true;
                this.standingOn = null;
            }}

            setOnGround(platform) {{
                this.onGround = true;
                this.standingOn = platform;
                this.lastGroundY = platform.y;
            }}

            heightInMeters() {{
                return Math.max(0, Math.floor((GROUND_TOP - (this.y + this.height)) / 15));
            }}
        }}

        class Platform {{
            constructor(x, y, width, height, number, type = 'normal') {{
                this.x = x;
                this.y = y;
                this.width = width;
                this.height = height;
                this.number = number;
                this.type = type;
                this.breaking = false;
                this.breakTimer = 0;

                const service = number === 0 ? null : awsServices[number - 1];
                this.serviceName = number === 0 ? START_NAME : service.name;
                this.serviceCategory = number === 0 ? 'Start' : service.category;
                this.serviceDescription = number === 0 ? START_DESC : service.description;

                this.isFinal = number === TOTAL_SERVICES;

                // Só as 'moving' usam isto, mas manter no construtor evita
                // criar campos depois (deoptimiza a classe na V8).
                this.startX = x;
                this.range = 90;
                this.velocityX = number % 2 === 0 ? 1.2 : -1.2;
                this.minX = Math.max(0, x - this.range);
                this.maxX = Math.min(canvas.width - width, x + this.range);
            }}

            update() {{
                if (this.type !== 'moving' || this.minX >= this.maxX) return;

                const previousX = this.x;
                this.x += this.velocityX;

                if (this.x <= this.minX) {{
                    this.x = this.minX;
                    this.velocityX = Math.abs(this.velocityX);
                }} else if (this.x >= this.maxX) {{
                    this.x = this.maxX;
                    this.velocityX = -Math.abs(this.velocityX);
                }}

                // Carrega o jogador junto, senão ela desliza debaixo dos pés dele.
                if (player.standingOn === this) {{
                    player.x += this.x - previousX;
                }}
            }}

            style() {{
                if (this.isFinal) return {{ color: '#FFD700', border: '#CC9A00' }};
                if (this.breaking) return {{ color: '#8B4513', border: '#5D2E0A' }};
                if (this.type === 'breakable') return {{ color: '#8B4513', border: '#5D2E0A' }};
                if (this.type === 'moving') return {{ color: '#4169E1', border: '#2E4BC7' }};
                return CATEGORY_STYLES[this.serviceCategory] || FALLBACK_STYLE;
            }}

            draw() {{
                ctx.save();
                ctx.translate(0, -gameState.cameraY);

                const {{ color, border }} = this.style();

                ctx.fillStyle = 'rgba(0,0,0,0.3)';
                ctx.fillRect(this.x + 3, this.y + 3, this.width, this.height);

                ctx.fillStyle = border;
                ctx.fillRect(this.x - 2, this.y - 2, this.width + 4, this.height + 4);

                ctx.fillStyle = color;
                ctx.fillRect(this.x, this.y, this.width, this.height);

                ctx.fillStyle = this.isFinal ? '#FFFF00' : 'rgba(255,255,255,0.4)';
                ctx.fillRect(this.x, this.y, this.width, 4);

                ctx.fillStyle = 'white';
                ctx.font = 'bold 14px Arial';
                ctx.textAlign = 'center';
                ctx.strokeStyle = 'black';
                ctx.lineWidth = 2;

                const maxWidth = this.width - 15;
                const words = this.serviceName.split(' ');
                let line = '';
                let lines = [];

                for (let n = 0; n < words.length; n++) {{
                    const testLine = line + words[n] + ' ';
                    if (ctx.measureText(testLine).width > maxWidth && n > 0) {{
                        lines.push(line.trim());
                        line = words[n] + ' ';
                    }} else {{
                        line = testLine;
                    }}
                }}
                lines.push(line.trim());

                if (lines.length > 3) {{
                    lines = lines.slice(0, 3);
                    lines[2] += '...';
                }}

                const lineHeight = 13;
                const startY = this.y + (this.height / 2) - ((lines.length - 1) * lineHeight / 2);
                for (let i = 0; i < lines.length; i++) {{
                    const yPos = startY + (i * lineHeight);
                    ctx.strokeText(lines[i], this.x + this.width / 2, yPos);
                    ctx.fillText(lines[i], this.x + this.width / 2, yPos);
                }}

                // O número fica no canto superior, discreto. Antes era desenhado na
                // MESMA linha de base do nome e no meio da margem esquerda: o nome
                // ficava centralizado de fato (52px x 53px de folga), mas o olho lia
                // o vão entre o número e o texto como margem, e a composição parecia
                // deslocada. Recuando o número, o nome lê como o que é — centralizado.
                ctx.save();
                ctx.globalAlpha = 0.7;
                ctx.font = 'bold 9px Arial';
                ctx.fillStyle = '#FFE680';
                ctx.textAlign = 'left';
                ctx.fillText(this.number.toString(), this.x + 4, this.y + 10);
                ctx.restore();

                if (this.isFinal) {{
                    ctx.fillStyle = '#FF0000';
                    ctx.font = 'bold 14px Arial';
                    ctx.textAlign = 'center';
                    ctx.strokeStyle = 'white';
                    ctx.lineWidth = 2;
                    ctx.strokeText('FINAL!', this.x + this.width / 2, this.y - 15);
                    ctx.fillText('FINAL!', this.x + this.width / 2, this.y - 15);
                }}

                ctx.restore();
            }}
        }}

        class Enemy {{
            constructor(x, y, emoji, patrolDistance) {{
                this.x = x;
                this.y = y;
                this.width = 30;
                this.height = 30;
                this.velocityX = Math.random() > 0.5 ? 2 : -2;
                this.emoji = emoji;
                this.patrolDistance = patrolDistance;
                this.startX = x;
            }}

            update() {{
                this.x += this.velocityX;
                if (Math.abs(this.x - this.startX) > this.patrolDistance) {{
                    this.velocityX *= -1;
                }}
            }}

            draw() {{
                ctx.save();
                ctx.translate(0, -gameState.cameraY);
                ctx.font = '24px Arial';
                ctx.textAlign = 'center';
                ctx.fillText(this.emoji, this.x + this.width / 2, this.y + this.height - 5);
                ctx.restore();
            }}
        }}

        class PowerUp {{
            constructor(x, y, type) {{
                this.x = x;
                this.y = y;
                this.width = 25;
                this.height = 25;
                this.type = type;
                this.bobOffset = 0;
                this.emoji = type === 'life' ? '💖' : type === 'score' ? '⭐' : '🍄';
            }}

            update() {{
                this.bobOffset += 0.1;
            }}

            draw() {{
                ctx.save();
                ctx.translate(0, -gameState.cameraY);
                ctx.font = '20px Arial';
                ctx.textAlign = 'center';
                const bobY = this.y + Math.sin(this.bobOffset) * 5;
                ctx.fillText(this.emoji, this.x + this.width / 2, bobY + this.height - 5);
                ctx.restore();
            }}
        }}

        class Collectible {{
            constructor(x, y) {{
                this.x = x;
                this.y = y;
                this.width = 20;
                this.height = 20;
                this.rotation = 0;
            }}

            update() {{
                this.rotation += 0.2;
            }}

            draw() {{
                ctx.save();
                ctx.translate(0, -gameState.cameraY);
                ctx.font = '16px Arial';
                ctx.textAlign = 'center';
                const coin = Math.floor(this.rotation * 2) % 2 === 0 ? '🪙' : '💰';
                ctx.fillText(coin, this.x + this.width / 2, this.y + this.height - 2);
                ctx.restore();
            }}
        }}

        let player = new Player(150, GROUND_TOP - 50);
        let platforms = [];
        let enemies = [];
        let powerUps = [];
        let collectibles = [];

        function initLevel() {{
            platforms = [];
            enemies = [];
            powerUps = [];
            collectibles = [];

            platforms.push(new Platform(0, GROUND_TOP, canvas.width, GROUND_HEIGHT, 0));

            const enemyEmojis = ['🔥', '🦑', '🦨', '🐀', '🐓', '🦆', '🐖', '💩'];

            for (let i = 1; i <= TOTAL_SERVICES; i++) {{
                const width = 200 + Math.random() * 80;
                // A largura entra na conta: antes a plataforma vazava pela direita.
                const x = Math.random() * (canvas.width - width);
                const y = WORLD_HEIGHT - (i * PLATFORM_SPACING);

                // else-if: 175 e 350 são múltiplos de 25 E de 35, e o segundo if
                // sobrescrevia o primeiro, matando aquelas 'breakable'.
                let type = 'normal';
                if (i < TOTAL_SERVICES) {{
                    if (i % 35 === 0) type = 'moving';
                    else if (i % 25 === 0) type = 'breakable';
                }}

                platforms.push(new Platform(x, y, width, 30, i, type));

                if (i > 5 && Math.random() < 0.25) {{
                    const emoji = enemyEmojis[Math.floor(Math.random() * enemyEmojis.length)];
                    // Patrulha limitada à plataforma: antes eles flutuavam no vazio.
                    const patrol = Math.max(10, (width - 30) / 2 - 5);
                    enemies.push(new Enemy(x + width / 2 - 15, y - 35, emoji, patrol));
                }}

                if (Math.random() < 0.12) {{
                    const types = ['life', 'score', 'power'];
                    powerUps.push(new PowerUp(
                        x + width / 2,
                        y - 35,
                        types[Math.floor(Math.random() * types.length)]
                    ));
                }}

                if (Math.random() < 0.35) {{
                    collectibles.push(new Collectible(x + Math.random() * (width - 40) + 20, y - 30));
                }}
            }}

            player.x = 150;
            player.y = GROUND_TOP - player.height;
            player.velocityX = 0;
            player.velocityY = 0;
            player.onGround = true;
            player.standingOn = null;
            player.lastGroundY = GROUND_TOP;

            // A câmera só é ajustada dentro de player.update(), que não roda
            // enquanto o jogo não começou. Sem isto, a tela de início mostrava
            // o topo do mundo (a última plataforma) em vez do mascote no chão.
            centerCameraOnPlayer();
        }}

        function centerCameraOnPlayer() {{
            gameState.cameraY = Math.max(
                0,
                Math.min(player.y - canvas.height / 2, WORLD_HEIGHT - canvas.height)
            );
        }}

        function checkCollision(a, b) {{
            return a.x < b.x + b.width &&
                   a.x + a.width > b.x &&
                   a.y < b.y + b.height &&
                   a.y + a.height > b.y;
        }}

        function checkPlatformCollisions() {{
            for (let i = platforms.length - 1; i >= 0; i--) {{
                const platform = platforms[i];

                if (platform.breaking) {{
                    if (--platform.breakTimer <= 0) platforms.splice(i, 1);
                }}

                if (!checkCollision(player, platform)) continue;
                if (player.velocityY <= 0 || player.y >= platform.y) continue;

                player.y = platform.y - player.height;
                player.velocityY = 0;
                player.setOnGround(platform);

                // O card segue a plataforma em que o jogador está PISANDO — não a
                // mais alta já alcançada. Descer para uma plataforma anterior traz
                // a descrição dela de volta.
                showService(platform);

                if (platform.number > gameState.currentPlatform) {{
                    gameState.currentPlatform = platform.number;
                    gameState.score += 75;

                    if (platform.isFinal) {{
                        gameWin();
                        return;
                    }}
                }}

                if (platform.type === 'breakable' && !platform.breaking) {{
                    platform.breaking = true;
                    platform.breakTimer = 90;   // 1,5s em ticks — não setTimeout,
                    gameState.score += 150;     // que ignora pausa e restart.
                }}
            }}
        }}

        const START_NAME = 'Início da Escalada AWS';
        const START_DESC = 'Comece sua aventura pelos serviços AWS! A cada plataforma que você ' +
                           'pisar, a descrição do serviço correspondente aparece aqui.';

        // Qual plataforma o card está exibindo. Sem isto, a colisão reescreveria
        // o DOM a cada quadro enquanto o jogador estivesse parado em cima dela.
        let displayedPlatform = -1;

        function showService(platform) {{
            if (!platform || platform.number === displayedPlatform) return;
            displayedPlatform = platform.number;

            // textContent, nunca innerHTML: a descrição vem do JSON e não deve
            // ser interpretada como marcação.
            document.getElementById('cardDescription').textContent = platform.serviceDescription;
        }}

        function checkEnemyCollisions() {{
            for (let i = enemies.length - 1; i >= 0; i--) {{
                const enemy = enemies[i];
                if (!checkCollision(player, enemy)) continue;

                if (player.velocityY > 0 && player.y < enemy.y) {{
                    enemies.splice(i, 1);
                    player.velocityY = -12;
                    gameState.score += 250;
                }} else {{
                    player.takeDamage();
                }}
            }}
        }}

        function checkPowerUpCollisions() {{
            for (let i = powerUps.length - 1; i >= 0; i--) {{
                const powerUp = powerUps[i];
                if (!checkCollision(player, powerUp)) continue;

                if (powerUp.type === 'life') {{
                    gameState.lives++;
                    gameState.score += 500;
                }} else if (powerUp.type === 'score') {{
                    gameState.score += 1000;
                }} else {{
                    gameState.score += 300;
                }}
                powerUps.splice(i, 1);   // coletado sai do array, não fica sendo iterado para sempre
            }}
        }}

        function checkCollectibleCollisions() {{
            for (let i = collectibles.length - 1; i >= 0; i--) {{
                if (!checkCollision(player, collectibles[i])) continue;
                collectibles.splice(i, 1);
                gameState.score += 100;
            }}
        }}

        function update() {{
            if (!gameState.gameRunning) return;

            for (const platform of platforms) platform.update();

            player.update();

            for (const enemy of enemies) enemy.update();
            for (const powerUp of powerUps) powerUp.update();
            for (const collectible of collectibles) collectible.update();

            checkPlatformCollisions();
            checkEnemyCollisions();
            checkPowerUpCollisions();
            checkCollectibleCollisions();

            document.getElementById('score').textContent = gameState.score;
            document.getElementById('lives').textContent = gameState.lives;
            document.getElementById('height').textContent = player.heightInMeters();
        }}

        function isVisible(entity, margin) {{
            return entity.y > gameState.cameraY - margin &&
                   entity.y < gameState.cameraY + canvas.height + margin;
        }}

        function draw() {{
            const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            gradient.addColorStop(0, '#001122');
            gradient.addColorStop(0.3, '#003366');
            gradient.addColorStop(0.7, '#004488');
            gradient.addColorStop(1, '#87CEEB');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            for (const platform of platforms) if (isVisible(platform, 150)) platform.draw();
            for (const enemy of enemies) if (isVisible(enemy, 100)) enemy.draw();
            for (const powerUp of powerUps) if (isVisible(powerUp, 100)) powerUp.draw();
            for (const collectible of collectibles) if (isVisible(collectible, 100)) collectible.draw();

            player.draw();
            drawProgressIndicator();
        }}

        function drawProgressIndicator() {{
            const width = 200;
            const height = 20;
            const x = canvas.width - width - 20;
            const y = 20;

            ctx.fillStyle = 'rgba(0,0,0,0.5)';
            ctx.fillRect(x - 5, y - 5, width + 10, height + 10);

            ctx.fillStyle = '#333';
            ctx.fillRect(x, y, width, height);

            const progress = gameState.currentPlatform / TOTAL_SERVICES;
            ctx.fillStyle = progress < 0.5 ? '#FF6B35' : progress < 0.8 ? '#FFA502' : '#32CD32';
            ctx.fillRect(x, y, width * progress, height);

            ctx.fillStyle = 'white';
            ctx.font = 'bold 12px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(
                gameState.currentPlatform + '/' + TOTAL_SERVICES,
                x + width / 2,
                y + 15
            );
        }}

        function gameLoop(now) {{
            requestAnimationFrame(gameLoop);

            if (lastFrameTime === null) lastFrameTime = now;
            const elapsed = Math.min(now - lastFrameTime, MAX_FRAME_MS);
            lastFrameTime = now;

            if (gameState.started) {{
                accumulator += elapsed;
                let ticks = 0;
                while (accumulator >= TICK_MS && ticks < MAX_TICKS_PER_FRAME) {{
                    update();
                    accumulator -= TICK_MS;
                    ticks++;
                }}
                // Não deixa a dívida acumular se a máquina não deu conta.
                if (ticks === MAX_TICKS_PER_FRAME) accumulator = 0;
            }}

            draw();
        }}

        function endRound(screenId, sound) {{
            gameState.gameRunning = false;
            if (audioElements.sonora) {{
                audioElements.sonora.pause();
                audioElements.sonora.currentTime = 0;
            }}
            playAudio(sound);
            document.getElementById(screenId).style.display = 'block';
        }}

        function gameOver() {{
            document.getElementById('finalScore').textContent = gameState.score;
            document.getElementById('finalHeight').textContent = player.heightInMeters();

            const service = gameState.currentPlatform > 0
                ? awsServices[gameState.currentPlatform - 1]
                : null;
            document.getElementById('finalService').textContent =
                service ? service.name : 'Início da Escalada AWS';

            endRound('gameOver', 'gameover');
        }}

        function gameWin() {{
            document.getElementById('winScore').textContent = gameState.score;
            endRound('gameWin', 'aplausos');
        }}

        function restartGame() {{
            stopAllAudio();

            gameState = newGameState();
            gameState.started = true;
            accumulator = 0;
            lastFrameTime = null;

            player = new Player(150, GROUND_TOP - 50);
            displayedPlatform = -1;   // força o card a reescrever
            initLevel();
            showService(platforms[0]);

            document.getElementById('gameOver').style.display = 'none';
            document.getElementById('gameWin').style.display = 'none';

            playAudio('sonora');
            canvas.focus();
        }}

        function startGame() {{
            initAudio();
            gameState.started = true;
            accumulator = 0;
            lastFrameTime = null;
            document.getElementById('startOverlay').style.display = 'none';
            // play() aqui dentro do clique: é o único momento em que o navegador
            // libera o áudio. Fora do handler ele bloqueia por autoplay policy.
            playAudio('sonora');
            canvas.focus();
        }}

        document.getElementById('startBtn').addEventListener('click', startGame);

        // O jogo vive num iframe. Sem isso, as setas iam para a página do
        // Streamlit (que rolava a tela) e o jogo não respondia ao teclado.
        canvas.addEventListener('mousedown', () => canvas.focus());

        window.addEventListener('keydown', (e) => {{
            gameState.keys[e.key] = true;
            if (e.key === ' ' || e.key.startsWith('Arrow')) e.preventDefault();
        }});

        window.addEventListener('keyup', (e) => {{
            gameState.keys[e.key] = false;
        }});

        let touchStartX = 0;
        let touchStartY = 0;

        canvas.addEventListener('touchstart', (e) => {{
            e.preventDefault();
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
        }}, {{ passive: false }});

        canvas.addEventListener('touchend', (e) => {{
            e.preventDefault();
            const touch = e.changedTouches[0];
            const deltaX = touch.clientX - touchStartX;
            const deltaY = touch.clientY - touchStartY;

            if (Math.abs(deltaY) > Math.abs(deltaX)) {{
                if (deltaY < -30 && player.onGround) {{
                    player.velocityY = -player.jumpPower;
                    player.onGround = false;
                    playAudio('pulo');
                }}
            }} else if (Math.abs(deltaX) > 30) {{
                const key = deltaX > 0 ? 'ArrowRight' : 'ArrowLeft';
                gameState.keys[key] = true;
                setTimeout(() => {{ gameState.keys[key] = false; }}, 200);
            }}
        }}, {{ passive: false }});

        initLevel();
        showService(platforms[0]);
        requestAnimationFrame(gameLoop);
    </script>
</body>
</html>
'''


with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <h3 style="color: #333; font-size: 18px;">🎨 Categorias & Cores</h3>
        <p style="font-size: 12px; color: #666; margin-bottom: 15px;">
            📊 Total: {len(aws_services)} serviços AWS
        </p>
    </div>
    """, unsafe_allow_html=True)

    for category, count in sorted(category_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        color = CATEGORY_COLORS.get(category, FALLBACK_COLOR)
        label = CATEGORY_LABELS.get(category, category)
        st.markdown(f"""
        <div style="display: flex; align-items: center; background: rgba(255,255,255,0.9); padding: 6px 10px; border-radius: 20px; border: 2px solid {color}; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 8px;">
            <div style="width: 16px; height: 16px; background: {color}; border-radius: 50%; margin-right: 8px; border: 1px solid rgba(0,0,0,0.2); flex-shrink: 0;"></div>
            <span style="font-size: 11px; font-weight: 600; color: #333; text-align: left;">{label}</span>
            <span style="margin-left: auto; font-size: 10px; color: #888;">{count}</span>
        </div>
        """, unsafe_allow_html=True)

components.html(
    build_game_html(),
    height=GAME_HEIGHT + CARD_GAP + CARD_HEIGHT + 14,
    scrolling=False,
)

st.markdown("""
<div style="text-align: center;">
    🧠 Memorize os serviços AWS enquanto escala com o S3!<br>
    Por <strong>Ary Ribeiro</strong> — <a href="https://linkedin.com/in/aryribeiro" target="_blank">linkedin.com/in/aryribeiro</a>
</div>
""", unsafe_allow_html=True)
