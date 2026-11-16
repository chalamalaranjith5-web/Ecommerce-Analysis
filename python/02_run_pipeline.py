"""Load raw CSVs into a local SQLite warehouse, run the SQL models, export marts + charts."""
import sqlite3, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
con = sqlite3.connect(ROOT / "data" / "warehouse.db")

# 1. Load raw (the "L" of ELT)
pd.read_csv(ROOT / "data/raw/orders.csv").to_sql("raw_orders", con, if_exists="replace", index=False)
pd.read_csv(ROOT / "data/raw/customers.csv").to_sql("raw_customers", con, if_exists="replace", index=False)

# 2. Transform: run SQL models in order
for f in sorted((ROOT / "sql").glob("*.sql")):
    con.executescript(f.read_text())
    print("ran", f.name)

# 3. Data quality checks (simple tests)
q = lambda s: con.execute(s).fetchone()[0]
assert q("SELECT COUNT(*) - COUNT(DISTINCT order_id) FROM stg_orders") == 0, "duplicate order_id"
assert q("SELECT COUNT(*) FROM stg_orders WHERE revenue <= 0") == 0, "non-positive revenue"
assert q("SELECT COUNT(*) FROM stg_orders o LEFT JOIN stg_customers c USING(customer_id) WHERE c.customer_id IS NULL") == 0, "orphan orders"
print("data tests passed")

# 4. Export marts for Power BI
out = ROOT / "data" / "marts"; out.mkdir(exist_ok=True)
marts = {}
for t in ["mart_monthly_kpis", "mart_delay_vs_review", "mart_region", "mart_segment_summary", "mart_channel_retention", "mart_customer_rfm"]:
    marts[t] = pd.read_sql(f"SELECT * FROM {t}", con)
    marts[t].to_csv(out / f"{t}.csv", index=False)
    if t != "mart_customer_rfm":
        print(f"\n== {t} ==\n{marts[t].to_string(index=False)}")

# 5. Charts
plt.rcParams.update({"figure.dpi": 130, "axes.spines.top": False, "axes.spines.right": False, "font.size": 10})
img = ROOT / "images"
d = marts["mart_delay_vs_review"]
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(d.delay_bucket, d.avg_review, color=["#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"])
ax.bar_label(bars, fmt="%.2f"); ax.set_ylim(0, 5)
ax.set_title("Average review score by delivery delay"); ax.set_xlabel("Days late"); ax.set_ylabel("Avg review (1-5)")
fig.tight_layout(); fig.savefig(img / "delay_vs_review.png")

s = marts["mart_segment_summary"]
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.barh(s.segment, s.revenue_share_pct, color="#264653")
ax.bar_label(bars, fmt="%.1f%%"); ax.invert_yaxis()
ax.set_title("Share of revenue by RFM customer segment"); ax.set_xlabel("% of revenue")
fig.tight_layout(); fig.savefig(img / "rfm_segments.png")

m = marts["mart_monthly_kpis"]
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(m.order_month, m.revenue / 1000, marker="o", color="#264653")
ax.set_title("Monthly revenue (k EUR)"); ax.set_xticks(m.order_month[::3])
ax.tick_params(axis="x", rotation=45)
fig.tight_layout(); fig.savefig(img / "monthly_revenue.png")
print("\ncharts saved to images/")
