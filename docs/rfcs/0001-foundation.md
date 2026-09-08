# RFC 0001: CFD foundation

Status: Draft

## Principles

- Governing equations, discretization and boundary conditions are part of the declared computation.
- Stability constraints such as timestep/CFL are explicit and observable.
- Solvers expose residual, convergence, iteration and failure evidence.
- Conservation and mesh/time convergence are first-class verification criteria.
- Reproducible modes define reduction/order expectations across parallel execution.
- Acceleration may alter layout and scheduling but must preserve the declared numerical contract.

## Pressure objectives

Multidimensional arrays and views, stencil/halo operations, sparse iterative solvers, generic dimensions/scalars, memory layout control, parallel loops/reductions, domain decomposition, ghost-cell ownership, SIMD, CUDA, asynchronous data movement and structured convergence/stability failures.
