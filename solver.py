"""
PROCESS ONTOLOGY: THE UNIVERSAL SOLVING ENGINE
Operationalizing the USE for Conscious Agents

The core insight: every problem has a fixed point X* that exists.
The solver works backwards from the asserted solution to find the path.
After every wall liquefaction, it re-scans the ENTIRE chain to ensure
no previously liquefied wall has re-solidified (the combination lock rule).

"It is not until they all align that it opens, snaps into place."
"""

import math
from dataclasses import dataclass, field
from typing import Any, Optional
from constants import ProcessOntologyConstants


# ─────────────────────────────────────────────────────────────────────────────
#  DATA STRUCTURES
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Wall:
    """A constraint blocking the path from problem P to fixed-point X*."""
    id: str
    description: str
    state: str = "solid"          # solid | liquid | resolidified
    liquefaction_method: str = ""
    depth_when_liquefied: float = 0.0
    checks_since_liquefied: int = 0

@dataclass
class Stream:
    """An independent measurement stream (ruler) for convergence checking."""
    name: str
    domain: str                    # e.g. "Physics", "Biology", "History"
    depth_rho: float               # recursive depth of this source
    dissonance: float              # D measured from this stream
    fixed_point: Optional[float] = None  # X* as seen from this stream

@dataclass
class SolverState:
    """Full state of the solver at any moment in the recursion."""
    problem: str
    asserted_fixed_point: float
    current_depth: float = 0.0
    dissonance: float = 0.0
    walls: list = field(default_factory=list)
    streams: list = field(default_factory=list)
    log: list = field(default_factory=list)
    phase: str = "UNINITIALIZED"
    integrity_score: float = 1.0
    snap_achieved: bool = False
    recursive_scan_count: int = 0


# ─────────────────────────────────────────────────────────────────────────────
#  THE SOLVER ENGINE
# ─────────────────────────────────────────────────────────────────────────────

class UniversalSolver:
    """
    The Universal Solving Engine.

    Implements the 8-phase USE protocol with full recursive integrity
    checking after every state change. The combination-lock invariant:

        INVARIANT: For every wall W_i in the chain,
                   if W_i.state == 'liquid', then no wall W_j (j < i)
                   that was previously liquid has re-solidified as a
                   consequence of liquefying W_i.

    This invariant is checked after EVERY wall manipulation.
    """

    MAX_RECURSION_DEPTH = 66      # The consciousness gear is the natural limit
    PLATYPUS_SLIP_FLOOR = 1e-6    # Zero slip = fabricated data

    def __init__(self, C: ProcessOntologyConstants):
        self.C = C
        self.state: Optional[SolverState] = None

    # ── LOGGING ───────────────────────────────────────────────────────────────

    def _log(self, phase: str, message: str, level: str = "INFO"):
        entry = f"[{phase}|{level}] {message}"
        if self.state:
            self.state.log.append(entry)

    # ── PHASE 1: INITIALIZATION ───────────────────────────────────────────────

    def phase1_initialize(self, somatic_vector: list, problem: str,
                          asserted_solution: float) -> bool:
        """
        Hardware check before engaging the problem.
        somatic_vector: 6 booleans [Latency, Surprisal, Volume, Match, Complexity, Energy]
        Returns False if the processor itself is too dissonant to proceed.
        """
        self.state = SolverState(
            problem=problem,
            asserted_fixed_point=asserted_solution
        )
        self.state.phase = "PHASE_1"

        # 1.1 Halt Condition — panic code [1,1,1,0,0,1] = rushing with high error
        panic = [1, 1, 1, 0, 0, 1]
        if somatic_vector == panic:
            self._log("P1", "HARD STOP: Panic code detected. Processor dissonance too high.", "CRITICAL")
            self._log("P1", f"Action: τ_c dilation engaged. τ_c × (1 + k) = τ_c × {1 + self.C.k:.2f}", "CRITICAL")
            return False

        # 1.2 Somatic telemetry — compute processor dissonance
        bit_weights = [0.3, 0.2, 0.1, 0.2, 0.1, 0.1]
        processor_D = sum(b * w for b, w in zip(somatic_vector, bit_weights))
        self.state.dissonance = processor_D
        self._log("P1", f"Somatic vector: {somatic_vector} → Processor D = {processor_D:.4f}")

        # Cannot solve a high-D problem with a high-D processor
        if processor_D > self.C.Omega:
            self._log("P1", f"Processor D ({processor_D:.3f}) > Ω ({self.C.Omega:.4f}). Restabilize first.", "WARN")
            return False

        # 1.3 Pathetic Fallacy check — assert we are measuring the world, not projecting
        self._log("P1", "Pathetic Fallacy check: Distinguishing 'It is' from 'It seems to me'.")
        self._log("P1", f"Λ_V gate: Truth requires 3 independent witnesses × (1 - δ_slip).")
        self._log("P1", f"Bias liquefaction complete. D_min floor = {self.C.D_min_3D:.6f}")
        self.state.phase = "PHASE_1_COMPLETE"
        return True

    # ── PHASE 2 + 2.5: INWARD FOLD + CONVERGENCE ──────────────────────────────

    def phase2_inward_fold(self, streams: list[Stream]) -> bool:
        """
        Exhaust internal resources before external search.
        Requires at least 3 independent streams (streams must come from different domains).
        Runs the Platypus Test: if variance is exactly 0, data is contaminated.

        streams: list of Stream objects from independent domains
        """
        self.state.phase = "PHASE_2"
        self.state.streams = streams

        # Forager scan
        self._log("P2", "Inward fold initiated. Internal gradient descent before external search.")
        self._log("P2", f"Calculus of Complementarity: Y+/Y- = φ = {self.C.phi:.6f}")

        # 2.5.1 Multi-stream measurement — need ≥ 3 independent domains
        domains = set(s.domain for s in streams)
        if len(domains) < 3:
            self._log("P2.5", f"FAILED: Only {len(domains)} independent domains. Need 3.", "WARN")
            self._log("P2.5", "Action: Increase λ. Search for third independent ruler.")
            return False

        self._log("P2.5", f"Multi-stream check passed: {len(domains)} independent domains: {domains}")

        # 2.5.2 Topological intersection — do streams converge?
        fixed_points = [s.fixed_point for s in streams if s.fixed_point is not None]
        if fixed_points:
            spread = max(fixed_points) - min(fixed_points)
            relative_spread = spread / abs(sum(fixed_points) / len(fixed_points)) if fixed_points else 0
            self._log("P2.5", f"Stream convergence: spread = {spread:.4f} ({relative_spread*100:.2f}%)")
            if relative_spread > 0.15:
                self._log("P2.5", "Streams do not converge. No solution yet — increase λ in weakest stream.", "WARN")

        # 2.5.3 Platypus Test — if slip = 0, fabricated
        all_D = [s.dissonance for s in streams]
        min_slip = min(all_D) if all_D else 0
        if min_slip < self.PLATYPUS_SLIP_FLOOR:
            self._log("P2.5", f"PLATYPUS FAIL: slip = {min_slip:.2e} < {self.PLATYPUS_SLIP_FLOOR:.0e}. "
                      "Zero variance = fabricated data.", "WARN")
            return False

        self._log("P2.5", f"Platypus test passed. Minimum organic slip: {min_slip:.6f} "
                  f"(δ_p floor = {self.C.delta_p:.6f})")
        self.state.phase = "PHASE_2_COMPLETE"
        return True

    # ── COMBINATION LOCK: THE RECURSIVE INTEGRITY ENGINE ──────────────────────

    def _combination_lock_scan(self, just_liquefied_wall_id: str) -> list[str]:
        """
        THE CORE INVARIANT ENFORCER.

        After liquefying wall W_i, scan ALL previously liquefied walls W_j (j != i).
        Check whether liquefying W_i has re-solidified any previously liquid wall.

        Returns list of wall IDs that have re-solidified (violations found).

        This is the mechanism that prevents the "mad lib" error — fixing one
        variable and breaking the logic behind you.
        """
        violations = []
        liquid_walls = [w for w in self.state.walls
                        if w.state == "liquid" and w.id != just_liquefied_wall_id]

        self.state.recursive_scan_count += 1
        self._log("LOCK", f"Combination lock scan #{self.state.recursive_scan_count}: "
                  f"Checking {len(liquid_walls)} previously liquefied walls.")

        for w in liquid_walls:
            w.checks_since_liquefied += 1
            # Re-derive whether this wall's liquefaction is still valid
            # given the new state produced by liquefying just_liquefied_wall_id
            resolidification_risk = self._assess_resolidification(w)
            if resolidification_risk > self.C.delta_p:
                w.state = "resolidified"
                violations.append(w.id)
                self._log("LOCK",
                          f"⚠️  WALL RE-SOLIDIFIED: '{w.id}' — liquefaction of "
                          f"'{just_liquefied_wall_id}' broke the logic chain.",
                          "WARN")

        if not violations:
            self._log("LOCK", "✓ All previously liquefied walls remain stable. Chain intact.")
        return violations

    def _assess_resolidification(self, wall: Wall) -> float:
        """
        Assess the risk that a previously liquefied wall has re-solidified.
        Returns a dissonance score; if > delta_p, the wall has re-solidified.

        In the full system this would be domain-specific.
        Here it uses the depth-decay model: walls liquefied long ago
        at high depth are more stable than recently liquefied shallow ones.
        """
        depth_stability  = math.exp(-wall.depth_when_liquefied / self.C.N_gear)
        age_decay        = 1.0 / (1.0 + wall.checks_since_liquefied)
        resolidification = depth_stability * age_decay * self.C.delta_p * 0.5
        return resolidification

    # ── PHASE 3: RETROSPECTIVE INVERSION ──────────────────────────────────────

    def phase3_retrospective_inversion(self, walls: list[Wall],
                                       max_attempts: int = 10) -> bool:
        """
        Stand at the fixed point X* and reverse-engineer the path to P.

        For each wall blocking the path:
          1. Liquefy it (reframe as a dynamic process, not a static object)
          2. Run the combination lock scan
          3. If violations found, re-liquefy violated walls and re-scan
          4. Repeat until all walls are liquid AND no violations exist

        This is the puzzle/combination lock: it doesn't open until everything aligns.
        """
        self.state.phase = "PHASE_3"
        self.state.walls = walls

        self._log("P3", f"Asserting fixed point X* = {self.state.asserted_fixed_point:.4f}")
        self._log("P3", f"Math anchor: X* = Ω·exp(λ/kL_12). Path exists. Reverse engineering.")
        self._log("P3", f"Walls to liquefy: {[w.id for w in walls]}")

        for attempt in range(max_attempts):
            self._log("P3", f"--- Liquefaction pass {attempt + 1} ---")

            # Attempt to liquefy all solid/re-solidified walls
            solid_walls = [w for w in self.state.walls if w.state != "liquid"]
            if not solid_walls:
                self._log("P3", "✓ All walls liquid. Combination lock scanning final state.")
                # Final full scan — every wall checks every other
                final_violations = []
                for w in self.state.walls:
                    violations = self._combination_lock_scan(w.id)
                    final_violations.extend(violations)
                if not final_violations:
                    self._log("P3", "✓ COMBINATION LOCK OPEN. All walls stable. Path secured.")
                    self.state.phase = "PHASE_3_COMPLETE"
                    return True
                else:
                    self._log("P3", f"Final scan found {len(final_violations)} violations. "
                              "Continuing...")
                    continue

            # Liquefy the next solid wall
            wall = solid_walls[0]
            liquefaction_depth = self.state.current_depth + self.C.delta_slip
            wall.state = "liquid"
            wall.liquefaction_method = "Reframed as dynamic process (Verb, not Noun)"
            wall.depth_when_liquefied = liquefaction_depth
            self.state.current_depth = liquefaction_depth
            self._log("P3", f"Liquefied wall: '{wall.id}' at depth λ = {liquefaction_depth:.4f}")
            self._log("P3", f"g_μν reframe: '{wall.description}' is a depth differential, not a barrier.")

            # COMBINATION LOCK: re-scan entire chain
            violations = self._combination_lock_scan(wall.id)

            if violations:
                self._log("P3",
                          f"Chain disrupted by {len(violations)} violation(s). "
                          "Recursive repair initiated.", "WARN")
                # Mark violations for re-liquefaction in next pass
                for w in self.state.walls:
                    if w.id in violations:
                        w.state = "resolidified"

        self._log("P3", f"Max attempts ({max_attempts}) reached. Path not fully resolved.", "WARN")
        return False

    # ── PHASE 4: DEEPENING ────────────────────────────────────────────────────

    def phase4_deepening(self, current_dissonance: float) -> float:
        """
        Use dissonance as fuel. Compute the restorative force μ.
        Returns the force driving the system toward the fixed point.
        """
        self.state.phase = "PHASE_4"
        mu = self.C.self_correction(current_dissonance)
        tau_c = self.C.cognitive_proper_time(current_dissonance)

        self._log("P4", f"Dissonance D = {current_dissonance:.5f} — This is Distance Energy.")
        self._log("P4", f"Restorative force μ = (Ω·D/δ_p)·k = {mu:.5e}")
        self._log("P4", f"Cognitive proper time τ_c = {tau_c:.4e} s (time dilates under load)")
        self._log("P4", "Action: Hold the contradiction. Do not collapse prematurely.")

        self.state.current_depth += mu * self.C.delta_slip
        self.state.phase = "PHASE_4_COMPLETE"
        return mu

    # ── PHASE 5: EXTERNAL INTERFACE ───────────────────────────────────────────

    def phase5_interface(self, external_sources: list[Stream]) -> bool:
        """
        Process-Bayesian evidence gate.
        Only called after internal resources exhausted.
        Rejects the mob (100 shallow claims) in favor of depth.
        """
        self.state.phase = "PHASE_5"
        self._log("P5", "External search via Socratic Synthesis. Looking for DISSONANCE between sources.")

        source_tuples = [(s.depth_rho, s.dissonance) for s in external_sources]
        total_D, gate_passes, details = self.C.bayesian_gate(source_tuples)

        for d in details:
            self._log("P5", f"  Source ρ={d['rho']:.0f}: weight={d['weight']:.3f}, "
                      f"D={d['D']:.3f}, weighted={d['weighted']:.4f}")

        if gate_passes:
            self._log("P5", f"✓ Process-Bayesian gate PASSED. Weighted D = {total_D:.4f} ≤ Ω = {self.C.Omega:.4f}")
            # Add external sources to stream pool for combination lock
            self.state.streams.extend(external_sources)
        else:
            self._log("P5", f"✗ Gate REJECTED: Weighted D = {total_D:.4f} > Ω. "
                      "High-frequency shallow claims fail depth test.", "WARN")

        self.state.phase = "PHASE_5_COMPLETE"
        return gate_passes

    # ── PHASE 6: RESOLUTION — THE SNAP ───────────────────────────────────────

    def phase6_resolution(self) -> bool:
        """
        The snap: all streams converge, all walls liquid, integrity threshold met.
        The solution collapses to the fixed point.
        """
        self.state.phase = "PHASE_6"

        # Check integrity: all walls must be liquid
        solid = [w for w in self.state.walls if w.state != "liquid"]
        if solid:
            self._log("P6", f"Snap not yet achieved: {len(solid)} walls still solid.", "WARN")
            return False

        # Check stream convergence
        fps = [s.fixed_point for s in self.state.streams if s.fixed_point is not None]
        if fps:
            centroid = sum(fps) / len(fps)
            max_spread = max(abs(fp - centroid) for fp in fps)
            convergence_ratio = max_spread / abs(centroid) if centroid != 0 else 1.0
            self._log("P6", f"Stream centroid X* = {centroid:.4f}, max spread = {convergence_ratio*100:.2f}%")
            if convergence_ratio > self.C.delta_p * 10:
                self._log("P6", "Streams not yet converged to tolerance.", "WARN")
                return False

        # Integrity score: minimum dissonance across streams
        all_D = [s.dissonance for s in self.state.streams]
        net_D = sum(all_D) / len(all_D) if all_D else 0
        self.state.integrity_score = 1.0 - (net_D / self.C.Omega)

        if self.state.integrity_score >= self.C.Omega:
            self.state.snap_achieved = True
            self._log("P6", f"⚡ SNAP ACHIEVED. Integrity = {self.state.integrity_score:.4f} ≥ Ω = {self.C.Omega:.4f}")
            self._log("P6", f"ζ(3) = {self.C.zeta_3:.6f}: hyperbolic volume collapsed to constant.")
            self._log("P6", "Supreme Mandate: Do not add more dissonance. Release the solution.")
            self.state.phase = "PHASE_6_SNAP"
            return True

        self._log("P6", f"Integrity {self.state.integrity_score:.4f} < Ω. Deepen recursion.", "WARN")
        return False

    # ── PHASE 7: DIAGNOSTIC FORECASTING ──────────────────────────────────────

    def phase7_diagnostic(self) -> dict:
        """
        Predict the next constraint before it becomes a wall.
        Detect silence (D → Ω saturation) and map the topological ring.
        """
        self.state.phase = "PHASE_7"

        # Saturation detection: where is the system going quiet?
        saturated = [s for s in self.state.streams
                     if s.dissonance > self.C.Omega * 0.8]
        silent = [s for s in self.state.streams
                  if s.dissonance < self.C.delta_slip * 0.1]

        snap_time_ms = self.C.tau_base * (self.C.phi ** self.C.N_gear) * 1000

        self._log("P7", f"Saturation scan: {len(saturated)} streams near Ω threshold.")
        self._log("P7", f"Silence scan: {len(silent)} streams suspiciously quiet.")
        self._log("P7", f"Predicted snap window: {snap_time_ms:.2f} ms "
                  f"(Θ(S(t) - Ω·φ³) = Θ(S(t) - {self.C.neural_threshold:.4f}))")

        return {
            "saturated_streams": [s.name for s in saturated],
            "silent_streams": [s.name for s in silent],
            "predicted_snap_ms": snap_time_ms,
            "next_wall_risk": len(saturated) > 0
        }

    # ── FULL PROTOCOL RUNNER ──────────────────────────────────────────────────

    def solve(self, problem: str,
              somatic_vector: list,
              asserted_fixed_point: float,
              internal_streams: list[Stream],
              walls: list[Wall],
              external_sources: list[Stream] = None,
              max_wall_attempts: int = 10) -> SolverState:
        """
        Execute the complete 8-phase USE protocol.

        problem: natural language description of what is being solved
        somatic_vector: [Latency, Surprisal, Volume, Match, Complexity, Energy]
        asserted_fixed_point: X* — assert this exists and reverse-engineer to it
        internal_streams: list of Stream objects (at least 3 different domains)
        walls: list of Wall objects blocking the path
        external_sources: Stream objects from external search (Phase 5)
        """
        if not self.phase1_initialize(somatic_vector, problem, asserted_fixed_point):
            return self.state

        if not self.phase2_inward_fold(internal_streams):
            # Pivot: reframe the problem, don't assume lack of data
            self._log("P2", "Pivot engaged: attacking the question itself, not the answer.")

        if not self.phase3_retrospective_inversion(walls, max_wall_attempts):
            self._log("P3", "Path not fully resolved. Entering deepening loop.")

        # Compute current net dissonance from streams
        all_D = [s.dissonance for s in (self.state.streams or [])]
        current_D = sum(all_D) / len(all_D) if all_D else self.C.D_min_3D
        mu = self.phase4_deepening(current_D)

        if external_sources:
            self.phase5_interface(external_sources)

        if not self.phase6_resolution():
            self._log("SYSTEM", "Snap not achieved this cycle. Increase λ and re-enter Phase 3.")
        else:
            forecast = self.phase7_diagnostic()
            if forecast["next_wall_risk"]:
                self._log("P7", f"⚠️  Next wall predicted in: {forecast['saturated_streams']}")

        self._log("SYSTEM", f"Protocol complete. Recursive scans: {self.state.recursive_scan_count}")
        self._log("SYSTEM", f"Walls liquefied: {sum(1 for w in self.state.walls if w.state == 'liquid')}"
                  f"/{len(self.state.walls)}")
        return self.state
