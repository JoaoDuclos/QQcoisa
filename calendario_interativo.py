import streamlit as st
from datetime import date, timedelta
import os
from PIL import Image
import calendar

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
    for _ in range(primeiro_dia):
        html_calendario += "<td></td>"

    for dia in range(1, num_dias + 1):
        if dia_atual.weekday() == 6 and dia_atual.day != 1:
            html_calendario += "</tr><tr>"

        if dia_atual in datas_importantes:
            evento = datas_importantes[dia_atual]
            html_calendario += (
                f"<td style='border: 1px solid #ddd; padding: 10px; text-align: center; "
                f"background-color: lightblue; cursor: pointer;' onclick='alert(\"{evento}\")'>"
                f"{dia}</td>"
            )
        else:
            html_calendario += (
                f"<td style='border: 1px solid #ddd; padding: 10px; text-align: center;'>"
                f"{dia}</td>"
            )

        dia_atual += timedelta(days=1)

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

# Interatividade com o Streamlit
st.write("Clique nas datas importantes para ver fotos:")
data_selecionada = st.date_input("Selecione uma data", value=date.today(), min_value=data_inicio, max_value=data_fim)

if data_selecionada in datas_importantes:
    data_str = data_selecionada.strftime('%Y-%m-%d')
    st.write(f"**{data_selecionada.strftime('%d/%m/%Y')}** - {datas_importantes[data_selecionada]}")
    if os.path.exists(f'fotos/{data_str}.jpg'):
        st.image(f'fotos/{data_str}.jpg', caption=datas_importantes[data_selecionada])
else:
    st.write("Não há evento ou foto para esta data.")