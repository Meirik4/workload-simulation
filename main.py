import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("📊 72時間以内の仕事処理シミュレーター")

st.write("曜日ごとの処理能力と受注数を設定して、バックログ（未処理案件）の推移を確認できます。")

# --- 入力欄 ---
st.sidebar.header("🗓 曜日ごとの設定")

weekdays = ["月", "火", "水", "木", "金", "土", "日"]

# 曜日ごとの処理能力
st.sidebar.subheader("処理能力（1日あたり）")
capacity_pattern = []
for day in weekdays:
    val = st.sidebar.number_input(f"{day}曜", min_value=0, max_value=200, value=35 if day in ["月", "火", "水"] else (10 if day in ["木", "金"] else 0))
    capacity_pattern.append(val)

# 曜日ごとの受注数
st.sidebar.subheader("受注数（1日あたり）")
inflow_pattern = []
for day in weekdays:
    val = st.sidebar.number_input(f"{day}曜 受注", min_value=0, max_value=200, value=100 if day == "月" else (10 if day == "金" else 0))
    inflow_pattern.append(val)

weeks = st.sidebar.slider("シミュレーション週数", 1, 8, 5)
days = weeks * 7

# --- データ生成 ---
daily_capacity = np.tile(capacity_pattern, weeks)
daily_inflow = np.tile(inflow_pattern, weeks)

# --- バックログ計算 ---
backlog_start = np.zeros(days)
backlog_end = np.zeros(days)
remaining = 0

for i in range(days):
    backlog_start[i] = remaining + daily_inflow[i]
    processed = min(backlog_start[i], daily_capacity[i])
    backlog_end[i] = backlog_start[i] - processed
    remaining = backlog_end[i]

# --- 72時間以内の処理可能量 ---
safe_limit = np.zeros(days)
for i in range(days):
    safe_limit[i] = np.sum(daily_capacity[i:i+3])

# --- グラフ描画 ---
plt.figure(figsize=(10, 5))
plt.plot(backlog_start, marker="o", label="仕事残数（開始時点）", color="blue")
plt.plot(safe_limit, "--", color="red", label="72時間以内の処理可能量")

# 超過部分を赤点でマーク
for i in range(days):
    if backlog_start[i] > safe_limit[i]:
        plt.scatter(i, backlog_start[i], color="red", s=50, zorder=3)

plt.title("72時間以内の仕事処理シミュレーション")
plt.xlabel("日数（0 = 最初の月曜）")
plt.ylabel("仕事量")
plt.legend()
plt.grid(True)
st.pyplot(plt)

# --- 結果メッセージ ---
overdue_days = np.sum(backlog_start > safe_limit)
if overdue_days == 0:
    st.success("🌟 全て72時間以内に処理可能です！")
else:
    st.error(f"⚠️ {overdue_days}日で72時間を超える仕事が発生しています。")
