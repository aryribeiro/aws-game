Obs.: caso o app esteja no modo "sleeping" (dormindo) ao entrar, basta clicar no botão que estará disponível e aguardar, para ativar o mesmo.
<p align="center">
  <img src="https://github.com/user-attachments/assets/00ad39c9-d15c-49c9-89fa-1a598d89e0ee" alt="mascote" width="150" height="212">
</p>

# ☁️ AWS Game - S3 Climbing Adventure 🎮

Um jogo de plataforma interativo onde você escala através de **374 serviços AWS**! Teste seus conhecimentos sobre os serviços da Amazon Web Services enquanto se diverte em uma aventura de escalada.

## 🎯 Sobre o Jogo

**AWS Game - S3 Climbing Adventure** é um jogo de plataforma 2D desenvolvido em Python com Streamlit por Ary Ribeiro, onde o jogador controla o mascote S3, que deve escalar plataformas representando diferentes serviços AWS. O objetivo é alcançar o topo, passando por todos os serviços disponíveis até o momento.

O número de plataformas é derivado do `servicos.json` em tempo de execução — não há contagem fixa no código.

### 🌟 Características

- **Uma plataforma por serviço AWS**, colorida pela categoria do serviço
- **Card de descrição**: ao pisar numa plataforma, a descrição oficial daquele serviço AWS aparece no card logo abaixo do jogo. Descer para uma plataforma anterior traz a descrição dela de volta — o card segue onde o personagem **está**, não a altura máxima alcançada.
- **Física independente da taxa de quadros**: o jogo simula 60 ticks/s em qualquer monitor (60, 120 ou 165Hz)
- **Mascote personalizável**: use sua própria imagem como personagem principal
- **Sistema de pontuação**: ganhe pontos explorando novos serviços AWS
- **Efeitos sonoros**: áudios para pulo, vitória e game over, além de música de fundo
- **Controles**: teclado e touch
- **Inimigos, power-ups e moedas**
- **Sistema de vidas**: 5 vidas para completar a jornada
- **Indicador de progresso**: acompanhe seu avanço através dos serviços AWS

## 🚀 Como Jogar

Clique em **▶ Jogar** para começar — o clique também dá foco ao jogo (ele roda dentro de um iframe) e libera o áudio no navegador.

### Controles do Teclado
- **Setas Esquerda/Direita**: mover o personagem
- **Seta para Cima ou Espaço**: pular
- **Bordas da tela**: atravesse para aparecer do outro lado

### Controles Touch (Mobile)
- **Deslizar para cima**: pular
- **Deslizar esquerda/direita**: mover o personagem

### Objetivos
1. Escale através das plataformas dos serviços AWS
2. Evite ou derrote os inimigos (pule em cima deles)
3. Colete power-ups e moedas para aumentar sua pontuação
4. Alcance a última plataforma para vencer o jogo

## 📋 Pré-requisitos

- Python 3.9 ou superior
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

3. **Estrutura esperada**

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

### Obrigatórios
- **`app.py`**: aplicação Streamlit (o jogo inteiro é gerado a partir daqui)
- **`servicos.json`**: dados dos serviços AWS

### Opcionais (Static)
- **`static/mascote.png`**: imagem do mascote
- **`static/aplausos.mp3`**: som de vitória
- **`static/pulo.mp3`**: som de pulo
- **`static/gameover.mp3`**: som de game over
- **`static/sonora.mp3`**: música de fundo

> **Nota**: os arquivos de `static/` são opcionais. O jogo funciona sem eles, com um sprite simples como fallback e sem áudio.

## ▶️ Executando o Jogo

```bash
streamlit run app.py
```

Acesse `http://localhost:8501`.

## 🎨 Personalização

### Mascote
Substitua `static/mascote.png`. Recomendado: PNG com fundo transparente, proporção próxima de 40×50.

### Áudios
Substitua os MP3 em `static/`, mantendo os mesmos nomes.

> Os assets são embutidos no HTML como base64, e o Streamlit Cloud não serve arquivos estáticos de forma confiável — por isso o base64. O áudio já foi encodado para bitrates adequados a um jogo de navegador (trilha em loop a 64 kbps mono, efeitos a 96 kbps): **790 KB no total**, contra 1997 KB dos arquivos originais. O HTML gerado tem **1,3 MB**. Se você substituir os MP3, mantenha bitrates nessa faixa — subir para 256 kbps devolve o peso de volta.

### Serviços AWS
Edite `servicos.json`. Schema real (atenção à caixa das chaves):

```json
{
  "nodes": [
    {
      "name": "Amazon MQ",
      "Category": "App-Integration",
      "Description": "serviço de agente de mensagens gerenciado..."
    }
  ]
}
```

- `name` é obrigatório; entradas sem nome ou com nome repetido são descartadas.
- `Category` usa o **slug oficial da AWS 2026** (`App-Integration`, `Networking-Content-Delivery`, `Artificial-Intelligence`…). São 24 categorias, definidas em `CATEGORY_COLORS` no `app.py`; o rótulo em português da legenda vem de `CATEGORY_LABELS`. Categoria fora dessa lista cai num cinza de fallback.
- A **ordem das entradas define a ordem da escalada**. O dataset atual está embaralhado de propósito, para que plataformas vizinhas não tenham a mesma cor.
- A legenda da sidebar é gerada a partir dos dados, então basta editar o JSON.

> ⚠️ **A descrição tem um teto.** O card abaixo do jogo tem **altura fixa** (`CARD_HEIGHT`, no `app.py`) com `overflow: hidden` — a altura é fixa de propósito, senão o layout pularia a cada plataforma. Uma descrição maior que a maior atual (**560 caracteres**, a da VPC) é **cortada em silêncio**, sem erro nenhum. Ao adicionar descrições longas, aumente o `CARD_HEIGHT` junto.

> O `@st.cache_data` guarda o dataset em memória. Ao trocar o `servicos.json` **localmente**, reinicie o Streamlit — um simples reload do navegador continua servindo o dataset antigo. No Streamlit Cloud isso não é problema: o push reinicia o app.

### Barra de status (mobile) e barra de rolagem
Ambas são azul-marinho (`NAVY`, no `app.py`) — o mesmo tom do degradê do jogo.

O `<meta name="theme-color">` **não funciona via `st.markdown` sozinho**: o Streamlit renderiza o markdown dentro de um contêiner, e o navegador móvel só lê essa meta no `<head>` do documento de topo. Por isso um `components.html(..., height=0)` injeta a meta no `parent` e no `top` document, e é ele também que injeta o CSS da barra de rolagem no `<head>` da página. O CSS traz as duas sintaxes — `::-webkit-scrollbar` (Chrome, Edge, Safari, Android) e `scrollbar-color`/`scrollbar-width` (Firefox e padrão CSS) — cobrindo desktop e móvel.

> Esse iframe de altura 0 **reserva espaço** se você não escondê-lo. O CSS já traz a regra (`iframe[height="0"] { display: none }`); removê-la abre um vão no topo da página.

### Cache
Duas coisas ficam em memória por 8 horas (`CACHE_TTL`): o dataset parseado (`load_aws_services`) e o HTML do jogo já montado (`build_game_html`).

O `build_game_html()` **não recebe argumentos de propósito**. O `@st.cache_data` hasheia todos os argumentos para montar a chave do cache — e passar o ~1 MB de base64 dos assets ali custava 23 ms por chamada, contra 7 ms para simplesmente remontar o HTML do zero. O cache ficava **mais lento que não ter cache**. Sem argumentos, a chave é trivial e o acerto sai por ~2 ms.

Pelo mesmo motivo o `load_asset_b64()` **não** é cacheado: só o `build_game_html()` o chama, e ele já é cacheado — então roda uma vez a cada 8 horas. Cacheá-lo duplicaria ~1 MB na memória, já que os mesmos bytes vivem dentro do HTML cacheado.

> O cache economiza **CPU do servidor**. Ele **não** reduz o que trafega até o navegador: o HTML vai pela rede em toda carga de página, com ou sem cache.

### Como o dataset foi construído
A pasta [`curadoria/`](curadoria/) guarda o rastro completo: o catálogo oficial da AWS baixado, o texto-fonte de cada descrição e as listas de decisão. As descrições vêm do console de gerenciamento da AWS e da documentação oficial (`docs.aws.amazon.com`) — nenhuma foi inventada.

## 🎮 Mecânicas do Jogo

### Pontuação
- **75 pontos**: alcançar uma nova plataforma/serviço
- **100 pontos**: coletar uma moeda
- **150 pontos**: pisar numa plataforma quebrável
- **250 pontos**: derrotar um inimigo
- **300 / 500 / 1000 pontos**: power-ups

### Tipos de Plataformas
- **Chão** (preta): a plataforma inicial, "Início da Escalada AWS"
- **Normais**: coloridas pela categoria do serviço
- **Quebráveis** (marrom): somem 1,5s depois que você pisa — a cada 25 níveis
- **Móveis** (azul): deslizam na horizontal e carregam o jogador junto — a cada 35 níveis
- **Final** (dourada): a última plataforma, marcada com "FINAL!"

### Power-ups
- **💖 Vida Extra**: +1 vida e 500 pontos
- **⭐ Pontos Bônus**: 1000 pontos
- **🍄 Cogumelo**: 300 pontos

## 🐛 Solução de Problemas

### O jogo não responde ao teclado
Clique dentro da área do jogo. Ele roda num iframe e precisa de foco — o botão **▶ Jogar** faz isso automaticamente.

### Sem áudio
O navegador só libera áudio após uma interação. Comece pelo botão **▶ Jogar**. Se ainda assim não houver som, confira se os MP3 estão em `static/`.

### O jogo não carrega
Verifique se `servicos.json` existe na raiz e se o JSON é válido.

### Erro de porta em uso
```bash
streamlit run app.py --server.port 8502
```

## 🎯 Roadmap

- [x] Curadoria do dataset: unificado com a lista oficial 2026, categorias oficiais da AWS, descontinuados removidos e 100% das descrições buscadas na fonte oficial
- [x] Exibir a descrição do serviço da plataforma atual na UI (card abaixo do jogo)
- [x] Reduzir o peso da página reencodando o áudio (2,89 MB → 1,32 MB)
- [ ] Sistema de high scores local
- [ ] Mais tipos de power-ups e inimigos
- [ ] Confirmar os nomes de `Amazon Q in QuickSight` e `QuickSight Paginated Reports` sob o Amazon Quick Suite — seguem com o nome antigo no dataset

---

Por **Ary Ribeiro** — [linkedin.com/in/aryribeiro](https://linkedin.com/in/aryribeiro)
