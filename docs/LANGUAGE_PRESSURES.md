# MNCS language pressure ledger

Record workload, observed behavior, required semantic, reproducer, owner, workaround and closure verification.

## How to read this ledger

Each entry: ID, workload, observed behavior, smallest reproducer,
required semantic, candidate owner, workaround in this repo, status.
A fast field update is not enough to close a pressure item;
validated numerical behavior must survive the change.

## P-FLUID-FIELD — length-generic outcome types (blocking for generality)

- Workload: every kernel returning a profile (`explicit_step`,
  `jacobi_*`, `trap_sum`, Thomas) plus a validation verdict.
- Observed: outcome enums/records cannot carry `[f64; N]` for
  generic N. `let` requires a type annotation, and `Wrap<4>`-style
  Nat application is not valid annotation syntax (MNP053); the
  binding `let w = ...` without annotation is refused (MNP051).
  Probes: `/tmp` probe3/probe4 (generic record/enum over Nat).
- Required: nameable length-generic nominal types, or generic-enum
  variants inferred at call sites.
- Candidate owner: `mncs-language` (type system), not Fluid.
- Workaround: split validation (scalar outcome enums) from total
  bare-array kernels, plus per-size concrete outcome enums
  (`Solve3/Solve7`, `Channel3/5/9`) in the FEM precedent.
- Status: OPEN. Cost is real: model1d carries 3 near-identical
  finish chains (~1 size per new grid). A generic-field repository
  must wait for this language capability; building one now would
  pour concrete around the workaround.

## P-FLUID-SOLVER — generic sparse/iterative solver home (non-blocking)

- Workload: steady viscous solve; future pressure-Poisson systems.
- Observed: no canonical f64 linear-system solver exists anywhere
  (same gap as FEM pressure F-001). Fluid implements Thomas for its
  own constant-coefficient system and Jacobi sweeps natively, both
  marked as Fluid-owned method code, not generic infrastructure.
- Required: canonical home for variable-coefficient tridiagonal /
  sparse iterative solves with residual/convergence contracts.
- Candidate owner: `mncs-math` (or a future numerical component).
- Workaround: none needed at this scale; no reference-backend
  bridge required (unlike FEM's solveref1d) because Thomas is
  native. Do NOT mistake tridiag.mncs for the canonical solver.
- Status: OPEN, non-blocking for 1D; blocking for 2D cavity flow.

## P-FLUID-UNITS — dimensional analysis (non-blocking)

- Workload: density/viscosity/geometry/solution quantities with SI
  units; Reynolds number dimensionlessness.
- Observed: no reusable dimension/unit system in MNCS today. Units
  live as documented contracts beside constructors; the types
  enforce positivity/validity outcomes, not dimensions.
- Required: generic dimensional-analysis support (quantity kinds,
  coherent derived units, dimensionless markers).
- Candidate owner: a generic owner (Numeric/Math ecosystem), not a
  private Fluid units system.
- Workaround: SI-per-field documentation + distinct record types
  for quantities where cheap (`FluidProps`, `DrivingForce`).
- Status: OPEN, non-blocking (no unit confusion occurred; the
  discipline held by review, not by types).

## P-FLUID-MESH — generic mesh topology (non-blocking)

- Workload: 1D channel lanes/faces; future 2D control volumes.
- Observed: `ChannelGrid` is deliberately Fluid-specific (walls,
  interiors, faces of one slice). No canonical generic mesh exists
  that fits without forcing (FEM owns FE topology; Geometry owns
  primitives, not connectivity).
- Required: decision on where generic mesh/connectivity lives when
  a second consumer needs it.
- Candidate owner: TBD (Geometry extension vs new topology home).
- Workaround: Fluid-local descriptor; no second mesh built.
- Status: OPEN, non-blocking (one consumer).

## P-FLUID-SELECT — eager `select` vs guarded indexing (guidance, closed in-repo)

- Workload: wall-lane guards around neighbor reads `u[i-1]`.
- Observed: `select` evaluates both candidates eagerly (confirmed
  in `mncs.core.geometry` docs); only `if`-branches are lazy
  (confirmed by FEM guard patterns + probe::neighbor_read).
- Required: nothing new — but every future stencil author must
  know: guards go in `if`, never in `select` arms.
- Workaround: if-guard + early-return lane functions throughout.
- Status: CLOSED by discipline; recorded so the next formulation
  does not rediscover it by trapping.

## P-FLUID-LITERAL — sequence-literal inference at generic calls (guidance)

- Workload: passing `[0.0, ...]` directly to `<N: Nat>` kernels.
- Observed: MNE183 (exact/bounded-view expected type required).
  Binding first (`let u: [f64; 5] = [...]`) then passing works
  (inference from bound values, Profile 0.13).
- Required: nothing new; call-site discipline.
- Workaround: always bind arrays with annotations before generic
  calls, in src and tests.
- Status: CLOSED by discipline.

## Initial pressure targets (from foundation RFC — status)

- Ergonomic N-dimensional arrays/slices/views: 1D fixed arrays
  suffice here; N-D stays OPEN (no 2D workload yet).
- Compile-time/runtime dimensions: Nat-generics + inference work
  for kernels; generic nominal types do not (P-FLUID-FIELD).
- Stencil iteration and neighbor access: PROVEN (traversal +
  guarded u64 indexing, `replace` incl. computed indices).
- Halo/ghost ownership: NOT NEEDED (single-process slice).
- Sparse iterative solvers: Jacobi pattern proven; generic home
  OPEN (P-FLUID-SOLVER).
- Deterministic reductions: traversal-order independence by
  construction (reads-old/writes-new); single-backend
  determinism verified (reruns green).
- Parallel loops/SIMD/CUDA/domain decomposition: NOT ATTEMPTED
  (correctness first, per campaign).
- Structured stability/convergence diagnostics: PROVEN
  (`StepCheck`, `Stability`, residuals, `ZeroPivot` as data).
