# *Predicting the best states and actions: Deep Q-networks*

#### *This chapter covers*

- **IMPLEMENTIFY INCO.** Implementing the Q function as a neural network
- **Building a deep Q-network using PyTorch to play Gridworld**
- Counteracting catastrophic forgetting with experience replay
- **IMPROVING IS ADDIGE 19** Improving learning stability with target networks

In this chapter we'll start off where the deep reinforcement learning revolution began: DeepMind's deep Q-networks, which learned to play Atari games. We won't be using Atari games as our testbed quite yet, but we will be building virtually the same system DeepMind did. We'll use a simple console-based game called Gridworld as our game environment.

 Gridworld is actually a family of similar games, but they all generally involve a grid board with a player (or agent), an objective tile (the "goal"), and possibly one or more special tiles that may be barriers or may grant negative or positive rewards. The player can move up, down, left, or right, and the point of the game is to get the player to the goal tile where the player will receive a positive reward. The player must not only reach the goal tile but must do so following the shortest path, and they may need to navigate through various obstacles.

# *3.1 The Q function*

We will use a very simple Gridworld engine that's included in the GitHub repository for this book. You can download it at <http://mng.bz/JzKp>in the Chapter 3 folder.

 The Gridworld game depicted in figure 3.1 shows the simple version of Gridworld we'll start with; we'll progressively tackle more difficult variants of the game. Our initial goal is to train a DRL agent to navigate the Gridworld board to the goal, following the most efficient route every time. But before we get too far into that, let's review the key terms and concepts from the previous chapter, which we will continue to use here.

![](_page_1_Figure_4.jpeg)

![](_page_1_Figure_5.jpeg)

The *state* is the information that our agent receives and uses to make a decision about what action to take. It could be the raw pixels of a video game, sensor data from an autonomous vehicle, or, in the case of Gridworld, a tensor representing the positions of all the objects on the grid.

The *policy*, denoted  $\pi$ , is the strategy our agent follows when provided a state. For example, a policy in Blackjack might be to look at our hand (the state) and hit or stay randomly. Although this would be a terrible policy, the important point to stress is that the policy confers which actions we take. A better policy would be to always hit until we have 19.

 The *reward* is the feedback our agent gets after taking an action, leading us to a new state. For a game of chess, we could reward our agent +1 when it performs an action that leads to a checkmate of the other player and –1 for an action that leads our agent to be checkmated. Every other state could be rewarded 0, since we do not know if the agent is winning or not.

Our agent makes a series of actions based upon its policy  $\pi$ , and repeats this process until the episode ends, thereby we get a succession of states, actions and the resulting rewards.

![](_page_1_Figure_10.jpeg)

We call the weighted sum of the rewards while following a policy from the starting state *S*1 the *value* of that state, or a state value. We can denote this by the *value function*  $V_{\pi}(s)$ , which accepts an initial state and returns the expected total reward.

$$
V_{\pi}(s) = \sum_{i=1}^{t} w_i R_i = w_1 R_1 + w_2 R_2 + \dots + w_t R_t
$$

The coefficients  $w_1$ ,  $w_2$ , etc., are the weights we apply to the rewards before summing them. For example, we often want to weight more recent rewards greater than distant future rewards. This weighted sum is an expected value, a common statistic in many quantitative fields, and it's often concisely denoted  $E[R | \pi, s]$ , read as "the expected rewards given a policy <sup>π</sup> and a starting state *s*." Similarly, there is an *action-value function,*  $Q_{\pi}(s, a)$ , that accepts a state *S* and an action *A* and returns the value of taking that action given that state; in other words,  $E[R | \pi, s, a]$ . Some RL algorithms or implementations will use one or the other.

 Importantly, if we base our algorithm on learning the state values (as opposed to action values), we must keep in mind that the value of a state depends completely on our policy, π. Using Blackjack as an example, if we're in the state of having a card total of 20, and we have two possible actions, hit or stay, the value of this state is only high if our policy says to stay when we have 20. If our policy said to hit when we have 20, we would probably bust and lose the game, so the value of that state would be low. In other words, the value of a state is equivalent to the value of the highest action taken in that state.

## *3.2 Navigating with Q-learning*

In 2013, DeepMind published a paper entitled "Playing Atari with Deep Reinforcement Learning" that outlined their new approach to an old algorithm, which gave them enough performance to play six of seven Atari 2600 games at record levels. Crucially, the algorithm they used only relied on analyzing the raw pixel data from the games, just like a human would. This paper really set off the field of deep reinforcement learning.

 The old algorithm they modified is called *Q-learning,* and it has been around for decades. Why did it take so long to make such significant progress? A large part is due to the general boost that artificial neural networks (deep learning) got a few years prior with the use of GPUs that allowed the training of much larger networks. But a significant amount is due to the specific novel features DeepMind implemented to address some of the other issues that reinforcement learning algorithms struggled with. We'll be covering it all in this chapter.

#### *3.2.1 What is Q-learning?*

What is Q-learning, you ask? If you guessed it has something to do with the actionvalue function  $Q_{\pi}(s, a)$  that we previously described, you are right, but that's only a small part of the story. Q-learning is a particular method of learning optimal action

values, but there are other methods. That is to say, value functions and action-value functions are general concepts in RL that appear in many places; Q-learning is a particular algorithm that uses those concepts.

 Believe it or not, we sort of implemented a Q-learning algorithm in the last chapter when we built a neural network to optimize the ad placement problem. The main idea of Q-learning is that your algorithm predicts the value of a state-action pair, and then you compare this prediction to the observed accumulated rewards at some later time and update the parameters of your algorithm, so that next time it will make better predictions. That's essentially what we did in the last chapter when our neural network predicted the expected reward (value) of each action given a state, observed the actual reward, and updated the network accordingly. That was a particular and simple implementation of a broader class of Q-learning algorithms that is described by the following update rule:

![](_page_3_Figure_3.jpeg)

Table 3.1 Q-learning update rule

The Q value at time *t* is updated to be the current predicted Q value plus the amount of value we expect in the future, given that we play optimally from our current state.

## *3.2.2 Tackling Gridworld*

You've now seen the formula for Q-learning. Let's take a step back and apply this formula to our Gridworld problem. Our goal in this chapter is to train a neural network to play a simple Gridworld game from scratch. All the agent will have access to is what the board looks like, just as a human player would; the algorithm has no informational advantage. Moreover, we're starting with an untrained algorithm, so it literally

knows nothing at all about the world. It has no prior information about how games work. The only thing we'll provide is the reward for reaching the goal. The fact that we will be able to teach the algorithm to learn to play, starting from nothing, is actually quite impressive.

 Unlike us humans who live in what appears to be a continuous flow of time, the algorithm lives in a discrete world, so something needs to happen at each discrete time step. At time step 1 the algorithm will "look" at the game board and make a decision about what action to take. Then the game board will be updated, and so on.

 Let's sketch out the details of this process now. Here's the sequence of events for a game of Gridworld.

- 1 We start the game in some state that we'll call  $S_t$ . The state includes all the information about the game that we have. For our Gridworld example, the game state is represented as a  $4 \times 4 \times 4$  tensor. We will go into more detail about the specifics of the board when we implement the algorithm.
- 2 We feed the  $S_t$  data and a candidate action into a deep neural network (or some other fancy machine-learning algorithm) and it produces a prediction of how valuable taking that action in that state is (see figure 3.2).

![](_page_4_Figure_6.jpeg)

Figure 3.2 The Q function could be any function that accepts a state and action and returns the value (expected rewards) of taking that action given that state.

Remember, the algorithm is not predicting the reward we will get after taking a particular action; it's predicting the expected value (the expected rewards), which is the long-term average reward we will get from taking an action in a state and then continuing to behave according to our policy  $\pi$ . We do this for several (perhaps all) possible actions we could take in this state.

- <sup>3</sup> We take an action, perhaps because our neural network predicted it is the highest value action or perhaps we take a random action. We'll label the action *At*. We are now in a new state of the game, which we'll call  $S_{t+1}$ , and we receive or observe a reward, labelled  $R_{t+1}$ . We want to update our learning algorithm to reflect the actual reward we received, after taking the action it predicted was the best. Perhaps we got a negative reward or a really big reward, and we want to improve the accuracy of the algorithm's predictions (see figure 3.3).
- 4 Now we run the algorithm using  $S_{t+1}$  as input and figure out which action our algorithm predicts has the highest value. We'll call this value  $Q(S_{t+1}, a)$ . To be clear, this is a single value that reflects the highest predicted *Q* value, given our new state and all possible actions.

<sup>5</sup> Now we have all the pieces we need to update the algorithm's parameters. We'll perform one iteration of training using some loss function, such as meansquared error, to minimize the difference between the predicted value from our algorithm and the target prediction of  $Q(S_t, A_t) + \alpha * [R_{t+1} + \gamma * \max Q(S_{t+1}, A)$  $-Q(S_t, A_t)$ ].

![](_page_5_Figure_2.jpeg)

Figure 3.3 Schematic of Q-learning with Gridworld. The Q function accepts a state and an action, and returns the predicted reward (value) of that stateaction pair. After taking the action, we observe the reward, and using the update formula, we use this observation to update the Q function so it makes better predictions.

## *3.2.3 Hyperparameters*

The parameters  $\gamma$  and  $\alpha$  are called *hyperparameters* because they're parameters that influence how the algorithm learns but they're not involved in the actual learning. The parameter  $\alpha$  is the *learning rate* and it's the same hyperparameter used to train many machine-learning algorithms. It controls how quickly we want the algorithm to learn from each move: a small value means it will only make small updates at each step, whereas a large value means the algorithm will potentially make large updates.

#### *3.2.4 Discount factor*

The parameter γ, the *discount factor*, is a variable between 0 and 1 that controls how much our agent discounts future rewards when making a decision. Let's take a simple example. Our agent has a decision between picking an action that leads to 0 reward then  $+1$  reward, or an action that leads to  $+1$  and then 0 reward (see figure 3.4).

![](_page_6_Figure_3.jpeg)

Figure 3.4 An illustration of action trajectories leading to the same total reward but that may be valued differently since more recent rewards are generally valued more than distant rewards.

Previously, we defined the value of a trajectory as the expected reward. Both trajectories in figure 3.4 provide +1 overall reward though, so which sequence of actions should the algorithm prefer? How can we break the tie? Well, if the discount factor,  $\chi$ is less than 1, we will discount future rewards more than immediate rewards. In this simple case, even though both paths lead to a total of  $+1$  rewards, action *b* gets the  $+1$ reward later than action *a*, and since we're discounting the action further in the future, we prefer action *a*. We multiply the +1 reward in action *b* by a weighting factor less than 1, so we lower the reward from +1 to say 0.8, so the choice of action is clear.

 The discount factor comes up in real life as well as RL. Suppose someone offers you \$100 now or \$110 one month from now. Most people would prefer to receive the money now, because we discount the future to some degree, which makes sense because the future is uncertain (what if the person offering you the money dies in two weeks?). Your discount factor in real life would depend on how much money someone would have to offer you in one month for you to be indifferent to choosing that versus getting \$100 right now. If you would only accept \$200 in a month versus \$100 right now, your discount factor would be  $$100/\$200 = 0.5$  (per month). This would mean that someone would have to offer you \$400 in two months for you to choose that option over getting \$100 now, since we'd discount 0.5 for 1 month, and 0.5 again for the next month, which is  $0.5 \times 0.5 = 0.25$ , and  $100 = 0.25x$ , so  $x = 400$ . Perhaps you might see the pattern that discounting is exponential in time. The value of something at time *t* with a discount factor of  $\gamma$ :[0,1) is  $\gamma$ <sup>t</sup>.

 The discount factor needs to be between 0 and 1, and we shouldn't set it exactly equal to 1, because if we don't discount at all, we would have to consider the future rewards infinitely far into the future, which is impossible in practice. Even if we discount at 0.99999, there will eventually come a time beyond which we no longer consider any data, since it will be discounted to 0.

 In Q-learning, we face the same decision: how much do we consider future observed rewards when learning to predict Q values? Unfortunately, there's no definitive answer to this, or to setting pretty much any of the hyperparameters we have control over. We just have to play around with these knobs and see what works best empirically.

 It's worth pointing out that most games are *episodic*, meaning that there are multiple chances to take actions before the game is over, and many games like chess don't naturally assign points to anything other than winning or losing the game. Hence, the reward signal in these games is sparse, making it difficult for trial-and-error based learning to reliably learn anything, as it requires seeing a reward fairly frequently.

 In Gridworld, we've designed the game so that any move that doesn't win the game receives a reward of –1, the winning move gets a reward of +10, and a losing move rewards –10. It's really only the final move of the game where the algorithm can say "Aha! Now I get it!" Since each episode of a Gridworld game can be won in a fairly small number of moves, the sparse reward problem isn't too bad, but in other games it is such a significant problem that even the most advanced reinforcement learning algorithms have yet to reach human-level performance. One proposed method of dealing with this is to stop relying on the objective of maximizing expected rewards and instead instruct the algorithm to seek novelty, through which it will learn about its environment, which is something we'll cover in chapter 8.

#### *3.2.5 Building the network*

Let's dig into how we will build our deep learning algorithm for this game. Recall that a neural network has a particular kind of architecture or network topology. When you build a neural network, you have to decide how many layers it should have, how many parameters each layer has (the "width" of the layer), and how the layers are connected. Gridworld is simple enough that we don't need to build anything fancy. We can get away with a fairly straightforward feedforward neural network with only a few layers, using the typical rectified linear activation unit (ReLU). The only parts that require some more careful thought are how we will represent our input data, and how we will represent the output layer.

 We'll cover the output layer first. In our discussion of Q-learning, we said that the Q function is a function that takes some state and some action and computes the value of that state-action pair,  $Q(s,a)$ . This is how the Q function was originally defined (figure 3.5). As we noted in the previous chapter, there is also a state-value function, usually denoted  $V_{\pi}(s)$ , that computes the value of some state, given that you're following a particular policy,  $\pi$ .

 Generally, we want to use the Q function because it can tell us the value of taking an action in some state, so we can take the action that has the highest predicted value. But it would be rather wasteful to separately compute the Q values for every possible action given the state, even though the Q function was originally defined that way. A much more efficient procedure, and the one that DeepMind employed in its implementation of deep Q-learning, is to instead recast the  $Q$  function as a vector-valued function, meaning that instead of computing and returning a single Q value for a single state-action pair, it will compute the Q values for all actions, given some state, and return the vector of all those Q values. So we might represent this new version of the Q function as  $Q_A(s)$ , where the subscript *A* denotes the set of all possible actions (figure 3.5).

![](_page_8_Figure_1.jpeg)

Figure 3.5 The original Q function accepts a state-action pair and returns the value of that state-action pair—a single number. DeepMind used a modified vector-valued Q function that accepts a state and returns a vector of state-action values, one for each possible action given the input state. The vector-valued Q function is more efficient, since you only need to compute the function once for all the actions.

Now it's easy to employ a neural network as our  $Q_A(s)$  version of the Q function; the last layer will simply produce an output vector of Q values—one for each possible action. In the case of Gridworld, there are only four possible actions (up, down, left, right) so the output layer will produce 4-dimensional vectors. We can then directly use the output of the neural network to decide what action to take using some action selection procedure, such as a simple epsilon-greedy approach or a softmax selection policy. In this chapter we'll use the epsilon-greedy approach (figure 3.6) as DeepMind did, and instead of using a static  $\epsilon$  value like we did in the last chapter, we will initialize it to a large value (i.e., 1, so we'll start with a completely random selection of actions) and we will slowly decrement it so that after a certain number of iterations, the  $\varepsilon$  value will rest at some small value. In this way, we will allow the algorithm to explore and learn a lot in the beginning, but then it will settle into maximizing rewards by exploiting what it has learned. Hopefully we will set the decrementing process so that it will not underexplore or overexplore, but that will have to be tested empirically.

![](_page_8_Figure_4.jpeg)

Figure 3.6 In an epsilon-greedy action selection method, we set the epsilon parameter to some value, e.g., 0.1, and with that probability we will randomly select an action (completely ignoring the predicted Q values) or with probability  $1 -$  epsilon = 0.9, we will select the action associated with the highest predicted Q value. An additional helpful technique is to start with a high epsilon value, such as 1, and then slowly decrement it over the training iterations.
We have the output layer figured out—now to tackle the rest. In this chapter, we will construct a network of just three layers with widths of 164 (input layer), 150 (hidden layer), 4 (the output layer you already saw). You are welcome and encouraged to add more hidden layers or to play with the size of the hidden layer—you will likely be able to achieve better results with a deeper network. We chose to implement a fairly shallow network here so that you can train the model with your own CPU (it takes our MacBook Air 1.7 GHz Intel Core i7, with 8 GB of RAM, only a few minutes to train).

 We already discussed why the output layer is of width 4, but we haven't talked about the input layer yet. Before we do that, though, we need to introduce the Gridworld game engine we will be using. We developed a Gridworld game for this book, and it is included in the GitHub repository for this chapter.

## *3.2.6 Introducing the Gridworld game engine*

In the GitHub repository for this chapter, you'll find a file called Gridworld.py. Copy and paste this file into whatever folder you'll be working out of. You can include it in your Python session by running from Gridworld import \*. The Gridworld module contains some classes and helper functions to run a Gridworld game instance. To create a Gridworld game instance, run the code in the following listing.

Listing 3.1 Creating a Gridworld game

```
from Gridworld import Gridworld
game = Gridworld(size=4, mode='static')
```

The Gridworld board is always square, so the size refers to one side's dimension—in this case a  $4 \times 4$  grid will be created. There are three ways to initialize the board. The first is to initialize it statically, as in listing 3.1, so that the objects on the board are initialized at the same predetermined locations. Second, you can set mode='player' so that just the player is initialized at a random position on the board. Last, you can initialize it so that all the objects are placed randomly (which is harder for the algorithm to learn) using mode='random'. We'll use all three options eventually.

 Now that we've created the game, let's play it. Call the display method to display the board and the makeMove method to make a move. Moves are encoded with a single letter: *u* for up, *l* for left, and so on. After each move, you should display the board to see the effect. Additionally, after each move you'll want to observe the reward/outcome of the move by calling the reward method. In Gridworld, every nonwinning move receives a  $-1$  reward. The winning move (reaching the goal) receives a  $+10$ reward, and there's a –10 reward for the losing move (landing on the pit).

```
>>> game.display()
array([['+', '-', ' ', 'P'],
        [' ', 'W', ' ', ' '],
       [ ' [ ', ', ' ', ', ', '' '],
         [' ', ' ', ' ', ' ']], dtype='<U2')
```

```
>>> game.makeMove('d')
>>> game.makeMove('d')
>>> game.makeMove('l')
>>> game.display()
array([[1+,1, 1-1, 1-1, 1-1, 1-1],[ ' ' ', ' 'W', ' ' ', ' '],
       [ ' ', ' ', 'P', ' '],
        [' ', ' ', ' ', ' ']], dtype='<U2')
>>> game.reward()
-1
```

Now let's look at how the game state is actually represented, since we will need to feed this into our neural network. Run the following command:

```
>>> game.board.render_np()
array([[[0, 0, 0, 0],
         [0, 0, 0, 0],
        [0, 0, 1, 0], [0, 0, 0, 0]],
        [[1, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 1, 0, 0],
         [0, 0, 0, 0],
        [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 0, 0],
        [0, 1, 0, 0],[0, 0, 0, 0],
         [0, 0, 0, 0]]], dtype=uint8)
>>> game.board.render np().shape
(4, 4, 4)
```

The state is represented as a  $4 \times 4 \times 4$  tensor where the first dimension indexes a set of four matrices of size 4 × 4. You can interpret this as having the dimensions *frames* by *height* by *width*. Each matrix is a  $4 \times 4$  grid of zeros and a single 1, where a 1 indicates the position of a particular object. Each matrix encodes the position of one of the four objects: the player, the goal, the pit, and the wall. If you compare the result from display with the game state, you can see that the first matrix encodes the position of the player, the second matrix encodes the position of the goal, the third matrix encodes the position of the pit, and the last matrix encodes the position of the wall.

 In other words, the first dimension of this 3-tensor is divided into four separate grid planes, where each plane represents the position of each element. Figure 3.7 shows an example where the player is at grid position  $(2,2)$ , the goal is at  $(0,0)$ , the pit is at  $(0,1)$ , and the wall is at  $(1,1)$ , where the planes are (row, column). All other elements are 0s.

![](0__page_11_Figure_1.jpeg)

Figure 3.7 This is how the Gridworld board is represented as a numpy array. It is a 4 x 4 x 4 tensor, composed of 4 "slices" of a 4 x 4 grid. Each grid slice represents the position of an individual object on the board and contains a single 1, with all other elements being Os. The position of the 1 indicates the position of that slice's object.

While we could, in principle, build a neural network that can operate on a  $4 \times 4 \times 4$ tensor, it is easier to just flatten it into a 1-tensor (a vector). A  $4 \times 4 \times 4$  tensor has  $4^3 = 64$ total elements, so the input layer of our neural network must be accordingly shaped. The neural network will have to learn what this data means and how it relates to maximizing rewards. Remember, the algorithm will know absolutely nothing to begin with.

## *3.2.7 A neural network as the Q function*

Let's build the neural network that will serve as our Q function. As you know, in this book we're using PyTorch for all our deep learning models, but if you're more comfortable with another framework such as TensorFlow or MXNet, it should be fairly straightforward to port the models.

 Figure 3.8 shows the general architecture for the model we will build. Figure 3.9 shows it in string diagram form with typed strings.

![](0__page_11_Figure_7.jpeg)

Figure 3.8 The neural network model we will use to play Gridworld. The model has an input layer that can accept a 64-length game state vector, some hidden layers (we use one, but two are depicted for generality), and an output layer that produces a 4-length vector of Q values for each action, given the state.

```
Deep Q-network
```

![](0__page_12_Figure_2.jpeg)

Figure 3.9 String diagram for our DQN. The input is a 64-length Boolean vector, and the output is a 4-length real vector of Q values.

To implement this with PyTorch, we'll use the nn module, which is the higher-level interface for PyTorch, similar to Keras for TensorFlow.

```
import numpy as np
import torch
from Gridworld import Gridworld
import random
from matplotlib import pylab as plt
11 = 6412 = 150l3 = 100
14 = 4model = torch.nn.Sequential(
    torch.nn.Linear(l1, l2),
     torch.nn.ReLU(),
     torch.nn.Linear(l2, l3),
     torch.nn.ReLU(),
     torch.nn.Linear(l3,l4)
)
loss_fn = torch.nn.MSELoss()
learning_rate = 1e-3
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
qamma = 0.9epsilon = 1.0
  Listing 3.2 Neural network Q function
```

So far, all we've done is set up the neural network model, define a loss function and learning rate, set up an optimizer, and define a couple of parameters. If this were a simple classification neural network, we'd almost be done. We'd just need to set up a for loop to iteratively run the optimizer to minimize the model error with respect to the data. It's more complicated with reinforcement learning, which is probably why you're reading this book. We covered the main steps well earlier, but let's zoom in a little.

 Listing 3.3 implements the main loop of the algorithm. In broad strokes, this is what it does:

- <sup>1</sup> We set up a for loop for the number of epochs.
- 2 In the loop, we set up a while loop (while the game is in progress).
- <sup>3</sup> We run the Q-network forward.
- 4 We're using an epsilon-greedy implementation, so at time *t* with probability  $\varepsilon$ we will choose a random action. With probability  $1 - \varepsilon$ , we will choose the action associated with the highest Q value from our neural network.
- <sup>5</sup> Take action *a* as determined in the preceding step, and observe the new state s′ and reward  $r_{t+1}$ .
- <sup>6</sup> Run the network forward using s′. Store the highest Q value, which we'll call max Q.
- 7 Our target value for training the network is  $r_{t+1} + \gamma \cdot \max Q_A(S_{t+1}),$  where  $\gamma$ (gamma) is a parameter between 0 and 1. If after taking action  $a_t$  the game is over, there is no legitimate  $s_{t+1}$ , so  $\gamma$ \*max $Q_A(S_{t+1})$  is not valid and we can set it to 0. The target becomes just  $r_{t+1}$ .
- <sup>8</sup> Given that we have four outputs and we only want to update (i.e., train) the output associated with the action we just took, our target output vector is the same as the output vector from the first run, except we change the one output associated with our action to the result we computed using the Q-learning formula.
- **9** Train the model on this one sample. Then repeat steps 2–9.

To be clear, when we first run our neural network and get an output of action values like this,

```
array([[-0.02812552, -0.04649779, -0.08819015, -0.00723661]])
```

our target vector for one iteration may look like this:

```
array([[-0.02812552, -0.04649779, 1, -0.00723661]])
```

Here we just changed a single entry to the value we wanted to update.

 There's one other detail we need to include in the code before we move on. The Gridworld game engine's makeMove method expects a character such as *u* to make a move, but our Q-learning algorithm only knows how to generate numbers, so we need a simple map from numeric keys to action characters:

```
action_set = \{ 0: 'u',
   1: 'd',2: 'l', 3: 'r',
}
```

Okay, let's get to coding the main training loop.

![](0__page_14_Figure_1.jpeg)

![](0__page_14_Figure_2.jpeg)

learning the abstract features of the data, ultimately preventing it from generalizing to new data.

There are a couple of things to point out that you may not have seen before. The first new thing is the use of the context torch.no\_grad() when computing the next state Q value. Whenever we run a PyTorch model with some input, it will implicitly create a computational graph. Each PyTorch tensor is not only a store of tensor data, it also keeps track of which computations were performed to produce it. By using the torch.no\_grad() context, we tell PyTorch to *not* create a computational graph for the code within the context; this will save memory when we don't need the computational graph. When we compute the Q values for state2, we're just using them as a target for training. We're not going to backpropagate through the computational graph that would have been created if we hadn't used torch.no\_grad. We only want to backpropagate through the computational graph that is created when we call model (state1), because we want to train the parameters with respect to state1, not state2.

Here's a simple example with a linear model:

```
>>> m = torch.Tensor([2.0])
>>> m.requires_grad=True
>>> b = torch.Tensor([1.0])
>>> b.requires_grad=True
>>> def linear model(x,m,b):
>>> y = m @ x + b>>> return y
\Rightarrow y = 1inear model(torch.Tensor([4.]), m,b)
>>> y
tensor([9.], grad_fn=<AddBackward0>)
>>> y.grad_fn
<AddBackward0 at 0x128dfb828>
>>> with torch.no qrad():
>>> y = linear model(torch.Tensor([4]),m,b)
>>> y
tensor([9.])
>>> y.grad_fn
None
```

We create two trainable parameters, m and b, by setting their requires grad attribute to True, which means PyTorch will consider these parameters as nodes in a computational graph and will store their history of computations. Any new tensors that are created using m and b, such as y in this case, will also have requires\_grad set to True and thus will also keep a memory of their computation history. You can see that the first time we call the linear model and print y, it gives us a tensor with the numeric result and also shows an attribute, grad\_fn=<AddBackward0>. We can also see this attribute directly by printing  $y$ . grad  $fn$ . This shows that this tensor was created by the addition operation. It is called AddBackward because it actually stores the derivative of the addition function.

 If you call this function given one input, it returns two outputs, like the opposite of addition, which takes two inputs and returns one output. Since our addition function

is a function of two variables, there is a partial derivative with respect to the first input and a partial derivative with respect to the second input. The partial derivative of  $y = a + b$  with respect to *m* is  $\frac{\partial y}{\partial a} = 1$  and  $\frac{\partial y}{\partial b} = 1$ . Or if  $y = a \cdot b$  then  $\frac{\partial y}{\partial a} = b$  and  $\frac{\partial y}{\partial b} = a$ . These are just the basic rules of taking derivatives. When we backpropagate from a given node, we need it to return all the partial derivatives, so that is why the AddBackward0 gradient function returns two outputs.  $\frac{\partial y}{\partial a} = 1$  and  $\frac{\partial y}{\partial b} = 1$ . Or if  $y = a \cdot b$  then  $\frac{\partial y}{\partial a} = b$  and  $\frac{\partial y}{\partial b} = a$ 

 We can verify that PyTorch is indeed computing gradients as expected by calling the backward method on y:

```
\Rightarrow y = 1inear model(torch.Tensor([4.]), m,b)
>>> y.backward()
>>> m.grad
tensor([4.])
>>> b.grad
tensor([1.])
```

This is exactly what we would get from computing these simple partial derivatives in our head or on paper. In order to backpropagate efficiently, PyTorch keeps track of all forward computations and stores their derivatives so that eventually when we call the backward() method on the output node of our computational graph, it will backpropagate through these gradient functions node by node until the input node. That's how we get the gradients for all the parameters in the model.

Notice that we also called the detach() method on the  $Y$  tensor. This was actually unnecessary, since we used torch.no qrad() when we computed newQ, but we included it because detaching nodes from the computational graph will become ubiquitous throughout the rest of the book, and not properly detaching nodes is a common source of bugs when training a model. If we call loss backward  $(X, Y)$ , and Y was associated with its own computational graph with trainable parameters, we would backpropagate into Y *and* X, and the training procedure would learn to minimize the loss by updating the trainable parameters in the X graph and the Y graph, whereas we only want to update the X graph. We *detach* the Y node from the graph so that it is just used as data and not as a computational graph node. You don't need to think too hard about the details, but you do need to pay attention to which parts of the graph you're actually backpropagating into and make sure you're not backpropagating into the wrong nodes.

 You can go ahead and run the training loop—1,000 epochs will be more than enough. Once it's done, you can plot the losses to see if the training is successful and the model converges. The loss should more or less decrease and plateau over the training time. Our plot is shown in figure 3.10.

 The loss plot is pretty noisy, but the moving average of the plot is significantly trending toward zero. This gives us some confidence the training worked, but we'll never know until we test it. We've written up a simple function in listing 3.4 that allows us to test the model on a single game.

![](0__page_17_Figure_1.jpeg)

Figure 3.10 The loss plot for our first Q-learning algorithm, which is clearly down-trending over the training epochs.

## Listing 3.4 Testing the Q-network

```
def test model(model, mode='static', display=True):
    i = 0test game = Gridworld(mode=mode)
    state = test game.board.render np().reshape(1,64) +
     np.random.rand(1,64)/10.0
    state = torch.from numpy(state).float()
     if display:
         print("Initial State:")
         print(test_game.display())
     status = 1
    while(status == 1):
         qval = model(state)
         qval_ = qval.data.numpy()
         action_ = np.argmax(qval_) 
        action = action set[action ]
         if display:
             print('Move #: %s; Taking action: %s' % (i, action))
         test_game.makeMove(action)
        state = test game.board.render np().reshape(1,64) +
     np.random.rand(1,64)/10.0
        state = torch.from numpy(state).float()
         if display:
                                         While the game is 
                                         still in progress
                                            Takes the action with 
                                            the highest Q value
```
```
 print(test_game.display())
     reward = test_game.reward()
     if reward != -1:
         if reward > 0:
             status = 2
             if display:
                 print("Game won! Reward: %s" % (reward,))
         else:
             status = 0
             if display:
                 print("Game LOST. Reward: %s" % (reward,))
    i + = 1 if (i > 15):
         if display:
             print("Game lost; too many moves.")
         break
 win = True if status == 2 else False
 return win
```

The test function is essentially the same as the code in our training loop, except we don't do any loss calculation or backpropagation. We just run the network forward to get the predictions. Let's see if it learned how to play Gridworld!

```
>>> test_model(model, 'static')
Initial State:
\left[\begin{array}{cccccccccccccc} \left[ \begin{array}{cccccccccccccc} 1 & + & 1 & - & 1 & - & 1 & - & 1 & - & 1 & - & 1 & 1 \end{array}\right] \end{array}\right][ [ \cdot \cdot \cdot \cdot \cdot \cdot \cdot \cdot [' ' ' ' ' ' ' ']
    [' ' ' ' ' ' ' ']]
Move #: 0; Taking action: d
[['+' '-' ' ' ' ']
  \begin{bmatrix} 1 & 1 & 1 \end{bmatrix} \begin{bmatrix} W^T & 1 & 1 \end{bmatrix} \begin{bmatrix} 1 & 1 \end{bmatrix} \begin{bmatrix} P^T \end{bmatrix} [' ' ' ' ' ' ' ']
    [' ' ' ' ' ' ' ']]
Move #: 1; Taking action: d
\left[\begin{array}{cccccccccc} 1 & + & 1 & -1 & -1 & -1 & -1 & -1 \end{array}\right][ [ \cdot \cdot \cdot \cdot \cdot \cdot \cdot \cdot\begin{bmatrix} 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1\\ 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1\\ 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1\\ 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1\\ 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1\\ 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1\\ 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1\\ 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 &  [' ' ' ' ' ' ' ']]
Move #: 2; Taking action: l
[['+' '-' ' ' ' ']
   \left[\begin{array}{cccccccccccccc} 1 & 1 & 1 & W & 1 & 1 & 1 & 1 & 1 \end{array}\right][ [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]  [' ' ' ' ' ' ' ']]
Move #: 3; Taking action: l
[ [ ' + ' ' ' - ' ' ' '' '' '' '' '' ''[ [ [ ] [ [ ] [ [ ] [ [ ] [ [ ] [ ] [ [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] \left[\begin{array}{cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc [' ' ' ' ' ' ' ']]
Move #: 4; Taking action: l
[ [ ] [ ] + ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] \left[\begin{array}{cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc ['P' ' ' ' ' ' ']
    [' ' ' ' ' ' ' ']]
```

```
Move #: 5; Taking action: u
 [ [ ] [ ] + ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] \left[\begin{array}{cccccccccc} \top\mathbf{P} & \top & \top\mathbf{W} & \top & \top & \top & \top & \top \end{array}\right] [' ' ' ' ' ' ' ']
      [' ' ' ' ' ' ' ']]
Move #: 6; Taking action: u
 \left[\begin{array}{cccccccccc} 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 \\ 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 \\ 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 \\ 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 \\ 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 \\ 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 \\ 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 \\ 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 \\ 1 & 1 & 1 & 1 & 1[ [ [ [ ] [ [ ] [ [ ] [ [ ] [ [ ] [ [ ] [ ] [ [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [1 - 1 - 1 - 1 - 1 - 1 - 1 - 1][ [ \cdot ] [ \cdot ] [ \cdot ] [ \cdot \cdot \cdot \cdot \cdot \cdot \cdot \cdotReward: 10
```

Can we get a round of applause for our Gridworld player here? Clearly it knows what it's doing; it went straight for the goal!

 But let's not get too excited; that was the static version of the game, which is really easy. If you use our test function with mode='random', you'll find some disappointment:

```
>>> testModel(model, 'random')
Initial State:
 [ [ [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ [ [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]  [' ' ' ' ' ' ' ']
     [' ' ' ' '-' ' ']]
Move #: 0; Taking action: d
 [ [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] \left[\begin{array}{cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc [' ' ' ' ' ' ' ']
    [ [ \vdots \vdots \vdots \vdots \vdots \vdots \vdots \vdots \vdots \vdotsMove #: 1; Taking action: d
 [ [ [ ] [ ] [ ] [ ] [ [ ] [ [ ] [ ] [ [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ' \cdots W' ' ' ' ' ' '
    \left[\begin{array}{cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc[ [ \vdots \vdots \vdots \vdots \vdots \vdots \vdots \vdots \vdotsMove #: 2; Taking action: l
 [[' ' '+' ' ' ' ']
    \left[\begin{array}{cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc[ [ \cdot ] [ \cdot ] [ \cdot ] [ \cdot \cdot ] [ \cdot \cdot ] [ [' ' ' ' '-' ' ']]
Move #: 3; Taking action: l
 [[' ' '+' ' ' ' ']
  [ ' ' \vee ' W' ' ' ' ' ' ' ' ' ' '
   \left[ \begin{array}{cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc[ [ \vdots \vdots \vdots \vdots \vdots \vdots \vdots \vdots \vdots \vdotsMove #: 4; Taking action: l
 \left[\begin{array}{cccccccccccccc} 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1\end{array}\right]\left[\begin{array}{cccccccccccccc} 1 & 1 & 1 & W & 1 & 1 & 1 & 1 & 1 \end{array}\right]\begin{bmatrix} 1 & P^T & 1 & P & P & P & P & P & P \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 &[ [ \vdots \vdots \vdots \vdots \vdots \vdots \vdots \vdots \vdots \vdotsMove #: 5; Taking action: u
 [ [ [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ \left[\begin{array}{cccccccccccccc} \mathbf{1} & \mathbf{P} & \mathbf{1} & \cdots & \mathbf{W} & \mathbf{1} & \cdots & \mathbf{1} & \cdots & \mathbf{1} & \cdots & \mathbf{1} \end{array}\right] [' ' ' ' ' ' ' ']
     [' ' ' ' '-' ' ']]
```

```
Move #: 6; Taking action: u
 [ [ \{ ' ] [ \{ ] [ \{ ] \{ \} \{ \} \{ \} \{ \} \{ \{ \} \{ \} \{ \} \{ \} \{ \{ \} \{ \} \{ \} \{ \{ \} \{ \} \{ \{ \} \{ \} \{ [ [ [ ] [ [ ] [ [ ] [ [ ] [ [ ] [ ] [ [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]  [' ' ' ' ' ' ' ']
     \left[\begin{array}{cccccccccccccc} 1 & 1 & 1 & 1 & 1 & 1 & -1 & 1 & 1 & 1 & 1 \\ 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 \\ 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 \\ 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 \\ 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 \\ 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 \\ 1 & 1 & 1 & 1 & 1 & Move #: 7; Taking action: d
 [ [ [ ] [ ] [ ] [ ] [ [ ] [ [ ] [ [ ] [ ] [ [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ [\begin{array}{ccccccccccccc} \cdot & \cdot & \cdot & \cdot & \cdot & \cdot & \cdot & \cdot & \cdot & \cdot & \cdot & \cdot & \cdot & \[ [ \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots[ [ \cdot ] \cdot [ \cdot ] \cdot [ \cdot \cdot \cdot \cdot \cdot \cdot \cdot \cdot# we omitted the last several moves to save space
Game lost; too many moves.
```

This is really interesting. Look carefully at the moves the network is making. The player starts off the game only two tiles to the right of the goal. If it *really* knew how to play the game, it would take the shortest path to the goal. Instead, it starts moving down and to the left, just like it would in the static game mode. It seems like the model just memorized the particular board it was trained on and didn't generalize at all.

 Maybe we just need to train it with the game mode set to random, and then it would really learn? Try it. Retrain it with random mode. Maybe you'll be luckier than us, but figure 3.11 shows our loss plot with random mode and 1,000 epochs. That

![](1__page_20_Figure_4.jpeg)

Figure 3.11 The loss plot for Q-learning in random mode, which doesn't show any signs of convergence.

doesn't look pretty. There's no sign that any significant learning is happening with random mode. (We won't show these results, but the model *did* seem to learn how to play with "player" mode, where only the player is randomly placed on the grid.)

 This is a big problem. Reinforcement learning won't be worth anything if all it can do is learn how to memorize or weakly learn. But this is a problem that the DeepMind team faced, and one they solved.

## *3.3 Preventing catastrophic forgetting: Experience replay*

We're slowly building up our skills, and we want our algorithm to train on the harder variant of the game where all the board pieces are randomly placed on the grid for each new game. The algorithm can't just memorize a sequence of steps to take, as before. It needs to be able to take the shortest path to the goal (without stepping into the pit) regardless of what the initial board configuration is. It needs to develop a more sophisticated representation of its environment.

## *3.3.1 Catastrophic forgetting*

The main problem we encountered in the previous section when we tried to train our model on random mode has a name: *catastrophic forgetting*. It's actually a very important issue associated with gradient descent-based training methods in *online* training. Online training is what we've been doing: we backpropagate after each move as we play the game.

 Imagine that our algorithm is training on (learning Q values for) game 1 of figure 3.12. The player is placed between the pit and the goal such that the goal is on the right and the pit is on the left. Using an epsilon-greedy strategy, the player takes a random move and by chance steps to the right and hits the goal. Great! The algorithm will try to learn that this state-action pair is associated with a high value by updating its weights in such a way that the output will more closely match the target value (i.e. via backpropagation).

 Now game 2 is initialized and the player is again between the goal and pit, but this time the goal is on the *left* and the pit is on the right. Perhaps to our naive algorithm, the state *seems* very similar to the last game. Since last time moving right gave a nice positive reward, the player chooses to make one step to the right again, but this time it ends up in the pit and gets –1 reward. The player is thinking, "What is going on? I thought going to the right was the best decision based on my previous experience." It may do backpropagation again to update its state-action value, but because this state-action is very similar to the last learned state-action, it may override its previously learned weights.

 This is the essence of catastrophic forgetting. There's a push-pull between very similar state-actions (but with divergent targets) that results in this inability to properly learn anything. We generally don't have this problem in the supervised learning realm, because we do randomized batch learning where we don't update our weights until we've iterated through some random subset of training data and computed the sum or average gradient for the batch. This averages over the targets and stabilizes the learning.

![](1__page_22_Figure_1.jpeg)

Figure 3.12 The idea of catastrophic forgetting is that when two game states are very similar and yet lead to very different outcomes, the Q function will get "confused" and won't be able to learn what to do. In this example, the catastrophic forgetting happens because the Q function learns from game 1 that moving right leads to a +1 reward, but in game 2, which looks very similar, it gets a reward of –1 after moving right. As a result, the algorithm forgets what it previously learned about game 1, resulting in essentially no significant learning at all.

## *3.3.2 Experience replay*

Catastrophic forgetting is probably not something we have to worry about with the first variant of our game because the targets are always stationary, and indeed the model successfully learned how to play it. But with the random mode, it's something we need to consider, and that is why we need to implement something called *experience replay*. Experience replay basically gives us batch updating in an online learning scheme. It's not a big deal to implement

Here's how experience replay works (figure 3.13):

- **1** In state *s*, take action *a*, and observe the new state  $s_{t+1}$  and reward  $r_{t+1}$ .
- 2 Store this as a tuple  $(s, a, s_{t+1}, r_{t+1})$  in a list.
- <sup>3</sup> Continue to store each experience in this list until you have filled the list to a specific length (this is up to you to define).
- <sup>4</sup> Once the experience replay memory is filled, randomly select a subset (again, you need to define the subset size).
- <sup>5</sup> Iterate through this subset and calculate value updates for each subset; store these in a target array (such as *Y*) and store the state, *s*, of each memory in *X*.

<sup>6</sup> Use *X* and *Y* as a mini-batch for batch training. For subsequent epochs where the array is full, just overwrite old values in your experience replay memory array.

![](1__page_23_Figure_2.jpeg)

Figure 3.13 This is the general overview of experience replay, a method for mitigating a major problem with online training algorithms: catastrophic forgetting. The idea is to employ mini-batching by storing past experiences and then using a random subset of these experiences to update the Q-network, rather than using just the single most recent experience.

Thus, in addition to learning the action value for the action you just took, you're also going to use a random sample of past experiences to train on, to prevent catastrophic forgetting.

 Listing 3.5 shows the same training algorithm from listing 3.4, except with experience replay added. Remember, this time we're training it on the harder variant of the game, where all the board pieces are randomly placed on the grid.

![](1__page_23_Figure_6.jpeg)

```
qval = qval.data.numpy() if (random.random() < epsilon): 
                            action = np.random.randn(), 4)
                        else:
                            action = np.argmax(qval)
                        action = action_set[action_]
                        game.makeMove(action)
                       state2 = qame.board.render np().reshape(1,64) +
                    np.random.rand(1,64)/100.0
                       state2 = torch.from numpy(state2).float()
                       reward = game.reward()\frac{1}{100} done = True if reward > 0 else False
        Adds the \vert exp = (state1, action, reward, state2, done) \rightarrow the next state as a tuple
                        replay.append(exp) 
                        state1 = state2
       replay list
                        if len(replay) > batch_size: 
                             minibatch = random.sample(replay, batch_size) 
                         \triangleright state1_batch = torch.cat([s1 for (s1, a, r, s2, d) in minibatch])
                            action batch = torch.Tensor([a for (s1,a,r,s2,d) in minibatch])
                            reward batch = torch.Tensor([r for (s1,a,r,s2,d) in minibatch])
                            state2 batch = torch.cat([s2 for (s1,a,r,s2,d) in minibatch])
                            done batch = torch.Tensor([d for (s1,a,r,s2,d) in minibatch])

components of each
                             Q1 = model(state1_batch) 
                            with torch.no qrad():
                                  Q2 = model(state2_batch) 
                            Y = reward batch + gamma * ((1 - done batch) *
 Computes the \begin{array}{ccc}\n\hline\n\downarrow\downarrow\downarrow\downarrow\downarrow\downarrow\downarrow\downarrow\downarrow\downarrow\downarrow\downarrow\downarrow\X = \setminus Q1.gather(dim=1,index=action_batch.long().unsqueeze(dim=1)).squeeze()
                            loss = loss fm(X, Y.detach()) optimizer.zero_grad()
                             loss.backward()
                             losses.append(loss.item())
                             optimizer.step()
                       if reward != -1 or mov > max moves:
                             status = 0
                            mov = 0losses = np.array(losses)
                                                                          Selects an action using the 
                                                                          epsilon-greedy strategy
                                                                                        Creates an experience of 
                                                                                        state, reward, action, and 
    experience to
  the experience
                                                                                   replay list If the replay list is at least as 
                                                                                   long as the mini-batch size, 
                                                                                   begins the mini-batch training
         Randomly
         samples a
      subset of the
         replay list
     Separates out the
       experience into
   separate mini-batch
              tensors
                                                                       Recomputes Q values for the mini-
                                                                      batch of states to get gradients
                                                                                       Computes Q values for the 
                                                                                       mini-batch of next states, 
                                                                                       but doesn't compute 
target Q values
  we want the
 DQN to learn
                                                                            If the game is over, 
                                                                            resets status and 
                                                                            mov number
```

In order to store the agent's experiences, we used a data structure called a *deque* in Python's built-in collections library. It's basically a list that you can set a maximum size on, so that if you try to append to the list and it is already full, it will remove the first item in the list and add the new item to the end of the list. This means new experiences replace the oldest experiences. The experiences themselves are tuples of (state1, reward, action, state2, done) that we append to the replay deque.

 The major difference with experience replay training is that we train with minibatches of data when our replay list is full. We randomly select a subset of experiences

from the replay, and we separate out the individual experience components into state1\_batch, reward\_batch, action\_batch, and state2\_batch. For example, state1 batch is of dimensions batch size  $\times$  64, or  $100 \times 64$  in this case. And reward batch is just a 100-length vector of integers. We follow the same training formula as we did earlier with fully online training, but now we're dealing with mini-batches. We use the tensor gather method to subset the Q1 tensor (a  $100 \times 4$  tensor) by the action indices so that we only select the Q values associated with actions that were actually chosen, resulting in a 100-length vector.

Notice that the target Q value, Y = reward batch + gamma \* ((1 - done batch) \* torch.max( $Q2$ , dim=1)[0]), uses done batch to set the right side to 0 if the game is done. Remember, if the game is over after taking an action, which we call a *terminal state*, there is no next state to take the maximum Q value on, so the target just becomes the reward,  $r_{t+1}$ . The done variable is a Boolean, but we can do arithmetic on it as if it were a  $0$  or  $1$  integer, so we just take  $1$  - done so that if done = True,  $1$  - done = 0, and it sets the right-side term to 0.

We trained for 5,000 epochs this time, since it's a more difficult game, but otherwise the Q-network model is the same as before. When we test the algorithm, it seems to play most of the games correctly. We wrote an additional testing script to see what percentage of games it wins out of 1,000 plays.

```
Listing 3.6 Testing the performance with experience replay
```

```
max qames = 1000
wins = 0
for i in range(max_games):
    win = test model(model, mode='random', display=False)
     if win:
       wins += 1win perc = float(wins) / float(max games)
print("Games played: \{0\}, # of wins: \{1\}".format(max games,wins))
print("Win percentage: {}".format(win perc))
```

When we run listing 3.6 on our trained model (trained for 5,000 epochs), we get about 90% accuracy. Your accuracy may be slightly better or worse. This certainly suggests it has learned *something* about how to play the game, but it's not exactly what we would expect if the algorithm really knew what it was doing (although you could probably improve the accuracy with a much longer training time). Once you actually know how to play, you should be able to win every single game.

 There's a small caveat that some of the initialized games may actually be impossible to win, so the win percentage may never reach 100%; there is no logic preventing the goal from being in the corner, stuck behind a wall and pit, making the game unwinnable. The Gridworld game engine does prevent most of the impossible board configurations, but a small number can still get through. Not only does this mean we can't win every game, but it also means the learning will be mildly corrupted, since it will attempt to follow a strategy that normally would work but fails for an unwinnable

game. We wanted to keep the game logic simple to focus on illustrating the concepts so we did not program in the sophisticated logic needed to ensure 100% winnable games.

 There's also another reason we're being held back from getting into the 95% + accuracy territory. Let's look at our loss plot, shown in figure 3.14 showing our running average loss (yours may vary significantly).

![](1__page_26_Figure_3.jpeg)

Figure 3.14 The DQN loss plot after implementing experience replay, which shows a clearly downtrending loss, but it's still very noisy.

In the loss in figure 3.14, you can see it's definitely trending downward, but it looks pretty unstable. This is the type of plot you'd be a bit surprised to see in a supervised learning problem, but it's quite common in bare DRL. The experience replay mechanism helps with training stabilization by reducing catastrophic forgetting, but there are other related sources of instability.

## *3.4 Improving stability with a target network*

So far, we've been able to successfully train a deep reinforcement learning algorithm to learn and play Gridworld with both a deterministic static initialization and a slightly harder version where the player is placed randomly on the board each game. Unfortunately, even though the algorithm appears to learn how to play, it is quite possible it is just memorizing all the possible board configurations, since there aren't that many on
a 4 × 4 board. The hardest variant of the game is where the player, goal, pit, and wall are all initialized randomly each game, making it much more difficult for the algorithm to memorize. This ought to enforce some amount of actual learning, but as you saw, we're still experiencing difficulty with learning this variant; we're getting very noisy loss plots. To help address this, we'll add another dimension to the updating rule that will smooth out the value updates.

# *3.4.1 Learning instability*

One potential problem that DeepMind identified when they published their deep Qnetwork paper was that if you keep updating the Q-network's parameters after each move, you might cause instabilities to arise. The idea is that since the rewards may be sparse (we only give a significant reward upon winning or losing the game), updating on every single step, where most steps don't get any significant reward, may cause the algorithm to start behaving erratically.

 For example, the Q-network might predict a high value for the "up" action in some state; if it moves up and by chance lands on the goal and wins, we update the Q-network to reflect the fact that it was rewarded +10. The next game, however, it thinks "up" is a really fantastic move and predicts a high Q value, but then it moves up and gets a  $-10$ reward, so we update and now it thinks "up" is not so great after all. Then, a few games later moving up leads to winning again. You can see how this might lead to a kind of oscillatory behavior, where the predicted Q value never settles on a reasonable value but just keeps getting jerked around. This is very similar to the catastrophic forgetting problem.

 This is not just a theoretical issue—it's something that DeepMind observed in their own training. The solution they devised is to duplicate the Q-network into two copies, each with its own model parameters: the "regular" Q-network and a copy called the *target network* (symbolically denoted Q-network, read "Q hat"). The target network is identical to the Q-network at the beginning, before any training, but its own parameters lag behind the regular Q-network in terms of how they're updated.

 Let's run through the sequence of events again, with the target network in play (we'll leave out the details of experience replay):

- **1** Initialize the Q-network with parameters (weights)  $\theta_Q$  (read "theta Q").
- <sup>2</sup> Initialize the target network as a copy of the Q-network, but with separate parameters  $\theta_T$  (read "theta T"), and set  $\theta_T = \theta_Q$ .
- <sup>3</sup> Use the epsilon-greedy strategy with the Q-network's Q values to select action *a*.
- 4 Observe the reward and new state  $r_{t+1}, s_{t+1}$ .
- 5 The target network's Q value will be set to  $r_{t+1}$  if the episode has just been terminated (i.e., the game was won or lost) or to  $r_{t+1} + \gamma \text{max} Q_{\theta_r}(S_{t+1})$  otherwise (notice the use of the target network here).
- <sup>6</sup> Backpropagate the target network's Q value through the Q-network (not the target network).
- 7 Every *C* number of iterations, set  $\theta_T = \theta_0$  (i.e., set the target network's parameters equal to the Q-network's parameters).

Notice from figure 3.15 that the only time we use the target network,  $\hat{Q}$ , is to calculate the target Q value for backpropagation through the Q-network. The idea is that we update the main Q-network's parameters on each training iteration, but we decrease the effect that recent updates have on the action selection, hopefully improving stability.

![](2__page_28_Figure_2.jpeg)

Figure 3.15 This is the general overview for Q-learning with a target network. It's a fairly straightforward extension of the normal Q-learning algorithm, except that you have a second Q-network called the target network whose predicted Q values are used to backpropagate through and train the main Q-network. The target network's parameters are not trained, but they are periodically synchronized with the Q-network's parameters. The idea is that using the target network's Q values to train the Q-network will improve the stability of the training.

The code is getting a bit long now, with both experience replay and a target network, so we'll just look at a portion of the full code here in the book. We'll leave it to you to check out the book's GitHub repository where you'll find all the code for this chapter.

 The following code is identical to listing 3.5 except for a few lines that add in the target network capability.

![](2__page_28_Figure_6.jpeg)

```
sync freq = 50loss fn = torch.nn.MSELoss()
learning_rate = 1e-3
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
                                          Synchronizes the frequency parameter; 
                                          every 50 steps we will copy the 
                                          parameters of model into model2
                                  (Code omitted) Uses the same 
                                  other settings as in listing 3.5
```

The target network is simply a lagged copy of the main DQN. Each PyTorch model has a state dict() method that returns all of its parameters organized in a dictionary. We use Python's built-in copy module to duplicate the PyTorch model data structure, and then we use the load state dict method on model2 to ensure that it has copied the parameters of the main DQN.

 Next we include the full training loop, which is mostly the same as listing 3.5 except that we use model2 when computing the maximum Q value for the next state. We also include a couple of lines of code to copy the parameters from the main model to model2 every 50 iterations.

#### Listing 3.8 DQN with experience replay and target network

```
from collections import deque
epochs = 5000losses = []
mem size = 1000batch size = 200replay = deque(maxlen=mem_size)
max moves = 50
h = 0sync_freq = 500 
\dot{\tau}=0for i in range(epochs):
     game = Gridworld(size=4, mode='random')
    state1 = game.board.render np().reshape(1,64) +
     np.random.rand(1,64)/100.0
    state1 = torch.from numpy(state1).float()
    status = 1mov = 0while(status == 1):
        1 + 1mov += 1 qval = model(state1)
        qval = qval.data.numpy() if (random.random() < epsilon):
            action = np.random.randnint(0,4) else:
            action = np.argmax(qval)
        action = action set[action ]
         game.makeMove(action)
        state2 = game.board.render np().reshape(1,64) +
     np.random.rand(1,64)/100.0
                                   Sets the update frequency 
                                    for synchronizing the 
                                    target model parameters 
                                  to the main DQN
```

```
state2 = torch.from numpy(state2 ).float()
         reward = game.reward()
         done = True if reward > 0 else False
         exp = (state1, action_, reward, state2, done)
         replay.append(exp) 
         state1 = state2
        if len(replay) > batch size:
             minibatch = random.sample(replay, batch_size)
            state1 batch = torch.cat([s1 for (s1, a, r, s2, d) in minibatch])
            action batch = torch.Tensor([a for (s1,a,r,s2,d) in minibatch])
            reward batch = torch.Tensor([r \text{ for } (s1,a,r,s2,d) \text{ in } minbatch])
            state2 batch = torch.cat([s2 for (s1,a,r,s2,d) in minibatch])
            done batch = torch.Tensor([d for (s1,a,r,s2,d) in minibatch])
             Q1 = model(state1_batch) 
            with torch.no qrad():
                  Q2 = model2(state2_batch) 
            Y = reward batch + gamma * ((1-done batch) * \
             torch.max(Q2,dim=1)[0])
            X = Q1.gether(dim=1,index=action_batch.log() \ \ \ \ \ .unsqueeze(dim=1)).squeeze()
            loss = loss fin(X, Y. detach()) print(i, loss.item())
             clear_output(wait=True)
             optimizer.zero_grad()
             loss.backward()
             losses.append(loss.item())
             optimizer.step()
            if j \text{ }} sync freq == 0:
                 model2.load_state_dict(model.state_dict())
         if reward != -1 or mov > max_moves:
            status = 0mov = 0losses = np.array(losses)
                                                             Uses the target network 
                                                             to get the maximum Q 
                                                             value for the next state
                                                  Copies the main 
                                                   model parameters to 
                                                   the target network
```

When we plot the loss for a target network approach with experience replay (figure 3.16), we still get a noisy loss plot, but it is significantly less noisy and clearly downtrending. You should try to experiment with the hyperparameters, such as the experience replay buffer size, the batch size, the target network update frequency, and the learning rate. The performance can be quite sensitive to these hyperparameters.

When we test the trained model on 1,000 games, we get about a 3% improvement in win percentage compared to training without a target network. We're getting a top accuracy of around 95%, which we think is probably the maximal accuracy given the limitations of this environment (i.e., the possibility of unwinnable states). We're only training up to 5,000 epochs, where each epoch is a single game. The number of possible game configurations (the size of the state-space) is approximately  $16 \cdot 15 \cdot 14 \cdot 13 =$ 43,680 (since there are 16 possible positions the agent can be in on a  $4 \times 4$  grid, and

![](2__page_31_Figure_1.jpeg)

Figure 3.16 The DQN loss plot after including a target network to stabilize training. This shows a much faster training convergence than without the target network, but it has noticeable spikes of error when the target network synchronizes with the main DQN.

then 15 possible configurations for the wall, since the agent and wall can't be overlapping in space, etc.), so we're only sampling about  $\frac{5,000}{43,680} = 0.11 = 11\%$  of the total number of possible starting game states. If the model can successfully play games it has never seen before, then we have some confidence it has generalized. If you're getting good results with the  $4 \times 4$  board, you should try training an agent to play on  $a$  5  $\times$  5 board or larger by changing the size parameter when creating the Gridworld game instance:

```
>>> game = Gridworld(size=6, mode='random')
>>> game.display()
\begin{array}{l} \arg\left(\left[\begin{array}{ccc} \{1,1\} & 1 \end{array}\right], \begin{array}{ccc} 1 & 1 \end{array}\right], \begin{array}{ccc} 1 & 1 \end{array}\right], \begin{array}{ccc} 1 & 1 \end{array}\right], \begin{array}{ccc} 1 & 1 \end{array}\right], \\ \left[\begin{array}{ccc} 1 & 1 \end{array}\right], \begin{array}{ccc} 1 & 1 \end{array}\right], \begin{array}{ccc} 1 & 1 \end{array}\right], \end{array} [' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', 'W', ' ', ' ', ' '],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1[ ' ', ' ', ' ', ' ', 'P', ''],
                  [ ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' ], dtype='<U2')
```

### DeepMind's deep Q-network

Believe it or not, but in this chapter we basically built the deep Q-network (DQN) that DeepMind introduced in 2015 and that learned to play old Atari games at superhuman performance levels. DeepMind's DQN used an epsilon-greedy action-selection strategy, experience replay, and a target network. Of course, the details of our implementation are different, since we are playing a custom Gridworld game and DeepMind was training on raw pixels from real video games. For example, one difference worth noting is that they actually input the last 4 frames of a game into their Q-network. That's because a single frame in a video game is not enough information to determine the speed and direction of the objects in the game, which is important when deciding what action to take.

You can read more about the specifics of DeepMind's DQN by searching for their paper "Human-level control through deep reinforcement learning." One thing to note is that they used a neural network architecture consisting of two convolutional layers followed by two fully connected layers. In our case we used three fully connected layers. It would be a worthwhile experiment to build a model with a convolutional layer, and try training it with Gridworld. One huge advantage of convolutional layers is that they are independent of the size of the input tensor. When we used a fully connected layer, for example, we had to make the first dimension 64—we used a  $64 \times 164$  parameter matrix for the first layer. A convolutional layer, however, can be applied to input data of any length. This would allow you to train a model on a  $4 \times 4$  grid and see if it generalizes enough to be able to play on a  $5 \times 5$  or bigger grid. Go ahead, try it!

# *3.5 Review*

We've covered a lot in this chapter, and once again we've smuggled in a lot of fundamental reinforcement learning concepts. We could have pushed a bunch of academic definitions in your face to start, but we resisted the temptation and decided to get to coding as quickly as possible. Let's review what we've accomplished and fill in a few terminological gaps.

 In this chapter we covered a particular RL algorithm called Q-learning. Q-learning has nothing to do with deep learning or neural networks on its own; it is an abstract mathematical construct. Q-learning refers to solving a control task by learning a function called a  $Q$  function. You give the  $Q$  function a state (e.g., a game state) and it predicts how valuable all the possible actions are that you could take given the input state, and we call these value predictions Q values. You decide what to do with these Q values. You might decide to take the action that corresponds to the highest Q value (a greedy approach), or you might opt for a more sophisticated selection process. As you learned in chapter 2, you have to balance exploration (trying new things) versus exploitation (taking the best action you know of). In this chapter we used the standard epsilon-greedy approach to select actions, where we initially take random actions to explore, and then progressively switch our strategy to taking the highest value actions.

 The Q function must be learned from data. The Q function has to learn how to make accurate Q value predictions of states. The Q function could be anything really anything from an unintelligent database to a complex deep learning algorithm. Since deep learning is the best class of learning algorithms we have at the moment, we employed neural networks as our Q functions. This means that "learning the Q function" is the same as training a neural network with backpropagation.

 One important concept about Q-learning that we held back until now is that it is an *off-policy* algorithm, in contrast to an *on-policy* algorithm. You already know what a policy is from the last chapter: it's the strategy an algorithm uses to maximize rewards over time. If a human is learning to play Gridworld, they might employ a policy that first scouts all possible paths toward the goal and then selects the one that is shortest. Another policy might be to randomly take actions until you land on the goal.

 An off-policy reinforcement learning algorithm like Q-learning means that the choice of policy does not affect the ability to learn accurate Q values. Indeed, our Qnetwork could learn accurate Q values if we selected actions at random; eventually it would experience a number of winning and losing games and infer the values of states and actions. Of course, this is terribly inefficient, but the policy matters only insofar as it helps us learn with the least amount of data. In contrast, an on-policy algorithm will explicitly depend on the choice of policy or will directly aim at learning a policy from the data. In other words, in order to train our DQN, we need to collect data (experiences) from the environment, and we could do this using any policy, so DQN is offpolicy. In contrast, an on-policy algorithm learns a policy while simultaneously using the same policy to collect experiences for training itself.

 Another key concept we've saved until now is the notion of *model-based* versus *modelfree* algorithms. To make sense of this, we first need to understand what a model is. We use this term informally to refer to a neural network, and it's often used to refer to any kind of statistical model, others being a linear model or a Bayesian graphical model. In another context, we might say a model is a mental or mathematical representation of how something works in "the real world." If we understand exactly how something works (i.e., what it's composed of and how those components interact) then we can not only explain data we've already seen, but we can predict data we haven't yet seen.

 For example, weather forecasters build very sophisticated models of the climate that take into account many relevant variables, and they're constantly measuring realworld data. They can use their models to predict the weather to some degree of accuracy. There's an almost cliché statistics mantra that "all models are wrong, but some are useful," meaning that it is impossible to build a model that 100% corresponds to reality; there will always be data or relationships that we're missing. Nonetheless, many models capture enough truth about a system we're interested in that they're useful for explanation and prediction.

 If we could build an algorithm that could figure out how Gridworld works, it would have inferred a model of Gridworld, and it would be able to play it perfectly. In Q-learning, all we gave the Q-network was a numpy tensor. It had no *a priori* model of Gridworld, but it still learned to play by trial and error. We did not task the Q-network with figuring out how Gridworld works; its only job was to predict expected rewards. Hence, Q-learning is a model-free algorithm.

 As the human architects of algorithms, we may be able to engineer in some of our own domain knowledge about a problem as a model to optimize our problem. We could then supply this model to a learning algorithm and let it figure out the details. This would be a model-based algorithm. For example, most chess-playing algorithms are model-based; they know the rules of how chess works and what the result of taking certain moves will be. The only part that isn't known (and that we'd want the algorithm to figure out) is what sequence of moves will win the game. With a model in hand, the algorithm can make long-term plans in order to achieve its aim.

 In many cases, we want to employ algorithms that can progress from being modelfree to planning with a model. For example, a robot learning how to walk may start to learn by trial and error (model-free), but once it has figured out the basics of walking, it can start to infer a model of its environment and then plan a sequence of steps to get from point A to B (model-based). We'll continue to explore on-policy, off-policy, model-based, and model-free algorithms in the rest of the book. In the next chapter we'll look at an algorithm that will help us build a network that can approximate the policy function.

# *Summary*

- A *state-space* is the set of all possible states that the environment can be in. Usually the states are encoded as tensors, so the state space may be a vector of type  $\mathbb{R}^n$  or a matrix in  $\mathbb{R}^{n \times m}$ .
- An *action-space* is the set of all possible actions given a state; for example, the action space for the game chess would be the set of all legal moves given some state of the game.
- A *state-value* is the expected sum of discounted rewards for a state given we follow some policy. If a state has a high state-value, that means that starting from this state will likely lead to high rewards.
- An *action-value* is the expected rewards for taking an action in a particular state. It is the value of a state-action pair. If you know the action-values for all possible actions for a state, you can decide to take the action with the highest actionvalue, and you would expect to receive the highest reward as a result.
- A *policy function* is a function that maps states to actions. It is the function that "decides" which actions to take given some input state.
- *Q function* is a function that takes a state-action pair and returns the action-value.
- **P** O-learning is a form of reinforcement learning where we attempt to model the Q function; in other words, we attempt to learn how to predict the expected rewards for each action given a state.
- A *deep Q-network (DQN)* is simply where we use a deep learning algorithm as the model in Q-learning.

- *Off-policy learning* is when we learn a policy while collecting data using a different policy.
- *On-policy learning* is when we learn a policy while also simultaneously using it to collect data for learning.
- *Catastrophic forgetting* is a big problem that machine learning algorithms face when training with small batches of data at a time, where the new data being learned erases or corrupts the old information already learned.
- **Experience replay** is a mechanism to allow batch training of reinforcement learning algorithms in order to mitigate catastrophic forgetting and allow stable training.
- A *target network* is a copy of the main DQN that we use to stabilize the update rule for training the main DQN.