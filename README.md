# Comparação de Algoritmos de Busca em Labirintos

## Objetivo
Este projeto implementa e compara algoritmos de busca em labirintos: **BFS**, **DFS**, **A\*** e **Busca Gulosa**, utilizando diferentes heurísticas (**Manhattan** e **Euclidiana**). O objetivo é analisar o desempenho de cada algoritmo em termos de tempo de execução, custo do caminho e número de nós expandidos.

## Estrutura do Repositório
```bash
meu-projeto/
│
├── src/
│ ├── generate_mazes.py
│ ├── maze.py
│ ├── search.py
│ ├── heuristics.py
│ ├── run_experiments.py
│ └── plot_comparative.py
│
├── data/ # Labirintos .txt gerados
├── results/ # CSV e gráficos
├── requirements.txt # Dependências externas
└── README.md
```
## Instalação

1. Clone o repositório:
```bash
git clone <URL_DO_REPOSITORIO>
cd meu-projeto
```
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como executar os códigos

1. Gerar labirintos
```bash
python src/generate_mazes.py
```

2. Rodar os experimentos
```bash
python src/run_experiments.py
```
Isso executa todos os algoritmos em todos os labirintos e salva os resultados em results/results_all.csv.

3. Gerar gráficos comparativos
```bash
python src/plot_comparative.py
```

Os gráficos mostrarão comparações de desempenho entre algoritmos e o impacto das heurísticas.
