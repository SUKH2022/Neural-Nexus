from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random
import time
import os

app = Flask(__name__)
CORS(app)

class NeuralNexusAI:
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty
        
    def get_valid_moves(self, board, player):
        valid_moves = []
        
        # Find all valid moves
        for i in range(8):
            for j in range(8):
                if board[i][j] == 0:
                    # Check if adjacent to existing pieces
                    if (i > 0 and board[i-1][j] != 0) or (i < 7 and board[i+1][j] != 0) or \
                       (j > 0 and board[i][j-1] != 0) or (j < 7 and board[i][j+1] != 0):
                        valid_moves.append((i, j))
        return valid_moves
    
    def get_best_move(self, board, difficulty):
        valid_moves = self.get_valid_moves(board, 2)  # 2 represents AI
        
        if not valid_moves:
            return None
            
        # Different strategies based on difficulty
        if difficulty == 'easy':
            time.sleep(1)
            return random.choice(valid_moves)
        elif difficulty == 'medium':
            time.sleep(1.5)
            # Prefer center positions
            center_moves = [move for move in valid_moves if 2 <= move[0] <= 5 and 2 <= move[1] <= 5]
            if center_moves:
                return random.choice(center_moves)
            return random.choice(valid_moves)
        elif difficulty == 'hard':
            time.sleep(2)
            # Try to find moves that capture pieces
            for move in valid_moves:
                i, j = move
                # Check if this move would capture pieces
                for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    x, y = i + dx, j + dy
                    if 0 <= x < 8 and 0 <= y < 8 and board[x][y] == 1:  # Player's piece
                        return move
            return random.choice(valid_moves)
        else:  # impossible
            time.sleep(0.5)
            # Try to find the move that captures the most pieces
            best_move = None
            best_capture = 0
            
            for move in valid_moves:
                i, j = move
                capture_count = 0
                
                # Check all directions for captures
                for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    x, y = i + dx, j + dy
                    if 0 <= x < 8 and 0 <= y < 8 and board[x][y] == 1:  # Player's piece
                        capture_count += 1
                
                if capture_count > best_capture:
                    best_capture = capture_count
                    best_move = move
            
            return best_move if best_move else random.choice(valid_moves)

# API endpoint for AI moves
@app.route('/ai_move', methods=['POST'])
def ai_move():
    try:
        data = request.json
        board = data['board']
        difficulty = data.get('difficulty', 'medium')
        
        ai = NeuralNexusAI(difficulty)
        move = ai.get_best_move(board, difficulty)
        
        if move:
            return jsonify({'row': move[0], 'col': move[1]})
        else:
            return jsonify({'error': 'No valid moves'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)