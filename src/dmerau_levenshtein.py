import Levenshtein

def damerau_levenshtein_distance(str1: str, str2: str) -> int:
    """
    Calculate the Damerau-Levenshtein distance between two strings.
    """
    distance = Levenshtein.distance(str1, str2)
    return distance

if __name__ == '__main__':
    print(damerau_levenshtein_distance("kitten", "sitting"))



# def damerau_levenshtein(seq1, seq2):
#     """
#     Calculates the Damerau-Levenshtein distance between two sequences.

#     Args:
#         seq1: The first sequence.
#         seq2: The second sequence.

#     Returns:
#         The Damerau-Levenshtein distance between the two sequences.
#     """

#     # Create a 2D table to store the edit distances.
#     n, m = len(seq1), len(seq2)
#     d = [[0 for _ in range(m + 1)] for _ in range(n + 1)]

#     # Initialize the first row and first column.
#     for i in range(1, n + 1):
#         d[i][0] = i
#     for j in range(1, m + 1):
#         d[0][j] = j

#     # Fill the table.
#     for i in range(1, n + 1):
#         for j in range(1, m + 1):
#         # Cost of deletion.
#         deletion = d[i - 1][j] + 1
#         # Cost of insertion.
#         insertion = d[i][j - 1] + 1
#         # Cost of substitution.
#         substitution = d[i - 1][j - 1] + (1 if seq1[i - 1] != seq2[j - 1] else 0)
#         # Cost of transposition.
#         transposition = min(
#             d[i - 2][j - 1] + 1,
#             d[i - 1][j - 2] + 1 if i > 1 and j > 1 and seq1[i - 2] == seq2[j - 1] and seq1[i - 1] == seq2[j - 2] else float('inf')
#         )
#         # Choose the minimum cost.
#         d[i][j] = min(deletion, insertion, substitution, transposition)

#     # Return the distance.
#     return d[n][m]

