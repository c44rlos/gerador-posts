# app.py — Gerador de Postagens (Variação 2) no Streamlit
# Gera apenas o TEXTO formatado, sem abrir navegador ou enviar.

import re
import streamlit as st

# ======================= Utilidades =======================
TITULO_PADRAO = "CAED OFERTAS"

def brl(value: float) -> str:
    inteiro, decimal = f"{value:,.2f}".split(".")
    inteiro = inteiro.replace(",", ".")
    return f"R$ {inteiro},{decimal}"

def to_float(num_str: str) -> float:
    s = (num_str or "").strip()
    if not s:
        return 0.0
    s = re.sub(r"[^\d,\.]", "", s)
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    return float(s or 0)

def pct_desconto(de: float, por: float) -> int:
    if de <= 0 or por <= 0 or por >= de:
        return 0
    return round((1 - por / de) * 100)

def bold_wpp(txt: str) -> str:
    return txt if (txt.startswith("*") and txt.endswith("*")) else f"*{txt}*"

def strike_wpp(txt: str) -> str:
    return f"~~{txt}~~"

def gerar_postagem(titulo: str, nome: str, por: float, link: str, de: float = 0.0) -> str:
    titulo_fmt = (titulo or "").strip() or TITULO_PADRAO
    linhas = [
        bold_wpp(titulo_fmt),
        "",  # espaçamento depois do título
        bold_wpp(f"💥 {nome}")
    ]
    if de > por and de > 0:
        de_fmt = brl(de)
        por_fmt = brl(por)
        off = pct_desconto(de, por)
        linhas += [
            "",
            f"❌ De {strike_wpp(de_fmt)}",
            bold_wpp(f"🔥 Por {por_fmt}" + (f" ({off}% OFF)" if off > 0 else "")),
        ]
    else:
        linhas.append(bold_wpp(f"🔥 Oferta: {brl(por)}"))
    linhas.append(bold_wpp("👉 Compre aqui:") + f" {link}")
    return "\n".join(linhas)

# ======================= UI (Streamlit) =======================
st.set_page_config(page_title="Gerador de Postagens", page_icon="📝", layout="centered")
st.title("📝 Gerador de Postagens (WhatsApp) — Variação 2")

with st.form("form_post"):
    titulo = st.text_input("Título (padrão: CAED OFERTAS)", placeholder="CAED OFERTAS")
    nome = st.text_input("Nome do produto", placeholder="Ex.: TV 50\" 4K")
    col_de, col_por = st.columns(2)
    with col_de:
        preco_de_str = st.text_input("Preço DE (opcional)", placeholder="Ex.: 3.499,90")
    with col_por:
        preco_por_str = st.text_input("Preço POR", placeholder="Ex.: 2.199,90")
    link = st.text_input("Link do produto", placeholder="https://...")

    gerar_btn = st.form_submit_button("Gerar postagem")

if gerar_btn:
    try:
        preco_por = to_float(preco_por_str)
    except Exception:
        st.error("Preço POR inválido.")
        st.stop()
    preco_de = to_float(preco_de_str) if preco_de_str else 0.0

    if not nome or not link or preco_por <= 0:
        st.error("Preencha: Nome, Preço POR (>0) e Link.")
        st.stop()

    postagem = gerar_postagem(titulo, nome, preco_por, link, de=preco_de)

    st.success("Postagem gerada!")
    st.text_area("Copie e cole no WhatsApp:", value=postagem, height=250)
