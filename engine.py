import chess
import random
import math


class Player:
   

    def get_move(self, board: chess.Board) -> chess.Move:
        
        raise NotImplementedError(
        )


class RandomAgent(Player):
   

    def get_move(self, board: chess.Board) -> chess.Move:
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
        return random.choice(legal_moves)


class BaseSearchAgent(Player):
   

    def __init__(self, depth: int):
        self.depth = depth

    def evaluate_board(self, board: chess.Board) -> float:
       
        return 0.0

    def minimax(
        self,
        board: chess.Board,
        depth: int,
        alpha: float,
        beta: float,
        maximizing_player: bool,
    ) -> float:
        
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        if maximizing_player:
            max_eval = -math.inf
            for move in board.legal_moves:
                board.push(move)  
                eval_score = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop() 
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  
            return max_eval
        else:
            min_eval = math.inf
            for move in board.legal_moves:
                board.push(move)
                eval_score = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  
            return min_eval

    def get_move(self, board: chess.Board) -> chess.Move:
       
        best_move = None
        legal_moves = list(board.legal_moves)

        if not legal_moves:
            return None

        maximizing_player = board.turn == chess.WHITE
        best_value = -math.inf if maximizing_player else math.inf

        for move in legal_moves:
            board.push(move)
            # Gọi minimax cho nhánh con
            board_value = self.minimax(
                board, self.depth - 1, -math.inf, math.inf, not maximizing_player
            )
            board.pop()

            if maximizing_player:
                if board_value > best_value:
                    best_value = board_value
                    best_move = move
            else:
                if board_value < best_value:
                    best_value = board_value
                    best_move = move

        if best_move is None:
            best_move = random.choice(legal_moves)

        return best_move
        # legal_moves = list(board.legal_moves)
        # return random.choice(legal_moves) if legal_moves else None




class PoorAgent(BaseSearchAgent):

    def __init__(self):
        super().__init__(depth=2) 

        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }

    def evaluate_board(self, board: chess.Board) -> float:
        
        if board.is_checkmate():
            
            return -9999 if board.turn == chess.WHITE else 9999

        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        score = 0

        for square, piece in board.piece_map().items():
            value = self.piece_values[piece.piece_type]
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value

        return score

class AverageAgent(BaseSearchAgent):
    def __init__(self):
        super().__init__(depth=3)
        
        self.piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }

        self.knight_pst = [
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50,
        ]

        self.pawn_pst = [
             0,  0,  0,  0,  0,  0,  0,  0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
             5,  5, 10, 25, 25, 10,  5,  5,
             0,  0,  0, 20, 20,  0,  0,  0,
             5, -5,-10,  0,  0,-10, -5,  5,
             5, 10, 10,-20,-20, 10, 10,  5,
             0,  0,  0,  0,  0,  0,  0,  0
        ]

        self.bishop_pst = [
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -20,-10,-10,-10,-10,-10,-10,-20,
        ]

        self.rook_pst = [
             0,  0,  0,  0,  0,  0,  0,  0,
             5, 10, 10, 10, 10, 10, 10,  5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
             0,  0,  0,  5,  5,  0,  0,  0
        ]

        self.queen_pst = [
            -20,-10,-10, -5, -5,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5,  5,  5,  5,  0,-10,
             -5,  0,  5,  5,  5,  5,  0, -5,
              0,  0,  5,  5,  5,  5,  0, -5,
            -10,  5,  5,  5,  5,  5,  0,-10,
            -10,  0,  5,  0,  0,  0,  0,-10,
            -20,-10,-10, -5, -5,-10,-10,-20
        ]

        self.king_pst = [
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -20,-30,-30,-40,-40,-30,-30,-20,
            -10,-20,-20,-20,-20,-20,-20,-10,
             20, 20,  0,  0,  0,  0, 20, 20,
             20, 30, 10,  0,  0, 10, 30, 20
        ]

    def evaluate_board(self, board: chess.Board) -> float:
        
        if board.is_checkmate():
            return -99999 if board.turn == chess.WHITE else 99999
        if board.is_stalemate() or board.is_insufficient_material():
            return 0.0

        score = 0.0
        
        for square, piece in board.piece_map().items():
            val = self.piece_values[piece.piece_type]
            
            
            pst_val = 0
            if piece.piece_type == chess.KNIGHT:
                sq_idx = square if piece.color == chess.WHITE else 63 - square
                pst_val = self.knight_pst[sq_idx]
            elif piece.piece_type == chess.PAWN:
                sq_idx = square if piece.color == chess.WHITE else 63 - square
                pst_val = self.pawn_pst[sq_idx]

            if piece.color == chess.WHITE:
                score += (val + pst_val)
            else:
                score -= (val + pst_val)

        return score


class GoodAgent(BaseSearchAgent):
    def __init__(self):
        super().__init__(depth=4)

        self.piece_value = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }

        # Pawn & Knight (đã có)
        self.pawn_pst = [
             0,0,0,0,0,0,0,0,
            50,50,50,50,50,50,50,50,
            10,10,20,30,30,20,10,10,
             5,5,10,25,25,10,5,5,
             0,0,0,20,20,0,0,0,
             5,-5,-10,0,0,-10,-5,5,
             5,10,10,-20,-20,10,10,5,
             0,0,0,0,0,0,0,0
        ]

        self.knight_pst = [
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,0,0,0,0,-20,-40,
            -30,0,10,15,15,10,0,-30,
            -30,5,15,20,20,15,5,-30,
            -30,0,15,20,20,15,0,-30,
            -30,5,10,15,15,10,5,-30,
            -40,-20,0,5,5,0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50
        ]

        # 🔥 Thêm đầy đủ PST
        self.bishop_pst = [
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,0,0,0,0,0,0,-10,
            -10,0,5,10,10,5,0,-10,
            -10,5,5,10,10,5,5,-10,
            -10,0,10,10,10,10,0,-10,
            -10,10,10,10,10,10,10,-10,
            -10,5,0,0,0,0,5,-10,
            -20,-10,-10,-10,-10,-10,-10,-20
        ]

        self.rook_pst = [
             0,0,0,0,0,0,0,0,
             5,10,10,10,10,10,10,5,
            -5,0,0,0,0,0,0,-5,
            -5,0,0,0,0,0,0,-5,
            -5,0,0,0,0,0,0,-5,
            -5,0,0,0,0,0,0,-5,
            -5,0,0,0,0,0,0,-5,
             0,0,0,5,5,0,0,0
        ]

        self.queen_pst = [
            -20,-10,-10,-5,-5,-10,-10,-20,
            -10,0,0,0,0,0,0,-10,
            -10,0,5,5,5,5,0,-10,
             -5,0,5,5,5,5,0,-5,
              0,0,5,5,5,5,0,-5,
            -10,5,5,5,5,5,0,-10,
            -10,0,5,0,0,0,0,-10,
            -20,-10,-10,-5,-5,-10,-10,-20
        ]

        self.king_pst = [
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -20,-30,-30,-40,-40,-30,-30,-20,
            -10,-20,-20,-20,-20,-20,-20,-10,
             20,20,0,0,0,0,20,20,
             20,30,10,0,0,10,30,20
        ]

    # 🔥 Move ordering
    def order_moves(self, board):
        return sorted(
            board.legal_moves,
            key=lambda move: board.is_capture(move),
            reverse=True
        )

    def evaluate_board(self, board: chess.Board) -> float:
        if board.is_checkmate():
            return -99999 if board.turn == chess.WHITE else 99999

        if board.is_stalemate() or board.is_insufficient_material():
            return 0.0

        score = 0.0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                material = self.piece_value[piece.piece_type]

                pst_index = square if piece.color == chess.WHITE else chess.square_mirror(square)
                position_score = 0

                if piece.piece_type == chess.PAWN:
                    position_score = self.pawn_pst[pst_index]
                elif piece.piece_type == chess.KNIGHT:
                    position_score = self.knight_pst[pst_index]
                elif piece.piece_type == chess.BISHOP:
                    position_score = self.bishop_pst[pst_index]
                elif piece.piece_type == chess.ROOK:
                    position_score = self.rook_pst[pst_index]
                elif piece.piece_type == chess.QUEEN:
                    position_score = self.queen_pst[pst_index]
                elif piece.piece_type == chess.KING:
                    position_score = self.king_pst[pst_index]

                if piece.color == chess.WHITE:
                    score += (material + position_score)
                else:
                    score -= (material + position_score)

        return score

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        if maximizing_player:
            max_eval = -math.inf
            for move in self.order_moves(board):
                board.push(move)
                eval_score = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in self.order_moves(board):
                board.push(move)
                eval_score = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval