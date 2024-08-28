import streamlit as st
from datetime import date, timedelta
import os
from PIL import Image
import calendar

# Inicializar o st.session_state para scroll_to_event
if 'scroll_to_event' not in st.session_state:
    st.session_state.scroll_to_event = False

# Função para carregar datas importantes
def carregar_datas_importantes():
    datas = {}
    with open('datas_importantes.txt', 'r') as f:
        for linha in f:
            data_str, descricao = linha.strip().split(',')
            datas[date.fromisoformat(data_str)] = descricao
    return datas

# Carregar datas importantes
datas_importantes = carregar_datas_importantes()

# Configurações iniciais
st.title("Calendário Interativo")

# Função para criar calendário HTML por mês
def criar_calendario_html_por_mes(ano, mes, datas_importantes):
    html_calendario = f"<h3 style='text-align: center;'>{calendar.month_name[mes]} {ano}</h3>"
    html_calendario += "<table style='width:100%; border-collapse: collapse;'>"
    html_calendario += "<tr>"

    # Cabeçalho com os dias da semana
    for dia in ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]:
        html_calendario += f"<th style='border: 1px solid #ddd; padding: 10px; background-color: #f2f2f2;'>{dia}</th>"
    html_calendario += "</tr><tr>"

    # Dias do mês
    primeiro_dia, num_dias = calendar.monthrange(ano, mes)
    dia_atual = date(ano, mes, 1)

    # Adicionar células vazias até o primeiro dia da semana correto
    primeiro_dia = date(ano, mes, 1).weekday()
    dia_da_semana = primeiro_dia % 7
    for _ in range(dia_da_semana):
        html_calendario += "<td></td>"

    num_dias = calendar.monthrange(ano, mes)[1]
    for dia in range(1, num_dias + 1):
        data_atual = date(ano, mes, dia)
        if data_atual in datas_importantes:
            html_calendario += f"<td><button onClick='document.getElementById(\"evento_{data_atual.strftime('%Y-%m-%d')}\").scrollIntoView({{behavior: \"smooth\"}});'>{dia}</button></td>"
        else:
            html_calendario += f"<td>{dia}</td>"

        dia_da_semana = (dia_da_semana + 1) % 7
        if dia_da_semana == 0:
            html_calendario += "</tr><tr>"

    # Adicionar células vazias até o final da semana
    while dia_da_semana != 6:
        html_calendario += "<td></td>"
        dia_da_semana = (dia_da_semana + 1) % 7

    html_calendario += "</tr></table>"
    return html_calendario

# Criar calendário HTML para um intervalo de datas
data_inicio = date(2023, 1, 1)
data_fim = date.today()

html_total = ""
for ano in range(data_inicio.year, data_fim.year + 1):
    for mes in range(1, 13):
        if ano == data_inicio.year and mes < data_inicio.month:
            continue
        if ano == data_fim.year and mes > data_fim.month:
            break
        html_total += criar_calendario_html_por_mes(ano, mes, datas_importantes)

# Mostrar calendário no Streamlit
st.markdown(html_total, unsafe_allow_html=True)

# Mostrar foto e recado quando uma data é clicada
for data, descricao in datas_importantes.items():
    if st.button(f"Mostrar evento de {data.strftime('%d/%m/%Y')}", key=data):
        # Atualiza o estado da sessão para controlar a rolagem
        st.session_state.scroll_to_event = data.strftime('%d/%m/%Y')
        # Adiciona um ancoramento para rolar até a imagem ou vídeo
        st.markdown(f"<div id='evento_{data}'></div>", unsafe_allow_html=True)
        st.write(f"**{data.strftime('%d/%m/%Y')}** - {descricao}")
        data_str = data.strftime('%Y-%m-%d')
        foto_path = f'fotos/{data_str}.jpeg'
        video_path = f'fotos/{data_str}.mp4'
        
        if os.path.exists(foto_path):
            st.image(foto_path, caption=descricao)
        elif os.path.exists(video_path):
            st.video(video_path)
            st.write(descricao)  # Adiciona a legenda abaixo do vídeo
        else:
            st.write("Nenhum arquivo encontrado para esta data.")
            st.write(f"Verifique se o caminho do arquivo está correto: {foto_path} ou {video_path}")

        # JavaScript para rolar a página até o ancoramento
        st.markdown(f"""
            <script>
                var element = document.getElementById('evento_{data}');
                if (element) {{
                    element.scrollIntoView({{behavior: 'smooth'}});
                }}
            </script>
        """, unsafe_allow_html=True)

# Executa o scroll se o botão tiver sido clicado
if st.session_state.scroll_to_event:
    st.markdown(f"""
        <script>
            var element = document.getElementById('evento_{st.session_state.scroll_to_event}');
            if (element) {{
                element.scrollIntoView({{behavior: 'smooth'}});
            }}
        </script>
    """, unsafe_allow_html=True)
    # Reseta o estado para evitar múltiplos scrolls
    st.session_state.scroll_to_event = False