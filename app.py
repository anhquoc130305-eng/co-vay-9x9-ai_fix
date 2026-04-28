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
    st.session_state.message = "Bạn là X. AI là O. Bạn đi trước."


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
    st.session_state.message = f"AI vừa đánh tại dòng {x}, cột {y}. Đến lượt bạn."


def check_game_over():
    game = st.session_state.game

    if game.is_game_over(st.session_state.board):
        st.session_state.game_over = True
        winner, black_score, white_score = game.get_winner(st.session_state.board)

        if winner == BLACK:
            st.session_state.message = f"Bạn thắng! Điểm bạn: {black_score} - Điểm AI: {white_score}"
        elif winner == WHITE:
            st.session_state.message = f"AI thắng! Điểm bạn: {black_score} - Điểm AI: {white_score}"
        else:
            st.session_state.message = f"Hòa! Điểm bạn: {black_score} - Điểm AI: {white_score}"

        return True
    return False


def player_move(x, y):
    game = st.session_state.game

    if st.session_state.game_over:
        return

    if not game.is_valid_move(st.session_state.board, x, y, BLACK):
        st.session_state.message = "Nước đi không hợp lệ. Hãy chọn vị trí khác."
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
        background: radial-gradient(circle at top, #1f2937 0%, #0f172a 45%, #020617 100%);
        color: #e5e7eb;
    }

    h1 {
        text-align: center;
        color: #f9fafb;
        font-weight: 900;
    }

    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #cbd5e1;
        margin-bottom: 20px;
    }

    [data-testid="stMetric"] {
        background: #111827;
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #334155;
        box-shadow: 0 8px 20px rgba(0,0,0,0.35);
    }

    [data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    div[data-testid="stAlert"] {
        border-radius: 14px;
        background-color: #172554;
        color: #bfdbfe;
        border: 1px solid #2563eb;
    }

    div[data-testid="column"] {
        padding: 0 !important;
    }

    .board-box {
        width: 520px;
        height: 520px;
        margin: 30px auto 10px auto;
        background: #d9a441;
        border: 16px solid #7c4a12;
        border-radius: 14px;
        box-shadow: 0 22px 45px rgba(0,0,0,0.55);
        position: relative;
    }

    .board-lines {
        position: absolute;
        inset: 42px;
        background-image:
            linear-gradient(to right, #1f1305 2px, transparent 2px),
            linear-gradient(to bottom, #1f1305 2px, transparent 2px);
        background-size: 54px 54px;
        background-position: 0 0;
        width: 432px;
        height: 432px;
    }

    .board-buttons {
        width: 520px;
        margin: -530px auto 35px auto;
        position: relative;
        z-index: 10;
    }

    .board-buttons .stButton > button {
        width: 42px !important;
        height: 42px !important;
        min-width: 42px !important;
        min-height: 42px !important;
        padding: 0 !important;
        margin: 0 !important;
        border-radius: 50% !important;
        border: none !important;
        background: transparent !important;
        color: transparent !important;
        box-shadow: none !important;
    }

    .board-buttons .stButton > button:hover {
        background: rgba(255,255,255,0.25) !important;
        border: 1px dashed rgba(0,0,0,0.4) !important;
    }

    .board-buttons .stButton > button:disabled {
        opacity: 1 !important;
    }

    .board-buttons .stButton > button p {
        font-size: 28px !important;
        line-height: 1 !important;
        margin: 0 !important;
    }

    .board-buttons .stButton > button:disabled p {
        opacity: 1 !important;
    }

    .black-stone {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 25%, #777, #050505 72%);
        box-shadow: 3px 4px 10px rgba(0,0,0,0.55);
        margin: auto;
    }

    .white-stone {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 25%, #ffffff, #d1d5db 75%);
        box-shadow: 3px 4px 10px rgba(0,0,0,0.35);
        margin: auto;
    }

    .empty-point {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #1f1305;
        margin: auto;
        opacity: 0.9;
    }

    .control button {
        width: 100% !important;
        height: 48px !important;
        border-radius: 12px !important;
        background: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("CỜ VÂY 9x9 - AI MINIMAX ALPHA-BETA")
st.markdown('<div class="sub-title">Người chơi: <b>X</b> | AI: <b>O</b></div>', unsafe_allow_html=True)

black_score, white_score = st.session_state.game.calculate_score(st.session_state.board)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Điểm người chơi", black_score)
with col2:
    st.metric("Điểm AI", white_score)
with col3:
    st.metric("Kích thước", "9x9")

st.info(st.session_state.message)

st.markdown('<div class="board-box"><div class="board-lines"></div></div>', unsafe_allow_html=True)
st.markdown('<div class="board-buttons">', unsafe_allow_html=True)

for i in range(BOARD_SIZE):
    left_space, *cols, right_space = st.columns([0.18] + [1] * BOARD_SIZE + [0.18], gap="small")

    for j in range(BOARD_SIZE):
        cell = st.session_state.board[i][j]

        if cell == BLACK:
            label = "●"
        elif cell == WHITE:
            label = "○"
        else:
            label = "·"

        disabled = st.session_state.game_over or cell != EMPTY

        with cols[j]:
            if st.button(label, key=f"{i}-{j}", disabled=disabled):
                player_move(i, j)
                st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

st.divider()

st.markdown('<div class="control">', unsafe_allow_html=True)
left, right = st.columns(2)

with left:
    if st.button("🔄 Chơi lại"):
        init_game()
        st.rerun()

with right:
    if st.button("🏁 Kết thúc & tính điểm"):
        st.session_state.game_over = True
        winner, black_score, white_score = st.session_state.game.get_winner(st.session_state.board)

        if winner == BLACK:
            st.session_state.message = f"Bạn thắng! Điểm bạn: {black_score} - Điểm AI: {white_score}"
        elif winner == WHITE:
            st.session_state.message = f"AI thắng! Điểm bạn: {black_score} - Điểm AI: {white_score}"
        else:
            st.session_state.message = f"Hòa! Điểm bạn: {black_score} - Điểm AI: {white_score}"

        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

with st.expander("Giải thích thuật toán"):
    st.write(
        """
        AI sử dụng thuật toán **Minimax** để giả lập các nước đi có thể xảy ra.

        Trong quá trình tìm kiếm, chương trình dùng **Alpha-Beta Pruning**
        để loại bỏ những nhánh không cần xét, giúp AI tìm nước đi nhanh hơn.

        Hàm heuristic đánh giá trạng thái bàn cờ dựa trên:

        - Số quân trong nhóm
        - Số khí còn lại của nhóm quân
        - Chênh lệch điểm giữa AI và người chơi
        """
    )
