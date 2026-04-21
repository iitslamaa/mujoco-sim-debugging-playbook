# Rust Simulation Kernel Note

The core project uses Python for experiment tooling and C++ for a terrain-update performance benchmark. Rust is included as a small, optional kernel scaffold because it is relevant to robotics simulation infrastructure in a few practical ways:

- memory safety for long-running simulation and data services
- C/C++-class performance for geometry, terrain, and scenario-processing kernels
- predictable ownership and concurrency for parallel batch evaluation
- easier distribution of safe command-line tooling than large C++ applications
- good fit for simulation infrastructure, log processing, replay tools, and ML-data pipelines

In this repo, `rust/terrain_kernel.rs` mirrors the C++ terrain kernel shape. It is intentionally optional: the normal Python test suite does not require Rust to be installed. If Rust is available, run:

```bash
make rust-terrain-kernel-smoke
```

That builds the standalone Rust terrain kernel with `rustc -C opt-level=3` and runs a small repeat-count smoke test.

The next serious Rust step would be one of:

- add a Cargo crate with unit tests and criterion benchmarks
- bind the Rust terrain kernel into Python via PyO3 or a C ABI
- compare Python, C++, and Rust kernels on the same terrain-update workload
- move replay/log ingestion into Rust for safe, parallel batch processing
