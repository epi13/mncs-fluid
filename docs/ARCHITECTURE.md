# Architecture

## Layers

1. **Domain/fields** — grids/meshes, cells/faces/nodes, fields, regions and ghost/halo data.
2. **Equations/discretization** — fluxes, gradients, divergence, Laplacian/stencil operators and boundary conditions.
3. **Time integration** — explicit/implicit stepping, timestep selection and stability/CFL contracts.
4. **Linear/nonlinear solve** — pressure/Poisson systems, iterative methods, preconditioning and convergence evidence.
5. **Flow models** — incompressible baseline followed by broader models only after verified foundations.
6. **Parallel execution** — threading, SIMD, domain decomposition and CUDA kernels.
7. **Verification** — conservation, residuals, manufactured solutions, benchmark cases and mesh/time convergence.

## First milestones

1. Structured field/grid and boundary-condition primitives.
2. Verified differential/stencil operators.
3. Poisson solver with reference cases.
4. Simple incompressible flow solver.
5. Conservation and mesh/time convergence corpus.
6. CPU/CUDA pressure and domain-decomposition experiments.
