import random

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(f"{num:4}" for num in row))
    print()

def create_matrix(N, fill_value=None):
    if fill_value is not None:
        return [[fill_value for _ in range(N)] for _ in range(N)]
    return [[random.randint(-10, 10) for _ in range(N)] for _ in range(N)]

def get_submatrix(matrix, start_row, start_col, size):
    submatrix = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(matrix[start_row + i][start_col + j])
        submatrix.append(row)
    return submatrix

def place_submatrix(matrix, submatrix, start_row, start_col):
    for i in range(len(submatrix)):
        for j in range(len(submatrix[0])):
            matrix[start_row + i][start_col + j] = submatrix[i][j]

def count_zeros_in_odd_columns_in_region_4(submatrix_E):
    size = len(submatrix_E)
    count = 0
    for j in range(0, size, 2):  # нечетные столбцы (индексация с 0)
        for i in range(size // 2, size):  # область 4 (нижняя половина)
            if submatrix_E[i][j] == 0:
                count += 1
    return count

def product_in_odd_rows_in_region_1(submatrix_E):
    size = len(submatrix_E)
    product = 1
    for i in range(0, size, 2):  # нечетные строки (индексация с 0)
        for j in range(0, size // 2):  # область 1 (левая половина)
            product *= submatrix_E[i][j]
    return product

def swap_symmetrically_region_1_and_2(submatrix_C):
    size = len(submatrix_C)
    for i in range(size // 2):
        for j in range(size // 2):
            # Область 1: левая верхняя; область 2: правая верхняя
            submatrix_C[i][j], submatrix_C[i][size - 1 - j] = submatrix_C[i][size - 1 - j], submatrix_C[i][j]

def swap_non_symmetrically_B_and_E(submatrix_B, submatrix_E):
    size = len(submatrix_B)
    for i in range(size):
        for j in range(size):
            submatrix_B[i][j], submatrix_E[i][j] = submatrix_E[i][j], submatrix_B[i][j]

def transpose_matrix(matrix):
    return [list(row) for row in zip(*matrix)]

def multiply_matrices(A, B):
    size = len(A)
    result = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            for k in range(size):
                result[i][j] += A[i][k] * B[k][j]
    return result

def add_matrices(A, B):
    size = len(A)
    return [[A[i][j] + B[i][j] for j in range(size)] for i in range(size)]

def scalar_multiply_matrix(matrix, scalar):
    return [[element * scalar for element in row] for row in matrix]

def main():
    K = int(input("Введите число K: "))
    N = int(input("Введите число N (размер матрицы A, должно быть четным): "))
    if N % 2 != 0:
        print("N должно быть четным числом.")
        return

    submatrix_size = N // 2

    # Создаем матрицу A и подматрицы B, C, D, E (для тестирования заполняем их не случайными значениями)
    # Для тестирования можно использовать конкретные значения, например:
    A = create_matrix(N, fill_value=0)  # Заполняем нулями для теста
    B = create_matrix(submatrix_size, fill_value=1)
    C = create_matrix(submatrix_size, fill_value=2)
    D = create_matrix(submatrix_size, fill_value=3)
    E = create_matrix(submatrix_size, fill_value=4)

    # Размещаем подматрицы в матрице A
    place_submatrix(A, E, 0, 0)
    place_submatrix(A, B, 0, submatrix_size)
    place_submatrix(A, D, submatrix_size, 0)
    place_submatrix(A, C, submatrix_size, submatrix_size)

    print("Матрица A:")
    print_matrix(A)

    # Создаем матрицу F как копию A
    F = [row.copy() for row in A]

    # Получаем подматрицы из F
    submatrix_E_F = get_submatrix(F, 0, 0, submatrix_size)
    submatrix_B_F = get_submatrix(F, 0, submatrix_size, submatrix_size)
    submatrix_C_F = get_submatrix(F, submatrix_size, submatrix_size, submatrix_size)

    zeros_in_E = count_zeros_in_odd_columns_in_region_4(submatrix_E_F)
    product_in_E = product_in_odd_rows_in_region_1(submatrix_E_F)

    print(f"Количество нулей в нечетных столбцах в области 4 подматрицы E: {zeros_in_E}")
    print(f"Произведение чисел в нечетных строках в области 1 подматрицы E: {product_in_E}")

    if zeros_in_E * K > product_in_E:
        print("Условие выполнено: меняем в C области 1 и 2 симметрично.")
        swap_symmetrically_region_1_and_2(submatrix_C_F)
        place_submatrix(F, submatrix_C_F, submatrix_size, submatrix_size)
    else:
        print("Условие не выполнено: меняем B и E несимметрично.")
        swap_non_symmetrically_B_and_E(submatrix_B_F, submatrix_E_F)
        place_submatrix(F, submatrix_B_F, 0, submatrix_size)
        place_submatrix(F, submatrix_E_F, 0, 0)

    print("Матрица F после преобразований:")
    print_matrix(F)

    # Вычисляем A * F
    A_times_F = multiply_matrices(A, F)
    print("Результат умножения A * F:")
    print_matrix(A_times_F)

    # Вычисляем K * F^T
    F_transposed = transpose_matrix(F)
    K_times_F_transposed = scalar_multiply_matrix(F_transposed, K)
    print("Результат умножения K * F^T:")
    print_matrix(K_times_F_transposed)

    # Вычисляем A * F + K * F^T
    result = add_matrices(A_times_F, K_times_F_transposed)
    print("Результат выражения A * F + K * F^T:")
    print_matrix(result)

if __name__ == "__main__":
    main()