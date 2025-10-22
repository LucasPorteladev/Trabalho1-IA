# src/plot_comparative.py
import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path
import numpy as np

def plot_comparative(csv_path: str, output_dir: str = "../results"):
    """
    Lê o arquivo CSV consolidado (results_all.csv) e gera:
      - Gráficos comparativos (tempo, nós, memória)
      - Resumo estatístico (tempo, nós, custo, memória)
    """

    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(csv_path)

    # -----------------------------
    # 1. Limpeza e tratamento
    # -----------------------------
    def parse_size(size_str):
        try:
            w, h = size_str.lower().split("x")
            return int(w), int(h)
        except Exception:
            return None, None

    df["width"], df["height"] = zip(*df["maze_size"].map(parse_size))
    df["cells"] = df["width"] * df["height"]

    def safe_to_float(x):
        try:
            return float(str(x).replace("%", ""))
        except ValueError:
            return None

    df["density"] = df["maze_density"].apply(safe_to_float)

    # Nova métrica de uso de memória (nós mantidos simultaneamente)
    df["memory_usage"] = df["max_frontier_size"] + df["max_explored_size"]

    df = df.dropna(subset=["width", "time_s", "nodes_expanded"])

    algorithms = ["BFS", "DFS", "Greedy-Manhattan", "Greedy-Euclidean", "A*-Manhattan", "A*-Euclidean"]
    colors = ["#171db6", "#d12222", "#7241a0", "#c5b0d5", "#178a1b", "#22f130"]

    # -----------------------------
    # 2. Gráfico – Tempo × Tamanho
    # -----------------------------
    grouped_size = (
        df.groupby(["algorithm", "width"], as_index=False)
        .agg({"time_s": "mean"})
        .sort_values(by="width")
    )

    plt.figure(figsize=(8, 5))
    for algo, color in zip(algorithms, colors):
        subset = grouped_size[grouped_size["algorithm"] == algo]
        plt.plot(subset["width"], subset["time_s"], marker="^", linewidth=2, markersize=6, color=color, label=algo)
    plt.title("Tempo médio por tamanho do labirinto", fontsize=13, weight="bold")
    plt.xlabel("Tamanho (largura)", fontsize=11)
    plt.ylabel("Tempo médio (s)", fontsize=11)
    if grouped_size["time_s"].max() / grouped_size["time_s"].min() > 50:
        plt.yscale("log")
        plt.ylabel("Tempo médio (s) [escala log]", fontsize=11)
    plt.legend(title="Algoritmo", fontsize=9)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "comparativo_tempo_tamanho.png"), dpi=300)
    plt.close()

    # -----------------------------
    # 3. Gráfico – Nós Expandidos × Tamanho
    # -----------------------------
    grouped_nodes = (
        df.groupby(["algorithm", "width"], as_index=False)
        .agg({"nodes_expanded": "mean"})
        .sort_values(by="width")
    )

    plt.figure(figsize=(8, 5))
    for algo, color in zip(algorithms, colors):
        subset = grouped_nodes[grouped_nodes["algorithm"] == algo]
        plt.plot(subset["width"], subset["nodes_expanded"], marker="^", linewidth=2, markersize=6, color=color, label=algo)
    plt.title("Nós expandidos por tamanho de labirinto", fontsize=13, weight="bold")
    plt.xlabel("Tamanho do labirinto", fontsize=11)
    plt.ylabel("Nós expandidos (média)", fontsize=11)
    plt.legend(title="Algoritmo", fontsize=9)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "comparativo_nos_tamanho.png"), dpi=300)
    plt.close()

    # -----------------------------
    # 4. Gráfico – Memória × Tamanho
    # -----------------------------
    grouped_memory = (
        df.groupby(["algorithm", "width"], as_index=False)
        .agg({"memory_usage": "mean"})
        .sort_values(by="width")
    )

    plt.figure(figsize=(8, 5))
    for algo, color in zip(algorithms, colors):
        subset = grouped_memory[grouped_memory["algorithm"] == algo]
        plt.plot(subset["width"], subset["memory_usage"], marker="^", linewidth=2, markersize=6, color=color, label=algo)
    plt.title("Uso de memória por tamanho do labirinto", fontsize=13, weight="bold")
    plt.xlabel("Tamanho do labirinto", fontsize=11)
    plt.ylabel("Nós armazenados simultaneamente (média)", fontsize=11)
    plt.legend(title="Algoritmo", fontsize=9)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "comparativo_memoria_tamanho.png"), dpi=300)
    plt.close()

    # -----------------------------
    # 5. Gráfico – Tempo × Densidade (opcional)
    # -----------------------------
    valid_density = df.dropna(subset=["density"])
    if not valid_density.empty:
        grouped_density = (
            valid_density.groupby(["algorithm", "density"], as_index=False)
            .agg({"time_s": "mean"})
            .sort_values(by="density")
        )

        plt.figure(figsize=(8, 5))
        for algo, color in zip(algorithms, colors):
            subset = grouped_density[grouped_density["algorithm"] == algo]
            plt.plot(subset["density"], subset["time_s"], marker="^", linewidth=2, markersize=6, color=color, label=algo)
        plt.title("Tempo médio por densidade de labirinto", fontsize=13, weight="bold")
        plt.xlabel("Densidade de paredes (%)", fontsize=11)
        plt.ylabel("Tempo médio (s)", fontsize=11)
        plt.legend(title="Algoritmo", fontsize=9)
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "comparativo_tempo_densidade.png"), dpi=300)
        plt.close()
        print("✅ Gráfico de densidade gerado com sucesso.")
    else:
        print("⚠️ Nenhuma densidade válida encontrada; gráfico de densidade não gerado.")

    # -----------------------------
    # 6. Resumo estatístico
    # -----------------------------
    stats = (
        df.groupby("algorithm")
        .agg(
            tempo_medio=("time_s", "mean"),
            tempo_desvio=("time_s", "std"),
            nos_medios=("nodes_expanded", "mean"),
            nos_desvio=("nodes_expanded", "std"),
            memoria_media=("memory_usage", "mean"),
            memoria_desvio=("memory_usage", "std"),
            custo_medio=("cost", "mean"),
        )
        .round(4)
        .reset_index()
    )

    # Salva o resumo
    stats_path = os.path.join(output_dir, "summary_statistics.csv")
    stats.to_csv(stats_path, index=False, encoding="utf-8")
    print("\n📊 Resumo estatístico salvo em:", stats_path)
    print(stats.to_string(index=False))

    print(f"\n✅ Todos os gráficos salvos em {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    HERE = Path(__file__).parent
    csv_path = os.path.join(HERE.parent, "results_all.csv")
    plot_comparative(csv_path)
