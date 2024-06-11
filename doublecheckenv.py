from aiTikTakToeEnv import EnvironmentCliTikTakToe

env = EnvironmentCliTikTakToe()
episodes = 100

for episode in range(episodes):
    done = False
    obs = env.reset()
    print('obs', obs)
    while not done: #not done:
        random_action = env.action_space.sample()
        print('action', random_action)
        obs, reward, info, = env.step(random_action)
        print('reward', reward)
        print('obs', obs)
        if reward == 1 or reward ==-10 or reward == 20:
            done = True
