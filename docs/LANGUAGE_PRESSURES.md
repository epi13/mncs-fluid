# MNCS language pressure ledger

Record workload, observed behavior, required semantic, reproducer, owner, workaround and closure verification.

## Initial pressure targets

- ergonomic N-dimensional arrays, slices and strided views
- compile-time/runtime dimensions without excessive overhead
- stencil iteration and neighbor access
- halo/ghost-region ownership and exchange
- sparse iterative solver abstractions
- deterministic/reproducible reductions
- parallel loop scheduling and locality
- SoA/AoS/tiled memory-layout control
- SIMD vectorization of stencil/flux kernels
- CUDA kernels and asynchronous transfers
- domain-decomposition communication boundaries
- structured stability/convergence diagnostics

A fast field update is not enough to close a pressure item; validated numerical behavior must survive the change.
