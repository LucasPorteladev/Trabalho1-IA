# src/run_experiments.py
import os
import csv
from pathlib import Path
from maze import Maze
from heuristics import h_manhattan, h_euclidean
from search import bfs_search, dfs_search, greedy_search, a_star_search

def run_all_in_directory(data_dir: str, output_csv: str = "results_all.csv"):
    """
    Executa todos os algoritmos (BFS, DFS, Gulosa, A*) em todos os labirintos .txt
    presentes na pasta data_dir, salvando um CSV consolidado.
    """

    # Caminhos e verificação
    data_path = Path(data_dir)
    if not data_path.exists():
        raise FileNotFoundError(f"Pasta de dados não encontrada: {data_dir}")

    maze_files = sorted([f for f in data_path.glob("*.txt")])
    if not maze_files:
        raise FileNotFoundError("Nenhum arquivo .txt encontrado em data/")

    print(f"🧩 {len(maze_files)} labirintos encontrados em '{data_dir}'")

    algorithms = [
    ("BFS", lambda m: bfs_search(m)),
    ("DFS", lambda m: dfs_search(m)),
    ("Greedy-Manhattan", lambda m: greedy_search(m, h_manhattan)),
    ("A*-Manhattan", lambda m: a_star_search(m, h_manhattan)),
    ("Greedy-Euclidean", lambda m: greedy_search(m, h_euclidean)),
    ("A*-Euclidean", lambda m: a_star_search(m, h_euclidean)),
]

    rows = []

    for maze_file in maze_files:
        print(f"\n=== Executando algoritmos em {maze_file.name} ===")
        mz = Maze.from_file(str(maze_file))

        # Extrai informações do nome (se seguir o padrão labirinto_10x10_d30.txt)
        name_parts = maze_file.stem.split("_")
        size = "?"
        density = "?"
        for part in name_parts:
            if "x" in part:
                size = part
            elif part.startswith("d"):
                density = part.replace("d", "") + "%"
        if size == "?":
            size = f"{mz.H}x{mz.W}"

        for name, fn in algorithms:
            print(f"  Rodando {name} ...")
            res = fn(mz)

            row = {
                "maze_file": maze_file.name,
                "maze_size": size,
                "maze_density": density,
                "algorithm": name,
                "found": res.found,
                "cost": res.cost if res.found else None,
                "time_s": round(res.time, 6),
                "nodes_generated": res.metrics.get("nodes_generated", 0),
                "nodes_expanded": res.metrics.get("nodes_expanded", 0),
                "max_frontier_size": res.metrics.get("max_frontier_size", 0),
                "max_explored_size": res.metrics.get("max_explored_size", 0),
                "path_length": len(res.path),
            }

            rows.append(row)
            print(
                f"     {name}: encontrado={row['found']}, "
                f"custo={row['cost']}, tempo={row['time_s']}s, "
                f"nós expandidos={row['nodes_expanded']}"
            )

    # Salva CSV consolidado
    output_path = Path(output_csv)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n Resultados consolidados salvos em: {output_path.resolve()}")

if __name__ == "__main__":
    HERE = Path(__file__).parent
    data_dir = os.path.join(HERE.parent, "data")
    output_csv = os.path.join(HERE.parent, "results", "results_all.csv")

    run_all_in_directory(data_dir, output_csv)
