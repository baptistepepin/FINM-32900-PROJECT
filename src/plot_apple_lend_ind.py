'''
This file plots apple's lending indicators and stores them in the output directory
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import config
import seaborn as sns
from compute_desc_stats import read_data

def plot_apple_lend_ind(df, data_dir=config.DATA_DIR, output_dir=config.OUTPUT_DIR):
    '''
    This function plots apple's lending indicators and stores the plot as a .png file in the output directory
    '''

    apple = df[df['cusip'] == '037833100']

    fig, ax = plt.subplots(2, 2, figsize=(15, 10))
    ax[0, 0].plot(apple['date'], apple['short interest ratio'])
    ax[0, 0].set_title('Short Interest Ratio')
    ax[0, 1].plot(apple['date'], apple['loan supply ratio'])
    ax[0, 1].set_title('Loan Supply Ratio')
    ax[1, 0].plot(apple['date'], apple['loan utilisation ratio'])
    ax[1, 0].set_title('Loan Utilisation Ratio')
    ax[1, 1].plot(apple['date'], apple['loan fee'])
    ax[1, 1].set_title('Loan Fee')
    plt.suptitle('Lending Indicators for Apple Inc.')

    file_path = Path(output_dir) / "apple_lend_ind.png"
    fig.savefig(file_path)


if __name__ == '__main__':
    df = read_data("merged_data")

    _ = plot_apple_lend_ind(df)
