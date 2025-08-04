# *Curiosity-driven exploration*

#### *This chapter covers*

- **Understanding the sparse reward problem**
- **Understanding how curiosity can serve as an** intrinsic reward
- **Playing Super Mario Bros. from OpenAI Gym**
- **Implementing an intrinsic curiosity module in** PyTorch
- Training a deep Q-network agent to successfully play Super Mario Bros. without using rewards

The fundamental reinforcement learning algorithms we have studied so far, such as deep Q-learning and policy gradient methods are very powerful techniques in a lot of situations, but they fail dramatically in other environments. Google's Deep-Mind pioneered the field of deep reinforcement learning back in 2013 when they used deep Q-learning to train an agent to play multiple Atari games at superhuman performance levels. But the performance of the agent was highly variable across different types of games. At one extreme, their DQN agent played the Atari game Breakout vastly better than a human, but at the other extreme the DQN was much worse than a human at playing Montezuma's Revenge (figure 8.1), where it could not even pass the first level.

![](_page_1_Picture_1.jpeg)

Figure 8.1 Screenshot from the Montezuma's Revenge Atari game. The player must navigate through obstacles to get a key before any rewards are received.

NOTE The paper that brought great attention to the field of deep reinforcement learning was "Human-level control through deep reinforcement learning" by Volodymyr Mnih and collaborators at Google DeepMind in 2015. The paper is fairly readable and contains the details you'd need to replicate their results.

What's the difference between the environments that explains these disparities in performance? The games that DQN was successful at all gave relatively frequent rewards during game play and did not require significant long-term planning. Montezuma's Revenge, on the other hand, only gives a reward after the player finds a key in the room, which also contains numerous obstacles and enemies. With a vanilla DQN, the agent starts exploring essentially at random. It will take random actions and wait to observe rewards, and those rewards reinforce which actions are best to take given the environment. But in the case of Montezuma's Revenge, it is extremely unlikely that the agent will find the key and get a reward with this random exploration policy, so it will never observe a reward and will never learn.

 This problem is called the *sparse reward problem*, since the rewards in the environment are sparsely distributed (figure 8.2). If the agent doesn't observe enough reward signals to reinforce its actions, it can't learn.

 Animal and human learning offer us the only natural examples of intelligent systems, and we can turn to them for inspiration. Indeed, researchers trying to tackle this sparse reward problem noticed that humans not only maximize extrinsic rewards

![](_page_2_Figure_1.jpeg)

Figure 8.2 In environments with dense rewards, the rewards are received fairly frequently during the training time, making it easy to reinforce actions. In sparse reward environments, rewards may only be received after many sub-goals are completed, making it difficult or impossible for an agent to learn based on reward signals alone.

(those from the environment), like food and sex, but they also demonstrate an intrinsic curiosity, a motivation to explore just for the sake of understanding how things work and to reduce their uncertainty about their environment.

 In this chapter you will we learn about methods for successfully training reinforcement learning agents in sparse reward environments by using principles from human intelligence, specifically our innate curiosity. You will see how curiosity can drive the development of basic skills that the agent can use to accomplish sub-goals and find the sparse rewards. In particular, you will see how a curiosity-powered agent can play the Atari game Super Mario Bros. and learn how to navigate the dynamic terrain just by curiosity alone.

NOTE The code for this chapter is in this book's GitHub repository in the chapter 8 folder: [http://mng.bz/JzKp.](http://mng.bz/JzKp)

## *8.1 Tackling sparse rewards with predictive coding*

In the world of neuroscience, and particularly computational neuroscience, there is a framework for understanding neural systems at a high level called the *predictive coding model*. In this model, the theory says that all neural systems from individual neurons up to large-scale neural networks are running an algorithm that attempts to predict inputs, and hence tries to minimize the *prediction error* between what it expects to experience and what it actually experiences. So at a high level, as you're going about your day, your brain is taking in a bunch of sensory information from the environment, and it's training to predict how the sensory information will evolve. It's trying to stay one step ahead of the actual raw data coming in.

 If something surprising (i.e., unexpected) happens, your brain experiences a large prediction error and then presumably does some parameter updating to prevent that from happening again. For example, you might be talking to someone you just met, and your brain is constantly trying to predict the next word that person will say before they say it. Since this is someone you don't know, your brain will probably have a relatively high average prediction error, but if you become best friends, you'll probably be quite good at finishing their sentences. This is not something you try to do; whether you want to or not, your brain is trying to reduce its prediction error.

 Curiosity can be thought of as a kind of desire to reduce the uncertainty in your environment (and hence reduce prediction errors). If you were a software engineer and you saw some online posts about this interesting field called machine learning, your curiosity to read a book like this would be based on the goal of reducing your uncertainty about machine learning.

 One of the first attempts to imbue reinforcement learning agents with a sense of curiosity involved using a prediction error mechanism. The idea was that in addition to trying to maximize extrinsic (i.e., environment-provided) rewards, the agent would also try to predict the next state of the environment given its action, and it would try to reduce its prediction error. In very familiar areas of an environment, the agent would learn how it works and would have a low prediction error. By using this prediction error as another kind of reward signal, the agent would be incentivized to visit areas of the environment that were novel and unknown. That is, the higher the prediction error is, the more surprising a state is, and therefore the agent should be incentivized to visit these high prediction error states. Figure 8.3 shows the basic framework for this approach.

![](_page_3_Figure_4.jpeg)

The idea is to sum the prediction error (which we will call the *intrinsic reward*) with the extrinsic reward and use that total as the new reward signal for the environment. Now the agent is incentivized to not only figure out how to maximize the environment reward but also to be curious about the environment. The prediction error is calculated as shown in figure 8.4.

 The intrinsic reward is based on the prediction error of states in the environment. This works fairly well on the first pass, but people eventually realized that it runs into another problem, often called the "noisy TV problem" (figure 8.5). It turns out that if you train these agents in an environment that has a constant source of randomness, such as a TV screen playing random noise, the agent will have a constantly high prediction error and will be unable to reduce it. It just stares at the noisy TV

![](_page_4_Figure_1.jpeg)

and produces a prediction for the subsequent state,  $\hat{\textbf{s}}_{t\texttt{+1}}$  (pronounced "S hat t+1", Figure 8.4 The prediction module takes in a state,  $S_t$ , (and action  $a_t$ , not shown) where the hat symbol suggests an approximation). This prediction, along with the true next state, are passed to a mean-squared error function (or some other error function), which produces the prediction error.

indefinitely, since it is highly unpredictable and thus provides a constant source of intrinsic rewards. This is more than just an academic problem, since many realworld environments have similar sources of randomness (e.g., a tree's leaves rustling in the wind).

![](_page_4_Figure_4.jpeg)

Figure 8.5 The noisy TV problem is a theoretical and practical problem where a reinforcement learning agent with a naive sense of curiosity will become entranced by a noisy TV, forever staring at it. This is because it is intrinsically rewarded by unpredictability, and white noise is very unpredictable.

At this point, it seems like prediction error has a lot of potential, but the noisy TV problem is a big flaw. Perhaps we shouldn't pay attention to the absolute prediction error but instead to the rate of change of prediction error. When the agent transitions to an unpredictable state, it will experience a transient surge of prediction error, but then it goes away. Similarly, if the agent encounters a noisy TV, at first it is highly unpredictable and therefore has a high prediction error, but the high prediction error is maintained, so the rate of change is zero.

 This formulation is better, but it still has some potential issues. Imagine that an agent is outside and sees a tree with leaves blowing in the wind. The leaves are blowing around randomly, so this is a high prediction error. The wind stops blowing, and the prediction error goes down, since the leaves are not moving anymore. Then the wind starts blowing again, and prediction error goes up. In this case, even if we're using a prediction error rate, the rate will be fluctuating along with the wind. We need something more robust.

 We want to use this prediction error idea, but we don't want it to be vulnerable to trivial randomness or unpredictability in the environment that doesn't matter. How do we add in the "doesn't matter" constraint to the prediction error module? Well, when we say that something doesn't matter, we mean that it does not affect us or is perhaps uncontrollable. If leaves are randomly blowing in the wind, the agent's actions don't affect the leaves, and the leaves don't affect the actions of the agent. It turns out we can implement this idea as a separate module, in addition to the state prediction module that's the subject of this chapter. This chapter is based on elucidating and implementing the idea from a paper by Deepak Pathak et al. titled "Curiosity-driven Exploration by Self-supervised Prediction" (2017), which successfully resolves the issues we've been discussing.

 We will follow this paper pretty closely because it was one of the biggest contributions to solving the sparse reward problem, and this paper led to a flurry of related research. It also turns out to describe one of the easiest algorithms to implement, among the many others in this area. In addition, one of the goals of this book is to not only teach you the foundational knowledge and skills of reinforcement learning, but to give you a solid-enough mathematics background to be able to read and understand reinforcement learning papers and implement them on your own. Of course, some papers require advanced mathematics, and they are outside the scope of this book, but many of the biggest papers in the field require only some basic calculus, algebra, and linear algebra—things that you probably know if you have made it this far. The only real barrier is getting past the mathematical notation, which we hope to make easier here. We want to teach you how to fish rather than just giving you fish, as the saying goes.

# *8.2 Inverse dynamics prediction*

 $\hat{S}_{t+1}$ , that takes a state and the action taken and returns the predicted next state (fig-We've described how we could use the prediction error as a curiosity signal. The prediction error module from the last section is implemented as a function,  $f: (S_b, a_t) \rightarrow$ ure 8.6). It is predicting the future (forward) state of the environment, so we call it the *forward-prediction model*.

 $\hat{a}_t$ . This is a function, *g*, that takes a state and the next state, and then returns a predic- Remember, we want to only predict aspects of the state that actually matter, not parts that are trivial or noise. The way we build in the "doesn't matter" constraint to the prediction model is to add another model called an *inverse model*,  $g: (S_t, S_{t+1}) \to$ tion for which action was taken that led to the transition from  $s_t$  to  $s_{t+1}$ , as shown in figure 8.7.

![](_page_6_Figure_1.jpeg)

sionality of  $\tilde{S}_t$  is significantly lower than the raw state  $S_t$  (figure 8.8). The raw state On its own, this inverse model is not really useful; there's an additional model that is tightly coupled to the inverse model called the *encoder model*, denoted φ. The encoder function,  $\phi: S_t \to \tilde{S}_t$ , takes a state and returns an encoded state  $\tilde{S}_t$  such that the dimenmight be an RGB video frame with height, width, and channel dimensions, and  $\phi$  will encode that state into a low-dimensional vector. For example, a frame might be 100 pixels by 100 pixels by 3 color channels for a total of 30,000 elements. Many of those pixels will be redundant and not useful, so we want our encoder to encode this state into say a 200-element vector with high-level non-redundant features.

![](_page_6_Figure_3.jpeg)

dimensionality. A variable with the hat symbol over it, such as  $\hat{S}_t$ , denotes an **NOTE** A variable with the tilde symbol over it, such as  $S_t$ , denotes some sort of transformed version of the underlying variable, which may have different approximation (or prediction) of the underlying state and has the same dimensionality.

The encoder model is trained via the inverse model because we actually use the encoded states as inputs to the forward and inverse models *f* and *g* rather than the

raw states. That is, the forward model becomes a function,  $f: \phi(S_t) \times a_t \to \hat{\phi}(S_{t+1}),$ becomes a function,  $g: \phi(S_t) \times \hat{\phi}(S_{t+1}) \to \hat{a}_t$  (figure 8.9). The notation  $P: a \times b \to c$ where  $\hat{\phi}(S_{t+1})$  refers to a prediction of the encoded state, and the inverse model means that we define some function *P* that takes a pair (*a*,*b*) and transforms it into a new object *c*.

![](_page_7_Figure_2.jpeg)

![](_page_7_Figure_3.jpeg)

The encoder model isn't trained directly—it is *not* an autoencoder. It is only trained through the inverse model. The inverse model is trying to predict the action that was taken to transition from one state to the next using the encoded states as inputs, and in order to minimize its own prediction error, its error will backpropagate through to the encoder model as well as itself. The encoder model will then learn to encode states in a way that is useful for the task of the inverse model. Importantly, although the forward model also uses the encoded states as inputs, we do *not* backpropagate from the forward model to the encoder model. If we did, the forward model would coerce the encoder model into mapping all states into a single fixed output, since that would be the easiest to predict.

 Figure 8.10 shows the overall graph structure: the forward pass of the components and also the backward (backpropagation) pass to update the model parameters. It is worth repeating that the inverse model backpropagates back through to the encoder model, and the encoder model is only trained together with the inverse model. We must use PyTorch's detach() method to detach the forward model from the encoder so it won't backpropagate into the encoder. The purpose of the encoder is not to give us a low-dimensional input for improved performance but to learn to encode the state using a representation that only contains information relevant for predicting actions. This means that aspects of the state that are randomly fluctuating and have no impact on the agent's actions will be stripped from this encoded representation. This, in theory, should avoid the noisy TV problem.

 Notice that for both the forward and inverse models we need access to the data for a full transition, i.e., we need  $(S_t, a_t, S_{t+1})$ . This is not an issue when we use an experience replay memory, as we did in chapter 3 about deep Q-learning, since the memory will store a bunch of these kinds of tuples.

![](_page_8_Figure_1.jpeg)

Figure 8.10 The curiosity module. First the encoder will encode states  $S_t$  and  $S_{t+1}$  into low-dimensional vectors,  $\phi(\mathbf{s}_t)$  and  $\phi(\mathbf{s}_{t+1})$  respectively. These encoded states are passed to the forward and inverse models. Notice that the inverse model backpropagates to the encoded model, thereby training it through its own error. The forward model is trained by backpropagating from its own error function, but it does *not* backpropagate through to the encoder like the inverse model does. This ensures that the encoder learns to produce state representations that are only useful for predicting which action was taken. The black circle indicates a copy operation that copies the output from the encoder and passes the copies to the forward and inverse models.

### *8.3 Setting up Super Mario Bros.*

Together, the forward, inverse, and encoder models form the *intrinsic curiosity module* (ICM), which we will discuss in detail later in this chapter. The components of the ICM function together for the sole purpose of generating an intrinsic reward that drives curiosity in the agent. The ICM generates a new intrinsic reward signal based on information from the environment, so it is independent of how the agent model is implemented. The ICM can be used for any type of environment, but it will be most useful in sparse reward environments.

 We could use whatever agent model implementation we want, such as a distributed actor-critic model (covered in chapter 5). In this chapter we will use a Q-learning model to keep things simple and focus on implementing the ICM. We will use Super Mario Bros. as our testbed.

 Super Mario Bros. does not really suffer from the sparse reward problem. The particular environment implementation we will use provides a reward in part based on forward progress through the game, so positive rewards are almost continuously provided. However, Super Mario Bros. is still a great choice to test the ICM because we can choose to "turn off" the extrinsic (environment-provided) reward signal; we can see how well the agent explores the environment just based on curiosity, and we can see how well correlated the extrinsic and intrinsic rewards are.
The implementation of Super Mario Bros. we will use has 12 discrete actions that can be taken at each time step, including a NO-OP (no-operation) action. Table 8.1 lists all the actions.

Table 8.1 Actions in Super Mario Bros.

| <b>Index</b>   | <b>Action</b>        |
|----------------|----------------------|
| 0              | $NO-OP$ / Do nothing |
| $\mathbf{1}$   | Right                |
| $\overline{c}$ | Right + Jump         |
| 3              | Right + Run          |
| $\overline{4}$ | Right + Jump + Run   |
| 5              | Jump                 |
| 6              | Left                 |
| 7              | Left + Run           |
| 8              | $Left + Jump$        |
| 9              | Left + Jump + $Run$  |
| 10             | Down                 |
| 11             | Up                   |

You can install Super Mario Bros. by itself with pip:

>>> pip install gym-super-mario-bros

After it is installed, you can test the environment (e.g., try running this code in a Jupyter Notebook) by playing a random agent and taking random actions. To review how to use the OpenAI Gym, please refer back to chapter 4. In the following listing we instantiate the Super Mario Bros. environment and test it by taking random actions.

![](0__page_9_Figure_7.jpeg)

```
done = True
for step in range(2500): 
     if done:
        state = env.reset()
    state, reward, done, info = env.step(env.action space.sample())
     env.render()
env.close()
                                     Tests the environment by 
                                   taking random actions
```

If everything went well, a little window should pop up displaying Super Mario Bros., but it will be taking random actions and not making any forward progress through the level. By the end of this chapter you will have trained an agent that makes consistent forward progress and has learned to avoid or jump on enemies and to jump over obstacles. This, only using the intrinsic curiosity-based reward.

 In the OpenAI Gym interface, the environment is instantiated as a class object called env and the main method you need to use is its step $(\ldots)$  method. The step method takes an integer representing the action to be taken. As with all OpenAI Gym environments, this one returns state, reward, done, and info data after each action is taken. The state is a numpy array with dimensions (240, 256, 3) representing an RGB video frame. The reward is bounded between –15 and 15 and is based on the amount of forward progress. The done variable is a Boolean that indicates whether or not the game is over (e.g., whether Mario dies). The info variable is a Python dictionary with the metadata listed in table 8.2.

| Key      | <b>Type</b> | <b>Description</b>                                    |
|----------|-------------|-------------------------------------------------------|
| coins    | int         | The number of collected coins                         |
| flag get | bool        | True if Mario reached a flag or ax                    |
| life     | int         | The number of lives left, i.e., $\{3, 2, 1\}$         |
| score    | int         | The cumulative in-game score                          |
| stage    | int         | The current stage, i.e., $\{1, \ldots, 4\}$           |
| status   | str         | Mario's status, i.e., { 'small', 'tall', 'fireball' } |
| time     | int         | The time left on the clock                            |
| world    | int         | The current world, i.e., $\{1, \ldots, 8\}$           |
| x pos    | int         | Mario's x position in the stage                       |

Table 8.2 The metadata returned after each action in the **info** variable (source: https://github.com/Kautenja/gym-super-mario-bros)

We will only need to use the  $x$  pos key. In addition to getting the state after calling the step method, you can also retrieve the state at any point by calling env.render ("rgb\_array"). That's basically all you need to know about the environment in order to train an agent to play it.

## *8.4 Preprocessing and the Q-network*

The raw state is an RGB video frame with dimensions (240, 256, 3), which is unnecessarily high-dimensional and would be computationally costly for no advantage. We will convert these RGB states into grayscale and resize them to  $42 \times 42$  to allow our model to train much faster.

```
Listing 8.2 Downsample state and convert to grayscale
import matplotlib.pyplot as plt
                                                   The scikit-image library 
from skimage.transform import resize 
                                                  has an image-resizing 
import numpy as np
                                                   function built in.
def downscale obs(obs, new size=(42,42), to qray=True):
     if to_gray:
         return resize(obs, new_size, anti_aliasing=True).max(axis=2) 
                                                                                  ∢
     else:
         return resize(obs, new_size, anti_aliasing=True)
                                       To convert to grayscale, we simply take the maximum
                                      values across the channel dimension for good contrast.
```

The downscale obs function accepts the state array (obs), a tuple indicating the new size in height and width, and a Boolean for whether to convert to grayscale or not. We set it to True by default since that is what we want. We use the scikit-image library's resize function, so you may need to install it if you don't have it already (go to the download page at [https://scikit-image.org/\)](https://scikit-image.org/). It's a very useful library for working with image data in the form of multidimensional arrays.

You can use matplotlib to visualize a frame of the state:

```
>>> plt.imshow(env.render("rgb_array"))
>>> plt.imshow(downscale obs(env.render("rgb array")))
```

The downsampled image will look pretty blurry, but it still contains enough visual information to play the game.

 We need to build a few other data processing functions to transform these raw states into a useful form. We will not just pass a single  $42 \times 42$  frame to our models; we will instead pass the last three frames of the game (in essence, adding a channel dimension) so the states will be a  $3 \times 42 \times 42$  tensor (figure 8.11). Using the last three frames gives our model access to velocity information (i.e., how fast and in which direction objects are moving) rather than just positional information.

 When the game first starts, we only have access to the first frame, so we prepare the initial state by concatenating the same state three times to get the  $3 \times 42 \times 42$  initial state. After this initial state, we can replace the last frame in the state with the most recent frame from the environment, replace the second frame with the old last one, and replace the first frame with the old second. Basically, we have a fixed length firstin-first-out data structure where we append to the right, and the left automatically pops off. Python has a built-in data structure called deque in the collections library that can implement this behavior when the maxlen attribute is set to 3.

![](0__page_12_Figure_1.jpeg)

Figure 8.11 Each state given to the agent is a concatenation of the three most recent (grayscale) frames in the game. This is necessary so that the model can have access to not just the position of objects, but also their direction of movement.

We will use three functions to prepare the raw states in a form that our agent and encoder models will use. The prepare\_state function resizes the image, converts to grayscale, converts from numpy to PyTorch tensor, and adds a batch dimension using the .unsqueeze(dim=) method. The prepare multi state function takes a tensor of dimensions Batch x Channel x Height x Width and updates the channel dimension with new frames. This function will only be used during the testing of the trained model; during training we will use a deque data structure to continuously append and pop frames. Lastly the prepare\_initial\_state function prepares the state when we first start the game and don't have a history of two prior frames. This function will copy the one frame three times to create a Batch x 3 x Height x Width tensor.

## Listing 8.3 Preparing the states

```
import torch
from torch import nn
from torch import optim
import torch.nn.functional as F
from collections import deque
def prepare state(state):
    return torch.from numpy(downscale obs(state,
     to qray=True)).float().unsqueeze(dim=0)
def prepare multi state(state1, state2):
     state1 = state1.clone()
    tmp = torch.from numpy(downscale obs(state2, to gray=True)).float()
     state1[0][0] = state1[0][1]
    statel[0][1] = statel[0][2]state1[0][2] = tmp return state1
def prepare initial state(state, N=3):
    state = torch.from numpy(downscale obs(state, to gray=True)).float()
    tmp = state .repeat((N,1,1)) return tmp.unsqueeze(dim=0)
                                                  Downscales state and converts 
                                                  to grayscale, converts to a 
                                                  PyTorch tensor, and finally 
                                                  adds a batch dimension
                                                      Given an existing 3-frame state1
                                                      and a new single frame 2, adds 
                                                      the latest frame to the queue
                                                      Creates a state with three 
                                                      copies of the same frame and 
                                                      adds a batch dimension
```

## *8.5 Setting up the Q-network and policy function*

As we mentioned, we will use a deep Q-network (DQN) for the agent. Recall that a DQN takes a state and produces action values, i.e., predictions for the expected rewards for taking each possible action. We use these action values to determine a policy for action selection. For this particular game there are 12 discrete actions, so the output layer of our DQN will produce a vector of length 12 where the first element is the predicted value of taking action 0, and so on.

 Remember that action values are (in general) unbounded in either direction; they can be positive or negative if the rewards can be positive or negative (which they can be in this game), so we do not apply any activation function on the last layer. The input to the DQN is a tensor of shape Batch  $x$  3  $x$  42  $x$  42, where, remember, the channel dimension (3) is for the most recent three frames of game play.

 For the DQN, we use an architecture consisting of four convolutional layers and two linear layers. The *exponential linear unit* (ELU) activation function is used after each convolutional layer and the first linear layer (but there's no activation function after the last linear layer). The architecture is diagrammed in figure 8.12. As an exercise you can add a *long short-term memory* (LSTM) or *gated recurrent unit* (GRU) layer that can allow the agent to learn from long-term temporal patterns.

 Our DQN will learn to predict the expected rewards for each possible action given the state (i.e., action values or  $Q$  values), and we use these action values to decide which action to take. Naively we should just take the action associated with the highest value, but our DQN will not produce accurate action values in the beginning, so we need to have a policy that allows for some exploration so the DQN can learn better action-value estimates.

![](0__page_13_Figure_6.jpeg)

Not shown: ELU activation function applied after each layer except the output layer.

Figure 8.12 The DQN architecture we will use. The state tensor is the input, and it is passed through four convolutional layers and then two linear layers. The ELU activation function is applied after the first five layers but not the output layer because the output needs to be able to produce arbitrarily scaled Q values. Earlier we discussed using the epsilon-greedy policy, where we take a random action with probability  $\varepsilon$  and take the action with the highest value with probability  $(1 - \varepsilon)$ . We usually set  $\varepsilon$  to be some reasonably small probability like 0.1, and often we'll slowly decrease  $\varepsilon$  during training so that it becomes more and more likely to choose the highest value action.

 We also discussed sampling from a softmax function as our policy. The softmax function essentially takes a vector input with arbitrary real numbers and outputs a same-sized vector where each element is a probability, so all elements sum to 1. It therefore creates a discrete probability distribution. If the input vector is a set of action values, the softmax function will return a discrete probability distribution over the actions based on their action values, such that the action with the highest action value will be assigned the highest probability. If we sample from this distribution, the actions with the highest values will be chosen more often, but other actions will also be chosen. The problem with this approach is that if the best action (according to the action values) is only slightly better than other options, the worse actions will still be chosen with a fairly high frequency. For example, in the following example we take an action-value tensor for five actions and apply the softmax function from PyTorch's functional module.

```
>>> torch.nn.functional.softmax(th.Tensor([3.6, 4, 3, 2.9, 3.5]))
tensor([0.2251, 0.3358, 0.1235, 0.1118, 0.2037])
```

As you can see, the best action (index 1) is only slightly better than the others, so all the actions have pretty high probability, and this policy is not that much different from a uniformly random policy. We will use a policy that begins with a softmax policy to encourage exploration, and after a fixed number of game steps we will switch to an epsilon-greedy strategy, which will continue to give us some exploration capacity but mostly just takes the best action.

![](0__page_14_Figure_5.jpeg)

The other big component we need for the DQN is an *experience replay memory*. Gradient-based optimization does not work well if you only pass one sample of data at a time because the gradients are too noisy. In order to average over the noisy gradients, we need to take sufficiently large samples (called batches or mini-batches) and average

or sum the gradients over all the samples. Since we only see one sample of data at a time when playing a game, we instead store the experiences in a "memory" store and then sample mini-batches from the memory for training.

 We will build an experience replay class that contains a list to store tuples of experiences, where each tuple is of the form  $(S_h a_h r_h S_{t+1})$ . The class will also have methods to add a memory and sample a mini-batch.

```
from random import shuffle
            import torch
            from torch import nn
            from torch import optim
            import torch.nn.functional as F
            class ExperienceReplay:
                def init (self, N=500, batch size=100):
                      self.N = N 
                     self.batch size = batch size
                      self.memory = [] 
                      self.counter = 0
                def add memory(self, state1, action, reward, state2):
                      self.counter +=1 
                     if self.counter % 500 == 0: self.shuffle_memory()
                     if len(self.memory) < self.N: 
                          self.memory.append( (state1, action, reward, state2) )
                      else:
                        rand index = np.random.random(0, self.N-1)self.memory[rand_index] = (state1, action, reward, state2)

random
               def shuffle memory(self):
   shuffle(self.memory)
                def qet batch(self):
                      if len(self.memory) < self.batch_size:
                         batch size = len(self.memory) else:
                         batch size = self.batch size if len(self.memory) < 1:
                          print("Error: No data in memory.")
                          return None
                      ind = np.random.choice(np.arange(len(self.memory)), \
                      batch_size,replace=False)
                     batch = [self.memory[i] for i in ind] #batch is a list of tuples
                     state1 batch = torch.stack([x[0].squareeze(dim=0) for x in batch],dim=0)
                     action batch = torch.Tensor([x[1] for x in batch]).long()
                     reward batch = torch.Tensor([x[2] for x in batch])
                      state2_batch = torch.stack([x[3].squeeze(dim=0) for x in batch],dim=0)
                      return state1_batch, action_batch, reward_batch, state2_batch
               Listing 8.5 Experience replay
                                                                      N is the maximum size 
                                                                      of the memory list.
                                                               batch_size is the number of samples 
                                                               to generate from the memory with 
                                                               the get_batch(…) method.
                                                               Every 500 iterations of adding a 
                                                                memory, shuffles the memory list to 
                                                                promote a more random sample
 If the memory
is not full, adds
   to the list;
    otherwise
    replaces a
 memory with
                                                      the new one Uses Python's built-in shuffle function 
                                                      to shuffle the memory list
                                                                  Randomly samples a 
                                                                  mini-batch from the 
                                                                 memory list
                                                                Creates an array of random 
                                                                 integers representing indices
```

The experience replay class essentially wraps a list with extra functionality. We want to be able to add tuples to the list, but only up to a maximum number, and we want to be able to sample from the list. When we sample with the get  $batch(...)$  method, we create an array of random integers representing indices in the memory list. We index into the memory list with these indices, retrieving a random sample of memories. Since each sample is a tuple,  $(S_{\nu}a_{\nu}r_{\nu}S_{t+1})$ , we want to separate out the different components and stack them together into a  $S_t$  tensor,  $a_t$  tensor, and so on, where the first dimension of the array is the batch size. For example, the  $S_t$  tensor we want to return should be of dimension batch\_size  $\times$  3 (channels)  $\times$  42 (height)  $\times$  42 (width). PyTorch's stack(...) function will concatenate a list of individual tensors into a single tensor. We also make use of the squeeze  $(\ldots)$  and unsqueeze  $(\ldots)$  methods to remove and add dimensions of size 1.

With all of that set up, we have just about everything we need to train a vanilla DQN besides the training loop itself. In the next section we will implement the intrinsic curiosity module.

## *8.6 Intrinsic curiosity module*

As we described earlier, the intrinsic curiosity module (ICM) is composed of three independent neural network models: the forward model, inverse model, and the encoder (figure 8.13). The forward model is trained to predict the next (encoded) state, given the current (encoded) state and an action. The inverse model is trained to predict the action that was taken, given two successive (encoded) states,  $\phi(S_t)$  and  $\phi(S_{t+1})$ . The encoder simply transforms a raw three-channel state into a single lowdimensional vector. The inverse model acts indirectly to train the encoder to encode states in a way that only preserves information relevant to predicting the action.

 The input and output types of each component of the ICM are shown in figure 8.14. The forward model is a simple two-layer neural network with linear layers. The input to the forward model is constructed by concatenating the state  $\phi(S_t)$  with the action *a<sub>t</sub>*. The encoded state  $\phi(S_i)$  is a tensor  $B \times 288$  and the action  $a_i : B \times 1$  is a batch of integers indicating the action index, so we make a one-hot encoded vector by creating a vector of size 12 and setting the respective  $a_t$  index to 1. Then we concatenate these two tensors to create a batch  $\times$  288 + 12 = batch  $\times$  300 dimensional tensor. We

![](0__page_16_Figure_6.jpeg)

Figure 8.13 A high-level overview of the intrinsic curiosity module (ICM). The ICM has three components that are each separate neural networks. The encoder model encodes states into a lowdimensional vector, and it is trained indirectly through the inverse model, which tries to predict the action that was taken given two consecutive states. The forward model predicts the next encoded state, and its error is the prediction error that is used as the intrinsic reward.

![](0__page_17_Figure_1.jpeg)

Figure 8.14 This figure shows the type and dimensionality of the inputs and outputs of each component of the ICM.

use the rectified linear unit (ReLU) activation unit after the first layer, but we do not use an activation function after the output layer. The output layer produces a  $B \times$ 288 tensor.

 The inverse model is also a simple two-layer neural network with linear layers. The input is two encoded states,  $S_t$  and  $S_{t+1}$ , concatenated to form a tensor of dimension batch  $\times$  288 + 288 = batch  $\times$  576. We use a ReLU activation function after the first layer. The output layer produces a tensor of dimension batch  $\times$  12 with a softmax function applied, resulting in a discrete probability distribution over actions. When we train the inverse model, we compute the error between this discrete distribution over actions and a one-hot encoded vector of the true action taken.

 The encoder is a neural network composed of four convolutional layers (with an identical architecture to the DQN), with an ELU activation function after each layer. The final output is then flattened to get a flat 288-dimensional vector output.

 The whole point of the ICM is to produce a single quantity, the forward-model prediction error (figure 8.15). We literally take the error produced by the loss function and use that as the intrinsic reward signal for our DQN. We can add this intrinsic

![](0__page_17_Figure_7.jpeg)

Figure 8.15 The DQN and the ICM contribute to a single overall loss function that is given to the optimizer to minimize with respect to the DQN and ICM parameters. The DQN's Q-value predictions are compared to the observed rewards. The observed rewards, however, are summed together with the ICM's prediction error to get a new reward value.
![](1__page_18_Figure_1.jpeg)

![](1__page_18_Figure_2.jpeg)

Figure 8.16 A complete view of the overall algorithm, including the ICM. First we generate *B* samples from the experience replay memory and use these for the ICM and DQN. We run the ICM forward to generate a prediction error, which is then provided to the DQN's error function. The DQN learns to predict action values that reflect not only extrinsic (environment provided) rewards but also an intrinsic (prediction error-based) reward.

reward to the extrinsic reward to get the final reward signal,  $r_t = r_i + r_e$ . We can scale the intrinsic or extrinsic rewards to control the proportions of the total reward.

 Figure 8.16 shows the ICM in more detail, including the agent model (DQN). Let's look at the code for the components of the ICM.

```
class Phi(nn.Module): 
    def __init__(self):
        super(Phi, self). init ()
        self.comv1 = nn.Conv2d(3, 32, kernel size=(3,3), stride=2, padding=1) self.conv2 = nn.Conv2d(32, 32, kernel_size=(3,3), stride=2, padding=1)
         self.conv3 = nn.Conv2d(32, 32, kernel_size=(3,3), stride=2, padding=1)
         self.conv4 = nn.Conv2d(32, 32, kernel_size=(3,3), stride=2, padding=1)
     def forward(self,x):
        x = F.normalize(x)y = F.elu(self.conv1(x))
        y = F.elu(self.conv2(y))
        y = F.elu(self.conv3(y))
        y = F.elu(self.conv4(y)) #size [1, 32, 3, 3] batch, channels, 3 x 3
         y = y.flatten(start_dim=1) #size N, 288
         return y
class Gnet(nn.Module): 
    def __ init (self):
        super(Gnet, self). init ()
        selfuinear1 = nn.Linear(576,256)
        selfuinear2 = nn.Linear(256,12)
     def forward(self, state1,state2):
        x = torch.cat( (state1, state2), dim=1)
        y = F.relu(self.linear1(x))
        y = selfuinear2(y)
        y = F.softmax(y, dim=1) return y
class Fnet(nn.Module): 
    def __ init (self):
        super(Fnet, self). init ()
        selfuinear1 = nn.Linear(300,256)
         self.linear2 = nn.Linear(256,288)
     def forward(self,state,action):
        action = torch.zeros(action.shape[0],12)
         indices = torch.stack( (torch.arange(action.shape[0]), 
     action.squeeze()), dim=0)
         indices = indices.tolist()
         action_[indices] = 1.
        x = torch.cat( (state, action ), dim=1)
        y = F.relu(self.linear1(x))
        y = selfuinear2(y)
         return y
  Listing 8.6 ICM components
                                  Phi is the encoder network.
                               Gnet is the inverse model.
                                  Fnet is the forward model.
                                                              The actions are stored as 
                                                              integers in the replay 
                                                              memory, so we convert 
                                                              to a one-hot encoded 
                                                              vector.
```

None of these components have complicated architectures. They're fairly mundane, but together they form a powerful system. Now we need to include our DQN model, which is a simple set of a few convolutional layers.

```
class Qnetwork(nn.Module):
    def _init_(self):
        super(Qnetwork, self). init ()
        self.conv1 = nn.Conv2d(in channels=3, out channels=32,
     kernel_size=(3,3), stride=2, padding=1)
         self.conv2 = nn.Conv2d(32, 32, kernel_size=(3,3), stride=2, padding=1)
         self.conv3 = nn.Conv2d(32, 32, kernel_size=(3,3), stride=2, padding=1)
         self.conv4 = nn.Conv2d(32, 32, kernel_size=(3,3), stride=2, padding=1)
        selfuinear1 = nn.Linear(288,100)
        selfuinear2 = nn.Linear(100,12)
     def forward(self,x):
        x = F.normalize(x)y = F.elu(self.conv1(x))
        y = F.elu(self.conv2(y))
        y = F.elu(self.conv3(y))
        y = F.elu(self.conv4(y))
        y = y.flatten(start dim=2)
        y = y.\text{view}(y.\text{shape}[0], -1, 32)y = y. flatten (start dim=1)
        y = F.elu(self.linear1(y))
         y = self.linear2(y) 
         return y
  Listing 8.7 Deep Q-network
                                         The output is of 
                                         shape N x 12.
```

We've covered the ICM components; now let's put them together. We're going to define a function that accepts  $(S_b a_t, S_{t+1})$  and returns the forward-model prediction error and the inverse-model error. The forward-model error will be used not only to backpropagate and train the forward model but also as the intrinsic reward for the DQN. The inverse-model error is only used to backpropagate and train the inverse and encoder models. First we'll look at the hyperparameter setup and the instantiation of the models.

```
params = \{'batch size':150,
     'beta':0.2,
     'lambda':0.1,
     'eta': 1.0,
     'gamma':0.2,
     'max_episode_len':100,
    'min progress':15,
    'action repeats':6,
     'frames_per_state':3
}
replay = ExperienceReplay(N=1000, batch_size=params['batch_size'])
Qmodel = Qnetwork()
encoder = Phi()forward_model = Fnet()
  Listing 8.8 Hyperparameters and model instantiation
```

```
inverse model = Gnet()
forward_loss = nn.MSELoss(reduction='none')
inverse_loss = nn.CrossEntropyLoss(reduction='none')
qloss = nn.MSELoss()
all model params = list(Qmodel.parameters()) + list(encoder.parameters()) \leftrightarrowall model params += list(forward model.parameters()) +
     list(inverse model.parameters())
opt = optim.Adam(lr=0.001, params=all_model_params)
                                                              We can add the parameters
                                                                 from each model into a
                                                             single list and pass that into
                                                                     a single optimizer.
```

Some of the parameters in the params dictionary will look familiar, such as batch \_size, but the others probably don't. We'll go over them, but first let's take a look at the overall loss function.

Here's the formula for the overall loss for all four models (including the DQN):

$$
minimize[\lambda \cdot Q_{loss} + (1 - \beta)F_{loss} + \beta \cdot G_{loss}]
$$

This formula adds the DQN loss to the forward and inverse model losses, each scaled by a coefficient. The DQN loss has a free-scaling parameter,  $\lambda$ , whereas the forward and inverse model losses share a scaling parameter,  $\beta$ , so that they're inversely related. This is the only loss function we backpropagate through, so at each training step we backpropagate through all four models starting from this single loss function.

The max episode len and min progress parameters are used to set the minimum amount of forward progress Mario must make or we'll reset the environment. Sometimes Mario will get stuck behind an obstacle and will just keep taking the same action forever, so if Mario doesn't move forward enough in a reasonable amount of time, we just assume he's stuck.

 During training, if the policy function says to take action 3 (for example), we will repeat that action six times (set according to the action\_repeats parameter) instead of just once. This helps the DQN learn the value of actions more quickly. During testing (i.e., inference), we only take the action once. The gamma parameter is the same gamma parameter from the DQN chapter. When training the DQN, the target value is not just the current reward  $r_t$  but the highest predicted action value for the next state, so the full target is  $r_t + \gamma \cdot \max(Q(S_{t+1}))$ . Lastly, the frames per state parameter is set to 3 since each state is the last three frames of the game play.

```
Listing 8.9 The loss function and reset environment
```

```
def loss_fn(q_loss, inverse_loss, forward_loss):
   loss = (1 -q) - params['beta']) * inverse loss
   loss += params['beta'] * forward loss
   loss = loss.sum() / loss .flatten().shape[0] loss = loss_ + params['lambda'] * q_loss
    return loss
def reset_env():
```

 $" " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "$ 

```
 Reset the environment and return a new initial state
" " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " env.reset()
state1 = prepare initial state(env.render('rgb array'))
 return state1
```

Finally, we get to the actual ICM function.

```
def ICM(state1, action, state2, forward scale=1., inverse scale=1e4):
       state1 hat = encoder(state1)
        state2_hat = encoder(state2)
       state2 hat pred = forward model(state1 hat.detach(), action.detach()) <
       forward pred err = forward scale * forward loss(state2 hat pred, \setminus state2_hat.detach()).sum(dim=1).unsqueeze(dim=1)
       pred action = inverse model(state1 hat, state2 hat)
       inverse pred err = inverse scale * inverse loss(pred action, \setminus action.detach().flatten())
                                               .unsqueeze(dim=1)
       return forward pred err, inverse pred err
     Listing 8.10 The ICM prediction error calculation
Encodes state1 and state2 
using the encoder model Runs the forward model using the encoded
                                                   states, but we detach them from the graph
                                                                      The inverse model
                                                             returns a softmax probability
                                                                distribution over actions.
```

It must be repeated how important it is to properly detach nodes from the graph when running the ICM. Recall that PyTorch (and pretty much all other machine learning libraries) builds a computational graph where nodes are *operations* (computations), and *connections* (also called edges) between nodes are the tensors that flow in and out of individual operations. By calling the .detach() method, we disconnect the tensor from the computational graph and treat it just like raw data; this prevents PyTorch from backpropagating through that edge. If we don't detach the state1\_hat and state2\_hat tensors when we run the forward model and its loss, the forward model will backpropagate into the encoder and will corrupt the encoder model.

 We've now approached the main training loop. Remember, since we're using experience replay, training only happens when we sample from the replay buffer. We'll set up a function that samples from the replay buffer and computes the individual model errors.

```
def minibatch train(use extrinsic=True):
            state1 batch, action_batch, reward_batch, state2_batch = replay.get_batch()
            action batch = action batch.view(action batch.shape[0],1))
            reward batch = reward batch.view(reward batch.shape[0], 1)
             forward_pred_err, inverse_pred_err = ICM(state1_batch, action_batch, 
          \Rightarrow state2 batch)
          Listing 8.11 Mini-batch training using experience replay
                                                            We reshape these tensors to add a single
                                                         dimension to be compatible with the models.
  Runs
the ICM
```

![](1__page_23_Figure_1.jpeg)

Now let's tackle the main training loop, shown in listing 8.12. We initialize the first state using the prepare initial state(...) function we defined earlier, which just takes the first frame and repeats it three times along the channel dimension. We also set up a deque instance, to which we will append each frame as we observe them. The deque is set to a maxlen of 3, so only the most recent three frames are stored. We convert the deque first to a list and then to a PyTorch tensor of dimensions  $1 \times 3 \times 42 \times 42$ before passing it to the Q-network.

```
epochs = 3500env.reset()
             state1 = prepare initial state(env.render('rgb array'))
             eps=0.15
             losses = []
             episode_length = 0
             switch to eps qreedy = 1000
             state deque = deque(maxlen=params['frames per state'])
             e reward = 0.
             last x pos = env.env.env. x position
             ep_lengths = []
             use explicit = False
             for i in range(epochs):
                  opt.zero_grad()
                  episode_length += 1
                  q_val_pred = Qmodel(state1) 
                  if i > switch to eps qreedy:
                      action = int(policy(q val pred,eps)) else:
                      action = int(policy(q val pred))for j in range(params['action repeats']):
                      state2, e reward, done, info = env.step(action)
                       last_x_pos = info['x_pos']
                       if done:
                          state1 = reset env()
                           break
                Listing 8.12 The training loop
                                                              We need to keep track of the 
                                                              last x position in order to reset 
                                                              if there's no forward progress.
                                                                Runs the DQN forward to get 
                                                                action-value predictions
                                                                   After the first 1,000 
                                                                   epochs, switches to the 
                                                                   epsilon-greedy policy
    Repeats
  whatever
  action the
policy says 6
  times, to
  speed up
   learning
```

![](1__page_24_Figure_1.jpeg)

While it's a bit lengthy, this training loop is pretty simple. All we do is prepare a state, input to the DQN, get action values (Q values), input to the policy, get an action to take, and then call the env.step(action) method to perform the action. We then get the next state and some other metadata. We add this full experience as a tuple,  $(S_h a_h r_h S_{h+1})$ , to the experience replay memory. Most of the action is happening in the mini-batch training function we already covered.

 That is the main code you need to build an end-to-end DQN and ICM to train on Super Mario Bros. Let's test it out by training for 5,000 epochs, which takes about 30 minutes or so running on a MacBook Air (with no GPU). We will train with use\_ extrinsic=False in the mini-batch function, so it is learning only from the intrinsic reward. You can plot the individual losses for each of the ICM components and the DQN with the following code. We will log-transform the loss data to keep them on a similar scale.

```
>>> losses_ = np.array(losses)
>>> plt.figure(figsize=(8,6))
>>> plt.plot(np.log(losses_[:,0]),label='Q loss')
>>> plt.plot(np.log(losses_[:,1]),label='Forward loss')
>>> plt.plot(np.log(losses_[:,2]),label='Inverse loss')
>>> plt.legend()
>>> plt.show()
```

![](1__page_25_Figure_1.jpeg)

Figure 8.17 These are the losses for the individual components of the ICM and the DQN. The losses do not smoothly decrease like we're used to with a single supervised neural network because the DQN and ICM are trained adversarially.

As shown in figure 8.17, the DQN loss initially drops and then slowly increases and plateaus. The forward loss seems to slowly decrease but is pretty noisy. The inverse model looks sort of flatlined, but if you were to zoom in, it does seem to very slowly decrease over time. The loss plots look a lot nicer if you set use\_extrinsic=True and use the extrinsic rewards. But don't feel let down by the loss plots. If we test the trained DQN, you will see that it does a lot better than the loss plots suggest. This is because the ICM and DQN are behaving like an adversarial dynamic system since the forward model is trying to lower its prediction error, but the DQN is trying to maximize the prediction error by steering the agent toward unpredictable states of the environment (figure 8.18).

 If you look at the loss plot for a *generative adversarial network* (GAN), the generator and discriminator loss look somewhat similar to our DQN and forward model loss with use extrinsic=False. The losses do not smoothly decrease like you're used to

![](1__page_26_Figure_1.jpeg)

Figure 8.18 The DQN agent and forward model are trying to optimize antagonistic objectives and hence form an adversarial pair.

A better assessment of how well the overall training is going is to track the episode length over time. The episode length should be increasing if the agent is learning how to progress through the environment more effectively. In our training loop, whenever the episode finishes (i.e., when the done variable becomes True because the agent dies or doesn't make sufficient forward progress), we save the current info['x\_pos'] to the ep\_lengths list. We expect that the maximum episode lengths will get longer and longer over training time.

```
>>> plt.figure()
>>> plt.plot(np.array(ep_lengths), label='Episode length')
```

In figure 8.19 we see that early on the biggest spike is getting to the 150 mark (i.e., the x position in the game), but over training time the farthest distance the agent is able to reach (represented by the height of the spikes) steadily increases, although there is some randomness.

 The episode length plot looks promising, but let's render a video of our trained agent playing Super Mario Bros. If you're running this on your own computer, the OpenAI Gym provides a render function that will open a new window with live game play. Unfortunately, this won't work if you're using a remote machine or cloud virtual machine. In those cases, the easiest alternative is to run a loop of the game, saving each observation frame to a list, and once the loop terminates, convert it to a numpy array. You can then save this numpy array of video frames as a video and play it in a Jupyter Notebook.

```
>>> import imageio; 
>>> from IPython.display import Video; 
>>> imageio.mimwrite('gameplay.mp4', renders, fps=30); 
>>> Video('gameplay.mp4')
```
![](2__page_27_Figure_1.jpeg)

Figure 8.19 Training time is on the *x* axis and episode length is on the *y* axis. We see bigger and bigger spikes over training time, which is what we expect.

In listing 8.13 we use the built-in OpenAI Gym render method to view the game in real-time.

# Listing 8.13 Testing the trained agent

```
eps=0.1
done = True
state deque = deque(maxlen=params['frames per state'])
for step in range(5000):
     if done:
         env.reset()
        state1 = prepare initial state(env.render('rgb array'))
     q_val_pred = Qmodel(state1)
     action = int(policy(q_val_pred,eps))
     state2, reward, done, info = env.step(action)
    state2 = prepare multi state(state1, state2)
     state1=state2
     env.render()
env.close()
```

There's not much to explain here if you followed the training loop; we're just extracting the part that runs the network forward and takes an action. Notice that we still use an epsilon-greedy policy with epsilon set to 0.1. Even during inference, the agent needs a little bit of randomness to keep it from getting stuck. One difference to notice is that in test (or inference) mode, we only enact the action once and not six times like we did in training. Assuming you get the same results as us, your trained agent should make fairly consistent forward progress and should be able to jump over obstacles (figure 8.20). Congratulations!

![](2__page_28_Picture_2.jpeg)

Figure 8.20 The Mario agent trained only from intrinsic rewards successfully jumping over a chasm. This demonstrates it has learned basic skills without any explicit rewards to do so. With a random policy, the agent would not even be able to move forward, let alone learn to jump over obstacles.

If you're not getting the same results, try changing the hyperparameters, particularly the learning rate, mini-batch size, maximum episode length, and minimum forward progress. Training for 5,000 epochs with intrinsic rewards works, but in our experience it's sensitive to these hyperparameters. Of course, 5,000 epochs is not very long, so training for longer will result in more interesting behavior.

### How will this work in other environments?

We trained our DQN agent with an ICM-based reward on a single environment, Super Mario Bros, but the paper "Large-Scale Study of Curiosity-Driven Learning" by Yuri Burda et al. (2018) demonstrated how effective intrinsic rewards alone can be. They ran a number of experiments using curiosity-based rewards across multiple games, finding that a curious agent could progress through 11 levels in Super Mario Bros. and could learn to play Pong, among other games. They used essentially the same ICM we just built, except they used a more sophisticated actor-critic model called *proximal policy optimization* (PPO) rather than DQN.

An experiment you can try is to replace the encoder network with a *random projection*. A random projection just means multiplying the input data by a randomly initialized matrix (e.g., a randomly initialized neural network that is fixed and not trained). The Burda et al. 2018 paper demonstrated that a random projection works almost as well as the trained encoder.

# *8.7 Alternative intrinsic reward mechanisms*

In this chapter we described the serious problem faced by RL agents in environments with sparse rewards. We considered the solution to be imbuing agents with a sense of curiosity, and we implemented an approach from the Pathak et al. 2017 paper, one of the most widely cited papers in reinforcement learning research in recent years. We chose to demonstrate this approach not just because it is popular, but because it builds on what we've learned in previous chapters without introducing too many new notions. Curiosity-based learning (which goes by many names) is a very active area of research, and there are many alternative approaches, some of which we think are better than the ICM.

 Many of the other exciting methods use Bayesian inference and information theory to come up with novel mechanisms to drive curiosity. The prediction error (PE) approach we used in this chapter is just one implementation under a broader PE umbrella. The basic idea, as you now know, is that the agent wants to reduce its PE (or in other words, its uncertainty about the environment), but it must do so by actively seeking out novelty lest it be surprised by something unexpected.

 Another umbrella is that of agent *empowerment.* Rather than seeking to minimize prediction error and make the environment more predictable, empowerment strategies optimize the agent to maximize its control over the environment (figure 8.21). One paper in this area is "Variational Information Maximisation for Intrinsically Motivated Reinforcement Learning" by Shakir Mohamed and Danilo Jimenez Rezende (2015). We can make the informal statement about maximizing control over the environment into a precise mathematical statement (which we will only approximate here).

 The premise relies on the quantity called *mutual information* (MI). We will not define it mathematically here, but informally, MI measures how much information is shared between two sources of data called *random variables* (because usually we deal with data that has some amount of randomness or uncertainty). Another less tautological definition is that MI measures how much your uncertainty about one quantity, *x*, is reduced given another quantity, *y*.

 Information theory was first developed with real-world communication problems in mind, where one problem is how to best encode messages across a possibly noisy communication channel so that the received message is the least corrupted (figure 8.22). Suppose we have an original message *x* that we want to send across a noisy communication line (e.g., using radio waves), and we want to maximize the mutual information

![](2__page_30_Figure_1.jpeg)

Figure 8.21 The two main approaches for solving the sparse reward problem with curiosity-like methods are prediction error methods, like the one we used in this chapter, and empowerment methods. Rather than trying to maximize the prediction error between a given state and the next predicted state, empowerment methods aim to maximize the mutual information (MI) between the agent's actions and the next states. If the MI between the agent's action and the next state is high, that means the agent has a high level of control (or power) over the resulting next states (i.e., if you know which action the agent took, you can predict the next state well). This incentivizes the agent to learn how to maximally control the environment.

![](2__page_30_Figure_3.jpeg)

Figure 8.22 Claude Shannon developed communication theory, which was born from the need to encode messages efficiently and robustly across noisy communication channels as depicted here. The goal is to encode the message such that the mutual information between the received message and the sent message is maximal.

between *x* and the received message *y*. We do this by developing some way of encoding *x*, which might be a textual document, into a pattern of radio waves that minimizes the probability of the data being corrupted by noise. Once someone else receives the decoded message, *y*, they can be assured that their received message is very close to the original message.

#### *Summary* **241**

 In our example, *x* and *y* were both some sort of written message, but *x* and *y* need not be the same type of quantities. For example, we can ask what the mutual information is between the one-year stock price history of a company and its annual revenue: If we start with a very uncertain estimate about the annual revenue of a company, and then we learn the one-year stock price history, how much is our uncertainty reduced? If it's reduced a lot, the MI is high.

 That example involved different quantities, but both used the units of dollars that need not be the case either. We could ask what the MI is between the daily temperature and the sales of ice cream shops.

 In the case of agent empowerment in reinforcement learning, the objective is to maximize the mutual information between an action (or sequence of actions) and the resulting future state (or states). Maximizing this objective means that if you know what action the agent took, you will have a high confidence about what the resulting state was. This means the agent has a high degree of control over the environment, since it can reliably reach states given its actions. Hence, a maximally empowered agent has maximal degrees of freedom.

 This is different than the prediction-error approach because minimizing PE directly encourages exploration, whereas maximizing empowerment may induce exploratory behavior as a means to learn empowering skills, but only indirectly. Consider a young woman, Sarah, who decides to travel the world and explore as much as possible. She is reducing her uncertainty about the world. Compare her to Bill Gates, who by being extraordinarily rich, has a high degree of power. He may not be interested in traveling as much as Sarah, but he can if he wants, and no matter where he is at any time, he can go where he wants to go.

 Both empowerment and curiosity objectives have their use cases. Empowermentbased objectives have been shown to be useful for training agents to acquire complex skills without any extrinsic reward (e.g., robotic tasks or sports games), whereas curiosity-based objectives tend to be more useful for exploration (e.g., games like Super Mario Bros. where the goal is to progress through levels). In any case, these two metrics are more similar than they are different.

## *Summary*

- The sparse reward problem is when an environment rarely produces a useful reward signal, which severely challenges the way ordinary DRL attempts to learn.
- The sparse reward problem can be solved by creating synthetic reward signals that we call curiosity rewards.
- A curiosity module creates synthetic rewards based on how unpredictable the next state of the environment is, encouraging the agent to explore more unpredictable parts of the environment.
- The intrinsic curiosity module (ICM) consists of three independent neural networks: a forward-prediction model, an inverse model, and an encoder.

- The encoder encodes high-dimensional states into a low-dimensional vector with high-level features (which removes noise and trivial features).
- The forward-prediction model predicts the next encoded state, and its error provides the curiosity signal.
- The inverse model trains the encoder by taking two successive encoded states and predicting the action that was taken.
- Empowerment is a closely related but alternative approach to curiosity-based learning. In empowerment, the agent is incentivized to learn how to maximize the amount of control it has over the environment.