# Escalation Matrix

Tracked triage items: `11`

Critical items: `5`

| severity | owner | target | escalation_trigger | escalation_path | incident_bundle |
| --- | --- | --- | --- | --- | --- |
| critical | simulation-debugging | episode 1 | Repeated zero-success episode under randomized dynamics | Escalate from self-serve debugging to simulator/policy review with incident bundle attached. | outputs/incidents/episode_1.md |
| critical | simulation-debugging | episode 14 | Repeated zero-success episode under randomized dynamics | Escalate from self-serve debugging to simulator/policy review with incident bundle attached. | outputs/incidents/episode_14.md |
| critical | simulation-debugging | episode 17 | Repeated zero-success episode under randomized dynamics | Escalate from self-serve debugging to simulator/policy review with incident bundle attached. | outputs/incidents/episode_17.md |
| critical | simulation-debugging | episode 9 | Repeated zero-success episode under randomized dynamics | Escalate from self-serve debugging to simulator/policy review with incident bundle attached. | outputs/incidents/episode_9.md |
| critical | simulation-debugging | episode 5 | Repeated zero-success episode under randomized dynamics | Escalate from self-serve debugging to simulator/policy review with incident bundle attached. | outputs/incidents/episode_5.md |
| high | controls-and-policy | low_damping_high_gain / expert_pd | Sustained benchmark risk in a named stress scenario | Escalate to controls-and-policy owners after reproducing with fixed seeds. | -- |
| high | controls-and-policy | low_damping_high_gain / hybrid_guardrail | Sustained benchmark risk in a named stress scenario | Escalate to controls-and-policy owners after reproducing with fixed seeds. | -- |
| medium | controls-and-policy | noise_heavy / expert_pd | No hard escalation trigger met | Handle in support/self-serve workflow and update documentation if the mitigation is validated. | -- |
| medium | controls-and-policy | noise_heavy / hybrid_guardrail | No hard escalation trigger met | Handle in support/self-serve workflow and update documentation if the mitigation is validated. | -- |
| medium | controls-and-policy | delay_heavy / expert_pd | No hard escalation trigger met | Handle in support/self-serve workflow and update documentation if the mitigation is validated. | -- |
| low | maintainer-review | 9947b32 -> HEAD | No hard escalation trigger met | Handle in support/self-serve workflow and update documentation if the mitigation is validated. | -- |