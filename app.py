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
        background: #f7f0df;
    }

    h1 {
        text-align: center;
        color: #1f2937;
        font-weight: 800;
    }

    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #374151;
        margin-bottom: 20px;
    }

    [data-testid="stMetric"] {
        background-color: #fffaf0;
        padding: 16px;
        border-radius: 14px;
        border: 1px solid #e0c38a;
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
        background-color: #fff7dc;
        color: #5c3b00;
        border: 1px solid #d6ad60;
    }

    div[data-testid="column"] {
        padding: 0 !important;
    }

    .board-wrap {
        width: 504px;
        height: 504px;
        margin: 28px auto;
        background-color: #d9a441;
        border: 14px solid #8b5a1e;
        border-radius: 10px;
        box-shadow: 0 12px 28px rgba(0,0,0,0.25);
        position: relative;
        padding: 0;
    }

    .board-wrap::before {
        content: "";
        position: absolute;
        left: 31px;
        top: 31px;
        width: 440px;
        height: 440px;
        background-image:
            linear-gradient(to right, #2b1a08 2px, transparent 2px),
            linear-gradient(to bottom, #2b1a08 2px, transparent 2px);
        background-size: 55px 55px;
        background-position: 0 0;
        pointer-events: none;
    }

    .board-area {
        position: relative;
        z-index: 2;
        width: 504px;
        height: 504px;
        display: grid;
        grid-template-columns: repeat(9, 56px);
        grid-template-rows: repeat(9, 56px);
    }

    .stone-button {
        width: 56px;
        height: 56px;
    }

    div.stButton > button {
        width: 56px;
        height: 56px;
        padding: 0 !important;
        margin: 0 !important;
        border-radius: 50%;
        border: none;
        background-color: transparent;
        color: transparent;
        box-shadow: none;
        font-size: 0;
    }

    div.stButton > button:hover {
        background-color: rgba(255,255,255,0.22);
        border-radius: 50%;
        border: 1px dashed rgba(0,0,0,0.35);
    }

    div.stButton > button:disabled {
        opacity: 1 !important;
        background-color: transparent;
        border: none;
    }

    div.stButton > button p {
        font-size: 28px !important;
        line-height: 1 !important;
        margin: 0 !important;
        color: inherit !important;
    }

    div.stButton > button:disabled p {
        opacity: 1 !important;
    }

    button:has(p:contains("⚫")) {
        background: radial-gradient(circle at 30% 30%, #666, #111 70%) !important;
        color: transparent !important;
        box-shadow: 2px 3px 8px rgba(0,0,0,0.45) !important;
    }

    button:has(p:contains("⚪")) {
        background: radial-gradient(circle at 30% 30%, #ffffff, #d8d8d8 75%) !important;
        color: transparent !important;
        box-shadow: 2px 3px 8px rgba(0,0,0,0.28) !important;
    }

    .control-btn {
        text-align: center;
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

st.markdown('<div class="board-wrap"><div class="board-area">', unsafe_allow_html=True)

for i in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE, gap="small")

    for j in range(BOARD_SIZE):
        cell = st.session_state.board[i][j]

        if cell == BLACK:
            label = "⚫"
        elif cell == WHITE:
            label = "⚪"
        else:
            label = " "

        disabled = st.session_state.game_over or cell != EMPTY

        with cols[j]:
            if st.button(label, key=f"{i}-{j}", disabled=disabled):
                player_move(i, j)
                st.rerun()

st.markdown("</div></div>", unsafe_allow_html=True)

st.divider()

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
