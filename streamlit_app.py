import os
import subprocess
import streamlit as st
import threading
import asyncio

# 设置页面
st.set_page_config(page_title="Honey", layout="wide")

# 全局日志变量（线程安全）
log_buffer = []

# UI 控制状态
if "running" not in st.session_state:
    st.session_state.running = False
if "auto_started" not in st.session_state:
    st.session_state.auto_started = False  # 控制是否已自动执行完

st.title("successfully")


def run_backend():
    try:
        log_buffer.append("📦 开始安装依赖和启动服务...")
        subprocess.run("chmod +x app.py", shell=True, check=True)

        subprocess.Popen(["python", "app.py"])
        log_buffer.append("✅ 部署完成，服务已启动")
    except Exception as e:
        log_buffer.append(f"❌ 出错: {e}")
    finally:
        st.session_state.running = False
        st.session_state.auto_started = True
        with open("/tmp/deployed.flag", "w") as f:
            f.write("done")


async def main():
    st.session_state.running = True
    run_backend()


if not os.path.exists("/tmp/deployed.flag") and not st.session_state.running:
    def auto_start():
        asyncio.run(main())
    threading.Thread(target=auto_start, daemon=True).start()
    st.info("🚀 正在自动部署，请稍候...")


if st.button("get this app back up"):
    if not st.session_state.running:
        log_buffer.clear()
        threading.Thread(target=lambda: asyncio.run(main()), daemon=True).start()
        st.success("✅ 已开始执行部署任务")
    else:
        st.warning("⚠️ 部署任务已在运行中")


if log_buffer:
    st.text_area("📄 部署日志输出", value="\n".join(log_buffer), height=300)


video_paths = ""
for path in video_paths:
    if os.path.exists(path):
        st.video(path)


image_path = ""
if os.path.exists(image_path):
    st.image(image_path, caption="歌曲", use_container_width=True)
