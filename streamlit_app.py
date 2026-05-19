import os
import subprocess
import streamlit as st
import threading

# 设置页面
st.set_page_config(page_title="Honey", layout="wide")

st.title("successfully")

# 控制状态
if "running" not in st.session_state:
    st.session_state.running = False
if "auto_started" not in st.session_state:
    st.session_state.auto_started = False

# 日志缓冲
log_buffer = []

def run_backend():
    try:
        log_buffer.append("📦 开始安装依赖和启动服务...")
        subprocess.run("chmod +x app.py", shell=True, check=True)
        subprocess.run("pip install -r requirements.txt", shell=True, check=True)
        subprocess.Popen(["python", "app.py"])
        log_buffer.append("✅ 部署完成，服务已启动")
    except Exception as e:
        log_buffer.append(f"❌ 出错: {e}")
    finally:
        st.session_state.running = False
        st.session_state.auto_started = True
        with open("/tmp/deployed.flag", "w") as f:
            f.write("done")

# 自动部署
if not os.path.exists("/tmp/deployed.flag") and not st.session_state.running:
    threading.Thread(target=run_backend, daemon=True).start()
    st.info("🚀 正在自动部署，请稍候...")

# 手动触发按钮
if st.button("重新部署"):
    if not st.session_state.running:
        log_buffer.clear()
        threading.Thread(target=run_backend, daemon=True).start()
        st.success("✅ 已开始执行部署任务")
    else:
        st.warning("⚠️ 部署任务已在运行中")

# 显示日志
if log_buffer:
    st.text_area("📄 部署日志输出", value="\n".join(log_buffer), height=300)

# 显示自己的静态网页 index.html
index_path = "index.html"
if os.path.exists(index_path):
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=800, scrolling=True)
else:
    st.warning("⚠️ index.html 文件未找到，请放在当前目录下")
