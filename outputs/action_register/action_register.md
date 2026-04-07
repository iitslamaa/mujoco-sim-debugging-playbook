# Action Register

- Actions: `3`

| priority | target | owner | action | reason |
| --- | --- | --- | --- | --- |
| high | low_damping_high_gain / expert_pd | simulation-debugging | Increase joint damping and reduce actuator gain before changing controller structure. | Current owner has a breaching item and should offload work to keep the queue moving. |
| high | low_damping_high_gain / hybrid_guardrail | simulation-debugging | Increase joint damping and reduce actuator gain before changing controller structure. | Current owner has a breaching item and should offload work to keep the queue moving. |
| medium | delay_heavy / expert_pd | simulation-debugging | Increase control frequency or use a more delay-tolerant guarded policy blend. | This item is at risk and benefits from parallel evidence gathering. |