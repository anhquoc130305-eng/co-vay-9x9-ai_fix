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

    if check_game_over():
        return

    run_ai_move()
    check_game_over()


st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top, #1f2937 0%, #111827 45%, #020617 100%);
        color: #e5e7eb;
    }

    h1 {
        text-align: center;
        color: #f9fafb;
        font-size: 34px;
        font-weight: 900;
        margin-bottom: 0px;
    }

    .sub-title {
        text-align: center;
        color: #cbd5e1;
        font-size: 17px;
        margin-bottom: 24px;
    }

    .game-card {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 22px;
        padding: 22px;
        box-shadow: 0 20px 45px rgba(0,0,0,0.35);
        margin-bottom: 18px;
    }

    [data-testid="stMetric"] {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 14px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.25);
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc;
        font-size: 24px;
    }

    div[data-testid="stAlert"] {
        background-color: #172554;
        color: #dbeafe;
        border: 1px solid #3b82f6;
        border-radius: 14px;
        font-size: 17px;
    }

    div.stButton > button {
        width: 48px;
        height: 48px;
        padding: 0px;
        font-size: 24px;
        font-weight: bold;
        border-radius: 12px;
        background-color: #b8833b;
        color: #111827;
        border: 1px solid #facc15;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.25), 0 4px 10px rgba(0,0,0,0.35);
        transition: 0.15s ease-in-out;
    }

    div.stButton > button:hover {
        background-color: #d99b45;
        border: 1px solid #fde68a;
        transform: scale(1.06);
    }

    div.stButton > button:disabled {
        opacity: 1;
        background-color: #b8833b;
        color: #111827;
        border: 1px solid #facc15;
    }

    .stButton button p {
        font-size: 24px;
        line-height: 1;
    }

    .control-btn button {
        width: 100% !important;
        height: 48px !important;
        font-size: 16px !important;
        border-radius: 14px !important;
        background: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
    }

    .small-guide {
        color: #cbd5e1;
        text-align: center;
        font-size: 14px;
        margin-top: 10px;
    }

    div[data-testid="stExpander"] {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("CỜ VÂY 9x9")
st.markdown(
    '<div class="sub-title">Bạn: <b>⚫ Quân đen</b> &nbsp; | &nbsp; AI: <b>⚪ Quân trắng</b></div>',
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

st.markdown('<div class="game-card">', unsafe_allow_html=True)

for i in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE, gap="small")

    for j in range(BOARD_SIZE):
        cell = st.session_state.board[i][j]

        if cell == BLACK:
            label = "⚫"
        elif cell == WHITE:
            label = "⚪"
        else:
            label = "·"

        disabled = st.session_state.game_over or cell != EMPTY

        with cols[j]:
            if st.button(label, key=f"{i}-{j}", disabled=disabled):
                player_move(i, j)
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="small-guide">Chọn dấu <b>·</b> để đặt quân. Quân đã đánh sẽ không chọn lại được.</div>',
    unsafe_allow_html=True
)

st.divider()

left, right = st.columns(2)

with left:
    st.markdown('<div class="control-btn">', unsafe_allow_html=True)
    if st.button("🔄 Chơi lại"):
        init_game()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="control-btn">', unsafe_allow_html=True)
    if st.button("🏁 Kết thúc & tính điểm"):
        st.session_state.game_over = True
        winner, black_score, white_score = st.session_state.game.get_winner(st.session_state.board)

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

        Trong quá trình tìm kiếm, chương trình dùng **Alpha-Beta Pruning**
        để bỏ qua các nhánh không cần xét, giúp AI chạy nhanh hơn.

        Hàm đánh giá bàn cờ dựa trên:

        - Số quân của mỗi bên
        - Số khí còn lại của nhóm quân
        - Chênh lệch điểm giữa AI và người chơi
        """
    )
