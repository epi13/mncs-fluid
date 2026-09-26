#!/usr/bin/env python3
"""Independent oracle for the mncs-fluid plane-Poiseuille foundation.

Derives every committed expectation from first principles with exact
rational arithmetic (Fraction) plus IEEE-754 double cross-checks,
entirely independent of the MNCS implementation. Fails loudly on any
mismatch against the values pinned in tests/native/ and
docs/VERIFICATION.md.

Canonical parameters: H = 2 m, G = 4 Pa/m, mu = 1 Pa.s, rho = 1 kg/m^3.

Usage:
    python3 tools/oracle_fluid.py
"""

import struct
from fractions import Fraction as Q

FAILURES = []


def check(name, got, want):
    ok = got == want
    print("%-46s got=%s want=%s %s" % (name, got, want, "OK" if ok else "MISMATCH"))
    if not ok:
        FAILURES.append(name)


# --- analytic solution -----------------------------------------------------
# u(y) = G/(2 mu) y (H - y); umax = G H^2/8mu; Q = G H^3/12mu;
# tau = G H/2; umean = Q/H; Re = rho umean H / mu.
H, G, MU, RHO = Q(2), Q(4), Q(1), Q(1)


def analytic_u(y):
    return G / (2 * MU) * y * (H - y)


def main():
    umax = G * H * H / (8 * MU)
    qexact = G * H * H * H / (12 * MU)
    tau = G * H / 2
    umean = qexact / H
    re = RHO * umean * H / MU
    check("analytic center umax", umax, Q(2))
    check("analytic flow rate Q", qexact, Q(8, 3))
    check("analytic wall shear", tau, Q(4))
    check("analytic mean velocity", umean, Q(4, 3))
    check("Reynolds number", re, Q(8, 3))
    check("center == profile(H/2)", analytic_u(H / 2), umax)

    # --- discrete grids: nodal exactness of the scheme ---------------------
    # Interior system: -u[i-1] + 2u[i] - u[i+1] = rhs, rhs = G h^2/mu.
    # Solve EXACTLY (Fraction Gaussian elimination) and require the
    # discrete solution to equal the analytic profile at the nodes.
    for cells in (2, 4, 8):
        h = H / cells
        n = cells - 1
        rhs = G * h * h / MU
        # exact solve of the n-lane tridiagonal system
        a = [Q(-1)] * n
        b = [Q(2)] * n
        c = [Q(-1)] * n
        d = [rhs] * n
        for i in range(1, n):  # forward elimination
            w = a[i] / b[i - 1]
            b[i] = b[i] - w * c[i - 1]
            d[i] = d[i] - w * d[i - 1]
        x = [Q(0)] * n
        x[-1] = d[-1] / b[-1]
        for i in range(n - 2, -1, -1):
            x[i] = (d[i] - c[i] * x[i + 1]) / b[i]
        for k, xk in enumerate(x):
            y = (k + 1) * h
            check("cells=%d lane=%d nodal exactness" % (cells, k + 1), xk, analytic_u(y))
        full = [Q(0)] + x + [Q(0)]
        # trapezoidal flow rate and its error
        qtrap = h * sum(full)
        check("cells=%d trap Q" % cells, qtrap,
              {2: Q(2), 4: Q(5, 2), 8: Q(21, 8)}[cells])
        # one-sided wall shears
        slo = MU * (full[1] - full[0]) / h
        shi = MU * (full[-1] - full[-2]) / h
        check("cells=%d shear_lo" % cells, slo, {2: Q(2), 4: Q(3), 8: Q(7, 2)}[cells])
        check("cells=%d shear antisymmetry" % cells, slo + shi, Q(0))
        # discrete conservation: (F_top - F_bottom) = G * span
        fb = -MU * (full[1] - full[0]) / h
        ft = -MU * (full[-1] - full[-2]) / h
        span = Q(n) * h
        check("cells=%d conservation imbalance" % cells, (ft - fb) - G * span, Q(0))

    # --- refinement ratios --------------------------------------------------
    check("Q err cells=2", Q(8, 3) - Q(2), Q(2, 3))
    check("Q err cells=4", Q(8, 3) - Q(5, 2), Q(1, 6))
    check("Q err cells=8", Q(8, 3) - Q(21, 8), Q(1, 24))
    check("Q order 2->4", (Q(8, 3) - Q(2)) / (Q(8, 3) - Q(5, 2)), Q(4))
    check("Q order 4->8", (Q(8, 3) - Q(5, 2)) / (Q(8, 3) - Q(21, 8)), Q(4))
    check("shear order 2->4", (Q(4) - Q(2)) / (Q(4) - Q(3)), Q(2))
    check("shear order 4->8", (Q(4) - Q(3)) / (Q(4) - Q(7, 2)), Q(2))

    # --- transient: exact FTCS steps on the 5-node grid ----------------------
    h = H / 4
    r = Q(1, 4)
    dt = r * h * h / (MU / RHO)
    src = dt * G / RHO
    check("dt from r=1/4", dt, Q(1, 16))
    check("src per step", src, Q(1, 4))

    def step(u):
        v = list(u)
        for i in (1, 2, 3):
            v[i] = u[i] + r * (u[i - 1] - 2 * u[i] + u[i + 1]) + src
        return v

    u0 = [Q(0)] * 5
    u1 = step(u0)
    check("step1 lane1", u1[1], Q(1, 4))
    check("step1 lane2", u1[2], Q(1, 4))
    u2 = step(u1)
    check("step2 lane1", u2[1], Q(7, 16))
    check("step2 lane2", u2[2], Q(1, 2))
    check("step2 symmetry", u2[1] - u2[3], Q(0))
    # fixed point: exact discrete steady state reproduces itself
    xs = [Q(0), Q(3, 2), Q(2), Q(3, 2), Q(0)]
    check("steady-state fixed point", step(xs), xs)
    # zero drive preserves zero
    def step_nosrc(u):
        v = list(u)
        for i in (1, 2, 3):
            v[i] = u[i] + r * (u[i - 1] - 2 * u[i] + u[i + 1])
        return v
    check("zero drive preserves zero", step_nosrc(u0), u0)
    # 32-step approach: within 1% of steady (slowest factor ~0.8536^32)
    u = u0
    for _ in range(32):
        u = step(u)
    check("32-step center close to 2", abs(u[2] - 2) < Q(1, 50), True)
    check("32-step clock t", dt * 32, Q(2))

    # --- double-literal validity for test constants --------------------------
    dbl = 8.0 / 3.0
    check("8/3 == nearest-double literal",
          struct.pack("<d", dbl), struct.pack("<d", 2.6666666666666665))

    print("----")
    if FAILURES:
        print("ORACLE FAIL: %d mismatches: %s" % (len(FAILURES), FAILURES))
        raise SystemExit(1)
    print("ORACLE PASS")


if __name__ == "__main__":
    main()
