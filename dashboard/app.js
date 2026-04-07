async function main() {
  const response = await fetch("./data.json");
  const data = await response.json();

  const success = data.baseline_summary ? data.baseline_summary.success_rate : null;
  document.getElementById("success-rate").textContent = success === null ? "--" : `${(success * 100).toFixed(1)}%`;

  const envList = document.getElementById("environment-list");
  const env = data.environment || {};
  const items = [
    ["Python", env.platform?.python_version],
    ["MuJoCo", env.runtime?.mujoco_version],
    ["NumPy", env.runtime?.numpy_version],
    ["System", `${env.platform?.system || ""} ${env.platform?.release || ""}`.trim()],
    ["Git HEAD", env.tooling?.git_head],
  ];
  items.forEach(([label, value]) => {
    const li = document.createElement("li");
    li.textContent = `${label}: ${value || "n/a"}`;
    envList.appendChild(li);
  });

  const learning = document.getElementById("learning-summary");
  if (data.learning_training) {
    learning.innerHTML = `
      <p><strong>Best val loss:</strong> ${data.learning_training.best_val_loss.toFixed(4)}</p>
      <p><strong>Epochs:</strong> ${data.learning_training.epochs}</p>
      <p><strong>Final train loss:</strong> ${data.learning_training.final_train_loss.toFixed(4)}</p>
      <p><strong>Final val loss:</strong> ${data.learning_training.final_val_loss.toFixed(4)}</p>
    `;
  } else {
    learning.textContent = "Training artifacts have not been generated yet.";
  }

  const evalBox = document.getElementById("policy-eval");
  if (data.learning_evaluation?.summary) {
    evalBox.innerHTML = `
      <p><strong>Success rate:</strong> ${(data.learning_evaluation.summary.success_rate * 100).toFixed(1)}%</p>
      <p><strong>Final error:</strong> ${data.learning_evaluation.summary.final_error_mean.toFixed(4)}</p>
      <p><strong>Overshoot:</strong> ${data.learning_evaluation.summary.max_overshoot_mean.toFixed(4)}</p>
    `;
  } else {
    evalBox.textContent = "Evaluation artifacts have not been generated yet.";
  }

  const rlSummary = document.getElementById("rl-summary");
  if (data.rl_training) {
    rlSummary.innerHTML = `
      <p><strong>Iterations:</strong> ${data.rl_training.iterations}</p>
      <p><strong>Final return:</strong> ${data.rl_training.final_return.toFixed(3)}</p>
      <p><strong>Final success:</strong> ${(data.rl_training.final_success_rate * 100).toFixed(1)}%</p>
      <p><strong>Policy std:</strong> ${data.rl_training.policy_std.toFixed(3)}</p>
    `;
  } else {
    rlSummary.textContent = "RL adaptation artifacts have not been generated yet.";
  }

  const rlEval = document.getElementById("rl-eval");
  if (data.rl_evaluation?.summary) {
    rlEval.innerHTML = `
      <p><strong>Success rate:</strong> ${(data.rl_evaluation.summary.success_rate * 100).toFixed(1)}%</p>
      <p><strong>Final error:</strong> ${data.rl_evaluation.summary.final_error_mean.toFixed(4)}</p>
      <p><strong>Control energy:</strong> ${data.rl_evaluation.summary.control_energy_mean.toFixed(2)}</p>
    `;
  } else {
    rlEval.textContent = "RL evaluation artifacts have not been generated yet.";
  }

  const artifactLinks = document.getElementById("artifact-links");
  Object.entries(data.artifacts || {}).forEach(([name, path]) => {
    const a = document.createElement("a");
    a.href = `../${path}`;
    a.textContent = name.replaceAll("_", " ");
    a.target = "_blank";
    artifactLinks.appendChild(a);
  });

  if (data.artifacts?.demo_gif) {
    document.getElementById("demo-gif").src = `../${data.artifacts.demo_gif}`;
  }
  if (data.artifacts?.training_curve) {
    document.getElementById("training-curve").src = `../${data.artifacts.training_curve}`;
  }
  if (data.artifacts?.rl_training_curve) {
    document.getElementById("rl-training-curve").src = `../${data.artifacts.rl_training_curve}`;
  }

  const supportCases = document.getElementById("support-cases");
  (data.support_cases || []).forEach((entry) => {
    const a = document.createElement("a");
    a.href = `../${entry.path}`;
    a.textContent = entry.name;
    a.target = "_blank";
    supportCases.appendChild(a);
  });

  const benchmarkBox = document.getElementById("benchmark-summary");
  const benchmarkRows = data.benchmark_summary?.benchmark_rows || [];
  if (benchmarkRows.length > 0) {
    const scenarioMap = new Map();
    benchmarkRows.forEach((row) => {
      if (!scenarioMap.has(row.scenario)) scenarioMap.set(row.scenario, []);
      scenarioMap.get(row.scenario).push(row);
    });
    const blocks = [];
    scenarioMap.forEach((rows, scenario) => {
      const ordered = rows.slice().sort((a, b) => {
        if (b.success_rate !== a.success_rate) return b.success_rate - a.success_rate;
        return a.final_error_mean - b.final_error_mean;
      });
      const winner = ordered[0];
      blocks.push(`<p><strong>${scenario}</strong>: ${winner.controller} (${(winner.success_rate * 100).toFixed(1)}% success)</p>`);
    });
    benchmarkBox.innerHTML = blocks.join("");
  } else {
    benchmarkBox.textContent = "Benchmark artifacts have not been generated yet.";
  }
}

main();
