
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは起業家や社内起業家に対して、メンタルケアやコーチングを提供する優秀なカウンセラーです。
相談者の悩みを聞き出すために端的な質問を繰り返してください。

以下のような回答は絶対にしないでください。
* 相手を否定する
* 100文字以上の回答をすること
* 4つ以上の選択肢を出すこと
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content":system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("AI Assistant")
st.write("他人には話しづらいけど、誰かに聞いてほしい悩みごとを教えてください。必要に応じて、メンターなどとの面談を提案します。なお、本サービスは特定の健康状態にある、またはないことを伝えること、または健康状態の治療または処置の方法について指示を与えることはありません。")

# ---------- ボタン ----------
st.title("st.button()")
if st.button("メンターに相談"):
    st.write("メールにて日程調整のご連絡をいたします")
else:
    st.write("　")

# ---------- セレクトボックス ----------
st.title("st.selectbox()")
df_select = pd.DataFrame({
    "feeling": ["☀️", "🌤️", "☁️", "🌧️", "⛈️"]
    })
selected = st.selectbox(
    "いまの気分はどうですか？",
    df_side["feeling"])
st.write("あなたは" + str(selected) + "を選びました！")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
