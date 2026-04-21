# Application Packet

Autonomous earthmoving simulation portfolio packet

A focused MuJoCo construction-autonomy simulation project showing terrain deformation, jobsite productivity scoring, task-plan evaluation, robustness analysis, and native-kernel performance.

Best entry point: [outputs/hiring_manager_packet/hiring_manager_packet.md](outputs/hiring_manager_packet/hiring_manager_packet.md)

## Proof Points

- Nominal best task plan `single_pass_wide_cut` reaches `7.65` m3/hr and is marked `release_candidate`.
- Robustness sweep pass rate is `50%` with P10 productivity `6.45` m3/hr.
- Top robustness driver is `soil.blade_coupling`, giving a concrete calibration/telemetry priority.
- Batch scale evaluation runs `60` randomized episodes at `287.91` episodes/s.
- C++ terrain-kernel benchmark reports `7.65x` speedup over Python.

## Links

- `hiring_manager_packet`: [outputs/hiring_manager_packet/hiring_manager_packet.md](outputs/hiring_manager_packet/hiring_manager_packet.md)
- `simulation_packet`: [EARTHMOVING_SIMULATION_PACKET.md](EARTHMOVING_SIMULATION_PACKET.md)
- `field_trial_case_study`: [outputs/field_trial_case_study/field_trial_case_study.md](outputs/field_trial_case_study/field_trial_case_study.md)
- `task_plan_robustness`: [outputs/task_plan_robustness/task_plan_robustness.md](outputs/task_plan_robustness/task_plan_robustness.md)
- `robustness_sensitivity`: [outputs/robustness_sensitivity/robustness_sensitivity.md](outputs/robustness_sensitivity/robustness_sensitivity.md)
- `terrain_kernel`: [cpp/terrain_kernel.cpp](cpp/terrain_kernel.cpp)

## Honest Limitations

- The terrain model is a lightweight heightmap approximation, not a production soil solver.
- Field logs are synthetic and used to demonstrate calibration workflow until real machine data is available.
- The selected task plan clears nominal gates but needs more robustness work before field-trial confidence.

## Message

```text
Hi [Name], I applied for Bedrock's Simulation Engineer role and wanted to send a focused technical artifact. I built a MuJoCo-based autonomous earthmoving simulation track with deformable terrain, jobsite productivity scoring, task-plan evaluation, robustness sweeps, sensitivity analysis, and a native terrain-kernel benchmark. The best entry point is `outputs/hiring_manager_packet/hiring_manager_packet.md`; it includes the limitations and the next calibration steps clearly. I would be grateful if you would be open to taking a look or pointing me toward the right person on the simulation team.
```