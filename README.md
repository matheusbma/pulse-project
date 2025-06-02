# 🎵 Pulse - Dashboard de Análise Musical

![Pulse Banner](https://via.placeholder.com/800x200/4c0db1/ffffff?text=PULSE+-+Music+Data+Visualization+Dashboard)

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Características Principais](#características-principais)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação e Configuração](#instalação-e-configuração)
- [Como Usar](#como-usar)
- [Funcionalidades por Página](#funcionalidades-por-página)
- [Estrutura dos Dados](#estrutura-dos-dados)
- [Visualizações Implementadas](#visualizações-implementadas)
- [Personalização Visual](#personalização-visual)
- [Contribuição](#contribuição)
- [Licença](#licença)

## 🎯 Sobre o Projeto

O **Pulse** é um dashboard interativo desenvolvido para análise e visualização de dados musicais, criado como projeto acadêmico para o curso de Gestão em Tecnologia da Informação da C.E.S.A.R School. O projeto oferece uma interface intuitiva para explorar informações detalhadas sobre artistas, suas músicas, álbuns, shows e conexões com outros artistas.

### 🎓 Contexto Acadêmico

Este projeto foi desenvolvido com foco em:
- **Análise de dados musicais** utilizando informações do Spotify e Bandsintown
- **Visualização interativa** com gráficos dinâmicos e mapas
- **Interface responsiva** e experiência do usuário otimizada
- **Aplicação prática** de conceitos de ciência de dados

## ✨ Características Principais

- 🎧 **Dashboard Interativo**: Interface moderna e responsiva para exploração de dados musicais
- 📊 **Visualizações Avançadas**: Gráficos dinâmicos, mapas mundiais e análises estatísticas
- 🎵 **Análise Multiperspectiva**: Dados de popularidade, gêneros, shows e conexões entre artistas
- 🗺️ **Mapeamento Global**: Visualização geográfica de turnês e shows
- 🎫 **Integração com Serviços**: Links diretos para Spotify e compra de ingressos
- 🎨 **Design Personalizado**: Tema dark com paleta de cores cuidadosamente selecionada

## 🛠️ Tecnologias Utilizadas

### Core Framework
- **[Streamlit](https://streamlit.io/)** - Framework principal para aplicações web
- **[Python 3.10+](https://python.org/)** - Linguagem de programação

### Manipulação e Análise de Dados
- **[Pandas](https://pandas.pydata.org/)** - Manipulação e análise de dados
- **[NumPy](https://numpy.org/)** - Computação científica

### Visualização
- **[Plotly](https://plotly.com/python/)** - Gráficos interativos
- **[Plotly Express](https://plotly.com/python/plotly-express/)** - Visualizações rápidas e eficientes

### Dados
- **CSV Files** - Armazenamento de dados estruturados
- **APIs Integration** - Spotify e Bandsintown (via dados pré-processados)

## 📁 Estrutura do Projeto

```
pulse-project/
│
├── streamlit_app.py              # Arquivo principal da aplicação
├── config.py                     # Configurações globais e tema
├── README.md                     # Documentação do projeto
├── requirements.txt              # Dependências do projeto
│
├── data/                         # Dados em formato CSV
│   ├── artists.csv              # Informações dos artistas
│   ├── tracks.csv               # Dados das músicas
│   ├── albums.csv               # Informações dos álbuns
│   ├── past_events.csv          # Shows realizados
│   ├── future_events.csv        # Shows futuros
│   └── related_artists.csv      # Artistas relacionados
│
└── views/                        # Páginas da aplicação
    ├── home.py                  # Página inicial
    ├── general.py               # Visão geral do artista
    ├── tracks.py                # Análise de músicas
    ├── albums.py                # Análise de álbuns
    ├── shows.py                 # Análise de shows e turnês
    └── related_artists.py       # Rede de artistas relacionados
```

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional, para clonagem do repositório)

### Passos para Instalação

1. **Clone o repositório**:
```bash
git clone https://github.com/matheusbma/pulse-project.git
cd pulse-project
```

2. **Crie um ambiente virtual** (recomendado):
```bash
python -m venv pulse
source pulse/bin/activate  # No Windows: pulse\Scripts\activate
```

3. **Instale as dependências**:
```bash
pip install streamlit pandas plotly
```

4. **Execute a aplicação**:
```bash
streamlit run streamlit_app.py
```

5. **Acesse no navegador**:
```
Local URL: http://localhost:8501
```

### Dependências Principais

```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
```

## 📖 Como Usar

### Navegação Básica

1. **Seleção de Artista**: Use a barra lateral para escolher o artista desejado
2. **Navegação entre Páginas**: Utilize o menu lateral para alternar entre diferentes análises
3. **Interação com Gráficos**: Clique, zoom e hover nos gráficos para explorar dados
4. **Links Externos**: Acesse Spotify ou compre ingressos através dos links disponíveis

### Estado da Sessão

O dashboard mantém o artista selecionado consistente entre todas as páginas, proporcionando uma experiência fluida de navegação.

## 🔍 Funcionalidades por Página

### 🏠 **Home** (`views/home.py`)
- Página de boas-vindas
- Introdução ao projeto
- Guia de navegação

### 📊 **Geral** (`views/general.py`)
- Informações básicas do artista
- Métricas do Spotify (popularidade, seguidores)
- Próximos shows com links para ingressos
- Histórico de shows realizados

### 🎵 **Músicas** (`views/tracks.py`)
- Top 10 músicas mais populares
- Distribuição de popularidade
- Análise por categorias de sucesso
- Estatísticas detalhadas

### 💿 **Álbuns** (`views/albums.py`)
- Timeline de lançamentos
- Análise por tipo de álbum
- Evolução do número de faixas
- Heatmap de produtividade por década

### 🎭 **Shows** (`views/shows.py`)
- Mapa mundial interativo
- Distribuição geográfica (países/cidades)
- Timeline de apresentações
- Análise de turnês

### 👥 **Artistas Relacionados** (`views/related_artists.py`)
- Comparação de popularidade
- Análise de gêneros musicais
- Categorização por popularidade
- Rede de conexões entre artistas

## 💾 Estrutura dos Dados

### `artists.csv`
```csv
spotify_id, artist_name, popularity, followers, genres, country, artist_type, gender, image_url, spotify_url
```

### `tracks.csv`
```csv
track_id, spotify_id, track_name, popularity
```

### `albums.csv`
```csv
album_id, spotify_id, album_name, release_date, type, total_tracks
```

### `past_events.csv` / `future_events.csv`
```csv
event_id, spotify_id, artist_name, event_date, venue_name, venue_city, venue_country, event_url, ticket_url, ticket_status
```

### `related_artists.csv`
```csv
spotify_id, related_artist_name, related_artist_popularity, related_artist_genres, followers
```

## 📈 Visualizações Implementadas

### Tipos de Gráficos
- **Gráficos de Barras**: Horizontais e verticais para rankings e comparações
- **Histogramas**: Distribuições de popularidade e análises estatísticas
- **Mapas Interativos**: Geolocalização mundial de shows
- **Box Plots**: Análises estatísticas detalhadas
- **Scatter Plots**: Correlações entre variáveis
- **Heatmaps**: Padrões temporais e categóricos
- **Timelines**: Evolução temporal de dados

### Paleta de Cores
```python
COLORS = {
    'primary': '#4c0db1',      # Roxo principal
    'secondary': '#7900ff',    # Roxo secundário
    'accent': '#cb88ff',       # Roxo claro/accent
    'highlight': '#00c4cc',    # Turquesa
    'accent2': '#e43397',      # Rosa/magenta
}
```

## 🎨 Personalização Visual

### Tema Dark
- Interface dark mode para melhor experiência visual
- Contraste otimizado para leitura
- Elementos visuais consistentes

### Gradientes de Cores
- **Baixo → Alto**: Turquesa → Roxo → Rosa
- Escalas contínuas para representação intuitiva de dados
- Consistência visual em todos os gráficos

### Layout Responsivo
- Colunas adaptáveis para diferentes tamanhos de tela
- Imagens otimizadas (100x100px para fotos de artistas)
- Espaçamento consistente entre elementos

## 🤝 Contribuição

### Como Contribuir

1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add: Amazing Feature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

### Áreas para Contribuição

- 📊 Novas visualizações e análises
- 🎨 Melhorias na interface e UX
- 📱 Responsividade mobile
- 🔗 Integração com mais fontes de dados
- 🌐 Internacionalização
- ⚡ Otimizações de performance

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Desenvolvimento

**Desenvolvido por**: [Matheus](https://github.com/matheusbma)

**Projeto Acadêmico**: Curso de Análise e Visualização de Dados

---

### 🔗 Links Úteis

- [Documentação do Streamlit](https://docs.streamlit.io/)
- [Plotly Python Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### 📞 Suporte

Para dúvidas, sugestões ou reportar problemas:
- Abra uma [Issue](https://github.com/matheusbma/pulse-project/issues)
- Entre em contato através do GitHub

---

<div align="center">

**🎵 Pulse Dashboard - Explorando o universo musical através de dados 🎵**

[![Made with Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-red)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.15+-green)](https://plotly.com/)

</div> 