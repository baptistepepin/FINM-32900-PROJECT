Do short sellers respond to ESG ratings?
==================

# Task List

- [ ] Create file `merge_data.py` to merge the data from the three sources
- [ ] Create file `calculate_ratios.py` to calculate the ratios from the merged data

- [ ] Create file `create_report.py` to create the final report (in LaTeX format, using the dataframes generated in the ratios file)
- [ ] Update the `dodo.py` file to include all the tasks (pulling data, merging data, calculating ratios, and creating the final report)

- [ ] Update the `requirements.txt` file that lists all the dependencies for the project
- [ ] Complete all the docstrings for the functions in the code
- [ ] Complete all the headers for the created files

- [ ] Create file `test_merge_data.py` to test the `merge_data.py` file

Should we add a specific file for cleaning the data? Or should we include this in the `merge_data.py` file?


Baptiste:
- [x] Create file `load_crsp.py` to pull data from CRSP
- [x] Create file `load_markit.py` to pull data from Markit
- [x] Create file `load_reprisk.py` to pull data from RepRisk
- [ ] Create file `merge_data.py` to merge the data RepRisk with Markit (isin or names)

Adriana:
- [ ] Complete the notebook `WRDS - Data - Demo.ipynb` and rename it, to explain the process of our project
- [ ] Update the `README.md` file that explains the project and how to run the code

Pranav:
- [ ] Create file `test_load_markit.py` to test the `load_markit.py` file
- [ ] Create file `test_load_reprisk.py` to test the `load_reprisk.py` file
- [ ] Create file `test_load_crsp.py` to test the `load_crsp.py` file

Diego:
- [ ] Create file `merge_data.py` to merge the data from Markit with CRSP

# About this project

This project amis to investigative the intricate relationship between Environmental, Social, and Governance (ESG) events and securities lending activities. Our goal is to provide a nuanced understanding of the interplay between ESG considerations and market activities, offering valuable insights into the considerations of short sellers in the context of ESG events. At the heart of our inquiry lies the pivotal question: 

$$\textbf{Is there a relationship between ESG events and securities lending activity? Do short sellers incorporate ESG events in their investment decisions?}$$

The relationship between Environmental, Social, and Governance (ESG) events and securities lending activities is a complex and multifaceted area of study within the financial market. The ESG events range from environmental disasters, social injustices, to governance failures—impact the behavior of short sellers and the broader securities lending market. 

#### Environmental Events

Environmental events can include incidents such as oil spills, deforestation, or emissions scandals. These events often lead to public backlash, regulatory scrutiny, and potentially significant financial impacts on the involved companies. Short sellers, anticipating a drop in stock prices due to these negative outcomes, may increase their activities. Consequently, the demand for borrowing shares of such companies may rise, affecting the securities lending market by increasing loan fees and utilization rates.

#### Social Events

Social events encompass issues like labor disputes, violations of human rights, and poor working conditions. These incidents can harm a company's reputation, leading to consumer boycotts or loss of investor confidence. Short sellers might view companies embroiled in social controversies as more likely to experience stock price declines, prompting an uptick in short selling activity. This dynamic can alter the supply-demand equilibrium in the securities lending market for the shares of the affected companies.

#### Governance Events

Governance events involve instances of poor management practices, corruption, executive misconduct, or lack of accountability. Such governance failures can erode investor trust and lead to financial penalties, impacting a company's stock performance. Short sellers often monitor these governance indicators as predictors of potential stock depreciation, influencing their investment strategies and, by extension, the securities lending market through variations in borrowing demand.


# Quick Start

To quickest way to run code in this repo is to use the following steps. First, note that you must have TexLive installed on your computer and available in your path.
You can do this by downloading and installing it from here ([windows](https://tug.org/texlive/windows.html#install) and [mac](https://tug.org/mactex/mactex-download.html) installers).
Having installed LaTeX, open a terminal and navigate to the root directory of the project and create a conda environment using the following command:
```
conda create -n project python=3.12
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


# Dependencies and Virtual Environments

## Working with `pip` requirements

`conda` allows for a lot of flexibility, but can often be slow. `pip`, however, is fast for what it does.  You can install the requirements for this project using the `requirements.txt` file specified here. Do this with the following command:
```
pip install -r requirements.txt
```

The requirements file can be created like this:
```
pip list --format=freeze
```

## Working with `conda` environments

The dependencies used in this environment (along with many other environments commonly used in data science) are stored in the conda environment called `blank` which is saved in the file called `environment.yml`. To create the environment from the file (as a prerequisite to loading the environment), use the following command:

```
conda env create -f environment.yml
```

Now, to load the environment, use

```
conda activate blank
```

Note that an environment file can be created with the following command:

```
conda env export > environment.yml
```

However, it's often preferable to create an environment file manually, as was done with the file in this project.

Also, these dependencies are also saved in `requirements.txt` for those that would rather use pip. Also, GitHub actions work better with pip, so it's nice to also have the dependencies listed here. This file is created with the following command:

```
pip freeze > requirements.txt
```

### Alternative Quickstart using Conda
Another way to  run code in this repo is to use the following steps.
First, open a terminal and navigate to the root directory of the project and create a conda environment using the following command:
```
conda env create -f environment.yml
```
Now, load the environment with
```
conda activate blank
```
Now, navigate to the directory called `src`
and run
```
doit
```
That should be it!



**Other helpful `conda` commands**

- Create conda environment from file: `conda env create -f environment.yml`
- Activate environment for this project: `conda activate blank`
- Remove conda environment: `conda remove --name myenv --all`
- Create blank conda environment: `conda create --name myenv --no-default-packages`
- Create blank conda environment with different version of Python: `conda create --name myenv --no-default-packages python` Note that the addition of "python" will install the most up-to-date version of Python. Without this, it may use the system version of Python, which will likely have some packages installed already.

## `mamba` and `conda` performance issues

Since `conda` has so many performance issues, it's recommended to use `mamba` instead. I recommend installing the `miniforge` distribution. See here: https://github.com/conda-forge/miniforge
