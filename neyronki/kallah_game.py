# @title Игра
class Kalah:
    def __init__(self, num_holes=6, num_seeds=6.):
        self.num_holes = num_holes
        self.num_seeds = num_seeds

        self.board = [float(num_seeds) for _ in range(num_holes * 2 + 2)]  # Заполняем лунки

        self.kalah1_index = self.num_holes  # Индекс корзины первого игрока
        self.kalah2_index = self.num_holes + 1  # Индекс корзины второго игрока

        self.board[self.kalah1_index] = 0.
        self.board[self.kalah2_index] = 0.

        self.current_player = 0  # Текущий игрок

        self.diff1 = self.num_holes + 2  # Разница между противоположными лунками относительно прямого порядка
        self.diff2 = self.num_holes  # Разница между противоположными лунками относительно обратного порядка

    def step(self, action):
        hole = action
        player = self.current_player
        boardCopy = self.board.copy()
        if player == 1: hole -= self.num_holes

        # Если в выбранной лунке 0 камней, заканчиваем игру и отдаем все камни противоположному игроку
        if boardCopy[hole] == 0:
            for i in range(len(boardCopy)):
                boardCopy[i] = 0.
            boardCopy[self.num_holes + 1 - player] = 2 * self.num_holes * self.num_seeds
            return [boardCopy, player]

        seeds = boardCopy[hole]  # Запоминаем количество в выбранной лунке

        boardCopy[hole] = 0.  # Обнуляем выбранную лунку

        # Запускаем распределение камней
        while seeds > 0:
            hole = hole + 1 if hole >= 0 else hole - 1

            # Если прошли свою корзину, переходим на другую сторону
            if hole == self.num_holes + 1:
                hole = -1
            if hole == -1 * self.num_holes - 2:
                hole = 0

            # Если распределение дошло до корзины соперника, пропускаем её
            if hole == self.num_holes and player == 1:
                continue
            if hole == -1 * self.num_holes - 1 and player == 0:
                continue

            boardCopy[hole] += 1.  # Увеличиваем кол-во камней в лунке
            seeds -= 1.  # Уменьшаем кол-во камней в выбранной лунке

        # Если последний камень оказался в корзине, выходим без смены хода
        if hole == self.num_holes:
            return [boardCopy, player]
        if hole == -1 * self.num_holes - 1:
            return [boardCopy, player]

        # Если последний камень попал в пустую лунку принадлежащую ему и противоположная лунка соперника не пуста, то этот камень и все камни из противоположной лунки соперника игрок переносит себе в корзину
        if boardCopy[hole] == 1 and boardCopy[hole + self.diff1 if player == 0 else hole + self.diff2] > 0:
            if hole >= 0 and player == 0 or hole < 0 and player == 1:
                boardCopy[self.num_holes if hole >= 0 else self.num_holes + 1] += boardCopy[
                                                                                      hole + self.diff1 if hole >= 0 else hole + self.diff2] + 1.
                boardCopy[hole] = 0.
                boardCopy[hole + self.diff1 if player == 0 else hole + self.diff2] = 0.

        player = 1 - player
        return [boardCopy, player]

    def do_step(self, action):
        tmp = self.step(action)
        self.board = tmp[0]
        self.current_player = tmp[1]

    def game_over(self):
        return sum(self.board[:self.num_holes]) == 0 or sum(self.board[self.diff1:]) == 0 or self.board[
            -1 * self.num_holes - 1] > (self.num_holes * self.num_holes) or self.board[self.num_holes] > (
                       self.num_holes * self.num_holes)

    def get_winner(self):
        if not self.game_over():
            return None
        return 0 if self.board[self.num_holes] > self.board[-1 * self.num_holes - 1] else 1

    def get_value(self, action):
        hole = action
        if self.current_player == 1: hole -= self.num_holes
        return self.board[hole]

    def get_state(self):
        return [self.board, self.current_player]

    def get_valid_moves(self):
        moves = []
        for i in range(self.num_holes):
            if self.get_value(i) != 0:
                moves.append(i)
        return moves