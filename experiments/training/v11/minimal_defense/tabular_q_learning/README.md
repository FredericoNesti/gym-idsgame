# Experiment `minimal_defense-v11`_`tabular_q_learning`

This is an experiment in the `minimal_defense-v11` environment. 
An environment where the defender is following the `defend_minimal` defense policy. 
The `defend_minimal` policy entails that the defender will always 
defend the attribute with the minimal value out of all of its neighbors.
 
This experiment trains an attacker agent using tabular q-learning to act optimally in the given
environment and defeat the defender.

The network configuration of the environment is as follows:

- `num_layers=0` (number of layers between the start and end nodes)
- `num_servers_per_layer=1`
- `num_attack_types=2`
- `max_value=2`  

<p align="center">
<img src="docs/env.png" width="600">
</p>

The starting state for each node in the environment is initialized as follows (with some randomness for where the vulnerabilities are placed).

- `defense_val=0`
- `attack_val=0`
- `num_vulnerabilities_per_node=0` (which type of defense at the node that is vulnerable is selected randomly when the environment is initialized)
- `det_val=1`
- `vulnerability_val=0` 
- `num_vulnerabilities_per_layer=0`

The environment has dense rewards (+1,-1 given whenever the attacker reaches a new level in the network)

The environment is fully observed for both the attacker and defender.

## Environment 

- Env: `minimal_defense-v11`

## Algorithm

- Tabular Q-learning with linear exploration annealing 
 
## Instructions 

To configure the experiment use the `config.json` file. Alternatively, 
it is also possible to delete the config file and edit the configuration directly in
`run.py` (this will cause the configuration to be overridden on the next run). 

Example configuration in `config.json`:

```json
{
    "attacker_type": 0,
    "defender_type": 1,
    "env_name": "idsgame-minimal_defense-v8",
    "idsgame_config": null,
    "initial_state_path": null,
    "logger": null,
    "mode": 0,
    "output_dir": "/Users/kimham/workspace/rl/gym-idsgame/experiments/training/v8/minimal_defense/tabular_q_learning",
    "py/object": "gym_idsgame.config.client_config.ClientConfig",
    "q_agent_config": {
        "alpha": 0.0005,
        "attacker": true,
        "attacker_load_path": null,
        "checkpoint_freq": 100000,
        "defender": false,
        "defender_load_path": null,
        "dqn_config": null,
        "epsilon": 1,
        "epsilon_decay": 0.9999,
        "eval_episodes": 100,
        "eval_frequency": 1000,
        "eval_log_frequency": 1,
        "eval_render": false,
        "eval_sleep": 0.9,
        "gamma": 0.99,
        "gif_dir": "/Users/kimham/workspace/rl/gym-idsgame/experiments/training/v8/minimal_defense/tabular_q_learning/results/gifs",
        "gifs": true,
        "logger": null,
        "min_epsilon": 0.01,
        "num_episodes": 20001,
        "py/object": "gym_idsgame.agents.q_learning.q_agent_config.QAgentConfig",
        "random_seed": 0,
        "render": false,
        "save_dir": "/Users/kimham/workspace/rl/gym-idsgame/experiments/training/v8/minimal_defense/tabular_q_learning/results/data",
        "train_log_frequency": 1,
        "video": true,
        "video_dir": "/Users/kimham/workspace/rl/gym-idsgame/experiments/training/v8/minimal_defense/tabular_q_learning/results/videos",
        "video_fps": 5,
        "video_frequency": 101
    },
    "random_seeds": [
        0,
        999,
        299,
        399,
        499
    ],
    "run_many": true,
    "simulation_config": null,
    "title": "TrainingQAgent vs DefendMinimalDefender"
}
```

Example configuration in `run.py`:

```python
q_agent_config = QAgentConfig(gamma=0.999, alpha=0.0005, epsilon=1, render=False, eval_sleep=0.9,
                                  min_epsilon=0.01, eval_episodes=100, train_log_frequency=1,
                                  epsilon_decay=0.9999, video=True, eval_log_frequency=1,
                                  video_fps=5, video_dir=default_output_dir() + "/results/videos", num_episodes=20001,
                                  eval_render=False, gifs=True, gif_dir=default_output_dir() + "/results/gifs",
                                  eval_frequency=1000, attacker=True, defender=False, video_frequency=101,
                                  save_dir=default_output_dir() + "/results/data")
env_name = "idsgame-minimal_defense-v11"
client_config = ClientConfig(env_name=env_name, attacker_type=AgentType.TABULAR_Q_AGENT.value,
                             mode=RunnerMode.TRAIN_ATTACKER.value,
                             q_agent_config=q_agent_config, output_dir=default_output_dir(),
                             title="TrainingQAgent vs DefendMinimalDefender",
                             run_many=True, random_seeds=[0, 999, 299, 399, 499])
```

After the experiment has finished, the results are written to the following sub-directories:

- **/data**: CSV file with metrics per episode for train and eval, e.g. `avg_episode_rewards`, `avg_episode_steps`, etc.
- **/gifs**: If the gif configuration-flag is set to true, the experiment will render the game during evaluation and save gif files to this directory. You can control the frequency of evaluation with the configuration parameter `eval_frequency` and the frequency of video/gif recording during evaluation with the parameter `video_frequency`
- **/hyperparameters**: CSV file with hyperparameters for the experiment.
- **/logs**: Log files from the experiment
- **/plots**: Basic plots of the results
- **/videos**: If the video configuration-flag is set to true, the experiment will render the game during evaluation and save video files to this directory. You can control the frequency of evaluation with the configuration parameter `eval_frequency` and the frequency of video/gif recording during evaluation with the parameter `video_frequency`
  

## Example Results

<p align="center">
<img src="docs/avg_summary.png" width="800">
</p>

### Policy Inspection

#### Evaluation after 0 Training Episodes

<p align="center">
<img src="docs/episode_0.gif" width="600">
</p> 

#### Evaluation after 15000 Training Episodes

<p align="center">
<img src="docs/episode_15000.gif" width="600">
</p>  
  

## Commands

Below is a list of commands for running the experiment

### Run

**Option 1**:
```bash
./run.sh
```

**Option 2**:
```bash
make all
```

**Option 3**:
```bash
python run.py
```

### Run Server (Without Display)

**Option 1**:
```bash
./run_server.sh
```

**Option 2**:
```bash
make run_server
```

### Clean

```bash
make clean
```

