import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def visualization(blocks, bin_matrix, strx=""):
    # 1. Собираем все уникальные вершины из bin_matrix
    vertices = sorted(set([key[0] for key in bin_matrix] + [key[1] for key in bin_matrix]))
    idx_map = {v: i for i, v in enumerate(vertices)}

    # 2. Создаем пустую матрицу
    matrix = np.full((len(vertices), len(vertices)), '', dtype=object)

    # 3. Заполняем только верхнюю треугольную часть
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            vi, vj = vertices[i], vertices[j]
            value = bin_matrix.get((vi, vj), bin_matrix.get((vj, vi), ''))
            matrix[i][j] = str(value)

    # 4. Формируем DataFrame
    df_upper = pd.DataFrame(matrix, index=vertices, columns=vertices)

    # 5. Визуализация
    fig, axs = plt.subplots(2, 1, figsize=(12, 12))

    # --- Блоки ---
    text = '\n'.join(['{' + ', '.join(b) + '}' for b in blocks])
    axs[0].axis('off')
    axs[0].text(0.01, 0.99, f'Блоки:\n{text}', va='top', ha='left', fontsize=14, fontfamily='monospace')

    # --- Таблица ---
    axs[1].axis('off')
    axs[1].set_title("Треугольная матрица", fontsize=14)

    table = axs[1].table(
        cellText=df_upper.values,
        rowLabels=vertices,
        colLabels=vertices,
        loc='center',
        cellLoc='center',
        rowColours=["#f2f2f2"] * len(vertices),
        colColours=["#f2f2f2"] * len(vertices),
    )

    # Поворот заголовков столбцов
    for (row, col), cell in table.get_celld().items():
        if row == 0 and col > -1:
            cell.set_text_props(rotation=90, ha='center', va='bottom')

    plt.tight_layout()

    # --- Сохранение ---
    png_path = f"triangular_blocks_and_matrix{strx}.png"
    ods_path = f"triangular_blocks_and_matrix{strx}.ods"

    plt.savefig(png_path)
    df_upper.to_excel(ods_path, engine="odf")
