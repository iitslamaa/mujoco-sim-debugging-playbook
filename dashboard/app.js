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

  const recommendationSummary = document.getElementById("recommendation-summary");
  if (data.recommendations?.recommendations) {
    const items = [];
    data.recommendations.recommendations.slice(0, 5).forEach((row) => {
      items.push(`<p><strong>${row.target}</strong>: ${row.recommendation}</p>`);
      items.push(`<p>${row.evidence}</p>`);
    });
    recommendationSummary.innerHTML = items.join("");
  } else {
    recommendationSummary.textContent = "Recommendation artifacts have not been generated yet.";
  }

  const triageSummary = document.getElementById("triage-summary");
  if (data.triage?.items) {
    const items = [];
    data.triage.items.slice(0, 6).forEach((row) => {
      items.push(`<p><strong>${row.target}</strong> (${row.kind}, ${Number(row.priority_score).toFixed(1)}): ${row.next_action}</p>`);
    });
    triageSummary.innerHTML = items.join("");
  } else {
    triageSummary.textContent = "Triage queue artifacts have not been generated yet.";
  }

  const incidentSummary = document.getElementById("incident-summary");
  if (data.incidents?.bundles) {
    const items = [];
    data.incidents.bundles.slice(0, 5).forEach((bundle) => {
      items.push(`<p><strong>${bundle.id}</strong> ${bundle.target}: ${bundle.next_action}</p>`);
    });
    incidentSummary.innerHTML = items.join("");
  } else {
    incidentSummary.textContent = "Incident bundle artifacts have not been generated yet.";
  }

  const knowledgeBaseSummary = document.getElementById("knowledge-base-summary");
  if (data.knowledge_base?.entries) {
    const items = [];
    data.knowledge_base.entries.slice(0, 5).forEach((entry) => {
      items.push(`<p><strong>${entry.id}</strong>: ${entry.question}</p>`);
    });
    knowledgeBaseSummary.innerHTML = items.join("");
  } else {
    knowledgeBaseSummary.textContent = "Knowledge base artifacts have not been generated yet.";
  }

  const escalationSummary = document.getElementById("escalation-summary");
  if (data.escalation?.items) {
    const items = [];
    data.escalation.items.slice(0, 5).forEach((row) => {
      items.push(`<p><strong>${row.target}</strong>: ${row.severity} / ${row.owner} / ${row.escalation_path}</p>`);
    });
    escalationSummary.innerHTML = items.join("");
  } else {
    escalationSummary.textContent = "Escalation artifacts have not been generated yet.";
  }

  const supportOpsSummary = document.getElementById("support-ops-summary");
  if (data.support_ops?.summary) {
    const summary = data.support_ops.summary;
    const items = [
      `<p><strong>Queue count:</strong> ${summary.queue_count}</p>`,
      `<p><strong>Incident coverage:</strong> ${(summary.incident_coverage * 100).toFixed(1)}%</p>`,
      `<p><strong>Knowledge base coverage:</strong> ${(summary.knowledge_base_coverage * 100).toFixed(1)}%</p>`,
      `<p><strong>Escalated items:</strong> ${summary.escalated_count}</p>`,
      `<p><strong>Self-serve items:</strong> ${summary.self_serve_count}</p>`,
    ];
    supportOpsSummary.innerHTML = items.join("");
  } else {
    supportOpsSummary.textContent = "Support ops artifacts have not been generated yet.";
  }

  const supportGapSummary = document.getElementById("support-gap-summary");
  if (data.support_gaps?.summary) {
    const summary = data.support_gaps.summary;
    const items = [
      `<p><strong>Needs follow-up:</strong> ${summary.needs_follow_up_count}</p>`,
      `<p><strong>Fully covered:</strong> ${summary.fully_covered_count}</p>`,
      `<p><strong>Critical gaps:</strong> ${summary.uncovered_critical_count}</p>`,
      `<p><strong>Top gap:</strong> ${summary.top_gap_target || "n/a"}</p>`,
    ];
    (data.support_gaps.items || []).slice(0, 4).forEach((item) => {
      const missing = item.missing_artifacts.length > 0 ? item.missing_artifacts.join(", ") : "none";
      items.push(
        `<p><strong>${item.target}</strong>: gap ${item.gap_score.toFixed(2)} | missing ${missing}</p>`
      );
    });
    supportGapSummary.innerHTML = items.join("");
  } else {
    supportGapSummary.textContent = "Support gap artifacts have not been generated yet.";
  }

  const workstreamSummary = document.getElementById("workstream-summary");
  if (data.workstreams?.summary) {
    const summary = data.workstreams.summary;
    const items = [
      `<p><strong>Active lanes:</strong> ${summary.lane_count}</p>`,
      `<p><strong>Planned items:</strong> ${summary.item_count}</p>`,
      `<p><strong>Blocking items:</strong> ${summary.blocking_count}</p>`,
      `<p><strong>Estimated points:</strong> ${summary.estimated_points}</p>`,
      `<p><strong>Top lane:</strong> ${summary.top_lane || "n/a"}</p>`,
    ];
    (data.workstreams.lanes || []).slice(0, 3).forEach((lane) => {
      items.push(
        `<p><strong>${lane.lane}</strong>: ${lane.item_count} items, ${lane.blocking_count} blocking, ${lane.estimated_points} pts</p>`
      );
    });
    workstreamSummary.innerHTML = items.join("");
  } else {
    workstreamSummary.textContent = "Workstream planning artifacts have not been generated yet.";
  }

  const slaSummary = document.getElementById("sla-summary");
  if (data.sla?.summary) {
    const summary = data.sla.summary;
    const items = [
      `<p><strong>At risk:</strong> ${summary.at_risk_count}</p>`,
      `<p><strong>Breaches:</strong> ${summary.breach_count}</p>`,
      `<p><strong>Next due target:</strong> ${summary.next_due_target || "n/a"}</p>`,
      `<p><strong>Slowest lane:</strong> ${summary.slowest_lane || "n/a"}</p>`,
    ];
    (data.sla.items || []).slice(0, 4).forEach((item) => {
      items.push(
        `<p><strong>${item.target}</strong>: ${item.status}, due ${item.due_date}, ${item.estimated_days} day estimate</p>`
      );
    });
    slaSummary.innerHTML = items.join("");
  } else {
    slaSummary.textContent = "Delivery forecast artifacts have not been generated yet.";
  }

  const capacitySummary = document.getElementById("capacity-summary");
  if (data.capacity?.summary) {
    const summary = data.capacity.summary;
    const items = [
      `<p><strong>Overloaded owners:</strong> ${summary.overloaded_owner_count}</p>`,
      `<p><strong>Rebalance candidates:</strong> ${summary.rebalance_item_count}</p>`,
      `<p><strong>Highest-pressure lane:</strong> ${summary.highest_pressure_lane || "n/a"}</p>`,
    ];
    (data.capacity.owners || []).slice(0, 3).forEach((owner) => {
      items.push(
        `<p><strong>${owner.owner}</strong>: ${owner.status}, ${owner.effort_points} pts, ${owner.breach_count} breaches</p>`
      );
    });
    (data.capacity.rebalance_items || []).slice(0, 3).forEach((item) => {
      items.push(
        `<p><strong>${item.target}</strong>: ${item.current_owner} -> ${item.recommended_owner}</p>`
      );
    });
    capacitySummary.innerHTML = items.join("");
  } else {
    capacitySummary.textContent = "Capacity planning artifacts have not been generated yet.";
  }

  const opsReviewSummary = document.getElementById("ops-review-summary");
  if (data.ops_review?.summary) {
    const summary = data.ops_review.summary;
    const items = [
      `<p><strong>Queue count:</strong> ${summary.queue_count}</p>`,
      `<p><strong>Breaches / at risk:</strong> ${summary.breach_count} / ${summary.at_risk_count}</p>`,
      `<p><strong>Highest-pressure lane:</strong> ${summary.highest_pressure_lane}</p>`,
      `<p><strong>Top gap:</strong> ${summary.top_gap_target}</p>`,
    ];
    (data.ops_review.wins || []).slice(0, 2).forEach((entry) => {
      items.push(`<p><strong>Win:</strong> ${entry}</p>`);
    });
    (data.ops_review.risks || []).slice(0, 2).forEach((entry) => {
      items.push(`<p><strong>Risk:</strong> ${entry}</p>`);
    });
    (data.ops_review.next_actions || []).slice(0, 2).forEach((item) => {
      items.push(`<p><strong>${item.target}</strong>: ${item.owner} -> ${item.action}</p>`);
    });
    opsReviewSummary.innerHTML = items.join("");
  } else {
    opsReviewSummary.textContent = "Ops review artifacts have not been generated yet.";
  }

  const supportReadinessSummary = document.getElementById("support-readiness-summary");
  if (data.support_readiness?.summary) {
    const summary = data.support_readiness.summary;
    const items = [
      `<p><strong>Status:</strong> ${summary.status}</p>`,
      `<p><strong>Failures:</strong> ${summary.failure_count}</p>`,
      `<p><strong>Warnings:</strong> ${summary.warning_count}</p>`,
    ];
    (data.support_readiness.checks || []).slice(0, 5).forEach((check) => {
      items.push(`<p><strong>${check.name}</strong>: ${check.status} | ${check.message}</p>`);
    });
    supportReadinessSummary.innerHTML = items.join("");
  } else {
    supportReadinessSummary.textContent = "Support readiness artifacts have not been generated yet.";
  }

  const scenarioPlanSummary = document.getElementById("scenario-plan-summary");
  if (data.scenario_plan?.baseline) {
    const baseline = data.scenario_plan.baseline;
    const items = [
      `<p><strong>Baseline:</strong> ${baseline.status} (${baseline.failure_count} failures, ${baseline.warning_count} warnings)</p>`,
    ];
    (data.scenario_plan.scenarios || []).forEach((scenario) => {
      items.push(
        `<p><strong>${scenario.name}</strong>: ${scenario.status} (${scenario.failure_count} failures, ${scenario.warning_count} warnings)</p>`
      );
    });
    scenarioPlanSummary.innerHTML = items.join("");
  } else {
    scenarioPlanSummary.textContent = "Scenario planning artifacts have not been generated yet.";
  }

  const artifactFreshnessSummary = document.getElementById("artifact-freshness-summary");
  if (data.artifact_freshness?.summary) {
    const summary = data.artifact_freshness.summary;
    const items = [
      `<p><strong>Fresh:</strong> ${summary.fresh_count}</p>`,
      `<p><strong>Stale:</strong> ${summary.stale_count}</p>`,
      `<p><strong>Missing:</strong> ${summary.missing_count}</p>`,
    ];
    (data.artifact_freshness.rows || []).slice(0, 6).forEach((row) => {
      items.push(`<p><strong>${row.artifact}</strong>: ${row.status}</p>`);
    });
    artifactFreshnessSummary.innerHTML = items.join("");
  } else {
    artifactFreshnessSummary.textContent = "Artifact freshness artifacts have not been generated yet.";
  }

  const regenerationPlanSummary = document.getElementById("regeneration-plan-summary");
  if (data.regeneration_plan?.summary) {
    const summary = data.regeneration_plan.summary;
    const items = [
      `<p><strong>Actions:</strong> ${summary.count}</p>`,
      `<p><strong>High priority:</strong> ${summary.high_priority_count}</p>`,
    ];
    (data.regeneration_plan.actions || []).slice(0, 6).forEach((action) => {
      items.push(`<p><strong>${action.artifact}</strong>: ${action.priority} | ${action.command}</p>`);
    });
    regenerationPlanSummary.innerHTML = items.join("");
  } else {
    regenerationPlanSummary.textContent = "Regeneration plan artifacts have not been generated yet.";
  }

  const dependencyMapSummary = document.getElementById("dependency-map-summary");
  if (data.dependency_map?.summary) {
    const summary = data.dependency_map.summary;
    const items = [
      `<p><strong>Artifacts mapped:</strong> ${summary.artifact_count}</p>`,
      `<p><strong>Max dependencies:</strong> ${summary.max_dependency_count}</p>`,
    ];
    (data.dependency_map.rows || []).slice(0, 6).forEach((row) => {
      items.push(
        `<p><strong>${row.artifact}</strong>: ${row.dependency_count} deps, ${row.existing_dependency_count} present</p>`
      );
    });
    dependencyMapSummary.innerHTML = items.join("");
  } else {
    dependencyMapSummary.textContent = "Dependency map artifacts have not been generated yet.";
  }

  const impactAnalysisSummary = document.getElementById("impact-analysis-summary");
  if (data.impact_analysis?.summary) {
    const summary = data.impact_analysis.summary;
    const items = [
      `<p><strong>Dependencies tracked:</strong> ${summary.dependency_count}</p>`,
      `<p><strong>Most impactful dependency:</strong> ${summary.most_impactful_dependency || "n/a"}</p>`,
      `<p><strong>Max impact count:</strong> ${summary.max_impact_count}</p>`,
    ];
    (data.impact_analysis.rows || []).slice(0, 6).forEach((row) => {
      items.push(`<p><strong>${row.dependency}</strong>: ${row.impact_count} downstream artifacts</p>`);
    });
    impactAnalysisSummary.innerHTML = items.join("");
  } else {
    impactAnalysisSummary.textContent = "Impact analysis artifacts have not been generated yet.";
  }

  const refreshBundleSummary = document.getElementById("refresh-bundle-summary");
  if (data.refresh_bundle?.summary) {
    const summary = data.refresh_bundle.summary;
    const items = [
      `<p><strong>Bundles:</strong> ${summary.bundle_count}</p>`,
      `<p><strong>Actions:</strong> ${summary.action_count}</p>`,
    ];
    (data.refresh_bundle.bundles || []).forEach((bundle) => {
      items.push(
        `<p><strong>${bundle.bundle}</strong>: ${bundle.action_count} actions, ${bundle.high_priority_count} high priority</p>`
      );
    });
    refreshBundleSummary.innerHTML = items.join("");
  } else {
    refreshBundleSummary.textContent = "Refresh bundle artifacts have not been generated yet.";
  }

  const refreshChecklistSummary = document.getElementById("refresh-checklist-summary");
  if (data.refresh_checklist?.summary) {
    const summary = data.refresh_checklist.summary;
    const items = [
      `<p><strong>Bundles:</strong> ${summary.bundle_count}</p>`,
      `<p><strong>Total steps:</strong> ${summary.total_steps}</p>`,
    ];
    (data.refresh_checklist.bundles || []).forEach((bundle) => {
      items.push(
        `<p><strong>${bundle.bundle}</strong>: ${bundle.step_count} steps, validate ${bundle.validation_target}</p>`
      );
    });
    refreshChecklistSummary.innerHTML = items.join("");
  } else {
    refreshChecklistSummary.textContent = "Refresh checklist artifacts have not been generated yet.";
  }

  const maintenanceRiskSummary = document.getElementById("maintenance-risk-summary");
  if (data.maintenance_risk?.summary) {
    const summary = data.maintenance_risk.summary;
    const items = [
      `<p><strong>Artifacts scored:</strong> ${summary.artifact_count}</p>`,
      `<p><strong>High risk:</strong> ${summary.high_risk_count}</p>`,
      `<p><strong>Medium risk:</strong> ${summary.medium_risk_count}</p>`,
      `<p><strong>Top risk artifact:</strong> ${summary.top_risk_artifact || "n/a"}</p>`,
      `<p><strong>Top risk score:</strong> ${Number(summary.top_risk_score || 0).toFixed(3)}</p>`,
    ];
    (data.maintenance_risk.rows || []).slice(0, 5).forEach((row) => {
      items.push(
        `<p><strong>${row.artifact}</strong>: ${row.status}, ${row.priority}, score ${Number(row.risk_score).toFixed(3)}</p>`
      );
    });
    maintenanceRiskSummary.innerHTML = items.join("");
  } else {
    maintenanceRiskSummary.textContent = "Maintenance risk artifacts have not been generated yet.";
  }

  const artifactReadinessSummary = document.getElementById("artifact-readiness-summary");
  if (data.artifact_readiness?.summary) {
    const summary = data.artifact_readiness.summary;
    const items = [
      `<p><strong>Status:</strong> ${summary.status}</p>`,
      `<p><strong>Failures:</strong> ${summary.failure_count}</p>`,
      `<p><strong>Warnings:</strong> ${summary.warning_count}</p>`,
      `<p><strong>Top risk artifact:</strong> ${summary.top_risk_artifact || "n/a"}</p>`,
      `<p><strong>Stale artifacts:</strong> ${summary.stale_count}</p>`,
      `<p><strong>Refresh steps:</strong> ${summary.refresh_step_count}</p>`,
    ];
    (data.artifact_readiness.checks || []).forEach((check) => {
      items.push(`<p><strong>${check.name}</strong>: ${check.status} | ${check.message}</p>`);
    });
    artifactReadinessSummary.innerHTML = items.join("");
  } else {
    artifactReadinessSummary.textContent = "Artifact readiness artifacts have not been generated yet.";
  }

  const artifactScenariosSummary = document.getElementById("artifact-scenarios-summary");
  if (data.artifact_scenarios?.baseline) {
    const baseline = data.artifact_scenarios.baseline;
    const items = [
      `<p><strong>Baseline:</strong> ${baseline.status} (${baseline.failure_count} failures, ${baseline.warning_count} warnings)</p>`,
    ];
    (data.artifact_scenarios.scenarios || []).forEach((scenario) => {
      items.push(
        `<p><strong>${scenario.name}</strong>: ${scenario.status}, ${scenario.stale_count} stale, ${scenario.refresh_step_count} steps</p>`
      );
    });
    artifactScenariosSummary.innerHTML = items.join("");
  } else {
    artifactScenariosSummary.textContent = "Artifact scenario artifacts have not been generated yet.";
  }

  const artifactRecoverySummary = document.getElementById("artifact-recovery-summary");
  if (data.artifact_recovery?.summary) {
    const summary = data.artifact_recovery.summary;
    const items = [
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Current failures:</strong> ${summary.current_failure_count}</p>`,
      `<p><strong>Phases:</strong> ${summary.phase_count}</p>`,
      `<p><strong>Top risk artifact:</strong> ${summary.top_risk_artifact || "n/a"}</p>`,
      `<p><strong>Target status:</strong> ${summary.target_status}</p>`,
    ];
    (data.artifact_recovery.phases || []).forEach((phase) => {
      items.push(
        `<p><strong>Phase ${phase.phase}: ${phase.name}</strong> -> ${phase.expected_status}, ${phase.expected_failure_count} failures</p>`
      );
    });
    artifactRecoverySummary.innerHTML = items.join("");
  } else {
    artifactRecoverySummary.textContent = "Artifact recovery artifacts have not been generated yet.";
  }

  const artifactDeliverySummary = document.getElementById("artifact-delivery-summary");
  if (data.artifact_delivery?.summary) {
    const summary = data.artifact_delivery.summary;
    const items = [
      `<p><strong>Phases:</strong> ${summary.phase_count}</p>`,
      `<p><strong>At risk:</strong> ${summary.at_risk_count}</p>`,
      `<p><strong>Breaches:</strong> ${summary.breach_count}</p>`,
      `<p><strong>Next due phase:</strong> ${summary.next_due_phase || "n/a"}</p>`,
      `<p><strong>Slowest phase:</strong> ${summary.slowest_phase || "n/a"}</p>`,
    ];
    (data.artifact_delivery.phases || []).forEach((phase) => {
      items.push(
        `<p><strong>Phase ${phase.phase}: ${phase.name}</strong> -> ${phase.status}, due ${phase.due_date}, max risk ${Number(phase.max_risk_score).toFixed(3)}</p>`
      );
    });
    artifactDeliverySummary.innerHTML = items.join("");
  } else {
    artifactDeliverySummary.textContent = "Artifact delivery artifacts have not been generated yet.";
  }

  const artifactCapacitySummary = document.getElementById("artifact-capacity-summary");
  if (data.artifact_capacity?.summary) {
    const summary = data.artifact_capacity.summary;
    const items = [
      `<p><strong>Owners tracked:</strong> ${summary.owner_count}</p>`,
      `<p><strong>Overloaded owners:</strong> ${summary.overloaded_owner_count}</p>`,
      `<p><strong>Phases tracked:</strong> ${summary.phase_count}</p>`,
      `<p><strong>Rebalance items:</strong> ${summary.rebalance_item_count}</p>`,
      `<p><strong>Highest-pressure phase:</strong> ${summary.highest_pressure_phase || "n/a"}</p>`,
    ];
    (data.artifact_capacity.phases || []).forEach((phase) => {
      items.push(
        `<p><strong>${phase.name}</strong>: ${phase.status}, owner ${phase.owner}, shift ${phase.suggested_capacity_shift}</p>`
      );
    });
    artifactCapacitySummary.innerHTML = items.join("");
  } else {
    artifactCapacitySummary.textContent = "Artifact capacity artifacts have not been generated yet.";
  }

  const artifactExecSummary = document.getElementById("artifact-exec-summary");
  if (data.artifact_exec_summary?.summary) {
    const summary = data.artifact_exec_summary.summary;
    const items = [
      `<p><strong>Status:</strong> ${summary.status}</p>`,
      `<p><strong>Failures:</strong> ${summary.failure_count}</p>`,
      `<p><strong>Top risk artifact:</strong> ${summary.top_risk_artifact || "n/a"}</p>`,
      `<p><strong>Breach phase:</strong> ${summary.breach_phase || "n/a"}</p>`,
      `<p><strong>Overloaded owner:</strong> ${summary.overloaded_owner || "n/a"}</p>`,
    ];
    (data.artifact_exec_summary.wins || []).slice(0, 2).forEach((win) => {
      items.push(`<p><strong>Win:</strong> ${win}</p>`);
    });
    (data.artifact_exec_summary.risks || []).slice(0, 2).forEach((risk) => {
      items.push(`<p><strong>Risk:</strong> ${risk}</p>`);
    });
    artifactExecSummary.innerHTML = items.join("");
  } else {
    artifactExecSummary.textContent = "Artifact executive summary has not been generated yet.";
  }

  const artifactHistorySummary = document.getElementById("artifact-history-summary");
  if (data.artifact_history?.summary) {
    const summary = data.artifact_history.summary;
    const items = [
      `<p><strong>Snapshots:</strong> ${summary.snapshot_count}</p>`,
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Projected terminal status:</strong> ${summary.projected_terminal_status}</p>`,
      `<p><strong>Status direction:</strong> ${summary.status_direction}</p>`,
      `<p><strong>Failure direction:</strong> ${summary.failure_direction}</p>`,
      `<p><strong>Top risk direction:</strong> ${summary.top_risk_direction}</p>`,
    ];
    (data.artifact_history.snapshots || []).forEach((snapshot) => {
      items.push(
        `<p><strong>${snapshot.name}</strong>: ${snapshot.status}, ${snapshot.failure_count} failures, risk ${Number(snapshot.top_risk_score).toFixed(3)}</p>`
      );
    });
    artifactHistorySummary.innerHTML = items.join("");
  } else {
    artifactHistorySummary.textContent = "Artifact history has not been generated yet.";
  }

  const artifactActionsSummary = document.getElementById("artifact-actions-summary");
  if (data.artifact_actions?.summary) {
    const summary = data.artifact_actions.summary;
    const items = [
      `<p><strong>Actions:</strong> ${summary.action_count}</p>`,
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Projected terminal status:</strong> ${summary.projected_terminal_status}</p>`,
      `<p><strong>Top risk artifact:</strong> ${summary.top_risk_artifact || "n/a"}</p>`,
    ];
    (data.artifact_actions.actions || []).forEach((action) => {
      items.push(
        `<p><strong>${action.priority}</strong> ${action.target}: ${action.owner} -> ${action.expected_impact}</p>`
      );
    });
    artifactActionsSummary.innerHTML = items.join("");
  } else {
    artifactActionsSummary.textContent = "Artifact actions have not been generated yet.";
  }

  const artifactAlertsSummary = document.getElementById("artifact-alerts-summary");
  if (data.artifact_alerts?.summary) {
    const summary = data.artifact_alerts.summary;
    const items = [
      `<p><strong>Alerts:</strong> ${summary.alert_count}</p>`,
      `<p><strong>Critical:</strong> ${summary.critical_count}</p>`,
      `<p><strong>Warning:</strong> ${summary.warning_count}</p>`,
      `<p><strong>Info:</strong> ${summary.info_count}</p>`,
    ];
    (data.artifact_alerts.alerts || []).forEach((alert) => {
      items.push(
        `<p><strong>${alert.severity}</strong> ${alert.title}: ${alert.message}</p>`
      );
    });
    artifactAlertsSummary.innerHTML = items.join("");
  } else {
    artifactAlertsSummary.textContent = "Artifact alerts have not been generated yet.";
  }

  const artifactDigestSummary = document.getElementById("artifact-digest-summary");
  if (data.artifact_digest?.summary) {
    const summary = data.artifact_digest.summary;
    const items = [
      `<p><strong>Headlines:</strong> ${summary.headline_count}</p>`,
      `<p><strong>Critical alerts:</strong> ${summary.critical_alert_count}</p>`,
      `<p><strong>Top actions:</strong> ${summary.action_count}</p>`,
      `<p><strong>Projected terminal status:</strong> ${summary.projected_terminal_status}</p>`,
    ];
    (data.artifact_digest.headlines || []).forEach((headline) => {
      items.push(`<p>${headline}</p>`);
    });
    artifactDigestSummary.innerHTML = items.join("");
  } else {
    artifactDigestSummary.textContent = "Artifact digest has not been generated yet.";
  }

  const artifactHandoffSummary = document.getElementById("artifact-handoff-summary");
  if (data.artifact_handoff?.summary) {
    const summary = data.artifact_handoff.summary;
    const items = [
      `<p><strong>Status:</strong> ${summary.status}</p>`,
      `<p><strong>Top risk artifact:</strong> ${summary.top_risk_artifact || "n/a"}</p>`,
      `<p><strong>Breach phase:</strong> ${summary.breach_phase || "n/a"}</p>`,
      `<p><strong>Handoff owner:</strong> ${summary.handoff_owner || "n/a"}</p>`,
      `<p><strong>Critical alerts:</strong> ${summary.critical_alert_count}</p>`,
    ];
    (data.artifact_handoff.actions || []).forEach((action) => {
      items.push(
        `<p><strong>${action.priority}</strong> ${action.target} -> ${action.owner}: ${action.expected_impact}</p>`
      );
    });
    artifactHandoffSummary.innerHTML = items.join("");
  } else {
    artifactHandoffSummary.textContent = "Artifact handoff has not been generated yet.";
  }

  const artifactReviewNoteSummary = document.getElementById("artifact-review-note-summary");
  if (data.artifact_review_note?.summary) {
    const summary = data.artifact_review_note.summary;
    const items = [
      `<p><strong>Status:</strong> ${summary.status}</p>`,
      `<p><strong>Projected terminal status:</strong> ${summary.projected_terminal_status}</p>`,
      `<p><strong>Changed items:</strong> ${summary.changed_count}</p>`,
      `<p><strong>Blockers:</strong> ${summary.blocker_count}</p>`,
      `<p><strong>Approval items:</strong> ${summary.approval_count}</p>`,
    ];
    (data.artifact_review_note.blockers || []).forEach((blocker) => {
      items.push(`<p><strong>Blocker:</strong> ${blocker}</p>`);
    });
    artifactReviewNoteSummary.innerHTML = items.join("");
  } else {
    artifactReviewNoteSummary.textContent = "Artifact review note has not been generated yet.";
  }

  const artifactCloseoutSummary = document.getElementById("artifact-closeout-summary");
  if (data.artifact_closeout?.summary) {
    const summary = data.artifact_closeout.summary;
    const items = [
      `<p><strong>Status:</strong> ${summary.status}</p>`,
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Projected terminal status:</strong> ${summary.projected_terminal_status}</p>`,
      `<p><strong>Blockers:</strong> ${summary.blocker_count}</p>`,
      `<p><strong>Remaining actions:</strong> ${summary.remaining_action_count}</p>`,
      `<p><strong>Handoff owner:</strong> ${summary.handoff_owner || "n/a"}</p>`,
    ];
    (data.artifact_closeout.closeout_checks || []).forEach((check) => {
      items.push(`<p><strong>${check.name}</strong>: ${check.status} | ${check.message}</p>`);
    });
    artifactCloseoutSummary.innerHTML = items.join("");
  } else {
    artifactCloseoutSummary.textContent = "Artifact closeout has not been generated yet.";
  }

  const artifactScorecardSummary = document.getElementById("artifact-scorecard-summary");
  if (data.artifact_scorecard?.summary) {
    const summary = data.artifact_scorecard.summary;
    const items = [
      `<p><strong>Metrics:</strong> ${summary.metric_count}</p>`,
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Closeout status:</strong> ${summary.closeout_status}</p>`,
      `<p><strong>Projected terminal status:</strong> ${summary.projected_terminal_status}</p>`,
    ];
    (data.artifact_scorecard.metrics || []).forEach((metric) => {
      items.push(`<p><strong>${metric.name}</strong>: ${metric.value}</p>`);
    });
    artifactScorecardSummary.innerHTML = items.join("");
  } else {
    artifactScorecardSummary.textContent = "Artifact scorecard has not been generated yet.";
  }

  const artifactPacketSummary = document.getElementById("artifact-packet-summary");
  if (data.artifact_packet?.summary) {
    const summary = data.artifact_packet.summary;
    const items = [
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Closeout status:</strong> ${summary.closeout_status}</p>`,
      `<p><strong>Projected terminal status:</strong> ${summary.projected_terminal_status}</p>`,
      `<p><strong>Headlines:</strong> ${summary.headline_count}</p>`,
      `<p><strong>Handoff owner:</strong> ${summary.handoff_owner}</p>`,
      `<p><strong>Remaining actions:</strong> ${summary.remaining_action_count}</p>`,
    ];
    (data.artifact_packet.digest?.headlines || []).forEach((headline) => {
      items.push(`<p>${headline}</p>`);
    });
    artifactPacketSummary.innerHTML = items.join("");
  } else {
    artifactPacketSummary.textContent = "Artifact packet has not been generated yet.";
  }

  const dashboardSnapshotSummary = document.getElementById("dashboard-snapshot-summary");
  if (data.dashboard_snapshot) {
    const snapshot = data.dashboard_snapshot;
    const items = [
      `<p><strong>Name:</strong> ${snapshot.name}</p>`,
      `<p><strong>Date:</strong> ${snapshot.date}</p>`,
      `<p><strong>Baseline success rate:</strong> ${Number(snapshot.baseline_success_rate).toFixed(3)}</p>`,
      `<p><strong>Current status:</strong> ${snapshot.artifact_summary.current_status}</p>`,
      `<p><strong>Closeout status:</strong> ${snapshot.artifact_summary.closeout_status}</p>`,
      `<p><strong>Projected terminal status:</strong> ${snapshot.artifact_summary.projected_terminal_status}</p>`,
    ];
    (snapshot.highlights || []).forEach((highlight) => {
      items.push(`<p>${highlight}</p>`);
    });
    dashboardSnapshotSummary.innerHTML = items.join("");
  } else {
    dashboardSnapshotSummary.textContent = "Dashboard snapshot has not been generated yet.";
  }

  const dashboardSnapshotHistorySummary = document.getElementById("dashboard-snapshot-history-summary");
  if (data.dashboard_snapshot_history?.summary) {
    const summary = data.dashboard_snapshot_history.summary;
    const items = [
      `<p><strong>Snapshots:</strong> ${summary.snapshot_count}</p>`,
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Status direction:</strong> ${summary.status_direction}</p>`,
      `<p><strong>Projected terminal status:</strong> ${summary.projected_terminal_status}</p>`,
    ];
    (data.dashboard_snapshot_history.snapshots || []).forEach((snapshot) => {
      items.push(
        `<p><strong>${snapshot.name}</strong>: ${snapshot.status}, ${snapshot.failure_count} failures, risk ${Number(snapshot.top_risk_score).toFixed(3)}</p>`
      );
    });
    dashboardSnapshotHistorySummary.innerHTML = items.join("");
  } else {
    dashboardSnapshotHistorySummary.textContent = "Dashboard snapshot history has not been generated yet.";
  }

  const dashboardSnapshotDriftSummary = document.getElementById("dashboard-snapshot-drift-summary");
  if (data.dashboard_snapshot_drift?.summary) {
    const summary = data.dashboard_snapshot_drift.summary;
    const items = [
      `<p><strong>Transitions:</strong> ${summary.transition_count}</p>`,
      `<p><strong>First pass snapshot:</strong> ${summary.first_pass_snapshot}</p>`,
      `<p><strong>Largest failure drop:</strong> ${summary.largest_failure_drop_transition} (${summary.largest_failure_drop})</p>`,
      `<p><strong>Largest risk drop:</strong> ${summary.largest_risk_drop_transition} (${Number(summary.largest_risk_drop).toFixed(3)})</p>`,
    ];
    (data.dashboard_snapshot_drift.transitions || []).forEach((transition) => {
      items.push(
        `<p><strong>${transition.from} -> ${transition.to}</strong>: ${transition.failure_delta} failures, risk ${Number(transition.risk_delta).toFixed(3)}</p>`
      );
    });
    dashboardSnapshotDriftSummary.innerHTML = items.join("");
  } else {
    dashboardSnapshotDriftSummary.textContent = "Dashboard snapshot drift has not been generated yet.";
  }

  const dashboardSnapshotAlertsSummary = document.getElementById("dashboard-snapshot-alerts-summary");
  if (data.dashboard_snapshot_alerts?.summary) {
    const summary = data.dashboard_snapshot_alerts.summary;
    const items = [
      `<p><strong>Alerts:</strong> ${summary.alert_count}</p>`,
      `<p><strong>Critical:</strong> ${summary.critical_count}</p>`,
      `<p><strong>Warning:</strong> ${summary.warning_count}</p>`,
      `<p><strong>Info:</strong> ${summary.info_count}</p>`,
    ];
    (data.dashboard_snapshot_alerts.alerts || []).forEach((alert) => {
      items.push(`<p><strong>[${alert.severity}] ${alert.title}</strong>: ${alert.message}</p>`);
    });
    dashboardSnapshotAlertsSummary.innerHTML = items.join("");
  } else {
    dashboardSnapshotAlertsSummary.textContent = "Dashboard snapshot alerts have not been generated yet.";
  }

  const dashboardSnapshotMonitorSummary = document.getElementById("dashboard-snapshot-monitor-summary");
  if (data.dashboard_snapshot_monitor?.summary) {
    const summary = data.dashboard_snapshot_monitor.summary;
    const items = [
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Projected terminal status:</strong> ${summary.projected_terminal_status}</p>`,
      `<p><strong>Headlines:</strong> ${summary.headline_count}</p>`,
      `<p><strong>Alerts:</strong> ${summary.alert_count}</p>`,
      `<p><strong>Critical alerts:</strong> ${summary.critical_count}</p>`,
      `<p><strong>Dominant transition:</strong> ${summary.dominant_transition}</p>`,
    ];
    (data.dashboard_snapshot_monitor.headlines || []).forEach((headline) => {
      items.push(`<p>${headline}</p>`);
    });
    if (data.dashboard_snapshot_monitor.highest_priority_alert) {
      const alert = data.dashboard_snapshot_monitor.highest_priority_alert;
      items.push(`<p><strong>[${alert.severity}] ${alert.title}</strong>: ${alert.message}</p>`);
    }
    dashboardSnapshotMonitorSummary.innerHTML = items.join("");
  } else {
    dashboardSnapshotMonitorSummary.textContent = "Dashboard snapshot monitor has not been generated yet.";
  }

  const dashboardSnapshotReviewSummary = document.getElementById("dashboard-snapshot-review-summary");
  if (data.dashboard_snapshot_review?.summary) {
    const summary = data.dashboard_snapshot_review.summary;
    const items = [
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Projected terminal status:</strong> ${summary.projected_terminal_status}</p>`,
      `<p><strong>Headlines:</strong> ${summary.headline_count}</p>`,
      `<p><strong>Critical alerts:</strong> ${summary.critical_count}</p>`,
      `<p><strong>Blockers:</strong> ${summary.blocker_count}</p>`,
      `<p><strong>Next focus:</strong> ${summary.next_focus}</p>`,
    ];
    (data.dashboard_snapshot_review.headlines || []).forEach((headline) => {
      items.push(`<p>${headline}</p>`);
    });
    if (data.dashboard_snapshot_review.top_alert) {
      const alert = data.dashboard_snapshot_review.top_alert;
      items.push(`<p><strong>[${alert.severity}] ${alert.title}</strong>: ${alert.message}</p>`);
    }
    (data.dashboard_snapshot_review.blockers || []).forEach((blocker) => {
      items.push(`<p>${blocker}</p>`);
    });
    dashboardSnapshotReviewSummary.innerHTML = items.join("");
  } else {
    dashboardSnapshotReviewSummary.textContent = "Dashboard snapshot review has not been generated yet.";
  }

  const dashboardSnapshotHandoffSummary = document.getElementById("dashboard-snapshot-handoff-summary");
  if (data.dashboard_snapshot_handoff?.summary) {
    const summary = data.dashboard_snapshot_handoff.summary;
    const items = [
      `<p><strong>Handoff owner:</strong> ${summary.handoff_owner}</p>`,
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Projected terminal status:</strong> ${summary.projected_terminal_status}</p>`,
      `<p><strong>Blockers:</strong> ${summary.blocker_count}</p>`,
      `<p><strong>Top items:</strong> ${summary.top_item_count}</p>`,
      `<p><strong>Dominant transition:</strong> ${summary.dominant_transition}</p>`,
    ];
    (data.dashboard_snapshot_handoff.top_items || []).forEach((item) => {
      items.push(`<p>${item}</p>`);
    });
    (data.dashboard_snapshot_handoff.headlines || []).forEach((headline) => {
      items.push(`<p>${headline}</p>`);
    });
    dashboardSnapshotHandoffSummary.innerHTML = items.join("");
  } else {
    dashboardSnapshotHandoffSummary.textContent = "Dashboard snapshot handoff has not been generated yet.";
  }

  const dashboardSnapshotCloseoutSummary = document.getElementById("dashboard-snapshot-closeout-summary");
  if (data.dashboard_snapshot_closeout?.summary) {
    const summary = data.dashboard_snapshot_closeout.summary;
    const items = [
      `<p><strong>Closeout status:</strong> ${summary.closeout_status}</p>`,
      `<p><strong>Handoff owner:</strong> ${summary.handoff_owner}</p>`,
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Projected terminal status:</strong> ${summary.projected_terminal_status}</p>`,
      `<p><strong>Remaining items:</strong> ${summary.remaining_item_count}</p>`,
      `<p><strong>Blockers:</strong> ${summary.blocker_count}</p>`,
    ];
    (data.dashboard_snapshot_closeout.remaining_items || []).forEach((item) => {
      items.push(`<p>${item}</p>`);
    });
    (data.dashboard_snapshot_closeout.blockers || []).forEach((blocker) => {
      items.push(`<p>${blocker}</p>`);
    });
    dashboardSnapshotCloseoutSummary.innerHTML = items.join("");
  } else {
    dashboardSnapshotCloseoutSummary.textContent = "Dashboard snapshot closeout has not been generated yet.";
  }

  const dashboardSnapshotScorecardSummary = document.getElementById("dashboard-snapshot-scorecard-summary");
  if (data.dashboard_snapshot_scorecard?.summary) {
    const summary = data.dashboard_snapshot_scorecard.summary;
    const items = [
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Projected terminal status:</strong> ${summary.projected_terminal_status}</p>`,
      `<p><strong>Closeout status:</strong> ${summary.closeout_status}</p>`,
      `<p><strong>Handoff owner:</strong> ${summary.handoff_owner}</p>`,
      `<p><strong>Headlines:</strong> ${summary.headline_count}</p>`,
      `<p><strong>Alerts:</strong> ${summary.alert_count}</p>`,
      `<p><strong>Critical alerts:</strong> ${summary.critical_count}</p>`,
      `<p><strong>Blockers:</strong> ${summary.blocker_count}</p>`,
      `<p><strong>Remaining items:</strong> ${summary.remaining_item_count}</p>`,
      `<p><strong>Dominant transition:</strong> ${summary.dominant_transition}</p>`,
    ];
    dashboardSnapshotScorecardSummary.innerHTML = items.join("");
  } else {
    dashboardSnapshotScorecardSummary.textContent = "Dashboard snapshot scorecard has not been generated yet.";
  }

  const dashboardSnapshotDigestSummary = document.getElementById("dashboard-snapshot-digest-summary");
  if (data.dashboard_snapshot_digest?.summary) {
    const summary = data.dashboard_snapshot_digest.summary;
    const items = [
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Closeout status:</strong> ${summary.closeout_status}</p>`,
      `<p><strong>Handoff owner:</strong> ${summary.handoff_owner}</p>`,
      `<p><strong>Headlines:</strong> ${summary.headline_count}</p>`,
      `<p><strong>Attention points:</strong> ${summary.attention_count}</p>`,
    ];
    (data.dashboard_snapshot_digest.headlines || []).forEach((headline) => {
      items.push(`<p>${headline}</p>`);
    });
    (data.dashboard_snapshot_digest.attention_points || []).forEach((point) => {
      items.push(`<p>${point}</p>`);
    });
    (data.dashboard_snapshot_digest.remaining_items || []).forEach((item) => {
      items.push(`<p>${item}</p>`);
    });
    dashboardSnapshotDigestSummary.innerHTML = items.join("");
  } else {
    dashboardSnapshotDigestSummary.textContent = "Dashboard snapshot digest has not been generated yet.";
  }

  const dashboardSnapshotActionsSummary = document.getElementById("dashboard-snapshot-actions-summary");
  if (data.dashboard_snapshot_actions?.summary) {
    const summary = data.dashboard_snapshot_actions.summary;
    const items = [
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Closeout status:</strong> ${summary.closeout_status}</p>`,
      `<p><strong>Handoff owner:</strong> ${summary.handoff_owner}</p>`,
      `<p><strong>Actions:</strong> ${summary.action_count}</p>`,
    ];
    (data.dashboard_snapshot_actions.actions || []).forEach((action) => {
      items.push(`<p><strong>[${action.priority}]</strong> ${action.title} (${action.owner})</p>`);
    });
    dashboardSnapshotActionsSummary.innerHTML = items.join("");
  } else {
    dashboardSnapshotActionsSummary.textContent = "Dashboard snapshot actions have not been generated yet.";
  }

  const dashboardSnapshotAlertPacketSummary = document.getElementById("dashboard-snapshot-alert-packet-summary");
  if (data.dashboard_snapshot_alert_packet?.summary) {
    const summary = data.dashboard_snapshot_alert_packet.summary;
    const items = [
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Handoff owner:</strong> ${summary.handoff_owner}</p>`,
      `<p><strong>Alerts:</strong> ${summary.alert_count}</p>`,
      `<p><strong>Critical:</strong> ${summary.critical_count}</p>`,
      `<p><strong>Warning:</strong> ${summary.warning_count}</p>`,
    ];
    (data.dashboard_snapshot_alert_packet.alerts || []).forEach((alert) => {
      items.push(`<p><strong>[${alert.severity}]</strong> ${alert.title} (${alert.owner})</p>`);
    });
    dashboardSnapshotAlertPacketSummary.innerHTML = items.join("");
  } else {
    dashboardSnapshotAlertPacketSummary.textContent = "Dashboard snapshot alert packet has not been generated yet.";
  }

  const dashboardSnapshotResolutionPlanSummary = document.getElementById("dashboard-snapshot-resolution-plan-summary");
  if (data.dashboard_snapshot_resolution_plan?.summary) {
    const summary = data.dashboard_snapshot_resolution_plan.summary;
    const items = [
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Handoff owner:</strong> ${summary.handoff_owner}</p>`,
      `<p><strong>Phases:</strong> ${summary.phase_count}</p>`,
      `<p><strong>Alerts:</strong> ${summary.alert_count}</p>`,
      `<p><strong>Critical alerts:</strong> ${summary.critical_count}</p>`,
    ];
    (data.dashboard_snapshot_resolution_plan.phases || []).forEach((phase) => {
      items.push(`<p><strong>${phase.name}</strong></p>`);
      (phase.items || []).forEach((item) => {
        items.push(`<p>[${phase.priority}] ${item}</p>`);
      });
    });
    dashboardSnapshotResolutionPlanSummary.innerHTML = items.join("");
  } else {
    dashboardSnapshotResolutionPlanSummary.textContent = "Dashboard snapshot resolution plan has not been generated yet.";
  }

  const dashboardSnapshotExecutionBoardSummary = document.getElementById("dashboard-snapshot-execution-board-summary");
  if (data.dashboard_snapshot_execution_board?.summary) {
    const summary = data.dashboard_snapshot_execution_board.summary;
    const items = [
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Handoff owner:</strong> ${summary.handoff_owner}</p>`,
      `<p><strong>Lanes:</strong> ${summary.lane_count}</p>`,
      `<p><strong>Active lanes:</strong> ${summary.active_lane_count}</p>`,
      `<p><strong>Planned lanes:</strong> ${summary.planned_lane_count}</p>`,
    ];
    (data.dashboard_snapshot_execution_board.lanes || []).forEach((lane) => {
      items.push(`<p><strong>${lane.lane}</strong>: ${lane.status}, ${lane.item_count} items</p>`);
      (lane.items || []).forEach((item) => {
        items.push(`<p>[${lane.priority}] ${item}</p>`);
      });
    });
    dashboardSnapshotExecutionBoardSummary.innerHTML = items.join("");
  } else {
    dashboardSnapshotExecutionBoardSummary.textContent = "Dashboard snapshot execution board has not been generated yet.";
  }

  const dashboardSnapshotOwnerLoadSummary = document.getElementById("dashboard-snapshot-owner-load-summary");
  if (data.dashboard_snapshot_owner_load?.summary) {
    const summary = data.dashboard_snapshot_owner_load.summary;
    const items = [
      `<p><strong>Owner:</strong> ${summary.owner}</p>`,
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Active lanes:</strong> ${summary.active_lane_count}</p>`,
      `<p><strong>Planned lanes:</strong> ${summary.planned_lane_count}</p>`,
      `<p><strong>Active items:</strong> ${summary.active_item_count}</p>`,
      `<p><strong>Planned items:</strong> ${summary.planned_item_count}</p>`,
      `<p><strong>Critical alerts:</strong> ${summary.critical_alert_count}</p>`,
      `<p><strong>Warning alerts:</strong> ${summary.warning_alert_count}</p>`,
    ];
    dashboardSnapshotOwnerLoadSummary.innerHTML = items.join("");
  } else {
    dashboardSnapshotOwnerLoadSummary.textContent = "Dashboard snapshot owner load has not been generated yet.";
  }

  const dashboardSnapshotReadinessGateSummary = document.getElementById("dashboard-snapshot-readiness-gate-summary");
  if (data.dashboard_snapshot_readiness_gate?.summary) {
    const summary = data.dashboard_snapshot_readiness_gate.summary;
    const items = [
      `<p><strong>Status:</strong> ${summary.status}</p>`,
      `<p><strong>Owner:</strong> ${summary.owner}</p>`,
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Failures:</strong> ${summary.failure_count}</p>`,
      `<p><strong>Warnings:</strong> ${summary.warning_count}</p>`,
    ];
    (data.dashboard_snapshot_readiness_gate.failures || []).forEach((failure) => {
      items.push(`<p>${failure}</p>`);
    });
    (data.dashboard_snapshot_readiness_gate.warnings || []).forEach((warning) => {
      items.push(`<p>${warning}</p>`);
    });
    dashboardSnapshotReadinessGateSummary.innerHTML = items.join("");
  } else {
    dashboardSnapshotReadinessGateSummary.textContent = "Dashboard snapshot readiness gate has not been generated yet.";
  }

  const dashboardSnapshotRecoveryForecastSummary = document.getElementById("dashboard-snapshot-recovery-forecast-summary");
  if (data.dashboard_snapshot_recovery_forecast?.summary) {
    const summary = data.dashboard_snapshot_recovery_forecast.summary;
    const items = [
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Projected next status:</strong> ${summary.projected_next_status}</p>`,
      `<p><strong>Confidence:</strong> ${summary.confidence}</p>`,
      `<p><strong>Phases:</strong> ${summary.phase_count}</p>`,
      `<p><strong>Critical alerts:</strong> ${summary.critical_count}</p>`,
    ];
    (data.dashboard_snapshot_recovery_forecast.rationale || []).forEach((item) => {
      items.push(`<p>${item}</p>`);
    });
    dashboardSnapshotRecoveryForecastSummary.innerHTML = items.join("");
  } else {
    dashboardSnapshotRecoveryForecastSummary.textContent = "Dashboard snapshot recovery forecast has not been generated yet.";
  }

  const dashboardSnapshotMilestonesSummary = document.getElementById("dashboard-snapshot-milestones-summary");
  if (data.dashboard_snapshot_milestones?.summary) {
    const summary = data.dashboard_snapshot_milestones.summary;
    const items = [
      `<p><strong>Current status:</strong> ${summary.current_status}</p>`,
      `<p><strong>Projected next status:</strong> ${summary.projected_next_status}</p>`,
      `<p><strong>Terminal status:</strong> ${summary.terminal_status}</p>`,
      `<p><strong>Confidence:</strong> ${summary.confidence}</p>`,
      `<p><strong>Milestones:</strong> ${summary.milestone_count}</p>`,
    ];
    (data.dashboard_snapshot_milestones.milestones || []).forEach((milestone) => {
      items.push(`<p><strong>${milestone.label}</strong>: ${milestone.status}</p>`);
    });
    dashboardSnapshotMilestonesSummary.innerHTML = items.join("");
  } else {
    dashboardSnapshotMilestonesSummary.textContent = "Dashboard snapshot milestones have not been generated yet.";
  }
}

main();
