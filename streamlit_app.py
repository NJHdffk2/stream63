import os
import subprocess
import streamlit as st
import threading

# 页面设置
st.set_page_config(page_title="Honey", layout="wide")

# 防止重复启动
if "started" not in st.session_state:
    st.session_state.started = False


def run_backend():
    try:
        subprocess.run(
            "pip install -r requirements.txt",
            shell=True,
            check=True
        )

        subprocess.Popen(["python", "app.py"])

        # 创建标记文件
        with open("/tmp/deployed.flag", "w") as f:
            f.write("done")

    except Exception as e:
        print("启动失败:", e)


# 自动启动（仅一次）
if (
    not os.path.exists("/tmp/deployed.flag")
    and not st.session_state.started
):
    st.session_state.started = True
    threading.Thread(target=run_backend, daemon=True).start()


# 显示 index.html
index_path = "index.html"

if os.path.exists(index_path):
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    st.components.v1.html(
        html_content,
        height=800,
        scrolling=True
    )
else:
    st.error("index.html 文件不存在")
