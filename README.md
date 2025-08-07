Obs.: caso o app esteja no modo "sleeping" (dormindo) ao entrar, basta clicar no botão que estará disponível e aguardar, para ativar o mesmo.
<p align="center">
  <img src="https://github.com/user-attachments/assets/00ad39c9-d15c-49c9-89fa-1a598d89e0ee" alt="mascote" width="150" height="212">
</p>
# ☁️ AWS Game 🎮 - S3 Climbing Adventure

Um jogo de plataforma interativo onde você escala através de 234 serviços AWS diferentes! Teste seus conhecimentos sobre os serviços da Amazon Web Services enquanto se diverte em uma aventura de escalada.

## 🎯 Sobre o Web Game

**AWS Game - S3 Climbing Adventure** é um jogo de plataforma 2D desenvolvido em Python com Streamlit por Ary Ribeiro, onde o jogador controla o mascote S3, que deve escalar plataformas representando diferentes serviços AWS. O objetivo é alcançar o topo, passando por todos os 234 serviços disponíveis até o momento.

### 🌟 Características

- **234 Plataformas Únicas**: Cada plataforma representa um serviço AWS real
- **Mascote Personalizável**: Use sua própria imagem como personagem principal
- **Sistema de Pontuação**: Ganhe pontos explorando novos serviços AWS
- **Efeitos Sonoros**: Áudios imersivos para pulos, vitória e game over
- **Controles Intuitivos**: Suporte para teclado e touch (mobile)
- **Inimigos e Power-ups**: Elementos de gameplay que tornam a experiência mais desafiadora
- **Sistema de Vidas**: 5 vidas para completar a jornada
- **Indicador de Progresso**: Acompanhe seu avanço através dos serviços AWS

## 🚀 Como Jogar

### Controles do Teclado
- **Setas Esquerda/Direita**: Mover o personagem
- **Seta para Cima ou Espaço**: Pular
- **Movimento Horizontal**: Atravessar as bordas da tela para aparecer do outro lado

### Controles Touch (Mobile)
- **Deslizar para Cima**: Pular
- **Deslizar Esquerda/Direita**: Mover o personagem

### Objetivos
1. Escale através das plataformas dos serviços AWS
2. Evite ou derrote os inimigos
3. Colete power-ups e moedas para aumentar sua pontuação
4. Alcance a plataforma 234 para vencer o jogo!

## 📋 Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)

## 🛠️ Instalação

1. **Clone ou baixe o repositório**
```bash
git clone <url-do-repositorio>
cd aws-game
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Prepare os arquivos necessários**

   Certifique-se de ter os seguintes arquivos na estrutura correta:

   ```
   aws-game/
   ├── app.py
   ├── servicos.json
   ├── requirements.txt
   ├── README.md
   └── static/
       ├── mascote.png
       ├── aplausos.mp3
       ├── pulo.mp3
       ├── gameover.mp3
       └── sonora.mp3
   ```

## 📁 Estrutura de Arquivos

### Arquivos Obrigatórios
- **`app.py`**: Arquivo principal da aplicação Streamlit
- **`servicos.json`**: Dados dos serviços AWS (deve conter array de nodes com name, description, category)

### Arquivos Opcionais (Static)
- **`static/mascote.png`**: Imagem do mascote (personagem principal)
- **`static/aplausos.mp3`**: Som de vitória
- **`static/pulo.mp3`**: Som de pulo
- **`static/gameover.mp3`**: Som de game over
- **`static/sonora.mp3`**: Música de fundo

> **Nota**: Os arquivos da pasta `static/` são opcionais. O jogo funcionará mesmo sem eles, usando fallbacks visuais e sem áudio.

## ▶️ Executando o Jogo

1. **Inicie a aplicação Streamlit**
```bash
streamlit run app.py
```

2. **Acesse o jogo**
   - O Streamlit abrirá automaticamente seu navegador
   - Ou acesse manualmente: `http://localhost:8501`

3. **Comece a jogar!**
   - Use as setas do teclado ou gestos touch para controlar o mascote
   - Escale através dos serviços AWS e divirta-se!

## 🎨 Personalização

### Adicionando seu Próprio Mascote
1. Substitua o arquivo `static/mascote.png` pela sua imagem
2. Recomendado: imagem 40x50 pixels, formato PNG com fundo transparente

### Personalizando Áudios
1. Substitua os arquivos MP3 na pasta `static/` pelos seus próprios áudios
2. Mantenha os mesmos nomes de arquivo

### Modificando Serviços AWS
1. Edite o arquivo `servicos.json`
2. Estrutura esperada:
```json
{
  "nodes": [
    {
      "name": "Nome do Serviço",
      "category": "Categoria",
      "description": "Descrição do serviço",      
      "isCentral": false
    }
  ]
}
```

## 🎮 Mecânicas do Jogo

### Sistema de Pontuação
- **75 pontos**: Por alcançar uma nova plataforma/serviço
- **100 pontos**: Por coletar moedas
- **150 pontos**: Por quebrar plataformas especiais
- **250 pontos**: Por derrotar inimigos
- **300-1000 pontos**: Por power-ups especiais

### Tipos de Plataformas
- **Normais**: Plataformas padrão coloridas por categoria
- **Quebráveis**: Desaparecem após alguns segundos (a cada 25 níveis)
- **Móveis**: Plataformas em movimento (a cada 35 níveis)
- **Final**: Plataforma dourada especial (nível 234)

### Power-ups Disponíveis
- **💖 Vida Extra**: Adiciona uma vida
- **⭐ Pontos Bônus**: 1000 pontos extras
- **🍄 Power**: 300 pontos e efeitos especiais

## 🐛 Solução de Problemas

### Jogo não carrega
- Verifique se o arquivo `servicos.json` existe na raiz do projeto
- Confirme que a estrutura JSON está correta

### Sem áudio
- Verifique se os arquivos MP3 estão na pasta `static/`
- O jogo funcionará normalmente sem áudio

### Mascote não aparece
- Verifique se `static/mascote.png` existe
- O jogo usará um sprite simples como fallback

### Erro de porta em uso
```bash
streamlit run app.py --server.port 8502
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🎯 Roadmap

### Próximas Features
- [ ] Sistema de high scores local
- [ ] Mais tipos de power-ups
- [ ] Novos tipos de inimigos
- [ ] Modo multiplayer local
- [ ] Exportação de estatísticas
- [ ] Aumento dos serviços AWS

---

Se encontrar problemas ou tiver sugestões:

** Ary Ribeiro - aryribeiro@gmail.com







