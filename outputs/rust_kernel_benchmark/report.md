# Rust Terrain Kernel Benchmark

Repeats: `200`
Python mean: `0.206484` ms
Rust mean: `0.023014` ms
Rust speedup: `8.97x`
Moved-volume delta: `0.00000000`
End-volume delta: `0.00000000`

| kernel | elapsed_ms | mean_ms | moved_volume | end_volume |
| --- | ---: | ---: | ---: | ---: |
| Python | 41.296875 | 0.206484 | 0.00118709 | 0.00296961 |
| Rust FFI | 4.602833 | 0.023014 | 0.00118709 | 0.00296961 |