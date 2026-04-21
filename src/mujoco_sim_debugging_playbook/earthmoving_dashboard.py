from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


def build_earthmoving_dashboard(
    *,
    review_packet_path: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    packet = json.loads(Path(review_packet_path).read_text())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    index_path = output / "index.html"
    data_path = output / "data.json"
    data_path.write_text(json.dumps(packet, indent=2))
    index_path.write_text(_render_html(packet))
    return {"output_dir": str(output), "index_path": str(index_path), "data_path": str(data_path)}


def _render_html(packet: dict[str, Any]) -> str:
    summary = packet["summary"]
    scenario_rows = "\n".join(
        "<tr>"
        f"<td>{html.escape(row['scenario'])}</td>"
        f"<td>{row['moved_volume']:.6f}</td>"
        f"<td>{row.get('deposit_forward_progress', 0.0):.4f}</td>"
        f"<td>{row['terrain_profile_rmse']:.6f}</td>"
        f"<td>{row['volume_conservation_error']:.6f}</td>"
        f"<td>{row['runtime_s']:.5f}</td>"
        "</tr>"
        for row in packet["scenario_table"]
    )
    sensitivity_rows = "\n".join(
        "<tr>"
        f"<td>{html.escape(row['soil_parameter'])}</td>"
        f"<td>{html.escape(row['metric'])}</td>"
        f"<td>{row['pearson_correlation']:.4f}</td>"
        "</tr>"
        for row in packet["top_sensitivities"][:6]
    )
    signals = "\n".join(
        f"<section><h3>{html.escape(item['name'])}</h3><p>{html.escape(item['value'])}</p><span>{html.escape(item['detail'])}</span></section>"
        for item in packet["readiness_signals"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Earthmoving Simulation Review</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #172026;
      --muted: #5f6b73;
      --line: #d7dde1;
      --panel: #f7f9fa;
      --accent: #1f7a5f;
    }}
    body {{
      margin: 0;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: #ffffff;
    }}
    main {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 32px 20px 48px;
    }}
    header {{
      border-bottom: 1px solid var(--line);
      padding-bottom: 20px;
      margin-bottom: 24px;
    }}
    h1 {{
      font-size: 32px;
      line-height: 1.15;
      margin: 0 0 8px;
      letter-spacing: 0;
    }}
    h2 {{
      font-size: 18px;
      margin: 30px 0 12px;
      letter-spacing: 0;
    }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
      gap: 10px;
      margin: 18px 0 0;
    }}
    .summary section, .signals section {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
    }}
    h3 {{
      margin: 0 0 8px;
      font-size: 13px;
      color: var(--muted);
      font-weight: 650;
    }}
    p {{
      margin: 0;
      font-size: 20px;
      font-weight: 720;
    }}
    span {{
      display: block;
      margin-top: 6px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.4;
    }}
    .signals {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 10px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    th, td {{
      border-bottom: 1px solid var(--line);
      padding: 10px 8px;
      text-align: left;
    }}
    th {{
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0;
    }}
    .plots {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 14px;
    }}
    .plots img {{
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
    }}
    a {{ color: var(--accent); }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Earthmoving Simulation Review</h1>
      <span>Terrain deformation, soil calibration, randomized scale, and sim-to-field diagnostics.</span>
      <div class="summary">
        <section><h3>Gate Status</h3><p>{html.escape(summary['gate_status'])}</p></section>
        <section><h3>Throughput</h3><p>{summary['episodes_per_second']:.2f}/s</p></section>
        <section><h3>Best Scenario</h3><p>{html.escape(summary['best_scenario'])}</p></section>
        <section><h3>Deposit Progress</h3><p>{summary.get('mean_deposit_forward_progress', 0.0):.3f} m</p></section>
        <section><h3>Calibration Error</h3><p>{summary['mean_calibration_error']:.4f}</p></section>
      </div>
    </header>
    <h2>Readiness Signals</h2>
    <div class="signals">{signals}</div>
    <h2>Scenario Results</h2>
    <table>
      <thead><tr><th>Scenario</th><th>Moved Volume</th><th>Deposit Progress</th><th>Terrain RMSE</th><th>Volume Error</th><th>Runtime</th></tr></thead>
      <tbody>{scenario_rows}</tbody>
    </table>
    <h2>Top Sensitivities</h2>
    <table>
      <thead><tr><th>Soil Parameter</th><th>Metric</th><th>Correlation</th></tr></thead>
      <tbody>{sensitivity_rows}</tbody>
    </table>
    <h2>Terrain Plots</h2>
    <div class="plots">
      <img src="../earthmoving_benchmark/baseline_push_terrain.png" alt="baseline push terrain">
      <img src="../earthmoving_benchmark/cohesive_soil_terrain.png" alt="cohesive soil terrain">
      <img src="../earthmoving_benchmark/shallow_blade_slip_terrain.png" alt="shallow blade slip terrain">
    </div>
  </main>
</body>
</html>
"""
