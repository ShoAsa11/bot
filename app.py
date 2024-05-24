
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
st.title("他人には話しづらいけど、誰かに聞いてほしい悩みごと")
st.write("本サービスは試作品です。特定の健康状態にある、またはないことを伝えること、または健康状態の治療または処置の方法について指示を与えることはありません。")


# ---------- サイドバー ----------
y = st.sidebar.slider("今の気分を教えて")
st.sidebar.write(str(y))

st.sidebar.title("相談")
if st.sidebar.button("メンターに相談"):
    st.sidebar.write("メールにて日程調整のご連絡をいたします")
else:
    st.sidebar.write("　")


# ---------- ユーザー種別 ----------
# メインのタイトルを設定
st.title("あなたの立場")

# ボタンの選択肢を定義
options = ["起業家", "社内起業家", "企業ワーカー"]

# ボタンを選択するための選択式のボタンを作成
selected_option = st.selectbox("あなたの立場を選択してください", options)

# 選択された立場ごとに次の質問を表示
if "起業家" in selected_option:
    st.title("質問の例")
    questions = ["責任が重く押しつぶされそうな気持ちになる", "メンバーとうまく同じ絵を共有できない", "自分のビジョンの自信が揺らいできた", "メンバーに弱いところを見せられない"]
    selected_question = st.selectbox("質問を選択してください", questions)
    
elif "社内起業家" in selected_option:
    st.title("質問の例")
    questions = ["検討が同じところをぐるぐる回っている気がする", "価値観・バックグラウンドの違いが大きく、社内の合意形成に長く時間がかかる", "周囲にやりたいことを理解されない", "解決したい課題がふわふわしている"]
    selected_question = st.selectbox("質問を選択してください", questions)
             
elif "企業ワーカー" in selected_option:
    st.title("質問の例")
    questions = ["マネージャーが考えていることについていけない", "今死に物狂いになっていることが自分にとって成長につながっているのか不安", "ロールモデルになるような人がいない", "他人と比較して落ち込む"]
    selected_question = st.selectbox("質問を選択してください", questions)

# ---------- メッセージ ----------
st.title("メッセージを入力してください（事業の方向性、チームメンバー、精神のコントロール、家庭との両立…")
st.text_input("メッセージを入力してください", value=selected_question, key="user_input")

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
