import streamlit as st

def apply_custom_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background: radial-gradient(circle at top, #0f172a 0%, #111827 28%, #0f172a 60%, #111827 100%);
            color: #f8fafc;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }
        .hero-card {
            background: rgba(15, 23, 42, 0.92);
            border: 1px solid rgba(56, 189, 248, 0.18);
            border-radius: 1.6rem;
            padding: 1.8rem 2rem;
            margin-bottom: 1.7rem;
            box-shadow: 0 20px 50px rgba(15, 23, 42, 0.28);
        }
        .hero-card-title {
            font-size: 2.4rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            color: #ffffff;
            margin: 0 0 0.5rem 0;
        }
        .hero-card-copy {
            font-size: 1rem;
            color: #cbd5e1;
            line-height: 1.8;
            margin: 0;
        }
        .hero-card strong { color: #38bdf8; }
        .login-box {
            background: rgba(15, 23, 42, 0.95);
            padding: 2rem 1.9rem;
            border-radius: 1.6rem;
            border: 1px solid rgba(96, 165, 250, 0.20);
            box-shadow: 0 20px 40px rgba(15, 23, 42, 0.30);
            margin-top: 1rem;
        }
        .login-title { color: #f8fafc; font-size: 2.4rem; font-weight: 900; margin: 0; }
        .login-cta { color: #e2e8f0; font-size: 1.05rem; margin: 0; line-height: 1.75; }
        .login-pill {
            display: inline-block;
            background: rgba(59, 130, 246, 0.24);
            color: #bfdbfe;
            padding: 0.55rem 1rem;
            border-radius: 999px;
            font-size: 0.9rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            margin-bottom: 1rem;
        }
        .stTextInput>div>div>input {
            background: rgba(30, 41,slate, 0.96) !important;
            border: 1px solid rgba(96, 165, 250, 0.20) !important;
            border-radius: 1rem !important;
            color: #f8fafc !important;
        }
        .stButton>button {
            background: linear-gradient(135deg, #fb7185 0%, #f97316 100%) !important;
            color: #ffffff !important;
            border-radius: 1rem !important;
            font-weight: 800 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )