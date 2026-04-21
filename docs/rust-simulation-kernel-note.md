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

There is also a Python-facing FFI path:

```bash
make rust-terrain-kernel-benchmark
```

That compiles `rust/terrain_kernel_ffi.rs` as a `cdylib`, loads it with Python `ctypes`, and compares the Rust terrain update against the Python terrain update on the same workload. This is the most directly useful Rust pattern for this project: keep Python for experiment orchestration while moving hot, deterministic kernels into memory-safe native code.

The next serious Rust step would be one of:

- add a Cargo crate with unit tests and criterion benchmarks
- replace the `ctypes` bridge with a PyO3 package if the Rust path becomes part of the standard developer workflow
- compare Python, C++, and Rust kernels on the same terrain-update workload in CI where Rust is installed
- move replay/log ingestion into Rust for safe, parallel batch processing
