import matplotlib.pyplot as plt
import numpy as np

def get_advantage_bar(score):
    score = max(-10, min(10, score))
    bar_width = 40
    white_percentage = (score + 10) / 20
    white_blocks = int(white_percentage * bar_width)
    black_blocks = bar_width - white_blocks
    bar = '[' + '█' * white_blocks + ' ' * black_blocks + ']'
    return bar

def plot_evaluation(history, filename="grafico_avaliacao.png"):
    history_array = np.array(history)
    move_numbers = np.arange(len(history_array))
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(14, 7))
    plt.fill_between(move_numbers, history_array, 0, where=(history_array >= 0), facecolor='white', interpolate=True, alpha=0.8)
    plt.fill_between(move_numbers, history_array, 0, where=(history_array <= 0), facecolor='black', interpolate=True, alpha=0.8)
    plt.plot(move_numbers, history_array, marker='', linestyle='-', color='royalblue', linewidth=2.5, label='Avaliação do Engine')
    plt.axhline(0, color='black', linewidth=1.0, linestyle='--')
    plt.title('Gráfico de Vantagem da Partida', fontsize=18, fontweight='bold')
    plt.xlabel('Número do Meio-Lance', fontsize=12)
    plt.ylabel('Pontuação (Vantagem)', fontsize=12)
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.ylim(-5, 5)
    plt.xticks(move_numbers)
    plt.savefig(filename, dpi=150)
    print(f"\nGráfico da avaliação salvo como '{filename}'")