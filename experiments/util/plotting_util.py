"""
Basic plotting functions
"""

from typing import Union
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd

def read_data(file) -> pd.DataFrame:
    """
    Utility function for reading csv files into pandas dataframes

    :param file: path to the csv file
    :return: df
    """
    return pd.read_csv(file)

def simple_line_plot(x: np.ndarray, y: np.ndarray, title: str ="Test", xlabel: str ="test", ylabel: str ="test",
                     file_name: str ="test.eps", xlims: Union[float, float] = None, ylims: Union[float, float] = None,
                     log: bool = False, smooth: bool = True) -> None:
    """
    Plots a line plot with a raw line and a smooth line (optionally)

    :param x: data for x-axis
    :param y: data for y-axis
    :param title: title of the plot
    :param xlabel: label of x-axis
    :param ylabel: label of y-axis
    :param file_name: name of the file to save the plot
    :param xlims: limits for the x-axis
    :param ylims: limits for the y-axis
    :param log: whether to log-scale the y-axis
    :return: None
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 3))
    if xlims is None:
        xlims = (min(x), max(x))
    if ylims is None:
        ylims = (min(y), max(y))
    ax.errorbar(x, y, yerr=None, color="red", ls='-', ecolor='black')
    if smooth:
        smooth = interp1d(x, y)
        x_smooth = np.linspace(min(x), max(x), len(x) // 10)
        ax.errorbar(x_smooth, smooth(x_smooth), yerr=None, color="black", ls='-', ecolor='black')
    ax.set_xlim(xlims)
    ax.set_ylim(ylims)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if log:
        ax.set_yscale("log")
    fig.tight_layout()
    #fig.show()
    fig.savefig(file_name, format="png")
    #fig.savefig(file_name, format='eps', dpi=500, bbox_inches='tight', transparent=True)

def read_and_plot_results(train_csv_path : str, eval_csv_path: str, train_log_frequency : int,
                 eval_frequency : int, eval_log_frequency : int, eval_episodes: int, output_dir: str, sim=False):
    eval_df = read_data(eval_csv_path)
    train_df = read_data(train_csv_path)
    plot_results(train_df["avg_attacker_episode_rewards"].values,
                 train_df["avg_defender_episode_rewards"].values,
                 train_df["avg_episode_steps"].values,
                 train_df["epsilon_values"], train_df["hack_probability"],
                 train_df["attacker_cumulative_reward"], train_df["defender_cumulative_reward"],
                 train_log_frequency, eval_frequency, eval_log_frequency, eval_episodes,
                 output_dir, eval=False, sim=sim)
    plot_results(eval_df["avg_attacker_episode_rewards"].values,
                 eval_df["avg_defender_episode_rewards"].values,
                 eval_df["avg_episode_steps"].values,
                 eval_df["epsilon_values"], eval_df["hack_probability"],
                 eval_df["attacker_cumulative_reward"], eval_df["defender_cumulative_reward"],train_log_frequency,
                 eval_frequency, eval_log_frequency, eval_episodes, output_dir, eval=True, sim=sim)

def plot_results(avg_attacker_episode_rewards: np.ndarray = None, avg_defender_episode_rewards: np.ndarray = None,
                 avg_episode_steps: np.ndarray = None,
                 epsilon_values: np.ndarray = None,
                 hack_probability: np.ndarray = None, attacker_cumulative_reward: np.ndarray = None,
                 defender_cumulative_reward: np.ndarray = None, log_frequency: int = None,
                 eval_frequency: int = None, eval_log_frequency: int = None, eval_episodes: int = None,
                 output_dir: str = None,
                 eval: bool = False, sim:bool = False) -> None:
    """
    Utility function for plotting results of an experiment in the idsgame environment

    :param avg_attacker_episode_rewards: list of average episode rewards recorded every <log_frequency> of attacker
    :param avg_defender_episode_rewards: list of average episode rewards recorded every <log_frequency> of defender
    :param avg_episode_steps:  list of average episode steps recorded every <log_frequency>
    :param epsilon_values: list of epsilon values recorded every <log_frequency>
    :param hack_probability: list of hack probabilities recorded every <log_frequency>
    :param attacker_cumulative_reward: list of attacker cumulative rewards recorded every <log_frequency>
    :param defender_cumulative_reward: list of defender cumulative rewards recorded every <log_frequency>
    :param log_frequency: frequency that the metrics were recorded
    :param eval_frequency: frequency of evaluation
    :param eval_frequency: number of evaluation episodes
    :param eval_log_frequency: log-frequency of evaluation
    :param output_dir: base directory to save the plots
    :param eval: if True save plots with "eval.png" suffix.
    :param sim: if True save plots with "sim.png" suffix.
    :return: None
    """
    step = log_frequency
    suffix = "train.png"
    if eval:
        suffix = "eval.png"
        step = eval_frequency/eval_episodes
    elif sim:
        suffix = "simulation.png"
    if avg_attacker_episode_rewards is not None:
        simple_line_plot(np.array(list(range(len(avg_attacker_episode_rewards)))) * step, avg_attacker_episode_rewards,
                         title="Avg Attacker Episodic Returns",
                         xlabel="Episode", ylabel="Avg Return",
                         file_name=output_dir + "/plots/avg_attacker_episode_returns_" + suffix)
    if avg_defender_episode_rewards is not None:
        simple_line_plot(np.array(list(range(len(avg_defender_episode_rewards)))) * step, avg_defender_episode_rewards,
                         title="Avg Defender Episodic Returns",
                         xlabel="Episode", ylabel="Avg Return",
                         file_name=output_dir + "/plots/avg_defender_episode_returns_" + suffix)
    if avg_episode_steps is not None:
        simple_line_plot(np.array(list(range(len(avg_episode_steps))))*step, avg_episode_steps,
                         title="Avg Episode Lengths",
                         xlabel="Episode", ylabel="Avg Length (num steps)",
                         file_name=output_dir + "/plots/avg_episode_lengths_" + suffix)
    if epsilon_values is not None:
        simple_line_plot(np.array(list(range(len(epsilon_values))))*step, epsilon_values,
                         title="Exploration rate (Epsilon)",
                         xlabel="Episode", ylabel="Epsilon", file_name=output_dir + "/plots/epsilon_" + suffix)
    if hack_probability is not None:
        simple_line_plot(np.array(list(range(len(hack_probability)))) * step, hack_probability,
                         title="Hack probability", ylims=(0,1),
                         xlabel="Episode", ylabel="P(Hacked)", file_name=output_dir +
                                                                         "/plots/hack_probability_" + suffix)
    if attacker_cumulative_reward is not None:
        simple_line_plot(np.array(list(range(len(attacker_cumulative_reward)))) * step, attacker_cumulative_reward,
                         title="Attacker Cumulative Reward",
                         xlabel="Episode", ylabel="Cumulative Reward",
                         file_name=output_dir + "/plots/attacker_cumulative_reward_" + suffix)
    if defender_cumulative_reward is not None:
        simple_line_plot(np.array(list(range(len(defender_cumulative_reward)))) * step,
                         defender_cumulative_reward,
                         title="Defender Cumulative Reward",
                         xlabel="Episode", ylabel="Cumulative Reward",
                         file_name=output_dir + "/plots/defender_cumulative_reward_" + suffix)

