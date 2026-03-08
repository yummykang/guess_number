import streamlit as st
import random

# 初始化游戏状态
if 'secret' not in st.session_state:
    st.session_state.secret = "".join(random.choices("0123456789", k=4))
    st.session_state.logs = []

st.title("🔢 4位数字对战机")

# 用户猜测区域
user_input = st.text_input("输入你的猜测 (4位数字):", max_chars=4)
if st.button("提交猜测"):
    if len(user_input) == 4:
        # 计算匹配
        matches = sum(1 for a, b in zip(st.session_state.secret, user_input) if a == b)
        st.session_state.logs.append(f"你猜 {user_input}：中了 {matches} 个")
        if matches == 4:
            st.success("🎉 你赢了！")
    else:
        st.error("请输入4位数字！")

# 显示历史记录
for log in reversed(st.session_state.logs):
    st.text(log)

if st.button("重新开始"):
    del st.session_state.secret
    st.rerun()