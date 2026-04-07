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

  const supportCases = document.getElementById("support-cases");
  (data.support_cases || []).forEach((entry) => {
    const a = document.createElement("a");
    a.href = `../${entry.path}`;
    a.textContent = entry.name;
    a.target = "_blank";
    supportCases.appendChild(a);
  });
}

main();
