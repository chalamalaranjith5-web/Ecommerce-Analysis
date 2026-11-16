# Business Recommendations (v0.1 – synthetic data)

## Context
An online retailer wants to improve customer satisfaction and repeat purchases.

## KPI definitions
| KPI | Definition |
|---|---|
| Late delivery % | delivered orders where delivery_days > promised_days |
| Avg review | mean review score (1–5), orders with a review only |
| Bad review % | share of reviews scoring 1 or 2 |
| Repeat rate | customers with 2+ delivered orders / all customers |
| RFM segment | Recency, Frequency, Monetary quartiles → Champions / Promising / At Risk / Hibernating |

## Recommendations
1. **Fix delivery in Occitanie and Nouvelle-Aquitaine first.** About 6 in 10 orders there arrive late, and reviews drop fast after 2 days late. Options: a regional carrier, or more realistic promised dates.
2. **Protect the "At Risk" segment.** They used to buy often but have stopped recently, and they still represent 17% of revenue. A win-back email campaign is cheaper than acquiring new customers.
3. **Alert when an order passes 2 days late.** Above 3 days late, bad reviews jump from 5% to 30%. A proactive message or voucher could limit the damage.

## Next step
Validate these findings on real data (Olist, v1.0).
