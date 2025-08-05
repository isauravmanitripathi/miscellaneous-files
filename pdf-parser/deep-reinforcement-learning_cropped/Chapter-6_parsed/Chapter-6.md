*Alternative optimization methods: Evolutionary algorithms*

#### *This chapter covers*

- **Evolution algorithms for solving optimization** problems
- **Pros and cons of evolutionary approaches versus** previous algorithms
- Solving the CartPole game without backpropagation
- Why evolutionary strategies can scale better than other algorithms

Neural networks were loosely inspired by real biological brains, and convolutional neural networks were also inspired by the biological mechanism of vision. There is a long tradition of advances in technology and engineering being motivated by biological organisms. Nature, through the process of evolution by natural selection, has solved many problems elegantly and efficiently. Naturally, people wondered whether evolution itself could be borrowed and implemented on a computer to generate solutions to problems. As you will see, we can indeed harness evolution to solve problems, and it works surprisingly well and is relatively easy to implement.

 In natural evolution, biological traits change and new traits are generated simply by the fact that some traits confer a survival and reproduction advantage that

results in those organisms being able to seed more copies of their genes in the next generation. The survival advantage of a gene depends entirely on the environment, which is often unpredictable and dynamic. Our use cases for simulated evolution are much simpler, since we generally want to maximize or minimize a single number, such as the loss when training a neural network.

 In this chapter you will learn how to use simulated evolutionary algorithms to train neural networks for use in reinforcement learning without using backpropagation and gradient descent.

## *6.1 A different approach to reinforcement learning*

Why would we even think about abandoning backpropagation? Well, with both DQN and policy gradient approaches we created one agent whose policy depended on a neural network to approximate the Q function or policy function. As shown in figure 6.1, the agent interacts with the environment, collects experiences, and then uses backpropagation to improve the accuracy of its neural network and, hence, its policy. We needed to carefully tune several hyperparameters ranging from selecting the right optimizer function, mini-batch size, and learning rate so that the training would be stable and successful. Since the training of both DQN and policy gradient algorithms relies on stochastic gradient descent, which as the name suggests relies on noisy gradients, there is no guarantee that these models will successfully learn (i.e., converge on a good local or global optimum).

![](_page_1_Figure_5.jpeg)

Figure 6.1 For the past algorithms that we covered, our agent interacted with environment, collected experiences, and then learned from those experiences. We repeated the same process over and over for each epoch until the agent stopped learning.

Depending on the environment and the complexity of the network, creating an agent with the right hyperparameters may be incredibly difficult. Moreover, in order to use

gradient descent and backpropagation, we need a model that is differentiable. There are certainly interesting and useful models you could construct that might be impossible to train with gradient descent due to the lack of differentiability.

 Instead of creating one agent and improving it, we can instead learn from Charles Darwin and use evolution by (un)natural selection. We could spawn multiple different agents with different parameters (weights), observe which ones did the best, and "breed" the best agents such that the descendants could inherit their parents' desirable traits—just like in natural selection. We could emulate biological evolution using algorithms. We wouldn't need to struggle to tune hyperparameters and wait for multiple epochs to see if an agent is learning "correctly." We could just pick the agents that are already performing better (figure 6.2).

![](_page_2_Figure_3.jpeg)

Figure 6.2 Evolutionary algorithms are different from gradient descent-based optimization techniques. With evolutionary strategies, we generate agents and pass the most favorable weights down to the subsequent agents.

This class of algorithms does not require an individual agent to learn. It does not rely on gradient descent and is aptly called a *gradient-free algorithm*. But just because individual agents are not being nudged toward some objective directly does not mean that we are relying on pure chance. The renowned evolutionary biologist Richard Dawkins once said, "Natural selection is anything but random." Similarly, in our quest to build, or more accurately *discover*, the best agent, we will not be relying on pure chance. We will be selecting for the fittest amongst a population with a variance in traits.

# *6.2 Reinforcement learning with evolution strategies*

In this section we'll talk about how fitness plays into evolution strategies, and we'll briefly cover the task of selecting the fittest agents. Next, we'll work on how to recombine those agents into new agents and show what happens when we introduce mutations. This evolution is a multiple-generation process, so we'll discuss that and recap the full training loop.

### *6.2.1 Evolution in theory*

If you remember from your high school biology class, natural selection selects for the "most fit" individuals from each generation. In biology this represents the individuals that had the greatest reproductive success, and hence passed on their genetic information to subsequent generations. Birds with beak shapes more adept at procuring seeds from trees would have more food and thus be more likely to survive to pass that beak shape gene to their children and grandchildren. But remember, "most fit" is relative to an environment. A polar bear is well adapted to the polar ice caps but would be very unfit in the Amazonian rainforests. You can think of the environment as determining an objective or fitness function that assigns individuals a fitness score based on their performance within that environment; their performance is determined solely by their genetic information.

 In biology, each mutation very subtly changes the characteristics of the organism, such that it may be difficult to discern one generation from another. However, allowing these mutations and variations to accumulate over multiple generations allows for perceptible changes. In the evolution of birds' beaks, for example, a population of birds would initially have had roughly the same beak shape. But as time progressed, random mutations were introduced into the population. Most of these mutations probably did not impact the birds at all or even had a deleterious effect, but with a large enough population and enough generations, random mutations occurred that affected beak shapes favorably. Birds with better suited beaks would have an advantage getting food over the other birds, and therefore they'd have a higher likelihood of passing down their genes. Therefore, the next generation would have an increased frequency of the favorably shaped beak gene.

 In *evolutionary reinforcement learning*, we are selecting for traits that give our agents the highest reward in a given environment, and by *traits* we mean model parameters (e.g., the weights of a neural network) or entire model structures. An RL agent's fitness can be determined by the expected reward it would receive if it were to perform in the environment.

 Let's say agent A played the Atari game Breakout and was able to achieve an average score of 500 while agent B was only able to obtain 300 points. We would say that agent A is more fit than agent B and that we want our optimal agent to be more similar to agent A than B. Remember, the only reason why agent A would be more fit than agent B is because its model parameters were slightly more optimized to the environment.

 The objective in evolutionary reinforcement learning is exactly the same as in backpropagation and gradient descent-based training. The only difference is that we use this evolutionary process, which is often referred to as a *genetic algorithm*, to optimize the parameters of a model such as a neural network (figure 6.3).

 The process is quite simple, but let's run through the steps of a genetic algorithm in more detail. Let's say we have a neural network that we want to use as an agent to play Gridworld, and we want to train it using a genetic algorithm. Remember, *training* a neural network just means iteratively updating its parameters such that its performance improves. Also recall that given a fixed neural network architecture, the parameters completely determine its behavior, so to copy a neural network we just need to copy its parameters.

![](_page_4_Figure_1.jpeg)

Figure 6.3 In an evolutionary algorithm approach to reinforcement learning, agents compete in an environment, and the agents that are more fit (those that generate more rewards) are preferentially copied to produce offspring. After many iterations of this process, only the most fit agents are left.

Here's how we would train such a neural network using a genetic algorithm (graphically depicted in figure 6.4):

- <sup>1</sup> We generate an initial population of random parameter vectors. We refer to each parameter vector in the population as an *individual*. Let's say this initial population has 100 individuals.
- <sup>2</sup> We iterate through this population and assess the fitness of each individual by running the model in Gridworld with that parameter vector and recording the rewards. Each individual is assigned a fitness score based on the rewards it earns. Since the initial population is random, they will all likely perform very poorly, but there will be a few, just by chance, that will perform better than others.
- <sup>3</sup> We randomly sample a pair of individuals ("parents") from the population, weighted according to their relative fitness score (individuals with higher fitness have a higher probability of being selected) to create a "breeding population."

NOTE There are many different methods of selecting "parents" for the next generation. One way is to simply map a probability of selection onto each individual based on their relative fitness score, and then sample from this distribution. In this way, the most fit will be selected most often, but there will still be a small chance of poor performers being selected. This may help maintain population diversity. Another way is to simply rank all the individuals and take the top *N* individuals, and use those to mate to fill the next generation. Just about any method that preferentially selects the top performers to mate will work, but some are better than others. There's a tradeoff between selecting the best performers and reducing population diversity—this is very similar to the exploration versus exploitation tradeoff in reinforcement learning.

![](_page_5_Figure_1.jpeg)

Figure 6.4 A genetic algorithm optimization of neural networks for reinforcement learning. A population of initial neural networks (the RL agents) is tested in the environment, earning rewards. Each individual agent is labeled by how fit it is, which is based on the rewards earned. Individuals are selected for the next generation based on their fitness; more fit individuals are more likely to be included in the next generation. The selected individuals "mate" and are "mutated" to increase genetic diversity.

- <sup>4</sup> The individuals in the breeding population will then "mate" to produce "offspring" that will form a new, full population of 100 individuals. If the individuals are simply parameter vectors of real numbers, mating vector 1 with vector 2 involves taking a subset from vector 1 and combining it with a complementary subset of vector 2 to make a new offspring vector of the same dimensions. For example, suppose you have vector 1: [1 2 3] and vector 2: [4 5 6]. Vector 1 mates with vector 2 to produce [1 5 6] and [4 2 3]. We simply randomly pair up individuals from the breeding populations and recombine them to produce two new offspring until we fill up a new population. This creates new "genetic" diversity with the best performers.
- <sup>5</sup> We now have a new population with the top solutions from the last generation, along with new offspring solutions. At this point, we will iterate over our solutions and randomly mutate some of them to make sure we introduce new genetic diversity into every generation to prevent premature convergence on a local optimum. Mutation simply means adding a little random noise to the parameter vectors. If these were binary vectors, mutation would mean randomly flipping a few bits; otherwise we might add some Gaussian noise. The mutation rate needs to be fairly low, or we'll risk ruining the already present good solutions.

<sup>6</sup> We now have a new population of mutated offspring from the previous generation. We repeat this process with the new population for *N* number of generations or until we reach *convergence* (which is when the average population's fitness has stopped improving significantly).

### *6.2.2 Evolution in practice*

Before we dive into the reinforcement learning application, we'll run a super simple genetic algorithm on an example problem for illustrative purposes. We will create a population of random strings and try to evolve them toward a target string of our choosing, such as "Hello World!"

 Our initial population of random strings will look like "gMIgSkybXZyP" and "adlBOM XIrBH." We'll use a function that can tell us how similar these strings are to the target string to give us the fitness scores. We'll then sample pairs of parents from the population weighted by their relative fitness scores, such that individuals with higher fitness scores are more likely to be chosen to become parents. Next we'll mate these parents (also called *crossing* or *recombining*) to produce two offspring strings and add them to the next generation. We'll also mutate the offspring by randomly flipping a few characters in the string. We'll iterate this process and expect that the population will become enriched with strings very close to our target; probably at least one will hit our target exactly (at which point we'll stop the algorithm). This evolutionary process for strings is depicted in figure 6.5.

![](_page_6_Figure_5.jpeg)

Figure 6.5 A string diagram outlining the major steps in a genetic algorithm for evolving a set of random strings toward a target string. We start with a population of random strings, compare each to the target string, and assign a fitness score to each string based on how similar it is to the target string. We then select high-fitness parents to "mate" (or recombine) to produce children, and then we mutate the children to introduce new genetic variance. We repeat the process of selecting parents and producing children until the next generation is full (when it's the same size as the starting population). This is perhaps a silly example, but it's one of the simplest demonstrations of a genetic algorithm, and the concepts will directly transfer to our reinforcement learning tasks. Listings 6.1 through 6.4 show the code.

 In listing 6.1 we begin by setting up the functions that will instantiate an initial population of random strings and also define a function that can compute a similarity score between two strings, which we will ultimately use as our fitness function.

![](_page_7_Figure_3.jpeg)

The preceding code creates an initial population of individuals which are class objects composed of a string field and a fitness score field. Then it creates the random strings by sampling from a list of alphabetic characters. Once we have a population, we need to evaluate the fitness of each individual. For strings, we can compute a similarity metric using a built-in Python module called SequenceMatcher.

 In listing 6.2, we define two functions, recombine and mutate. As their names suggest, the former will take two strings and recombine them to create two new strings, and the latter will randomly flip characters in a string to mutate them.

```
def recombine(p1, p2):
     p1 = p1_.string
    p2 = p2.string
    child1 = []child2 = []cross pt = random.random(0, len(p1)) child1.extend(p1[0:cross_pt])
  Listing 6.2 Evolving strings: recombine and mutate
                                    Recombines two 
                                     parent strings into 
                                   two new offspring
```

```
 child1.extend(p2[cross_pt:])
     child2.extend(p2[0:cross_pt])
     child2.extend(p1[cross_pt:])
     c1 = Individual(''.join(child1))
     c2 = Individual(''.join(child2))
     return c1, c2
def mutate(x, mut rate=0.01):
    new x = [] for char in x.string:
        if random.random() < mut rate:
            new x .extend(random.choices(alphabet,k=1))
         else:
             new_x_.append(char)
    new x = Individual(''.join(new x)) return new_x
                                       Mutates a string by 
                                      randomly flipping 
                                      characters
```

The preceding recombination function takes two parent strings like "hello there" and "fog world" and randomly recombines them by generating a random integer up to the length of the strings and taking the first piece of parent 1 and the second piece of parent 2 to create an offspring, such as "fog there" and "hello world" if the split happened in the middle. If we have evolved a string that contains part of what we want, like "hello" and another string that contains another part of what we want like "world," then the recombination process might give us all of what we want.

 The mutation process takes a string like "hellb" and, with some small probability (the mutation rate), will replace a character in the string with a random one. For example, if the mutation rate was  $20\%$  (0.2), it is probable that at least one of the 5 characters in "hellb" will be mutated to a random character. Hopefully it will be mutated into "hello" if that is the target. The purpose of mutation is to introduce new information (variance) into the population. If all we did was recombine, it is likely that all the individuals in the population would become too similar too quickly, and we wouldn't find the solution we wanted, because information gets lost each generation if there is no mutation. Note that the mutation rate is critical. If it's too high, the fittest individuals will lose their fitness by mutation, and if it's too low, we won't have enough variance to find the optimal individual. Unfortunately, you have to find the right mutation rate empirically.

 In listing 6.3 we define a function that will loop through each individual in a population of strings, compute its fitness score, and associate it with that individual. We also define a function that will create the subsequent generation.

```
def evaluate population(pop, target):
    avg fit = 0 for i in range(len(pop)):
         fit = similar(pop[i].string, target)
         pop[i].fitness = fit
        avg fit += fitListing 6.3 Evolving strings: evaluate individuals and create new generation
                                                     Assigns a fitness score 
                                                     to each individual in 
                                                     the population
```
```
avg fit /= len(pop)
     return pop, avg_fit
def next generation(pop, size=100, length=26, mut rate=0.01):
    new pop = []while len(new pop) < size:
         parents = random.choices(pop,k=2, weights=[x.fitness for x in pop])
         offspring_ = recombine(parents[0],parents[1])
        child1 = mutate(offspring [0], mut rate=mut rate)
         child2 = mutate(offspring_[1], mut_rate=mut_rate)
         offspring = [child1, child2]
        new_pop.extend(offspring)
     return new_pop
                                                 Generates a new generation by
                                                   recombination and mutation
```

These are the last two functions we need to complete the evolutionary process. We have a function that evaluates each individual in the population and assigns a fitness score, which just indicates how similar the individual's string is to the target string. The fitness score will vary depending on what the objective is for a given problem. Lastly, we have a function that generates a new population by sampling the most fit individuals in the current population, recombining them to produce offspring, and mutating them.

 In listing 6.4 we put everything together and iterate the previous steps to some maximum number of generations. That is, we start with an initial population, go through the process of fitness-scoring individuals and creating a new offspring population, and then repeat this sequence a number of times. After a sufficient number of generations, we expect the final population to be enriched with strings very close to our target string.

![](0__page_9_Figure_4.jpeg)

If you run the algorithm, it should take a few minutes on a modern CPU. You can find the highest ranked individual in the population as follows:

```
>>> pop.sort(key=lambda x: x.fitness, reverse=True) #sort in place, highest 
    fitness first
>>> pop[0].string
"Hello World!"
```

It worked! You can also see the average fitness level of the population increasing each generation in figure 6.6. This is actually a more difficult problem to optimize using an evolutionary algorithm because the space of strings is not continuous; it is hard to take small, incremental steps in the right direction since the smallest step is flipping a character. Hence, if you try making a longer target string, it will take much more time and resources to evolve.

![](0__page_10_Figure_2.jpeg)

Figure 6.6 This is a plot of average population fitness over the generations. The average population fitness increases fairly monotonically and then plateaus, which looks promising. If the plot was very jagged, the mutation rate might be too high or the population size too low. If the plot converged too quickly, the mutation rate might be too low.

When we're optimizing real-valued parameters in a model, even a small increase in value might improve the fitness, and we can exploit that, which makes optimization faster. But although discrete-valued individuals are harder to optimize in an evolutionary algorithm, they are *impossible* to optimize using vanilla gradient descent and backpropagation, because they are not differentiable.

# *6.3 A genetic algorithm for CartPole*

Let's see how this evolution strategy works in a simple reinforcement learning example. We're going to use an evolutionary process to optimize an agent to play CartPole, the environment we introduced in chapter 4 where the agent is rewarded for keeping the pole upright (figure 6.7).

 We can represent an agent as a neural network that approximates the policy function—it accepts a state and outputs an action, or more typically a probability distribution over actions. The following listing shows an example of a three-layer network.

![](0__page_11_Figure_1.jpeg)

![](0__page_11_Figure_2.jpeg)

#### Listing 6.5 Defining an agent

![](0__page_11_Figure_4.jpeg)

The function in listing 6.5 defines a 3-layer neural network. The first two layers use rectified linear unit activation functions, and the last layer uses a log-softmax activation function so that we get log probabilities over actions as the final output. Notice that this function expects an input state, x, and unpacked\_params, which is a tuple of individual parameter matrices that are used in each layer.

 To make the recombination and mutation process easier, we will create a population of parameter vectors (1-tensors) that we must then "unpack" or decompose into individual parameter matrices for use in each layer of the neural network.

![](0__page_11_Figure_7.jpeg)

The preceding function takes a flat parameter vector as the params input and a specification of the layers that it contains as the layers input, which is a list of tuples; it unpacks the parameter vector into a set of individual layer matrices and bias vectors stored in a list. The default set for layers specifies a 3-layer neural network, which therefore consists of 3 weight matrices with dimensions  $25 \times 4$ ,  $10 \times 25$ , and  $2 \times 10$ , and 3 bias vectors of dimensions  $1 \times 25$ ,  $1 \times 10$ , and  $1 \times 2$  for a total of  $4 * 25 + 25 + 10$  $* 25 + 10 + 2 * 10 + 2 = 407$  parameters in the flattened parameter vector.

 The only reason we're adding this complexity of using flattened parameter vectors and unpacking them for use is that we want to be able to mutate over and recombine the entire set of parameters, which ends up being simpler overall and matches what we did with strings. An alternative approach would be to think of each layer's neural network as an individual chromosome (if you remember the biology)—only matched chromosomes will recombine. Using this approach, you would only recombine parameters from the same layer. This would prevent information from later layers corrupting the earlier layers. We encourage you to try to implement it using this "chromosomal" approach as a challenge once you're comfortable with the way we do it here. You'll need to iterate over each layer, recombine, and mutate them separately.

Next let's add a function to create a population of agents.

```
def spawn population(N=50, size=407):
              pop = [] for i in range(N):
               \Rightarrow vec = torch.randn(size) / 2.0
                   fit = 0p = \{ 'params': vec, 'fitness': fit \} pop.append(p)
               return pop
             Listing 6.7 Spawning a population
                                                                N is the number of individuals in 
                                                                the population; size is the length 
                                                                of the parameter vectors.
Creates a
randomly
initialized
parameter
   vector
                                                                       Creates a dictionary to store 
                                                                       the parameter vector and its 
                                                                      associated fitness score
```

Each agent will be a simple Python dictionary that stores the parameter vector for that agent and the fitness score for that agent.

 Next we implement the function that will recombine two parent agents to produce two new child agents.

![](0__page_12_Figure_7.jpeg)

```
c1 = \{ 'params':child1, 'fitness': 0.0 \}c2 = {^\text{'}params':child2, \text{ 'fitness': 0.0}} return c1, c2
                                                          Creates new child agents by 
                                                          packaging the new parameter 
                                                          vectors into dictionaries
```

This function takes two agents who serve as parents and produces two children or offspring. It does so by taking a random split or crossover point, and then taking the first piece of parent 1 and combining it with the second piece of parent 2, and likewise combines the second piece of parent 1 and the first piece of parent 2. This is exactly the same mechanism we used to recombine strings before.

 That was the first stage for populating the next generation; the second stage is to mutate the individuals with some fairly low probability. Mutation is the only source of new genetic information in each generation—recombination only shuffles around information that already exists.

![](0__page_13_Figure_4.jpeg)

We follow basically the same procedure as we did for strings; we randomly change a few elements of the parameter vector. The mutation rate parameter controls the number of elements that we change. We need to control the mutation rate carefully to balance the creation of new information that can be used to improve existing solutions and the destruction of old information.

 Next we need to assess the fitness of each agent by actually testing them on the environment (CartPole in our case).

```
import gym
            env = gym.make("CartPole-v0")
            def test_model(agent):
                  done = False
                 state = torch.from numpy(env.reset()).float()
                  score = 0
               while not done: 
                      params = unpack_params(agent['params'])
                      probs = model(state,params) 
                      action = torch.distributions.Categorical(probs=probs).sample() 
                     state, reward, done, info = env.setep(action.item())state = torch.from numpy(state ).float()
               Listing 6.10 Testing each agent in the environment
While game
 is not lost
                                                                       Gets the action probabilities 
                                                                       from the model using the 
                                                                       agent's parameter vector
                                                                           Probabilistically selects an
                                                                           action by sampling from a
                                                                             categorical distribution
```

```
 score += 1 
 return score
```

**Keeps track of the number of time steps the game is not lost as the score**

The test\_model function takes an *agent* (a dictionary of a parameter vector and its fitness value) and runs it in the CartPole environment until it loses the game and returns the number of time steps it lasted as its score. We want to breed agents that can last longer and longer in CartPole (therefore achieving a high score).

We need to do this for all the agents in the population.

![](0__page_14_Figure_5.jpeg)

The evaluate population function iterates through each agent in the population and runs test model on them to assess their fitness.

The final main function we need is the next generation function in listing 6.12. Unlike our string genetic algorithm from earlier, where we probabilistically selected parents based on their fitness score, here we employ a different selection mechanism. The *probabilistic selection mechanism* is similar to how we choose actions in a policy gradient method, and it works well there, but for choosing parents in a genetic algorithm, it often ends up leading to too rapid convergence. Genetic algorithms require more exploration than gradient-descent–based methods. In this case we'll use a selection mechanism called *tournament-style selection* (figure 6.8).

 In tournament-style selection we select a random subset from the whole population and then choose the top two individuals in this subset as the parents. This ensures we don't always select the same top two parents, but we do end up selecting the betterperforming agents more often.

 We can change the *tournament size* (the size of the random subset) to control the degree to which we favor choosing the best agents in the current generation, at the risk of losing genetic diversity. In the extreme case, we could set the tournament size to be equal to the size of the population, in which case we would only select the top two individuals in the population. At the other extreme, we could make the tournament size 2, so that we are randomly selecting parents.

 In this example we set the tournament size as a percentage of the size of the population. Empirically, tournament sizes of about 20% seem to work fairly well.

![](0__page_15_Figure_1.jpeg)

Figure 6.8 In tournament selection we evaluate the fitness of all the individuals in the population as usual, and then we choose a random subset of the full population (in this figure just 2 of 4), and then choose the top individuals (usually 2) in this subset, mate them to produce offspring and mutate them. We repeat this selection process until we fill up the next generation.

#### Listing 6.12 Creating the next generation

![](0__page_15_Figure_4.jpeg)

The next generation function creates a list of random indices to index the population list and create a subset for a tournament batch. We use the enumerate function to keep track of the index positions of each agent in the subset so we can refer back to them in the main population. Then we sort the batch of fitness scores in ascending

order and take the last two elements in the list as the top two individuals in that batch. We look up their indices and select the whole agent from the original population list.

 Putting it all together, we can train a population of agents to play CartPole in just a handful of generations. You should experiment with the hyperparameters of mutation rate, population size, and number of generations.

![](0__page_16_Figure_3.jpeg)

The first generation begins with a population of random parameter vectors, but by chance some of these will be better than the others, and we preferentially select these to mate and produce offspring for the next generation. To maintain genetic diversity, we allow each individual to be mutated slightly. This process repeats until we have individuals who are exceptionally good at playing CartPole. You can see in figure 6.9 that the score steadily increases each generation of evolution.

![](0__page_16_Figure_5.jpeg)

Figure 6.9 The average score of the population over generations in a genetic algorithm used to train agents to play CartPole.

# *6.4 Pros and cons of evolutionary algorithms*

The algorithm we implemented in this chapter is a bit different from the previous approaches we've used in this book. There are circumstances where an evolutionary approach works better, such as with problems that would benefit more from exploration; other circumstances make it impractical, such as problems where it is expensive to gather data. In this section we'll discuss the advantages and disadvantages of evolutionary algorithms and where you might benefit from using them over gradient descent.

### *6.4.1 Evolutionary algorithms explore more*

One advantage of gradient-free approaches is that they tend to explore more than their gradient-based counterparts. Both DQN and policy gradients followed a similar strategy: collect experiences and nudge the agent to take actions that led to greater rewards. As we discussed, this tends to cause agents to abandon exploring new states if they prefer an action already. We addressed this with DQN by incorporating an epsilon-greedy strategy, meaning there's a small chance the agent will take a random action even if it has a preferred action. With the stochastic policy gradient we relied on drawing a variety of actions from the action probability vector output by our model.

 The agents in the genetic algorithm, on the other hand, are not nudged in any direction. We produce a lot of agents in each generation, and with so much random variation between them, most of them will have different policies than each other. There still is an exploration versus exploitation problem in evolutionary strategies because too little mutation can lead to premature convergence where the whole population becomes filled with nearly identical individuals, but it's generally easier to ensure adequate exploration with genetic algorithms than with gradient descentbased ones.

## *6.4.2 Evolutionary algorithms are incredibly sample intensive*

As you could probably see from the code in this chapter, we needed to run each agent in a population of 500 through the environment to determine their fitness. That means we needed to perform 500 major computations before we could make an update to the population. Evolutionary algorithms tend to be more sample hungry than gradient-based methods, since we aren't strategically adjusting the weights of our agents; we are just creating lots of agents and hoping that the random mutations and recombinations we introduce are beneficial. We will say that evolutionary algorithms are less *data-efficient* than DQN or PG methods.

 Suppose we want to decrease the size of the population to make the algorithm run faster. If we decrease the population size, there are fewer agents to select from when we are picking the two parents. This will make it likely that less fit individuals will make it into the next generation. We rely on a large number of agents being produced in hopes of finding a combination that leads to better fitness. Additionally, as in biology,
mutations usually have a negative impact and lead to worse fitness. Having a larger population increases the probability that at least a few mutations will be beneficial.

 Being data-inefficient is a problem if collecting data is expensive, such as in robotics or with autonomous vehicles. Having a robot collect one episode of data usually takes a couple of minutes, and we know from our past algorithms that training a simple agent takes hundreds if not thousands of episodes. Imagine how many episodes an autonomous vehicle would need to sufficiently explore its state space (the world). In addition to taking considerably more time, training with physical agents is much more expensive, since you need to purchase the robot and account for any maintenance. It would be ideal if we could train such agents without having to give them physical bodies.

### *6.4.3 Simulators*

Simulators address the preceding concerns. Instead of using an expensive robot or building a car with the necessary sensors, we could instead use computer software to emulate the experiences the environment would provide. For example, when training agents to drive autonomous cars, instead of equipping cars with the necessary sensors and deploying the model on physical cars, we could just train the agents inside software environments, such as the driving game Grand Theft Auto. The agent would receive as input the images of its surroundings, and it would be trained to output driving actions that would get the vehicle to the programmed destination as safely as possible.

 Not only are simulators significantly cheaper to train agents with, but agents are able to train much more quickly since they can interact with the simulated environment much faster than in real life. If you need to watch and understand a two-hour movie, it will require two hours of your time. If you focus more intensely, you could probably increase the playback speed by two or three, dropping the amount of time needed to an hour or a bit less. A computer, on the other hand, could be finished before you've viewed the first act. For example, an 8 GPU computer (which could be rented from a cloud service) running ResNet-50, an established deep learning model for image classification, can process over 700 images per second. In a two-hour movie running at 24 frames per second (standard in Hollywood), there are 172,800 frames that need to be processed. This would require four minutes to finish. We could also effectively increase the playback speed for our deep learning model by dropping every few frames, which will drop our processing time to under two minutes. We could also throw more computers at the problem to increase processing power. For a more recent reinforcement learning example, the OpenAI Five bots were able to play 180 years of Dota 2 games each day. You get the picture—computers can process faster than we can, and that's why simulators are valuable.

# *6.5 Evolutionary algorithms as a scalable alternative*

If a simulator is available, the time and financial costs of collecting samples with evolutionary algorithms is less of an issue. In fact, producing a viable agent with evolutionary algorithms can sometimes be faster than gradient-based approaches because we

do not have to compute the gradients via backpropagation. Depending on the complexity of the network, this will cut down the computation time by roughly 2–3 times. But there is another advantage of evolutionary algorithms that can allow them to train faster than their gradient counterparts—evolutionary algorithms can scale incredibly well when parallelized. We will discuss this in some detail in this section.

# *6.5.1 Scaling evolutionary algorithms*

OpenAI released a paper called "Evolutionary Strategies as a Scalable Alternative to Reinforcement Learning" by Tim Salimans et al. (2017), in which they described training agents incredibly quickly and efficiently by adding more machines. On a single machine with 18 CPU cores, they were able to make a 3D humanoid learn to walk in 11 hours. But with 80 machines (1,440 CPU cores) they were able to produce an agent in under 10 minutes.

 You may be thinking that's obvious—they just threw more machines and money at the problem. But this is actually trickier than it sounds, and other gradient-based approaches struggle to scale to that many machines.

 Let's first look at how their algorithm differs from what we did earlier. *Evolutionary algorithm* is an umbrella term for a wide variety of algorithms that take inspiration from biological evolution and rely on iteratively selecting slightly better solutions from a large population to optimize a solution. The approach we implemented to play Cart-Pole is more specifically called a *genetic algorithm*, because it more closely resembles the way biological genes get "updated" from generation to generation through recombination and mutation.

 There's another class of evolutionary algorithms confusingly termed *evolutionary strategies* (ES), which employ a less biologically accurate form of evolution, as illustrated in figure 6.10.

![](1__page_19_Figure_7.jpeg)

Figure 6.10 In an evolutionary strategy we create a population of individuals by repeatedly adding a small amount of random noise to a parent individual to generate multiple variants of the parent. We then assign fitness scores to each variant by testing them in the environment, and then we get a new parent by taking a weighted sum of all the variants.

If we're training a neural network with an ES algorithm, we start with a single parameter vector  $\theta$ <sub>b</sub>, sample a bunch of noise vectors of equal size (usually from a Gaussian distribution), such as  $e_i \sim N(\mu, \sigma)$ , where *N* is a Gaussian distribution with mean vector  $\mu$  and standard deviation  $\sigma$ . We then create a population of parameter vectors that are mutated versions of  $\theta_t$  by taking  $\theta'_i = \theta + e_i$ . We test each of these mutated parameter vectors in the environment and assign them fitness scores based on their performance in the environment. Lastly, we get an updated parameter vector by taking a weighted sum of each of the mutated vectors, where the weights are proportional to their fitness scores (figure 6.11).

![](1__page_20_Figure_2.jpeg)

![](1__page_20_Figure_3.jpeg)

This evolutionary strategy algorithm is significantly simpler than the genetic algorithm we implemented earlier since there is no mating step. We only perform mutation, and the recombination step does not involve swapping pieces from different parents but is just a simple weighted summation which is very easy to implement and computationally fast. As we'll see, this approach is also easier to parallelize.

## *6.5.2 Parallel vs. serial processing*

When we used a genetic algorithm to train agents to play CartPole, we had to sequentially iterate over each agent and let each agent play CartPole until it lost, in order to determine the fittest agent in each generation before we started the next run. If the agent takes 30 seconds to run through the environment, and we are determining the fitness for 10 agents, this will take 5 minutes. This is known as running a program *serially* (figure 6.12).

 Determining each agent's fitness will generally be the longest-running task in an evolutionary algorithm, but each agent can evaluate its own fitness independent of each other. But there's no reason we need to wait for agent 1 to finish playing in the environment before we start evaluating agent 2. We could instead run each agent in the generation on multiple computers at the same time. Each of the 10 agents would go on 10 machines, and we can determine their fitness simultaneously. This means that completing one generation will take ~30 seconds on 10 machines as opposed to 5 minutes on one machine, a 10x speedup. This is known as running the process in *parallel* (figure 6.13).

![](1__page_21_Figure_1.jpeg)

Figure 6.12 Determining the fitness of an agent is often the slowest step in a training loop and requires that we run the agent through the environment (possibly many times). If we are doing this on a single computer, we will be doing this in serial—we have to wait for one to finish running through the environment before we can start determining the fitness of the second agent. The time it takes to run this algorithm is a function of the number of agents *and* the time it takes to run through the environment for a single agent.

![](1__page_21_Figure_3.jpeg)

Figure 6.13 If we have multiple machines at our disposal, we can determine the fitness of each agent on its own machine in parallel with each other. We do not have to wait for one agent to finish running through the environment before starting the next one. This will provide a huge speed up if we are training agents with a long episode length. You can see now that this algorithm is only a function of the time it takes to assess the fitness of a single agent, and not the number of agents we are assessing.

### *6.5.3 Scaling efficiency*

Now we can throw more machines and money at the problem, and we won't have to wait nearly as long. In the previous hypothetical example where we added 10 machines and got a 10x speedup—a scaling efficient of 1.0. *Scaling efficiency* is a term used to describe how a particular approach improves as more resources are thrown at it and can be calculated as follows:

Scaling Efficiency = Multiple of Performance Speed up after adding resources<br>Multiple of Resources Added

In the real world, processes never have a scaling efficiency of 1. There is always some additional cost to adding more machines that decreases efficiency. More realistically, adding 10 more machines will only give us a 9x speedup. Using the previous scaling efficiency equation we can calculate the scaling efficiency as 0.9 (which is pretty good in the real world).

 Ultimately we need to combine the results from assessing the fitness of each agent in parallel so that we can recombine and mutate them. Thus, we need to use true parallel processing followed by a period of sequential processing. This is more generally referred to as *distributed computing* (figure 6.14), since we start with a single processor (often called the *master node*) and distribute tasks to multiple processors to run in parallel, and then collect the results back onto the master node.

![](1__page_22_Figure_3.jpeg)

Figure 6.14 A general schematic for how distributed computing works. A master node assigns tasks to worker nodes; the worker nodes perform those tasks and then send their results back to the master node (not shown).

Every step takes a little bit of network time to communicate between machines, which is something we would not encounter if we were running everything on a single machine. Additionally, if just one machine is slower than the others, the other workers will need to wait. To get the maximal scaling efficiency, we want to reduce the amount of communication between nodes as much as possible, both in terms of the number of times nodes need to send data as well as the amount of data that they send.

### *6.5.4 Communicating between nodes*

The researchers at OpenAI developed a neat strategy for distributed computing where each node sends only one number (not a whole vector) to each other node, eliminating the need for a separate master node. The idea is that each worker is first initialized with the same parent parameter vector. Then each worker adds a noise vector to its parent to create a slightly different child vector (figure 6.15). Each worker then runs the child vector through the environment to get its fitness score. The fitness score from each worker is sent to all other workers, which just involves sending a single number. Since each worker has the same set of random seeds, each worker can recreate the noise vectors used by all the other workers. Lastly, each worker creates the same new parent vector and the process repeats.

 Setting the random seed allows us to consistently generate the same random numbers every time, even on different machines. If you run the code in listing 6.14, you will get the output shown, even though these numbers should be generated "randomly."

![](1__page_23_Figure_1.jpeg)

Figure 6.15 The architecture derived from OpenAI's distributed ES paper. Each worker creates a child parameter vector from a parent by adding noise to the parent. Then it evaluates the child's fitness and sends the fitness score to all other agents. Using shared random seeds, each agent can reconstruct the noise vectors used to create the other vectors from the other workers without each having to send an entire vector. Lastly, new parent vectors are created by performing a weighted sum of the child vectors, weighted according to their fitness scores.

#### Listing 6.14 Setting the random seed

```
import numpy as np
np.random.seed(10)
np.random.rand(4)
>>> array([0.77132064, 0.02075195, 0.63364823, 0.74880388])
np.random.seed(10)
np.random.rand(4)
>> array([0.77132064, 0.02075195, 0.63364823, 0.74880388])
```

Seeding is important; it allows experiments involving random numbers to be reproduced by other researchers. If you do not supply an explicit seed, the system time or some other sort of variable number is used. If we came up with a novel RL algorithm, we would want others to be able to verify our work on their own machines. We would want the agent that another lab generated to be identical, to eliminate any source of error (and therefore doubt). That's why it's important we provide as much detail about our algorithm as possible—the architecture, the hyperparameters used, and sometimes the random seed we used. However, we hope we've developed an algorithm that is robust and that the particular set of random numbers generated doesn't matter to the performance of the algorithm.

# *6.5.5 Scaling linearly*

Because the OpenAI researchers reduced the volume of data sent between the nodes, adding nodes did not affect the network significantly. They were able to scale to over a thousand workers linearly.

*Scaling linearly* means that for every machine added, we receive roughly the same performance boost as we did by adding the previous machine. This is denoted by a straight line on a graph of performance over resources, as seen in figure 6.16.

![](1__page_24_Figure_4.jpeg)

Figure 6.16 Figure recreated from the OpenAI "Evolutionary Strategies as a Scalable Alternative to Reinforcement Learning" paper. The figure demonstrates that as more computing resources were added, the time improvement remained constant.

### *6.5.6 Scaling gradient-based approaches*

Gradient-based approaches can be trained on multiple machines as well. However, they do not scale nearly as well as ES. Currently, most distributed training of gradientbased approaches involves training the agent on each worker and then passing the gradients back to a central machine to be aggregated. All the gradients must be passed for each epoch or update cycle, which requires a lot of network bandwidth and strain on the central machine. Eventually the network gets saturated, and adding more workers does not improve training speed as well (figure 6.17).

 Evolutionary approaches, on the other hand, do not require backpropagation, so they do not need to send gradient updates to a central server. And with smart techniques like the ones that OpenAI developed, they may only need to send a single number.

![](1__page_25_Figure_1.jpeg)

![](1__page_25_Figure_2.jpeg)

Number of CPU cores

Figure 6.17 The performance of current gradient-based approaches looks like this. In the beginning, there is a seemingly linear trend because the network has not been saturated. But eventually, as more resources are added, we get less and less of a performance boost.

# *Summary*

- Evolutionary algorithms provide us with more powerful tools for our toolkit. Based on biological evolution, we
  - Produce individuals
  - Select the best from the current generation
  - Shuffle the genes around
  - Mutate them to introduce some variation
  - Mate them to create new generations for the next population
- Evolutionary algorithms tend to be more data hungry and less data-efficient than gradient-based approaches; in some circumstances this may be fine, notably if you have a simulator.
- Evolutionary algorithms can optimize over nondifferentiable or even discrete functions, which gradient-based methods cannot do.
- Evolutionary strategies (ES) are a subclass of evolutionary algorithms that do not involve biological-like mating and recombination, but instead use copying with noise and weighted sums to create new individuals from a population.