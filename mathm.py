import numpy as np


def all_eq_test(arr):
    y = arr[0]
    for x in arr:
        if x != y:
            return False
    return True


def normalize(vect):
    v0 = vect[0]
    k = vect[len(vect) - 1] - v0
    if k == 0:
        k = 1
    res = []
    for i in range(len(vect)):
        res.append((vect[i] - v0) / k)
    return res[1: len(res) - 1]


def cosine_similarity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    norm_vector1 = np.linalg.norm(vector1)
    norm_vector2 = np.linalg.norm(vector2)

    similarity = dot_product / (norm_vector1 * norm_vector2)

    return similarity


def average_of_arrays(array_of_arrays):
    res = []
    for i in range(len(array_of_arrays[0])):
        res.append(0)
        for j in range(len(array_of_arrays)):
            res[i] += array_of_arrays[j][i]
    for i in range(len(res)):
        res[i] /= len(array_of_arrays)
    return res


# def mlt(A, B):
#     return [[sum(A[i][k] * B[k][j] for k in range(len(A[0])))
#                for j in range(len(B[0]))] for i in range(len(A))]
#
#
# def haar_matrix(n):
#     if n == 1:
#         return np.array([[1]])
#     else:
#         h = np.eye(2)
#         while h.shape[0] < n:
#             top = np.kron(h, [1, 1])
#             bottom = np.kron(np.eye(h.shape[0]), [1, -1])
#             h = np.vstack((top, bottom))
#         return h[:n, :n]
