# Análise de Ministérios - IDPB Filadélfia

Este projeto foi desenvolvido para realizar uma análise detalhada dos ministérios da igreja **IDPB Filadélfia**, a partir de dados fornecidos sobre o engajamento, desempenho e contribuição dos membros. O objetivo é oferecer insights para apoiar o crescimento espiritual e administrativo dos ministérios, identificando pontos fortes e áreas de melhoria.

## Objetivo

A análise busca:

- **Apoiar a liderança** na avaliação da saúde espiritual e financeira dos membros dos ministérios.
- **Identificar o engajamento** de cada membro em atividades essenciais como discipulado, ganho de vidas, assiduidade nos cultos e contribuições financeiras (dízimos e ofertas).
- **Sugerir melhorias** com base nas estratégias apresentadas pelos próprios membros.
- **Promover uma visão clara e visual dos dados**, facilitando a tomada de decisões pela liderança da igreja.

## Principais Indicadores Analisados

A análise foca nos seguintes indicadores, apresentados em gráficos e relatórios detalhados:

1. **Dízimos e Ofertas**
    - Análise do percentual de fidelidade dos membros nos dízimos e ofertas, incluindo ofertas para missões.
2. **Dificuldades Financeiras**
    - Comparação entre a contribuição financeira e as dificuldades relatadas, oferecendo uma visão clara sobre a relação entre ambas.
3. **Assiduidade nas Celebrações**
    - Avaliação da frequência dos ministros nas celebrações e cultos.
4. **Discipulado e Evangelismo**
    - Participação em discipulados periódicos e quantidade de vidas ganhas nos anos de 2023 e 2024.
5. **Engajamento e Desempenho nos Ministérios**
    - Respostas sobre engajamento categorizadas em alto, moderado e baixo, além de sugestões de melhoria para cada ministério.
6. **Relacionamentos Românticos**
    - Monitoramento da quantidade de membros em relacionamento romântico, com foco em assegurar o entendimento da visão da igreja sobre namoro cristão.

## Funcionalidades do Projeto

- **Apresentação de Insights em Formato de Slides**: Navegação pelos principais indicadores e insights sobre cada ministério.
- **Visualização dos Gráficos**: Gráficos específicos para respostas de Sim/Não e porcentagens, ajustados para facilitar a interpretação dos dados.
- **Análise por Ministério**: Cada ministério recebe uma análise específica com sugestões e estratégias para melhoria.
- **Recomendações Gerais**: Sugestões de ações baseadas nas respostas dos membros para fortalecer a unidade, engajamento e desempenho dos ministérios.

## Tecnologias Utilizadas

- **Python** para análise e manipulação de dados.
- **Pandas** para tratamento e estruturação dos dados.
- **Plotly** para criação de gráficos interativos.
- **Streamlit** para desenvolvimento da interface de visualização e navegação.

## Instruções para Execução

1. **Pré-requisitos**:
    - Python 3.8 ou superior.
    - As bibliotecas `pandas`, `plotly`, e `streamlit` instaladas.
2. **Configuração**:
    - Coloque o arquivo de dados (`dados.csv`) na mesma pasta que o script `app.py`.
3. **Execução**:
    - No terminal, execute:
        
        ```bash
        bash
        Copiar código
        streamlit run app.py
        
        ```
        
    - Navegue pela aplicação no navegador.

## Estrutura da Análise

A análise está estruturada para que cada insight seja exibido de maneira intuitiva e em formato de slides. A interface permite navegar entre diferentes indicadores e ministérios, proporcionando uma visão completa sobre o engajamento dos membros e o desempenho dos ministérios da igreja.
