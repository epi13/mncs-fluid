# Architecture

## Layers

1. **Domain/fields** — grids/meshes, cells/faces/nodes, fields, regions and ghost/halo data.
2. **Equations/discretization** — fluxes, gradients, divergence, Laplacian/stencil operators and boundary conditions.
3. **Time integration** — explicit/implicit stepping, timestep selection and stability/CFL contracts.
4. **Linear/nonlinear solve** — pressure/Poisson systems, iterative methods, preconditioning and convergence evidence.
5. **Flow models** — incompressible baseline followed by broader models only after verified foundations.
6. **Parallel execution** — threading, SIMD, domain decomposition and CUDA kernels.
7. **Verification** — conservation, residuals, manufactured solutions, benchmark cases and mesh/time convergence.

## Status (first canonical implementation)

Layer coverage after the foundation slice (all MNCS-native,
Profile 0.18, except language-provided float ops and
`mncs-numerics` scalar discipline):

- Domain/fields: 1D channel lanes implemented (`grid1d`);
  node-vs-face location semantics explicit (`stencil1d`,
  `derived`). N-D fields, halos: deferred (pressures
  P-FLUID-FIELD, P-FLUID-MESH).
- Equations/discretization: steady viscous operator + FTCS
  update + oriented face fluxes, all guarded (`stencil1d`).
- Time integration: fixed-count explicit drivers (8/32 steps),
  `SimClock` as data, r <= 1/2 gate with structured `Unstable`
  evidence. Implicit/adaptive: deferred.
- Solve: native Thomas (constant-coefficient) + native Jacobi
  with residuals and fixed-count convergence drivers. Generic
  sparse: pressure P-FLUID-SOLVER.
- Flow models: steady + transient plane Poiseuille
  (incompressible, laminar, Newtonian). Everything else deferred
  (see FLUID_MODEL.md).
- Parallel: not attempted (correctness first).
- Verification: 74 native tests + 48-check exact oracle;
  analytic, conservation, refinement (Q 2nd-order, shear
  1st-order), symmetry, limiting (zero-drive), cross-solver
  agreement, fixed-point formulation agreement.

## First milestones

1. Structured field/grid and boundary-condition primitives. DONE
   (`grid1d`, `bc`, `props`).
2. Verified differential/stencil operators. DONE (`stencil1d` +
   oracle nodal-exactness proof).
3. Poisson solver with reference cases. SUPERSEDED: the viscous
   system is solved directly (Thomas/Jacobi); a standalone
   pressure-Poisson awaits a 2D formulation that needs it.
4. Simple incompressible flow solver. DONE (`model1d`: steady +
   transient Poiseuille).
5. Conservation and mesh/time convergence corpus. DONE
   (`derived`, refinement tests, oracle).
6. CPU/CUDA pressure and domain-decomposition experiments.
   DEFERRED (no verified parallel semantics to preserve yet).
