from fpdf import FPDF
from datetime import datetime
import os

class RiskReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Risk Assessment Report', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, body)
        self.ln()

def generate_q1_2024_report():
    """Q1 2024 - Normal conditions"""
    pdf = RiskReportPDF()
    pdf.add_page()
    
    pdf.chapter_title("Executive Summary - Q1 2024")
    pdf.chapter_body("""
The first quarter of 2024 showed stable loan portfolio performance with default rates remaining 
consistent at 8.2%, in line with historical averages. Economic conditions remained favorable 
with steady employment rates and moderate interest rates.

Key Highlights:
- Total loan originations: $2.1B across all products
- Default rate: 8.2% (within target range of 7-9%)
- Average credit score of applicants: 685
- Geographic concentration: Ontario (42%), British Columbia (28%), Alberta (18%)
""")
    
    pdf.chapter_title("Loan Portfolio Performance")
    pdf.chapter_body("""
Mortgage Products: Performed strongly with only 3.2% default rate. The low interest rate 
environment and strong housing market in major urban centers contributed to excellent performance.

Personal Loans: Default rate of 9.1%, slightly above target but within acceptable range. 
Concentrated in younger demographics (25-35 age range) with moderate income levels.

Auto Loans: Stable at 6.8% default rate. Longer loan terms (60-72 months) becoming more common 
but not yet showing elevated risk.

Small Business Loans: Default rate of 11.3%. Small businesses in retail and hospitality sectors 
showing some stress due to changing consumer behavior, but overall portfolio remains healthy.

Credit Cards: Revolving credit showing 12.1% default rate, consistent with industry standards.
""")
    
    pdf.chapter_title("Risk Factors & Mitigation")
    pdf.chapter_body("""
Identified Risk Factors:
1. Interest Rate Sensitivity: Bank of Canada signaled potential rate increases in coming quarters. 
   Variable rate mortgage holders may face payment stress.

2. Regional Concentration: High exposure to Ontario and BC real estate markets. A correction 
   in housing prices could impact mortgage performance.

3. Credit Score Trends: Slight decline in average applicant credit scores (down 5 points YoY), 
   suggesting potential quality degradation.

Mitigation Strategies:
- Enhanced stress testing for variable rate mortgages
- Diversification efforts in Prairie provinces
- Tightened underwriting standards for sub-650 credit scores
- Increased monitoring of high-risk sectors (retail, hospitality)
""")
    
    pdf.chapter_title("Forward-Looking Assessment")
    pdf.chapter_body("""
Outlook for Q2 2024: MODERATE RISK

The economic environment remains supportive but warning signs are emerging:
- Bank of Canada likely to raise rates by 50-75 basis points
- Employment data showing early signs of softening
- Consumer debt levels at record highs
- Housing market showing cooling in major markets

Recommendation: Maintain current risk appetite but prepare for potential deterioration in Q2-Q3.
Recommend increasing provisions by 15% as a precautionary measure.
""")
    
    os.makedirs('app/data/unstructured', exist_ok=True)
    pdf.output('app/data/unstructured/Q1_2024_Risk_Report.pdf')
    print("✅ Generated Q1 2024 Risk Report")

def generate_q2_2024_report():
    """Q2 2024 - Conditions deteriorating (explains the default spike!)"""
    pdf = RiskReportPDF()
    pdf.add_page()
    
    pdf.chapter_title("Executive Summary - Q2 2024")
    pdf.chapter_body("""
ALERT: The second quarter of 2024 showed significant deterioration in loan portfolio performance 
with default rates jumping to 14.7%, well above our risk tolerance threshold of 9%. This represents 
a 79% increase from Q1 levels and requires immediate attention.

Key Highlights:
- Total loan originations: $1.8B (down 14% from Q1) - tightened standards
- Default rate: 14.7% (CRITICAL - outside acceptable range)
- Average credit score of applicants: 671 (continued decline)
- Delinquency rates increased across all products
""")
    
    pdf.chapter_title("Root Cause Analysis")
    pdf.chapter_body("""
CRITICAL FACTORS CONTRIBUTING TO DEFAULT SPIKE:

1. Interest Rate Shock (PRIMARY DRIVER):
   Bank of Canada raised rates by 75 basis points in April and another 50 bps in June, bringing 
   the overnight rate to 5.0%. Variable rate mortgage holders experienced average payment increases 
   of 28%, creating significant financial stress.

2. Employment Market Deterioration:
   - Unemployment rose from 5.1% to 6.3% during the quarter
   - Tech sector layoffs impacted high-income earners in Toronto and Vancouver
   - Retail and hospitality sectors shed 42,000 jobs nationally

3. Cost of Living Crisis:
   - Inflation remained elevated at 6.8% despite rate increases
   - Food prices up 11.2% YoY, gasoline up 18.3%
   - Disposable income squeezed across all demographics

4. Housing Market Correction:
   - Average home prices declined 12% in Toronto, 9% in Vancouver
   - Some borrowers now underwater on mortgages
   - Reduced home equity limiting refinancing options

5. Consumer Debt Levels:
   - Average household debt-to-income ratio at 186% (record high)
   - Credit card balances increased 14% as consumers struggled with expenses
   - Line of credit utilization at maximum for many borrowers
""")
    
    pdf.chapter_title("Segment Performance - Detailed")
    pdf.chapter_body("""
Mortgage Products: Default rate SPIKED to 8.9% (from 3.2% in Q1). Variable rate mortgages 
showing 15.3% default rate. Fixed rate performing better at 4.1%. Geographic concentration: 
worst performance in Ontario (11.2% default) and BC (9.7%).

Personal Loans: Default rate jumped to 18.4%. Younger demographics (25-35) hit hardest with 
22.1% default rate. Income levels correlate strongly - sub-$50K income showing 31% default rate.

Auto Loans: Rose to 13.2% default rate. Long-term loans (72+ months) showing 19.8% default. 
Used vehicle loans performing worse than new vehicle loans.

Small Business Loans: CRITICAL at 21.7% default rate. Retail sector at 34.2%, hospitality at 
28.9%. Only technology and healthcare sectors showing stable performance.

Credit Cards: Reached 19.3% default rate with utilization at record highs. Sub-prime segment 
showing 41% default rate.
""")
    
    pdf.chapter_title("Geographic Analysis")
    pdf.chapter_body("""
Provincial Default Rates (Q2 2024):
- Ontario: 16.8% (highest exposure, housing market correction severe)
- British Columbia: 14.2% (tech sector layoffs, housing correction)
- Alberta: 11.3% (energy sector providing some buffer)
- Quebec: 10.9% (lower housing exposure, more stable employment)
- Manitoba: 9.1% (least affected)
- Saskatchewan: 9.8%
- Atlantic provinces: 12.4% (employment challenges)

Urban vs Rural: Major metropolitan areas showing 17.2% default rates vs 11.1% in rural areas.
""")
    
    pdf.chapter_title("Immediate Actions Taken")
    pdf.chapter_body("""
Emergency Response Measures Implemented:

1. Underwriting Standards (IMMEDIATE):
   - Minimum credit score raised to 680 for all unsecured products
   - Debt-to-income ratio cap reduced to 38% (from 42%)
   - Additional income verification for all applications
   - Suspended lending in highest-risk segments

2. Portfolio Management:
   - Increased provisions by 140% (from $420M to $1.01B)
   - Accelerated collection efforts on 30+ day delinquencies
   - Proactive outreach to at-risk borrowers (payment deferrals, restructuring)
   - Reduced exposure to retail and hospitality small business sectors

3. Risk Monitoring:
   - Daily default rate monitoring (previously weekly)
   - Enhanced early warning system implementation
   - Stress testing of entire portfolio under multiple scenarios
   - Executive risk committee now meeting weekly (previously monthly)
""")
    
    pdf.chapter_title("Forward-Looking Assessment")
    pdf.chapter_body("""
Outlook for Q3 2024: HIGH RISK - CRISIS MANAGEMENT MODE

The situation is expected to remain challenging:
- Bank of Canada may implement additional rate increases (25-50 bps likely)
- Employment market likely to weaken further (forecast: 6.8% unemployment by Q3 end)
- Housing prices may decline additional 5-8%
- Consumer spending pullback will impact retail and hospitality further

CRITICAL RISK: Potential for 18-20% default rates if conditions continue to deteriorate.

Recommendations:
1. Maintain tightened underwriting standards through at least Q4 2024
2. Increase provisions by additional 30% to $1.3B
3. Implement aggressive collection strategies
4. Consider portfolio sales for highest-risk segments
5. Prepare stress capital analysis for regulatory review
6. CEO to brief Board of Directors on crisis response plan

This is the most challenging credit environment we have faced since 2008-2009 financial crisis.
Immediate and decisive action is required to protect the bank's capital position.
""")
    
    os.makedirs('app/data/unstructured', exist_ok=True)
    pdf.output('app/data/unstructured/Q2_2024_Risk_Report.pdf')
    print("✅ Generated Q2 2024 Risk Report")

def generate_q3_2024_report():
    """Q3 2024 - Stabilization begins"""
    pdf = RiskReportPDF()
    pdf.add_page()
    
    pdf.chapter_title("Executive Summary - Q3 2024")
    pdf.chapter_body("""
The third quarter showed signs of stabilization with default rates declining to 11.2%, down from 
the Q2 peak of 14.7%. While still elevated compared to historical norms, the trajectory is improving 
and emergency measures appear to be working.

Key Highlights:
- Total loan originations: $1.6B (continued conservative approach)
- Default rate: 11.2% (improving but still elevated)
- Average credit score of applicants: 692 (quality improving due to stricter standards)
- Early delinquency rates showing modest improvement
""")
    
    pdf.chapter_title("Stabilization Factors")
    pdf.chapter_body("""
What Changed in Q3:

1. Interest Rate Pause:
   Bank of Canada held rates steady at 5.0% throughout the quarter, providing relief to 
   variable rate borrowers. Markets now pricing in potential rate cuts in early 2025.

2. Employment Stabilization:
   Unemployment peaked at 6.5% in July but stabilized through September. Tech sector 
   hiring resumed modestly. Retail sector showing resilience.

3. Consumer Adaptation:
   Households adjusting to higher rates. Increased savings rates and reduced discretionary 
   spending helping with debt servicing.

4. Government Support Programs:
   Federal and provincial programs providing targeted support to affected borrowers, 
   reducing default risk.

5. Bank Interventions:
   Proactive loan modifications and payment deferrals preventing defaults. Restructured 
   2,847 loans totaling $412M.
""")
    
    pdf.chapter_title("Forward-Looking Assessment")
    pdf.chapter_body("""
Outlook for Q4 2024 and Beyond: MODERATE RISK - CAUTIOUS OPTIMISM

Expected trajectory:
- Q4 2024: Default rates 9-10% (continued improvement)
- Q1 2025: Return to 8-9% range (near historical norms)
- Rate cuts expected Q1 2025 (25-50 bps) will provide additional relief

Recommendation: Maintain enhanced monitoring but begin gradual return to normal lending standards 
in Q1 2025. Continue elevated provisions through Q4 2024 as precautionary measure.

The crisis appears to be contained, but vigilance remains critical.
""")
    
    os.makedirs('app/data/unstructured', exist_ok=True)
    pdf.output('app/data/unstructured/Q3_2024_Risk_Report.pdf')
    print("✅ Generated Q3 2024 Risk Report")

def generate_lending_policy():
    """Internal lending policy document"""
    pdf = RiskReportPDF()
    pdf.add_page()
    
    pdf.chapter_title("Lending Policy - Credit Risk Standards")
    pdf.chapter_body("""
Document Version: 2024.2
Last Updated: July 1, 2024
Classification: Internal Use Only

This document outlines lending standards and credit risk management framework across 
all retail and commercial lending products.
""")
    
    pdf.chapter_title("Credit Score Requirements")
    pdf.chapter_body("""
Minimum Credit Score Thresholds (Updated July 2024):

Mortgage Products:
- Prime mortgages: 680 minimum (increased from 650)
- Alt-A mortgages: 620 minimum
- Maximum LTV: 80% (95% with CMHC insurance)

Personal Loans:
- Unsecured personal loans: 680 minimum (increased from 640)
- Secured personal loans: 620 minimum
- Maximum loan amount: $50,000 unsecured

Auto Loans:
- New vehicles: 660 minimum
- Used vehicles: 680 minimum
- Maximum term: 72 months (84 months requires executive approval)

Small Business Loans:
- Minimum personal credit score: 680
- Business credit score: 70+ (Paydex equivalent)
- Minimum 2 years operating history

Credit Cards:
- Prime cards: 700 minimum
- Standard cards: 660 minimum
- Secured cards: No minimum (requires security deposit)
""")
    
    pdf.chapter_title("Debt-to-Income Ratio Requirements")
    pdf.chapter_body("""
Maximum DTI Ratios (Updated July 2024):

Mortgage Products:
- GDS (Gross Debt Service): 32% maximum
- TDS (Total Debt Service): 38% maximum (reduced from 42%)
- Stress test: Must qualify at 5.25% or contract rate + 2%, whichever is higher

All Other Products:
- Maximum TDS: 38% including new debt obligation
- High-income exception: 42% for borrowers with income >$150K and credit score >750
""")
    
    pdf.chapter_title("Income Verification Standards")
    pdf.chapter_body("""
Required Documentation:

Salaried Employees (Minimum 2 years continuous employment):
- Two most recent pay stubs
- T4 for previous tax year
- Letter of employment
- Optional: ROE if employment gap exists

Self-Employed / Commission-Based (Minimum 2 years self-employment):
- Two years of complete tax returns (T1 General + NOAs)
- Financial statements (if incorporated)
- Bank statements (6 months) showing income deposits
- Business license/registration

Additional verification required for:
- Rental income: Lease agreements + tax returns
- Investment income: Portfolio statements + T3/T5 slips
- Pension income: Pension statements or direct confirmation
""")
    
    pdf.chapter_title("Risk-Based Pricing Matrix")
    pdf.chapter_body("""
Interest Rate Adjustments Based on Risk Profile:

Credit Score Tiers:
- 750+: Prime rate
- 700-749: Prime + 0.25%
- 680-699: Prime + 0.50%
- 650-679: Prime + 0.75%
- 620-649: Prime + 1.25%
- Below 620: Declined or alternative products only

LTV Adjustments (Mortgages):
- 0-65% LTV: Best rate
- 65-80% LTV: +0.10%
- 80-90% LTV: +0.20% (requires insurance)
- 90-95% LTV: +0.30% (requires insurance)

DTI Adjustments:
- DTI <32%: Standard rate
- DTI 32-38%: +0.15%
- DTI 38-42%: +0.35% (executive approval required)
""")
    
    pdf.chapter_title("Portfolio Concentration Limits")
    pdf.chapter_body("""
Maximum Exposure Limits to Prevent Concentration Risk:

Geographic:
- No single province >45% of total portfolio
- No single metropolitan area >25% of total portfolio

Industry (Small Business):
- No single industry >20% of small business portfolio
- High-risk industries (retail, hospitality) capped at 15% combined

Product:
- Unsecured products <30% of total retail portfolio
- Subprime products <10% of total retail portfolio

Single Borrower:
- Retail: $2M maximum unsecured, $5M maximum secured
- Small business: $10M maximum (requires executive approval above $5M)
""")
    
    os.makedirs('app/data/unstructured', exist_ok=True)
    pdf.output('app/data/unstructured/Lending_Policy_2024.pdf')
    print("✅ Generated Lending Policy Document")

def generate_economic_outlook():
    """External economic outlook document"""
    pdf = RiskReportPDF()
    pdf.add_page()
    
    pdf.chapter_title("Canadian Economic Outlook - 2024")
    pdf.chapter_body("""
Prepared by:((venv) ) stephentorku@Stephens-MacBook-Pro-3 financial-analyst-agent % python app/test_tools.py
🧪 Testing tools...

1. Testing SQL Tool...
   Result: Query executed successfully. Returned 1 rows.

 total_loans
        1000...
   ✅ SQL Tool works!

2. Testing Analysis Tool...
   Result: 5.5
   ✅ Analysis Tool works!

3. Testing Document Search Tool (this takes a minute)...
📚 Loading 5 PDF documents...
  ✅ Loaded Q1_2024_Risk_Report.pdf
  ✅ Loaded Lending_Policy_2024.pdf
  ✅ Loaded Q3_2024_Risk_Report.pdf
  ✅ Loaded Q2_2024_Risk_Report.pdf
  ✅ Loaded Economic_Outlook_2024.pdf
📄 Created 25 text chunks
🔄 Creating embeddings (this may take a minute)...
🆕 Creating new vector store...
Failed to send telemetry event ClientStartEvent: capture() takes 1 positional argument but 3 were given
Failed to send telemetry event ClientCreateCollectionEvent: capture() takes 1 positional argument but 3 were given
✅ Vector store ready!
Failed to send telemetry event CollectionQueryEvent: capture() takes 1 positional argument but 3 were given
   Result: Found relevant information from internal documents:

--- Source: Q2_2024_Risk_Report.pdf ---
Risk Assessment Report
Executive Summary - Q2 2024
ALERT: The second quarter of 2024 showed significan... Economics Department
Date: August 2024
Distribution: Internal

This report provides economic forecast for Canada through 2025 and implications 
for lending operations.
""")
    
    pdf.chapter_title("Interest Rate Environment")
    pdf.chapter_body("""
Bank of Canada Policy Outlook:

Current overnight rate: 5.00% (as of June 2024)

Expected path:
- Q3 2024: Hold at 5.00%
- Q4 2024: Hold at 5.00%
- Q1 2025: Cut to 4.75% (March 2025)
- Q2 2025: Cut to 4.50% (June 2025)
- End 2025: Terminal rate ~4.25%

Rationale: Inflation moderating toward 2% target. Economic growth slowing significantly. 
Unemployment rising creates conditions for rate cuts in early 2025.

Risk: If inflation proves sticky above 3%, BoC may delay cuts or implement fewer cuts than expected.
""")
    
    pdf.chapter_title("Employment and Income")
    pdf.chapter_body("""
Labour Market Forecast:

Unemployment Rate:
- Q3 2024: 6.4%
- Q4 2024: 6.6%
- Q1 2025: 6.7% (peak)
- Q2 2025: 6.5%
- End 2025: 6.2%

Wage Growth:
- Currently: 4.2% YoY
- Expected to moderate to 3.5% by end 2024
- Further moderation to 3.0% through 2025

Sectors at Risk:
- Technology: Continued restructuring, 5-10% headcount reductions expected
- Retail: Store closures and consolidation continuing
- Construction: Residential construction declining 15-20%

Sectors Showing Strength:
- Healthcare: Chronic labor shortages, steady hiring
- Professional services: Moderate growth
- Government: Stable employment
""")
    
    pdf.chapter_title("Housing Market")
    pdf.chapter_body("""
Real Estate Forecast:

National Home Prices:
- Q3 2024: -3% YoY (continued correction)
- Q4 2024: -2% YoY
- 2025: +1% to +3% (stabilization and modest recovery)

Regional Outlook:
- Toronto: -8% in 2024, +2% in 2025 (oversupply concerns)
- Vancouver: -6% in 2024, +3% in 2025
- Calgary/Edmonton: +4% in 2024, +5% in 2025 (energy sector support)
- Montreal: -2% in 2024, +2% in 2025

Sales volumes down 18% YoY due to affordability constraints. First-time buyers largely 
sidelined. Investor activity declined 40%.

Mortgage Stress: 1.2M variable rate mortgages hitting trigger rates or payment caps. 
Approximately 200,000 borrowers at risk of default without intervention.
""")
    
    pdf.chapter_title("Implications for Lending")
    pdf.chapter_body("""
Strategic Recommendations:

1. Mortgage Lending:
   - Maintain conservative underwriting through Q4 2024
   - Begin returning to normal standards Q1 2025 as rates decline
   - Focus on high-quality borrowers with strong employment in stable sectors
   - Emphasize fixed-rate products to reduce variable rate exposure

2. Unsecured Lending:
   - Tighten standards remain appropriate through Q4 2024
   - Credit card limits should be reviewed conservatively
   - Personal loan growth should be moderate and selective

3. Small Business:
   - Avoid concentration in struggling sectors (retail, hospitality, construction)
   - Emphasize healthcare, professional services, technology
   - Require strong personal guarantees

4. Geographic Strategy:
   - Reduce concentration in Toronto and Vancouver
   - Increase focus on Prairie provinces showing stability
   - Quebec market showing resilience

5. Pricing:
   - Maintain risk-based pricing through 2024
   - Begin competitive pricing for prime segments in Q1 2025
   - Expect increased competition as market stabilizes
""")
    
    os.makedirs('app/data/unstructured', exist_ok=True)
    pdf.output('app/data/unstructured/Economic_Outlook_2024.pdf')
    print("✅ Generated Economic Outlook Document")

if __name__ == "__main__":
    print("Generating unstructured documents...")
    
    # Install fpdf if needed
    try:
        from fpdf import FPDF
    except ImportError:
        print("Installing fpdf...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'fpdf'])
        from fpdf import FPDF
    
    generate_q1_2024_report()
    generate_q2_2024_report()
    generate_q3_2024_report()
    generate_lending_policy()
    generate_economic_outlook()
    
    print("\n✅ All unstructured documents generated successfully!")
    print("\nGenerated files:")
    print("- Q1_2024_Risk_Report.pdf")
    print("- Q2_2024_Risk_Report.pdf")
    print("- Q3_2024_Risk_Report.pdf")
    print("- Lending_Policy_2024.pdf")
    print("- Economic_Outlook_2024.pdf")