#!/usr/bin/env python
# -*- coding: utf-8 -*-


from eshirazi_2048_bot.board import Board, IllegalMoveException
from eshirazi_2048_bot.helpers import tuple_not_implemented, tuple_max, tuple_weighted_average
from eshirazi_2048_bot.moves import ALL_MOVES


DEFAULT_ILLEGAL_MOVE_SCORE = -1


class BaseStrategy(object):
    def get_next_move(self, board):
        raise NotImplementedError()


class BaseBoardScoreStrategy(BaseStrategy):
    def __init__(self, board_score_heuristic):
        self._board_score_heuristic = board_score_heuristic

    def get_next_move(self, board):
        return max(
            (move for move in board.get_legal_moves()),
            key=lambda move: self.calc_score_for_move(board, move)
        )

    def calc_score_for_move(self, board, move):
        raise NotImplementedError()


class AdvancedBoardScoreStrategy(BaseBoardScoreStrategy):
    """
    This strategy is similar to the simple one, but tries to "peek into the future".
    It tries various options that different moves lead to, and chooses a move according to
    agg_func - a score aggregation function.
    """

    def __init__(
            self,
            board_score_heuristic,
            depth_modifier=0,
            alpha_agg_func=tuple_not_implemented,
            beta_agg_func=tuple_not_implemented,
            illegal_move_score=DEFAULT_ILLEGAL_MOVE_SCORE
    ):
        super(AdvancedBoardScoreStrategy, self).__init__(board_score_heuristic)
        self._depth_modifier = depth_modifier
        self._alpha_agg_func = alpha_agg_func
        self._beta_agg_func = beta_agg_func
        self._illegal_move_score = illegal_move_score

    def calc_max_depth(self, board):
        num_free_tiles_left = board.get_num_free_tiles()

        return max(
            {
                0: 8,
                1: 7,
                2: 6,
                3: 5,
                4: 4,
                5: 4,
                6: 3,
                7: 3,
                8: 3,
                9: 3,
                10: 2,
                11: 2,
                12: 2,
                13: 2,
                14: 2,
                15: 2,
            }[num_free_tiles_left]
            + self._depth_modifier,
            1
        )

    def calc_alpha_score(self, board, iteration, max_depth):
        if iteration == max_depth:
            return self._board_score_heuristic(board)

        scores = []

        for move in ALL_MOVES:
            next_board = Board(board)

            try:
                next_board.move_only_swipe(move)
            except IllegalMoveException:
                scores.append(
                    (
                        self._illegal_move_score,
                        1
                    )
                )
                # Only counting possible moves
                continue

            scores.append(
                (
                    self.calc_beta_score(
                        next_board,
                        iteration=iteration + 1,
                        max_depth=max_depth
                    ),
                    1
                )
            )

        return self._alpha_agg_func(scores)

    def calc_beta_score(self, board, iteration, max_depth):
        if iteration == max_depth:
            return self._board_score_heuristic(board)

        scores = []

        for new_tile_value, probability in ((2, 9), (4, 1)):
            for tile in board.get_free_tiles():
                next_board = Board(board)

                next_board[tile] = new_tile_value

                scores.append(
                    (
                        self.calc_alpha_score(
                            next_board,
                            iteration=iteration + 1,
                            max_depth=max_depth
                        ),
                        probability
                    )
                )

        return self._beta_agg_func(scores)

    def calc_score_for_move(self, board, move):
        max_depth = self.calc_max_depth(board)

        next_board = Board(board)
        next_board.move_only_swipe(move)

        return self.calc_beta_score(
            next_board,
            1,
            max_depth=max_depth
        )


class ExpectimaxStrategy(AdvancedBoardScoreStrategy):
    def __init__(
            self,
            board_score_heuristic,
            depth_modifier=0,
            alpha_agg_func=tuple_max,
            beta_agg_func=tuple_weighted_average,
            illegal_move_score=DEFAULT_ILLEGAL_MOVE_SCORE
    ):
        super(ExpectimaxStrategy, self).__init__(
            board_score_heuristic,
            depth_modifier,
            alpha_agg_func,
            beta_agg_func,
            illegal_move_score
        )
