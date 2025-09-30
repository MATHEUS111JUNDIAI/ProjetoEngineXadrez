[![Status do Projeto](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)](https://github.com/MATHEUS111JUNDIAI/ProjetoEngineXadrez)

# Engine de Análise de Xadrez em Python

## 📖 Descrição

Este projeto é uma Inteligência Artificial Clássica para jogar e analisar partidas de xadrez, desenvolvida inteiramente em Python. O sistema é capaz de:
- Jogar uma partida completa contra um oponente humano.
- Analisar partidas existentes a partir do formato padrão PGN (Portable Game Notation).
- Avaliar a qualidade de uma posição com base em heurísticas de material e posicionamento.
- Gerar visualizações de dados, como gráficos de vantagem, para facilitar a compreensão da dinâmica do jogo.

O núcleo do engine é um algoritmo de busca Minimax otimizado com a técnica de Poda Alfa-Beta.

## ✨ Funcionalidades Principais

* **Jogo Interativo:** Execute `play.py` para jogar uma partida completa contra o engine diretamente no terminal.
* **Análise de Partidas:** Execute `main.py` para carregar uma partida de um arquivo `partida.pgn`, analisar cada lance e gerar um relatório visual.
* **Visualização de Dados:** Para cada análise, o programa gera uma barra de vantagem textual no console e salva um gráfico completo da avaliação da partida como uma imagem (`.png`).

## 🛠️ Tecnologias Utilizadas

* **Python 3:** Linguagem principal do projeto.
* **python-chess:** Biblioteca utilizada para a representação do tabuleiro, geração de movimentos legais e manipulação de arquivos PGN.
* **NumPy:** Utilizada para cálculos numéricos eficientes na geração do gráfico de avaliação.
* **Matplotlib:** Utilizada para a plotagem e visualização do gráfico de avaliação da partida.

## 📂 Estrutura do Projeto

O código foi refatorado em múltiplos módulos para seguir as boas práticas de engenharia de software, promovendo organização, reutilização e manutenibilidade.

```
/
|- constants.py       # "Conhecimento" do engine (valor das peças, tabelas posicionais)
|- engine.py          # "Cérebro" do engine (algoritmos de avaliação e busca)
|- visualizer.py      # Funções de apresentação (barra de vantagem, gráfico)
|- main.py            # Orquestrador da análise de partidas PGN
|- play.py            # Orquestrador do jogo interativo Humano vs. Engine
|- partida.pgn        # Arquivo de exemplo para análise
```

## 🧠 Arquitetura e Conceitos de IA

A inteligência do engine é dividida em módulos lógicos, cada um com uma responsabilidade clara.

### `constants.py` - O "Livro de Sabedoria"

Este módulo armazena o conhecimento estático do engine. Ele traduz a sabedoria estratégica do xadrez em números, que são usados pela função de avaliação.

```python
# Exemplo: Definição do valor material das peças
piece_value = {
    'p': 1,  # Peão
    'n': 3,  # Cavalo
    'q': 9,  # Rainha
    # ...
}
```

### `engine.py` - O "Cérebro" Pensante

Este módulo contém a lógica principal da IA.

* **Função de Avaliação (`evaluate_board`):** Atua como o "juiz", dando uma nota para qualquer posição do tabuleiro. Ela combina o valor material das peças com um bônus ou penalidade posicional retirado das tabelas em `constants.py`.

    ```python
    # Trecho da função que combina material e posição
    total_score += material_score + (positional_score / 100.0)
    ```

* **Algoritmo de Busca (`minimax_alpha_beta`):** O "estrategista". É um algoritmo recursivo que explora a árvore de lances futuros para encontrar a melhor jogada. A Poda Alfa-Beta é a otimização que torna essa busca eficiente.

    ```python
    # A linha que implementa a Poda Alfa-Beta, economizando processamento
    if beta <= alpha:
        break # "Poda" o galho da árvore de busca
    ```

### `visualizer.py` - O "Rosto" da Análise

Este módulo é responsável por traduzir a pontuação numérica do engine em formatos visuais e de fácil compreensão para humanos.

```python
# Trecho que colore as áreas de vantagem no gráfico
plt.fill_between(move_numbers, history_array, 0, 
                 where=(history_array >= 0), 
                 facecolor='white', alpha=0.8)

plt.fill_between(move_numbers, history_array, 0, 
                 where=(history_array <= 0), 
                 facecolor='black', alpha=0.8)
```

## 🚀 Como Executar o Projeto

1.  **Pré-requisitos:**
    Certifique-se de ter o [Python 3](https://www.python.org/downloads/) instalado no seu sistema.

2.  **Instalar as dependências:**
    Abra um terminal na pasta do projeto e execute o comando abaixo para instalar as bibliotecas necessárias:
    ```bash
    pip install python-chess numpy matplotlib
    ```

3.  **Para jogar contra o engine:**
    Execute o script `play.py`.
    ```bash
    python play.py
    ```

4.  **Para analisar uma partida de exemplo:**
    Certifique-se de ter um arquivo `partida.pgn` na mesma pasta do projeto e execute o script `main.py`.
    ```bash
    python main.py
    ```
    Um arquivo de imagem com o gráfico da partida (`grafico_avaliacao_aprimorado.png`) será salvo no diretório.

## 🔮 Próximos Passos

Este projeto serve como uma base sólida para futuras expansões, como:
- Desenvolvimento de uma interface gráfica (GUI) com PyGame ou Tkinter.
- Implementação de um "livro de aberturas" para jogadas iniciais mais rápidas.
- Criação de um sistema de otimização de parâmetros (Machine Learning) para ajustar os valores das tabelas posicionais.
- Substituição da função de avaliação por uma Rede Neural treinada com Aprendizado por Reforço.
