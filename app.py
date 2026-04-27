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
        background: linear-gradient(135deg, #fff8ec, #eef6ff);
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
        background-color: white;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
        background-color: #e8f2ff;
        color: #0f4c81;
        border: 1px solid #b6d7ff;
    }

    div.stButton > button {
        width: 52px;
        height: 52px;
        padding: 0px;
        font-size: 22px;
        font-weight: bold;
        border-radius: 10px;
        background-color: #f7dfaa;
        color: #111827;
        border: 1px solid #d6ad60;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        transition: 0.2s;
    }

    div.stButton > button:hover {
        background-color: #e9c46a;
        border: 1px solid #b7791f;
        color: #111827;
        transform: scale(1.03);
    }

    div.stButton > button:disabled {
        background-color: #f5deb3;
        color: #111827;
        opacity: 1;
        border: 1px solid #d6ad60;
    }

    .stButton button p {
        font-size: 22px;
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


for i in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE)

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


st.divider()

left, right = st.columns(2)

with left:
    if st.button("🔄"):
        init_game()
        st.rerun()
    st.caption("Chơi lại")

with right:
    if st.button("🏁"):
        st.session_state.game_over = True
        winner, black_score, white_score = st.session_state.game.get_winner(st.session_state.board)

        if winner == BLACK:
            st.session_state.message = f"Bạn thắng! Điểm bạn: {black_score} - Điểm AI: {white_score}"
        elif winner == WHITE:
            st.session_state.message = f"AI thắng! Điểm bạn: {black_score} - Điểm AI: {white_score}"
        else:
            st.session_state.message = f"Hòa! Điểm bạn: {black_score} - Điểm AI: {white_score}"

        st.rerun()
    st.caption("Kết thúc & tính điểm")


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
