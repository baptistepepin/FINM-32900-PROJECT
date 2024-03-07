#!/usr/bin/env python
# coding: utf-8

# # Do short sellers respond to ESG ratings?
# 
# This notebook has been design as a reference guide of the cleaning and comparison process conducted in the project as well as some of the analysis performed.

# Before starting the project, we will need to install the `wrds package`. We can do this by running `pip install wrds` in our terminal. For more information, refer to: https://pypi.org/project/wrds/. This package will be used for examining datasets on the Wharton Research Data Services (WRDS) platform, and extracting data to Pandas dataframes. A WRDS account is required, however since we are UChicago students we have access to this dataset already. The package is included in the requirements.txt for the project. 

# In[ ]:


import wrds
import config


# Then, we generate the connection using our API information

# In[ ]:


WRDS_USERNAME = config.WRDS_USERNAME
db = wrds.Connection(wrds_username=WRDS_USERNAME)


# ## 1. Introduction
# 
# This project amis to investigative the intricate relationship between Environmental, Social, and Governance (ESG) events and securities lending activities. Our goal is to provide a nuanced understanding of the interplay between ESG considerations and market activities, offering valuable insights into the considerations of short sellers in the context of ESG events. At the heart of our inquiry lies the pivotal question: 
# 
# $$\textbf{Is there a relationship between ESG events and securities lending activity?}$$ 
# $$\textbf{Do short sellers incorporate ESG events in their investment decisions?}$$
# 
# The relationship between Environmental, Social, and Governance (ESG) events and securities lending activities is a complex and multifaceted area of study within the financial market. The ESG events range from environmental disasters, social injustices, to governance failures—impact the behavior of short sellers and the broader securities lending market. 
# 
# #### Environmental Events
# 
# Environmental events can include incidents such as oil spills, deforestation, or emissions scandals. These events often lead to public backlash, regulatory scrutiny, and potentially significant financial impacts on the involved companies. Short sellers, anticipating a drop in stock prices due to these negative outcomes, may increase their activities. Consequently, the demand for borrowing shares of such companies may rise, affecting the securities lending market by increasing loan fees and utilization rates.
# 
# #### Social Events
# 
# Social events encompass issues like labor disputes, violations of human rights, and poor working conditions. These incidents can harm a company's reputation, leading to consumer boycotts or loss of investor confidence. Short sellers might view companies embroiled in social controversies as more likely to experience stock price declines, prompting an uptick in short selling activity. This dynamic can alter the supply-demand equilibrium in the securities lending market for the shares of the affected companies.
# 
# #### Governance Events
# 
# Governance events involve instances of poor management practices, corruption, executive misconduct, or lack of accountability. Such governance failures can erode investor trust and lead to financial penalties, impacting a company's stock performance. Short sellers often monitor these governance indicators as predictors of potential stock depreciation, influencing their investment strategies and, by extension, the securities lending market through variations in borrowing demand.

# #### Securities Lending Market Dynamics
# 
# The Securities Lending Market is a crucial component of the financial markets, providing liquidity and facilitating the smooth functioning of securities trading. In this market, securities are temporarily transferred from one party to another. The lender of the securities, typically institutional investors like pension funds or mutual funds, loans out securities to borrowers, often for the purpose of short selling. The borrower, in return, provides collateral to the lender, which can be cash, other securities, or a letter of credit, and pays a fee based on an agreed-upon percentage of the loaned securities' value.
# 
# Market dynamics in securities lending are influenced by supply and demand for specific securities. High demand for borrowing certain securities can lead to higher lending fees, making it more profitable for lenders.

# ## 2. Financial Data Pulling 
# 
# To study this puzzling fact, we will refer to WRDS database. Wharton Research Data Services (WRDS) is a comprehensive repository of financial, economic, and insurance data. Renowned for its high-quality, reliable information, WRDS is indispensable for conducting precise financial analysis and research. Utilizing the WRDS platform, specifically through the wrds package, enables the swift and efficient extraction of large datasets. This efficiency in data collection affords researchers more time for in-depth analysis.
# 
# For this project, we have chosen to utilize multiple datasets, including:
# 
# * The **RepRisk Library**, which evaluates environmental, social, and governance (ESG) risks, as well as business conduct, using an extensive array of public sources. The incident-based data encompasses a variety of issues such as environmental impacts, labor practices, human rights, supply chain management, corruption, legal disputes, and regulatory violations.
# 
#     Additionally, this dataset features the RepRisk Index (RRI), which dynamically captures and quantifies reputational risk exposure related to ESG issues. The RepRisk Rating (RRR), ranging from AAA to D, allows for the benchmarking and integration of ESG and business conduct risks.
# 
# * The **IHS Markit library** is a leading, global financial information services company with over 15,000 employees. The company provides independent data, valuations and trade processing across all asset classes in order to enhance transparency, reduce risk and improve operational efficiency.
# 
# After thorough data cleaning, analysis, and comparison of the datasets mentioned above, the project will elucidate whether a relationship exists between ESG events and securities lending activities, offering insights into the considerations of short sellers regarding ESG events in their investment strategies.

# ### 2.1. Download and Read the data from RepRisk
# 
# As previously stated, we will start by importing the information from the `company_identifiers` table from the RepRisk library using a database connection object. This table contains identifiers for companies analyzed, providing essential data for researching company-specific environmental, social, and governance (ESG) risks.

# In[ ]:


# RepRisk - Company Identifiers
RepRisk_company_identifiers = db.get_table(library='reprisk', table='v2_company_identifiers')
RepRisk_company_identifiers.head()


# From the `company_identifiers` table the following variables will be extracted:
# 
# 1. reprisk_id (COMAPNY ID)
# 2. company_name	(COMPANY Name)
# 3. headquarters_country	(Headquarters Country)
# 4. headquarters_country_isocode	(Headquarters Country ISO Code)
# 5. sectors (Sector(s))
# 6. url (URL)
# 7. isins (Isin(s))
# 8. primary_isin	(Primary ISIN)
# 9. no_reported_risk_exposure (No reported risk exposure) 

# From the Reprisk database, we will also import the `risk_incidents` table which has compiling information on various risk incidents since 2007. This dataset is notably large, encompassing an array of metrics that exceed the requirements of this project. To streamline the dataset and enhance its efficiency, we will refine our focus to a select group of columns. Specifically, we will retain only the following columns: *reprisk_id, story_id, incident_date, unsharp_incident, related_countries, related_countries_codes, severity, reach, novelty, environment, social, and governance*.

# In[ ]:


# RepRisk - Risk Incidents available since 2007
RepRisk_risk_incidents = db.get_table(library='reprisk', table='v2_risk_incidents')
RepRisk_risk_incidents.head()


# From the `risk_incidents` table the following variables will be extracted:
# 
# 1. company_name	(COMPANY Name)
# 2. headquarters_country_isocode	(Headquarters Country ISO Code)
# 3. primary_isin	(Primary ISIN)
# 4. reprisk_id (Reprisk Company ID)
# 5. story_id	(Story ID)
# 6. incident_date (Incident Date)
# 7. unsharp_incident	(Unsharp Incident)
# 8. related_countries (Related Countries)
# 9. related_countries_codes (Related Countries Codes)
# 10. severity (Severity)
# 11. reach (Reach)
# 12. novelty	(Novelty)
# 13. environment	(ENVIRONMENT)
# 14. social (SOCIAL)
# 15. governance (GOVERNANCE)

# Finally, we will import the `metrics` table from the Reprisk library. Out of all the metrics available, we will only focus on :
# 
# * The *Current RRI* denotes the current level of media and stakeholder attention of a company related to ESG issues.
# * The *Trend RRI* states the difference in the RepRisk Index (RRI) between current date and the date 30 days ago.
# * The *RepRisk Rating RRR* facilitates corporate benchmarking against a peer group and the sector, as well as integration of ESG and business conduct risks into business processes. It combines the company-specific ESG risk exposure (provided by the Peak RRI) and the Country-Sector ESG risk exposure (provided by the Country-Sector Average value of a company).

# In[ ]:


# RepRisk - Metrics available since 2007
RepRisk_metrics = db.get_table(library='reprisk', table='v2_metrics', obs=10)
RepRisk_metrics.head()


# From the `metrics` table the following variables will be extracted:
# 
# 1. company_name	(COMPANY Name)
# 2. headquarters_country_isocode	(Headquarters Country ISO Code)
# 3. primary_isin	(Primary ISIN)
# 4. reprisk_id (RepRisk COMPANY ID)
# 5. date	(Date)
# 6. current_rri (Current RRI)
# 7. trend_rri (Trend RRI)
# 8. peak_rri	(Peak RRI)
# 9. peak_rri_date (Peak RRI Date)
# 10. reprisk_rating (RepRisk Rating)

# The three previous Reprisk tables will be extracted under the same SQL query since they belong to the same library. Furthermore, they will be joined using the `reprisk_id`, a unique identifier available in each table. 
# 
# The extraction and loading process is managed by `load_reprisk.py` a Python script designed for efficient data retrieval. 

# ### 2.2. Download and Read the data from Markit
# 
# The next step is to download the data from the Markit Securities database. Initially, the data was going to get extracted from the American Equities table know as `msfaamer`, however, after checking the available tables under the `msfanly` library, we discovered is not longer available, and neither is in the `markit_msf_analytics_eqty_amer` library. So the only feasible workaround is extract the Markit data year by year instead from the `amereqty` table. 
# 
# You will find the code that extracts the data for the multiple years and load it into the system in the file called `load_markit.py`.

# In[ ]:


MarkitSecurities_american_equities_2024 = db.get_table(library='msfanly', table='amereqty2024', obs=10)
MarkitSecurities_american_equities_2024.head()


# From the `amereqty` table the following variables will be extracted:
# 
# 1. datadate	(Date)
# 2. dxliD (DataExplorer ID)
# 3. isin	(Primary ISIN)
# 4. sedol (Stock Exchange Daily Official List number)
# 5. cusip (Committee on Uniform Securities Identification Procedures number)
# 6. instrumentname (Financial Instrument Name)
# 7. indicativefee (Indicative Fee)
# 8. utilisation	(Utilisation)
# 9. shortloanquantity (Short On Loan Quantity)
# 10. quantityonloan (Quantity On Loan)
# 11. lendablequantity (Lendable Quantity)
# 12. lenderconcentration (Lender Concentration)
# 13. borrowerconcentration (Borrower Concentration)
# 14. inventoryconcentration (Inventory Concentration)

# ### 2.3. Download and Read the data from CRSP

# Unfortunatelly, not all the required data to compute the ratios can be extracted from the two previous libraries, specially the data regarding outstanding shares, hence we will need to download data from CRSP (Center for Research in Security Prices) database for a specified date range. 
# 
# To ensure compatibility with the other imported datasets, we will need to compute the CUSIP id. This number is very useful for linking purposes and can be computed combining the CRSP identifiers permno, permco, cusip (columns that will be imported). Then, we will join this crspid table with the MSF identifiers through the common historical CUSIP link. For more information, refer to https://wrds-www.wharton.upenn.edu/pages/wrds-research/database-linking-matrix/linking-markit-with-crsp-2/#connecting-with-crsp
# 
# The extraction will be done through wrd pacakge, using the `crspq.stksecurityinfohist` library. You will find the code that extracts this data and loads in the file called `load_crps.py`.

# In[ ]:


# CRSP Daily Stock available since 1925

CRSP_daily_stock = db.get_table(library='crspq', table='dsf', columns=['cusip', 'date', 'permco', 'permno', 'shrout'], obs=10)
CRSP_daily_stock.head()


# From the `dsf` table the following variables will be extracted:
# 
# 1. date (Date)
# 2. permno
# 3. permco
# 4. cusip
# 5. shrout (Shares Outstanding)

# ### 2.4. Download and Read the data from FRED

# Lastly, we will download the data from FRED (Federal Reserve Economic Data) which is a comprehensive database maintained by the Research division of the Federal Reserve Bank of St. Louis. It offers access to a vast of economic data time series from more than 80 national, international, public, and private sources. FRED aggregates a wide array of data, including employment, GDP, inflation rates, and hundreds of other economic indicators that are essential for economic research, forecasting, and policy analysis.
# 
# This database will be useful to extract the information regarding the CPI (Consumer Price Index), Nominal GDP (Gross Domestic Product) and real GDP. You will find the code that extracts this data from the `mkdir` table and loads in the file called `load_fred.py`.

# In[ ]:


# Code to show data from FRED


# From the `mkdir` table the following variables will be extracted:
# 
# 1. CPI (Consumer Price Index)
# 2. Noinal GDP
# 3. Real GDP

# # 3. Data Manipulation
# 
# # 3.1. Data Merging
# 
# The data merging operation was structured in two distinct phases to bolster the accuracy and reliability of the data integration process, ensuring that data correlations consistent. Initially, the process focused on the integration of Markit data with the CRSP (Center for Research in Security Prices) database and after its successful amalgamation, the second phase introduced the integration of Reprisk data, a strategic move designed to enrich the dataset with environmental, social, and governance (ESG) risk assessments. 
# 
# Each step in the process is executed with precision, leveraging custom-designed functions to guarantee that the integration not only maintains data integrity but also optimizes the dataset for nuanced analysis, avoiding data repetition or missing values. 
# 
# 
# ## 3.1.1. Merging Markit - CRSP  
# 
# The `merge_markit_crsp.py` module facilitates the merging of Markit and CRSP datasets by aligning them on dates and CUSIP8 identifiers. This merging process results in a unified table that inherently includes all the necessary details to calculate key financial ratios, so instead of creating another function that returns the required ratios, the function itself enriches the dataset by appending four additional columns, which represent the short interest, loan supply, loan utilisation, and loan fees ratios.
# 
# For the incorporation of RepRisk data alongside these datasets, WRDS suggests prioritizing the ISIN number for matching purposes with CUSIP. Nonetheless, given the notable occurrence of missing ISIN numbers within the RepRisk dataset, a fallback strategy involves matching based on company names. 
# 
# 
# # 3.1.2. Merging Markit - CRSP - RepRisk
# 
# The `merge_markit_crsp_reprisk.py` module contain the function designed to integrate a pre-merged Markit and CRSP dataframe with a Reprisk dataframe, based on shared 'cusip' and 'date' fields.
# 
# +++

# # 3.1. Recode the missing data
# 
# * Drop na
# * forwards fill
# 
# Still TBD
# 
# # 3.2. Select the desired subsample of the data
# 
# * 2022 to 2024 - test it and later try a wider date range
# 
# # 3.3. Drop data that we no longer need
# 
# TBD

# # 4. Construct new metrics

# ## 4.1. Ratios
# 
# This project aims to empirically examine whether there is a quantifiable relationship between ESG events and changes in securities lending activity, such as variations in short interest ratios, loan supply ratios, and loan fees. By analyzing data on ESG incidents and securities lending metrics, the study seeks to determine if and how short sellers incorporate ESG considerations into their investment decisions, potentially using ESG events as indicators to guide their short-selling strategies. 
# 
# In the realm of securities lending, several key metrics are pivotal for assessing market dynamics and investor sentiment. Below, we delve into the critical ratios and explore additional variables of interest within the Markit dataset.
# 
# ### Key Ratios
# 
# 1. **Short Interest Ratio**: This ratio indicates the proportion of shares that are currently borrowed for short selling compared to the total shares outstanding. A higher ratio suggests a more significant interest in short selling the stock, potentially indicating bearish market sentiment towards the company.
# 
#    $$\text{Short Interest Ratio} = \frac{\text{Shares on Loan}}{\text{Shares Outstanding}} \quad \text{or} \quad \frac{\text{QuantityOnLoan}}{\text{SHROUT}}$$
# 
# 2. **Loan Supply Ratio**: This metric measures the availability of shares for lending against the total shares outstanding. It reflects the willingness of shareholders to lend their shares for short selling, indicating the liquidity and accessibility of shares for short sellers.
# 
#    $$\text{Loan Supply Ratio} = \frac{\text{Shares Available to be Lent}}{\text{Shares Outstanding}} \quad \text{or} \quad \frac{\text{LendableQuantity}}{\text{SHROUT}}$$
# 
# 3. **Loan Utilization Ratio**: This ratio compares the demand to the supply of loanable shares. A higher utilization rate suggests a strong demand for borrowing shares, often associated with an increased short selling activity.
# 
#    $$\text{Loan Utilization Ratio} = \text{Utilisation}$$
# 
# 4. **Loan Fee**: The indicative fee associated with borrowing shares. This fee can vary based on the demand and supply dynamics of the loanable shares, acting as a cost indicator for short sellers.
# 
#    $$\text{Loan Fee} = \text{IndicativeFee}$$
# 
# ### Additional Variables of Interest in Markit
# 
# - **LenderConcentration**: Measures the concentration of shares being lent by a small number of lenders. A higher concentration could indicate a less competitive lending market, potentially affecting loan fees and availability.
# 
# - **BorrowerConcentration**: Reflects the concentration of shares borrowed by a small number of borrowers. This can highlight the dependency on certain borrowers and potential risks associated with borrower default.
# 
# - **InventoryConcentration**: Indicates the concentration of shares available for lending held by a few entities. High concentration may suggest potential manipulation or control over the lending market by a limited number of participants.
# 
# Exploring these ratios and variables provides a comprehensive view of the securities lending market, offering insights into short selling trends, market sentiment, and the operational dynamics of the lending ecosystem.

# ## 4.2. Summary statistics

# <font color = 'blue'>
# 
# **REMOVE**
# 
# 3.	Summary statistics (p10, p25, p50 / median, p75, p90, mean, SD, N):
# 
#     a.	For each level of ESG incident / severity / novelty / news reach / disentangled E, S, and G risks, produce summary statistics on:
#         
#     * i.	Contemporaneous short interest, loan supply, loan utilization, and loan fees.
#     * ii.	Changes in short interest, loan supply, loan utilization, and loan fees from time of ESG incident to 1-week / 1-month ahead
# 
#     b.	Feel free to include summary statistics on any additional variables which may be of interest!
# 

# For the summary statistics part we have computed the following metrics:
# 
# Some of the chosen metrics have been `quantiles` which are cut points dividing the range of a probability distribution into continuous intervals with equal probabilities
# 
# * 10% quantile  
# * 25% quantile
# * 50% quantile (or median)  
# * 75% quantile  
# * 90% quantile  
# 
# We have also computed the `mean`, so the average of a data set, the `standard deviation`, to measure of how dispersed the data is in relation to the mean and finally the `count`, so the amount of data points analyzed.

# <font color = 'red'>
# 
# **Add to which columns we have computed the statistics metrics**

# 
