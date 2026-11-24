import glob
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def load_results(folder):
    tables = []
    for file in glob.glob(folder + '/*.csv'):
        tables.append(pd.read_csv(file))
    results = pd.concat(tables)
    results['win'] = results['win/fail'].astype(str).str.lower() == 'true'
    results['level pack'] = results['level'].str.split('-').str[0]
    return results


def summarize(results, parameter):
    summary = results.groupby([parameter, 'ttfw']).agg(
        win_rate=('win', 'mean'),
        run_time=('run time', 'mean'),
        nodes_evaluated=('nodes evaluated', 'mean'),
        most_backtracked_nodes=('most backtracked nodes', 'mean'),
        levels=('level', 'count'),
    ).reset_index()
    summary['win_rate'] = summary['win_rate'] * 100
    summary['run_time'] = summary['run_time'] / 1000
    return summary


def draw_heatmap(summary, parameter, parameter_label, value, title, file_name, number_format):
    table = summary.pivot(index=parameter, columns='ttfw', values=value)
    plt.figure(figsize=(11, 8))
    sns.heatmap(table, annot=True, fmt=number_format, cmap='viridis')
    plt.title(title)
    plt.xlabel('timeToFinish weight')
    plt.ylabel(parameter_label)
    plt.savefig('images/' + file_name, bbox_inches='tight')
    plt.close()


def draw_all(folder, parameter, parameter_label, name):
    results = load_results(folder)
    results.to_csv('results/' + name + '-merged.csv', index=False)

    summary = summarize(results, parameter)
    summary.to_csv('results/' + name + '-summary.csv', index=False)

    draw_heatmap(summary, parameter, parameter_label, 'win_rate',
                 'Win rate [%] (' + name + ')', name + '-win-rate.png', '.1f')
    draw_heatmap(summary, parameter, parameter_label, 'run_time',
                 'Average run time per level [s] (' + name + ')', name + '-run-time.png', '.1f')
    draw_heatmap(summary, parameter, parameter_label, 'nodes_evaluated',
                 'Average nodes evaluated per level (' + name + ')', name + '-nodes-evaluated.png', '.0f')

    for pack in results['level pack'].unique():
        pack_summary = summarize(results[results['level pack'] == pack], parameter)
        draw_heatmap(pack_summary, parameter, parameter_label, 'win_rate',
                     'Win rate [%] on ' + pack + ' levels (' + name + ')', name + '-win-rate-' + pack + '.png', '.1f')


os.makedirs('images', exist_ok=True)

if os.path.exists('results/common'):
    draw_all('results/common', 'searchSteps', 'searchSteps', 'common')

if os.path.exists('results/cellsize'):
    draw_all('results/cellsize', 'cellSize', 'cell size [px]', 'cellsize')
