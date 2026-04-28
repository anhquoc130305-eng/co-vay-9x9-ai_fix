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
        margin-bottom: 6px;
    }

    .subtitle {
        text-align: center;
        color: #cbd5e1;
        margin-bottom: 20px;
        font-size: 15px;
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

    [data-testid="stMetricLabel"] {
        color: #cbd5e1;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc;
    }

    .board-area {
        width: 520px;
        height: 520px;
        margin: 28px auto 12px auto;
        background-color: #c98f3a;
        border: 6px solid #8b5a1e;
        border-radius: 10px;
        box-shadow: 0 20px 45px rgba(0,0,0,0.45);
        padding: 20px;
        position: relative;
    }

    .board-area::before {
        content: "";
        position: absolute;
        left: 45px;
        top: 45px;
        width: 400px;
        height: 400px;
        background-image:
            linear-gradient(#2b1a08 2px, transparent 2px),
            linear-gradient(90deg, #2b1a08 2px, transparent 2px);
        background-size: 50px 50px;
        background-position: 0 0;
        pointer-events: none;
    }

    div[data-testid="column"] {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    div.stButton > button {
        width: 44px;
        height: 44px;
        padding: 0;
        border-radius: 50%;
        border: none;
        background: transparent;
        color: #111827;
        font-size: 24px;
        box-shadow: none;
        position: relative;
        z-index: 3;
    }

    div.stButton > button:hover {
        background: rgba(255,255,255,0.22);
        border-radius: 50%;
    }

    div.stButton > button:disabled {
        background: transparent;
        color: inherit;
        opacity: 1;
    }

    .guide {
        text-align: center;
        color: #cbd5e1;
        font-size: 14px;
        margin-bottom: 24px;
    }

    .control button {
        width: 100% !important;
        height: 46px !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        background: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
    }

    .control button:hover {
        background: #334155 !important;
        color: white !important;
        border: 1px solid #64748b !important;
    }

    div[data-testid="stExpander"] {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 12px;
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


st.markdown('<div class="board-area">', unsafe_allow_html=True)

for i in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE, gap="small")

    for j in range(BOARD_SIZE):
        cell = st.session_state.board[i][j]
        is_last = st.session_state.last_move == (i, j)

        if cell == BLACK:
            label = "🟢" if is_last else "⚫"
        elif cell == WHITE:
            label = "🟢" if is_last else "⚪"
        else:
            label = "·"

        disabled = st.session_state.game_over or cell != EMPTY

        with cols[j]:
            if st.button(label, key=f"move-{i}-{j}", disabled=disabled):
                player_move(i, j)
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="guide">Bấm vào giao điểm để đặt quân. Quân vừa đánh sẽ hiện màu xanh.</div>',
    unsafe_allow_html=True
)


left, right = st.columns(2)

with left:
    st.markdown('<div class="control">', unsafe_allow_html=True)
    if st.button("🔄 Chơi lại"):
        init_game()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="control">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)


with st.expander("Giải thích thuật toán"):
    st.write(
        """
        AI sử dụng thuật toán **Minimax** để tìm nước đi tốt nhất.

        Chương trình dùng **Alpha-Beta Pruning** để bỏ qua các nhánh không cần xét,
        giúp AI chạy nhanh hơn.

        Hàm đánh giá dựa trên số quân, số khí và chênh lệch điểm giữa hai bên.
        """
    )
