# *Multi-agent reinforcement learning*

#### *This chapter covers*

- Why ordinary Q-learning can fail in the multi-agent setting
- How to deal with the "curse of dimensionality" with multiple agents
- How to implement multi-agent Q-learning models that can perceive other agents
- How to scale multi-agent Q-learning by using the mean field approximation
- How to use DONs to control dozens of agents in a multi-agent physics simulation and game

So far, the reinforcement learning algorithms we have covered—Q-learning, policy gradients, and actor-critic algorithms—have all been applied to control a single agent in an environment. But what about situations where we want to control multiple agents that can interact with each other? The simplest example of this would be a two-player game where each player is implemented as a reinforcement learning agent. But there are other situations in which we might want to model hundreds or thousands of individual agents all interacting with each other, such as a

traffic simulation. In this chapter you will learn how to adapt what you've learned so far into this multi-agent scenario by implementing an algorithm called *mean field Q-learning* (MF-Q), first described in a paper titled "Mean Field Multi-Agent Reinforcement Learning" by Yaodong Yang et al. (2018).

## *9.1 From one to many agents*

In the case of games, the environment might contain other agents that we do not control, often called *non-player characters* (NPCs). For example, in chapter 8 we trained an agent to play Super Mario Bros., which has many NPCs. These NPCs are controlled by some other unseen game logic, but they can and often do interact with the main player. From the perspective of our deep Q-network (DQN) agent, these NPCs are nothing more than patterns in the state of the environment that change over time. Our DQN is not directly aware of the actions of the other players. This is not an issue because these NPCs do not learn; they have fixed policies. As you'll see in this chapter, sometimes we want to go beyond mere NPCs and actually model the behavior of many interacting agents that learn (figure 9.1), and this requires a bit of a reformulation of the basic reinforcement learning framework you've learned about so far in this book.

![](_page_1_Figure_4.jpeg)

Figure 9.1 In the multi-agent setting, each agent's actions not only affect the evolution of the environment, but also the policies of other agents, leading to highly dynamic agent interactions. The environment will produce a state and reward, which each agent 1 through *j* use to take actions using their own policies. However, each agent's policy will affect all the other agents' policies.

For example, imagine that we directly want to control the actions of many interacting agents in some environment using a deep reinforcement learning algorithm. For example, there are games with multiple players grouped into teams, and we may want to develop an algorithm that can play a bunch of players on a team against another team. Or we may want to control the actions of hundreds of simulated cars to model traffic patterns. Or maybe we're economists and we want to model the behavior of thousands of agents in a model of an economy. This is a different situation than having

NPCs because, unlike NPCs, these other agents all learn, and their learning is affected by each other.

 The most straightforward way to extend what we know already into a multi-agent setting is to instantiate multiple DQNs (or some other similar algorithm) for the various agents, and each agent sees the environment as it is and takes actions. If the agents we are trying to control all use the same policy, which is a reasonable assumption in some cases (e.g., in a multi-player game where each player is identical), then we could even re-use a single DQN (i.e., a single set of parameters) to model multiple agents.

 This approach is called *independent Q-learning* (IL-Q), and it works reasonably well, but it misses the fact that interactions between agents affect the decision-making of each. With an IL-Q algorithm, each agent is completely unaware of what other agents are doing and how other agents' actions might affect itself. Each agent only gets a state representation of the environment, which includes the current state of each other agent, but it essentially treats the activity of other agents in the environment as noise since the behavior of other agents is, at most, only partially predictable (figure 9.2).

![](_page_2_Figure_4.jpeg)

Figure 9.2 In independent Q-learning, an agent does not directly perceive the actions of other agents but rather pretends they are part of the environment. This is an approximation that loses the convergence guarantees that Q-learning has in the single-agent setting, since the other agents make the environment nonstationary.

In the ordinary Q-learning we've done so far, where there's only a single agent in the environment, we know the Q function will converge to the optimal value, so we will converge on an optimal policy (it is mathematically guaranteed to converge in the long run). This is because in the single-agent setting, the environment is *stationary*, meaning the distribution of rewards for a given action in a given state is always the same (figure 9.3). This stationary feature is violated in the multi-agent setting since the rewards an individual agent receives will vary not only based on its own actions but on the actions of other agents. This is because all agents are reinforcement learning agents that learn through experience; their policies are constantly changing in response to changes in the environment. If we use IL-Q in this nonstationary environment, we lose the convergence guarantee, and this can impair the performance of independent Q-learning significantly.

![](_page_3_Figure_1.jpeg)

Figure 9.3 In a stationary environment, the expected (i.e., average) value over time for a given state will remain constant (stationary). Any particular state transition may have a stochastic component, hence the noisy-looking time series, but the mean of the time series is constant. In a nonstationary environment, the expected value for a given state transition will change over time, which is depicted in this time series as a changing mean or baseline over time. The Q function is trying to learn the expected value for state-actions, and it can only converge if the state-action values are stationary, but in the multi-agent setting, the expected state-action values can change over time due to the evolving policies of other agents.

A normal Q function is a function  $Q(s,a): S \times A \rightarrow R$  (figure 9.4); it's a function from a state-action pair to a reward (some real number). We can remedy the problems with IL-Q by making a slightly more sophisticated Q function that incorporates knowledge of the actions of other agents,  $Q_j(s, a_j, a_{-j})$ :  $S \times A_j \times A_{-j} \to R$ . This is a Q function for the agent indexed by *j* that takes a tuple of the state, agent *j*'s action, and all the other agents' actions (denoted  $-j$ , pronounced "not  $j$ ") to the predicted reward for this tuple (again, just a real number). It is known that a Q function of this sort regains the convergence guarantee that it will eventually learn the optimal value and policy functions, and thus this modified Q function is able to perform much better.

 Unfortunately, this new Q function is intractable when the number of agents is large because the joint action-space  $a_{-i}$  is extremely large and grows exponentially with the number of agents. Remember how we encode an action? We use a vector with length equal to the number of actions. If we want to encode a single action, we make this a *one-hot vector* where all elements are 0 except at the position corresponding to the action, which is set to 1. For example, in the Gridworld environment the agent has four actions (up, down, left, right), so we encode actions as a length 4 vector, where  $[1,0,0,0]$  could be encoded as "up" and  $[0,1,0,0]$  could be "down" and so forth.

![](_page_4_Figure_3.jpeg)

Figure 9.4 The Q function takes a state and produces state-action values (Q values), which are then used by the policy function to produce an action. Alternatively, we can directly train a policy function that operates on a state and returns a probability distribution over actions.

Remember, the policy  $\pi(s): S \to A$  is a function that takes a state and returns an action. If it is a deterministic policy, it will have to return one of these one-hot vectors; if it is a stochastic policy, it returns a probability distribution over the actions, e.g., [0.25,0.25,0.2,0.3]. The exponential growth is due to the fact that if we want to unambiguously encode a joint action—for example, the joint action of two agents with four actions each in Gridworld—then we have to use a  $4^2$  = 16 length one-hot vector instead of just a 4 length vector. This is because there are 16 different possible combinations of actions between two agents with 4 actions each: [Agent 1: Action 1, Agent 2: Action 4], [Agent 1: Action 3, Agent 2: Action 3] and so on (see figure 9.5).

If we want to model the joint action of 3 agents, we have to use a  $4^3 = 64$  length vector. So, in general for Gridworld, we have to use a  $4^N$  length vector, where N is the number of agents. For any environment, the size of the joint action vector will be  $|A|^{N}$ where  $|A|$  refers to the size of the action space (i.e., the number of discrete actions). That is an exponentially growing vector in the number of agents, and this is impractical

![](_page_5_Figure_1.jpeg)

Figure 9.5 If each agent has an action space of size 4 (i.e., it is represented by a 4 element one-hot vector), the joint action space of two agents is  $4^2 = 16$ , or  $4^N$  where N is the number of agents. This means the growth of the joint action space is exponential in the number of agents. The figure on the right shows the joint action space size for agents with individual action spaces of size 2. Even with just 25 agents, the joint action space becomes a 33,554,432 element one-hot vector, which is computationally impractical to work with.

and intractable for any significant number of agents. Exponential growth is always a bad thing, since it means your algorithm can't scale. This exponentially large joint action space is the main new complication that *multi-agent reinforcement learning* (MARL) brings, and it is the problem we'll spend this chapter solving.

#### *9.2 Neighborhood Q-learning*

You might be wondering if there is a more efficient and compact way of representing actions and joint actions that might get around this issue of an impractically large joint-action space, but unfortunately there is no unambiguous way to represent an action using a more compact encoding. Try thinking of how you could communicate, unambiguously, which actions a group of agents took using a single number, and you'll realize you can't do it better than with an exponentially growing number.

 At this point, MARL doesn't seem practical, but we can change that by making some approximations to this idealized joint-action Q function. One option is to recognize that in most environments, only agents in close proximity to each other will have any significant effect on each other. We don't necessarily need to model the joint actions of *all* the agents in the environment; we can approximate this by only modeling the joint actions of agents within the same *neighborhood*. In a sense, we divide the full joint-action space into a set of overlapping subspaces and only compute Q values for these much smaller subspaces. We might call this method *neighborhood Q-learning* or *subspace Q-learning* (figure 9.6).

![](_page_6_Figure_1.jpeg)

#### **Neighborhood MARL**

![](_page_6_Figure_3.jpeg)

By constraining the size of the neighborhood, we stop the exponential growth of the joint-action space to the fixed size we set for the neighborhood. If we have a multiagent Gridworld with 4 actions for each agent and 100 agents total, the full jointaction space is  $4^{\wedge}100$ , which is an intractable size; no computer could possibly compute with (or even store) such a large vector. However, if we use subspaces of the jointaction space and set the size of each subspace (neighborhood) to 3 (so the size of each subspace is  $4^3$  = 64), this is a much bigger vector than with a single agent, but it's definitely something we can compute with. In this case, if we're computing the Q values for agent 1, we find the 3 agents closest in distance to agent 1 and build a jointaction one-hot vector of length 64 for these 3 agents. That's what we give to the Q function (figure 9.7). So for each of the 100 agents, we would build these subspace joint-action vectors, and use them to compute Q values for each agent. Then we would use those Q values to take actions as usual.

![](_page_6_Figure_5.jpeg)

Figure 9.7 The neighborhood Q function for agent *j* accepts the current state and the jointaction vector for the other agents within its neighborhood (or field of view), denoted *a*–*j*. It produces Q values that get passed to the policy function that chooses the action to take.

Let's write some pseudocode for how this works.

![](_page_7_Figure_1.jpeg)

The pseudocode in listing 9.1 shows that we need a function that takes the current agent *j* and finds its nearest three neighbors, and then we need another function that will build the joint action using these three nearest neighbors. At this point, we have another problem: how do we build the joint action without already knowing the actions of the other agents? In order to compute the Q values for agent *j* (and thus take an action), we need to know the actions that agents –*j* are taking (we use –*j* to denote the agents that are *not* agent *j*, but in this case only the nearest neighbors). In order to figure out the actions of agents –*j*, however, we would need to compute all of their Q values, and then it seems like we get into an infinite loop and never get anywhere.

 To avoid this problem, we start by initializing all the actions for the agents randomly, and then we can compute the joint actions using these random actions. But if that's all we did, using joint actions wouldn't be much help, since they're random. In the pseudocode in listing 9.2 we address the problem by rerunning this process a few times (that's the for m in range(M) part, where M is some small number like 5). The first time we run this, the joint action will be random, but then all the agents will have taken an action based on their Q functions, so the second time it will be slightly less random, and if we keep doing this a few more times, the initial randomness will be sufficiently diluted and we can take the actions at the end of this iteration in the real environment.

![](_page_7_Figure_4.jpeg)

```
for j in agents: 
   environment.take action(j.action)
    reward = environment.get_reward()
```

**Needs to loop through agents again to take the final actions that were computed in the previous loop**

Listings 9.1 and 9.2 show the basic structure of how we will implement neighborhood Q-learning, but one detail we've left out is exactly how to construct the jointaction space for the neighboring agents. We build a joint action from a set of individual actions by using the *outer product* operation from linear algebra. The simplest way to express this is to "promote" an ordinary vector to a matrix. For example, we have a length 4 vector and we could promote it to a  $4 \times 1$  matrix. In PyTorch and numpy we can do this using the reshape method on a tensor, e.g., torch.Tensor( $[1,0,0,0]$ ). reshape $(1,4)$ . The result we get when multiplying two matrices depends on their dimensions and the order in which we multiply them. If we take an *A*:  $1 \times 4$  matrix and multiply it by another matrix *B*:  $4 \times 1$ , then we get a  $1 \times 1$  result, which is a *scalar* (a single number). This would be the *inner product* of two vectors (promoted to matrices), since the largest dimensions are sandwiched in between the two singlet dimensions. The outer product is just the reverse of this, where the two large dimensions are on the outside and the two singlet dimensions are on the inside, resulting in a  $4 \times 1 \otimes 1 \times 4 = 4 \times 4$  matrix.

If we have two agents in Gridworld with individual actions  $[0,0,0,1]$  ("right") and [0,0,1,0] ("left"), their joint action can be computed by taking the outer product of these vectors. Here's how we do it in numpy:

```
>>> np.array([[0,0,0,1]]).T @ np.array([[0,1,0,0]])
array([[0, 0, 0, 0],
      [0, 0, 0, 0],
        [0, 0, 0, 0],
       [0, 1, 0, 0]]
```

The result is a  $4 \times 4$  matrix, with a total of 16 elements as we would expect from our discussion in the previous section. The dimension of the result of the outer product between two matrices is  $\dim(A)$  \*  $\dim(B)$ , where *A* and *B* are vectors and "dim" refers to the size (dimension) of the vector. The outer product is the reason why the jointaction space grows exponentially. Generally, we need our neural network Q function to operate on inputs that are vectors, so since the outer product gives us a matrix result, we simply flatten it into a vector:

```
>>> z = np.array([[0,0,0,1]]).T @ np.array([[0,1,0,0]])
>>> z.flatten()
array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0])
```

Hopefully, you can appreciate that the neighborhood Q-learning approach is not much more complicated than ordinary Q-learning. We just need to give it an additional input, which is the joint-action vector of each agent's nearest neighbors. Let's figure out the details by tackling a real problem.

## *9.3 The 1D Ising model*

In this section we're going to apply MARL to solve a real physics problem that was first described in the early 1920s by physicist Wilhelm Lenz and his student Ernst Ising. But first, a brief physics lesson. Physicists were trying to understand the behavior of magnetic materials such as iron by mathematical models. A piece of iron that you can hold in your hand is a collection of iron atoms that are grouped together by metallic bonding. An atom is composed of a nucleus of protons (positively charged), neutrons (no charge), and an outer "shell" of electrons (negatively charged). Electrons, like other elementary particles, have a property called *spin*, which is quantized such that an electron can only have a spin-up or spin-down at any time (figure 9.8).

![](_page_9_Figure_3.jpeg)

![](_page_9_Figure_4.jpeg)

The spin property can be thought of as the electron rotating either clockwise or counter-clockwise; this is not literally true, but it suffices for our purposes. When a charged object rotates, it creates a magnetic field, so if you took a rubber balloon, gave it a static charge by rubbing it on the carpet, and then spun it around, you would have yourself a balloon magnet (albeit an extremely weak magnet). Electrons likewise create a magnetic field by virtue of their spin and electric charge, so electrons really are very tiny magnets, and since all iron atoms have electrons, the entire piece of iron can become a big magnet if all of its electrons are aligned in the same direction (i.e., all spin-up or all spin-down).

 Physicists were trying to study how the electrons "decide" to align themselves, and how the temperature of the iron affects this process. If you heat up a magnet, at some point the aligned electrons will start randomly alternating their spins so that the material loses its net magnetic field. Physicists knew that an individual electron creates a magnetic field, and that a tiny magnetic field will affect a nearby electron. If you've ever played with two bar magnets, you've noticed that they will naturally line up in one direction or repel in the opposite direction. The electrons do the same thing. It makes sense that electrons would also try to align themselves to be the same spin (figure 9.9).

 There's one added complexity though. Although individual electrons have a tendency to align themselves, a sufficiently large group of aligned electrons actually becomes unstable. This is because as the number of aligned electrons grows larger,
![](0__page_10_Picture_1.jpeg)

**Low energy**

![](0__page_10_Figure_3.jpeg)

the magnetic field grows and creates some internal strain on the material. So what really happens is that electrons will form clusters, called *domains*, in which all the electrons are aligned (either spin up or down), but other domains also form. For example, there might be a domain of 100 electrons aligned spin-up next to another domain of 100 electrons all aligned spin-down. So at the very local level, electrons minimize their energy by being aligned, but when too many are aligned and the magnetic field becomes too strong, the overall energy of the system grows, causing the electrons to align only into relatively small domains.

 Presumably the interactions between trillions of electrons in the bulk material result in the complex organization of electrons into domains, but it is very difficult to model that many interactions. So physicists made a simplifying assumption that a given electron is only affected by its nearest neighbors, which is exactly the same assumption we've made with neighborhood Q-learning (figure 9.10).

![](0__page_10_Figure_6.jpeg)

Figure 9.10 This is a high-resolution Ising model where each pixel represents an electron. The lighter pixels are spinup, and black is spin-down. You can see that the electrons organize into domains where all the electrons within a domain are aligned, but nearby electrons in an adjacent domain are anti-aligned with respect to the first domain. This organization reduces the energy of the system.

Remarkably, we can model the behavior of many electrons and observe the large-scale emergent organization with multi-agent reinforcement learning. All we need to do is interpret the energy of an electron as its "reward." If an electron changes its spin to align with its neighbor, we will give it a positive reward; if it decides to anti-align, we give it a negative reward. When all the electrons are trying to maximize their rewards, this is the same as trying to minimize their energy, and we will get the same result the physicists get when they use energy-based models.

 You might wonder why these modeled electrons wouldn't just all align in the same direction rather than form domains like a real magnet if the electrons get positive rewards for being aligned. Our model is not completely realistic, but it does end up forming domains because with a sufficiently large number of electrons, it becomes increasingly improbable for all of them to align in the same direction, given that there is some randomness to the process (figure 9.11).

| $+$ | $+$                  | $  +$ | $+$ | $+$ | $+$ | $+$   | $+$   | $+$       | $\ddot{}$ |
|-----|----------------------|-------|-----|-----|-----|-------|-------|-----------|-----------|
| $+$ |                      | $+$   |     |     |     |       |       |           |           |
| $+$ |                      |       | $+$ | $+$ | $+$ | $\pm$ | $\pm$ |           |           |
| $+$ | $\ddot{\phantom{1}}$ |       | $+$ |     |     |       |       | $\ddot{}$ | $\pm$     |
| $+$ | $+$                  | $+$   | $+$ | $+$ | $+$ | $+$   | $+$   | $+$       |           |

Figure 9.11 This is a depiction of a 2D Ising model of electron spins where + is spin-up and – is spin-down. There is a domain of electrons that are all spin-down (highlighted in black), and these are surrounded by a shell of spin-up electrons.

As you'll see, we can also model the temperature of the system by changing the amount of exploration and exploitation. Remember, exploration involves randomly choosing actions, and a high temperature involves random changes as well. They're quite analogous.

 Modeling the behavior of electron spins may seem unimportant, but the same basic modeling technique used for electrons can be used to solve problems in genetics, finance, economics, botany, and sociology, among others. It also happens to be one of the simplest ways to test out MARL, so that's our main motivation here.

 The only thing we need to do to create an Ising model is to create a grid of binary digits where 0 represents spin-down and 1 represents spin-up. This grid could be of any dimensions. We could have a one-dimensional grid (a vector), a two-dimensional grid (a matrix), or some high-order tensor.

 Over the next few code listings we will first solve the 1D Ising model, since it is so easy that we don't need to use any fancy mechanisms like experience replay or distributed algorithms. We won't even use PyTorch's built-in optimizers—we will write out the gradient descent manually in just a few lines of code. In listing 9.3 we'll define some functions to create the electron grid.

```
Listing 9.3 1D Ising model: Create the grid and produce rewards
import numpy as np
import torch
from matplotlib import pyplot as plt
def init grid(size=(10,)):
     grid = torch.randn(*size)
                                      Converts the floating-
    grid[grid > 0] = 1point numbers into a byte 
    qrid[qrid \le 0] = 0object to make it binary
     grid = grid.byte() 
                              \sim return grid
def get reward(s,a):
                            \leftarrowThis function takes neighbors 
    r = -1in s and compares them to 
     for i in s:
                                 agent a; if they match, the 
        if i == a:
                               reward is higher.r + = 0.9r * = 2.
     return r
```

We have two functions in listing 9.3; the first creates a randomly initialized 1D grid (a vector) by first creating a grid of numbers drawn from a standard normal distribution. Then we set all the negative numbers to be 0 and all the positive numbers to be 1, and we will get approximately the same number of 1s and 0s in the grid. We can visualize the grid using matplotlib:

```
\gg \gt size = (20, )>>> grid = init_grid(size=size)
>>> grid
tensor([1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
        dtype=torch.uint8)
>>> plt.imshow(np.expand_dims(grid,0))
```

As you can see in figure 9.12, the 1s are lightly shaded and the 0s are dark. We have to use the np.expand dims( $\dots$ ) function to make the vector into a matrix by adding a singlet dimension, since plt. imshow only works on matrices or 3-tensors.

 The second function in listing 9.3 is our reward function. It accepts a list, s, of binary digits, and a single binary digit, a, and then compares how many values in s match a. If all of the values match, the reward is maximal, and if none of them match, the reward is negative. The input s will be the list of neighbors. In this case, we will use the two nearest neighbors, so for a given agent its neighbors will be the agents to its

![](0__page_13_Figure_1.jpeg)

Figure 9.12 This is a 1D Ising model representing the electron spins for electrons arranged in a single row.

left and right on the grid. If an agent is at the end of the grid, its right neighbor will be the first element in the grid, so we wrap around to the beginning. This makes the grid into a circular grid.

Each element in the grid (either 1 or 0) represents an electron being spin-up or spin-down. In reinforcement learning jargon, the electrons are individual *agents* in the environment. Agents need to have value functions and policies, so they cannot merely be a binary number. The binary number on the grid represents the action of the agent, choosing to be either spin-up or spin-down. Hence, we need to model our agents using a neural network. We will use a Q-learning approach rather than the policy gradient method. In listing 9.4 we define a function that will create parameter vectors to be used in a neural network.

```
def gen_params(N,size): 
    ret = [] for i in range(N):
          vec = torch.randn(size) / 10.
          vec.requires_grad = True
          ret.append(vec)
     return ret
   Listing 9.4 The 1D Ising model: Generate neural network parameters
                                               This function 
                                               generates a list of 
                                               parameter vectors for 
                                              a neural network.
```

Since we will be using a neural network to model the Q function, we need to generate the parameters for it. In our case, we will use a separate neural network for each agent, although this is unnecessary; each agent has the same policy, so we could re-use the same neural network. We'll do this just to show how it works; for the later examples we will use a shared Q function for agents with identical policies.

 Since the 1D Ising model is so simple, we will write the neural network manually by specifying all the matrix multiplications rather than using PyTorch's built-in layers. We need to make a Q function that accepts a state vector and a parameter vector, and in the function body we unpack the parameter vector into multiple matrices that form each layer of the network.

```
def qfunc(s,theta,layers=[(4,20),(20,2)],afn=torch.tanh):
    \ln = \text{layers}[0]l1s = np.prod(l1n)Listing 9.5 The 1D Ising model: Defining the Q function
                                      Takes the first tuple in layers and multiplies those numbers 
                                     to get the subset of the theta vector to use as the first layer
```

```
theta 1 = \text{theta}[0:11s].reshape(l1n)
                                                   \overline{a}Reshapes the theta vector subset 
l2n = layers[1]into a matrix for use as the first 
l2s = np.prod(l2n)layer of the neural network
theta 2 = \text{theta}[lls:l2s+lls].reshape(l2n)
bias = torch.ones((1, \text{theta 1.shape}[1]))This is the first layer computation. 
11 = s @ theta 1 + biasThe s input is a joint-action vector 
 l1 = torch.nn.functional.elu(l1)
                                                      of dimensions (4,1).
12 = afn(11 % the t = 2)We can also input an activation function 
 return l2.flatten()
                                       to use for the last layer; the default is 
                                       tanh since our reward ranges [-1,1].
```

This is the Q function implemented as simple 2-layer neural network (figure 9.13). It expects a state vector, s, that is the binary vector of neighbors states, and a parameter vector, theta. It also needs the keyword parameter, layers, which is a list of the form  $[(s1, s2), (s3, s4) \dots]$  that indicates the shape of the parameter matrix for each layer. All Q functions return Q values for each possible action; in this case they are for down or up (two actions). For example, it might return the vector [-1,1], indicating the expected reward for changing the spin to down is –1 and the expected reward for changing the spin to up is +1.

Joint-action Parameters

![](0__page_14_Figure_4.jpeg)

Figure 9.13 The Q function for agent *j* accepts a parameter vector and a onehot encoded joint-action vector for the neighbors of agent *j*.

The advantage of using a single parameter vector is that it is easy to store all the parameters for multiple neural networks as a list of vectors. We just let the neural network unpack the vector into layer matrices. We use the tanh activation function because its output is in the interval  $[-1,1]$ , and our reward is in the interval  $[-2,2]$ , so a +2 reward will strongly push the Q value output toward +1. However, we want to be able to re-use this Q function for our later projects, so we provide the activation function as an optional keyword parameter, afn. In listing 9.6 we define some helper functions to produce state information from the environment (which is the grid).

## Listing 9.6 The 1D Ising model: Get the state of the environment

```
def get_substate(b): 
                    s = torch.zeros(2)
                    if b > 0:
                          s[1] = 1
                     else:
                         s[0] = 1 return s
               def joint state(s):
                    s1 = get substance(s[0])Takes a single binary number and turns it into 
                                                     a one-hot encoded action vector like [0,1].
                                                    If the input is 0 (down), the action 
                                                   vector is [1,0]; otherwise it is [0,1].
                                                         s is a vector with 2 elements where 
                                                         s[0] = left neighbor, s[1] = right neighbor.
      Gets
 the action
    vectors
   for each
element in s
```

```
s2 = qet subsetate(s[1])ret = (s1. reshape(2,1) \ @ \ s2. reshape(1,2)). flatten() return ret
                                      Creates the joint-action space using the
                                    outer-product, then flattens into a vector
```

The functions in listing 9.6 are two auxiliary functions we need to prepare the state information for the  $Q$  function. The get substate function takes a single binary number (0 for spin-down and 1 for spin-up) and turns it into a one-hot encoded action vector, where 0 becomes  $[1,0]$  and 1 becomes  $[0,1]$  for an action space of [down, up]. The grid only contains a series of binary digits representing the spin of each agent, but we need to turn those binary digits into action vectors and then take the outer product to get a joint-action vector for the Q function. In listing 9.7 we put some of the pieces we've made together to create a new grid and a set of parameter vectors that, in effect, comprises the set of agents on the grid.

![](0__page_15_Figure_3.jpeg)

If you run the listing 9.7 code, you should get something like figure 9.14, but yours will look different since it is randomly initialized.

tensor([0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0], dtype=torch.uint8) –0.5 0.0 0.5 0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5

Figure 9.14 A 1D Ising model of electrons arranged in a single row.

You will notice that the spins are pretty randomly distributed between up (1) and down  $(0)$ . When we train our Q function, we expect to get the spins to align themselves in the same direction. They may not *all* align in the same direction, but they should at least cluster into domains that are all aligned. Let's get into the main training loop now that we have all of the necessary functions defined.

![](0__page_16_Figure_1.jpeg)

In the main training loop, we iterate through all 20 agents (which are representing electrons), and for each one we find its left and right neighbors, get their jointaction vector, and use that to compute  $Q$  values for the two possible actions of spindown and spin-up. The 1D Ising model, as we've set it up, isn't just a line of grid cells but rather a circular chain of grid cells such that all agents have a left and right neighbor (figure 9.15).

![](0__page_16_Figure_3.jpeg)

– Figure 9.15 We are representing the 1D Ising model with a single binary vector, but it is actually a circular grid because we treat the leftmost electron as being immediately next to the rightmost electron.

Each agent has its own associated parameter vector that we use to parameterize the Q function, so each agent is controlled by a separate deep Q-network (although it is only a 2-layer neural network, so not really "deep"). Again, since each agent has the same optimal policy, which is to align the same way as its neighbors, we could have used a single DQN to control them all. We will use this approach in our subsequent projects, but we thought it was useful to show how straightforward it is to model each agent separately. In other environments, where agents may have differing optimal policies, you would need to use separate DQNs for each one.

We've simplified this main training function a bit to avoid distractions (figure 9.16). First, notice that the policy we use is a greedy policy. The agent takes the action that has the highest Q value every time; there's no epsilon-greedy policy where we sometimes take a random action. In general, some sort of exploration strategy is necessary, but this is such a simple problem that it still works. In the next section, we will solve a 2D Ising model on a square grid, and in that case we will use a softmax policy where the temperature parameter will model the actual physical temperature of the system of electrons we are trying to model.

![](0__page_17_Figure_3.jpeg)

Figure 9.16 This is a string diagram for the main training loop. For each agent, *j*, the corresponding Q function accepts a parameter vector and the joint-action vector for agent *j*, denoted *a*–*j*. The Q function outputs a 2-element Q value vector that is input to the policy function, and it chooses an action (a binary digit) that then gets stored in a mirror (clone) of the grid environment. After all agents have chosen actions, the mirrored grid synchronizes with the main grid. The rewards are generated for each agent and are passed to the loss function, which computes a loss and backpropagates the loss into the Q function, and ultimately into the parameter vector for updating.

The other simplification we made is that the target Q value is set to be  $r_{t+1}$  (the reward after taking the action). Normally it would be  $r_{t+1} + \gamma^* V(S_{t+1})$ , where the last term is the discount factor gamma times the value of the state after taking the action. The  $V(S_{t+1})$  is calculated by just taking the maximum Q value of the subsequent state  $S_{t+1}$ . This is the bootstrapping term we learned about in the DQN chapter. We will include this term in the 2D Ising model later in this chapter.

 If you run the training loop and plot the grid again, you should see something like this:

```
>>> fig,ax = plt.subplots(2,1)
>>> for i in range(size[0]):
        ax[0].scatter(np.arange(len(losses[i])),losses[i])
>>> print(grid,grid.sum())
>>> ax[1].imshow(np.expand dims(grid,0))
```

The first plot in figure 9.17 is a scatter plot of the losses over each epoch for each agent (each color is a different agent). You can see that the losses all fall and plateau around 30 epochs. The bottom plot is our Ising model grid, of course, and you can see that it has organized into two domains that are all completely aligned with each other. The lighter part in the middle is a group of agents that are aligned in the up (1) direction, and the rest are aligned in the down (0) direction. This is much better than the random distribution we started off with, so our MARL algorithm definitely worked in solving this 1D Ising model.

![](0__page_18_Figure_4.jpeg)

Figure 9.17 Top: The losses for each agent over the training epochs. You can see that they all decrease and at a minimum at around 30 epochs or so. Bottom: The 1D Ising model after maximizing rewards (minimizing energy). You can see that all the electrons are clustered together into domains where they are all oriented the same way.

We have successfully "solved" the 1D Ising model. Let's add a bit more complexity by moving on to a 2D Ising model. In addition to addressing some of the simplifications we've made, we'll introduce a new approach to neighborhood Q-learning called *mean field Q-learning*.

## *9.4 Mean field Q-learning and the 2D Ising model*

You just saw how a neighborhood Q-learning approach is able to solve the 1D Ising model fairly rapidly. This is because, rather than using the full joint-action space that would have been a  $2^{20}$  = 1,048,576 element joint-action vector, which is intractable, we

just used each agent's left and right neighbors. That reduced the size down to a  $2^2$  =  $4$ element joint-action vector, which is very manageable.

 In a 2D grid, if we want to do the same thing and just get the joint-action space of an agent's immediate neighbors, there are 8 neighbors, so the joint-action space is a  $2<sup>8</sup>$ = 256 element vector. Computing with a 256 element vector is definitely doable, but doing it for say 400 agents in a  $20 \times 20$  grid will start to get costly. If we wanted to use a 3D Ising model, the number of immediate neighbors would be 26 and the joint-action space is  $2^{26} = 67,108,864$ ; now we're into intractable territory again.

 As you can see, the neighborhood approach is much better than using the full joint-action space, but with more complex environments, even the joint-action space of immediate neighbors is too large when the number of neighbors is large. We need to make an even bigger simplifying approximation. Remember, the reason why the neighborhood approach works in the Ising model is because an electron's spin is most affected by the magnetic field of its nearest neighbors. The magnetic field strength decreases proportionally to the square of the distance from the field source, so it is reasonable to ignore distant electrons.

 We can make another approximation by noting that when two magnets are brought together, the resulting field is a kind of sum of these two magnets (figure 9.18). We can replace the knowledge of there being two separate magnets with an approximation of there being one magnet with a magnetic field that is the sum of the two components.

![](0__page_19_Figure_5.jpeg)

Figure 9.18 Left: A single bar magnet and its magnetic field lines. Recall that a magnet has two magnetic poles, often called North (N) and South (S). Right: Put two bar magnets close together, and their combined magnetic field is a bit more complicated. When we're modeling how the electron spins behave in a 2D or 3D grid, we care about the overall magnetic field generated by the contributations of all the electrons in a neighborhood; we don't need to know what the magnetic field is for each individual electron.
It is not the individual magnetic fields of the nearest electrons that matter so much as their sum, so rather than giving our Q function the spin information about each neighboring electron, we can instead give it the sum of their spins. For example, in the 1D grid, if the left neighbor has an action vector of  $[1,0]$  (down) and the right neighbor has an action vector of  $[0,1]$  (up), the sum would be  $[1,0] + [0,1] = [1,1]$ .

 Machine learning algorithms perform better when data is normalized within a fixed range like [0,1], partly due to the fact that the activation functions only output data within a limited output range (the *codomain*), and they can be "saturated" by inputs that are too large or too small. For example, the tanh function has a codomain (the range of values that it can possibly output) in the interval  $[-1, +1]$ , so if you give it two really large but non-equal numbers, it will output numbers very close to 1. Since computers have limited precision, the output values both might end up rounding to 1 despite being based on different inputs. If we had normalized these inputs to be within  $[-1,1]$ , for example, tanh might return 0.5 for one input and 0.6 for the other, a meaningful difference.

 So rather than just giving the sum of the individual action vectors to our Q function, we will give it the sum divided by the total value of all the elements, which will normalize the elements in the resulting vector to be between [0,1]. For example, we will compute  $[1,0] + [0,1] = [1,1]/2 = [0.5,0.5]$ . This normalized vector will sum to 1, and each element will be between  $[0,1]$ , so what does that remind you of? A probability distribution. We will, in essence, compute a probability distribution over the actions of the nearest neighbors, and give that vector to our Q function.

## Computing the mean field action vector

In general, we compute the mean field action vector with this formula,

$$
a_{-j} = \frac{1}{N} \sum_{i=0}^N a_i
$$

where *a–j* is just a notation for the mean field of the neighboring agents around agent *j*, and *ai* refers to the action vector for agent *i*, which is one of agent *j*'s neighbors. So we sum all the action vectors in the neighborhood of size *N* for agent *j*, and then we divide by the size of the neighborhood to normalize the results. If the math doesn't suit you, you will see how this works in Python soon.

This approach is called a *mean field approximation*, or in our case, *mean field Q-learning* (MF-Q). The idea is that we compute a kind of average magnetic field around each electron rather than supplying the individual magnetic fields of each neighbor (figure 9.19). The great thing about this approach is that the mean field vector is only as long as an individual action vector, no matter how big our neighborhood size is or how many total agents we have.

 This means that our mean field vector for each agent will only be a 2-element vector for the 1D Ising model and also for the 2D and higher dimensional Ising models.

![](1__page_21_Figure_1.jpeg)

**Mean field approximation**

Figure 9.19 The joint action for a pair of electron spins is the outer product between their individual action vectors, which is a 4-element one-hot vector. Rather than using this exact joint action, we can approximate it by taking the average of these two action vectors, resulting in what's called the *mean field approximation*. For two electrons together, with one spin-up and the other spin-down, the mean field approximation results in reducing this two electron system to a single "virtual" electron with an indeterminate spin of [0.5,0.5].

Our environment can be arbitrarily complex and high-dimensional, and it will still be computationally easy.

 Let's see how mean field Q-learning (MF-Q) works on the 2D Ising model. The 2D Ising model is exactly the same as the 1D version, except now it's a 2D grid (i.e., a matrix). The agent in the top-left corner will have its left neighbor be the agent in the top-right corner, and its neighbor above will be the agent in the bottom-left corner, so the grid is actually wrapped around the surface of a sphere (figure 9.20).

![](1__page_21_Picture_6.jpeg)

![](1__page_21_Figure_7.jpeg)

![](1__page_21_Figure_8.jpeg)

The first new function we're going to use for the 2D Ising model is the softmax function. You saw this before in chapter 2 when we introduced the idea of a policy function. A policy function is a function,  $\pi: S \to A$ , from the space of states to the space of actions. In other words, you give it a state vector and it returns an action to take. In chapter 4 we used a neural network as a policy function and directly trained it to output the best actions. In Q-learning, we have the intermediate step of first computing action values (Q values) for a given state, and then we use those action values to decide which action to take. So in Q-learning, the policy function takes in Q values and returns an action.

DEFINITION The softmax function is defined mathematically as

$$
P_t(a) = \frac{\exp(q_t(a)/\tau)}{\sum_{i=1}^n \exp(q_t(i)/\tau)},
$$

where  $P_t(a)$  is the probability distribution over actions,  $q_t(a)$  is a Q-value vector, and  $\tau$  is the temperature parameter.

As a reminder, the softmax function takes in a vector with arbitrary numbers and then "normalizes" this vector to be a probability distribution, so that all the elements are positive and sum to 1, and each element after the transformation is proportional to the element before the transformation (i.e., if an element was the largest in the vector, it will be assigned the largest probability). The softmax function has one additional input, the temperature parameter, denoted with the Greek symbol tau,  $\tau$ .

 If the temperature parameter is large, it will minimize the difference in probabilities between the elements, and if the temperature is small, differences in the input will be magnified. For example, the vector softmax  $(10, 5, 90)$ , temp=100) =  $[0.2394$ ,  $0.2277, 0.5328$ ] and softmax ( $[10,5,90]$ , temp=0.1) =  $[0.0616, 0.0521, 0.8863]$ . With a high temperature, even though the last element, 90, is 9 times larger than the second-largest element, 10, the resulting probability distribution assigns it a probability of 0.53, which is only about twice as big as the second-largest probability. When the temperature approaches infinity, the probability distribution will be uniform (i.e., all probabilities are equal). When the temperature approaches 0, the probability distribution will become a *degenerate distribution* where all the probability mass is at a single point. By using this as a policy function, when  $\tau \rightarrow \infty$ , the actions will be selected completely randomly, and when  $\tau \rightarrow 0$ , the policy becomes the argmax function (which we used in the previous section with the 1D Ising model).

 The reason this parameter is called "temperature" is because the softmax function is also used in physics to model physical systems like the spins of a system of electrons, where the temperature changes the behavior of the system. There's a lot of cross-pollination between physics and machine learning. In physics it's called the *Boltzmann distribution*, where it "gives the probability that a system will be in a certain state as a function of that state's energy and the temperature of the system" (Wikipedia). In

some reinforcement learning academic papers you might see the softmax policy referred to as the Boltzmann policy, but now you know it's the same thing.

 We are using a reinforcement learning algorithm to solve a physics problem, so the temperature parameter of the softmax function actually corresponds to the temperature of the electron system we are modeling. If we set the temperature of the system to be very high, the electrons will spin randomly and their tendency to align to neighbors will be overcome by the high temperature. If we set the temperature too low, the electrons will be stuck and won't be able to change much. In listing 9.10 we introduce a function to find the coordinates of agents and another function to generate the rewards in the new 2D environment.

![](1__page_23_Figure_3.jpeg)

It is inconvenient to work with [x,y] coordinates to refer to agents in the 2D grid. We generally refer to agents using a single index value based on flattening the 2D grid into a vector, but we need to be able to convert this flat index into [x,y] coordinates, and that is what the get coords function does. The get reward 2d function is our new reward function for the 2D grid. It computes the difference between an action vector and a mean field vector. For example, if the mean field vector is [0.25,0.75] and the action vector is  $[1,0]$ , the reward should be lower than if the action vector were  $[0,1]$ :

```
>>> get_reward_2d(torch.Tensor([1,0]),torch.Tensor([0.25, 0.75]))
tensor(-0.8483)
>>> get reward 2d(torch.Tensor([0,1]),torch.Tensor([0.25, 0.75]))
tensor(0.8483)
```

Now we need to create a function that will find an agent's nearest neighbors and then compute the mean field vector for these neighbors.

```
def mean_action(grid,j):
    x,y = qet \text{ coords}(qrid,j)Listing 9.11 Mean field Q-learning: Calculate the mean action vector
                                             Converts vectorized index j into grid 
                                             coordinates [x,y], where [0,0] is top left
```

```
action mean = torch.zeros(2)This will be the action mean 
 for i in [-1,0,1]: 
                                       vector that we will add to.
     for k in [-1,0,1]:
                                      Two for loops allow us to find each of 
        if i == k == 0:
              continue
                                      the 8 nearest neighbors of agent j.
        x, y = x + i, y + kx = x if x \ge 0 else grid.shape[0] - 1
        Y_ = Y_ if Y_ >= 0 else grid.shape[1] - 1
        x = x if x < grid.shape[0] else 0
        Y_ - = Y_ if Y_ - < grid.shape[1] else 0
        cur_n = grid[x_, y_Converts each neighbor's binary 
         s = get_substate(cur_n) 
                                            spin into an action vector
         action_mean += s
 action_mean /= action_mean.sum() 
                                        \triangleleftNormalizes the action vector to 
 return action_mean
                                            be a probability distribution
```

This function accepts an agent index, j (a single integer, the index based on the flattened grid) and returns that agent's eight nearest (surrounding) neighbors' mean action on the grid. We find the eight nearest neighbors by getting the agent's coordinates, such as [5,5], and then we just add every combination of [x,y] where  $x, y \in \{0,1\}$ . So we'll do  $[5,5] + [1,0] = [6,5]$  and  $[5,5] + [-1,1] = [4,6]$ , etc.

 These are all the additional functions we need for the 2D case. We'll re-use the init grid function and gen params functions from earlier. Let's initialize the grid and parameters.

```
>>> size = (10,10)
>>> J = np.prod(size) 
>>> hid_layer = 10
>>> layers = [(2,hid_layer),(hid_layer,2)]
>>> params = gen_params(1,2*hid_layer+hid_layer*2)
>>> grid = init_grid(size=size)
>>> grid_ = grid.clone()
>>> grid__ = grid.clone()
>>> plt.imshow(grid)
>>> print(grid.sum())
```

We're starting with a  $10 \times 10$  grid to make it run faster, but you should try playing with larger grid sizes. You can see in figure 9.21 that the spins are randomly distributed on the initial grid, so we hope that after we run our MARL algorithm it will look a lot more organized—we hope to see clusters of aligned electrons. We've reduced the hidden layer size to 10, to further reduce the computational cost. Notice that we're only generating a single parameter vector; we're going to be using a single DQN to control all of the 100 agents, since they have the same optimal policy. We're creating two copies of the main grid for reasons that will be clear once we get to the training loop.

 For this example, we are going to add some of the complexities we left out of the 1D case, since this is a harder problem. We will be using an experience replay mechanism to store experiences and train on mini-batches of these experiences. This reduces the variance in the gradients and stabilizes the training. We will also use the

![](1__page_25_Figure_1.jpeg)

![](1__page_25_Figure_2.jpeg)

proper target Q values,  $r_{t+1} + \gamma^* V(S_{t+1})$ , so we need to calculate Q values twice per iteration: once to decide which action to take, and then again to get  $V(S_{t+1})$ . In listing 9.12 we jump into the main training loop of the 2D Ising model.

![](1__page_25_Figure_4.jpeg)

```
exp = (actions, rewards, act means, q next)
                     replay.append(exp)
                     shuffle(replay)
                    if len(replay) > batch size:
                         ids = np.random.randint(low=0,high=len(replay),size=batch_size) 
                         exps = [replay[idx] for idx in ids]
                        for j in range(J):
                             jacts = torch.stack([ex[0][j] for ex in exps]).detach()
                              jrewards = torch.stack([ex[1][j] for ex in exps]).detach()
                             jmeans = torch.stack([ex[2][j] for ex in exps]).detach()
                            vs = torch.stack([ex[3][j] for ex in exps]).detach()
                             qvals = torch.stack([
                                      qfunc(jmeans[h].detach(),params[0],layers=layers) \
                                                     for h in range(batch_size)])
                             target = qvals.clone().detach()
                             target[:,torch.argmax(jacts,dim=1)] = jrewards + gamma * vs
                             loss = torch.sum(torch.pow(qvals - target.detach(),2))
                             losses[j].append(loss.item())
                             loss.backward()
                              with torch.no_grad():
                                 params[0] = params[0] - Ir * params[0]. qrad
                              params[0].requires_grad = True
                                                                         Collects an experience and 
                                                                          adds to the experience 
                                                                         replay buffer
     Once the
   experience
  replay buffer
    has more
  experiences
than the batch
size parameter,
starts training
       Generates a
     list of random
        indices to
        subset the
      replay buffer
```

That's a lot of code, but it's only a little more complicated than what we had for the 1D Ising model. The first thing to point out is that since the mean field of each agent depends on its neighbors, and the neighbors' spins are randomly initialized, all the mean fields will be random to begin with too. To help convergence, we first allow each agent to select an action based on these random mean fields, and we store the action in the temporary grid copy, grid\_\_, so that the main grid doesn't change until all agents have made a final decision about which action to take. After each agent has made a tentative action in grid\_\_, we update the second temporary grid copy, grid\_ which is what we're using to calculate the mean fields. In the next iteration, the mean fields will change, and we allow the agents to update their tentative actions. We do this a few times (controlled by the num\_iter parameter) to allow the actions to stabilize around a near optimal value based on the current version of the Q function. Then we update the main grid and collect all the actions, rewards, mean fields, and  $q$  next values  $(V(S_{t+1})$  and add them to the experience replay buffer.

 Once the replay buffer has more experiences than the batch size parameter, we can begin training on mini-batches of experiences. We generate a list of random index values and use these to subset some random experiences in the replay buffer. Then we run one step of gradient descent as usual. Let's run the training loop and see what we get.

```
>>> fig,ax = plt.subplots(2,1)
>>> ax[0].plot(np.array(losses).mean(axis=0))
>>> ax[1].imshow(grid)
```

It worked! You can see from figure 9.22 that all but three of the electrons (agents) have their spins aligned in the same direction, which minimizes the energy of the system (and maximizes the reward). The loss plot looks chaotic partly because we're using a single DQN to model each agent, so the DQN is sort of in a battle against itself when one agent is trying to align to its neighbor but its neighbor is trying to align to another agent. Some instability can happen.

![](1__page_27_Figure_2.jpeg)

Figure 9.22 The top graph is the loss plot for the DQN. The loss doesn't look like it is converging, but we can see that it does indeed learn to minimize the energy of the system (maximize reward) as a whole in the bottom panel.

In the next section we will push our multi-agent reinforcement learning skills to the next level by tackling a harder problem with two teams of agents battling against each other in a game.

## *9.5 Mixed cooperative-competitive games*

If you think of the Ising model as a multiplayer game, it would be considered a pure cooperative multiplayer game, since all the agents have the same objective and their reward is maximized when they work together to all align in the same direction. In contrast, chess would be a pure competitive game, because when one player is winning the other player is losing; it is zero-sum. Team-based games, like basketball or football, are called *mixed cooperative-competitive games,* since the agents on the same team need to cooperate in order to maximize their rewards, but when one team as a whole is winning, the other team must be losing, so at the team-to-team level it is a competitive game.

 In this section we are going to use an open source Gridworld-based game that is specially designed for testing multi-agent reinforcement learning algorithms in cooperative, competitive, or mixed cooperative-competitive scenarios (figure 9.23). In our case, we will set up a mixed cooperative-competitive scenario with two teams of Gridworld agents that can move around in the grid and can also attack other agents on the opposing team. Each agent starts with 1 "health point" (HP), and when they're attacked the HP decreases little by little until it gets to 0, at which point the agent dies and is cleared off the grid. Agents get rewards for attacking and killing agents on the opposing team.

![](1__page_28_Figure_4.jpeg)

Figure 9.23 Screenshot from the MAgent multiplayer Gridworld game with two opposing teams of Gridworld agents. The objective is for each team to kill the other.

Since all the agents on one team share the same objective and hence the optimal policy, we can use a single DQN to control all the agents on one team, and a different DQN to control the agents on the other team. It's basically a battle between two

DQNs, so this would be a perfect opportunity to try out different kinds of neural networks and see which is better. To keep things simple, though, we'll use the same DQN for each team.

 You'll need to install the MAgent library from<https://github.com/geek-ai/MAgent> by following the instructions on the readme page. From this point on, we'll assume you have it installed and that you can successfully run import magent in your Python environment.

![](1__page_29_Figure_3.jpeg)

MAgent is highly customizable, but we will be using the built-in configuration called "battle" to set up a two-team battle scenario. MAgent has an API similar to OpenAI Gym but there are some important differences. First, we have to set up "handles" for each of the two teams. These are objects, team1 and team2, that have methods and attributes relevant to each team. We generally pass these handles to a method of the environment object, env. For example, to get a list of the coordinates of each agent on team 1, we use env.get pos(team1).

 We're going to use the same technique to solve this environment as we did for the 2D Ising model, but with two DQNs. We'll use a softmax policy and experience replay buffer. Things will get a bit complicated because the number of agents changes over training, since agents can die and be removed from the grid.

 With the Ising model, the state of the environment was the joint actions; there was no additional state information. In MAgent we additionally have the positions and health points of agents as state information. The Q function will be  $Q_j(s_b a_{-j})$  where  $a_{-j}$ is the mean field for the agents within agent *j*'s *field of view* (FOV) or neighborhood. By default, each agent has a FOV of the  $13 \times 13$  grid around itself. Thus, each agent will have a state of this binary  $13 \times 13$  FOV grid that shows a 1 where there are other agents. However, MAgent separates the FOV matrix by teams, so each agent has two 13 × 13 FOV grids: one for its own team and one for the other team. We will need to combine these into a single state vector by flattening and concatenating them together. MAgent also provides the health points of the agents in the FOV, but for simplicity we will not use these.
We've initialized the environment, but we haven't initialized the agents on the grid. We now have to decide how many agents and where to place them on the grid for each team.

```
Listing 9.14 Adding the agents
hid_layer = 25
                                                        Generates two parameter
in size = 359vectors to parameterize
act space = 21two DQNs
layers = [(in size,hid layer), (hid layer, act space)]
params = gen_params(2,in_size*hid_layer+hid_layer*act_space) 
                                                                          \leqmap size = 30Sets the number of agents 
width = height = map_size
                                    for each team to 16
n1 = n2 = 16 
qap = 1Sets the initial gap distance 
epochs = 100between each team's agents
replay_size = 70
batch size = 25Loops to position agents
                                                                 on team 1 on the left side
side1 = int(math.sqrt(n1)) * 2of the grid
pos1 = []for x in range(width//2 - gap - side1, width//2 - gap - side1 + side1, 2): \leftarrowfor y in range((height - side1)//2, (height - side1)//2 + side1, 2):
         pos1.append([x, y, 0])
                                                                         Loops to position 
                                                                         agents on team 2 
side2 = int(math.sqrt(n2)) * 2on the right side 
pos2 = []of the grid
for x in range(width//2 + gap, width//2 + gap + side2, 2):
    for y in range((height - side2)//2, (height - side2)//2 + side2, 2):
         pos2.append([x, y, 0])
                                                              Adds the agents to the grid 
                                                              for team 1 using the position 
env.reset()
                                                         lists we just created
env.add agents(team1, method="custom", pos=pos1)
env.add_agents(team2, method="custom", pos=pos2)
```

Here we've set up our basic parameters. We're creating a  $30 \times 30$  grid with 16 agents for each team to keep the computational cost low, but if you have a GPU, feel free to make a bigger grid with more agents. We initialize two parameter vectors, one for each team. Again we're only using a simple two-layer neural network as the DQN. We can now visualize the grid.

```
>>> plt.imshow(env.get global minimap(30,30)[:,:,:].sum(axis=2))
```

Team 2 is on the left and team 1 on the right (figure 9.24). All the agents are initialized in a square pattern, and the teams are separated by just one grid square. Each agent's action space is a 21-length vector, depicted in figure 9.25. In listing 9.15 we introduce a function to find the neighboring agents of a particular agent.

![](2__page_31_Figure_2.jpeg)

We need this function to find the neighbors in the FOV of each agent to be able to calculate the mean action vector. We can use env.get\_pos(team1) to get a list of coordinates for each agent on team 1, and then we can pass this into the get neighbors function along with an index, j, to find the neighbors of agent j.

```
>>> get neighbors(5,env.get pos(team1))
[0, 1, 2, 4, 6, 7, 8, 9, 10, 13]
```

So agent 5 has 10 other agents on team 1 within its 13 × 13 FOV.

 We now need to create a few other helper functions. The actions that the environment accepts and returns are integers 0 to 20, so we need to be able to convert this to a one-hot action vector and back to integer form. We also need a function that will get the mean field vector for the neighbors around an agent.

| Listing 9.16 Calculating the mean field action                                                                                                                                                                                                           |                                                                                    |                                                                                                                                           |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| def qet onehot $(a, l=21)$ :<br>$x =$ torch. zeros (21)<br>$x[a] = 1$<br>return x                                                                                                                                                                        | Converts integer representation<br>of action into one-hot vector<br>representation |                                                                                                                                           |
| def get scalar(v):<br>$\text{get\_scalar}(v):$<br>$\text{Conv}(v)$ $\text{Conv}(v)$ $\text{Conv}(v)$ $\text{C}{\text{conv}(v)}$ $\text{Conv}(v)$ $\text{C}{\text{inv}(v)}$ $\text{C}{\text{inv}(v)}$ $\text{C}{\text{inv}(v)}$ $\text{C}{\text{inv}(v)}$ |                                                                                    |                                                                                                                                           |
| def get mean field(j, pos list, act list, $r=7$ , l=21):<br>$neighbors = get neighbors(j, pos list, r=r)$<br>mean field = $torch. zeros(1)$<br>for k in neighbors:<br>$act = act list[k]$<br>$act = get onehot(act)$<br>mean field $+=$ act              | Finds all the<br>neighbors of the<br>agents using pos_list                         | Gets the mean field<br>action of agent j; pos_list<br>is what is returned by<br>env.get pos(team1), and<br>I is action space<br>dimension |
| $tot = mean field.sum()$<br>mean_field = mean_interaction / tot if tot > 0 else mean_field <-   don't divide<br>return mean field                                                                                                                        |                                                                                    | Makes sure we                                                                                                                             |

The get mean field function first calls the get neighbors function to get the coordinates of all the agents for agent j. The get\_mean\_field function then uses these coordinates to get the agents' action vectors, add them, and divide by the total number of agents to normalize. The get\_mean\_field function expects the corresponding action vector act\_list (a list of integer-based actions) where indices in pos\_list and act list match to the same agent. The parameter r refers to the radius in grid squares around agent j that we want to include as neighbors, and l is the size of the action space, which is 21.

 Unlike the Ising model examples, we're going to create separate functions to select actions for each agent and to do training, since this is a more complex environment and we want to modularize a bit more. After each step in the environment, we get an observation tensor for all the agents simultaneously.

The observation returned by env.get observation(team1) is actually a tuple with two tensors. The first tensor is shown in the top portion of figure 9.26. It is a complex high-order tensor, whereas the second tensor in the tuple has some additional information that we will ignore. From now on, when we say *observation* or *state*, we mean the first tensor as depicted in figure 9.26.

 Figure 9.26 shows that this observation tensor is arranged in slices. The observation is an  $N \times 13 \times 13 \times 7$  tensor where *N* is the number of agents (in our case 16). Each  $13 \times 13$  slice of the tensor for a single agent shows the FOV with the location of the wall (slice 0), team 1 agents (slice 1), team 1 agents' HPs (slice 2), and so forth.

![](2__page_33_Figure_1.jpeg)

We will only be using slices 1 and 4 for the locations of the agents on team 1 and team 2 within the FOV. So, a single agent's observation tensor will be  $13 \times 13 \times 2$ , and we will flatten this into a vector to get a 338-length state vector. We'll then concatenate this state vector with the mean field vector, which is length 21, to get a  $338 + 21 = 359$ length vector that will be given to the Q function. It would be ideal to use a twoheaded neural network like we did in chapter 7. That way one head could process the state vector and the other could process the mean field action vector, and we could then recombine the processed information in a later layer. We did not do that here for simplicity, but is a good exercise for you to try. In listing 9.27 we define a function to choose the action for an agent, given its observation (the mean field of its neighboring agents).

![](2__page_33_Figure_3.jpeg)

This is the function we will use to choose all the actions for each agent after we get an observation. It utilizes a mean field Q function parameterized by param and layers to sample actions for all agents using the softmax policy. The inferacts function takes the following parameters (vector dimensions in parentheses for each):

- $\blacksquare$  obs is the observation tensor,  $N \times 13 \times 13 \times 2$ .
- $\blacksquare$  mean fields is tensor containing all the mean field actions for each agent,  $N \times 21$ .
- pos list is list of positions for each agent returned by env.get pos(...).
- $\blacksquare$  acts is a vector of integer-represented actions of each agent  $(N, )$ .
- num iter is the number of times to alternative between action sampling and policy updates.
- temp is the softmax policy temperature, to control the exploration rate.

The function returns a tuple:

- $\blacksquare$  acts is a vector of integer actions sampled from policy  $(N,).$
- $\blacksquare$  mean fields is a tensor of mean field vectors for each agent (N,21).
- qvals is a tensor of Q values for each action for each agent  $(N,21)$ .

Lastly, we need the function that does the training. We will give this function our parameter vector and experience replay buffer and let it do the mini-batch stochastic gradient descent.

|                                                                                  | Listing 9.18 The training function                                                                                                                                                                                                                                                                                                 |                                                                       |                                                                                    |
|----------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|------------------------------------------------------------------------------------|
|                                                                                  | Subsets the experience replay buffer<br>to get a mini-batch of data                                                                                                                                                                                                                                                                | Generates a random list of indices<br>to subset the experience replay |                                                                                    |
| <b>Collects</b><br>all states<br>from the<br>mini-batch<br>into single<br>tensor | def train (batch size, replay, param, layers, J=64, gamma=0.5, lr=0.001) :<br>ids = np.random.randint(low=0,high=len(replay), size=batch size)<br>$exps = [replay[idx] for idx in ids]$<br>$losses = []$<br>jobs = torch.stack( $[ex[0]$ for ex in exps]).detach()<br>jacts = torch.stack( $[ex[1]$ for ex in exps]).detach()<br>→ |                                                                       | Collects all rewards<br>from the mini-batch<br>into a single tensor                |
| <b>Collects all</b><br>actions from<br>the mini-batch<br>into a single<br>tensor | jrewards = $torch.setack([ex[2] for ex in exps]).detach()$<br>jmeans = $torch.setack([ex[3] for ex in exps]).detach()$<br>$vs = torch.setack([ex[4] for ex in exps]).detach()$<br>$\sigma s = []$                                                                                                                                  |                                                                       | Collects all mean<br>field actions from<br>the mini-batch into<br>a single tensor  |
| Loops<br>through each<br>experience in<br>the mini-batch                         | $\rightarrow$ for h in range(batch size):<br>state = $torch.cat((iobs[h].flatten(),imeans[h]))$<br>qs.append(qfunc(state.detach(),param,layers=layers))<br>-⊳<br>$qvals = torch.setack(qs)$<br>$target = qvals.close() .delta()$<br>$target[:, jacts] = jrewards + gamma * torch.max(vs, dim=1) [0]$                               |                                                                       | <b>Collects all state</b><br>values from the<br>mini-batch into<br>a single tensor |
| <b>Computes 0</b><br>values for each<br>experience in                            | $loss = torch.sum(torch.pow(qvals - target.detach(), 2))$<br>losses.append(loss.detach().item())<br>loss.backward()                                                                                                                                                                                                                |                                                                       | <b>Computes</b><br>the target<br><b>O</b> values                                   |
| the replay                                                                       | with torch.no grad():<br>$param = param - lr * param.read$<br>param.requires grad = True<br>return np.array(losses).mean()                                                                                                                                                                                                         | ⋖<br><b>Stochastic</b><br>gradient<br>descent                         |                                                                                    |

This function works pretty much the same way we did experience replay with the 2D Ising model in listing 9.12, but the state information is more complicated.

 The train function trains a single neural network using stored experiences in an experience replay memory buffer. It has the following inputs and outputs:

- **I**nputs:
  - batch\_size (int)
  - replay, list of tuples (obs\_1\_small, acts\_1,rewards1,act\_means1,qnext1)
  - param (vector) neural network parameter vector
  - layers (list) contains shape of neural network layers
  - $-$  J (int) number of agents on this team
  - gamma (float in [0,1]) discount factor
  - lr (float) learning rate for SGD
- **Returns:** 
  - loss (float)

We've now set up the environment, set up the agents for the two teams, and defined several functions to let us train the two DQNs we're using for mean field Q-learning. Now we get into the main loop of game play. Be warned, there is a lot of code in the next few listings, but most of it is just boilerplate and isn't critical for understanding the overall algorithm.

 Let's first set up our preliminary data structures, like the replay buffers. We will need separate replay buffers for team 1 and team 2. In fact, we will need almost everything separate for team 1 and team 2.

```
N1 = env.get_num(team1) 
N2 = env.get_num(team2)
step ct = 0acts 1 = \text{torch.random}(low=0,high=act space, size=(N1,))acts 2 = torch.randint(low=0,high=act space,size=(N2,))
replay1 = deque(maxlen=replay_size) 
replay2 = deque(maxlen=replay_size)
qnext1 = <i>torch.zeros</i>(N1)qpext2 = torch.zeros(N2)act means1 = init mean field(N1, act space)
act means2 = init mean field(N2, act space)
rewards1 = torch.zeros(N1) 
rewards2 = torch.zeros(N2)
losses1 = []losses2 = []Listing 9.19 Initializing the actions
                                     Stores the number of 
                                     agents on each team
                                                                        Initializes the actions 
                                                                       for all the agents
                                                 Creates replay buffer using 
                                                 a deque data structure
                                     Creates tensors to store the Q(s') 
                                      values, where s' is the next state
                                                           Initializes the mean 
                                                           fields for each agent
                                      Creates tensors to store the 
                                      rewards for each agent
```

The variables in listing 9.19 allow us to keep track of the actions (integers), mean field action vectors, rewards, and next state Q values for each agent so that we can package these into experiences and add them into the experience replay system. In listing 9.20 we define a function to take actions on behalf of a particular team of agents and another function to store experiences in the replay buffer.

![](2__page_36_Figure_2.jpeg)

The team step function is the workhouse of the main loop. We use it to collect all the data from the environment and to run the DQN to decide which actions to take. The add to replay function takes the observation tensor, action tensor, reward tensor, action mean field tensor, and the next state Q value tensor and adds each individual agent experience to the replay buffer separately.

 The rest of the code is all within a giant while loop, so we will break it into parts, but just remember that it's all part of the same loop. Also remember that all this code is together in Jupyter Notebooks on this book's GitHub page at [http://mng.bz/JzKp.](http://mng.bz/JzKp) It contains all of the code we used to create the visualizations, and more comments. We finally get to the main training loop of the algorithm in listing 9.21.

```
for i in range(epochs):
         done = False
         while not done: 
             acts 1, act means1, qvals1, obs small 1, ids 1 = \setminusteam step(team1, params[0], acts 1, layers)
              env.set_action(team1, acts_1.detach().numpy().astype(np.int32)) 
       Listing 9.21 Training loop
                                            While the game 
                                            is not over
                                                                     Uses the team_step method
                                                                     to collect environment data
                                                                      and choose actions for the
                                                                          agents using the DQN
Instantiates the chosen 
actions in the environment
```

```
acts 2, act means2, qvals2, obs small 2, ids 2 = \langle team_step(team2,params[0],acts_2,layers)
                      env.set action(team2, acts 2.detach().numpy().astype(np.int32))
                  \Rightarrow done = env.step()
                        _, _, qnext1, _, ids_1 = team_step(team1,params[0],acts_1,layers) 
                      \mu, \mu qnext2, \mu, ids_2 = team_step(team2, params[0], acts 2, layers)
                   \rightarrow env.render()
                       rewards1 = torch.from_numpy(env.get_reward(team1)).float() 
                       rewards2 = torch.from_numpy(env.get_reward(team2)).float()
 Takes a step in
the environment,
     which will
 generate a new
observation and
       rewards Reruns team_step to get the Q values for
                                                                      the next state in the environment
       Renders the
   environment for
                                                  Collects the rewards into a tensor for each agent
```

The while loop runs as long as the game is not over; the game ends when all the agents on one team die. Within the team\_step function, we first get the observation tensor and subset the part we want as we described before, resulting in a  $13 \times 13 \times 2$ tensor. We also get ids\_1, which are the indices for the agents that are still alive on team 1. We also need to get the coordinate positions of each agent on each team. Then we use our infer acts function to choose actions for each agent and instantiate them in the environment, and finally take an environment step, which will generate new observations and rewards. Let's continue in the while loop.

```
Listing 9.22 Adding to the replay (still in while loop from listing 9.21)
                    replay1 = add to replay(replay1, obs small 1,
                    acts 1, rewards1, act means1, qnext1)
                                                                               Builds a zipped list of
  Adds to
                    replay2 = add to replay(replay2, obs small 2,
                                                                                 IDs to keep track of
experience
                                                                                  which agents died
                    acts 2, rewards2, act means2, qnext2)
   replay
                                                                                 and will be cleared
                     shuffle(replay1) 
                                                                                      from the grid
                     shuffle(replay2)
    Shuffles
  the replay
                    ids 1 = list(zip(np.arange(ids 1.shape[0]),ids 1))buffer
                    ids 2 = list(zip(np.arange(ids 2.shape[0]),ids 2))env.clear dead()
    Clears the
                                                                    Now that the dead agents 

dead agents
                     ids_1 = env.get_agent_id(team1) 
                                                                    are cleared, gets the new 
   off the grid
                                                                  list of agent IDs
                    ids 2 = env.get agent id(team2)ids_1 = [i for (i,j) inids_1 if j inids_1]Subsets the old list 
                    ids 2 = [i for (i,j) in ids 2 if j in ids 2]of IDs based on which 
                                                                                  agents are still alive
                    acts_1 = acts_1[ids_1]\leftrightarrowSubsets the action list 
                    acts 2 = \arcts 2[ids 2]based on the agents 
                                                       that are still alive step_ct += 1
                    if step ct > 250:
                         break
```

| If the replay | $\rightarrow$ if len(replay1) > batch size and len(replay2) > batch size: |
|---------------|---------------------------------------------------------------------------|
| buffers are   | $loss1 = train(batch size, replay1,params[0], layers=layers, J=NI)$       |
| sufficiently  | $loss2 = train(batch size, replay2,params[1], layers=layers, J=NI)$       |
| full, starts  | losses1.append(loss1)                                                     |
| training      | losses2.append(loss2)                                                     |

In this last part of the code, all we do is collect all the data into a tuple and append it to the experience replay buffers for training. The one complexity of MAgent is that the number of agents decreases over time as they die, so we need to do some housekeeping with our arrays to make sure we're keeping the data matched up with the right agents over time.

 If you run the training loop for just a handful of epochs, the agents will start demonstrating some skill in battle, since we made the grid very small and only have 16 agents on each team. You can view a video of the recorded game by following the instructions here: [http://mng.bz/aRdz.](http://mng.bz/aRdz) You should see the agents charge at each other and a few get killed before the video ends. Figure 9.27 is a screenshot toward the end of our video showing one of the teams clearly beating the other team by attacking them in a corner.

![](2__page_38_Picture_4.jpeg)

Figure 9.27 Screenshot of the MAgent battle game after training with mean field Q-learning. The dark team has forced the light team into the corner and it's attacking them.

## *Summary*

- Ordinary Q-learning does not work well in the multi-agent setting because the environment becomes nonstationary as agents learn new policies.
- A nonstationary environment means that the expected value of rewards changes over time.
- In order to handle this nonstationarity, the Q function needs to have access to the joint-action space of other agents, but this joint-action space scales

exponentially with the number of agents, which becomes intractable for most practical problems.

- Neighborhood Q-learning can mitigate the exponential scaling by only computing over the joint-action space of the immediate neighbors of a given agent, but even this can be too large if the number of neighbors is large.
- Mean field Q-learning (MF-Q) scales linearly with the number of agents because we only compute a mean action rather than a full joint-action space.