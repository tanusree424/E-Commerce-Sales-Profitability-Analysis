E-Commerce Sales & Profitability Analysis | Power BI
Project Overview
This portfolio project analyzes e-commerce sales, profitability, product performance, and customer behavior using Power BI. The report contains six interactive dashboard pages designed to translate transactional data into business insights and recommendations.
Business Problem
Sales revenue is increasing, but profit is not growing at exactly the same rate. The objective is to examine revenue and profit trends, cost efficiency, product-level margins, discounts, and customer patterns to identify potential opportunities to improve profitability.
Tools and Skills
- Power BI: Interactive dashboards, data modeling, DAX measures, filters, and conditional formatting
- Power Query: Data preparation and transformation
- SQL / MySQL: Data exploration and querying
- Analytical skills: KPI validation, year-over-year comparison, profitability analysis, customer segmentation, and business storytelling
Dashboard Pages
Page	Focus
Customer Overview	Revenue, cost, profit, regional performance, customer segments, and leading customers
Sales Analysis	Sales trends, orders, category contributions, regional sales, and leading products
Profit Analysis	Profit trends, revenue-versus-profit comparisons, and profitability by category and product
Product Analysis	Product sales, category contribution, returns, and product performance
Customer Analysis	Customer counts, repeat purchases, geographic concentration, and purchasing behavior
Profitability & Root Cause Analysis	Revenue and profit growth, cost-to-revenue ratio, discounts versus margins, category margins, and product-level margin gaps


Key Performance Indicators
Approximate values displayed on the dashboards; validate measures and report filters before publication.
Metric	Dashboard Value
Total Revenue / Net Sales	115.63M
Total Profit	32.07M
Total Cost	83.43M
Overall Profit Margin	27.74%
Total Orders	6,474
Total Products	178
Average Order Value	17.86K
Product Analysis Return Rate	9.36%


Note: Monetary units follow the source dashboard and dataset. Customer metrics can change with date filters; the Customer Analysis page currently shows 1,112 total customers and 880 repeat customers, pending measure validation.

Key Business Insights
1. Revenue and profit are growing at slightly different rates
The dashboard reports 2025 revenue growth of approximately 164.50% and profit growth of 162.54%. The difference is relatively small, so the evidence does not indicate a major overall profitability collapse. Year-over-year comparisons should be checked against equivalent reporting periods.
2. Overall cost intensity is relatively stable
The cost-to-revenue ratio is approximately 72.04% in both 2024 and 2025. This suggests that a large increase in aggregate costs relative to revenue is not clearly established as the explanation for the growth gap.
3. Revenue is concentrated in two categories
Furniture contributes approximately 45.68% of sales and Electronics approximately 29.67%. Together, they account for roughly three-quarters of sales, making their performance especially important to overall results.
4. High revenue does not guarantee a strong margin
Jamuna Smartphone Classic 646 generates approximately 7.13M in revenue but has a 16.98% profit margin, below the 27.74% overall business margin. Its pricing, procurement costs, and discounting merit further investigation.
5. Profitability differs by category and product
The category-level dashboard shows differences in profit margins. Electronics performs relatively strongly among identified categories, while Home & Kitchen has a lower displayed margin. An Unknown category also appears and should be investigated before drawing category-specific conclusions.
6. Discounting alone does not explain product margins
The discount-versus-profit-margin scatter plot shows products with similar discounts but different margins. This supports investigating costs and product mix alongside discounting, rather than assuming discounts are the sole cause.
7. Customer activity is concentrated geographically
The Customer Analysis dashboard shows Dhaka as the leading city by customer count among the five displayed, followed by Gazipur and Tangail. These markets warrant closer analysis of repeat purchases, order value, and profitability.
Business Recommendations
1. Investigate high-revenue products with below-average profit margins, including product costs, pricing, and discounts.
2. Monitor revenue, profit, and margin together at both category and product levels.
3. Assess discount effectiveness within comparable products or categories instead of relying on an overall average.
4. Strengthen regional inventory and marketing decisions with demand and profitability metrics.
5. Track new and repeat customers by first purchase date and customer cohorts.
6. Standardize KPI definitions, reporting periods, and treatment of missing product/customer classifications.
Analytical Approach
1. Explore and clean the e-commerce transactional dataset.
2. Prepare the model and define DAX measures for sales, cost, profit, margins, growth, and customer metrics.
3. Build six Power BI dashboard pages to examine performance from multiple business perspectives.
4. Compare revenue growth with profit growth and cost efficiency.
5. Drill down into category and product margins, discounts, returns, and customer patterns.
6. Document findings, limitations, and business recommendations.
Project Structure
Ecommerce-Sales-Profitability-Analysis/
├── README.md
├── dashboard/
│   └── Ecommerce_Dashboard.pbix
├── data/
│   └── cleaned_ecommerce_data.csv
├── screenshots/
│   ├── customer_overview.png
│   ├── sales_analysis.png
│   ├── profit_analysis.png
│   ├── product_analysis.png
│   ├── customer_analysis.png
│   └── profitability_root_cause.png
└── reports/
    └── Business_Insights_Report.pdf
Suggested repository layout: add or rename files to match your actual repository contents. Do not upload confidential or restricted datasets.
How to Explore the Dashboard
1. Open dashboard/Ecommerce_Dashboard.pbix in Power BI Desktop.
2. Navigate between the six report pages.
3. Use available date, region, customer, and product filters to explore performance.
4. Inspect the profitability page to compare growth, costs, discounts, and margins.
Data Quality and Interpretation Notes
- The Product Analysis Total Discount card currently displays an implausible percentage and needs a corrected measure before publication.
- The Customer Analysis page shows New Customers = Total Customers; the definition should be reviewed for the selected date range.
- A large (Blank) customer-name category and an Unknown product category require investigation.
- The product table's Top N total represents the selected products, not the whole company.
- Growth comparisons involving partial years or small base periods can be misleading.
- The dashboard identifies associations and potential improvement areas; it does not prove that discounts, costs, or customer behavior caused the profit-growth difference.
Conclusion
Revenue and profit have grown substantially, with overall profitability remaining relatively stable. Product- and category-level margin differences offer useful opportunities for deeper investigation. The project demonstrates how Power BI can connect financial KPIs with operational and customer data to support evidence-based decisions.