## *Tackling more complex problems with actor-critic methods*

## *This chapter covers*

- The limitations of the REINFORCE algorithm
- **Introducing a** *critic* to improve sample efficiency and decrease variance
- **Using the advantage function to speed up** convergence
- **Speeding up the model by parallelizing training**

In the previous chapter we introduced a vanilla version of a policy gradient method called REINFORCE. This algorithm worked fine for the simple CartPole example, but we want to be able to apply reinforcement learning to more complex environments. You already saw that deep Q-networks can be quite effective when the action space is discrete, but it has the drawback of needing a separate policy function such as epsilon-greedy. In this chapter you'll learn how to combine the advantages of REINFORCE and those of DQN to create a class of algorithms called actor-critic models. These have proven to yield state-of-the-art results in many domains.

 The REINFORCE algorithm is generally implemented as an *episodic algorithm*, meaning that we only apply it to update our model parameters after the agent has completed an entire episode (and collected rewards along the way). Recall that the

policy is a function,  $\pi S \rightarrow P(a)$ . That is, it's a function that takes a state and returns a probability distribution over actions (figure 5.1).

![](_page_1_Figure_2.jpeg)

Figure 5.1 A policy function takes a state and returns a probability distribution over actions, where a higher probability indicates an action that is more likely to result in the highest reward.

Then we sample from this distribution to get an action, such that the most probable action (the "best" action) is most likely to be sampled. At the end of the episode, we compute the *return* of the episode, which is essentially the sum of the discounted rewards in the episode. The return is calculated as

$$
R = \sum_{t} \gamma_t \cdot r_t
$$

After the game is over, the return for that episode is the sum of all the rewards acquired, multiplied by their respective discount rate, where γ*t* exponentially decays as a function of time. For example, if action 1 was taken in state *A* and resulted in a return of +10, the probability of action 1 given state *A* will be increased a little, whereas if action 2 was taken in state *A* and resulted in a return of –20, the probability of action 2 given state *A* will decrease. Essentially, we minimize this loss function:

$$
Loss = -log(P(a|S)) \cdot R
$$

This says "minimize the logarithm of the probability of the action *a* given state *S* times the return *R*." If the reward is a big positive number, and  $P(a_1 | S_A) = 0.5$  for example, minimizing this loss will involve increasing this probability. So with REINFORCE we just keep sampling episodes (or trajectories more generally) from the agent and environment, and periodically update the policy parameters by minimizing this loss.

NOTE Remember, we only apply the logarithm to the probability because a probability is bounded by 0 and 1, whereas the log probability is bounded by  $-\infty$ (negative infinity) and 0. Given that numbers are represented by a finite number of bits, we can represent very small (close to 0) or very large (close to 1) probabilities without underflowing or overflowing the computer's numerical precision. Logarithms also have nicer mathematical properties that we won't cover, but that is why you'll almost always see log probabilities used in algorithms and machine learning papers, even though we are conceptually interested in the raw probabilities themselves.

By sampling a full episode, we get a pretty good idea of the true value of an action because we can see its downstream effects rather than just its immediate effect (which may be misleading due to randomness in the environment); this full episode sampling is under the umbrella of Monte Carlo approaches. But not all environments are episodic, and sometimes we want to be able to make updates in an incremental or *online* fashion, i.e., make updates at regular intervals irrespective of what is going on in the environment. Our deep Q-network did well in the non-episodic setting and it could be considered an online-learning algorithm, but it required an experience replay buffer in order to effectively learn.

 The replay buffer was necessary because true online learning where parameter updates are made after each action is unstable due to the inherent variance in the environment. An action taken once may by chance result in a big negative reward, but in expectation (the average long-term rewards) it may be a good action—updating after a single action may result in erroneous parameter updates that will ultimately prevent adequate learning.

 In this chapter, we will introduce a new kind of policy gradient method called *distributed advantage actor-critic* (DA2C) that will have the online-learning advantages of DQN without a replay buffer. It will also have the advantages of policy methods where we can directly sample actions from the probability distribution over actions, thereby eliminating the need for choosing a policy (such as the epsilon-greedy policy) that we needed with DQN.

## *5.1 Combining the value and policy function*

The great thing about Q-learning is that it learns directly from the available information in the environment, which are the rewards. It basically learns to predict rewards, which we call values. If we use a DQN to play pinball, it will learn to predict the values for the two main actions—operating the left and right paddles. We're then free to use these values to decide which action to take, generally opting for the action associated with the highest value.

 A policy gradient function is more directly connected to the concept of *reinforcement*, since we positively reinforce actions that result in a positive reward and negatively reinforce actions that lead to a negative reward. Hence, the policy function learns which actions are best in a more hidden way. In pinball, if we hit the left paddle and score a bunch of points, that action will get positively reinforced and will be more likely to be selected the next time the game is in a similar state.

 In other words, Q-learning (such as DQN) uses a trainable function to directly model the value (the expected reward) of an action, given a state. This is a very intuitive way of solving a Markov decision process (MDP) since we only observe states and rewards—it makes sense to predict the rewards and then just take actions that have high predicted rewards. On the other hand, we saw the advantage of direct policy learning (such as policy gradients). Namely, we get a true conditional probability distribution over actions,  $P(a|S)$ , that we can directly sample from to take an action.

Naturally, someone decided it might be a good idea to combine these two approaches to get the advantages of both.

 In building such a combined value-policy learning algorithm, we will start with the policy learner as the foundation. There are two challenges we want to overcome to increase the robustness of the policy learner:

- We want to improve the sample efficiency by updating more frequently.
- We want to decrease the variance of the reward we used to update our model.

These problems are related, since the reward variance depends on how many samples we collect (more samples yields less variance). The idea behind a combined value-policy algorithm is to use the value learner to reduce the variance in the rewards that are used to train the policy. That is, instead of minimizing the REINFORCE loss that included direct reference to the observed return, *R*, from an episode, we instead add a baseline value such that the loss is now:

![](_page_3_Figure_6.jpeg)

Here, *V* (*S*) is the value of state *S*, which is the state-value function (a function of the state) rather than an action-value function (a function of both state and action), although an action-value function could be used as well. This quantity,  $V(S) - R$ , is termed the *advantage*. Intuitively, the advantage quantity tells you how much better an action is, relative to what you expected.

NOTE Remember that the value function (state value or action value) implicitly depends on the choice of policy, so we ought to write  $V_\pi(S)$  to make it explicit; however, we drop the  $\pi$  subscript for notational simplicity. The policy's influence on the value is crucial, since a policy of taking random actions all the time would result in all states being of more or less equally low value.

Imagine that we're training a policy on a Gridworld game with discrete actions and a small discrete state-space, such that we can use a vector where each position in the vector represents a distinct state, and the element is the average rewards observed after that state is visited. This look-up table would be the  $V(S)$ . We might sample action 1 from the policy and observe reward +10, but then we'd use our value look-up table and see that on average we get +4 after visiting this state, so the advantage of action 1 given this state is  $10 - 4 = +6$ . This means that when we took action 1, we got a reward that was significantly better than what we expected based on past rewards from that state, which suggests that it was a good action. Compare this to the case where we take action 1 and receive reward +10 but our value look-up table says we expected to see

+15, so the advantage is  $10 - 15 = -5$ . That suggests this was a relatively bad action despite the fact that we received a reasonably large positive reward.

 Rather than using a look-up table, we will use some sort of parameterized model, such as a neural network that can be trained to predict expected rewards for a given state. So we want to simultaneously train a policy neural network and a state-value or action-value neural network.

 Algorithms of this sort are called *actor-critic* methods, where "actor" refers to the policy, because that's where the actions are generated, and "critic" refers to the value function, because that's what (in part) tells the actor how good its actions are. Since we're using  $R - V(S)$  to train the policy rather than just  $V(S)$ , this is called *advantage actor-critic* (figure 5.2).

![](_page_4_Figure_4.jpeg)

Figure 5.2 Q-learning falls under the category of value methods, since we attempt to learn action values, whereas policy gradient methods like REINFORCE directly attempt to learn the best actions to take. We can combine these two techniques into what's called an actor-critic architecture.

NOTE What we have described so far would not be considered a true actorcritic method by some, because we're only using the value function as a baseline and not using it to "bootstrap" by making a prediction about a future state based on the current state. You will see how bootstrapping comes into play soon.

The policy network has a sensitive loss function that depends on the rewards collected at the end of the episode. If we naively tried to make online updates with the wrong type of environment, we might never learn anything because the rewards might be too sparse.

 In Gridworld, which we introduced in chapter 3, the reward is –1 on every move except for the end of the episode. The vanilla policy gradient method wouldn't know what action to reinforce, since most actions result in the same reward of  $-1$ . In contrast, a Q-network can learn decent Q values even when the rewards are sparse, because it *bootstraps*. When we say an algorithm bootstraps, we mean it can make a prediction from a prediction.

 If we ask you what the temperature will be like two days from now, you might first predict what the temperature will be tomorrow, and then base your 2-day prediction on that (figure 5.3). You're bootstrapping. If your first prediction is bad, your second may be even worse, so bootstrapping introduces a source of *bias*. Bias is a systematic deviation from the true value of something, in this case from the true Q values. On

the other hand, making predictions from predictions introduces a kind of self-consistency that results in lower *variance*. Variance is exactly what it sounds like: a lack of precision in the predictions, which means predictions that vary a lot. In the temperature example, if we make our day 2 temperature prediction based on our day 1 prediction, it will likely not be too far from our day 1 prediction.

![](_page_5_Figure_2.jpeg)

Figure 5.3 Read from left to right, raw data is fed into a predict temperature model that predicts the next day's temperature. That prediction is then used in another prediction model that predicts day 2's temperature. We can keep doing this, but initial errors will compound and our predictions will become inaccurate for distant predictions.

Bias and variance are key concepts relevant to all of machine learning, not just deep learning or deep reinforcement learning (figure 5.4). Generally, if you reduce bias you will increase variance, and vice versa (figure 5.5). For example, if we ask you to predict the temperature for tomorrow and the next day, you could give us a specific temperature: "The 2-day temperature forecast is 20.1 C and 20.5 C." This is a high-precision prediction—you've given us a temperature prediction to a tenth of a degree! But you don't have a crystal ball, so your prediction is almost surely going to be systematically off, biased toward whatever your prediction procedure involved. Or you could have told us,

![](_page_5_Figure_5.jpeg)

Figure 5.4 The bias-variance tradeoff is a fundamental machine learning concept that says any machine learning model will have some degree of systematic deviation from the true data distribution and some degree of variance. You can try to reduce the variance of your model, but it will always come at the cost of increased bias.

![](_page_6_Figure_1.jpeg)

Figure 5.5 The bias-variance tradeoff. Increasing model complexity can reduce bias, but it will increase variance. Reducing variance will increase bias.

"The 2-day temperature forecast is 15–25 C and 18–27 C." In this case, your prediction has a lot of spread, or variance, since you're giving fairly wide ranges, but it has low bias, meaning that you have a good chance of the real temperatures falling in your intervals. This spread might be because your prediction algorithm didn't give undue weight to any of the variables used for prediction, so it's not particularly biased in any direction. Indeed, machine learning models are often *regularized* by imposing a penalty on the magnitude of the parameters during training; i.e., parameters that are significantly bigger or smaller than 0 are penalized. Regularization essentially means modifying your machine learning procedure in a way to mitigate overfitting.

 We want to combine the potentially high-bias, low-variance value prediction with the potentially low-bias, high-variance policy prediction to get something with moderate bias and variance—something that will work well in the online setting. The role of the critic is hopefully starting to become clear. The actor (the policy network) will take a move, but the critic (the state-value network) will tell the actor how good or bad the action was, rather than only using the potentially sparse raw reward signals from the environment. Thus the critic will be a term in the actor's loss function. The critic, just like with Q-learning, will learn directly from the reward signals coming from the environment, but the sequence of rewards will depend on the actions taken by the actor, so the actor affects the critic too, albeit more indirectly (figure 5.6).

![](_page_6_Figure_5.jpeg)

Figure 5.6 The general overview of actor-critic models. First, the actor predicts the best action and chooses the action to take, which generates a new state. The critic network computes the value of the old state and the new state. The relative value of S<sub>t+1</sub> is called its advantage, and this is the signal used to reinforce the action that was taken by the actor.

The actor is trained in part by using signals coming from the critic, but how exactly do we train a state-value function as opposed to the action value (Q) functions we're more accustomed to? With action values, we computed the expected return (the sum of future discounted rewards) for a given state-action pair. Hence, we could predict whether a state-action pair would result in a nice positive reward, a bad negative reward, or something in between. But recall that with our DQN, our Q-network returned separate action values for each possible discrete action, so if we employ a reasonable policy like epsilon-greedy, the state value will essentially be the highest action value. Thus, the state-value function just computes this highest action value rather than separately computing action values for each action.

## *5.2 Distributed training*

As we mentioned in the introduction, our goal in this chapter is to implement a model called distributed advantage actor-critic (DA2C), and we've discussed the "advantage actor-critic" part of the name at a conceptual level. Let's do the same for the "distributed" part now.

 For virtually all deep learning models we do *batch training*, where a random subset of our training data is batched together and we compute the loss for this entire batch before we backpropagate and do gradient descent. This is necessary because the gradients, if we trained with single pieces of data at a time, would have too much variance, and the parameters would never converge on their optimal values. We need to average out the noise in a batch of data to get the real signal before updating the model parameters.

 For example, if you're training an image classifier to recognize hand-drawn digits, and you train it with one image at a time, the algorithm would think that the background pixels are just as important as the digits in the foreground; it can only see the signal when averaged together with other images. The same concept applies in reinforcement learning, which is why we had to use an experience replay buffer with DQN.

 Having a sufficiently large replay buffer requires a lot of memory, and in some cases a replay buffer is impractical. A replay buffer is possible when your reinforcement learning environment and agent algorithm follow the strict criteria of a Markov decision process, and in particular, the Markov property. Recall the Markov property says that the optimal action for a state  $S_t$  can be computed without reference to any prior states  $S_{t-1}$ ; there is no need to keep a history of previously visited states. For simple games, this is the case, but for more complex environments, it may be necessary to remember the past in order to select the best option now.

 Indeed, in many complex games it is common to use recurrent neural networks (RNNs) like a long short-term memory (LSTM) network or a gated recurrent unit (GRU). These RNNs can keep an internal state that can store traces of the past (figure 5.7). They are particularly useful for natural language processing (NLP) tasks where keeping track of preceding words or characters is critical to being able to

![](_page_8_Figure_1.jpeg)

Figure 5.7 A generic recurrent neural network (RNN) layer processes a sequence of data by incorporating its previous output with the new input. The input on the left, along with a previous output is fed into an RNN module, which then produces an output. The output is fed back into the RNN on the next time step, and a copy may be fed into another layer. An RNN will not work properly with single experiences in an experience replay buffer since it needs to work on sequences of experiences.

encode or decode a sentence. Experience replay doesn't work with an RNN unless the replay buffer stores entire trajectories or full episodes, because the RNN is designed to process sequential data.

 One way to use RNNs without an experience replay is to run multiple copies of the agent in parallel, each with separate instantiations of the environment. By distributing multiple independent agents across different CPU processes (figure 5.8), we can collect a varied set of experiences and therefore get a sample of gradients that we can average together to get a lower variance mean gradient. This eliminates the need for experience replay and allows us to train an algorithm in a completely online fashion, visiting each state only once as it appears in the environment.

![](_page_8_Figure_5.jpeg)

Figure 5.8 The most common form of training a deep learning model is to feed a batch of data together into the model to return a batch of predictions. Then we compute the loss for each prediction and average or sum all the losses before backpropagating and updating the model parameters. This averages out the variability present across all the experiences. Alternatively, we can run multiple models with each taking a single experience and making a single prediction, backpropagate through each model to get the gradients, and then sum or average the gradients before making any parameter updates.
## Multiprocessing versus multithreading

Modern desktop and laptop computers have central processing units (CPUs) with multiple cores, which are independent processing units capable of running computations simultaneously. Therefore, if you can split a computation into pieces that can be computed separately and combined later, you can get dramatic speed increases. The operating system software abstracts the physical CPU processors into virtual processes and threads. A process contains its own memory space, and threads run within a single process. There are two forms of parallel computations, *multithreading* and *multiprocessing*, and only in the latter form are computations performed truly simultaneously. In multiprocessing, computations are performed simultaneously on multiple, physically distinct processing units such as CPU or GPU cores.

![](0__page_9_Figure_3.jpeg)

Processes are an abstraction of the underlying CPU hardware created by the operating system. If you have two CPUs, you can run two simultaneous processes. However, the operating system will let you spawn more than two virtual processes, and it will figure out how to multitask between them. Each process has its own memory address space and can have multiple threads (tasks). While one thread is waiting for an external process to finish (such as an input/output operation), the OS can let another thread run. This maximizes the use of whatever CPUs you have.

Multithreading is like when people multitask: they can work on only one thing at a time but they switch between different tasks while another task is idle. Therefore, tasks are not truly performed simultaneously with multithreading; it is a software-level mechanism to improve efficiency in running multiple computations. Multithreading is really effective when your task requires a lot of input/output operations, such as reading and writing data to the hard disk. When data is being read into RAM from the hard disk, computation on the CPU is idle as it waits for the required data, and the operating system can use that idle CPU time to work on a different task and then switch back when the I/O operation is done.

Machine learning models generally do not require I/O operations; machine learning is limited by computation speed, so it benefits from true simultaneous computation with multiprocessing.

Large machine learning models all but require graphics processing units (GPUs) to perform efficiently, but distributed models on multiple CPUs can be competitive in some cases. Python provides a library called "multiprocessing" that makes multiprocessing very easy. Additionally, PyTorch wraps this library and has a method for allowing a model's parameters to be shared across multiple processes. Let's look at a simple example of multiprocessing.

 As a contrived simple example, suppose we have an array with the numbers 0, 1, 2, 3 … 64 and we want to square each number. Since squaring a number does not depend on any other numbers in the array, we can easily parallelize this across multiple processors.

```
Listing 5.1 Introduction to multiprocessing
import multiprocessing as mp
                                   This function takes an array 
import numpy as np
                                  and squares each element.
def square(x): 
return np.square(x)
                            Sets up an array with a 
                         \leftarrowx = np.arange(64)sequence of numbers
>>> print(x)
array([ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
        17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
        34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
        51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63])
>>> mp.cpu_count()
                                 Sets up a multiprocessing 
     8
                                  processor pool with 8 processes
pool = mp.Pool(8)squared = pool.map(square, [x[8*1:8*1+8] for i in range(8)]) \leftarrowUses the pool's 
>>> squared
                                                                       map function to 
[array([ 0, 1, 4, 9, 16, 25, 36, 49]),
                                                                       apply the square 
 array([ 64, 81, 100, 121, 144, 169, 196, 225]),
                                                                       function to each 
  array([256, 289, 324, 361, 400, 441, 484, 529]),
                                                                       array in the list 
  array([576, 625, 676, 729, 784, 841, 900, 961]),
                                                                       and returns the 
  array([1024, 1089, 1156, 1225, 1296, 1369, 1444, 1521]),
                                                                     results in a list array([1600, 1681, 1764, 1849, 1936, 2025, 2116, 2209]),
  array([2304, 2401, 2500, 2601, 2704, 2809, 2916, 3025]),
  array([3136, 3249, 3364, 3481, 3600, 3721, 3844, 3969])]
```

Here we define a function, square, that takes an array and squares it. This is the function that will get distributed across multiple processes. We create some sample data that is simply the list of numbers from 0 to 63, and rather than sequentially squaring them in a single process, we chop up the array into 8 pieces and compute the squares for each piece independently on a different processor (figure 5.9).

 You can see how many hardware processors your computer has by using the mp.cpu count () function. You can see in listing  $5.1$  that we have 8. Many modern computers may have 4 independent hardware processors, but they will have twice as many "virtual" processors via something called *hyperthreading*. Hyperthreading is a performance trick some processors use that can allow two processes to run essentially simultaneously on one physical processor. It is important not to create more processes

![](0__page_11_Figure_1.jpeg)

Figure 5.9 A simple multiprocessing example. We want to more efficiently square all the numbers in an array. Rather than squaring each element one by one, we can split the array into two pieces and send each piece to a different processor that will square them simultaneously. Then we can recombine the pieces back into a single array.

than there are CPUs on your machine, as the additional processes will essentially function as threads, and the CPU will have to rapidly switch between processes.

 In listing 5.1 we set up a processor pool of 8 processes with mp.Pool(8), and then we used pool.map to distribute the square function across the 8 pieces of data. You can see we get a list of 8 arrays with all their elements squared, just as we wanted. Processes will return as soon as they're complete, so the order of the elements in the returned list may not always be in the order they were mapped.

 We're going to need a bit more control over our processes than a processor pool allows, so we will create and start a bunch of processes manually.

![](0__page_11_Figure_6.jpeg)

```
for proc in processes: 
proc.terminate()
results = []
while not queue.empty(): 
     results.append(queue.get())
>>> results
[array([ 0, 1, 4, 9, 16, 25, 36, 49]),
 array([256, 289, 324, 361, 400, 441, 484, 529]),
  array([ 64, 81, 100, 121, 144, 169, 196, 225]),
 array([1600, 1681, 1764, 1849, 1936, 2025, 2116, 2209]),
  array([576, 625, 676, 729, 784, 841, 900, 961]),
  array([1024, 1089, 1156, 1225, 1296, 1369, 1444, 1521]),
  array([2304, 2401, 2500, 2601, 2704, 2809, 2916, 3025]),
  array([3136, 3249, 3364, 3481, 3600, 3721, 3844, 3969])]
                                Terminates each 
                                 process 
                                      Converts the multiprocessing 
                                      queue into a list
```

This is more code, but functionally it's the same as what we did before with the Pool. Now, though, it's easy to share data between processes using special shareable data structures in the multiprocessing library, and we have more control over the processes.

 We modified our square function a little to accept an integer representing the process ID, the array to square, and a shared global data structure called a queue that we can put data into and extract data from using the .get() method.

 To run through the code, we first set up a list to hold the instances of our processes, we created the shared queue object, and we created our sample data as before. We then define a loop to create (in our case) 8 processes and start them using the .start() method. We add them to our processes list so we can access them later. Next we run through the processes list and call each process's .join() method; this lets us wait to return anything until all the processes have finished. Then we call each process's .terminate() method to ensure it is killed. Lastly, we collect all the elements of the queue into a list and print it out.

 The results look the same as with the process pool, except they were in a random order. That's really all there is to distributing a function across multiple CPU processors.

## *5.3 Advantage actor-critic*

Now that we know how to distribute computation across processes, we can get back to the real reinforcement learning. In this section we'll put together the pieces of the full distributed advantage actor-critic model. To allow fast training and to compare the results to the previous chapter, we will again use the CartPole game as our test environment. If you choose, though, you can easily adapt the algorithm to a more difficult game such as Pong in OpenAI Gym; you can find such an implementation on this chapter's GitHub page: [http://mng.bz/JzKp.](http://mng.bz/JzKp)

 So far we've presented the actor and critic as two separate functions, but we can combine them into a single neural network with two output "heads." That's what we'll do in the following code. Instead of a normal neural network that returns a single vector, it can return two different vectors: one for the policy and one for the value. This allows for some parameter sharing between the policy and value that can make things

more efficient, since some of the information needed to compute values is also useful for predicting the best action for the policy. But if a two-headed neural network seems too exotic right now, you can go ahead and write two separate neural networks—it will work just fine. Let's look at some pseudocode for the algorithm. Then we'll translate it to Python.

![](0__page_13_Figure_2.jpeg)

This is very simplified pseudocode, but it gets the main idea across. The important part to point out is the advantage calculation. Consider the case where we take an action, we receive reward +10, the value prediction is +5, and the value prediction for the next state is +7. Since future predictions are always less valuable than the currently observed reward, we discount the value of the next state by the gamma discount factor. Our advantage =  $10 + 0.9 * 7 - 5 = 10 + (6.3 - 5) = 10 + 1.3 = +11.3$ . Since the difference between the next state value and the current state value is positive, it increases the overall value of the action we just took, so we will reinforce it more. Notice that the advantage function *bootstraps* because it computes a value for the current state and action based on predictions for a future state.

 In this chapter we're going to use our DA2C model on CartPole again, which is episodic, so if we do a full Monte Carlo update where we update after the full episode is complete, value next will always be 0 for the last move since there is no next state when the episode is over. In this case, the advantage term actually reduces to advantage = reward – value, which is the value baseline we discussed at the beginning of the chapter. The full advantage expression,  $A = r_{t+1} + \gamma * v(s_{t+1}) - v(s_t)$ , is used when we do online or *N-step learning*.

![](0__page_13_Figure_5.jpeg)

*N*-step learning is what's in between fully online learning and waiting for a full episode before updating (i.e., Monte Carlo). As the name suggests, we accumulate rewards over *N* steps and then compute our loss and backpropagate. The number of steps can be anywhere from 1, which reduces to fully online learning, to the maximum number of steps in the episode, which is Monte Carlo. Usually we pick something in between to get the advantages of both. We will first show the episodic actor-critic algorithm, and then we will adapt it to *N*-step with *N* set to 10.

 Figure 5.10 shows the broad overview of an actor-critic algorithm. An actor-critic model needs to produce both a state value and action probabilities. We use the action probabilities to select an action and receive a reward, which we compare with the state value to compute an advantage. The advantage is ultimately what we use to reinforce the action and train the model.

![](0__page_14_Figure_3.jpeg)

Figure 5.10 An actor-critic model produces a state value and action probabilities, which are used to compute an advantage value and this is the quantity that is used to train the model rather than raw rewards as with just Q-learning.

With that in mind, let's get to coding an actor-critic model to play CartPole. Here's the sequence of steps.

- <sup>1</sup> Set up our actor-critic model, a two-headed model (or you can set up two independent actor and critic networks). The model accepts a CartPole state as input, which is a vector of 4 real numbers. The actor head is just like the policy network (actor) from the previous chapter, so it outputs a 2-dimensional vector representing a discrete probability distribution over the 2 possible actions. The critic outputs a single number representing the state value. The critic is denoted  $v(s)$  and the actor is denoted  $\pi(s)$ . Remember that  $\pi(s)$  returns the log probabilities for each possible action, which in our case is 2 actions.
- <sup>2</sup> While we're in the current episode
  - **a** Define the hyperparameter:  $\gamma$  (gamma, discount factor).
  - <sup>b</sup> Start a new episode, in initial state *st*.
  - **c** Compute the value  $v(s_t)$  and store it in the list.

- d Compute  $\pi(s_i)$ , store it in the list, sample, and take action  $a_i$ . Receive the new state  $s_{t+1}$  and the reward  $r_{t+1}$ . Store the reward in the list.
- <sup>3</sup> Train
  - a Initialize  $R = 0$ . Loop through the rewards in reverse order to generate returns:  $R = r_i + \gamma * R$ .
  - **b** Minimize the actor loss:  $-1 * \gamma_i * (R v(s_i)) * \pi(a|s)$ .
  - Minimize the critic loss:  $(R-v)^2$ .
- <sup>4</sup> Repeat for a new episode.

The following listing implements these steps in Python.

![](0__page_15_Figure_8.jpeg)

For CartPole, we have a fairly simple neural network, apart from having two output heads. In listing 5.4 we first normalize the input so that the state values are all within the same range; then the normalized input is fed through the first two layers, which are ordinary linear layers with the ReLU activation functions. Then we fork the model into two paths.

 The first path is the actor head that takes the output of layer 2 and applies another linear layer and then the log softmax function. The log softmax is logically equivalent to doing  $log(softmax(...)))$ , but the combined function is more numerically stable because if you compute the functions separately you might end up with overflowed or underflowed probabilities after the softmax.

 The second path is the critic head, which applies a linear layer and ReLU to the output of layer 2, but notice that we call  $y \cdot$  detach(), which detaches the y node from the graph so the critic's loss won't backpropagate and modify the weights in layers 1 and 2 (figure 5.11). Only the actor will cause these weights to be modified. This prevents conflict between what the actor and critic want when the actor and critic are trying to make opposing updates to the earlier layers. With two-headed models, it often makes sense to make one head dominant and allow it to control most of the parameters by detaching the other head from the first several layers. Lastly, the critic applies another linear layer with the tanh activation function that bounds the output to the interval  $(-1,1)$ , which is perfect for CartPole since the rewards are  $+1$  and  $-1$ .

![](0__page_16_Figure_2.jpeg)

Figure 5.11 This is an overview of the architecture for our two-headed actor-critic model. It has two shared linear layers and a branching point where the output of the first two layers is sent to a logsoftmax layer of the actor head and also to a ReLU layer of the critic head before finally passing through a tanh layer, which is an activation function that restricts output between -1 and 1. This model returns a 2-tuple of tensors rather than a single tensor. Notice that the critic head is detached (indicated by the dotted line), which means we do not backpropagate from the critic head into the actor head or the beginning of the model. Only the actor backpropagates through the beginning of the model.

In the following listing we develop the code necessary for distributing multiple instances of the actor-critic model across different processes.

![](0__page_16_Figure_5.jpeg)

![](0__page_17_Figure_1.jpeg)

This is exactly the same setup we had when we demonstrated how to split up an array across multiple processes, except this time we're going to be running a function called worker that will run our CartPole reinforcement learning algorithm.

 Next we'll define the worker function, which will run a single agent in an instance of the CartPole environment.

|                                                                                                | Listing 5.6 The main training loop                                                                                                                                         |                                                                                                             |  |                                                                         |                                                                                                                                     |  |                                                                                          |                                                                                                                                                                      |  |
|------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|--|-------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|--|------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|
|                                                                                                |                                                                                                                                                                            | def worker(t, worker model, counter, params):<br>worker env = gym.make("CartPole-v1")<br>worker env.reset() |  |                                                                         |                                                                                                                                     |  | Each process runs its own isolated<br>environment and optimizer but<br>shares the model. |                                                                                                                                                                      |  |
| We use the<br>collected<br>data from<br>run episode<br>to run one<br>parameter<br>update step. | worker $opt = optim$ . Adam ( $lr = 1e-4$ , params=worker model. parameters ())<br>worker opt.zero qrad()<br>for i in range (params ['epochs']):<br>worker opt.zero qrad() |                                                                                                             |  |                                                                         |                                                                                                                                     |  |                                                                                          |                                                                                                                                                                      |  |
|                                                                                                |                                                                                                                                                                            |                                                                                                             |  | actor loss, critic loss, eplen =<br>$counter.value = counter.value + 1$ | update params (worker opt, values, logprobs, rewards)<br>counter is a globally shared counter<br>between all the running processes. |  |                                                                                          | values, logprobs, rewards = run episode (worker env, worker model)<br>The run_episode function<br>plays an episode of the<br>game, collecting data<br>along the way. |  |

The worker function is the function that each individual process will run separately. Each worker (i.e., process) will create its own CartPole environment and its own optimizer but will share the actor-critic model, which is passed in as an argument to the function. Since the model is shared, whenever a worker updates the model parameters, they are updated for all the workers. This is shown at a high-level in figure 5.12.

 Since each worker is spawned in a new process that has its own memory, all the data the worker needs should be passed in as an argument to the function explicitly. This also prevents bugs.

 In listing 5.7 we define a function to run a single instance of the actor-critic model through one episode in the CartPole environment.
![](1__page_18_Figure_2.jpeg)

Figure 5.12 Within each process, an episode of the game is run using the shared model. The loss is computed within each process, but the optimizer acts to update the shared actor-critic model that is used by each process.

![](1__page_18_Figure_4.jpeg)

The run episode function just runs through a single episode of CartPole and collects the computed state values from the critic, log probabilities over actions from the actor, and rewards from the environment. We store these in lists and use them to compute

our loss function later. Since this is an actor-critic method and not Q-learning, we take actions by directly sampling from the policy rather than arbitrarily choosing a policy like epsilon-greedy in Q-learning. There's nothing too out of the ordinary in this function, so let's move on to the updating function.

![](1__page_19_Figure_2.jpeg)

The update params function is where all the action is, and it's what sets distributed advantage actor-critic apart from the other algorithms we've learned so far. First we take the lists of rewards, log probabilities, and state values and convert them to PyTorch tensors. We then reverse their order because we want to consider the most recent action first, and we make sure they are flattened 1D arrays by calling the .view(-1) method.

The actor loss is computed as we described earlier in this section with math, using the advantage (technically the baseline, since there's no bootstrapping) rather than the raw reward. Crucially, we must detach the values tensor from the graph when we use the actor loss, or we will backpropagate through the actor and critic heads, and we only want to update the actor head. The critic loss is a simple squared error between the state values and the returns, and we make sure *not* to detach here since we want to update the critic head. Then we sum the actor and critic losses to get the overall loss. We scale down the critic loss by multiplying by 0.1 because we want the actor to learn faster than the critic. We return the individual losses and the length of the rewards tensor (which indicates how long the episode lasted) to monitor their progress during training.

 The way we've set it up here, each worker will update the shared model parameters *asynchronously*, whenever it is done running an episode. We could have designed it such that we wait for all workers to finish running one episode and then sum their gradients together and update the shared parameters synchronously, but this is more complicated, and the asynchronous approach works well in practice.

 Put it all together and run it, and you'll get a trained CartPole agent within one minute on a modern computer running on just a few CPU cores. If you plot the loss over time for this, it probably won't be a nice down-trending line like you'd hope because the actor and critic are in competition with one another (figure 5.13). The critic is incentivized to model the returns as best as it can (and the returns depend on what the actor does), but the actor is incentivized to beat the expectations of the critic. If the actor improves faster than the critic, the critic's loss will be high, and vice versa, so there is a somewhat adversarial relationship between the two.

![](1__page_20_Figure_3.jpeg)

Figure 5.13 The actor and critic have a bit of an adversarial relationship since the actions that the agent take affect the loss of the critic, and the critic makes predictions of state values that get incorporated into the return that affects the training loss of the actor. Hence, the overall loss plot may look chaotic despite the fact that the agent is indeed increasing in performance.

Adversarial training like this is a very powerful technique in many areas of machine learning, not just reinforcement learning. For example, generative adversarial networks (GANs) are an unsupervised method for generating realistic-appearing synthetic samples of data from a training data set using a pair of models that function similarly to an actor and critic. In fact, we will build an even more sophisticated adversarial model in chapter 8.

 The take-home here is that if you're using an adversarial model, the loss will be largely uninformative (unless it goes to 0 or explodes toward infinity, in which case something is probably wrong). You have to rely on actually evaluating the objective you care about, which in our case is how well the agent is performing in the game. Figure 5.14 shows the plot of average episode length during the first 120 epochs (about 45 seconds of) training.

![](1__page_21_Figure_1.jpeg)

![](1__page_21_Figure_2.jpeg)

Figure 5.14 The mean episode length over training time for our Monte Carlo distributed advantage actor-critic model. This model is not considered a true critic, since the critic is not bootstrapping during training. As a result, the training performance has high variance.

## *5.4 N-step actor-critic*

In the last section, we implemented distributed advantage actor-critic, except that we trained in Monte Carlo mode—we ran a full episode before updating the model parameters. While that makes sense for a simple game like CartPole, usually we want to be able to make more frequent updates. We briefly touched on *N*-step learning before, but to reiterate, it means we simply calculate our loss and update the parameters after *N* steps, where *N* is whatever we choose it to be. If *N* is 1, this is fully online learning; if *N* is very large, it will be Monte Carlo again. The sweet spot is somewhere in between.

 With Monte Carlo full-episode learning, we don't take advantage of bootstrapping, since there's nothing to bootstrap. We do bootstrap in online learning, as we did with DQN, but with 1-step learning the bootstrap may introduce a lot of bias. This bias may be harmless if it pushes our parameters in the right direction, but in some cases the bias can be so off that we never move in the right direction.

 This is why *N*-step learning is usually better than 1-step (online) learning—the target value for the critic is more accurate, so the critic's training will be more stable and will be able to produce less biased state values. With bootstrapping, we're making a prediction from a prediction, so the predictions will be better if you're able to collect more data before making them. And we like bootstrapping because it improves sample efficiency; you don't need to see as much data (e.g., frames in a game) before updating the parameters in the right direction.

Let's modify our code to do *N*-step learning. The only function we need to modify is run\_episode. We need to change it to run for only *N* steps rather than wait for the episode to finish. If the episode finishes before *N* steps, the last return value will be set to 0 (since there is no next state when the game is over) as it was in the Monte Carlo case. However, if the episode hasn't finished by *N* steps, we'll use the last state value as our prediction for what the return would have been had we kept playing—that's where the bootstrapping happens. Without bootstrapping, the critic is just trying to predict the future returns from a state, and it gets the actual returns as training data. With bootstrapping, it is still trying to predict future returns, but it is doing so in part by using its own prediction about future returns (since the training data will include its own prediction).

```
def run episode(worker env, worker model, N steps=10):
  raw state = np.array(worker env.env.state)
  state = torch.from numpy(raw state).float()
   values, logprobs, rewards = [],[],[]
   done = False
  \dot{\eta}=0 G=torch.Tensor([0]) 
  while (j \lt N steps and done == False):
      j += 1 policy, value = worker_model(state)
       values.append(value)
       logits = policy.view(-1)
      action dist = torch.distributions.Categorical(logits=logits)
      action = action dist.sample()
       logprob_ = policy.view(-1)[action]
       logprobs.append(logprob_)
       state_, _, done, info = worker_env.step(action.detach().numpy())
      state = torch.from numpy(state).float()
       if done:
          reward = -10 worker_env.reset()
       else: 
          reward = 1.0G = value.detach() rewards.append(reward)
   return values, logprobs, rewards, G
Listing 5.9 N-step training with CartPole
                                                    The variable G refers to the 
                                                    return. We initialize to 0.
                                                    Plays game until N steps 
                                                     or when episode is over
                                      If episode is not done, 
                                      sets return to the last 
                                     state value
```

The only things we've changed are the conditions for the while loop (exit by *N* steps), and we've set the return to be the state value of the last step if the episode is not over, thereby enabling bootstrapping. This new run\_episode function explicitly returns G, the return, so to get this to work we need to make a couple minor updates to the update params function and the worker function.

 First, add the G parameter to the definition of the update\_params function, and change  $ret = G$ :

```
def update params(worker opt,values,logprobs,rewards,G,clc=0.1,qamma=0.95):
 rewards = torch.Tensor(rewards).flip(dims=(0,)).view(-1)
```

```
 logprobs = torch.stack(logprobs).flip(dims=(0,)).view(-1)
  values = torch.\,stack(vvalues).flip(dims=(0,)).\,view(-1) Returns = []
  ret = G……………………………………………………………………………………………………
```

The rest of the function is exactly the same and is omitted here.

 All we need to change in the worker function is to capture the newly returned G array and pass it to update\_params:

```
def worker(t, worker model, counter, params):
   worker_env = gym.make("CartPole-v1")
   worker_env.reset()
  worker opt = optim.Adam(lr=1e-4,params=worker model.parameters())
   worker_opt.zero_grad()
   for i in range(params['epochs']):
       worker_opt.zero_grad()
      values, logprobs, rewards, G = run episode(worker env,worker model)
       actor_loss,critic_loss,eplen = 
   update_params(worker_opt,values,logprobs,rewards, G)
       counter.value = counter.value + 1
```

You can run the training algorithm again as before, and everything should work the same except with better performance. You might be surprised at how much more efficient *N*-step learning is. Figure 5.15 shows the plot of episode length over the first 45 seconds of training for this model.

![](1__page_23_Figure_6.jpeg)

Figure 5.15 Performance plot for distributed advantage actor-critic with true *N*-step bootstrapping. Compared to our previous Monte Carlo algorithm, the performance is much smoother due to the more stable critic.

Notice in figure 5.15 that the *N*-step model starts getting better right away and reaches an episode length of 300 (after just 45 seconds), compared to only about 140 for the Monte Carlo version. Also notice that this plot is much smoother than the Monte Carlo one. Bootstrapping reduces the variance in the critic and allows it to learn much more rapidly than Monte Carlo.

As a concrete example, imagine the case where you get 3-step rewards of  $[1,1,-1]$ for episode 1 and then [1,1,1] for episode 2. The overall return for episode 1 is 0.01 (with  $\gamma = 0.99$ ) and 1.99 for episode 2; that's two orders of magnitude difference in return just based on the random outcome of the episode early in training. That's a lot of variance. Compare that to the same case except with (simulated) bootstrapping, so that the return for each of those episodes also includes the bootstrapped predicted return. With a bootstrapped return prediction of 1.0 for both (assuming the states are similar), the calculated returns are 0.99 and 2.97, which are much closer than without bootstrapping. You can reproduce this example with the following code.

## #Simulated rewards for 3 steps $r1 = [1, 1, -1]$ $r2 = [1, 1, 1]$ $R1, R2 = 0.0, 0.0$ #No bootstrapping for i in range(len(r1)-1, $0, -1$ ): $R1 = r1[i] + 0.99*R1$ for i in range(len(r2)-1, $0, -1$ ): $R2 = r2[i] + 0.99*R2$ print("No bootstrapping") print(R1,R2) #With bootstrapping $R1, R2 = 1.0, 1.0$ for i in range(len(r1)-1, $0, -1$ ): $R1 = r1[i] + 0.99*R1$ for i in range(len(r2)-1, $0, -1$ ): $R2 = r2[i] + 0.99*R2$ print("With bootstrapping") print(R1,R2) >>> No bootstrapping Listing 5.10 Returns with and without bootstrapping

0.010000000000000009 1.99 With bootstrapping 0.9901 2.9701

To recap, in the plain policy gradient method of the previous chapter, we only trained a policy function that would output a probability distribution over all the actions, such that the predicted best action would be assigned the highest probability. Unlike Qlearning where a target value is learned, the policy function is directly reinforced to increase or decrease the probability of the action taken depending on the reward. Often the same action may produce opposite results in terms of reward, causing high variance in the training.

 To mitigate this, we introduced a critic model (or in this chapter we used a single, two-headed model) that reduces the variance of the policy function updates by directly modeling the state value. This way, if the actor (policy) takes an action and gets an unusually big or small reward, the critic can moderate this big swing and prevent an unusually large (and possibly destructive) parameter update to the policy. This also leads to the notion of advantage, where instead of training the policy based on raw return (average accumulated rewards), we train based on how much better (or worse) the action was compared to what the critic predicted it would be. This is helpful, because if two actions both lead to the same positive reward, we will naively assume their equivalent actions, but if we compare to what we expected would happen, and one reward performed much better than anticipated, that action should be reinforced more.

 As with the rest of the deep learning methods, we generally must use batches of data in order to effectively train. Training with a single example a time introduces too much noise, and the training will likely never converge. To introduce batch training with Q-learning we used an experience replay buffer that could randomly select batches of previous experiences. We could have used experience replay with actorcritic, but it is more common to use distributed training with actor-critic (and, to be clear, Q-learning can also be distributed). Distributed training in actor-critic models is more common because we often want to use a recurrent neural network (RNN) layer as part of our reinforcement learning model in cases where keeping track of prior states is necessary or helpful in achieving the goal. But RNNs need a sequence of temporally related examples, and experience replay relies on a batch of independent experiences. We could store entire trajectories (sequences of experiences) in a replay buffer, but that just adds complexity. Instead, with distributed training and each process running online with its own environment, the models can easily incorporate RNNs.

 We didn't cover it here, but there's another way to train an online actor-critic algorithm besides distributed training: simply utilize multiple copies of your environment, and then batch together the states from each independent environment, feeding it into a single actor-critic model that will then produce independent predictions for each environment. This is a viable alternative to distributed training when the environments are not expensive to run. If your environment is a complicated, high-memory- and computer-intensive simulator, it's probably going to be very slow to run multiple copies of it in a single process, so in that case a distributed approach is better.

 We have now covered what we consider to be the most foundational parts of reinforcement learning today. You should now be comfortable with the basic mathematical framework of reinforcement learning as a Markov decision process (MDP), and you should be able to able to implement Q-learning, plain policy gradient, and actorcritic models. If you've followed along so far, you should have a good foundation for tackling many other reinforcement learning domains.

 In the rest of the book, we'll cover more advanced reinforcement learning methods with the aim of teaching you some of the most advanced RL algorithms of recent times in an intuitive way.

## *Summary*

- Q-learning learns to predict the discounted rewards given a state and action.
- Policy methods learn a probability distribution over actions given a state.
- Actor-critic models combine a Q-learner with a policy learner.
- Advantage actor-critic learns to compute advantages by comparing the expected value of an action to the reward that was actually observed, so if an action is expected to result in  $a -1$  reward but actually results in  $a +10$  reward, its advantage will be higher than an action that is expected to result in +9 and actually results in +10.
- Multiprocessing is running code on multiple different processors that can operate simultaneously and independently.
- Multithreading is like multitasking; it allows you to run multiple tasks faster by letting the operating system quickly switch between them. When one task is idle (perhaps waiting for a file to download), the operating system can continue working on another task.
- Distributed training works by simultaneously running multiple instances of the environment and a single shared instance of the DRL model; after each time step we compute losses for each individual model, collect the gradients for each copy of the model, and then sum or average them together to update the shared parameters. This lets us do mini-batch training without an experience replay buffer.
- **N**-Step learning is in between fully online learning, which trains 1 step at a time, and fully Monte Carlo learning, which only trains at the end of an episode. *N*-step learning thus has the advantages of both: the efficiency of 1-step learning and the accuracy of Monte Carlo.