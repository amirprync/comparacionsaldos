import streamlit as st
import pandas as pd
import io

def create_sample_excel():
    sample_data = {
        'numero de comitente': [1, 2, 3],
        'cantidad': [100, 200, 300]
    }
    sample_df = pd.DataFrame(sample_data)
    excel_io = io.BytesIO()
    with pd.ExcelWriter(excel_io, engine='xlsxwriter') as writer:
        sample_df.to_excel(writer, sheet_name='Hoja1', index=False)
    excel_io.seek(0)
    return excel_io

def compare_files(file1, file2):
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    
    if 'numero de comitente' not in df1.columns or 'cantidad' not in df1.columns:
        st.error("El archivo 1 debe tener columnas llamadas 'numero de comitente' y 'cantidad'")
        return
    if 'numero de comitente' not in df2.columns or 'cantidad' not in df2.columns:
        st.error("El archivo 2 debe tener columnas llamadas 'numero de comitente' y 'cantidad'")
        return
    
    merged_df = pd.merge(df1, df2, on='numero de comitente', how='outer', suffixes=('_file1', '_file2'))
    
    diff_df = merged_df[merged_df['cantidad_file1'] != merged_df['cantidad_file2']]
    
    if diff_df.empty:
        st.write("No hay diferencias en las cantidades para los mismos números de comitente.")
    else:
        st.write("Se encontraron diferencias en las siguientes entradas:")
        st.write(diff_df)

# Streamlit app
st.title("Comparador de Archivos Excel")

# Botón para descargar el archivo Excel modelo
sample_excel = create_sample_excel()
st.download_button(
    label="Descargar archivo Excel modelo",
    data=sample_excel,
    file_name="modelo_comitente_cantidad.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

uploaded_file1 = st.file_uploader("Sube el primer archivo Excel", type=['xlsx'])
uploaded_file2 = st.file_uploader("Sube el segundo archivo Excel", type=['xlsx'])

if uploaded_file1 is not None and uploaded_file2 is not None:
    compare_files(uploaded_file1, uploaded_file2)
