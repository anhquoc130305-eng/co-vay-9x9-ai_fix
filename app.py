import streamlit as st
from game_logic import GoGame, BOARD_SIZE, BLACK, WHITE, EMPTY
from ai import MinimaxAI


st.set_page_config(
    page_title="Cờ Vây 9x9 AI",
    page_icon="⚫",
    layout="centered"
)


def init_game():
    st.session_state.game = GoGame()
    st.session_state.ai = MinimaxAI(st.session_state.game, depth=2)
    st.session_state.board = st.session_state.game.board
    st.session_state.game_over = False
    st.session_state.message = "Bạn là ⚫. AI là ⚪. Bạn đi trước."
    st.session_state.last_move = None


if "game" not in st.session_state:
    init_game()


def run_ai_move():
    game = st.session_state.game
    ai = st.session_state.ai

    move = ai.get_best_move(st.session_state.board)

    if move is None:
        st.session_state.message = "AI không còn nước đi."
        return

    x, y = move
    st.session_state.board = game.make_move(st.session_state.board, x, y, WHITE)
    st.session_state.last_move = (x, y)
    st.session_state.message = f"AI vừa đánh tại dòng {x + 1}, cột {y + 1}. Đến lượt bạn."


def check_game_over():
    game = st.session_state.game

    if game.is_game_over(st.session_state.board):
        st.session_state.game_over = True
        winner, black_score, white_score = game.get_winner(st.session_state.board)

        if winner == BLACK:
            st.session_state.message = f"Bạn thắng! ⚫ {black_score} - ⚪ {white_score}"
        elif winner == WHITE:
            st.session_state.message = f"AI thắng! ⚫ {black_score} - ⚪ {white_score}"
        else:
            st.session_state.message = f"Hòa! ⚫ {black_score} - ⚪ {white_score}"

        return True

    return False


def player_move(x, y):
    game = st.session_state.game

    if st.session_state.game_over:
        return

    if not game.is_valid_move(st.session_state.board, x, y, BLACK):
        st.session_state.message = "Nước đi không hợp lệ. Hãy chọn ô khác."
        return

    st.session_state.board = game.make_move(st.session_state.board, x, y, BLACK)
    st.session_state.last_move = (x, y)

    if check_game_over():
        return

    run_ai_move()
    check_game_over()


# xử lý click từ bàn cờ HTML
move = st.query_params.get("move")
if move and not st.session_state.game_over:
    try:
        x, y = map(int, move.split("-"))
        player_move(x, y)
    except:
        pass

    st.query_params.clear()
    st.rerun()


st.markdown(
    """
    <style>
    .stApp {
        background: #0f172a;
        color: white;
    }

    h1 {
        text-align: center;
        color: #f8fafc;
        font-size: 34px;
        font-weight: 900;
    }

    .subtitle {
        text-align: center;
        color: #cbd5e1;
        margin-bottom: 20px;
    }

    div[data-testid="stAlert"] {
        background-color: #1e3a8a;
        color: #dbeafe;
        border-radius: 14px;
        border: 1px solid #3b82f6;
    }

    [data-testid="stMetric"] {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 14px;
    }

    .board-wrap {
        display: flex;
        justify-content: center;
        margin-top: 20px;
        margin-bottom: 18px;
    }

    .go-board {
        width: 540px;
        height: 540px;
        background-color: #c98f3a;
        background-image:
            linear-gradient(#2b1a08 2px, transparent 2px),
            linear-gradient(90deg, #2b1a08 2px, transparent 2px);
        background-size: 67.5px 67.5px;
        background-position: 33.75px 33.75px;
        border: 6px solid #8b5a1e;
        border-radius: 8px;
        display: grid;
        grid-template-columns: repeat(9, 1fr);
        grid-template-rows: repeat(9, 1fr);
        box-shadow: 0 20px 45px rgba(0,0,0,0.45);
    }

    .cell {
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
    }

    .stone {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        box-shadow: 0 5px 12px rgba(0,0,0,0.45);
    }

    .black {
        background: radial-gradient(circle at 30% 25%, #64748b, #020617 65%);
    }

    .white {
        background: radial-gradient(circle at 30% 25%, #ffffff, #cbd5e1 70%);
    }

    .last {
        outline: 4px solid #22c55e;
        outline-offset: 3px;
    }

    .empty:hover {
        background: rgba(255,255,255,0.18);
        border-radius: 50%;
    }

    .guide {
        text-align: center;
        color: #cbd5e1;
        font-size: 14px;
        margin-bottom: 24px;
    }

    div.stButton > button {
        width: 100%;
        height: 46px;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 700;
        background: #1e293b;
        color: #f8fafc;
        border: 1px solid #475569;
    }

    div.stButton > button:hover {
        background: #334155;
        color: white;
        border: 1px solid #64748b;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("CỜ VÂY 9x9")
st.markdown(
    '<div class="subtitle">Bạn: <b>⚫ Quân đen</b> | AI: <b>⚪ Quân trắng</b></div>',
    unsafe_allow_html=True
)

black_score, white_score = st.session_state.game.calculate_score(st.session_state.board)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Bạn", black_score)
with col2:
    st.metric("AI", white_score)
with col3:
    st.metric("Bàn cờ", "9x9")

st.info(st.session_state.message)


board_html = '<div class="board-wrap"><div class="go-board">'

for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
        cell = st.session_state.board[i][j]
        is_last = st.session_state.last_move == (i, j)

        if cell == BLACK:
            last_class = " last" if is_last else ""
            board_html += f'<div class="cell"><div class="stone black{last_class}"></div></div>'

        elif cell == WHITE:
            last_class = " last" if is_last else ""
            board_html += f'<div class="cell"><div class="stone white{last_class}"></div></div>'

        else:
            if st.session_state.game_over:
                board_html += '<div class="cell"></div>'
            else:
                board_html += f'<a class="cell empty" href="?move={i}-{j}"></a>'

board_html += '</div></div>'

st.markdown(board_html, unsafe_allow_html=True)

st.markdown(
    '<div class="guide">Bấm vào giao điểm trống để đặt quân. Quân vừa đánh sẽ có vòng màu xanh.</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)

with left:
    if st.button("🔄 Chơi lại"):
        init_game()
        st.rerun()

with right:
    if st.button("🏁 Kết thúc & tính điểm"):
        st.session_state.game_over = True
        winner, black_score, white_score = st.session_state.game.get_winner(
            st.session_state.board
        )

        if winner == BLACK:
            st.session_state.message = f"Bạn thắng! ⚫ {black_score} - ⚪ {white_score}"
        elif winner == WHITE:
            st.session_state.message = f"AI thắng! ⚫ {black_score} - ⚪ {white_score}"
        else:
            st.session_state.message = f"Hòa! ⚫ {black_score} - ⚪ {white_score}"

        st.rerun()


with st.expander("Giải thích thuật toán"):
    st.write(
        """
        AI sử dụng thuật toán **Minimax** để tìm nước đi tốt nhất.

        Chương trình dùng **Alpha-Beta Pruning** để bỏ qua các nhánh không cần xét,
        giúp AI chạy nhanh hơn.

        Hàm đánh giá dựa trên số quân, số khí và chênh lệch điểm giữa hai bên.
        """
    )
