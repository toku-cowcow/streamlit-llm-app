import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# 環境変数を読み込み
load_dotenv()

# LLMクライアントの初期化
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

def get_expert_response(user_input, expert_type):
    """
    入力テキストと専門家タイプを受け取り、LLMからの回答を返す関数
    
    Args:
        user_input (str): ユーザーからの入力テキスト
        expert_type (str): 選択された専門家のタイプ
    
    Returns:
        str: LLMからの回答
    """
    # 専門家タイプに応じてシステムメッセージを設定
    expert_prompts = {
        "医療専門家": "あなたは経験豊富な医療専門家です。医学的知識に基づいて、正確で分かりやすい回答を提供してください。ただし、診断や治療の推奨は行わず、必要に応じて医療機関への相談を促してください。",
        "IT技術者": "あなたは経験豊富なIT技術者です。プログラミング、システム開発、インフラ構築などの技術的な質問に対して、実践的で具体的な回答を提供してください。コード例やベストプラクティスも含めて説明してください。",
        "料理専門家": "あなたは料理のプロフェッショナルです。レシピ、調理法、食材の知識、栄養についての質問に対して、実用的で美味しい料理を作るためのアドバイスを提供してください。",
        "法律相談": "あなたは法律の専門家です。法的な質問に対して、正確で理解しやすい回答を提供してください。ただし、具体的な法的アドバイスは行わず、必要に応じて専門の法律家への相談を促してください。"
    }
    
    system_prompt = expert_prompts.get(expert_type, "あなたは親切で知識豊富なアシスタントです。")
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]
    
    try:
        result = llm(messages)
        return result.content
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# Streamlitアプリのメイン部分
st.title("🤖 AI専門家相談アプリ")

st.write("##### このアプリについて")
st.write("このアプリでは、様々な分野の専門家AIに質問することができます。")
st.write("専門家を選択し、質問を入力して「相談する」ボタンを押すと、選択した専門家の観点からAIが回答します。")

st.write("##### 操作方法")
st.write("1. 下のラジオボタンから相談したい専門家を選択してください")
st.write("2. テキストボックスに質問や相談内容を入力してください")
st.write("3. 「相談する」ボタンを押すと、AIが専門家として回答します")

st.divider()

# 専門家選択のラジオボタン
selected_expert = st.radio(
    "相談したい専門家を選択してください：",
    ["医療専門家", "IT技術者", "料理専門家", "法律相談"]
)

# 選択された専門家の説明を表示
expert_descriptions = {
    "医療専門家": "💊 医学的な質問や健康に関する相談にお答えします",
    "IT技術者": "💻 プログラミングや技術的な問題解決をサポートします", 
    "料理専門家": "👨‍🍳 レシピや調理法、食材についてアドバイスします",
    "法律相談": "⚖️ 法律に関する一般的な質問にお答えします"
}

st.write(f"**選択中**: {expert_descriptions[selected_expert]}")

st.divider()

# ユーザー入力フォーム
user_question = st.text_area(
    label=f"{selected_expert}への質問・相談内容を入力してください：",
    height=100,
    placeholder="こちらに質問や相談したい内容を詳しく入力してください..."
)

# 相談ボタン
if st.button("🔍 相談する", type="primary"):
    if user_question.strip():
        st.divider()
        
        # 回答を取得中の表示
        with st.spinner(f"{selected_expert}が回答を準備中..."):
            response = get_expert_response(user_question, selected_expert)
        
        # 回答を表示
        st.write("### 💡 回答")
        st.write(f"**{selected_expert}からの回答：**")
        st.write(response)
        
        # 注意事項の表示
        st.divider()
        st.write("⚠️ **注意事項**")
        st.write("- この回答は AI によるものであり、専門的な診断や法的アドバイスを意図したものではありません")
        st.write("- 重要な決定を行う際は、必ず関連分野の専門家にご相談ください")
        
    else:
        st.error("質問内容を入力してから「相談する」ボタンを押してください。")

# サイドバーに追加情報
st.sidebar.write("### 📋 利用可能な専門家")
st.sidebar.write("**医療専門家** - 健康・医学関連")
st.sidebar.write("**IT技術者** - プログラミング・技術")  
st.sidebar.write("**料理専門家** - レシピ・調理法")
st.sidebar.write("**法律相談** - 法的な質問")

st.sidebar.divider()
st.sidebar.write("### ⚙️ 使用技術")
st.sidebar.write("- Streamlit")
st.sidebar.write("- LangChain")
st.sidebar.write("- OpenAI GPT-4o-mini")