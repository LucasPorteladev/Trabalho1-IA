# src/generate_mazes.py
import random
import os

def generate_maze(width, height, densidade=0.25, nome_arquivo="labirinto.txt"):
    """
    Gera um labirinto aleatório com densidade de paredes controlada.
    """
    grid = [['.' for _ in range(width)] for _ in range(height)]

    # Posição inicial e final fixas nos cantos
    grid[0][0] = 'S'
    grid[height-1][width-1] = 'G'

    # Preenche com paredes aleatórias
    for r in range(height):
        for c in range(width):
            if (r, c) not in [(0, 0), (height-1, width-1)]:
                if random.random() < densidade:
                    grid[r][c] = '#'

    # Garante que início e fim estão livres
    grid[0][0] = 'S'
    grid[height-1][width-1] = 'G'

    os.makedirs("../data", exist_ok=True)
    caminho = os.path.join("../data", nome_arquivo)
    with open(caminho, 'w', encoding='utf-8') as f:
        for linha in grid:
            f.write(''.join(linha) + '\n')
    print(f"Labirinto salvo em {caminho}")

if __name__ == "__main__":
    random.seed(42)
    tamanhos = [(5,5), (10,10), (15,15), (20,20)]
    densidades = [0.2, 0.3]

    for h, w in tamanhos:
        for d in densidades:
            nome = f"labirinto_{h}x{w}_d{int(d*100)}.txt"
            generate_maze(w, h, densidade=d, nome_arquivo=nome)
