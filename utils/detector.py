def detect_move(prev_occ, curr_occ):
    from_sq, to_sq = None, None
    for i in range(8):
        for j in range(8):
            if prev_occ[i][j] == 1 and curr_occ[i][j] == 0:
                from_sq = (i, j)
            elif prev_occ[i][j] == 0 and curr_occ[i][j] == 1:
                to_sq = (i, j)
    return from_sq, to_sq


def update_board_matrix(board_matrix, from_sq, to_sq):
    piece = board_matrix[from_sq[0]][from_sq[1]]
    board_matrix[from_sq[0]][from_sq[1]] = ""
    board_matrix[to_sq[0]][to_sq[1]] = piece
    return board_matrix