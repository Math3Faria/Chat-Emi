import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import base64

# --- CRITICAL: ALL IMPORTS AND NON-STREAMLIT CONFIGURATION FIRST ---
load_dotenv() # Carrega as variáveis de ambiente (como GEMINI_API_KEY)

# --- CONFIGURAÇÕES DA PÁGINA ---
ASSISTANT_NAME = "CHAT EMI"
USER_AVATAR_EMOJI = "👤"

ASSISTANT_AVATAR_IMAGE_PATH = "nctech_avatar.png"
BACKGROUND_IMAGE_PATH = "background_blur_ai.jpg"

LOGO_EMI_PATH = "logo_emi.png"
LOGO_EMS_FOOTER_PATH = "logo_ems.png"
LOGO_NCTECH_FOOTER_PATH = "logo_nctech.png"
LOGO_GRUPONC_FOOTER_PATH = "logo_gruponc.png"

# --- Perguntas e Respostas Fixas (FAQs) ---
FAQ_QUESTIONS_ANSWERS = {
    "Qual é o código de ética da EMS?": "O Código de Ética da EMS estabelece os princípios e valores que devem guiar a conduta de todos os colaboradores, parceiros e fornecedores, visando a integridade, transparência e responsabilidade social. Ele aborda temas como combate à corrupção, conflito de interesses e proteção de informações confidenciais.",
    "Como faço para denunciar uma conduta indevida?": "Denúncias de conduta indevida podem ser feitas através do Canal de Denúncias da EMS, disponível no site oficial da empresa ou por telefone. As denúncias podem ser anônimas e são tratadas com confidencialidade para garantir a segurança do denunciante.",
    "Quais são as políticas de compliance da EMS?": "As políticas de compliance da EMS englobam diversas diretrizes para assegurar que a empresa atue em conformidade com as leis, regulamentos e padrões éticos. Isso inclui políticas anticorrupção, de privacidade de dados, de concorrência leal e de segurança do trabalho.",
    "Onde posso encontrar o manual de conduta?": "O manual de conduta está disponível na intranet da EMS, na seção de 'Documentos Corporativos'. Caso não tenha acesso, entre em contato com o departamento de Recursos Humanos ou Compliance para obter uma cópia."
}

def get_image_data_uri_safe(image_path, fallback_value):
    if not os.path.exists(image_path):
        return fallback_value
    try:
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/png;base64,{encoded}"
    except Exception as e:
        print(f"Erro ao carregar a imagem '{image_path}': {e}")
        return fallback_value

assistant_avatar_data_uri = get_image_data_uri_safe(ASSISTANT_AVATAR_IMAGE_PATH, None)
logo_emi_data_uri = get_image_data_uri_safe(LOGO_EMI_PATH, None)
logo_ems_footer_data_uri = get_image_data_uri_safe(LOGO_EMS_FOOTER_PATH, None)
logo_nctech_footer_data_uri = get_image_data_uri_safe(LOGO_NCTECH_FOOTER_PATH, None)
logo_gruponc_footer_data_uri = get_image_data_uri_safe(LOGO_GRUPONC_FOOTER_PATH, None)

if assistant_avatar_data_uri:
    ASSISTANT_PAGE_ICON = assistant_avatar_data_uri
else:
    ASSISTANT_PAGE_ICON = "🌍"

st.set_page_config(
    page_title=ASSISTANT_NAME,
    page_icon=ASSISTANT_PAGE_ICON,
    layout="centered",
    initial_sidebar_state="collapsed"
)

if assistant_avatar_data_uri:
    ASSISTANT_CHAT_AVATAR = assistant_avatar_data_uri
else:
    ASSISTANT_CHAT_AVATAR = "🌍"
    st.warning(f"A imagem do avatar do assistente '{ASSISTANT_AVATAR_IMAGE_PATH}' não foi encontrada. Usando emoji padrão.")

def get_base64_for_html(data_uri, path_name):
    if data_uri:
        return data_uri.split(',')[1]
    else:
        st.warning(f"A imagem da logo '{path_name}' não foi encontrada. O logo pode não aparecer.")
        return ""

logo_emi_base64_for_html = get_base64_for_html(logo_emi_data_uri, LOGO_EMI_PATH)
logo_ems_footer_base64_for_html = get_base64_for_html(logo_ems_footer_data_uri, LOGO_EMS_FOOTER_PATH)
logo_nctech_footer_base64_for_html = get_base64_for_html(logo_nctech_footer_data_uri, LOGO_NCTECH_FOOTER_PATH)
logo_gruponc_footer_base64_for_html = get_base64_for_html(logo_gruponc_footer_data_uri, LOGO_GRUPONC_FOOTER_PATH)

def get_api_key():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("🚨 Erro Crítico: A variável de ambiente GEMINI_API_KEY não foi definida! Verifique seu arquivo .env ou as configurações de ambiente.")
        st.stop()
    return api_key

def set_background(image_path):
    if not os.path.exists(image_path):
        st.warning(f"A imagem de fundo '{image_path}' não foi encontrada. O fundo padrão será usado.")
        return
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def apply_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

        body {
            font-family: 'Roboto', sans-serif;
            color: #333;
        }

        /* Container Principal do Chat - Agora transparente */
        .block-container {
            max-width: 700px !important;
            padding: 1.5rem !important; /* REDUZIDO: de 2rem para 1.5rem */
            background-color: rgba(255, 255, 255, 0.7) !important;
            border-radius: 16px !important;
            box-shadow: 0 10px 40px 0 rgba(0, 86, 145, 0.15) !important;
            backdrop-filter: blur(8px) !important;
            -webkit-backdrop-filter: blur(8px) !important;
            border: 1px solid rgba(0, 86, 145, 0.1) !important;
            margin-top: 1.5rem !important; /* REDUZIDO: de 2rem para 1.5rem */
            margin-bottom: 1.5rem !important; /* REDUZIDO: de 2rem para 1.5rem */
        }

        /* Títulos */
        h2 {
            color: #005691 !important;
            text-align: center !important;
            font-weight: 700 !important;
            margin-bottom: 0.5rem !important;
            letter-spacing: -0.5px !important;
        }
        p.subheader {
            color: #005691 !important;
            text-align: center !important;
            margin-bottom: 1.5rem !important; /* REDUZIDO: de 2rem para 1.5rem */
            font-weight: 400 !important;
            font-size: 1.1em !important;
            opacity: 0.9 !important;
        }

        /* Balões de Mensagem - Fundos mais transparentes */
        .stChatMessage {
            border-radius: 12px !important;
            padding: 16px 20px !important;
            margin-bottom: 10px !important; /* REDUZIDO: de 15px para 10px */
            box-shadow: 0 4px 15px rgba(0,86,145,0.1) !important;
            border: none !important;
            word-wrap: break-word !important;
            line-height: 1.6 !important;
        }

        /* Mensagem do Assistente - Azul claro transparente */
        div[data-testid="stChatMessage"]:has(div.stMarkdown) div.stMarkdown {
            background-color: rgba(224, 242, 247, 0.85) !important;
            color: #263238 !important;
            border-radius: 12px !important;
            padding: 16px 20px !important;
            border-left: 5px solid #005691 !important;
            padding-left: 25px !important;
        }

        /* Mensagem do Usuário - Branco transparente */
        div[data-testid="stChatMessage"]:has(span[data-testid="chatAvatarIcon-user"]) div.stMarkdown {
            background-color: rgba(255, 255, 255, 0.85) !important;
            color: #263238 !important;
            border: 1px solid rgba(0, 86, 145, 0.2) !important;
            border-radius: 12px !important;
            padding: 16px 20px !important;
        }

        /* Área de Input - Totalmente transparente */
        .stChatInputContainer {
            background-color: transparent !important;
            border-top: 1px solid rgba(0, 86, 145, 0.1) !important;
            padding-top: 1rem !important; /* REDUZIDO: de 1.5rem para 1rem */
            margin-top: 0.5rem !important; /* REDUZIDO: de 1rem para 0.5rem */
        }

        /* Campo de Input - Fundo transparente */
        .stTextInput > div > div > input {
            border-radius: 25px !important;
            padding: 12px 20px !important;
            border: 1px solid #005691 !important;
            background-color: rgba(255, 255, 255, 0.8) !important;
            box-shadow: 0 2px 8px rgba(0,86,145,0.1) !important;
            font-size: 1.05em !important;
            color: #333 !important;
        }

        /* Botão de enviar - Mantém o azul EMS */
        button[title="Send"] {
            background-color: #005691 !important;
            color: white !important;
            border-radius: 50% !important;
            width: 45px !important;
            height: 45px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            box-shadow: 0 4px 10px rgba(0,86,145,0.2) !important;
            transition: background-color 0.3s ease !important;
        }

        button[title="Send"]:hover {
            background-color: #003F6E !important;
        }
        .header-container {
            text-align: center;
            margin-bottom: 0.5rem; /* REDUZIDO: de 1rem para 0.5rem */
            padding-top: 0.5rem; /* REDUZIDO: de 1rem para 0.5rem */
            background-color: transparent !important;
        }

        .main-logo {
            width: 280px; /* REDUZIDO: de 350px para 280px */
            height: auto;
            margin-bottom: 5px; /* REDUZIDO: de 10px para 5px */
        }

        /* ESTA É A PARTE CHAVE PARA AUMENTAR O TAMANHO DO AVATAR NO CHAT! */
        /* Seleciona a imagem dentro do span do avatar do chat e força o tamanho */
        div[data-testid="stChatMessage"] span[data-testid^="chatAvatarIcon-"] img {
            width: 70px !important; /* REDUZIDO: de 90px para 70px */
            height: 70px !important; /* REDUZIDO: de 90px para 70px */
            object-fit: cover;
            border-radius: 50%;
        }

        div[data-testid="stChatMessage"]:has(span[data-testid="chatAvatarIcon-assistant"]),
        div[data-testid="stChatMessage"]:has(span[data-testid="chatAvatarIcon-user"]) {
            background-color: transparent !important;
        }

        .stChatMessage p {
            color: inherit !important;
            margin-bottom: 0 !important;
        }

        /* Ajustes finos para Streamlit - pode remover se causar problemas */
        div.css-fg4pbf,
        div[data-testid="stVerticalBlock"] > div:first-child > div:nth-child(2) {
            padding-top: 0.5rem !important; /* Ajustado */
            padding-bottom: 0.5rem !important; /* Ajustado */
        }

        .main .block-container {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
        }

        /* Estilo para a seção de FAQ */
        .faq-section-title {
            color: #005691 !important;
            text-align: center !important;
            font-weight: 700 !important;
            margin-top: 1.5rem !important; /* REDUZIDO: de 2.5rem para 1.5rem */
            margin-bottom: 0.5rem !important;
            font-size: 1.6em !important; /* LIGEIRAMENTE REDUZIDO: de 1.8em para 1.6em */
            letter-spacing: -0.5px !important;
        }

        .faq-section-description {
            color: #555;
            text-align: center;
            margin-bottom: 1rem; /* REDUZIDO: de 1.5rem para 1rem */
            font-size: 0.95em; /* LIGEIRAMENTE REDUZIDO: de 1em para 0.95em */
            line-height: 1.5;
        }

        .faq-grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); /* REDUZIDO: minmax de 280px para 260px */
            gap: 10px; /* REDUZIDO: de 15px para 10px */
            margin-top: 15px; /* REDUZIDO: de 20px para 15px */
            margin-bottom: 20px; /* REDUZIDO: de 30px para 20px */
            width: 100%;
            max-width: 650px;
        }

        /* NOVO ESTILO PARA OS BOTÕES DE FAQ - AGORA SIMULANDO OS CARTÕES */
        .stButton > button {
            background-color: rgba(255, 255, 255, 0.9) !important;
            border: 1px solid #005691 !important;
            border-radius: 12px !important;
            padding: 12px 15px !important; /* REDUZIDO: de 15px 20px para 12px 15px */
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 12px rgba(0, 86, 145, 0.1) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            min-height: 70px !important; /* REDUZIDO: de 80px para 70px */
            width: 100% !important;
            color: #005691 !important;
            font-weight: 500 !important;
            font-size: 0.9em !important; /* LIGEIRAMENTE REDUZIDO: de 0.95em para 0.9em */
            white-space: normal !important;
            line-height: 1.4 !important;
        }

        .stButton > button:hover {
            background-color: #005691 !important;
            color: white !important;
            transform: translateY(-3px) !important; /* EFEITO SUAVIZADO: de -5px para -3px */
            box-shadow: 0 5px 15px rgba(0, 86, 145, 0.2) !important; /* SOMBRA SUAVIZADA */
        }

        /* Novo estilo para o rodapé de logos */
        .footer-logos-container {
            text-align: center;
            margin-top: 2rem; /* REDUZIDO: de 3rem para 2rem */
            padding-top: 1rem; /* REDUZIDO: de 1.5rem para 1rem */
            border-top: 1px solid rgba(0, 86, 145, 0.1);
            background-color: rgba(0, 0, 0, 0.1);
            border-radius: 0 0 16px 16px;
            padding-bottom: 0.8rem; /* REDUZIDO: de 1rem para 0.8rem */
        }

        .footer-logos-container p {
            color: #005691;
            font-size: 0.85em; /* LIGEIRAMENTE REDUZIDO: de 0.9em para 0.85em */
            margin-bottom: 0.8rem; /* REDUZIDO: de 1rem para 0.8rem */
            font-weight: 500;
        }

        .footer-logos {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px; /* REDUZIDO: de 20px para 15px */
            flex-wrap: wrap;
        }

        .footer-logos img {
            height: 35px; /* REDUZIDO: de 40px para 35px */
            width: auto;
            object-fit: contain;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1)); /* SOMBRA SUAVIZADA */
        }

        </style>
    """, unsafe_allow_html=True)

def main():
    set_background(BACKGROUND_IMAGE_PATH)
    apply_custom_css()

    st.markdown(f"""
        <div class="header-container">
            <img src="data:image/png;base64,{logo_emi_base64_for_html}" class="main-logo">
        </div>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Olá! Estou aqui para ajudar com suas dúvidas sobre governança na empresa EMS. Você pode digitar sua pergunta ou escolher uma das opções abaixo:"}
        ]

    st.markdown("---")
    st.markdown("<h2 class='faq-section-title'>Perguntas Frequentes</h2>", unsafe_allow_html=True)
    st.markdown("<p class='faq-section-description'>Clique em uma das perguntas abaixo para obter uma resposta rápida:</p>", unsafe_allow_html=True)
    
    num_cols = 2
    effective_num_cols = min(num_cols, len(FAQ_QUESTIONS_ANSWERS)) if len(FAQ_QUESTIONS_ANSWERS) > 0 else 1
    cols = st.columns(effective_num_cols)

    faq_questions_list = list(FAQ_QUESTIONS_ANSWERS.keys())
    for i, question in enumerate(faq_questions_list):
        with cols[i % effective_num_cols]: 
            if st.button(question, key=f"faq_btn_{i}"):
                st.session_state.messages.append({"role": "user", "content": question})
                st.session_state.messages.append({"role": "assistant", "content": FAQ_QUESTIONS_ANSWERS[question]})
                st.rerun()

    st.markdown("---")

    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message("assistant", avatar=ASSISTANT_CHAT_AVATAR):
                st.markdown(message["content"])
        else:
            with st.chat_message("user", avatar=USER_AVATAR_EMOJI):
                st.markdown(message["content"])

    prompt = st.chat_input("Digite sua pergunta aqui...")
    if prompt:
        if prompt in FAQ_QUESTIONS_ANSWERS:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar=USER_AVATAR_EMOJI):
                st.markdown(prompt)
            with st.chat_message("assistant", avatar=ASSISTANT_CHAT_AVATAR):
                st.markdown(FAQ_QUESTIONS_ANSWERS[prompt])
            st.session_state.messages.append({"role": "assistant", "content": FAQ_QUESTIONS_ANSWERS[prompt]})
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar=USER_AVATAR_EMOJI):
                st.markdown(prompt)

            with st.chat_message("assistant", avatar=ASSISTANT_CHAT_AVATAR):
                message_placeholder = st.empty()
                message_placeholder.markdown("Digitando... ▌")

                try:
                    api_key = get_api_key()
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash-latest')

                    chat_history_for_api = []
                    for msg in st.session_state.messages:
                        role = "model" if msg["role"] == "assistant" else "user"
                        chat_history_for_api.append({"role": role, "parts": [msg["content"]]})

                    history_context = chat_history_for_api[:-1]
                    chat = model.start_chat(history=history_context)
                    response = chat.send_message(prompt)
                    full_response = response.text

                except Exception as e:
                    full_response = f"Desculpe, ocorreu um erro ao contatar a IA: {str(e)}"
                    st.error(full_response)

                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

    st.markdown(f"""
        <div class="footer-logos-container">
            <p>Empresas Colaboradoras:</p>
            <div class="footer-logos">
                <img src="data:image/png;base64,{logo_ems_footer_base64_for_html}" alt="EMS Logo">
                <img src="data:image/png;base64,{logo_nctech_footer_base64_for_html}" alt="NCTECH Logo">
                <img src="data:image/png;base64,{logo_gruponc_footer_base64_for_html}" alt="GRUPONC Logo">
            </div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()