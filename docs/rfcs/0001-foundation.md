# RFC 0001: CFD foundation

Status: Partially implemented (foundation slice, 2026-09-26).
Superseded statements are marked below; the principles stand.

Implemented: governing equations/discretization/BCs as declared
computation (`stencil1d`, `bc`, `model1d`); stability gate r <= 1/2
as observable data (`StepCheck`/`Stability`); solver residual,
convergence, iteration-count and failure evidence (`jacobi`,
`tridiag` outcomes); conservation + measured mesh convergence as
first-class criteria (`derived`, refinement tests, oracle).

Deferred (deliberately, not by omission): parallel
reduction/order expectations (no parallel execution yet — a
correctness-first decision, not a gap in the proof); acceleration
layout/scheduling contracts (no accelerated path exists to
constrain); halo/ghost operations (single-process slice).

Pressure objectives status: stencil operations PROVEN in
1D; sparse iterative solver pattern PROVEN locally with the
generic home still OPEN (P-FLUID-SOLVER); structured
convergence/stability failures PROVEN as data. Multidimensional
arrays/views, memory layout control, parallel loops/reductions,
domain decomposition, ghost cells, SIMD, CUDA, async movement:
OPEN, correctly untouched until a verified solver exists whose
contract they must preserve.

## Principles

- Governing equations, discretization and boundary conditions are part of the declared computation.
- Stability constraints such as timestep/CFL are explicit and observable.
- Solvers expose residual, convergence, iteration and failure evidence.
- Conservation and mesh/time convergence are first-class verification criteria.
- Reproducible modes define reduction/order expectations across parallel execution.
- Acceleration may alter layout and scheduling but must preserve the declared numerical contract.

## Pressure objectives

Multidimensional arrays and views, stencil/halo operations, sparse iterative solvers, generic dimensions/scalars, memory layout control, parallel loops/reductions, domain decomposition, ghost-cell ownership, SIMD, CUDA, asynchronous data movement and structured convergence/stability failures.
