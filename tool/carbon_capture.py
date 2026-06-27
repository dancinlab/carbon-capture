"""carbon_capture — shared runnable harness for HYPOTHESES hypothesis cards.

Deterministic, dependency-free (stdlib `math` only) primitives for the CO2
capture-storage-conversion (HEXA-CCUS) problem. HYPOTHESES cards reference these
functions from their per-hypothesis run scripts under `state/<hX>/` (anima-parity:
shared machinery lives in repo-root `tool/`, per-hypothesis runs live in `state/`).

Every function is a closed-form public relation — no fitting, no hidden constants
beyond documented defaults. All inputs are explicit so a card's falsifiers can be
evaluated against the returned numbers.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# Universal gas constant (J/mol/K).
R_GAS = 8.314462618

# Molar mass of CO2 (g/mol) — used for gravimetric uptake <-> mass-fraction conversion.
M_CO2 = 44.009

# Molar mass of carbon (g/mol).
M_C = 12.011

# Standard enthalpy of formation of CO2 from graphite + O2 (J/mol, magnitude). The
# reverse (CO2 -> C(graphite) + O2) costs at least this much — the thermodynamic floor
# to reduce captured CO2 back to solid carbon (HEXA-TRANSMUTE L5).
DH_F_CO2 = 393.5e3

# Atmospheric mass of CO2 per ppmv (Gt CO2 / ppmv). 1 ppmv CO2 ~ 2.13 Gt C ~ 7.82 Gt CO2.
GT_CO2_PER_PPM = 7.82


# --- thermodynamic separation floor -------------------------------------------

def min_separation_work(x_co2: float, temp_k: float = 298.15) -> float:
    """Minimum reversible work to separate CO2 from a mixture, per mole CO2:

        W_min = R * T * ln(1 / x_CO2)        [J/mol]

    The Sherwood/thermodynamic floor. At ambient air x_CO2 ~ 4.2e-4 and T=298 K
    this is ~ 20 kJ/mol (the HEXA-CCUS `J2 - tau = 20` target floor); today's wet
    amine rigs sit ~ 10x above it.
    """
    if not (0.0 < x_co2 < 1.0):
        raise ValueError(f"x_co2 must be in (0,1): {x_co2}")
    if temp_k <= 0:
        raise ValueError(f"temp_k must be > 0: {temp_k}")
    return R_GAS * temp_k * math.log(1.0 / x_co2)


def energy_headroom(current_kj_mol: float, floor_kj_mol: float) -> float:
    """Reduction factor between a current capture energy and the thermodynamic
    floor: current / floor. ~10x for 200 kJ/mol amine vs the ~20 kJ/mol floor."""
    if floor_kj_mol <= 0:
        raise ValueError(f"floor must be > 0: {floor_kj_mol}")
    return current_kj_mol / floor_kj_mol


# --- sorbent / capacity --------------------------------------------------------

def capacity_ratio(target_mmol_g: float, baseline_mmol_g: float) -> float:
    """Working-capacity improvement of a sorbent vs a baseline (e.g. Climeworks
    ~2.0 mmol/g). Target 48 mmol/g = J2*phi gives a 24x ratio."""
    if baseline_mmol_g <= 0:
        raise ValueError(f"baseline must be > 0: {baseline_mmol_g}")
    return target_mmol_g / baseline_mmol_g


# --- cost / throughput ---------------------------------------------------------

def cost_ratio(baseline_usd_ton: float, target_usd_ton: float) -> float:
    """Capture-cost reduction factor, baseline / target. Climeworks ~$600/ton vs
    the $24/ton (= J2) target gives a 25x ratio."""
    if target_usd_ton <= 0:
        raise ValueError(f"target must be > 0: {target_usd_ton}")
    return baseline_usd_ton / target_usd_ton


def annual_capacity_ratio(plant_ton_yr: float, baseline_ton_yr: float) -> float:
    """Per-plant annual-capture scale-up vs a baseline (Climeworks ~4 kt/yr).
    HEXA-PLANT 1 Mt/yr gives a 250x ratio."""
    if baseline_ton_yr <= 0:
        raise ValueError(f"baseline must be > 0: {baseline_ton_yr}")
    return plant_ton_yr / baseline_ton_yr


# --- gravimetric bound ---------------------------------------------------------

def co2_mass_fraction(mmol_per_g: float) -> float:
    """Convert a gravimetric CO2 uptake (mmol CO2 per gram of sorbent) into the
    mass of CO2 captured per gram of sorbent:

        m_CO2/m_sorbent = uptake[mol/g] * M_CO2[g/mol]
                        = mmol_per_g * 1e-3 * 44.009

    A physical sanity bound for any sorbent target. The HEXA-CCUS `48 mmol/g`
    (= J2*phi) target maps to 48e-3 * 44.009 = 2.11 g CO2 per g sorbent (211 %
    of the sorbent's own mass) — far above any measured adsorbent, which top out
    near ~1 mmol/g at DAC partial pressure and well under ~1 g/g even at high
    pressure. Returned value is dimensionless (g per g)."""
    if mmol_per_g < 0:
        raise ValueError(f"mmol_per_g must be >= 0: {mmol_per_g}")
    return mmol_per_g * 1e-3 * M_CO2


# --- packing geometry ----------------------------------------------------------

def perimeter_area_ratio(n_sides: int) -> float:
    """Dimensionless wall-cost of a regular n-gon channel: perimeter divided by
    sqrt(area), the cross-sectional wall length per unit throughput area.

        P / sqrt(A) = 2 * sqrt(n * tan(pi / n))

    Lower = less wall material per unit flow area. Among the only three regular
    polygons that tile the plane (n=3,4,6), the hexagon (n=6) is the minimum —
    the closed-form statement behind the honeycomb conjecture (Hales 2001) and
    the HEXA-REACTOR geometry choice. The circle (limit n->inf) gives 2*sqrt(pi)
    = 3.545 but does not tile."""
    if n_sides < 3:
        raise ValueError(f"n_sides must be >= 3: {n_sides}")
    return 2.0 * math.sqrt(n_sides * math.tan(math.pi / n_sides))


# --- sensing resolution (L3 chip) ---------------------------------------------

def bits_for_resolution(full_scale: float, resolution: float) -> float:
    """ADC bit-depth required to resolve `resolution` over a `full_scale` span:

        bits = log2(full_scale / resolution)

    e.g. resolving 1 ppb of CO2 over a 420 ppm (= 420_000 ppb) ambient full-scale
    needs log2(420_000) ~ 18.7 bits — far above the HEXA-CHIP `sigma = 12`-bit ADC.
    Returned value is a real number of bits (not yet rounded up)."""
    if full_scale <= 0 or resolution <= 0:
        raise ValueError(f"full_scale and resolution must be > 0: {full_scale}, {resolution}")
    return math.log2(full_scale / resolution)


# --- CO2 -> carbon reduction floor (L5 transmute) -----------------------------

def carbon_reduction_energy_floor(dh_f_co2_j_mol: float = DH_F_CO2) -> float:
    """Thermodynamic minimum energy to reduce CO2 to one ton of solid carbon, per
    ton of carbon product:

        E_floor = dh_f_co2 / M_C * 1e6        [J / ton C]

    Uses the CO2 formation enthalpy (default DH_F_CO2 = 393.5 kJ/mol). This is the
    reverse-of-combustion floor for CO2 -> C + O2 (HEXA-TRANSMUTE), before any CVD
    overhead — a hard lower bound, ignoring catalysts/electrochem efficiency."""
    if dh_f_co2_j_mol <= 0:
        raise ValueError(f"dh_f_co2_j_mol must be > 0: {dh_f_co2_j_mol}")
    return dh_f_co2_j_mol / M_C * 1e6


# --- planetary mass balance (L6 universal) ------------------------------------

def ppm_to_gt_co2(delta_ppm: float, gt_per_ppm: float = GT_CO2_PER_PPM) -> float:
    """Atmospheric CO2 mass (Gt CO2) corresponding to a `delta_ppm` change in mixing
    ratio: delta_ppm * GT_CO2_PER_PPM. Drawing 420 -> 280 ppm (140 ppm) is ~1095 Gt
    CO2 of gross atmospheric removal (before ocean re-equilibration)."""
    if delta_ppm < 0:
        raise ValueError(f"delta_ppm must be >= 0: {delta_ppm}")
    return delta_ppm * gt_per_ppm


# --- process: regeneration sensible heat (L1) ---------------------------------

def regeneration_sensible_heat(
    cp_kj_per_kg_k: float, delta_t_k: float, working_capacity_mol_per_kg: float
) -> float:
    """Sensible-heat penalty of a temperature-swing (TSA) regeneration, per mole of
    CO2 cycled:

        q = cp * delta_T / working_capacity        [kJ/mol CO2]

    Heating the whole sorbent bed by delta_T to desorb costs cp*delta_T per kg, spread
    over the working capacity (mol CO2/kg) released that cycle. This is WHY real TSA
    sits far above the separation floor: at cp~1 kJ/kg/K, delta_T~100 K, working
    capacity~1 mol/kg this is ~100 kJ/mol — independent of, and on top of, W_min.
    Returns kJ/mol CO2 (heat-integration/recovery not modelled — a raw upper estimate)."""
    if working_capacity_mol_per_kg <= 0:
        raise ValueError(f"working_capacity must be > 0: {working_capacity_mol_per_kg}")
    if cp_kj_per_kg_k < 0 or delta_t_k < 0:
        raise ValueError("cp and delta_T must be >= 0")
    return cp_kj_per_kg_k * delta_t_k / working_capacity_mol_per_kg


# --- storage: isothermal compression work (L4) --------------------------------

def isothermal_compression_work(p_final: float, p_initial: float, temp_k: float = 298.15) -> float:
    """Ideal isothermal compression work per mole of gas:

        W = R * T * ln(p_final / p_initial)        [J/mol]

    For pipeline/injection CO2 from ~1 bar to 12 MPa (120 bar) at 298 K this is
    ~11.9 kJ/mol — the storage-compression add-on to the capture energy. Ideal-gas,
    isothermal, single-stage; real multi-stage compression with intercooling is higher."""
    if p_final <= 0 or p_initial <= 0:
        raise ValueError("pressures must be > 0")
    if temp_k <= 0:
        raise ValueError("temp_k must be > 0")
    return R_GAS * temp_k * math.log(p_final / p_initial)


# --- sorbent: Langmuir coverage / binding optimum (L0) ------------------------

def langmuir_coverage(
    e_ads_kj_per_mol: float,
    partial_pressure_bar: float,
    temp_k: float = 298.15,
    pre_exp_bar_inv: float = 1e-6,
) -> float:
    """Equilibrium fractional surface coverage from a Langmuir isotherm with an
    Arrhenius-style affinity:

        b = pre_exp * exp(E_ads / R T)     theta = b*p / (1 + b*p)

    `e_ads_kj_per_mol` is the (positive) adsorption energy. Too weak -> theta tiny at
    the 4.2e-4 bar DAC partial pressure (no uptake); too strong -> theta ~ 1 but the
    same E_ads must be paid back to regenerate. The pre-exponential is a documented
    representative entropic prefactor, not fitted. Returns theta in [0, 1)."""
    if partial_pressure_bar < 0 or temp_k <= 0 or pre_exp_bar_inv <= 0:
        raise ValueError("invalid Langmuir inputs")
    b = pre_exp_bar_inv * math.exp(e_ads_kj_per_mol * 1000.0 / (R_GAS * temp_k))
    bp = b * partial_pressure_bar
    return bp / (1.0 + bp)


# --- plant: air throughput per ton CO2 (L4) -----------------------------------

def air_volume_per_ton_co2(
    x_co2: float, air_density_kg_m3: float = 1.2, capture_efficiency: float = 1.0
) -> float:
    """Volume of air that must pass the contactor to capture one ton of CO2 at mole
    fraction `x_co2` and a given single-pass capture efficiency:

        n_CO2 = 1e6 g / M_CO2          n_air = n_CO2 / (x_co2 * efficiency)
        V_air = n_air * M_air[kg/mol] / rho_air

    At 420 ppm, eff=1 this is ~1.3e9 m^3 air per ton CO2 — the air-handling scale wall
    behind DAC fan power. M_air = 0.02896 kg/mol; rho default 1.2 kg/m^3."""
    if not (0.0 < x_co2 < 1.0):
        raise ValueError(f"x_co2 must be in (0,1): {x_co2}")
    if not (0.0 < capture_efficiency <= 1.0):
        raise ValueError(f"capture_efficiency must be in (0,1]: {capture_efficiency}")
    if air_density_kg_m3 <= 0:
        raise ValueError("air_density must be > 0")
    m_air_kg_per_mol = 0.02896
    n_co2 = 1e6 / M_CO2
    n_air = n_co2 / (x_co2 * capture_efficiency)
    return n_air * m_air_kg_per_mol / air_density_kg_m3


# --- lifecycle: net-negativity (system) ---------------------------------------

def net_capture_fraction(e_capture_j_per_ton: float, grid_intensity_kg_per_kwh: float) -> float:
    """Net CO2 actually removed per ton captured, after subtracting the CO2 emitted to
    power the capture:

        emitted_kg = (E_capture[J] / 3.6e6 J/kWh) * grid_intensity[kg/kWh]
        net_fraction = 1 - emitted_kg / 1000        [ton net / ton captured]

    < 0 means the capture EMITS more than it removes (futile on that energy source).
    At 9 GJ/ton (= 2500 kWh/ton) a fossil grid ~0.45 kg/kWh emits ~1125 kg > 1000 kg
    captured -> net negative. Clean energy (< ~0.4 kg/kWh) is required for net removal."""
    if e_capture_j_per_ton < 0 or grid_intensity_kg_per_kwh < 0:
        raise ValueError("inputs must be >= 0")
    emitted_kg = (e_capture_j_per_ton / 3.6e6) * grid_intensity_kg_per_kwh
    return 1.0 - emitted_kg / 1000.0


# --- humidity: water co-load vs CO2 (L0/L1) -----------------------------------

def humidity_to_co2_ratio(
    rh_fraction: float, temp_c: float, x_co2: float = 420e-6, p_atm_kpa: float = 101.325
) -> float:
    """Molar ratio of water vapour to CO2 in ambient air:

        es(T) = 0.6108 * exp(17.27*T / (T + 237.3))   [kPa, Tetens]
        x_H2O = rh * es / p_atm        ratio = x_H2O / x_co2

    At 50 % RH, 25 C this is ~37 — the contactor sees ~37× more H2O than CO2, the
    parasitic co-adsorption load behind much of DAC's real energy on physisorbents."""
    if not (0.0 <= rh_fraction <= 1.0):
        raise ValueError(f"rh_fraction must be in [0,1]: {rh_fraction}")
    if not (0.0 < x_co2 < 1.0) or p_atm_kpa <= 0:
        raise ValueError("invalid x_co2 / p_atm")
    es = 0.6108 * math.exp(17.27 * temp_c / (temp_c + 237.3))
    x_h2o = rh_fraction * es / p_atm_kpa
    return x_h2o / x_co2


# --- synthesis: total DAC energy decomposition (system optimizer) -------------

# kJ/mol CO2 per GJ/ton CO2: 1 GJ/ton = 1e9 J / (1e6 g / M_CO2 g/mol) = M_CO2*1e3 J/mol.
KJ_PER_MOL_PER_GJ_TON = M_CO2  # 1 GJ/ton ~= 44.009 kJ/mol


def total_dac_energy(
    working_capacity_mol_per_kg: float,
    delta_t_k: float = 100.0,
    cp_kj_per_kg_k: float = 1.0,
    heat_recovery: float = 0.0,
    include_compression: bool = True,
    x_co2: float = 420e-6,
    temp_k: float = 298.15,
) -> dict:
    """Synthesis model: total addressable DAC energy per mole CO2, decomposed into the
    three VERIFIED component terms (each its own hypothesis):

        E_sep   = min_separation_work(x, T)               (H_001, irreducible 2nd-law floor)
        E_regen = regeneration_sensible_heat(...) * (1 - heat_recovery)   (H_010, addressable)
        E_comp  = isothermal_compression_work(120 bar, 1 bar, T)   (H_011, storage only)
        E_total = E_sep + E_regen + E_comp

    All terms in kJ/mol CO2; also reports GJ/ton and kWh/ton. `heat_recovery` in [0,1)
    models heat integration; `include_compression=False` is the conversion/aqueous path
    (H_008 / moisture-swing) that skips storage compression. This composes the verified
    primitives into one objective so the optimal operating point can be searched — it is a
    LOWER-BOUND on the addressable terms (ignores heat-of-adsorption, water co-load H_016,
    fan power H_013, and kinetics), not a full plant model."""
    if not (0.0 <= heat_recovery < 1.0):
        raise ValueError(f"heat_recovery must be in [0,1): {heat_recovery}")
    e_sep = min_separation_work(x_co2, temp_k) / 1000.0
    e_regen = regeneration_sensible_heat(cp_kj_per_kg_k, delta_t_k,
                                         working_capacity_mol_per_kg) * (1.0 - heat_recovery)
    e_comp = (isothermal_compression_work(120.0, 1.0, temp_k) / 1000.0
              if include_compression else 0.0)
    e_total = e_sep + e_regen + e_comp
    return {
        "e_sep_kj_mol": e_sep,
        "e_regen_kj_mol": e_regen,
        "e_comp_kj_mol": e_comp,
        "e_total_kj_mol": e_total,
        "e_total_gj_ton": e_total / KJ_PER_MOL_PER_GJ_TON,
        "e_total_kwh_ton": e_total / KJ_PER_MOL_PER_GJ_TON * 1e9 / 3.6e6,
    }


# --- 🜂 ABSTRACT-track kernels (deterministic graduation of imagination cards) ---

M_AIR = 0.02896          # kg/mol, mean molar mass of air
MU0 = 4.0e-7 * math.pi   # vacuum permeability (T·m/A)
EV_KJ_MOL = 96.485       # 1 eV/molecule = 96.485 kJ/mol
F_FARADAY = 96485.0      # C/mol


def ev_to_kj_mol(ev: float) -> float:
    """Convert per-molecule eV to kJ/mol (× 96.485). Photon/bond energies (H_A003/A008)."""
    return ev * EV_KJ_MOL


def centrifuge_separation_factor(delta_m_kg_mol: float, rim_speed_m_s: float,
                                 temp_k: float = 298.15) -> float:
    """Gas-centrifuge per-stage separation factor by molecular mass (H_A001):
        alpha = exp(delta_M * v^2 / (2 R T)).
    CO2/N2: delta_M=16e-3, v=600 -> ~3.2. Mass-selective, sorbent-free."""
    if delta_m_kg_mol <= 0 or rim_speed_m_s <= 0 or temp_k <= 0:
        raise ValueError("inputs must be > 0")
    return math.exp(delta_m_kg_mol * rim_speed_m_s ** 2 / (2.0 * R_GAS * temp_k))


def centrifuge_kinetic_energy_per_mol_co2(rim_speed_m_s: float, x_co2: float = 420e-6,
                                          m_air_kg_mol: float = M_AIR) -> float:
    """Kinetic energy to spin the air that carries one mole of CO2, per mole CO2 (H_A001):
        E = (0.5 * M_air * v^2) / x_co2        [J/mol CO2]
    The throughput-energy wall: at v=600 m/s, 400 ppm this is ~1.2e7 J/mol = ~640x the floor."""
    if not (0.0 < x_co2 < 1.0) or rim_speed_m_s <= 0:
        raise ValueError("invalid inputs")
    return (0.5 * m_air_kg_mol * rim_speed_m_s ** 2) / x_co2


def clausius_clapeyron_temp(p_target_pa: float, dh_j_mol: float,
                            t_ref_k: float, p_ref_pa: float) -> float:
    """Phase-line temperature at p_target from a reference point (H_A002 frost, H_A009 hydrate):
        1/T = 1/T_ref - (R/dH) * ln(p_target/p_ref).
    CO2 frost at its 400-ppm partial pressure lands ~130 K (-143 C)."""
    if p_target_pa <= 0 or p_ref_pa <= 0 or dh_j_mol <= 0 or t_ref_k <= 0:
        raise ValueError("invalid inputs")
    inv_t = 1.0 / t_ref_k - (R_GAS / dh_j_mol) * math.log(p_target_pa / p_ref_pa)
    if inv_t <= 0:
        raise ValueError("non-physical temperature")
    return 1.0 / inv_t


def magnetic_thermal_ratio(chi_vol_si: float, b_tesla: float,
                           pressure_pa: float = 101325.0) -> float:
    """Ratio of magnetic energy density to thermal/pressure energy density for a gas (H_A004):
        (chi * B^2 / (2 mu0)) / P.
    Gas-phase O2 at 10 T gives ~1e-3 — magnetic sorting is overwhelmed by thermal motion."""
    if pressure_pa <= 0:
        raise ValueError("pressure must be > 0")
    return (chi_vol_si * b_tesla ** 2 / (2.0 * MU0)) / pressure_pa


def fan_work_per_ton(air_vol_m3_per_ton: float, delta_p_pa: float) -> float:
    """Ideal fan work to push the contactor air for one ton CO2 (H_A005):
        W = volume * delta_P        [J/ton CO2].
    At ~1.3e6 m3/ton and a low 100 Pa open-mesh drop this is ~0.13 GJ/ton — small if delta_P is low."""
    if air_vol_m3_per_ton < 0 or delta_p_pa < 0:
        raise ValueError("inputs must be >= 0")
    return air_vol_m3_per_ton * delta_p_pa


def electrochem_energy_per_mol(electrons_per_co2: float, cell_voltage_v: float) -> float:
    """Electrochemical energy per mole CO2 (H_A006 electro-swing):
        E = n * V * F        [J/mol]. 1-2 e-/CO2 at 0.5-1.0 V -> ~48-193 kJ/mol (amine-TSA band)."""
    if electrons_per_co2 < 0 or cell_voltage_v < 0:
        raise ValueError("inputs must be >= 0")
    return electrons_per_co2 * cell_voltage_v * F_FARADAY


def areal_capture_ceiling_gt_yr(rate_g_m2_day: float, area_m2: float) -> float:
    """Annual capture ceiling from an areal rate over a deployed area (H_A007/A010):
        Gt/yr = rate[g/m2/day] * area[m2] * 365 / 1e15."""
    if rate_g_m2_day < 0 or area_m2 < 0:
        raise ValueError("inputs must be >= 0")
    return rate_g_m2_day * area_m2 * 365.0 / 1e15


def solar_area_for_carbon(mass_c_ton_yr: float, solar_to_fuel_eff: float,
                          insolation_w_m2: float = 200.0,
                          reduction_j_per_ton_c: float = None) -> float:
    """Land area to photo-reduce a given carbon mass per year (H_A011 artificial leaf):
        area = (mass_C * E_reduction / eff) / (insolation * seconds_per_year)   [m^2].
    Energy is free sunlight, so AREA is the binding cost."""
    if reduction_j_per_ton_c is None:
        reduction_j_per_ton_c = carbon_reduction_energy_floor()
    if not (0.0 < solar_to_fuel_eff <= 1.0) or insolation_w_m2 <= 0 or mass_c_ton_yr < 0:
        raise ValueError("invalid inputs")
    energy_needed = mass_c_ton_yr * reduction_j_per_ton_c / solar_to_fuel_eff
    return energy_needed / (insolation_w_m2 * 3.1536e7)


# --- cross-family figure of merit (H_020) -------------------------------------

def nnr_fom(active_grid_kwh_per_ton: float, grid_intensity_kg_per_kwh: float = 0.45) -> dict:
    """Net-Negativity-Robust figure of merit: net CO2 removed per unit of ACTIVE grid
    energy, evaluated on a realistic (default fossil 0.45 kgCO2/kWh) grid — the metric
    that makes electric DAC, enhanced weathering, the artificial leaf, and moisture-swing
    directly comparable across mechanism-families (H_020).

        net   = 1 - (active_grid_kwh * grid_intensity) / 1000   [ton net / ton processed]
        NNR   = net / (active_grid_kwh * 3.6e-3)                [ton net / GJ active grid energy]

    Free-energy paths (sunlight, ambient humidity, rock chemistry) draw little GRID energy,
    so they keep a high net AND a small denominator -> they dominate electric DAC, whose net
    collapses toward 0 on a dirty grid (H_014). Returns net and NNR (ton/GJ)."""
    if active_grid_kwh_per_ton <= 0 or grid_intensity_kg_per_kwh < 0:
        raise ValueError("active energy must be > 0 and intensity >= 0")
    net = 1.0 - (active_grid_kwh_per_ton * grid_intensity_kg_per_kwh) / 1000.0
    nnr = net / (active_grid_kwh_per_ton * 3.6e-3)
    return {"net_fraction": net, "nnr_ton_per_gj": nnr, "active_kwh": active_grid_kwh_per_ton}


# --- path-selection: abatement-before-removal (H_023) -------------------------

def abatement_crossover_intensity(dac_kwh_per_ton: float) -> float:
    """Marginal grid carbon intensity (kgCO2/kWh) at which spending a clean kWh on
    electric DAC ties spending it to displace fossil generation (H_023):

        DAC nets 1000 kg / dac_kwh per kWh of clean power; displacement avoids the
        marginal grid intensity g per kWh. They tie at g* = 1000 / dac_kwh.

    Above g* (dirtier marginal plant), a clean kWh AVOIDS more CO2 by displacing
    fossil than it REMOVES via DAC -> abatement before removal. For Gen3 DAC
    (1500 kWh/ton) g* = 0.667 kgCO2/kWh (≈ a gas plant); coal (~0.9) is above it."""
    if dac_kwh_per_ton <= 0:
        raise ValueError("dac_kwh_per_ton must be > 0")
    return 1000.0 / dac_kwh_per_ton


def dominates(a: dict, b: dict) -> bool:
    """True if scorecard `a` is >= `b` on every axis and strictly > on at least one
    (Pareto domination). Used by H_021 to test for a single best path."""
    keys = set(a) & set(b)
    if not keys:
        raise ValueError("no shared axes")
    return all(a[k] >= b[k] for k in keys) and any(a[k] > b[k] for k in keys)


# --- falsifier harness --------------------------------------------------------

@dataclass
class Falsifier:
    """One pre-registered, measurable falsifier. `predicate(metrics) -> bool`
    returns True when the falsifier is TRIGGERED (hypothesis component refuted)."""

    name: str
    predicate: object  # callable(dict) -> bool
    desc: str = ""


def evaluate(metrics: dict, falsifiers: list) -> dict:
    """Run each falsifier against the measured metrics. A falsifier PASSes when
    it is NOT triggered. Returns a verdict ledger (all-stdlib, JSON-safe)."""
    results = []
    for f in falsifiers:
        triggered = bool(f.predicate(metrics))
        results.append(
            {"name": f.name, "triggered": triggered, "status": "FAIL" if triggered else "PASS"}
        )
    n_pass = sum(1 for r in results if r["status"] == "PASS")
    return {
        "metrics": metrics,
        "falsifiers": results,
        "n_pass": n_pass,
        "n_total": len(results),
        "all_pass": n_pass == len(results),
    }
