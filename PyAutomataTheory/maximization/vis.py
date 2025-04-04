import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def visualization(blocks, bin_matrix, strx=""):
    import pandas as pd
    # Уникальные вершины
    vertices = sorted(set(k for b in blocks for k in b))
    idx_map = {v: i for i, v in enumerate(vertices)}

    # Создаем треугольную матрицу (верхнюю)
    matrix = np.full((len(vertices), len(vertices)), '', dtype=object)
    for (i, j), val in bin_matrix.items():
        if i in idx_map and j in idx_map:
            row, col = idx_map[i], idx_map[j]
            if row < col:
                matrix[row][col] = str(val)

    # Меняем строки и столбцы местами (строки справа)
    df_upper = pd.DataFrame(matrix, index=vertices, columns=vertices)

    # Визуализация блоков и треугольной таблицы
    fig, axs = plt.subplots(2, 1, figsize=(10, 10))

    # Блоки
    text = '\n'.join(['{' + ', '.join(b) + '}' for b in blocks])
    axs[0].axis('off')
    axs[0].text(0.01, 0.99, f'Блоки:\n{text}', va='top', ha='left', fontsize=14, fontfamily='monospace')

    # Таблица (треугольная)
    axs[1].axis('off')
    axs[1].set_title("Бинарная матрица", fontsize=14)
    table = axs[1].table(cellText=df_upper.values, rowLabels=['']*len(vertices),
                        colLabels=df_upper.columns, loc='center', cellLoc='center',
                        rowColours=["#f2f2f2"]*len(vertices), colColours=["#f2f2f2"]*len(vertices))

    # Поворачиваем подписи строк вправо
    for i, key in enumerate(table.get_celld()):
        cell = table.get_celld()[key]
        if key[1] == -1:  # колонки
            cell.set_text_props(rotation=90)
        if key[0] == len(vertices):  # названия строк (справа)
            cell.get_text().set_horizontalalignment('left')

    plt.tight_layout()
    output_path_triangle = f"triangular_blocks_and_matrix{strx}.png"
    plt.savefig(output_path_triangle)
    import pandas as pd

    # Создаем DataFrame для треугольной матрицы смежности
    df_upper_ods = pd.DataFrame(df_upper.values, columns=vertices, index=vertices)

    # Сохраняем в формат ODS (OpenDocument Spreadsheet)
    ods_path = f"triangular_blocks_and_matrix{strx}.ods"
    df_upper_ods.to_excel(ods_path, engine="odf")
