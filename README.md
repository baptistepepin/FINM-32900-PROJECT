Do short sellers respond to ESG ratings?
==================

# About this project

This project amis to investigative the intricate relationship between Environmental, Social, and Governance (ESG) events and securities lending activities. Our goal is to provide a nuanced understanding of the interplay between ESG considerations and market activities, offering valuable insights into the considerations of short sellers in the context of ESG events. At the heart of our inquiry lies the pivotal question: 

```math
\textbf{Is there a relationship between ESG events and securities lending activity?}
```

```math
\textbf{Do short sellers incorporate ESG events in their investment decisions?}
```

The relationship between Environmental, Social, and Governance (ESG) events and securities lending activities is a complex and multifaceted area of study within the financial market. The ESG events range from environmental disasters, social injustices, to governance failures—impact the behavior of short sellers and the broader securities lending market. 

#### Environmental Events

Environmental events can include incidents such as oil spills, deforestation, or emissions scandals. These events often lead to public backlash, regulatory scrutiny, and potentially significant financial impacts on the involved companies. Short sellers, anticipating a drop in stock prices due to these negative outcomes, may increase their activities. Consequently, the demand for borrowing shares of such companies may rise, affecting the securities lending market by increasing loan fees and utilization rates.

#### Social Events

Social events encompass issues like labor disputes, violations of human rights, and poor working conditions. These incidents can harm a company's reputation, leading to consumer boycotts or loss of investor confidence. Short sellers might view companies embroiled in social controversies as more likely to experience stock price declines, prompting an uptick in short selling activity. This dynamic can alter the supply-demand equilibrium in the securities lending market for the shares of the affected companies.

#### Governance Events

Governance events involve instances of poor management practices, corruption, executive misconduct, or lack of accountability. Such governance failures can erode investor trust and lead to financial penalties, impacting a company's stock performance. Short sellers often monitor these governance indicators as predictors of potential stock depreciation, influencing their investment strategies and, by extension, the securities lending market through variations in borrowing demand.

#### Securities Lending Market Dynamics

The Securities Lending Market is a crucial component of the financial markets, providing liquidity and facilitating the smooth functioning of securities trading. In this market, securities are temporarily transferred from one party to another. The lender of the securities, typically institutional investors like pension funds or mutual funds, loans out securities to borrowers, often for the purpose of short selling. The borrower, in return, provides collateral to the lender, which can be cash, other securities, or a letter of credit, and pays a fee based on an agreed-upon percentage of the loaned securities' value.

Market dynamics in securities lending are influenced by supply and demand for specific securities. High demand for borrowing certain securities can lead to higher lending fees, making it more profitable for lenders.

## Financial Data Pulling 

To study this puzzling fact, we will refer to WRDS database. Wharton Research Data Services (WRDS) is a comprehensive repository of financial, economic, and insurance data. Renowned for its high-quality, reliable information, WRDS is indispensable for conducting precise financial analysis and research. Utilizing the WRDS platform, specifically through the wrds package, enables the swift and efficient extraction of large datasets. This efficiency in data collection affords researchers more time for in-depth analysis.

For this project, we have chosen to utilize multiple datasets, including:

* The **RepRisk Library**, which evaluates environmental, social, and governance (ESG) risks, as well as business conduct, using an extensive array of public sources. The incident-based data encompasses a variety of issues such as environmental impacts, labor practices, human rights, supply chain management, corruption, legal disputes, and regulatory violations.

    Additionally, this dataset features the RepRisk Index (RRI), which dynamically captures and quantifies reputational risk exposure related to ESG issues. The RepRisk Rating (RRR), ranging from AAA to D, allows for the benchmarking and integration of ESG and business conduct risks.

* The **IHS Markit library** is a leading, global financial information services company with over 15,000 employees. The company provides independent data, valuations and trade processing across all asset classes in order to enhance transparency, reduce risk and improve operational efficiency.

We have also referred to a third database:

* The **CRSP (Center for Research in Security Prices) database** offers a historical perspective on stock prices, returns, and trading volumes, alongside crucial market indicators. For this study, the CRSP database is instrumental in furnishing the missing pieces of our dataset puzzle, especially in terms of shares outstanding. By leveraging CRSP data, we can accurately compute the financial ratios critical to our analysis. 

After thorough data cleaning, analysis, and comparison of the datasets mentioned above, the project will elucidate whether a relationship exists between ESG events and securities lending activities, offering insights into the considerations of short sellers regarding ESG events in their investment strategies.

# Quick Start

To quickest way to run code in this repo is to use the following steps. First, note that you must have TexLive installed on your computer and available in your path.
You can do this by downloading and installing it from here ([windows](https://tug.org/texlive/windows.html#install) and [mac](https://tug.org/mactex/mactex-download.html) installers).
Having installed LaTeX, open a terminal and navigate to the root directory of the project and create a conda environment using the following command:
```
conda create -n project python=3.11
conda activate project
```
and then install the dependencies with pip
```
pip install -r requirements.txt
```
You can then navigate to the `src` directory and then run 
```
doit
```
# General Directory Structure

 - The `assets` folder is used for things like hand-drawn figures or other pictures that were not generated from code. These things cannot be easily recreated if they are deleted.

 - The `output` folder, on the other hand, contains tables and figures that are generated from code. The entire folder should be able to be deleted, because the code can be run again, which would again generate all of the contents.

 - I'm using the `doit` Python module as a task runner. It works like `make` and the associated `Makefile`s. To rerun the code, install `doit` (https://pydoit.org/) and execute the command `doit` from the `src` directory. Note that doit is very flexible and can be used to run code commands from the command prompt, thus making it suitable for projects that use scripts written in multiple different programming languages.

 - I'm using the `.env` file as a container for absolute paths that are private to each collaborator in the project. You can also use it for private credentials, if needed. It should not be tracked in Git.

# Data and Output Storage

I'll often use a separate folder for storing data. I usually write code that will pull the data and save it to a directory in the data folder called "pulled"  to let the reader know that anything in the "pulled" folder could hypothetically be deleted and recreated by rerunning the PyDoit command (the pulls are in the dodo.py file).

I'll usually store manually created data in the "assets" folder if the data is small enough. Because of the risk of manually data getting changed or lost, I prefer to keep it under version control if I can.

Output is stored in the "output" directory. This includes tables, charts, and rendered notebooks. When the output is small enough, I'll keep this under version control. I like this because I can keep track of how tables change as my analysis progresses, for example.

Of course, the data directory and output directory can be kept elsewhere on the machine. To make this easy, I always include the ability to customize these locations by defining the path to these directories in environment variables, which I intend to be defined in the `.env` file, though they can also simply be defined on the command line or elsewhere. The `config.py` is reponsible for loading these environment variables and doing some like preprocessing on them. The `config.py` file is the entry point for all other scripts to these definitions. That is, all code that references these variables and others are loading by importing `config`.
