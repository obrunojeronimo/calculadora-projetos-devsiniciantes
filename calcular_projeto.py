import streamlit as st
from datetime import datetime
from fpdf import FPDF

def calcular_valor_projeto(taxa_hora, horas_trabalhadas, qtd_pessoas, urgencia, taxas_pessoas):
    valor_total = (taxa_hora * horas_trabalhadas) + sum(taxas_pessoas)
    multiplicador_urgencia = {'Baixa': 1.0, 'Média': 1.25, 'Alta': 1.5}.get(urgencia, 1.0)
    valor_total *= multiplicador_urgencia
    return valor_total

def gerar_pdf(valor_total, taxa_hora, horas_trabalhadas, data_entrega, qtd_pessoas, taxas_pessoas, urgencia, conhecimentos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Orçamento do Projeto", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Valor da sua hora de trabalho: R${taxa_hora:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Horas estimadas para o projeto: {horas_trabalhadas}", ln=True)
    pdf.cell(200, 10, txt=f"Data de entrega do projeto: {data_entrega.strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(200, 10, txt=f"Nível de urgência: {urgencia}", ln=True)
    pdf.cell(200, 10, txt=f"Valor total do projeto: R${valor_total:.2f}", ln=True)
    
    
    pdf.ln(10)
    pdf.cell(200, 10, txt="Valores por pessoa:", ln=True)
    for idx, taxa in enumerate(taxas_pessoas, start=1):
        pdf.cell(200, 10, txt=f"Pessoa {idx}: R${taxa:.2f} por hora", ln=True)
    
    
    pdf.ln(10)
    pdf.cell(200, 10, txt="Conhecimentos necessários:", ln=True)
    for conhecimento in conhecimentos:
        pdf.cell(200, 10, txt=f"- {conhecimento}", ln=True)

    pdf.ln(10)
    output_path = "orcamento_projeto.pdf"  
    pdf.output(output_path)
    return output_path

def capturar_dados_projeto():
    taxa_hora = st.number_input('Valor da sua hora de trabalho (R$)', min_value=0.0, value=50.0, step=5.0)
    horas_trabalhadas = st.number_input('Horas estimadas para o projeto', min_value=1, value=10, step=1)
    data_entrega = st.date_input('Data de entrega do projeto', min_value=datetime.today())
    qtd_pessoas = st.number_input('Número de pessoas envolvidas (além de você)', min_value=0, value=1, step=1)

    taxas_pessoas = []
    for pessoa in range(1, int(qtd_pessoas) + 1):
        taxa = st.number_input(f'Valor da hora para a pessoa {pessoa} (R$)', min_value=0.0, value=50.0, step=5.0)
        taxas_pessoas.append(taxa)

    urgencia = st.selectbox('Nível de urgência do projeto', ['Baixa', 'Média', 'Alta'])
    conhecimentos = st.text_area('Conhecimentos necessários (separe por vírgulas)', placeholder="Ex.: Python, SQL, Power BI")
    conhecimentos_list = [conhecimento.strip() for conhecimento in conhecimentos.split(",")]

    return taxa_hora, horas_trabalhadas, data_entrega, qtd_pessoas, taxas_pessoas, urgencia, conhecimentos_list

st.title('Calculadora de Projetos: Seu Primeiro Passo na Carreira de Dados! 🚀')
st.write('Desenvolvedores e analistas de dados, sua nova aliada chegou! Esta calculadora de projetos permite estimar rapidamente o valor do seu trabalho, considerando urgência e habilidades necessárias. Com uma interface intuitiva, você pode calcular orçamentos e gerar um PDF do seu orçamento final. Prepare-se para conquistar seus projetos com confiança!')

taxa_hora, horas_trabalhadas, data_entrega, qtd_pessoas, taxas_pessoas, urgencia, conhecimentos = capturar_dados_projeto()

if st.button('Calcular valor do projeto'):
    valor_total = calcular_valor_projeto(taxa_hora, horas_trabalhadas, qtd_pessoas, urgencia, taxas_pessoas)
    st.session_state['valor_total'] = valor_total
    st.write(f'O valor total do projeto é: R${valor_total:.2f}')

if st.button('Exportar orçamento em PDF'):
    if 'valor_total' not in st.session_state:
        st.warning('Calcule o valor do projeto antes de exportar para PDF!')
    else:
        pdf_path = gerar_pdf(st.session_state['valor_total'], taxa_hora, horas_trabalhadas, data_entrega, qtd_pessoas, taxas_pessoas, urgencia, conhecimentos)
        st.success('Orçamento exportado com sucesso!')
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(label="Baixar PDF", data=pdf_file, file_name="orcamento_projeto.pdf", mime="application/pdf")


st.markdown("---") 
st.subheader("Desenvolvido por:")
st.write("Bruno Jerônimo") 

st.write("Para entrar em contato comigo, clique nos links abaixo 👇")
st.write("📧 [E-mail](mailto:brnjeronimo@gmail.com)")
st.write("🔗 [GitHub](https://github.com/obrunojeronimo)")
st.write("🔗 [LinkedIn](https://linkedin.com/in/brunojeronimo)")
st.write("📸 [Instagram](https://instagram.com/obrunojeronimo)")
st.write("🌐 [Portfólio](https://www.datascienceportfol.io/brunojeronimo)")

st.markdown("---")  # Linha horizontal para finalizar a seção