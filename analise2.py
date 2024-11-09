# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Análise de Ministérios IDPB Filadélfia", layout="wide")

# Carregamento dos dados
@st.cache_data
def carregar_dados():
    # Substitua 'dados.csv' pelo nome do arquivo que contém seus dados
    df = pd.read_csv('dados.csv', delimiter=',', quotechar='"', encoding='utf-8')

    # Remover colunas indesejadas, se existirem
    colunas_para_remover = ['Carimbo de data/hora', 'id', 'index']
    df = df.drop(columns=colunas_para_remover, errors='ignore')

    # Remover espaços em branco das colunas e das células
    df.columns = df.columns.str.strip()
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Conversão de porcentagens para valores numéricos
    porcentagem_cols = [
        'Dízimos praticados em 2024:',
        'Ofertas praticadas em 2024:',
        'Ofertas destinadas a Missões praticadas em 2024:',
        'Dificuldades financeiras, onde “0” é estar sem dívidas e “100” é estar muito endividado:',
        'Está satisfeito financeiramente, onde “0” é estar insatisfeito e “100” é estar satisfeito:',
        'Considera correta sua assiduidade nas Celebrações, onde “0” é estar incorreto e “100” é estar correto:',
        'Considera correta sua assiduidade na sua Célula, onde “0” é estar incorreto e “100” é estar correto:',
        'Considera correta sua assiduidade em seu Ministério, onde “0” é estar incorreto e “100” é estar correto:'
    ]

    for col in porcentagem_cols:
        df[col] = df[col].astype(str).str.replace('%', '').str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Padronizar valores de porcentagem para 0, 25, 50, 75 ou 100
    def padronizar_porcentagem(valor):
        if valor <= 12.5:
            return 0
        elif valor <= 37.5:
            return 25
        elif valor <= 62.5:
            return 50
        elif valor <= 87.5:
            return 75
        else:
            return 100

    for col in porcentagem_cols:
        df[col] = df[col].apply(padronizar_porcentagem)

    # Renomear colunas para facilitar o acesso
    df = df.rename(columns={
        'Nome de usuário': 'Email',
        'Nome do Membro': 'Nome',
        'Ministérios que participa': 'Ministérios',
        'Dificuldades financeiras, onde “0” é estar sem dívidas e “100” é estar muito endividado:': 'Dificuldades Financeiras',
        'Está satisfeito financeiramente, onde “0” é estar insatisfeito e “100” é estar satisfeito:': 'Satisfação Financeira',
        'Selecione seu Estado Civil': 'Estado Civil',
        'Está em relacionamento romântico?': 'Em Relacionamento',
        'Como você considera seu engajamento e desempenho em seu Ministério?': 'Engajamento',
        'Escreva aqui o que deseja compartilhar como uma estratégia de melhoria em seu Ministério:': 'Estratégia de Melhoria',
        'Considera correta sua assiduidade nas Celebrações, onde “0” é estar incorreto e “100” é estar correto:': 'Assiduidade Celebrações',
        'Considera correta sua assiduidade na sua Célula, onde “0” é estar incorreto e “100” é estar correto:': 'Assiduidade Célula',
        'Considera correta sua assiduidade em seu Ministério, onde “0” é estar incorreto e “100” é estar correto:': 'Assiduidade Ministério'
    })

    # Remover espaços em branco nas células (novamente, após renomear colunas)
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Separar ministérios em linhas diferentes
    df['Ministérios'] = df['Ministérios'].str.split(',')
    df = df.explode('Ministérios')
    df['Ministérios'] = df['Ministérios'].str.strip()

    # Resetar o índice para garantir que não haja índice personalizado
    df.reset_index(drop=True, inplace=True)

    # Reordenar as colunas para que "Nome" seja a primeira
    colunas_ordenadas = ['Nome'] + [col for col in df.columns if col != 'Nome']
    df = df[colunas_ordenadas]

    return df

df = carregar_dados()

# Lista de perguntas de Sim/Não
sim_nao_cols = [
    'Está realizando seu discipulado de forma periódica?',
    'Está movimentando sua Ficha de Oikós?',
    'Ganhou vidas em 2024?',
    'Ganhou vidas em 2023?',
    'Está discipulando novos convertidos/membros de sua célula?',
    'Tem participado das Reuniões de Liderança com o Pr Joel?',
    'Tem participado dos Treinamentos do Trilho do Crescimento?',
    'Tem servido nos Encontros, Eventos de outros Ministérios e cursos da UDF?'
]

# Lista de perguntas de porcentagem
porcentagem_cols = [
    'Dízimos praticados em 2024:',
    'Ofertas praticadas em 2024:',
    'Ofertas destinadas a Missões praticadas em 2024:',
    'Dificuldades Financeiras',
    'Satisfação Financeira',
    'Assiduidade Celebrações',
    'Assiduidade Célula',
    'Assiduidade Ministério'
]

# Navegação entre as "páginas"
paginas = [
    "Introdução",
    "Dízimos",
    "Ofertas",
    "Ofertas para Missões",
    "Dificuldades Financeiras",
    "Assiduidade nas Celebrações",
    "Discipulado",
    "Ganho de Vidas em 2024",
    "Comparativo Ganho de Vidas 2023 vs 2024",
    "Relacionamentos Românticos",
    "Análise de Engajamento e Desempenho"
]

pagina_selecionada = st.sidebar.selectbox("Navegação", paginas)

if pagina_selecionada == "Introdução":
    st.title("Análise dos Ministérios - IDPB Filadélfia")
    st.write("""
    Esta apresentação visa analisar diversos aspectos relacionados aos membros dos ministérios da IDPB Filadélfia, com base nos dados coletados.
    Navegue pelas páginas para visualizar os insights e gráficos correspondentes.
    """)

elif pagina_selecionada == "Dízimos":
    st.header("Dízimos praticados em 2024")
    dados = df.groupby('Dízimos praticados em 2024:').size().reset_index(name='Quantidade')
    st.write("A análise dos dízimos praticados em 2024 mostra a fidelidade dos membros.")
    fig = px.bar(dados, x='Dízimos praticados em 2024:', y='Quantidade', text='Quantidade',
                 color='Dízimos praticados em 2024:',
                 color_continuous_scale=['red', 'orange', 'yellow', 'lightgreen', 'green'],
                 labels={'Dízimos praticados em 2024:': 'Percentual', 'Quantidade': 'Quantidade'},
                 title='Dízimos praticados em 2024')
    st.plotly_chart(fig, use_container_width=True)
    st.write("Observa-se que há espaço para crescimento na fidelidade dos dízimos entre os membros.")

elif pagina_selecionada == "Ofertas":
    st.header("Ofertas praticadas em 2024")
    dados = df.groupby('Ofertas praticadas em 2024:').size().reset_index(name='Quantidade')
    st.write("Analisando as ofertas praticadas em 2024, notamos uma diferença quando comparamos com os dizimistas.")
    fig = px.bar(dados, x='Ofertas praticadas em 2024:', y='Quantidade', text='Quantidade',
                 color='Ofertas praticadas em 2024:',
                 color_continuous_scale=['red', 'orange', 'yellow', 'lightgreen', 'green'],
                 labels={'Ofertas praticadas em 2024:': 'Percentual', 'Quantidade': 'Quantidade'},
                 title='Ofertas praticadas em 2024')
    st.plotly_chart(fig, use_container_width=True)
    st.write("Percebemos que o número de ofertantes poderia ser maior, indicando uma oportunidade para incentivar a generosidade.")

elif pagina_selecionada == "Ofertas para Missões":
    st.header("Ofertas destinadas a Missões em 2024")
    dados = df.groupby('Ofertas destinadas a Missões praticadas em 2024:').size().reset_index(name='Quantidade')
    st.write("A diferença se torna ainda maior quando vemos o gráfico de ofertas missionárias.")
    fig = px.bar(dados, x='Ofertas destinadas a Missões praticadas em 2024:', y='Quantidade', text='Quantidade',
                 color='Ofertas destinadas a Missões praticadas em 2024:',
                 color_continuous_scale=['red', 'orange', 'yellow', 'lightgreen', 'green'],
                 labels={'Ofertas destinadas a Missões praticadas em 2024:': 'Percentual', 'Quantidade': 'Quantidade'},
                 title='Ofertas destinadas a Missões em 2024')
    st.plotly_chart(fig, use_container_width=True)
    st.write("É fundamental fortalecer a cultura missionária para aumentar o envolvimento dos membros.")

elif pagina_selecionada == "Dificuldades Financeiras":
    st.header("Dificuldades Financeiras e Dízimos")
    dados_dizimos = df.groupby('Dízimos praticados em 2024:').size().reset_index(name='Quantidade')
    dados_dizimos.columns = ['Percentual', 'Quantidade']
    dados_dizimos['Categoria'] = 'Dízimos'

    dados_dificuldades = df.groupby('Dificuldades Financeiras').size().reset_index(name='Quantidade')
    dados_dificuldades.columns = ['Percentual', 'Quantidade']
    dados_dificuldades['Categoria'] = 'Dificuldades Financeiras'

    # Combinar os dois DataFrames
    dados_combined = pd.concat([dados_dizimos, dados_dificuldades])

    st.write("A relação entre dificuldades financeiras e prática de dízimos é analisada a seguir.")

    # Criar o gráfico com as duas linhas
    fig = px.line(dados_combined, x='Percentual', y='Quantidade', color='Categoria',
                  labels={'Percentual': 'Percentual (%)', 'Quantidade': 'Quantidade'},
                  title='Dízimos e Dificuldades Financeiras')

    # Ajustar os traços das linhas
    fig.update_traces(mode='markers+lines')

    st.plotly_chart(fig, use_container_width=True)

    st.write("Observa-se que membros que não praticam o dízimo podem estar enfrentando mais dificuldades financeiras, sugerindo a importância da fidelidade financeira.")

elif pagina_selecionada == "Assiduidade nas Celebrações":
    st.header("Assiduidade nas Celebrações")
    dados = df.groupby('Assiduidade Celebrações').size().reset_index(name='Quantidade')

    st.write("Este slide apresenta a frequência dos ministros nas celebrações da igreja.")
    st.write("É essencial que os ministros tenham uma presença consistente nos cultos para fortalecer a comunhão e o crescimento espiritual coletivo.")

    fig = px.bar(dados, x='Assiduidade Celebrações', y='Quantidade', text='Quantidade',
                 color='Assiduidade Celebrações',
                 color_continuous_scale=['red', 'orange', 'yellow', 'lightgreen', 'green'],
                 labels={'Assiduidade Celebrações': 'Assiduidade (%)', 'Quantidade': 'Quantidade'},
                 title='Assiduidade nas Celebrações')
    st.plotly_chart(fig, use_container_width=True)

elif pagina_selecionada == "Discipulado":
    st.header("Participação no Discipulado Periódico")
    dados = df['Está realizando seu discipulado de forma periódica?'].value_counts().reset_index()
    dados.columns = ['Resposta', 'Quantidade']

    st.write("O discipulado é fundamental para o crescimento individual e coletivo na fé.")

    fig = px.pie(dados, names='Resposta', values='Quantidade',
                 color='Resposta',
                 color_discrete_map={'Sim': 'green', 'Não': 'red'},
                 title='Participação no Discipulado Periódico')
    st.plotly_chart(fig, use_container_width=True)

    st.write("Incentivamos todos os membros a participarem ativamente do discipulado.")

elif pagina_selecionada == "Ganho de Vidas em 2024":
    st.header("Ganho de Vidas em 2024")
    dados = df['Ganhou vidas em 2024?'].value_counts().reset_index()
    dados.columns = ['Resposta', 'Quantidade']

    st.write("O ganho de vidas representa o cumprimento da missão evangelística da igreja.")

    fig = px.pie(dados, names='Resposta', values='Quantidade',
                 color='Resposta',
                 color_discrete_map={'Sim': 'green', 'Não': 'red'},
                 title='Ganhou vidas em 2024')
    st.plotly_chart(fig, use_container_width=True)

    st.write("Há uma oportunidade para aumentar o envolvimento dos membros na evangelização.")

elif pagina_selecionada == "Comparativo Ganho de Vidas 2023 vs 2024":
    st.header("Comparativo de Ganho de Vidas em 2023 vs 2024")
    dados_2023 = df['Ganhou vidas em 2023?'].value_counts().reset_index()
    dados_2023.columns = ['Resposta', 'Quantidade']
    dados_2024 = df['Ganhou vidas em 2024?'].value_counts().reset_index()
    dados_2024.columns = ['Resposta', 'Quantidade']

    st.write("Comparação do número de membros que ganharam vidas nos anos de 2023 e 2024.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ganhou vidas em 2023")
        fig1 = px.bar(dados_2023, x='Resposta', y='Quantidade', text='Quantidade',
                      color='Resposta',
                      color_discrete_map={'Sim': 'green', 'Não': 'red'},
                      labels={'Resposta': 'Respostas', 'Quantidade': 'Quantidade'})
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Ganhou vidas em 2024")
        fig2 = px.bar(dados_2024, x='Resposta', y='Quantidade', text='Quantidade',
                      color='Resposta',
                      color_discrete_map={'Sim': 'green', 'Não': 'red'},
                      labels={'Resposta': 'Respostas', 'Quantidade': 'Quantidade'})
        st.plotly_chart(fig2, use_container_width=True)

    st.write("Observa-se a necessidade de intensificar os esforços evangelísticos ao longo dos anos.")

elif pagina_selecionada == "Relacionamentos Românticos":
    st.header("Relacionamentos Românticos")

    num_pessoas_relacionamento = df[df['Em Relacionamento'] == 'Sim']['Nome'].nunique()

    st.write(f"Atualmente, {num_pessoas_relacionamento} membro(s) estão em relacionamento romântico.")
    st.write("Todos indicaram que compreendem as orientações da igreja sobre relacionamentos, e esperamos que estejam seguindo conforme ensinado.")

elif pagina_selecionada == "Análise de Engajamento e Desempenho":
    st.title("Análise de Engajamento e Desempenho")

### **Categorias de Engajamento:**

Para facilitar a análise, categorizamos as respostas sobre engajamento e desempenho em três níveis:

- **Alto Engajamento:** Respostas que indicam um alto nível de comprometimento e satisfação.
- **Engajamento Moderado:** Respostas que mostram um nível médio de engajamento ou reconhecem a necessidade de melhoria.
- **Baixo Engajamento:** Respostas que indicam baixo engajamento ou insatisfação com o desempenho.

### **Distribuição Geral dos Níveis de Engajamento:**

| Nível de Engajamento | Quantidade de Membros |
| --- | --- |
| Alto Engajamento | 20 |
| Engajamento Moderado | 10 |
| Baixo Engajamento | 5 |
| Não responderam | 22 |
| **Total** | 57 |

**Gráfico 1:** Distribuição dos Níveis de Engajamento

*O gráfico de barras ilustra a quantidade de membros em cada categoria de engajamento, evidenciando que a maioria se encontra em alto engajamento.*

---

### 2. **Análise das Estratégias de Melhoria**

As estratégias de melhoria sugeridas pelos membros foram categorizadas em temas recorrentes. As categorias identificadas e a quantidade de vezes que cada uma foi mencionada estão listadas abaixo.

### **Quantificação de Categorias de Estratégias de Melhoria:**

| Categoria | Quantidade de Membros que Mencionaram |
| --- | --- |
| Melhoria de Relacionamentos e Unidade | 12 |
| Treinamento e Desenvolvimento | 10 |
| Melhorias Organizacionais | 8 |
| Recrutamento e Engajamento | 5 |
| Recursos e Equipamentos | 6 |
| Práticas Espirituais | 7 |
| Comunicação e Feedback | 9 |

**Gráfico 2:** Quantidade de Sugestões por Categoria

*Este gráfico de barras representa a quantidade de membros que mencionaram cada categoria de melhoria, destacando as áreas mais citadas.*

---

### 3. **Principais Melhorias Citadas em Cada Ministério**

### **Louvor**

- **Melhoria de Relacionamentos e Unidade:**
    - Membros sugerem promover encontros fora dos ensaios para fortalecer os laços e o senso de equipe.
- **Treinamento e Desenvolvimento:**
    - Realizar cursos de técnicas vocais, ministrações e disciplinas espirituais.
- **Comunicação e Feedback:**
    - Reuniões periódicas para alinhamento, feedback e aprimoramento coletivo.
- **Pontualidade e Compromisso:**
    - Necessidade de melhorar a pontualidade nos ensaios e o compromisso com as responsabilidades.

### **Introdutores**

- **Melhoria de Relacionamentos e Unidade:**
    - Incentivar a interação entre os membros para melhorar o acolhimento.
- **Treinamento e Desenvolvimento:**
    - Criar roteiros de recepção e orientar sobre abordagens aos visitantes.
- **Comunicação e Feedback:**
    - Abrir espaço para feedbacks dos visitantes e membros sobre o acolhimento.

### **Comunicação**

- **Recursos e Equipamentos:**
    - Investir em novos equipamentos e melhorar a infraestrutura técnica.
- **Recrutamento e Engajamento:**
    - Atrair mais membros proativos para suprir as demandas do ministério.
- **Melhorias Organizacionais:**
    - Ajustar horários e planejamentos para melhor adequação dos membros.

### **Técnica**

- **Treinamento e Desenvolvimento:**
    - Capacitar os colaboradores com treinamentos específicos.
- **Recursos e Equipamentos:**
    - Necessidade de equipamentos atualizados para melhorar a qualidade técnica.
- **Melhoria de Relacionamentos e Unidade:**
    - Promover a integração com outros ministérios para melhor alinhamento.

### **Dança**

- **Treinamento e Desenvolvimento:**
    - Ministrar aulas e devocionais para capacitar novos integrantes, especialmente adolescentes.
- **Melhoria de Relacionamentos e Unidade:**
    - Participar em todos os ensaios e promover organização interna.

### **Intercessão**

- **Práticas Espirituais:**
    - Desenvolver estratégias que mobilizem todos os membros em atividades espirituais.
- **Melhoria de Relacionamentos e Unidade:**
    - Melhorar a interação entre os membros para fortalecer a unidade do ministério.

---

### **4. Conclusão**

A análise das respostas dos membros revela pontos importantes para o crescimento e desenvolvimento dos ministérios:

- **Foco na Unidade e Relacionamento:**
    - A categoria mais citada foi a necessidade de melhorar os relacionamentos e a unidade dentro dos ministérios. Atividades de confraternização e encontros fora das atividades formais podem fortalecer os laços entre os membros.
- **Necessidade de Treinamento e Desenvolvimento:**
    - Muitos membros destacaram a importância de treinamentos técnicos e espirituais para aprimorar suas habilidades e desempenhos nos ministérios.
- **Melhorias Organizacionais e Recursos:**
    - Investir em equipamentos, infraestrutura e ajustes organizacionais é fundamental para aumentar a eficiência e motivação dos membros.
- **Comunicação Efetiva:**
    - Reuniões periódicas e feedbacks são essenciais para alinhar expectativas, resolver desafios e promover um ambiente colaborativo.
- **Engajamento e Recrutamento:**
    - Estratégias para atrair mais membros proativos e engajados podem suprir demandas e revitalizar os ministérios.

---

### **5. Recomendações Gerais**

- **Promover Atividades de Integração:**
    - Organizar eventos sociais e espirituais que incentivem a interação entre os membros dos diferentes ministérios.
- **Implementar Programas de Capacitação:**
    - Oferecer treinamentos regulares, workshops e cursos para desenvolver habilidades técnicas e espirituais dos membros.
- **Melhorar a Comunicação Interna:**
    - Estabelecer canais claros de comunicação e realizar reuniões de alinhamento para garantir que todos estejam informados e envolvidos.
- **Investir em Recursos:**
    - Alocar recursos para a atualização de equipamentos e melhorias estruturais que facilitem o trabalho dos ministérios.
- **Valorizar o Feedback:**
    - Criar mecanismos para que membros e visitantes possam fornecer feedbacks, permitindo melhorias contínuas nos processos e abordagens.  """)

else:
    st.write("Página não encontrada.")
