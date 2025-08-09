import streamlit as st
import streamlit.components.v1 as components
import json
import os
import base64

# Configuração da página
st.set_page_config(
    page_title="AWS Game 🎮",
    page_icon="☁️",
    layout="centered"
)

# Título e descrição centralizados
st.markdown("""
<div style="text-align: center;">
    <h1>☁️ AWS Game 🎮</h1>
    <h4>S3 Climbing Adventure</h4>
</div>
""", unsafe_allow_html=True)

# Função para carregar imagem como base64
@st.cache_data
def load_image_as_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        return None

# Função para carregar áudio como base64
@st.cache_data
def load_audio_as_base64(audio_path):
    try:
        with open(audio_path, "rb") as audio_file:
            return base64.b64encode(audio_file.read()).decode()
    except FileNotFoundError:
        return None

# Carregar dados dos serviços AWS
@st.cache_data
def load_aws_services():
    try:
        with open('servicos.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extrair apenas os serviços (excluindo o nó central)
        services = [node for node in data['nodes'] if not node.get('isCentral', False)]
        
        # Criar lista expandida com serviços S3 adicionais para chegar a 234
        s3_services = [
            "S3 Express One Zone", "S3 Transfer Acceleration",
            "S3 Cross-Region Replication", "S3 Same-Region Replication", "S3 Inventory", "S3 Analytics",
        ]
        
        # Combinar serviços reais com S3 expandido
        all_services = []
        
        # Adicionar serviços reais primeiro
        for service in services:
            # Verificar diferentes possíveis nomes do campo categoria (maiúsculo e minúsculo)
            category = (service.get('Category') or service.get('category') or 
                       service.get('Categoria') or service.get('group') or 
                       service.get('type') or 'AWS')
            all_services.append({
                'name': service['name'],
                'description': service.get('Description', service.get('description', '')),
                'category': category
            })
        
        # Adicionar serviços S3 adicionais para completar 234
        for s3_service in s3_services:
            if len(all_services) >= 234:
                break
            all_services.append({
                'name': s3_service,
                'description': f'Recurso do S3: {s3_service}',
                'category': 'S3 Services'
            })
        
        # Garantir exatamente 234 serviços
        while len(all_services) < 234:
            all_services.append({
                'name': f'AWS Advanced Service {len(all_services) + 1}',
                'description': 'Serviço AWS',
                'category': 'AWS'
            })
        
        return all_services[:234]  # Garantir exatamente 234
        
    except FileNotFoundError:
        st.error("Arquivo servicos.json não encontrado na raiz do projeto!")
        return []
    except json.JSONDecodeError:
        st.error("Erro ao decodificar o arquivo servicos.json!")
        return []

# Carregar categorias AWS
@st.cache_data
def load_aws_categories():
    try:
        with open('categorias aws.txt', 'r', encoding='utf-8') as f:
            categories = [line.strip() for line in f.readlines() if line.strip()]
        return categories
    except FileNotFoundError:
        # Fallback categories from document
        return [
            "Analytics", "Armazenamento", "Banco de Dados", "Blockchain", "Busca",
            "Centro de Atendimento", "Computação", "Computação Quântica", "Comunicação",
            "Conformidade", "Desenvolvimento de Jogos", "Ferramentas de Desenvolvedor",
            "Geoespacial", "Gerenciamento de Custos", "Gerenciamento e Governança",
            "Híbrido", "Integração de Aplicações", "Internet das Coisas", "Machine Learning",
            "Marketing", "Migração e Transferência", "Monitoramento", "Mídia", "Otimização",
            "Produtividade", "Realidade Virtual/Aumentada", "Rede e Entrega de Conteúdo",
            "Robótica", "Satélite", "Saúde", "Segurança e Identidade", "Suporte",
            "Suporte ao Desenvolvedor", "Terceiros", "Usuário Final"
        ]

# Carregar recursos
aws_services = load_aws_services()
aws_categories = load_aws_categories()
mascot_base64 = load_image_as_base64('static/mascote.png')
aplausos_base64 = load_audio_as_base64('static/aplausos.mp3')
pulo_base64 = load_audio_as_base64('static/pulo.mp3')
gameover_base64 = load_audio_as_base64('static/gameover.mp3')
sonora_base64 = load_audio_as_base64('static/sonora.mp3')

if not aws_services:
    st.stop()

# Definir cores para cada categoria
category_colors = {
    "Analytics": "#FFA502",
    "Armazenamento": "#5F27CD", 
    "Banco de Dados": "#FF4757",
    "Blockchain": "#3742FA",
    "Busca": "#2ED573",
    "Centro de Atendimento": "#FF6348",
    "Computação": "#4ECDC4",
    "Computação Quântica": "#A4B0BE",
    "Comunicação": "#00D2D3",
    "Conformidade": "#747D8C",
    "Desenvolvimento de Jogos": "#5F27CD",
    "Ferramentas de Desenvolvedor": "#FF9FF3",
    "Geoespacial": "#54A0FF",
    "Gerenciamento de Custos": "#5F27CD",
    "Gerenciamento e Governança": "#FF6B35",
    "Híbrido": "#26DE81",
    "Integração de Aplicações": "#FD79A8",
    "Internet das Coisas": "#FDCB6E",
    "Machine Learning": "#6C5CE7",
    "Marketing": "#A29BFE",
    "Migração e Transferência": "#FC7753",
    "Monitoramento": "#F8B500",
    "Mídia": "#E17055",
    "Otimização": "#00B894",
    "Produtividade": "#00CEC9",
    "Realidade Virtual/Aumentada": "#E84393",
    "Rede e Entrega de Conteúdo": "#0984E3",
    "Robótica": "#6C5CE7",
    "Satélite": "#2D3436",
    "Saúde": "#00B894",
    "Segurança e Identidade": "#54A0FF",
    "Suporte": "#FDCB6E",
    "Suporte ao Desenvolvedor": "#FD79A8",
    "Terceiros": "#636E72",
    "Usuário Final": "#74B9FF"
}

# HTML do jogo modificado
game_html = f'''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title> ... S3 Climbing Adventure</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: linear-gradient(180deg, #001122 0%, #003366 50%, #87CEEB 100%);
            font-family: 'Arial', sans-serif;
            overflow: hidden;
        }}
        
        #gameContainer {{
            position: relative;
            width: 700px;
            height: 650px;
            margin: 0 auto;
            border: 3px solid #2E8B57;
            border-radius: 10px;
            overflow: hidden;
        }}
        
        canvas {{
            display: block;
            background: transparent;
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
        }}
        
        #gameOver, #gameWin {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.9);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            display: none;
            z-index: 200;
            border: 3px solid #FFD700;
        }}
        
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
        
        button:hover {{
            background: #32CD32;
        }}
    </style>
</head>
<body>
    <div id="gameContainer">
        <canvas id="gameCanvas" width="700" height="650"></canvas>
        
        <!-- UI Elements -->
        <div id="ui">
            <div>Pontos: <span id="score">0</span></div>
            <div>Vidas: <span id="lives">5</span></div>
            <div>Altura: <span id="height">0</span>m</div>
            <div style="font-size: 12px; margin-top: 5px;">Atual: <span id="currentService">Início</span></div>
        </div>
        
        <!-- Game Over Screen -->
        <div id="gameOver">
            <h2>💀 Game Over!</h2>
            <p>Você parou no: <span id="finalService">Início</span></p>
            <p>Altura alcançada: <span id="finalHeight">0</span>m</p>
            <p>Pontuação Final: <span id="finalScore">0</span></p>
            <button onclick="restartGame()">🔄 Jogar Novamente</button>
        </div>
        
        <!-- Victory Screen -->
        <div id="gameWin">
            <h2>🏆 PARABÉNS!</h2>
            <p>Completou + de 200 serviços AWS!</p>
            <p>Pontuação Final: <span id="winScore">0</span></p>
            <button onclick="restartGame()">🔄 Jogar Novamente</button>
        </div>
    </div>

    <script>
        // Audio Setup
        const audioSources = {{
            aplausos: {json.dumps(aplausos_base64) if aplausos_base64 else 'null'},
            pulo: {json.dumps(pulo_base64) if pulo_base64 else 'null'},
            gameover: {json.dumps(gameover_base64) if gameover_base64 else 'null'},
            sonora: {json.dumps(sonora_base64) if sonora_base64 else 'null'}
        }};
        
        const audioElements = {{}};
        
        // Initialize audio elements
        function initAudio() {{
            for (const [key, base64Data] of Object.entries(audioSources)) {{
                if (base64Data) {{
                    audioElements[key] = new Audio('data:audio/mp3;base64,' + base64Data);
                    if (key === 'sonora') {{
                        audioElements[key].loop = true;
                        audioElements[key].volume = 0.3;
                    }}
                }}
            }}
        }}
        
        // Play audio function
        function playAudio(audioKey) {{
            if (audioElements[audioKey]) {{
                audioElements[audioKey].currentTime = 0;
                audioElements[audioKey].play().catch(e => console.log('Audio play failed:', e));
            }}
        }}
        
        // AWS Services Data
        const awsServices = {json.dumps(aws_services)};
        
        // Game Canvas Setup
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        // Game State
        let gameState = {{
            score: 0,
            lives: 5,
            currentPlatform: 0,
            gameRunning: true,
            keys: {{}},
            camera: {{ x: 0, y: 0 }},
            worldHeight: 234 * 220,
            backgroundMusicStarted: false
        }};
        
        // Load mascot image
        let mascotImage = null;
        if ({json.dumps(bool(mascot_base64))}) {{
            mascotImage = new Image();
            mascotImage.src = 'data:image/png;base64,{mascot_base64 or ""}';
        }}
        
        // Player Class (Mascot)
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
                this.direction = 1;
                this.invulnerable = false;
                this.invulnerabilityTimer = 0;
                this.maxFallDistance = 700;
                this.lastGroundY = y;
            }}
            
            update() {{
                // Handle input
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
                
                // Apply gravity
                this.velocityY += 0.8;
                
                // Update position
                this.x += this.velocityX;
                this.y += this.velocityY;
                
                // Friction
                this.velocityX *= 0.85;
                
                // Boundary checks (horizontal wrapping)
                if (this.x < -this.width) this.x = canvas.width;
                if (this.x > canvas.width) this.x = -this.width;
                
                // Check for fall death
                if (this.y > this.lastGroundY + this.maxFallDistance) {{
                    this.takeDamage();
                }}
                
                // Invulnerability timer
                if (this.invulnerable) {{
                    this.invulnerabilityTimer--;
                    if (this.invulnerabilityTimer <= 0) {{
                        this.invulnerable = false;
                    }}
                }}
                
                // Update camera to follow player
                gameState.camera.y = this.y - canvas.height / 2;
                if (gameState.camera.y < 0) gameState.camera.y = 0;
                if (gameState.camera.y > gameState.worldHeight - canvas.height) {{
                    gameState.camera.y = gameState.worldHeight - canvas.height;
                }}
            }}
            
            draw() {{
                ctx.save();
                
                // Apply camera transform
                ctx.translate(0, -gameState.camera.y);
                
                // Flashing effect when invulnerable
                if (this.invulnerable && Math.floor(this.invulnerabilityTimer / 10) % 2) {{
                    ctx.globalAlpha = 0.5;
                }}
                
                // Draw mascot image if available, otherwise draw fallback
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
                    // Fallback: simple colored rectangle
                    ctx.fillStyle = '#228B22';
                    ctx.fillRect(this.x, this.y, this.width, this.height);
                    
                    // Simple face
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
                if (!this.invulnerable) {{
                    gameState.lives--;
                    this.invulnerable = true;
                    this.invulnerabilityTimer = 180;
                    
                    if (gameState.lives <= 0) {{
                        gameOver();
                    }} else {{
                        this.respawn();
                    }}
                }}
            }}
            
            respawn() {{
                let respawnPlatform = null;
                let highestY = Infinity;
                
                for (let platform of platforms) {{
                    if (platform.number <= gameState.currentPlatform && platform.y < highestY) {{
                        highestY = platform.y;
                        respawnPlatform = platform;
                    }}
                }}
                
                if (respawnPlatform) {{
                    this.x = respawnPlatform.x + respawnPlatform.width / 2 - this.width / 2;
                    this.y = respawnPlatform.y - this.height;
                    this.lastGroundY = respawnPlatform.y;
                }} else {{
                    this.x = 150;
                    this.y = gameState.worldHeight - 150;
                    this.lastGroundY = gameState.worldHeight - 100;
                }}
                
                this.velocityX = 0;
                this.velocityY = 0;
                this.onGround = true;
            }}
            
            setOnGround(y) {{
                this.onGround = true;
                this.lastGroundY = y;
            }}
        }}
        
        // Platform Class
        class Platform {{
            constructor(x, y, width, height, number, type = 'normal') {{
                this.x = x;
                this.y = y;
                this.width = width;
                this.height = height;
                this.number = number;
                this.type = type;
                this.visited = false;
                this.serviceName = number === 0 ? 'Início da Escalada AWS' : (awsServices[number - 1] ? awsServices[number - 1].name : `Serviço AWS ${{number}}`);
                this.serviceCategory = number === 0 ? 'Start' : (awsServices[number - 1] ? awsServices[number - 1].category : 'AWS');
                this.serviceDescription = number === 0 ? 'Comece sua aventura pelos serviços AWS!' : (awsServices[number - 1] ? awsServices[number - 1].description : 'Serviço AWS especializado');
            }}
            
            draw() {{
                ctx.save();
                ctx.translate(0, -gameState.camera.y);
                
                // Platform color based on type and category
                let color = '#228B22';
                let borderColor = '#1F5F1F';
                
                if (this.type === 'breakable') {{
                    color = '#8B4513';
                    borderColor = '#5D2E0A';
                }} else if (this.type === 'moving') {{
                    color = '#4169E1';
                    borderColor = '#2E4BC7';
                }} else if (this.number === 234) {{
                    color = '#FFD700';
                    borderColor = '#CC9A00';
                }} else {{
                    // Mapeamento de cores baseado nas categorias AWS
                    const categoryColors = {{
                        'Analytics': '#FFA502',
                        'Armazenamento': '#5F27CD', 
                        'Banco de Dados': '#FF4757',
                        'Blockchain': '#3742FA',
                        'Busca': '#2ED573',
                        'Centro de Atendimento': '#FF6348',
                        'Computação': '#4ECDC4',
                        'Computação Quântica': '#A4B0BE',
                        'Comunicação': '#00D2D3',
                        'Conformidade': '#747D8C',
                        'Desenvolvimento de Jogos': '#5F27CD',
                        'Ferramentas de Desenvolvedor': '#FF9FF3',
                        'Geoespacial': '#54A0FF',
                        'Gerenciamento de Custos': '#5F27CD',
                        'Gerenciamento e Governança': '#FF6B35',
                        'Híbrido': '#26DE81',
                        'Integração de Aplicações': '#FD79A8',
                        'Internet das Coisas': '#FDCB6E',
                        'Machine Learning': '#6C5CE7',
                        'Marketing': '#A29BFE',
                        'Migração e Transferência': '#FC7753',
                        'Monitoramento': '#F8B500',
                        'Mídia': '#E17055',
                        'Otimização': '#00B894',
                        'Produtividade': '#00CEC9',
                        'Realidade Virtual/Aumentada': '#E84393',
                        'Rede e Entrega de Conteúdo': '#0984E3',
                        'Robótica': '#6C5CE7',
                        'Satélite': '#2D3436',
                        'Saúde': '#00B894',
                        'Segurança e Identidade': '#54A0FF',
                        'Suporte': '#FDCB6E',
                        'Suporte ao Desenvolvedor': '#FD79A8',
                        'Terceiros': '#636E72',
                        'Usuário Final': '#74B9FF',
                        'S3 Services': '#FF6B35',
                        'AWS': '#32CD32',
                        'Start': '#FFD700'
                    }};
                    
                    // Definir cor da plataforma baseada na categoria
                    if (categoryColors[this.serviceCategory]) {{
                        color = categoryColors[this.serviceCategory];
                        // Calcular cor da borda (mais escura)
                        const hexToRgb = (hex) => {{
                            const r = parseInt(hex.slice(1, 3), 16);
                            const g = parseInt(hex.slice(3, 5), 16);
                            const b = parseInt(hex.slice(5, 7), 16);
                            return [r, g, b];
                        }};
                        const [r, g, b] = hexToRgb(color);
                        borderColor = `rgb(${{Math.max(0, r-50)}}, ${{Math.max(0, g-50)}}, ${{Math.max(0, b-50)}})`;
                    }} else {{
                        // Fallback para categorias não mapeadas
                        color = '#666666';
                        borderColor = '#444444';
                    }}
                }}
                
                // Draw platform shadow
                ctx.fillStyle = 'rgba(0,0,0,0.3)';
                ctx.fillRect(this.x + 3, this.y + 3, this.width, this.height);
                
                // Draw platform border
                ctx.fillStyle = borderColor;
                ctx.fillRect(this.x - 2, this.y - 2, this.width + 4, this.height + 4);
                
                // Draw platform main body
                ctx.fillStyle = color;
                ctx.fillRect(this.x, this.y, this.width, this.height);
                
                // Platform top highlight
                ctx.fillStyle = this.number === 234 ? '#FFFF00' : 'rgba(255,255,255,0.4)';
                ctx.fillRect(this.x, this.y, this.width, 4);
                
                // Service name (wrapped text for long names)
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
                    const metrics = ctx.measureText(testLine);
                    const testWidth = metrics.width;
                    if (testWidth > maxWidth && n > 0) {{
                        lines.push(line.trim());
                        line = words[n] + ' ';
                    }} else {{
                        line = testLine;
                    }}
                }}
                lines.push(line.trim());
                
                // Limit to 3 lines max
                if (lines.length > 3) {{
                    lines = lines.slice(0, 3);
                    lines[2] = lines[2] + '...';
                }}
                
                // Draw text lines
                const lineHeight = 13;
                const startY = this.y + (this.height / 2) - ((lines.length - 1) * lineHeight / 2);
                
                for (let i = 0; i < lines.length; i++) {{
                    const yPos = startY + (i * lineHeight);
                    ctx.strokeText(lines[i], this.x + this.width/2, yPos);
                    ctx.fillText(lines[i], this.x + this.width/2, yPos);
                }}
                
                // Platform number in corner
                ctx.font = 'bold 10px Arial';
                ctx.fillStyle = 'yellow';
                ctx.textAlign = 'left';
                ctx.strokeStyle = 'black';
                ctx.lineWidth = 1;
                ctx.strokeText(this.number.toString(), this.x + 5, this.y + 15);
                ctx.fillText(this.number.toString(), this.x + 5, this.y + 15);
                
                // Special indicator for final platform
                if (this.number === 234) {{
                    ctx.fillStyle = '#FF0000';
                    ctx.font = 'bold 14px Arial';
                    ctx.textAlign = 'center';
                    ctx.strokeStyle = 'white';
                    ctx.lineWidth = 2;
                    ctx.strokeText('FINAL!', this.x + this.width/2, this.y - 15);
                    ctx.fillText('FINAL!', this.x + this.width/2, this.y - 15);
                }}
                
                ctx.restore();
            }}
        }}
        
        // Enemy Class
        class Enemy {{
            constructor(x, y, emoji = '👾') {{
                this.x = x;
                this.y = y;
                this.width = 30;
                this.height = 30;
                this.velocityX = Math.random() > 0.5 ? 2 : -2;
                this.emoji = emoji;
                this.patrolDistance = 120;
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
                ctx.translate(0, -gameState.camera.y);
                ctx.font = '24px Arial';
                ctx.textAlign = 'center';
                ctx.fillText(this.emoji, this.x + this.width/2, this.y + this.height - 5);
                ctx.restore();
            }}
        }}
        
        // PowerUp Class
        class PowerUp {{
            constructor(x, y, type = 'life') {{
                this.x = x;
                this.y = y;
                this.width = 25;
                this.height = 25;
                this.type = type;
                this.collected = false;
                this.bobOffset = 0;
                this.emoji = type === 'life' ? '💖' : type === 'score' ? '⭐' : '🍄';
            }}
            
            update() {{
                this.bobOffset += 0.1;
            }}
            
            draw() {{
                if (!this.collected) {{
                    ctx.save();
                    ctx.translate(0, -gameState.camera.y);
                    const bobY = this.y + Math.sin(this.bobOffset) * 5;
                    ctx.font = '20px Arial';
                    ctx.textAlign = 'center';
                    ctx.fillText(this.emoji, this.x + this.width/2, bobY + this.height - 5);
                    ctx.restore();
                }}
            }}
        }}
        
        // Collectible Class
        class Collectible {{
            constructor(x, y) {{
                this.x = x;
                this.y = y;
                this.width = 20;
                this.height = 20;
                this.collected = false;
                this.rotation = 0;
            }}
            
            update() {{
                this.rotation += 0.2;
            }}
            draw() {{
               if (!this.collected) {{
                   ctx.save();
                   ctx.translate(0, -gameState.camera.y);
                   ctx.font = '16px Arial';
                   ctx.textAlign = 'center';
                   let coin = Math.floor(this.rotation * 2) % 2 === 0 ? '🪙' : '💰';
                   ctx.fillText(coin, this.x + this.width/2, this.y + this.height - 2);
                   ctx.restore();
               }}
           }}
       }}
       
       // Game Objects
       let player = new Player(150, 0);
       let platforms = [];
       let enemies = [];
       let powerUps = [];
       let collectibles = [];
       
       // Initialize Level with 234 platforms
       function initLevel() {{
           platforms = [];
           enemies = [];
           powerUps = [];
           collectibles = [];
           
           // Ground platform (platform 0)
           platforms.push(new Platform(0, gameState.worldHeight - 60, canvas.width, 60, 0));
           
           // Generate 234 platforms going upward
           for (let i = 1; i <= 234; i++) {{
               let x = Math.random() * (canvas.width - 250);
               let y = gameState.worldHeight - (i * 220);
               let width = 200 + Math.random() * 80;
               
               let type = 'normal';
               if (i % 25 === 0 && i < 234) type = 'breakable';
               if (i % 35 === 0 && i < 234) type = 'moving';
               
               platforms.push(new Platform(x, y, width, 30, i, type));
               
               if (i > 5 && Math.random() < 0.25) {{
                   let enemyEmojis = ['🐓', '🐖', '🦨', '🐀', '🐃', '🦆', '🦑', '💩'];
                   let emoji = enemyEmojis[Math.floor(Math.random() * enemyEmojis.length)];
                   enemies.push(new Enemy(x + 30, y - 35, emoji));
               }}
               
               if (Math.random() < 0.12) {{
                   let types = ['life', 'score', 'power'];
                   let type = types[Math.floor(Math.random() * types.length)];
                   powerUps.push(new PowerUp(x + width/2, y - 35, type));
               }}
               
               if (Math.random() < 0.35) {{
                   collectibles.push(new Collectible(x + Math.random() * (width - 40) + 20, y - 30));
               }}
           }}
           
           player.x = 150;
           player.y = gameState.worldHeight - 180;
           player.lastGroundY = gameState.worldHeight - 60;
       }}
       
       function checkCollision(rect1, rect2) {{
           return rect1.x < rect2.x + rect2.width &&
                  rect1.x + rect1.width > rect2.x &&
                  rect1.y < rect2.y + rect2.height &&
                  rect1.y + rect1.height > rect2.y;
       }}
       
       function checkPlatformCollisions() {{
           for (let platform of platforms) {{
               if (checkCollision(player, platform)) {{
                   if (player.velocityY > 0 && player.y < platform.y) {{
                       player.y = platform.y - player.height;
                       player.velocityY = 0;
                       player.setOnGround(platform.y);
                       
                       if (platform.number > gameState.currentPlatform) {{
                           gameState.currentPlatform = platform.number;
                           gameState.score += 75;
                           
                           updateCurrentServiceUI(platform.serviceName);
                           
                           if (platform.number === 234) {{
                               gameWin();
                               return;
                           }}
                       }}
                       
                       if (platform.type === 'breakable' && !platform.visited) {{
                           platform.visited = true;
                           setTimeout(() => {{
                               let index = platforms.indexOf(platform);
                               if (index > -1) platforms.splice(index, 1);
                           }}, 1500);
                           gameState.score += 150;
                       }}
                   }}
               }}
           }}
       }}
       
       function updateCurrentServiceUI(serviceName) {{
           const serviceElement = document.getElementById('currentService');
           if (serviceElement) {{
               const displayName = serviceName.length > 25 ? 
                   serviceName.substring(0, 25) + '...' : serviceName;
               serviceElement.textContent = displayName;
           }}
       }}
       
       function checkEnemyCollisions() {{
           for (let i = enemies.length - 1; i >= 0; i--) {{
               let enemy = enemies[i];
               if (checkCollision(player, enemy)) {{
                   if (player.velocityY > 0 && player.y < enemy.y) {{
                       enemies.splice(i, 1);
                       player.velocityY = -12;
                       gameState.score += 250;
                   }} else {{
                       player.takeDamage();
                   }}
               }}
           }}
       }}
       
       function checkPowerUpCollisions() {{
           for (let powerUp of powerUps) {{
               if (!powerUp.collected && checkCollision(player, powerUp)) {{
                   powerUp.collected = true;
                   if (powerUp.type === 'life') {{
                       gameState.lives++;
                       gameState.score += 500;
                   }} else if (powerUp.type === 'score') {{
                       gameState.score += 1000;
                   }} else if (powerUp.type === 'power') {{
                       gameState.score += 300;
                   }}
               }}
           }}
       }}
       
       function checkCollectibleCollisions() {{
           for (let collectible of collectibles) {{
               if (!collectible.collected && checkCollision(player, collectible)) {{
                   collectible.collected = true;
                   gameState.score += 100;
               }}
           }}
       }}
       
       function update() {{
           if (!gameState.gameRunning) return;
           
           if (!gameState.backgroundMusicStarted && (gameState.keys['ArrowLeft'] || gameState.keys['ArrowRight'] || gameState.keys['ArrowUp'] || gameState.keys[' '])) {{
               playAudio('sonora');
               gameState.backgroundMusicStarted = true;
           }}
           
           player.update();
           
           for (let enemy of enemies) {{
               enemy.update();
           }}
           
           for (let powerUp of powerUps) {{
               powerUp.update();
           }}
           
           for (let collectible of collectibles) {{
               collectible.update();
           }}
           
           checkPlatformCollisions();
           checkEnemyCollisions();
           checkPowerUpCollisions();
           checkCollectibleCollisions();
           
           document.getElementById('score').textContent = gameState.score;
           document.getElementById('lives').textContent = gameState.lives;
           document.getElementById('height').textContent = Math.floor((gameState.worldHeight - player.y) / 15);
       }}
       
       function draw() {{
           let gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
           gradient.addColorStop(0, '#001122');
           gradient.addColorStop(0.3, '#003366');
           gradient.addColorStop(0.7, '#004488');
           gradient.addColorStop(1, '#87CEEB');
           ctx.fillStyle = gradient;
           ctx.fillRect(0, 0, canvas.width, canvas.height);
           
           for (let platform of platforms) {{
               if (platform.y > gameState.camera.y - 150 && platform.y < gameState.camera.y + canvas.height + 150) {{
                   platform.draw();
               }}
           }}
           
           for (let enemy of enemies) {{
               if (enemy.y > gameState.camera.y - 100 && enemy.y < gameState.camera.y + canvas.height + 100) {{
                   enemy.draw();
               }}
           }}
           
           for (let powerUp of powerUps) {{
               if (powerUp.y > gameState.camera.y - 100 && powerUp.y < gameState.camera.y + canvas.height + 100) {{
                   powerUp.draw();
               }}
           }}
           
           for (let collectible of collectibles) {{
               if (collectible.y > gameState.camera.y - 100 && collectible.y < gameState.camera.y + canvas.height + 100) {{
                   collectible.draw();
               }}
           }}
           
           player.draw();
           
           drawProgressIndicator();
       }}
       
       function drawProgressIndicator() {{
           const progressWidth = 200;
           const progressHeight = 20;
           const progressX = canvas.width - progressWidth - 20;
           const progressY = 20;
           
           ctx.fillStyle = 'rgba(0,0,0,0.5)';
           ctx.fillRect(progressX - 5, progressY - 5, progressWidth + 10, progressHeight + 10);
           
           ctx.fillStyle = '#333';
           ctx.fillRect(progressX, progressY, progressWidth, progressHeight);
           
           const progress = gameState.currentPlatform / 234;
           ctx.fillStyle = progress < 0.5 ? '#FF6B35' : progress < 0.8 ? '#FFA502' : '#32CD32';
           ctx.fillRect(progressX, progressY, progressWidth * progress, progressHeight);
           
           ctx.fillStyle = 'white';
           ctx.font = '10px Arial';
           ctx.textAlign = 'center';
           ctx.fillText(`${{gameState.currentPlatform}}/234`, progressX + progressWidth/2, progressY + 14);
       }}
       
       function gameLoop() {{
           update();
           draw();
           requestAnimationFrame(gameLoop);
       }}
       
       function gameOver() {{
           gameState.gameRunning = false;
           
           if (audioElements.sonora) {{
               audioElements.sonora.pause();
               audioElements.sonora.currentTime = 0;
           }}
           
           playAudio('gameover');
           
           document.getElementById('finalScore').textContent = gameState.score;
           document.getElementById('finalHeight').textContent = Math.floor((gameState.worldHeight - player.y) / 15);
           
           let currentServiceName = 'Início da Escalada AWS';
           if (gameState.currentPlatform > 0 && awsServices[gameState.currentPlatform - 1]) {{
               currentServiceName = awsServices[gameState.currentPlatform - 1].name;
           }}
           document.getElementById('finalService').textContent = currentServiceName;
           
           document.getElementById('gameOver').style.display = 'block';
       }}
       
       function gameWin() {{
           gameState.gameRunning = false;
           
           if (audioElements.sonora) {{
               audioElements.sonora.pause();
               audioElements.sonora.currentTime = 0;
           }}
           
           playAudio('aplausos');
           
           document.getElementById('winScore').textContent = gameState.score;
           document.getElementById('gameWin').style.display = 'block';
       }}
       
       function restartGame() {{
           gameState = {{
               score: 0,
               lives: 5,
               currentPlatform: 0,
               gameRunning: true,
               keys: {{}},
               camera: {{ x: 0, y: 0 }},
               worldHeight: 234 * 220,
               backgroundMusicStarted: false
           }};
           player = new Player(150, gameState.worldHeight - 180);
           initLevel();
           updateCurrentServiceUI('Início da Escalada AWS');
           document.getElementById('gameOver').style.display = 'none';
           document.getElementById('gameWin').style.display = 'none';
           
           for (const audio of Object.values(audioElements)) {{
               if (audio) {{
                   audio.pause();
                   audio.currentTime = 0;
               }}
           }}
       }}
       
       document.addEventListener('keydown', (e) => {{
           gameState.keys[e.key] = true;
           if (e.key === ' ' || e.key === 'ArrowUp') e.preventDefault();
       }});
       
       document.addEventListener('keyup', (e) => {{
           gameState.keys[e.key] = false;
       }});
       
       let touchStartX = 0;
       let touchStartY = 0;
       
       canvas.addEventListener('touchstart', (e) => {{
           e.preventDefault();
           const touch = e.touches[0];
           touchStartX = touch.clientX;
           touchStartY = touch.clientY;
       }});
       
       canvas.addEventListener('touchend', (e) => {{
           e.preventDefault();
           const touch = e.changedTouches[0];
           const deltaX = touch.clientX - touchStartX;
           const deltaY = touch.clientY - touchStartY;
           
           if (Math.abs(deltaY) > Math.abs(deltaX)) {{
               if (deltaY < -30) {{
                   if (player.onGround) {{
                       player.velocityY = -player.jumpPower;
                       player.onGround = false;
                       playAudio('pulo');
                   }}
               }}
           }} else {{
               if (Math.abs(deltaX) > 30) {{
                   if (deltaX > 0) {{
                       gameState.keys['ArrowRight'] = true;
                       setTimeout(() => gameState.keys['ArrowRight'] = false, 200);
                   }} else {{
                       gameState.keys['ArrowLeft'] = true;
                       setTimeout(() => gameState.keys['ArrowLeft'] = false, 200);
                   }}
               }}
           }}
       }});
       
       initAudio();
       initLevel();
       updateCurrentServiceUI('Início da Escalada AWS');
       gameLoop();
   </script>
</body>
</html>
'''

# Sidebar com legenda de categorias
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h3 style="color: #333; font-size: 18px;">🎨Categorias & Cores</h3>
        <p style="font-size: 12px; color: #666; margin-bottom: 15px;">📊 Total: 234 serviços AWS</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Criar lista vertical de categorias
    for category in aws_categories:
        color = category_colors.get(category, '#666')
        st.markdown(f"""
        <div style="display: flex; align-items: center; background: rgba(255,255,255,0.9); padding: 6px 10px; border-radius: 20px; border: 2px solid {color}; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 8px;">
            <div style="width: 16px; height: 16px; background: {color}; border-radius: 50%; margin-right: 8px; border: 1px solid rgba(0,0,0,0.2); flex-shrink: 0;"></div>
            <span style="font-size: 11px; font-weight: 600; color: #333; text-align: left;">{category}</span>
        </div>
        """, unsafe_allow_html=True)

# Renderizar o jogo
components.html(game_html, height=650, scrolling=False)

st.markdown("""
<style>
    .main {
        background-color: #ffffff;
        color: #333333;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    /* Esconde completamente todos os elementos da barra padrão do Streamlit */
    header {display: none !important;}
    footer {display: none !important;}
    #MainMenu {display: none !important;}
    /* Remove qualquer espaço em branco adicional */
    div[data-testid="stAppViewBlockContainer"] {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    /* Remove quaisquer margens extras */
    .element-container {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center;">
    <h4>AWS Game: S3 Climbing Adventure</h4>
    🧠Memorize os serviços AWS enquanto escala com o S3! Por <strong>Ary Ribeiro</strong>: <a href="mailto:aryribeiro@gmail.com">aryribeiro@gmail.com</a><br>
    <em>Obs.: o web app foi testado apenas em computador.</em>
</div>
""", unsafe_allow_html=True)