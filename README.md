# White dwarf planet project

## Research question

How does a distant brown-dwarf companion influence the survival of an Earth-mass planet as its host star evolves into a white dwarf?

Inspired by the observed system KMT-2020-BLG-0414L.

## What we have so far

These are results from the notebooks so far. For specifics, check the markdown in each notebook. The idea is to build things up one piece at a time and check each piece before combining them. If a name like “source knots” gets in the way, there's a [short glossary below](#what-do-these-words-even-mean).

**[00 — Environment](notebooks/00_environment_check.ipynb).** Check that AMUSE, the environment and the required workers actually work before running anything. Workers are the separate programs AMUSE launches to do the calculations.

**[01 — Stellar evolution](notebooks/01_stellar_evolution.ipynb).** Evolve a 1.2-M☉, Z = 0.02 star with SeBa, our stellar evolution code. M☉ means solar masses; Z = 0.02 means 2% of the initial mass is in elements heavier than helium. The coarse first run (I'll keep calling this **the pilot**) gave a white dwarf (WD) mass of 0.53244 M☉. Refining the requested steps changed it to **0.54021 M☉**. Basically, we ask SeBa to evolve to more closely spaced times and check whether the results converge somewhere. (It's a whole thing in SeBa why we say *requested* steps, and I don't like it! — Kostas.)

At refinement 64, the largest sampled radii in the RGB and AGB stages are **0.7947 and 1.1832 au**. These are two giant phases: the red giant branch and the later asymptotic giant branch. The saved mass and radius over time become our **stellar driver** in 04: the changing star that the orbital calculation follows. We leave the pilot available for the simpler example in 02.

**[02 — Isolated planet](notebooks/02_isolated_planet.ipynb).** Start with just the star and planet. The star loses mass slowly compared with an orbit, equally in all directions (*isotropic*). The orbit expands while keeping the same eccentricity e. Its semimajor axis a measures the orbit's size, and follows `a(Mstar + mplanet) = constant`.

For an initially circular orbit, the pilot's **geometric crossing boundary** is **a₀ ≈ 0.8182 au**. Start inside this boundary and the planet reaches the star's surface at some point, start outside it and the planet stays safe in this model. This accounts for the orbit expanding too. The equivalent refined boundary from 01 is **0.8219 au**. We have no tides or brown dwarf here.

**[03 — Brown-dwarf dynamics](notebooks/03_brown_dwarf_dynamics.ipynb).** Add the brown dwarf but keep all masses fixed. Its gravity can change the planet's eccentricity and therefore its **pericentre**, the closest distance to the star: `q = a(1 − e)`. We use SecularMultiple, which follows, as I understand it, only the slow changes in the orbits rather than every trip around the star.

At 60° (big for a clear effect but not too extreme) mutual inclination (the angle between the two orbital planes), the quadrupole run reaches **eₘₐₓ = 0.763744**, close to the analytical **0.763763**. Quadrupole is the leading approximation we use for the companion's effect; higher expansion orders can add finer corrections. Our conservation and numerical checks pass, but a closer-companion example is more sensitive to those extra terms. We also compare with Huayno, which integrates the motion directly that comparison still needs some more testing. I use the quadrupole setup for notebook 04, the extra terms are important to check if we have the time.

**[04 — Coupled mass loss](notebooks/04_mass_loss_coupling.ipynb).** Now let the changing star effect the orbits. First replay its saved track with the companion's perturbations off. A 1-au orbit expands to **2.22134 au**. The maximum fractional error in the constant `a(Mstar + mplanet)` from 02 is about **2.4 × 10⁻¹⁰**, so that transfer works very accurately.

Then add the brown dwarf **during the star's AGB window** (This is both to use a smaller stellar lifetime and to use the, I think, most consequential part of its lifetime). The inner and outer orbits start at **5 and 100 au** at the start of this window. With the stellar track held fixed, the numerical checks pass. The minimum sampled clearance, `q − (Rstar + Rplanet)`, is about **0.907 au**: positive means no geometric contact at that sample. However, using stellar refinements 64 and 128 changes the pericentre by up to **0.01025 au**, above our 0.001-au target. So I note it down as `needs_review` and investigate the stellar input while adding tides next.

**[05 — Tides](notebooks/05_tides.ipynb).** Add tidal friction and bulges to the AGB test from 04. In SecularMultiple we can switch friction on separately in the star and planet. On both fine stellar tracks, the planet stayed clear of the giant, with a minimum sampled clearance of about **0.91 au**. The two tracks start contracting towards the white dwarf at slightly different ages, so the spin through that transition still needs checking.

**[06 — Full history](notebooks/06_full_history.ipynb).** What if the planet was there before the star became a giant? We start it at **1 au** at stellar age zero and compare the same system with and without a brown dwarf at **20 au**. In both cases the planet reaches the star before the AGB. In the finer runs, contact happens **6.51 Myr earlier with the brown dwarf**. The triple’s contact age still shifts by **21–56 kyr** when we change the numerical settings. We still need to try other starting orbits to see where the companion actually changes whether the planet survives.

For the longer runs in notebooks 05 and 06, extract `notebook0506_data.zip` (or whatever I will call it, I will try putting it under `releases`)  at the project root. It puts the inputs under `data/`, alongside `notebooks/`. To compare how the longer runs perform on different PCs, you turn on only `RUN_PC_BENCHMARK` in the notebook you want and choose **Run All**. The 05 case took **2 h 17 min** on my laptop with another case running. For 06, allow **4–5 h**. Run one case at a time and check the `benchmark.json` it produces so we can compare specs, runtime and results. (The benchmark code was mostly chatgpt-ed so Its not 100% verified by me)


## What do these words even mean

This is a section of explanations on AMUSE and numerical terminology I found confusing. This compilation of terms was made using AI with editing by me. Let me know if anything is not clear of it made a mistake. - Kostas

### The input star

| Name  | Explanation |
| --- | --- |
| **Source / source track** | The input history supplied to the orbital calculation: a saved SeBa track, or a prescribed history for a simple test. |
| **Stellar track / stellar driver** | The star's properties over time, especially mass and radius. “Driver” means these values drive the orbital evolution. |
| **State / sample** | Values at one time: stellar mass and radius, for example, or orbital size, eccentricity and spin. |
| **Source knots / source nodes / stellar knots** | The input table's sample times and their values. For SeBa, these are saved stellar samples. “Keep every knot” means retain every original input point. |
| **Piecewise-linear history** | Basically interpolation, join neighbouring samples with straight lines to estimate values between them. Mass and radius change at constant rates within each source interval. |
| **Replay / one-way coupling / fixed driver** | Evolve the orbits using a saved stellar history. We can change orbital settings while holding that input fixed; the orbits do not feed changes back into SeBa. |

### Numerical terms

| Name  | Explanation |
| --- | --- |
| **Requested steps / stellar sampling** | The gaps between times we ask SeBa to evolve to and save. These differ from its internal steps. |
| **Stellar refinement** | Rerun stellar evolution with smaller requests. Refinement 64 divides the base requested steps by 64; it does not mean 64 samples. |
| **Mixed schedule** | Change refinement partway through a continuous stellar run: `mixed_pre128_agb2048` uses 128 before the AGB, then 2048 during it. |
| **Coupling intervals / substeps / subdivisions** | Intervals over which we advance the orbits with the supplied stellar changes. We can subdivide them without changing the stellar source. |
| **Solver tolerances / tight run** | Numerical accuracy settings. “Tight” asks the solver to control its error more strictly, independently of stellar sampling. |
| **Outputs / output cadence** | When and how often we record results. Output times can also trigger integration calls, so changing them can affect numerical error. |
| **Common grid / union grid / midpoints** | A grid is a list of times. Common grids compare runs at matching ages; a union includes all selected grids' times. Midpoints lie halfway between neighbours. |
| **Stellar age / window time / local clock** | Age counts from the stellar run's start; window time from the AGB segment's start. The solver's local clock advances each short interval from zero, keeping total time separately for numerical precision. |

## On the speeding up of code.
This is what I have found on how we can parallelize/accelerate different amuse solvers in the docs and from tests

| Code | Where we use it | Parallel or GPU  | What to investigate |
|---|---|---|---|
| **SecularMultiple** | 03–06 · Orbits and tides | CPU. Independent systems can run in parallel, one worker per process. | **First priority for running many cases.** Two short cases finished **1.59× faster** together. Test whether that holds for the multi-hour runs. | Maybe we can split up the data into many smaller cases to run in parallel?
| **Huayno** | 03 · Direct gravity check | Optional **OpenCL GPU** and **OpenMP CPU** workers.| **Best GPU candidate.** Our three-body case is below the GPU offload threshold. Test CPU versus GPU with a larger particle system. If this can be massively accelerated we could just move to Huanyo in general if it becomes faster than secularmultiple, though I doubt it. |
| **SeBa** | 01 · Stellar evolution | CPU. Independent stellar tracks can run in parallel. | **Lower priority.** Run different stellar masses or refinements side by side, though this doesnt take too long anyways |

[1]: https://amuse.readthedocs.io/en/latest/reference/available-codes.html?utm_source=chatgpt.com "Currently supported Community Codes"

# Todos
TODO: check computation time, if possible check the parameterspace for planet survival w and wo brown dwarf?
TODO(Siquan): report writing

