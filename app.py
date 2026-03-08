import streamlit as st
import random
import itertools

# --- 核心逻辑函数 ---
def count_matches(s1, s2):
    return sum(1 for a, b in zip(s1, s2) if a == b)

# --- 初始化状态 ---
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.player_secret = "" # 你的秘密数字（电脑要猜的）
    st.session_state.ai_secret = "".join(random.choices("0123456789", k=4))
    st.session_state.possible_codes = [''.join(p) for p in itertools.product("0123456789", repeat=4)]
    st.session_state.player_logs = []
    st.session_state.ai_logs = []
    st.session_state.game_over = False

st.set_page_config(page_title="数字对战中心", layout="wide")
st.title("🤖 4位数字：人机对决")
st.caption("规则：数字和位置都对上才算中。谁先猜到对方的4位数字谁赢！")

# --- 侧边栏：操作区 ---
with st.sidebar:
    st.header("游戏控制")
    if st.button("🔄 开启新对局", use_container_width=True):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
    
    st.divider()
    st.info(f"AI 剩余可能组合：{len(st.session_state.possible_codes)} 个")

# --- 主界面布局 ---
col1, col2 = st.columns(2)

# --- 左列：玩家回合 ---
with col1:
    st.subheader("🤺 你的进攻")
    user_guess = st.text_input("输入你的猜测 (4位):", key="u_input", max_chars=4)
    if st.button("发射猜测 🚀") and not st.session_state.game_over:
        if len(user_guess) == 4 and user_guess.isdigit():
            score = count_matches(st.session_state.ai_secret, user_guess)
            st.session_state.player_logs.insert(0, f"你猜 `{user_guess}` → **中 {score} 个**")
            if score == 4:
                st.balloons()
                st.success("🎉 你先赢了！电脑的数字就是 " + user_guess)
                st.session_state.game_over = True
        else:
            st.warning("请输入合法的4位数字")
    
    for log in st.session_state.player_logs:
        st.write(log)

# --- 右列：电脑回合 ---
with col2:
    st.subheader("💻 AI 的反击")
    if not st.session_state.game_over and st.session_state.possible_codes:
        # 电脑选一个猜测
        if 'current_ai_guess' not in st.session_state:
            st.session_state.current_ai_guess = random.choice(st.session_state.possible_codes)
        
        curr_guess = st.session_state.current_ai_guess
        st.chat_message("assistant").write(f"我猜你的数字是：**{curr_guess}**")
        
        st.write("请诚实告诉我，我猜中了几个位置？")
        # 按钮横向排列
        btn_cols = st.columns(5)
        for i in range(5):
            if btn_cols[i].button(str(i), key=f"btn_{i}"):
                if i == 4:
                    st.error(f"💀 AI 赢了！它识破了你的数字：{curr_guess}")
                    st.session_state.game_over = True
                else:
                    # 逻辑过滤
                    st.session_state.possible_codes = [
                        p for p in st.session_state.possible_codes 
                        if count_matches(p, curr_guess) == i
                    ]
                    st.session_state.ai_logs.insert(0, f"AI 猜 `{curr_guess}` → 你说中 {i} 个")
                    # 准备下一次猜测
                    if st.session_state.possible_codes:
                        st.session_state.current_ai_guess = random.choice(st.session_state.possible_codes)
                    st.rerun()

    for log in st.session_state.ai_logs:
        st.write(log)

if not st.session_state.possible_codes and not st.session_state.game_over:
    st.error("AI 发现你在撒谎！没有符合条件的数字了。")