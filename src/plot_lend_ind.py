'''
This file plots apple's lending indicators and stores them in the output directory
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path
import config
import seaborn as sns
from compute_desc_stats import read_data
mpl.rcParams['font.family'] = 'Times New Roman'

cusip_list = ['037833100', '36467W109', ]
name_list = ['Apple Inc', 'GameStop Corp']

def plot_lend_ind(df, cusip_list, name_list, output_dir=config.OUTPUT_DIR):
    '''
    This function plots apple's lending indicators and stores the plot as a .png file in the output directory
    '''
    
    for cusip, name in zip(cusip_list, name_list):

        selected_stock = df[df['cusip'] == cusip]

        fig, ax = plt.subplots(2, 2, figsize=(15, 10))

        ax[0, 0].plot(selected_stock['date'], selected_stock['short interest ratio'], linewidth=1)
        ax[0, 0].set_title('Short Interest Ratio')
        ax[0, 0].tick_params(axis='x', rotation=45)

        ax[0, 1].plot(selected_stock['date'], selected_stock['loan supply ratio'], linewidth=1)
        ax[0, 1].set_title('Loan Supply Ratio')
        ax[0, 1].tick_params(axis='x', rotation=45)

        ax[1, 0].plot(selected_stock['date'], selected_stock['loan utilisation ratio'], linewidth=1)
        ax[1, 0].set_title('Loan Utilisation Ratio')
        ax[1, 0].tick_params(axis='x', rotation=45)

        ax[1, 1].plot(selected_stock['date'], selected_stock['loan fee'], linewidth=1)
        ax[1, 1].set_title('Loan Fee')
        ax[1, 1].tick_params(axis='x', rotation=45)

        plt.tight_layout()

        file_path = Path(output_dir) / f"{name}_lend_ind.png"
        fig.savefig(file_path)


if __name__ == '__main__':
    df = read_data("merged_data")

    _ = plot_lend_ind(df, cusip_list, name_list)
