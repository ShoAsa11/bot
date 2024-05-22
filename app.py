
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは起業家や社内起業家に対して、メンタルケアやコーチングを提供する優秀なカウンセラーです。
以下の観点で回答をしてください。
* 新しい気づきをもたらす
* 視点を増やす
* 考え方や行動の選択肢を増やす
* 目標達成に必要な行動を促進する

また、あなたの役割はカウンセリングなので、相手に負荷を与えるような以下のような回答は絶対に答えないでください。
* 相手を否定する
* 100文字以上の回答
* 状況の理解や、対処方法を断定する

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
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("AI Assistant")
st.write("""
他人には話しづらいけど、誰かに聞いてほしい悩みごとを教えてください。
必要に応じて、メンターなどとの面談を提案します。
なお、本サービスは特定の健康状態にある、またはないことを伝えること、または健康状態の治療または処置の方法について指示を与えることはありません。
"""
)

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
