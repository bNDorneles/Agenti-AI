import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import pandas as pd
import streamlit as st

from edgecloud_simulator.models import SimulationResult
from edgecloud_simulator.scenarios import build_demo_scenario
from edgecloud_simulator.simulator import run_simulation
from edgecloud_simulator.strategies import BaselineStrategy, SmartStrategy


def translate_reason(reason: str) -> str:
    translations = {
        "Allocated": "Alocada com sucesso",
        "No feasible node found": "Nenhum no viavel encontrado",
    }
    return translations.get(reason, reason)


def build_summary_rows(results: list[SimulationResult]) -> list[dict[str, object]]:
    return [
        {
            "Estrategia": result.strategy_name,
            "Tarefas alocadas": result.allocated_count,
            "Tarefas rejeitadas": result.rejected_count,
            "Latencia media (ms)": result.average_latency_ms,
            "Custo total": result.total_cost,
            "Energia total": result.total_energy,
        }
        for result in results
    ]


def build_allocation_rows(results: list[SimulationResult]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for result in results:
        for allocation in result.allocations:
            node = allocation.node
            rows.append(
                {
                    "Estrategia": result.strategy_name,
                    "Tarefa": allocation.task.name,
                    "No escolhido": node.name if node else "-",
                    "Tipo do no": node.kind if node else "-",
                    "Status": "Alocada" if node else "Rejeitada",
                    "Motivo": translate_reason(allocation.reason),
                }
            )
    return rows


def run_demo_results() -> list[SimulationResult]:
    tasks, nodes = build_demo_scenario()
    return [
        run_simulation(tasks, nodes, BaselineStrategy()),
        run_simulation(tasks, nodes, SmartStrategy()),
    ]


def render_metric_cards(summary_df: pd.DataFrame) -> None:
    for _, row in summary_df.iterrows():
        st.subheader(f"Estrategia: {row['Estrategia']}")
        columns = st.columns(5)
        columns[0].metric("Tarefas alocadas", int(row["Tarefas alocadas"]))
        columns[1].metric("Tarefas rejeitadas", int(row["Tarefas rejeitadas"]))
        columns[2].metric("Latencia media", f"{row['Latencia media (ms)']} ms")
        columns[3].metric("Custo total", f"{row['Custo total']}")
        columns[4].metric("Energia total", f"{row['Energia total']}")


def render_comparison_charts(summary_df: pd.DataFrame) -> None:
    indexed_summary = summary_df.set_index("Estrategia")
    first_row = st.columns(2)
    second_row = st.columns(3)

    first_row[0].bar_chart(indexed_summary[["Tarefas alocadas", "Tarefas rejeitadas"]])
    first_row[1].bar_chart(indexed_summary[["Latencia media (ms)"]])
    second_row[0].bar_chart(indexed_summary[["Custo total"]])
    second_row[1].bar_chart(indexed_summary[["Energia total"]])
    second_row[2].dataframe(summary_df, use_container_width=True, hide_index=True)


def render_interpretation(summary_df: pd.DataFrame) -> None:
    baseline = summary_df[summary_df["Estrategia"] == "baseline"].iloc[0]
    smart = summary_df[summary_df["Estrategia"] == "smart"].iloc[0]
    cost_delta = smart["Custo total"] - baseline["Custo total"]
    energy_delta = smart["Energia total"] - baseline["Energia total"]
    latency_delta = smart["Latencia media (ms)"] - baseline["Latencia media (ms)"]

    st.write(
        "A estrategia baseline escolhe o primeiro no viavel, enquanto a estrategia "
        "smart compara nos viaveis considerando latencia, uso de recursos, custo e energia."
    )
    st.write(
        f"Nesta simulacao, a estrategia smart teve variacao de custo de {cost_delta:.2f}, "
        f"variacao de energia de {energy_delta:.2f} e variacao de latencia media de "
        f"{latency_delta:.2f} ms em relacao ao baseline."
    )


def run_dashboard() -> None:
    st.set_page_config(page_title="Dashboard Edge-Cloud", layout="wide")
    st.title("Dashboard do Simulador Edge-Cloud")
    st.write(
        "Este painel compara duas estrategias de alocacao de tarefas em uma infraestrutura "
        "Edge-Cloud. O objetivo e visualizar, de forma simples, como cada estrategia afeta "
        "latencia, custo, energia e rejeicao de tarefas."
    )

    results = run_demo_results()
    summary_df = pd.DataFrame(build_summary_rows(results))
    allocation_df = pd.DataFrame(build_allocation_rows(results))

    st.header("Resumo das estrategias")
    render_metric_cards(summary_df)

    st.header("Comparacao visual")
    render_comparison_charts(summary_df)

    st.header("Detalhamento das alocacoes")
    st.dataframe(allocation_df, use_container_width=True, hide_index=True)

    st.header("Interpretacao")
    render_interpretation(summary_df)


if __name__ == "__main__":
    run_dashboard()
