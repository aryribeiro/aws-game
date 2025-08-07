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

# Título e descrição
st.title("☁️ AWS Game 🎮")

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
            all_services.append({
                'name': service['name'],
                'description': service.get('description', ''),
                'category': service.get('category', 'AWS')
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

# Carregar recursos
aws_services = load_aws_services()
mascot_base64 = load_image_as_base64('static/mascote.png')
aplausos_base64 = load_audio_as_base64('static/aplausos.mp3')
pulo_base64 = load_audio_as_base64('static/pulo.mp3')
gameover_base64 = load_audio_as_base64('static/gameover.mp3')
sonora_base64 = load_audio_as_base64('static/sonora.mp3')

if not aws_services:
    st.stop()

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
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
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
        <canvas id="gameCanvas" width="700" height="650" style="width: 100%; height: 100%;"></canvas>
        
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
                    // Category-based colors
                    switch(this.serviceCategory) {{
                        case 'AWS':
                            color = '#32CD32';
                            borderColor = '#228B22';
                            break;
                        case 'S3 Services':
                            color = '#FF6B35';
                            borderColor = '#CC4A1F';
                            break;
                        case 'Compute':
                            color = '#4ECDC4';
                            borderColor = '#3BA39C';
                            break;
                        case 'Database':
                            color = '#FF4757';
                            borderColor = '#E63946';
                            break;
                        case 'Storage':
                            color = '#5F27CD';
                            borderColor = '#4C1FA3';
                            break;
                        case 'Network':
                            color = '#00D2D3';
                            borderColor = '#00A8A9';
                            break;
                        case 'Security':
                            color = '#54A0FF';
                            borderColor = '#2F80CC';
                            break;
                        case 'Analytics':
                            color = '#FFA502';
                            borderColor = '#CC7A00';
                            break;
                        case 'Machine Learning':
                            color = '#A4B0BE';
                            borderColor = '#747D8C';
                            break;
                        default:
                            color = '#228B22';
                            borderColor = '#1F5F1F';
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
                let y = gameState.worldHeight - (i * 220); // Espaçamento aumentado
                let width = 200 + Math.random() * 80; // Plataformas maiores (200-280px)
                
                // Special platforms
                let type = 'normal';
                if (i % 25 === 0 && i < 234) type = 'breakable';
                if (i % 35 === 0 && i < 234) type = 'moving';
                
                platforms.push(new Platform(x, y, width, 30, i, type)); // Altura aumentada para 30px
                
                // Add enemies (less frequent to give more space)
                if (i > 5 && Math.random() < 0.25) {{
                    let enemyEmojis = ['🐓', '🐖', '🦨', '🐀', '🐃', '🦆', '🦑', '💩'];
                    let emoji = enemyEmojis[Math.floor(Math.random() * enemyEmojis.length)];
                    enemies.push(new Enemy(x + 30, y - 35, emoji));
                }}
                
                // Add power-ups
                if (Math.random() < 0.12) {{
                    let types = ['life', 'score', 'power'];
                    let type = types[Math.floor(Math.random() * types.length)];
                    powerUps.push(new PowerUp(x + width/2, y - 35, type));
                }}
                
                // Add collectibles
                if (Math.random() < 0.35) {{
                    collectibles.push(new Collectible(x + Math.random() * (width - 40) + 20, y - 30));
                }}
            }}
            
            // Set player at ground level
            player.x = 150;
            player.y = gameState.worldHeight - 180;
            player.lastGroundY = gameState.worldHeight - 60;
        }}
        
        // Collision Detection
        function checkCollision(rect1, rect2) {{
            return rect1.x < rect2.x + rect2.width &&
                   rect1.x + rect1.width > rect2.x &&
                   rect1.y < rect2.y + rect2.height &&
                   rect1.y + rect1.height > rect2.y;
        }}
        
        // Platform Collision
        function checkPlatformCollisions() {{
            for (let platform of platforms) {{
                if (checkCollision(player, platform)) {{
                    // Top collision (landing on platform)
                    if (player.velocityY > 0 && player.y < platform.y) {{
                        player.y = platform.y - player.height;
                        player.velocityY = 0;
                        player.setOnGround(platform.y);
                        
                        // Update current platform
                        if (platform.number > gameState.currentPlatform) {{
                            gameState.currentPlatform = platform.number;
                            gameState.score += 75; // Increased score for reaching new service
                            
                            // Update UI with current service name
                            updateCurrentServiceUI(platform.serviceName);
                            
                            // Check for victory
                            if (platform.number === 234) {{
                                gameWin();
                                return;
                            }}
                        }}
                        
                        // Break breakable platforms
                        if (platform.type === 'breakable' && !platform.visited) {{
                            platform.visited = true;
                            setTimeout(() => {{
                                let index = platforms.indexOf(platform);
                                if (index > -1) platforms.splice(index, 1);
                            }}, 1500); // More time before breaking
                            gameState.score += 150;
                        }}
                    }}
                }}
            }}
        }}
        
        // Update Current Service UI
        function updateCurrentServiceUI(serviceName) {{
            const serviceElement = document.getElementById('currentService');
            if (serviceElement) {{
                // Truncate long service names for UI
                const displayName = serviceName.length > 25 ? 
                    serviceName.substring(0, 25) + '...' : serviceName;
                serviceElement.textContent = displayName;
            }}
        }}
        
        // Enemy Collision
        function checkEnemyCollisions() {{
            for (let i = enemies.length - 1; i >= 0; i--) {{
                let enemy = enemies[i];
                if (checkCollision(player, enemy)) {{
                    // Jump on enemy (defeat)
                    if (player.velocityY > 0 && player.y < enemy.y) {{
                        enemies.splice(i, 1);
                        player.velocityY = -12; // Bigger bounce
                        gameState.score += 250;
                    }} else {{
                        // Take damage
                        player.takeDamage();
                    }}
                }}
            }}
        }}
        
        // Power-up Collision
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
                        // Could add temporary power-up effects here
                    }}
                }}
            }}
        }}
        
        // Collectible Collision
        function checkCollectibleCollisions() {{
            for (let collectible of collectibles) {{
                if (!collectible.collected && checkCollision(player, collectible)) {{
                    collectible.collected = true;
                    gameState.score += 100;
                }}
            }}
        }}
        
        // Update Game
        function update() {{
            if (!gameState.gameRunning) return;
            
            // Start background music on first movement
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
            
            // Update UI
            document.getElementById('score').textContent = gameState.score;
            document.getElementById('lives').textContent = gameState.lives;
            document.getElementById('height').textContent = Math.floor((gameState.worldHeight - player.y) / 15);
        }}
        
        // Draw Game
        function draw() {{
            // Clear canvas with gradient background
            let gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            gradient.addColorStop(0, '#001122');
            gradient.addColorStop(0.3, '#003366');
            gradient.addColorStop(0.7, '#004488');
            gradient.addColorStop(1, '#87CEEB');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw platforms
            for (let platform of platforms) {{
                // Only draw platforms that are visible (with some margin)
                if (platform.y > gameState.camera.y - 150 && platform.y < gameState.camera.y + canvas.height + 150) {{
                    platform.draw();
                }}
            }}
            
            // Draw enemies
            for (let enemy of enemies) {{
                if (enemy.y > gameState.camera.y - 100 && enemy.y < gameState.camera.y + canvas.height + 100) {{
                    enemy.draw();
                }}
            }}
            
            // Draw power-ups
            for (let powerUp of powerUps) {{
                if (powerUp.y > gameState.camera.y - 100 && powerUp.y < gameState.camera.y + canvas.height + 100) {{
                    powerUp.draw();
                }}
            }}
            
            // Draw collectibles
            for (let collectible of collectibles) {{
                if (collectible.y > gameState.camera.y - 100 && collectible.y < gameState.camera.y + canvas.height + 100) {{
                    collectible.draw();
                }}
            }}
            
            // Draw player
            player.draw();
            
            // Draw progress indicator
            drawProgressIndicator();
        }}
        
        // Draw Progress Indicator
        function drawProgressIndicator() {{
            const progressWidth = 200;
            const progressHeight = 20;
            const progressX = canvas.width - progressWidth - 20;
            const progressY = 20;
            
            // Background
            ctx.fillStyle = 'rgba(0,0,0,0.5)';
            ctx.fillRect(progressX - 5, progressY - 5, progressWidth + 10, progressHeight + 10);
            
            // Progress bar background
            ctx.fillStyle = '#333';
            ctx.fillRect(progressX, progressY, progressWidth, progressHeight);
            
            // Progress bar fill
            const progress = gameState.currentPlatform / 234;
            ctx.fillStyle = progress < 0.5 ? '#FF6B35' : progress < 0.8 ? '#FFA502' : '#32CD32';
            ctx.fillRect(progressX, progressY, progressWidth * progress, progressHeight);
            
            // Progress text
            ctx.fillStyle = 'white';
            ctx.font = '10px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(`${{gameState.currentPlatform}}/234`, progressX + progressWidth/2, progressY + 14);
        }}
        
        // Game Loop
        function gameLoop() {{
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }}
        
        // Game Over
        function gameOver() {{
            gameState.gameRunning = false;
            
            // Stop background music
            if (audioElements.sonora) {{
                audioElements.sonora.pause();
                audioElements.sonora.currentTime = 0;
            }}
            
            // Play game over sound
            playAudio('gameover');
            
            document.getElementById('finalScore').textContent = gameState.score;
            document.getElementById('finalHeight').textContent = Math.floor((gameState.worldHeight - player.y) / 15);
            
            // Get current service name
            let currentServiceName = 'Início da Escalada AWS';
            if (gameState.currentPlatform > 0 && awsServices[gameState.currentPlatform - 1]) {{
                currentServiceName = awsServices[gameState.currentPlatform - 1].name;
            }}
            document.getElementById('finalService').textContent = currentServiceName;
            
            document.getElementById('gameOver').style.display = 'block';
        }}
        
        // Game Win
        function gameWin() {{
            gameState.gameRunning = false;
            
            // Stop background music
            if (audioElements.sonora) {{
                audioElements.sonora.pause();
                audioElements.sonora.currentTime = 0;
            }}
            
            // Play victory sound
            playAudio('aplausos');
            
            document.getElementById('winScore').textContent = gameState.score;
            document.getElementById('gameWin').style.display = 'block';
        }}
        
        // Restart Game
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
            
            // Stop all audio
            for (const audio of Object.values(audioElements)) {{
                if (audio) {{
                    audio.pause();
                    audio.currentTime = 0;
                }}
            }}
        }}
        
        // Event Listeners
        document.addEventListener('keydown', (e) => {{
            gameState.keys[e.key] = true;
            if (e.key === ' ' || e.key === 'ArrowUp') e.preventDefault();
        }});
        
        document.addEventListener('keyup', (e) => {{
            gameState.keys[e.key] = false;
        }});
        
        // Touch controls for mobile
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
                    // Swipe up - jump
                    if (player.onGround) {{
                        player.velocityY = -player.jumpPower;
                        player.onGround = false;
                        playAudio('pulo');
                    }}
                }}
            }} else {{
                if (Math.abs(deltaX) > 30) {{
                    // Horizontal movement
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
        
        // Initialize and Start Game
        initAudio();
        initLevel();
        updateCurrentServiceUI('Início da Escalada AWS');
        gameLoop();
    </script>
</body>
</html>
'''

# Exibir informações sobre o jogo
st.markdown("#### ... S3 Climbing Adventure")

# Verificar arquivo
if not os.path.exists('servicos.json'):
    st.error("⚠️ Arquivo 'servicos.json' não encontrado na raiz do projeto!")
    st.info("📁 Certifique-se de que o arquivo está no mesmo diretório que app.py")
else:
    st.success("✅ Arquivo 'servicos.json' carregado com sucesso!")
    st.info(f"📊 Total de serviços: {len(aws_services)}")

# Verificar mascote
if mascot_base64:
    st.success("✅ Mascote carregado como personagem principal!")
else:
    st.warning("⚠️ Arquivo 'static/mascote.png' não encontrado - usando sprite fallback")

# Verificar áudios
audio_status = []
audio_files = ['aplausos.mp3', 'pulo.mp3', 'gameover.mp3', 'sonora.mp3']
for audio_file in audio_files:
    if eval(f"{audio_file.split('.')[0]}_base64"):
        audio_status.append(f"✅ {audio_file}")
    else:
        audio_status.append(f"⚠️ {audio_file} não encontrado")

st.info("🔊 Status dos áudios:")
for status in audio_status:
    st.write(status)

# Renderizar o jogo
components.html(game_html, height=min(650, int(0.85 * 800)), scrolling=False)