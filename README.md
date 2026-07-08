# Mini-Simulador: Alocacao de Tarefas em Edge-Cloud

Protótipo desenvolvido para o desafio técnico da bolsa PROBIC/FAPERGS do AI Horizon Labs.

O objetivo é simular a decisão de onde executar tarefas em uma infraestrutura Edge-Cloud, considerando capacidade computacional, memória, latência, custo e consumo energético.

## Resumo

Infraestruturas distribuídas combinam servidores próximos do usuário, chamados de borda, com servidores mais distantes e robustos, chamados de nuvem. A decisão de onde executar cada tarefa afeta diretamente a latência, o custo, o consumo de energia e a qualidade do serviço.

Este mini-simulador modela esse problema de forma simples e reprodutível. Ele executa o mesmo conjunto de tarefas com duas estratégias de alocação:

- `baseline`: escolhe o primeiro nó viável.
- `smart`: escolhe o nó viável com menor pontuação, considerando latência, pressão de recursos, custo e energia.

## Problema Modelado

Cada tarefa possui requisitos de CPU, memória, latência máxima tolerada e prioridade. Cada nó da infraestrutura possui tipo (`edge` ou `cloud`), capacidade de CPU e memória, latência, custo por tarefa e consumo energético.

Uma tarefa só pode ser alocada se o nó tiver recursos suficientes e se a latência do nó respeitar o limite máximo da tarefa.

## Estrutura

```text
.
├── main.py
├── src/
│   └── edgecloud_simulator/
│       ├── models.py
│       ├── scenarios.py
│       ├── simulator.py
│       └── strategies.py
├── tests/
│   ├── test_models.py
│   ├── test_simulator.py
│   └── test_strategies.py
└── README.md
```

## Como Rodar

Para executar apenas o simulador de linha de comando, use Python 3. O dashboard visual usa as dependências listadas em `requirements.txt`.

```bash
python main.py
```

## Como Rodar o Dashboard Visual

Instale as dependencias:

```bash
python -m pip install -r requirements.txt
```

Execute o painel:

```bash
streamlit run dashboard.py
```

O dashboard apresenta as metricas do simulador em portugues, com cards, graficos comparativos e uma tabela detalhada das alocacoes.

## Como Rodar os Testes

Como o projeto usa o layout `src/`, defina `PYTHONPATH` antes de executar os testes.

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests -p "test_*.py" -v
```

Em Linux/macOS:

```bash
PYTHONPATH=src python -m unittest discover -s tests -p "test_*.py" -v
```

## Metodologia

O simulador executa as tarefas em sequência. Para cada tarefa, a estratégia ativa recebe a lista de nós e seleciona um nó viável ou rejeita a tarefa quando não há opção compatível.

A estratégia `smart` calcula uma pontuação para cada nó viável:

```text
score = latencia ponderada pela prioridade
      + pressao de recursos
      + custo
      + energia
```

O nó com menor pontuação é escolhido. Essa abordagem torna a decisão mais explicável do que simplesmente escolher o primeiro nó possível.

## Métricas

Ao final da execução, o simulador apresenta:

- número de tarefas alocadas;
- número de tarefas rejeitadas;
- latência média;
- custo total;
- energia total.

Essas métricas permitem comparar diferentes políticas de alocação sob o mesmo cenário experimental.

## Exemplo de Resultado

No cenário de demonstração, a estratégia inteligente tende a distribuir melhor algumas tarefas, reduzindo custo e energia, enquanto mantém uma taxa de alocação equivalente à estratégia baseline. A pequena variação de latência ilustra o trade-off clássico entre desempenho, custo e uso eficiente da infraestrutura.

## Relação com o Projeto de Pesquisa

O projeto institucional trata de alocação de recursos computacionais em infraestruturas distribuídas usando Agentic AI. Este protótipo representa uma primeira camada experimental: um ambiente simples onde diferentes estratégias podem ser comparadas de forma controlada.

Em trabalhos futuros, um agente poderia usar esse simulador como ferramenta para:

- testar diferentes políticas de alocação;
- explicar decisões;
- ajustar pesos da função de pontuação;
- comparar heurísticas clássicas com decisões baseadas em Agentic AI.

## Limitações e Trabalhos Futuros

O simulador utiliza um cenário fixo e uma heurística determinística. Como evolução, seria possível adicionar geração automática de cargas de trabalho, gráficos, múltiplas sementes de simulação, novas heurísticas e uma camada agentic para propor ou explicar decisões de alocação.
