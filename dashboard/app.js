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

  const randomizationBox = document.getElementById("randomization-summary");
  const randomizationRows = data.randomization_summary?.rows || [];
  if (randomizationRows.length > 0) {
    const grouped = new Map();
    randomizationRows.forEach((row) => {
      if (!grouped.has(row.controller)) grouped.set(row.controller, []);
      grouped.get(row.controller).push(row);
    });
    const summaries = [];
    grouped.forEach((rows, controller) => {
      const success = rows.reduce((acc, row) => acc + row.success, 0) / rows.length;
      const finalError = rows.reduce((acc, row) => acc + row.final_error, 0) / rows.length;
      summaries.push(`<p><strong>${controller}</strong>: ${(success * 100).toFixed(1)}% success, ${finalError.toFixed(4)} mean final error</p>`);
    });
    randomizationBox.innerHTML = summaries.join("");
  } else {
    randomizationBox.textContent = "Domain-randomization artifacts have not been generated yet.";
  }

  const caseStudyLinks = document.getElementById("case-study-links");
  const caseStudies = data.case_studies || {};
  Object.entries(caseStudies).forEach(([name, path]) => {
    const a = document.createElement("a");
    a.href = `../${path}`;
    a.textContent = name.replaceAll("_", " ");
    a.target = "_blank";
    caseStudyLinks.appendChild(a);
  });
  if (data.artifacts?.case_study_image) {
    document.getElementById("case-study-image").src = `../${data.artifacts.case_study_image}`;
  }

  const regressionSummary = document.getElementById("regression-summary");
  if (data.regression_diff?.scalar_deltas) {
    const blocks = Object.entries(data.regression_diff.scalar_deltas).map(
      ([key, value]) => `<p><strong>${key}</strong>: ${Number(value).toFixed(4)}</p>`
    );
    regressionSummary.innerHTML = blocks.join("");
  } else {
    regressionSummary.textContent = "Regression diff artifacts have not been generated yet.";
  }
  if (data.artifacts?.regression_diff_image) {
    document.getElementById("regression-image").src = `../${data.artifacts.regression_diff_image}`;
  }

  const regressionGate = document.getElementById("regression-gate");
  if (data.regression_gate) {
    const violations = data.regression_gate.violations || [];
    const summary = [
      `<p><strong>Status:</strong> ${data.regression_gate.status.toUpperCase()}</p>`,
      `<p><strong>Violations:</strong> ${data.regression_gate.violation_count}</p>`,
    ];
    if (violations.length > 0) {
      summary.push("<p><strong>Triggered checks:</strong></p>");
      violations.forEach((violation) => {
        const target = violation.controller
          ? `${violation.metric} / ${violation.controller}`
          : violation.metric;
        summary.push(`<p>${target}: ${violation.message}</p>`);
      });
    } else {
      summary.push("<p>All configured thresholds are passing.</p>");
    }
    regressionGate.innerHTML = summary.join("");
  } else {
    regressionGate.textContent = "Regression gate artifacts have not been generated yet.";
  }

  const regressionHistory = document.getElementById("regression-history-summary");
  if (data.regression_history?.trend_summary) {
    const snapshots = data.regression_history.snapshots || [];
    const items = [
      `<p><strong>Snapshots tracked:</strong> ${snapshots.length}</p>`,
    ];
    Object.entries(data.regression_history.trend_summary).forEach(([metric, summary]) => {
      items.push(
        `<p><strong>${metric}</strong>: ${summary.direction}, delta ${Number(summary.delta).toFixed(4)}, latest ${Number(summary.latest).toFixed(4)}</p>`
      );
    });
    regressionHistory.innerHTML = items.join("");
  } else {
    regressionHistory.textContent = "Regression history artifacts have not been generated yet.";
  }
  if (data.artifacts?.regression_history_image) {
    document.getElementById("regression-history-image").src = `../${data.artifacts.regression_history_image}`;
  }

  const provenance = document.getElementById("provenance-summary");
  if (data.provenance_index?.summary) {
    const summary = data.provenance_index.summary;
    const manifests = data.provenance_index.manifests || [];
    const blocks = [
      `<p><strong>Manifest count:</strong> ${summary.manifest_count}</p>`,
      `<p><strong>Run types:</strong> ${(summary.run_types || []).join(", ")}</p>`,
      `<p><strong>Latest Git HEAD:</strong> ${summary.latest_git_head || "n/a"}</p>`,
    ];
    manifests.slice(0, 5).forEach((manifest) => {
      blocks.push(
        `<p><strong>${manifest.run_type}</strong>: ${manifest.created_at} | ${manifest.manifest_path}</p>`
      );
    });
    provenance.innerHTML = blocks.join("");
  } else {
    provenance.textContent = "Provenance index artifacts have not been generated yet.";
  }

  const releaseNotes = document.getElementById("release-notes-summary");
  if (data.release_notes) {
    const items = [
      `<p><strong>Comparison:</strong> ${data.release_notes.base_ref} -> ${data.release_notes.head_ref}</p>`,
      `<p><strong>Commits:</strong> ${data.release_notes.commit_count}</p>`,
      `<p><strong>Diffstat:</strong> ${data.release_notes.diffstat || "n/a"}</p>`,
      `<p><strong>Regression gate:</strong> ${data.release_notes.regression_gate.status} (${data.release_notes.regression_gate.violation_count} violations)</p>`,
    ];
    Object.entries(data.release_notes.changed_areas || {}).forEach(([area, count]) => {
      items.push(`<p><strong>${area}</strong>: ${count} files</p>`);
    });
    releaseNotes.innerHTML = items.join("");
  } else {
    releaseNotes.textContent = "Release note artifacts have not been generated yet.";
  }

  const anomalySummary = document.getElementById("anomaly-summary");
  if (data.anomalies) {
    const items = [];
    (data.anomalies.benchmark_anomalies?.top_cases || []).slice(0, 3).forEach((row) => {
      items.push(`<p><strong>${row.scenario} / ${row.controller}</strong>: risk ${Number(row.risk_score).toFixed(3)}</p>`);
    });
    (data.anomalies.parameter_effects || []).slice(0, 2).forEach((row) => {
      items.push(`<p><strong>${row.parameter}</strong>: corr ${Number(row.correlation_with_difficulty).toFixed(3)}</p>`);
    });
    anomalySummary.innerHTML = items.join("");
  } else {
    anomalySummary.textContent = "Anomaly artifacts have not been generated yet.";
  }
  if (data.artifacts?.anomaly_benchmark_image) {
    document.getElementById("anomaly-benchmark-image").src = `../${data.artifacts.anomaly_benchmark_image}`;
  }
  if (data.artifacts?.anomaly_difficulty_image) {
    document.getElementById("anomaly-difficulty-image").src = `../${data.artifacts.anomaly_difficulty_image}`;
  }
}

main();
