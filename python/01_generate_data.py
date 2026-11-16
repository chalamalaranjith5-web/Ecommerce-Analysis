"""Generate a SYNTHETIC e-commerce dataset (v0.1).
Real public data (Olist) replaces this in v1.0. Fixed seed -> reproducible."""
import numpy as np, pandas as pd
from pathlib import Path

rng = np.random.default_rng(42)
OUT = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)

N_CUST, N_ORD = 4000, 12000
regions = ["Ile-de-France", "Auvergne-Rhone-Alpes", "Occitanie", "Nouvelle-Aquitaine", "Hauts-de-France", "Grand Est"]
channels = ["Organic Search", "Paid Social", "Email", "Referral", "Direct"]
categories = {"Electronics": 180, "Home & Kitchen": 65, "Fashion": 45, "Beauty": 30, "Sports": 70, "Books": 18}

customers = pd.DataFrame({
    "customer_id": [f"C{i:05d}" for i in range(1, N_CUST + 1)],
    "region": rng.choice(regions, N_CUST, p=[.32, .17, .14, .13, .12, .12]),
    "acquisition_channel": rng.choice(channels, N_CUST, p=[.30, .25, .15, .10, .20]),
    "signup_date": pd.to_datetime("2024-01-01") + pd.to_timedelta(rng.integers(0, 420, N_CUST), unit="D"),
})

# loyal customers order more often (skewed distribution)
weights = rng.pareto(1.5, N_CUST) + 1
cust_idx = rng.choice(N_CUST, N_ORD, p=weights / weights.sum())
cust = customers.iloc[cust_idx].reset_index(drop=True)
days_left = (pd.Timestamp("2025-12-31") - cust["signup_date"]).dt.days.to_numpy()
order_date = cust["signup_date"] + pd.to_timedelta((rng.random(N_ORD) * days_left).astype(int), unit="D")

cat = rng.choice(list(categories), N_ORD, p=[.18, .22, .24, .14, .12, .10])
price = np.round([categories[c] * rng.lognormal(0, .35) for c in cat], 2)
qty = rng.choice([1, 1, 1, 2, 2, 3], N_ORD)
promised = rng.integers(3, 8, N_ORD)
# regions far from the warehouse get more delays
delay_bias = np.where(cust["region"].isin(["Occitanie", "Nouvelle-Aquitaine"]), 1.5, 0)
actual = np.maximum(1, promised + np.round(rng.normal(-0.5 + delay_bias, 2.2, N_ORD))).astype(int)
days_late = np.maximum(0, actual - promised)
# review score falls when delivery is late (this is the pattern the analysis should discover)
review = np.clip(np.round(rng.normal(4.4 - 0.45 * days_late, 0.7)), 1, 5).astype(int)
status = np.where(rng.random(N_ORD) < .03, "cancelled", "delivered")

orders = pd.DataFrame({
    "order_id": [f"O{i:06d}" for i in range(1, N_ORD + 1)],
    "customer_id": cust["customer_id"],
    "order_date": order_date.dt.date,
    "product_category": cat,
    "unit_price": price,
    "quantity": qty,
    "order_status": status,
    "promised_days": promised,
    "delivery_days": np.where(status == "delivered", actual, np.nan),
    "review_score": np.where(status == "delivered", review, np.nan),
})
# realistic dirt for the cleaning step: duplicates + missing reviews
orders.loc[rng.choice(N_ORD, 250, replace=False), "review_score"] = np.nan
orders = pd.concat([orders, orders.sample(40, random_state=1)], ignore_index=True)

customers.assign(signup_date=customers.signup_date.dt.date).to_csv(OUT / "customers.csv", index=False)
orders.to_csv(OUT / "orders.csv", index=False)
print(f"customers: {len(customers)}  orders (incl. 40 duplicates): {len(orders)}")
