# Run: uv run python demos/intent_demo.py
import pandas as pd
import numpy as np

from intent_engine.manager import IntentManager

# --- synth dataset ---
rng = np.random.default_rng(42)
n = 1200
plans = np.array(["basic", "pro", "enterprise"])
plan = rng.choice(plans, size=n, p=[0.5, 0.35, 0.15])
base = {"basic": 35.0, "pro": 55.0, "enterprise": 95.0}
revenue = np.array([rng.normal(base[p] , 10.0) for p in plan]).clip(1, None)
churn_rate = rng.beta(a=2, b=12, size=n) + (plan == "enterprise") * 0.06

date = pd.date_range("2025-01-01", periods=n, freq="D")
df = pd.DataFrame({"plan": plan, "revenue": revenue, "churn_rate": churn_rate, "date": date})

# --- manager + intents ---
mgr = IntentManager(df)

print("\n--- Intent 1: DESCRIBE ---")
intent1 = mgr.parse("Describe revenue distribution")
for c in mgr.suggest(intent1):
    print(f"* {c.spec['type']}  :: score={c.scoring['score']:.2f} :: {c.rationale}")

print("\n--- Intent 2: COMPARE ---")
intent2 = mgr.parse("Compare revenue by plan in Q2")
for c in mgr.suggest(intent2):
    ig = c.scoring.get("IG_proxy", 0.0)
    print(f"* {c.spec['type']}  :: score={c.scoring['score']:.2f} (IG≈{ig:.2f}) :: {c.rationale}")

