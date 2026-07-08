# Design: Dashboard Streamlit do Simulador Edge-Cloud

## Objetivo

Criar uma visualizacao simples em Streamlit para apresentar os resultados do mini-simulador Edge-Cloud em portugues. O dashboard deve facilitar a compreensao das estrategias `baseline` e `smart` por meio de metricas resumidas, graficos comparativos, tabelas detalhadas e uma interpretacao textual curta.

## Escopo

O trabalho adiciona uma interface visual ao projeto atual sem alterar a logica central do simulador. A simulacao continuara usando o cenario de demonstracao existente em `build_demo_scenario()` e comparara as estrategias `BaselineStrategy` e `SmartStrategy`.

Faz parte do escopo:

- criar um arquivo `dashboard.py` na raiz do projeto;
- exibir informacoes em portugues;
- comparar as estrategias por tarefas alocadas, tarefas rejeitadas, latencia media, custo total e energia total;
- mostrar uma tabela detalhada de alocacoes por estrategia;
- atualizar a documentacao com instrucoes para executar o dashboard;
- declarar as dependencias necessarias para Streamlit.

Nao faz parte do escopo inicial:

- editar tarefas e nos pela interface;
- ajustar pesos da estrategia inteligente pela interface;
- criar backend HTTP ou frontend React;
- persistir resultados em banco de dados ou arquivos.

## Arquitetura

O dashboard sera uma camada de apresentacao sobre os modulos existentes:

- `dashboard.py` importa `build_demo_scenario`, `run_simulation`, `BaselineStrategy` e `SmartStrategy`;
- a cada execucao da pagina, o dashboard roda as duas simulacoes;
- os resultados sao convertidos em estruturas tabulares simples para exibicao;
- a logica de alocacao permanece nos arquivos atuais em `src/edgecloud_simulator`.

Essa abordagem mantem o projeto facil de explicar: o simulador calcula, e o Streamlit apenas apresenta.

## Interface

A tela unica tera:

- titulo: "Dashboard do Simulador Edge-Cloud";
- texto curto explicando o objetivo da simulacao;
- selecao visual das duas estrategias comparadas;
- cards de metricas para cada estrategia;
- graficos de barras para comparar alocadas, rejeitadas, latencia media, custo total e energia total;
- tabela com tarefa, no escolhido, status e motivo;
- secao de interpretacao em portugues destacando os principais trade-offs.

## Dados

As metricas virao de `SimulationResult`:

- `allocated_count`;
- `rejected_count`;
- `average_latency_ms`;
- `total_cost`;
- `total_energy`;
- `allocations`.

Para a tabela, cada `Allocation` sera convertido em uma linha com:

- estrategia;
- tarefa;
- no escolhido;
- tipo do no;
- status;
- motivo.

## Tratamento de Erros

Como o dashboard usa um cenario fixo e codigo local, o risco principal e erro de importacao ou dependencia ausente. A documentacao deve orientar a instalacao das dependencias e a execucao a partir da raiz do projeto. O `dashboard.py` deve configurar o caminho `src/` de forma semelhante ao `main.py`.

## Testes e Verificacao

A verificacao deve incluir:

- executar os testes existentes com `python -m unittest discover -s tests -p "test_*.py" -v`;
- validar que o dashboard importa e prepara os dados sem erro;
- iniciar o Streamlit localmente para confirmar que a interface abre.

## Criterios de Aceite

O dashboard sera considerado pronto quando:

- puder ser iniciado com `streamlit run dashboard.py`;
- mostrar todas as informacoes principais em portugues;
- comparar claramente `baseline` e `smart`;
- preservar os testes existentes passando;
- o README explicar como executar a interface visual.
