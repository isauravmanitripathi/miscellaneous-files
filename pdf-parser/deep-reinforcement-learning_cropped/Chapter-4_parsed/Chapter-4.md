# *Learning to pick the best policy: Policy gradient methods*

# *This chapter covers*

- **Implementing the policy function as a neural** network
- **Introducing the OpenAI Gym API**
- **Applying the REINFORCE algorithm on the OpenAI** CartPole problem

In the previous chapter we discussed deep Q-networks, an off-policy algorithm that approximates the Q function with a neural network. The output of the Q-network was Q values corresponding to each action for a given state (figure 4.1); recall that the Q value is the expected (weighted average) of rewards.

![](_page_0_Figure_6.jpeg)

Figure 4.1 A Q-network takes a state and returns Q values (action values) for each action. We can use those action values to decide which actions to take.

Given these predicted Q values from the Q-network, we can use some strategy to select actions to perform. The strategy we employed in the last chapter was the epsilon-greedy approach, where we selected an action at random with probability  $\varepsilon$ , and with probability  $1 - \varepsilon$  we selected the action associated with the highest Q value (the action the Q-network predicts is the best, given its experience so far). There are any number of other policies we could have followed, such as using a softmax layer on the Q values.

 What if we skip selecting a policy on top of the DQN and instead train a neural network to output an action directly? If we do that, our neural network ends up being a *policy function*, or a *policy network*. Remember from chapter 3 that a policy function,  $\pi$ *. State*  $\rightarrow$  *P*(*Action State*), accepts a state and returns the best action. More precisely, it will return a probability distribution over the actions, and we can sample from this distribution to select actions. If a probability distribution is an unfamiliar concept to you, don't worry. We'll discuss it more in this chapter and throughout the book.

# *4.1 Policy function using neural networks*

In this chapter we'll introduce a class of algorithms that allow us to approximate the policy function,  $\pi(s)$ , instead of the value function,  $V_{\pi}$  or *Q*. That is, instead of training a network that outputs action values, we will train a network to output (the probability of) actions.

#### *4.1.1 Neural network as the policy function*

In contrast to a Q-network, a policy network tells us exactly what to do given the state we're in. No further decisions are necessary. All we need to do is randomly sample from the probability distribution  $P(A|S)$ , and we get an action to take (figure 4.2). The actions that are most likely to be beneficial will have the highest chance of being selected from random sampling, since they are assigned the highest probability.

![](_page_1_Figure_7.jpeg)

Figure 4.2 A policy network is a function that takes a state and returns a probability distribution over the possible actions.

Imagine the probability distribution  $P(A|S)$  as a jar filled with little notes with an action written on each. In a game with four possible actions, there will be notes with labels 1–4 (or 0–3 if they're indices in Python). If our policy network predicts that action 2 is the most likely to result in the highest reward, it will fill this jar with a lot of little notes labeled 2, and fewer notes labeled 1, 3, and 4. In order to select an action then, all we do is close our eyes and grab a random note from the jar. We're most likely to choose action 2, but sometimes we'll grab another action, and that gives us the opportunity to explore. Using this analogy, every time the state of the environment

changes, we give the state to our policy network, and it uses that to fill the jar with a new set of labeled notes representing the actions in different proportions. Then we randomly pick from the jar.

 This class of algorithms is called *policy gradient methods,* and it has a few important differences from the DQN algorithm; we'll explore these differences in this chapter. Policy gradient methods offer a few advantages over value prediction methods like DQN. One is that, as we already discussed, we no longer have to worry about devising an action-selection strategy like epsilon-greedy; instead, we directly sample actions from the policy. Remember, we spent a lot of time cooking up methods to improve the stability of training our DQN—we had to use experience replay and target networks, and there are a number of other methods in the academic literature that we could have used. A policy network tends to simplify some of that complexity.

#### *4.1.2 Stochastic policy gradient*

There are many different flavors of policy gradient methods. We will start with the *stochastic policy gradient* method (figure 4.3), which is what we just described. With a stochastic policy gradient, the output of our neural network is an action vector that represents a probability distribution.

![](_page_2_Figure_5.jpeg)

Figure 4.3 A stochastic policy function. A policy function accepts a state and returns a probability distribution over actions. It is *stochastic* because it returns a probability distribution over actions rather than returning a deterministic, single action.

The policy we'll follow is selecting an action from this probability distribution. This means that if our agent ends up in the same state twice, we may not end up taking the same action every time. In figure 4.3 we feed our function the state, which is (1,2), and the output is a vector of probabilities corresponding to each action. If this was a Gridworld agent, for example, the agent would have a 0.50 probability of going up, no chance of going down, a 0.25 probability of going left, and a 0.25 probability of going right.

 If the environment is stationary, which is when the distribution of states and rewards is constant, and we use a deterministic strategy, we'd expect the probability distribution to eventually converge to a *degenerate probability distribution*, as shown in figure 4.4. A degenerate probability distribution is a distribution in which all the probability mass is assigned to a single potential outcome. When dealing with discrete probability distributions as we do in this book, all the probabilities must sum to 1, so a

![](_page_3_Figure_1.jpeg)

Figure 4.4 A deterministic policy function, often represented by the Greek character pi, takes a state and returns a specific action to take, unlike a stochastic policy, which returns a probability distribution over actions.

degenerate distribution is one where all outcomes are assigned 0 probability except for one, which is assigned 1.

 Early in training we want the distribution to be fairly uniform so that we can maximize exploration, but over the course of training we want the distribution to converge on the optimal actions, given a state. If there is only one optimal action for a state, we'd expect to converge toward a degenerate distribution, but if there are two equally good actions, then we would expect the distribution to have two *modes*. A mode of a probability distribution is just another word for a "peak."

#### I forget … What's a probability distribution?

In Gridworld, we had four possible actions: up, down, left, and right. We call this our action set or actions-space, since we can describe it mathematically as a set, e.g., *A* = {*up,down,left,right*} where the curly braces indicate a set. (A set in mathematics is just an abstract unordered collection of things with certain operations defined.) So what does it mean to apply a probability distribution over this set of actions?

Probability is actually a very rich and even controversial topic in its own right. There are varying philosophical opinions on exactly what *probability* means. To some people, the probability means that, if you were to flip a coin a very large number of times (ideally an infinite number of times, mathematically speaking) the probability of a fair coin turning up heads is equal to the proportion of heads in that infinitely long sequence of flips. That is, if we flip a fair coin 1,000,000 times, we would expect about half of the flips to be heads and the other half tails, so the probability is equal to that proportion. This is a frequentist interpretation of probability, since probability is interpreted as the long-term frequency of some event repeated many times.

Another school of thought interprets probability only as a degree of belief, a subjective assessment of how much someone can predict an event given the knowledge they currently possess. This degree of belief is often called a *credence*. The probability of a fair coin turning up heads is 0.5 or 50% because, given what we know about the coin, we don't have any reason to predict heads more than tails, or tails more than heads, so we split our belief evenly across the two possible outcomes. Hence, anything that we can't predict deterministically (i.e., with probability 0 or 1, and nothing in between) results from a lack of knowledge.

#### *(continued)*

You're free to interpret probabilities however you want, since it won't affect our calculations, but in this book we tend to implicitly use the credence interpretation of probability. For our purposes, applying a probability distribution over the set of actions in Gridworld, *A* = {*up,down,left,right*} means we're assigning a degree of belief (a real number between 0 and 1) to each action in the set such that all the probabilities sum to 1. We interpret these probabilities as the probability that an action is the best action to maximize the expected rewards, given that we're in a certain state.

Concretely, a probability distribution over our action set *A* is denoted  $P(A): A_i \rightarrow [0,1]$ , meaning that *P*(*A*) is a map from a set *A* to a set of real numbers between 0 and 1. In particular, each element  $a_i \in A$  is mapped to a single number between 0 and 1 such that the sum of all these numbers for each action is equal to 1. We might represent this map for our Gridworld action set as just a vector, where we identify each position in the vector with an element in the action set, e.g., [up, down, left, right]  $\rightarrow$ [0.25, 0.25, 0.10, 0.4]. This map is called a *probability mass function* (PMF).

What we just described is actually a *discrete* probability distribution, since our action set was discrete (a finite number of elements). If our action set was infinite, i.e., a continuous variable like velocity, we would call this a *continuous* probability distribution and instead we would need to define a *probability density function* (PDF).

The most common example of a PDF is the normal (also known as Gaussian, or just bell-curve) distribution. If we have a probability with a continuous action, say a car game where we need to control the velocity of the car from 0 to some maximum value, which is a continuous variable, how might we do this with a policy network? Well, we could drop the idea of probability distribution and just train the network to produce the single value of velocity that it predicts is best, but then we'd risk not exploring enough (and it is difficult to train such a network). A lot of power comes from a little bit of randomness. The kind of neural networks we employ in this book only produce vectors (or tensors more generally) as output, so they can't produce a continuous probability distribution—we have to be more clever. A PDF like a normal distribution is defined by two parameters, the mean and variance. Once we have those, we have a normal distribution that we can sample from. So we can just train a neural network to produce mean and standard deviation values that we can then plug into the normal distribution equation and sample from that.

Don't worry if this isn't all making sense now. We will continue to go over it again and again because these concepts are ubiquitous in reinforcement learning and machine learning more broadly.

# *4.1.3 Exploration*

Recall from the previous chapter that we needed our policy to include some randomness, which would allow us to visit new states during training. For DQNs we followed the epsilon-greedy policy, where there was a chance we would not follow the action that led to the greatest predicted reward. If we always selected the action that led to the maximum predicted reward, we'd never discover the even better actions and states available to us. For the stochastic policy gradient method, because our output is

a probability distribution, there should be a small chance that we explore all spaces; only after sufficient exploration will the action distribution converge to producing the single best action, a degenerate distribution. Or if the environment itself has some randomness, the probability distribution will retain some probability mass to each action. When we initialize our model in the beginning, the probability of our agent picking each action should be approximately equal or uniform, since the model has zero information about which action is better.

 There is a variant of policy gradient called *deterministic policy gradient* (DPG) where there is a single output that the agent will always follow (as illustrated in figure 4.4). In the case of Gridworld, for example, it would produce a 4-dimensional binary vector with a 1 for the action to be taken and 0s for the other actions. The agent won't explore properly if it always follows the output because there's no randomness in the action selection. Since the output of a deterministic policy function for a discrete action set would be discrete values, it is also difficult to get this working in the fully differentiable manner that we are accustomed to with deep learning, so we'll focus on stochastic policy gradients. Building a notion of uncertainty into the models (e.g., using probability distributions) is generally a good thing.

# *4.2 Reinforcing good actions: The policy gradient algorithm*

From the previous section, you understand that there is a class of algorithms that attempts to create a function that outputs a probability distribution over actions, and that this policy function  $\pi(s)$  can be implemented with a neural network. In this section we'll delve into how to actually implement these algorithms and train (i.e., optimize) them.

# *4.2.1 Defining an objective*

Recall that neural networks need an objective function that is differentiable with respect to the network weights (parameters). In the last chapter we trained the deep Q-network with a minimizing mean squared error (MSE) loss function with respect to its predicted Q values and the target Q value. We had a nice formula for calculating the target Q value based on the observed reward, since Q values are just averaged rewards (i.e., expectations), so this was not much different from how we would normally train a supervised deep learning algorithm.

 How do we train a policy network that gives us a probability distribution over actions given a state,  $P(A|S)$ ? There's no obvious way to map our observed rewards after taking an action to updating  $P(A|S)$ . Training the DQN was not much different from solving a supervised learning problem because our Q-network generated a vector of predicted Q values, and by using a formula we were able to generate the target Q value vector. Then we just minimized the error between the Q-network's output vector and our target vector.

 With a policy network, we're predicting actions directly, and there is no way to come up with a target vector of actions we should have taken instead, given the rewards. All we

know is whether the action led to positive or negative rewards. In fact, what the best action is secretly depends on a value function, but with a policy network we're trying to avoid computing these action values directly.

 Let's go through an example to see how we might optimize our policy network. We'll start with some notation. Our policy network is denoted  $\pi$  and is parameterized by a vector  $\theta$ , which represents all of the parameters (weights) of the neural network. As you know, neural networks have parameters in the form of multiple weight matrices, but for the purposes of easy notation and discussion, it is standard to consider all the network parameters together as a single long vector that we denote  $\theta$  (theta).

Whenever we run the policy network forward, the parameter vector  $\theta$  is fixed; the variable is the data that gets fed into the policy network (i.e., the state). Hence, we denote the parameterized policy as  $\pi_{\theta}$ . Whenever we want to indicate that some input to a function is fixed, we will include it as a subscript rather than as an explicit input like  $\pi(x,\theta)$  where *x* is some input data (i.e., the state of the game). Notations like  $\pi(x,\theta)$ suggest  $\theta$  is a variable that changes along with *x*, whereas  $\pi_{\theta}$  indicates that  $\theta$  is a fixed parameter of the function.

Let's say we give our initially untrained policy network  $\pi_{\theta}$  some initial game state for Gridworld, denoted *s*, and run it forward by computing  $\pi_{\theta}(s)$ . It returns a probability distribution over the four possible actions, such as [0.25, 0.25, 0.25, 0.25]. We sample from this distribution, and since it's a uniform distribution, we end up taking a random action (figure 4.5). We continue to take actions by sampling from the produced action distribution until we reach the end of the episode.

![](_page_6_Figure_5.jpeg)

Figure 4.5 The general overview of policy gradients for an environment with four possible discrete actions. First we input the state to the policy network, which produces a probability distribution over the actions, and then we sample from this distribution to take an action, which produces a new state.

Remember, some games like Gridworld are episodic, meaning that there is a welldefined start and end point to an episode of the game. In Gridworld, we start the game in some initial state and play until we either hit the pit, land on the goal, or take too many moves. So an episode is a sequence of states, actions, and rewards from an initial state to the terminal state where we win or lose the game. We denote this episode as

$$
\pmb{\epsilon} = (S_0, A_0, R_1), (S_1, A_1, R_2) \dots (S_{t-1}, A_{t-1}, R_t)
$$
Each tuple is one time-step of the Gridworld game (or a Markov decision process, more generally). After we've reached the end of the episode at time *t*, we've collected a bunch of historical data on what just happened. Let's say that by chance we hit the goal after just three moves determined by our policy network. Here's what our episode looks like:

$$
\pmb{\epsilon}=(S_0,\!3,\!-\!1), (S_1,\!1,\!-\!1), (S_2,\!3,\!+\!10)
$$

We've encoded the actions as integers from 0 to 3 (referring to array indices of the action vector) and we've left the states denoted symbolically since they're actually 64 length vectors. What is there to learn from in this episode? Well, we won the game, indicated by the +10 reward in the last tuple, so our actions must have been "good" to some degree. Given the states we were in, we should encourage our policy network to make those actions more likely next time. We want to reinforce those actions that led to a nice positive reward. We will address what happens when our agent loses (receives a terminal reward of –10) later in this section, but in the meantime we will focus on positive reinforcement.

### *4.2.2 Action reinforcement*

We want to make small, smooth updates to our gradients to encourage the network to assign more probability to these winning actions in the future. Let's focus on the last experience in the episode, with state  $S_2$ . Remember, we're assuming our policy network produced the action probability distribution [0.25, 0.25, 0.25, 0.25], since it was untrained, and in the last time step we took action 3 (corresponding to element 4 in the action probability array), which resulted in us winning the game with a  $+10$ reward. We want to positively reinforce this action, given state  $S_2$ , such that whenever the policy network encounters  $S_2$  or a very similar state, it will be more confident in predicting action 3 as the highest probability action to take.

 A naive approach might be to make a target action distribution, [0, 0, 0, 1], so that our gradient descent will move the probabilities from [0.25, 0.25, 0.25, 0.25] close to  $[0, 0, 0, 1]$ , maybe ending up as  $[0.167, 0.167, 0.167, 0.5]$  (see figure 4.6). This is something we often do in the supervised learning realm, when we are training a softmax-based image classifier. But in that case, there is a single correct classification for an image, and there is no temporal association between each prediction. In our RL case, we want more control over how we make these updates. First, we want to make small, smooth updates because we want to maintain some stochasticity in our action sampling to adequately explore the environment. Second, we want to be able to weight how much we assign credit to each action for earlier actions. Let's review some more notation before diving into these two problems.

Recall that our policy network is typically denoted  $\pi_{\theta}$  when we are running it forward (i.e., using it to produce action probabilities), because we think of the network parameters,  $\theta$ , as being fixed and the input state is what varies. Hence, calling  $\pi_{\theta}(s)$  for some state *s* will return a probability distribution over the possible actions, given a

![](0__page_8_Figure_1.jpeg)

Figure 4.6 Once an action is sampled from the policy network's probability distribution, it produces a new state and reward. The reward signal is used to reinforce the action that was taken, that is, it increases the probability of that action given the state if the reward is positive, or it decreases the probability if the reward is negative. Notice that we only received information about action 3 (element 4), but since the probabilities must sum to 1, we have to lower the probabilities of the other actions.

fixed set of parameters. When we are training the policy network, we need to vary the parameters with respect to a fixed input to find a set of parameters that optimizes our objective (i.e., minimizes a loss or maximizes a utility function), which is the function  $\pi_{s}(\theta)$ .

DEFINITION The probability of an action, given the parameters of the policy network, is denoted  $\pi_s(a|\theta)$ . This makes it clear that the probability of an action, *a*, explicitly depends on the parameterization of the policy network. In general, we denote a *conditional probability* as *P*(*x* | *y*), read "the probability distribution over *x* given *y*." This means we have some function that takes a parameter *y* and returns a probability distribution over some other parameter *x*.

In order to reinforce action 3, we want to modify our policy network parameters  $\theta$ such that we increase  $\pi_s(a_3|\theta)$ . Our objective function merely needs to maximize  $\pi_s(a_3|\theta)$  where  $a_3$  is action 3 in our example. Before training,  $\pi_s(a_3|\theta) = 0.25$ , but we want to modify  $\theta$  such that  $\pi_s(a_3 | \theta) > 0.25$ . Because all of our probabilities must sum to 1, maximizing  $\pi_s(a_3|\theta)$  will minimize the other action probabilities. And remember, we prefer to set things up so that we're minimizing an objective function instead of maximizing, since it plays nicely with PyTorch's built-in optimizers—we should instead tell PyTorch to minimize  $1 - \pi_s(a|\theta)$ . This loss function approaches 0 as  $\pi_s(a|\theta)$ nears 1, so we are encouraging the gradients to maximize  $\pi_s(a|\theta)$  for the action we took. We will subsequently drop the subscript  $a_3$ , as it should be clear from the context which action we're referring to.

## *4.2.3 Log probability*

Mathematically, what we've described is correct. But due to computation imprecisions we need to make adjustments to this formula to stabilize the training. One problem is that probabilities are bounded by 0 and 1 by definition, so the range of values that the

optimizer can operate over is limited and small. Sometimes probabilities may be extremely tiny or very close to 1, and this runs into numerical issues when optimizing on a computer with limited numerical precision. If we instead use a surrogate objective, namely  $-\log \pi_s(a|\theta)$  (where log is the natural logarithm), we have an objective that has a larger "dynamic range" than raw probability space, since the log of probability space ranges from  $(-\infty,0)$ , and this makes the log probability easier to compute. Moreover, logarithms have the nice property that  $log(a \cdot b) = log(a) + log(b)$ , which means when we multiply log probabilities, we can turn this multiplication into a sum, which is also more numerically stable than multiplication. If we set our objective as  $-\log \pi_s(a|\theta)$  instead of  $1 - \pi_s(a|\theta)$ , our loss still abides by the intuition that the loss function approaches 0 as  $\pi_s(a|\theta)$  approaches 1. Our gradients will be tuned to try to increase  $\pi_s(a|\theta)$  to 1, where  $a$  = action 3, for our running example.

#### *4.2.4 Credit assignment*

Our objective function is  $-\log \pi_s(a|\theta)$ , but this assigns equal weight to every action in our episode. The weights in the network that produced the last action will be updated to the same degree as the first action. Why shouldn't that be the case? Well, it makes sense that the last action right before the reward deserves more credit for winning the game than does the first action in the episode. For all we know, the first action was actually sub-optimal, but then we later made a comeback and hit the goal. In other words, our confidence in how "good" each action is diminishes the further we are from the point of reward. In a game of chess, we attribute more credit to the last move made than the first one. We're very confident that the move that directly led to us to winning was a good move, but we become less confident the further back we go. How much did the move five time steps ago contribute to winning? We're not so sure. This is the problem of *credit assignment*.

 We express this uncertainty by multiplying the magnitude of the update by the discount factor, which you learned in chapter 3 ranges from 0 to 1. The action right before the episode ends will have a discount factor of 1, meaning it will receive the full gradient update, while earlier moves will be discounted by a fraction such as 0.5 so the gradient steps will be smaller.

 Let's add those into our objective (loss) function. The final objective function that we will tell PyTorch to minimize is  $-\gamma_t * G_t * \log \pi_s(a|\theta)$ . Remember,  $\gamma_t$  is the discount factor, and the subscript *t* tells us its value will depend on the time step *t*, since we want to discount more distant actions more than more recent ones. The parameter  $G_t$  is called the *total return*, or *future return*, at time step *t*. It is the return we expect to collect from time step *t* until the end of the episode, and it can be approximated by adding the rewards from some state in the episode until the end of the episode.

$$
G_t = r_t + r_{t+1} \dots + r_{T-1} + r_T
$$

Actions temporally more distant from the received reward should be weighted less than actions closer. If we win a game of Gridworld, the sequence of discounted rewards

from the start to the terminal state might look something like [0.970, 0.980, 0.99, 1.0]. The last action led to the winning state of +1, and it is not discounted at all. The previous action is assigned a scaled reward by multiplying the terminal reward with the  $\gamma_{-1}$ discount factor, which we've set to 0.99.

The discount is exponentially decayed from 1,  $\gamma_t = \gamma_0^{(T-t)}$ , meaning that the discount at time *t* is calculated as the starting discount (here 0.99) exponentiated to the integer time distance from the reward. The length of the episode (the total number of time steps) is denoted *T*, and the local time step for a particular action is *t*. For  $T - t = 0$ ,  $\gamma_{T-0} = 0.99^0 = 1$ . For  $T - t = 2$ , the  $\gamma_{T-2} = 0.99^2 = 0.9801$ , and so on. Each time step back, the discount factor is exponentiated to the distance from the terminal step, which results in an exponential decay of the discount factor the more distant (and irrelevant) the action was to the reward outcome.

For example, if the agent is in state  $S_0$  (i.e., time step  $t = 0$ ) and it takes action  $a_1$  and receives reward  $t_{t+1} = -1$ , the target update will be  $-\gamma^0(-1) \log \pi(a_1 | \theta, S_0) = \log \pi(a_1 | \theta, S_0)$ , which is the log-probability output from the policy network (see figure 4.7).

![](0__page_10_Figure_4.jpeg)

Figure 4.7 A string diagram for training a policy network for Gridworld. The policy network is a neural network parameterized by  $\theta$  (the weights) that accepts a 64-dimensional vector for an input state. It produces a discrete 4-dimensional probability distribution over the actions. The sample action box samples an action from the distribution and produces an integer as the action, which is given to the environment (to produce a new state and reward) and to the loss function so we can reinforce that action. The reward signal is also fed into the loss function, which we attempt to minimize with respect to the policy network parameters.

# *4.3 Working with OpenAI Gym*

To illustrate how policy gradients work, we've been using Gridworld as an example, since it is already familiar to you from last chapter. However, we should use a different problem to actually implement the policy gradient algorithm, both for variety and also to introduce the OpenAI Gym.

 The OpenAI Gym is an open source suite of environments with a common API that is perfect for testing reinforcement learning algorithms. If you come up with

![](0__page_11_Picture_1.jpeg)

Figure 4.8 Two example environments provided by OpenAI's Gym environment. The OpenAI Gym provides hundreds of environments to test your reinforcement learning algorithms on.

some new DRL algorithm, testing it on a few of the environments in the Gym is a great way to get some idea of how well it performs. The Gym contains a variety of environments from easy ones can be "solved" by simple linear regression all the way through to ones that all but require a sophisticated DRL approach (see figure 4.8). There are games, robotic control, and other types of environments. There's probably something in there you'll be interested in.

 OpenAI lists all of its currently supported environments on its website: [https://gym](https://gym.openai.com/envs/) [.openai.com/envs/.](https://gym.openai.com/envs/) At the time of writing, they are broken down into seven categories:

- Algorithms
- Atari
- Box2D
- Classic control
- $\blacksquare$  MuJoCo
- Robotics
- Toy text

You can also view the entire list of environments from the OpenAI registry in your Python shell with the following code.

```
Listing 4.1 Listing the OpenAI Gym environments
```

```
from gym import envs
envs.registry.all()
```

There are hundreds of environments to choose from (797 in v0.9.6). Unfortunately, some of these environments require licenses (MuJoCo) or external dependencies (Box2D, Atari) and will therefore require a bit of setup time. We will be starting with a simple example, CartPole (figure 4.9), to avoid any unnecessary complications and to get us coding right away.

![](0__page_12_Figure_2.jpeg)

![](0__page_12_Figure_3.jpeg)

### *4.3.1 CartPole*

The CartPole environment falls under OpenAI's Classic Control section, and it has a very simple objective—don't let the pole fall over. It's the game equivalent of trying to balance a pencil on the tip of your finger. In order to balance the pole successfully, you have to apply just the right amount of small left and right movements to the cart. In this environment, there are only two actions that correspond to making a small push left or right.

 In the OpenAI Gym API, environments with discrete action spaces all have actions represented as integers from 0 to the total number of actions for the particular environment, so in CartPole the possible actions are 0 and 1, which denote a push to the left or to the right. The state is represented as a vector of length 4 that indicates the cart position, cart velocity, pole angle, and pole velocity. We receive a reward of +1 for every step the pole has not fallen over, which happens when the pole angle is more than 12° from the center or when the cart position is outside the window. Hence, the goal of CartPole is to maximize the length of the episode, since each step returns a positive +1 reward. More information can be found on the OpenAI Gym GitHub page ([https://github.com/openai/gym/wiki/CartPole-v0\)](https://github.com/openai/gym/wiki/CartPole-v0). Note that not every subsequent problem has a nice specification page like CartPole does, but we will define the scope of the problem beforehand in all subsequent chapters.

## *4.3.2 The OpenAI Gym API*

The OpenAI Gym has been built to be incredibly easy to use, and there are less than half a dozen methods that you'll routinely use. You already saw one in listing 4.1 where we listed all the available environments. Another important method is creating an environment.

```
import gym
env = gym.make('CartPole-v0')
  Listing 4.2 Creating an environment in OpenAI Gym
```

From now on, we will be interacting solely with this env variable. We need a way to observe the current state of the environment and then to interact with it. There are only two methods you need to do this.

```
Listing 4.3 Taking an action in CartPole
```

```
state1 = env.reset()
action = env.action_space.sample()
state, reward, done, info = env.step(action)
```

The reset method initializes the environment and returns the first state. For this example, we used the sample method of the env. action space object to sample a random action. Soon enough, we'll sample actions from a trained policy network that will act as our reinforcement learning agent.

 Once we initialize the environment, we are free to interact with it via the step method. The step method returns four important variables that our training loop needs access to in order to run. The first parameter, state, represents the next state after we take the action. The second parameter, reward, is the reward at that time step, which for our CartPole problem is 1 unless the pole has fallen down. The third parameter, done, is a Boolean that indicates whether or not a terminal state has been reached. For our CartPole problem, this would always return false until the pole has fallen or the cart has moved outside the window. The last parameter, info, is a dictionary with diagnostic information that may be useful for debugging, but we will not use it. That's all you need to know to get most environments up and running in OpenAI Gym.

## *4.4 The REINFORCE algorithm*

Now that you how to create an OpenAI Gym environment and have hopefully developed an intuition for the policy gradient algorithm, let's dive in to getting a working implementation. Our discussion of policy gradients in the previous section focused on a particular algorithm that has been around for decades (like most of deep learning and reinforcement learning) called REINFORCE (yes, it's always fully capitalized). We're going to consolidate what we discussed previously, formalize it, and
then turn it into Python code. Let's implement the REINFORCE algorithm for the CartPole example.

# *4.4.1 Creating the policy network*

We will build and initialize a neural network that serves as a policy network. The policy network will accept state vectors as inputs, and it will produce a (discrete) probability distribution over the possible actions. You can think of the agent as a thin wrapper around the policy network that samples from the probability distribution to take an action. Remember, an agent in reinforcement learning is whatever function or algorithm takes a state and returns a concrete action that will be executed in the environment.

Let's express this in code.

```
import gym
import numpy as np
import torch
11 = 412 = 15013 = 2model = torch.nn.Sequential(
     torch.nn.Linear(l1, l2),
     torch.nn.LeakyReLU(),
     torch.nn.Linear(l2, l3),
     torch.nn.Softmax() 
)
learning rate = 0.0009optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
   Listing 4.4 Setting up the policy network
                        The input data is length 4 
                        ("l1" is short for layer 1)
                          The middle layer produces 
                          a vector of length 150
                                     The output is a 2-length 
                                     vector for the left and 
                                    right actions
                                      The output is a softmax 
                                     probability distribution 
                                       over actions
```

That should all look fairly familiar to you at this point. The model is only two layers: a leaky ReLU activation function for the first layer, and the Softmax function for the last layer. We chose the leaky ReLU because it performed better empirically. You saw the Softmax function back in chapter 2; it just takes an array of numbers and squishes them into the range of 0 to 1 and makes sure they all sum to 1, basically creating a discrete probability distribution out of any list of numbers that are not probabilities to start with. For example,  $softmax([-1,2,3]) = [0.0132, 0.2654, 0.7214]$ . Unsurprisingly, the Softmax function will turn the bigger numbers into larger probabilities.

## *4.4.2 Having the agent interact with the environment*

The agent consumes the state and takes an action, *a*, probabilistically. More specifically, the state is input to the policy network, which then produces the probability distribution over the actions  $P(A | \theta, S_t)$  given its current parameters and the state. Note, the capital *A* refers to the set of all possible actions given the state, whereas the lowercase *a* generally refers to a particular action.

 The policy network might return a discrete probability distribution in the form of a vector, such as [0.25, 0.75] for our two possible actions in CartPole. This means the policy network predicts that action 0 is the best with 25% probability, and action 1 is the best with 75% probability (or confidence). We call this array pred.

| Listing 4.5 Using the policy network to sample an action                                                                                                                          |  |  |  |  |  |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|--|--|--|--|
| Samples an action from the probability<br>Calls the policy network model to<br>distribution produced by the policy network<br>produce predicted action probabilities              |  |  |  |  |  |
| $\rightarrow$ pred = model(torch.from numpy(state1).float())<br>$action = np.random.chole(np.array([0,1]), p=pred.data.numpy())$<br>state2, reward, done, info = env.step(action) |  |  |  |  |  |
| Takes the action and receives the new state and reward. The info<br>variable is produced by the environment but is irrelevant.                                                    |  |  |  |  |  |

The environment responds to the action by producing a new state,  $s<sub>2</sub>$ , and a reward, *r*2. We store those into two arrays (a states array and an actions array) for when we need to update our model after the episode ends. We then plug the new state into our model, get a new state and reward, store those, and repeat until the episode ends (the pole falls over and the game is finished).

# *4.4.3 Training the model*

We train the policy network by updating the parameters to minimize the objective (i.e., loss) function. This involves three steps:

- <sup>1</sup> Calculate the probability of the action actually taken at each time step.
- 2 Multiply the probability by the discounted return (the sum of rewards).
- <sup>3</sup> Use this probability-weighted return to backpropagate and minimize the loss.

We'll look at these in turn.

### CALCULATING THE PROBABILITY OF THE ACTION

Calculating the probability of the action taken is easy enough. We can use the stored past transitions to recompute the probability distributions using the policy network, but this time we extract just the predicted probability for the action that was actually taken. We'll denote this quantity  $P(a_t | \theta, s_i)$ ; this is a single probability value, like 0.75.

To be concrete, let's say the current state is  $S_5$  (the state at time step 5). We input that into the policy network and it returns  $P_{\theta}(A \mid s_5) = [0.25, 0.75]$ . We sample from this distribution and take action  $a = 1$  (the second element in the action array), and after this the pole falls over and the episode has ended. The total duration of the episode was *T* = 5. For each of these 5 time steps, we took an action according to  $P_{\theta}(A|s_i)$  and we stored the specific probabilities of the actions that were actually taken,  $P_{\theta}(a|s_i)$ , in an array, which might look like [0.5, 0.3, 0.25, 0.5, 0.75]. We simply multiply these probabilities by the discounted rewards (explained in the next section), take the sum, multiply it by –1, and call that our overall loss for this episode. Unlike Gridworld, in CartPole the last action is the one that loses the episode; we discount it the most

since we want to penalize the worst move the most. In Gridworld we would do the opposite and discount the first action in the episode most, since it would be the least responsible for winning or losing.

Minimizing this objective function will tend to increase those probabilities  $P_{\theta}(a|s_t)$ weighted by the discounted rewards. So every episode we're tending to increase  $P_{\theta}(a|s_t)$ , but for a particularly long episode (if we're doing well in the game and get a large end-of-episode return) we will increase the  $P_{\theta}(a|s_i)$  to a greater degree. Hence, on average over many episodes we will reinforce the actions that are good, and the bad actions will get left behind. Since probabilities must sum to 1, if we increase the probability of a good action, that will automatically steal probability mass from the other presumably less good actions. Without this redistributive nature of probabilities, this scheme wouldn't work (i.e., everything both good and bad would tend to increase).

#### CALCULATING FUTURE REWARDS

We multiply  $P(a_t | \theta, s_t)$  by the total reward (a.k.a. return) we received after this state. As mentioned earlier in the section, we can get the total reward by just summing the rewards (which is equal to the number of time steps the episode lasted in CartPole) and create a return array that starts with the episode duration and decrements by 1 until 1. If the episode lasted 5 time steps, the return array would be  $[5,4,3,2,1]$ . This makes sense because our first action should be rewarded the most, since it is the least responsible for the pole falling and losing the episode. In contrast, the action right before the pole fell is the worst action, and it should have the smallest reward. But this is a linear decrement—we want to discount the rewards exponentially.

To compute the discounted rewards, we make an array of  $\gamma_t$  by taking our  $\gamma$  parameter, which may be set to 0.99 for example, and exponentiating it according to the distance from the end of the episode. For example, we start with gamma  $t = [0.99, 0.99,$ 0.99, 0.99, 0.99], then create another array of exponents  $exp = [1, 2, 3, 4, 5]$  and compute torch.power(gamma\_t, exp), which will give us [1.0, 0.99, 0.98, 0.97, 0.96].

#### THE LOSS FUNCTION

Now that we have discounted returns, we can use these to compute the loss function to train the policy network. As we discussed previously, we make our loss function the negative log-probability of the action given the state, scaled by the reward returns. In PyTorch, this is defined as  $-1 *$  torch.sum(r  $*$  torch.log(preds)). We compute the loss with the data we've collected for the episode, and run the torch optimizer to minimize the loss. Let's run through some actual code.

|                                                                                  | Listing 4.6 Computing the discounted rewards                         |  |  |                                                                                          |
|----------------------------------------------------------------------------------|----------------------------------------------------------------------|--|--|------------------------------------------------------------------------------------------|
|                                                                                  | def discount rewards (rewards, qamma=0.99):<br>$lenr = len(rewards)$ |  |  | <b>Computes exponentially</b><br>decaying rewards                                        |
| disc return = torch.pow(gamma,torch.arange(lenr).float()) * rewards $\leftarrow$ |                                                                      |  |  |                                                                                          |
|                                                                                  | disc return $/$ = disc return.max $()$<br>return disc return         |  |  | Normalizes the rewards to be within the<br>[0,1] interval to improve numerical stability |

Here we define a special function to compute the discounted rewards given an array of rewards that would look like  $[50, 49, 48, 47, \ldots]$  if the episode lasted 50 time steps. It essentially turns this linear sequence of rewards into an exponentially decaying sequence of rewards (e.g., [50.0000, 48.5100, 47.0448, 45.6041, ...]), and then it divides by the maximum value to bound the values in the interval [0,1].

 The reason for this normalization step is to improve the learning efficiency and stability, since it keeps the return values within the same range no matter how big the raw return is. If the raw return is 50 in the beginning of training but then reaches 200 by the end of training, the gradients are going to change by almost an order of magnitude, which hampers stability. It will still work without normalization, but not as reliably.

### **BACKPROPAGATING**

Now that we have all the variables in our objective function, we can calculate the loss and backpropagate to adjust the parameters. The following listing shows the loss function, which is just a Python translation of the math we described earlier.

![](1__page_17_Figure_5.jpeg)

### *4.4.4 The full training loop*

Initialize, collect experiences, calculate the loss from those experiences, backpropagate, and repeat. The following listing defines the full training loop of our REINFORCE agent.

![](1__page_17_Figure_8.jpeg)

![](1__page_18_Figure_1.jpeg)

We start an episode, use the policy network to take actions, and record the states and actions we observe. Then, once we break out of an episode, we have to recompute the predicted probabilities to use in our loss function. Since we record all the transitions in each episode as a list of tuples, once we're out of the episode we can separate each component of each transition (the state, action, and reward) into separate tensors to train on a batch of data at a time. If you run this code, you should be able to plot the episode duration against the episode number, and you will hopefully see a nicely increasing trend, as in figure 4.10.

 The agent learns how to play CartPole! The nice thing about this example is that it should be able to train in under a minute on your laptop with just the CPU. The state of CartPole is just a 4-dimensional vector, and our policy network is only two small layers, so it's much faster to train than the DQN we created to play Gridworld. OpenAI's documentation says that the game is considered "solved" if the agent can play an episode beyond 200 time steps. Although the plot looks like it tops off at around 190, that's because it's a moving average plot. There are many episodes that reach 200 but a few times where it randomly fails early on, bringing the average down a bit. Also, we capped the episode duration at 200, so if you increase the cap it will be able to play even longer.

# *4.4.5 Chapter conclusion*

REINFORCE is an effective and very simple way of training a policy function, but it's a little too simple. For CartPole it works very well, since the state space is very small and there are only two actions. If we're dealing with an environment with many more possible actions, reinforcing all of them each episode and hoping that on average it will only reinforce the good actions becomes less and less reliable. In the next two chapters we'll explore more sophisticated ways of training the agent.

![](1__page_19_Figure_1.jpeg)

Figure 4.10 After training the policy network to 500 epochs, we get a plot that demonstrates the agent really is learning how to play CartPole. Note that this is a moving average plot with a window of 50 to smooth the plot.

# *Summary*

- **Probability** is a way of assigning degrees of belief about different possible outcomes in an unpredictable process. Each possible outcome is assigned a probability in the interval [0,1] such that all probabilities for all outcomes sum to 1. If we believe a particular outcome is more likely than another, we assign it a higher probability. If we receive new information, we can change our assignments of probabilities.
- **P** Probability distribution is the full characterization of assigned probabilities to possible outcomes. A probability distribution can be thought of as a function  $P:O\to$  $[0,1]$  that maps all possible outcomes to a real number in the interval  $[0,1]$ such that the sum of this function over all outcomes is 1.
- A *degenerate probability distribution* is a probability distribution in which only 1 outcome is possible (i.e., it has probability of 1, and all other outcomes have a probability of 0).
- *Conditional probability* is the probability assigned to an outcome, assuming you have some additional information (the information that is conditioned).

- A *policy* is a function,  $\pi S \rightarrow A$ , that maps states to actions and is usually implemented as a probabilistic function,  $\pi P(A|S)$ , that creates a probability distribution over actions given a state.
- The *return* is the sum of discounted rewards in an episode of the environment.
- A *policy gradient method* is a reinforcement learning approach that tries to directly learn a policy by generally using a parameterized function as a policy function (e.g., a neural network) and training it to increase the probability of actions based on the observed rewards.
- **REINFORCE** is the simplest implementation of a policy gradient method; it essentially maximizes the probability of an action times the observed reward after taking that action, such that each action's probability (given a state) is adjusted according to the size of the observed reward.