import streamlit as st
from datetime import date, timedelta
import os
from PIL import Image

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

# Selecionar intervalo de datas
data_inicio = st.date_input("Data de Início", value=date(2023, 1, 1))
data_fim = st.date_input("Data de Fim", value=date.today())

# Mostrar o calendário
for single_date in (data_inicio + timedelta(n) for n in range((data_fim - data_inicio).days + 1)):
    data_str = single_date.strftime('%Y-%m-%d')
    if single_date in datas_importantes:
        st.write(f"**{single_date.strftime('%d/%m/%Y')}** - {datas_importantes[single_date]}")
        if os.path.exists(f'fotos/{data_str}.jpg'):
            st.image(f'fotos/{data_str}.jpg', caption=datas_importantes[single_date])
    else:
        st.write(single_date.strftime('%d/%m/%Y'))