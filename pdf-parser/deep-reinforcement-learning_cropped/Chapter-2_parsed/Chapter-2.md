# *Modeling reinforcement learning problems: Markov decision processes*

#### *This chapter covers*

- **String diagrams and our teaching methods**
- The PyTorch deep learning framework
- Solving *n*-armed bandit problems
- **Balancing exploration versus exploitation**
- **Modeling a problem as a Markov decision** process (MDP)
- **Implementing a neural network to solve an** advertisement selection problem

This chapter covers some of the most fundamental concepts in all of reinforcement learning, and it will be the basis for the rest of the book. But before we get into that, we want to first go over some of the recurring teaching methods we'll employ in this book—most notably, the string diagrams we mentioned last chapter.

## *2.1 String diagrams and our teaching methods*

In our experience, when most people try to teach something complicated, they tend to teach it in the reverse order in which the topic itself was developed. They'll give you a bunch of definitions, terms, descriptions, and perhaps theorems, and

then they'll say, "great, now that we've covered all the theory, let's go over some practice problems." In our opinion, that's exactly the opposite order in which things should be presented. Most good ideas arise as solutions to real-world problems, or at least imagined problems. The problem-solver stumbles across a potential solution, tests it, improves it, and then eventually formalizes and possibly mathematizes it. The terms and definitions come *after* the solution to the problem was developed.

 We think learning is most motivating and effective when you take the place of that original idea-maker, who was thinking of how to solve a particular problem. Only once the solution crystalizes does it warrant formalization, which is indeed necessary to establish its correctness and to faithfully communicate it to others in the field.

 There is a powerful urge to engage in this reverse chronological mode of teaching, but we will do our best to resist it and develop the topic as we go. In that spirit, we will introduce new terms, definitions, and mathematical notations as we need them. For example, we will use "callouts" like this:

DEFINITION A *neural network* is a kind of machine learning model composed of multiple "layers" that perform a matrix-vector multiplication followed by the application of a nonlinear "activation" function. The matrices of the neural network are the model's learnable parameters and are often called the "weights" of the neural network.

You will only see these callouts once per term, but we will often repeat the definition in different ways in the text to make sure you really understand and remember it. This is a course on reinforcement learning, not a textbook or reference, so we won't shy away from repeating ourselves when we think something is important to remember.

 Whenever we need to introduce some math, we will typically use a box showing the math and a pseudo-Python version of the same underlying concept. Sometimes it's easier to think in terms of code or of math, and we think it's good to get familiar with both. As a super simple example, if we were introducing the equation of a line, we would do it like this:

| <b>Math</b>  | <b>Pseudocode</b>                            |
|--------------|----------------------------------------------|
| $y = mx + b$ | $def$ line $(x, m, b)$ :<br>return $m*x + b$ |

Table 2.1 Example of the side-by-side mathematics and pseudocode we use in this book

We will also include plenty of inline code (short snippets) and code listings (longer code examples) as well as the code for complete projects. All of the code in the book is provided in Jupyter Notebooks categorized by chapter on the book's GitHub repository (<http://mng.bz/JzKp>). If you're actively following the text and building the projects in this book, we strongly recommend following the code in this associated GitHub repository rather than copying the code in the text—we will keep the GitHub code updated and bug-free, whereas the code in the book may get a bit out of date as the Python libraries we use are updated. The GitHub code is also more complete (e.g., showing you how to generate the visualizations that we include), whereas the code in the text has been kept as minimal as possible to focus on the underlying concepts.

 Since reinforcement learning involves a lot of interconnecting concepts that can become confusing when just using words, we will include a lot of diagrams and figures of varying sorts. The most important kind of figure we'll use is the *string diagram*. It's perhaps an odd name, but it's a really simple idea and is adapted from category theory, a branch of math we mentioned in the first chapter where they tend to use a lot of diagrams to supplement or replace traditional symbolic notation.

 You already saw the string diagram in figure 2.1 when we introduced the general framework for reinforcement learning in chapter 1. The idea is that the boxes contain nouns or noun phrases, whereas the arrows are labeled with verbs or verb phrases. It's slightly different from typical flow diagrams, but this makes it easy to translate the string diagram into English prose and vice versa. It's also very clear what the arrows are *doing* functionally. This particular kind of string diagram is also called an *ontological log*, or *olog* ("oh-log"). You can look them up if you're curious about learning more.

![](_page_2_Figure_4.jpeg)

Figure 2.1 The standard reinforcement learning model in which an agent takes actions in an evolving environment that produces rewards to reinforce the actions of the agent.

More generally, string diagrams (sometimes referred to as *wiring diagrams* in other sources) are flow-like diagrams that represent the flow of typed data along strings (i.e., directed or undirected arrows) into processes (computations, functions, transformations, processes, etc.), which are represented as boxes. The important difference between string diagrams and other similar-looking flow diagrams you may have seen is

that all the data on the strings is explicitly typed (e.g., a numpy array with shape  $[10,$ 10], or maybe a floating-point number), and the diagrams are fully compositional. By compositional, we mean that we can zoom in or out on the diagram to see the bigger more abstract picture or to drill down to the computational details.

 If we're showing a higher-level depiction, the process boxes may just be labeled with a word or short phrase indicating the kind of process that happens, but we could also show a zoomed-in view of that process box that reveals all its internal details, composed of its own set of substrings and subprocesses. The compositional nature of these diagrams also means that we can plug parts of one diagram into another diagram, forming more complex diagrams, as long as all the strings' types are compatible. For example, here's a single layer of a neural network as a string diagram:

![](_page_3_Figure_3.jpeg)

Reading from left to right, we see that some data of type n flows into a process box called Neural Network Layer and produces output of type m. Since neural networks typically take vectors as inputs and produce vectors as outputs, these types refer to the dimensions of the input and output vectors respectively. That is, this neural network layer accepts a vector of length or dimension *n* and produces a vector of dimension *m*. It's possible that *n* = *m* for some neural network layers.

 This manner of *typing* the strings is simplified, and we do it only when it's clear what the types mean from the context. In other cases, we may employ mathematical notation such as  $\mathbb R$  for the set of all real numbers, which in programming languages basically translates to floating-point numbers. So for a vector of floating-point numbers with dimension *n*, we could type the strings like this:

![](_page_3_Figure_6.jpeg)

Now that the typing is richer, we not only know the dimensions of the input and output vectors, we know that they're real/floating-point numbers. While this is almost always the case, sometimes we may be dealing with integers or binary numbers. In any case, our Neural Network Layer process box is left as a black box; we don't know exactly what's going on in there other than the fact that it transforms a vector into another vector of possibly different dimensions. We can decide to zoom in on this process to see what specifically is happening:

![](_page_3_Figure_8.jpeg)

Now we can see the inside the original process box, and it is composed of its own set of subprocesses. We can see that our *n*-dimensional vector gets multiplied by a matrix of dimensions  $n \times m$ , which produces an *m*-dimensional vector product. This vector then passes through some process called "ReLU," which you may recognize as a standard neural network activation function, the rectified linear unit. We could continue to zoom in on the ReLU sub-subprocess if we wanted. Anything that deserves the name *string diagram* must be able to be scrutinized at any level of abstraction and remain *well typed* at any level (meaning the types of the data entering and exiting the processes must be compatible and make sense—a process that is supposed to produce sorted lists should not be hooked up to another process that expects integers).

 As long as the strings are well typed, we can string together a bunch of processes into a complex system. This allows us to build components once and re-use them wherever they're type-matched. At a somewhat high level, we might depict a simple two-layer recurrent neural network (RNN) like this:

![](_page_4_Figure_3.jpeg)

This RNN takes in a *q* vector and produces an *s* vector. However, we can see the inside processes. There are two layers, and each one looks identical in its function. They each take in a vector and produce a vector, except that the output vector is copied and fed back into the layer process as part of the input, hence the recurrence.

 String diagrams are a very general type of diagram; in addition to diagramming neural networks, we could use them to diagram how to bake a cake. A *computational graph* is a special kind of string diagram where all the processes represent concrete computations that a computer can perform, or that can be described in some programming language like Python. If you've ever visualized a computational graph in TensorFlow's TensorBoard, you'll know what we mean. The goal of a good string diagram is that we can view an algorithm or machine learning model at a high level to get the big picture, and then gradually zoom in until our string diagram is detailed enough for us to actually implement the algorithm based almost solely on our knowledge of the diagram.

 Between the mathematics, simple Python code, and string diagrams that we'll present in this book, you should have no problem understanding how to implement some pretty advanced machine learning models.

## *2.2 Solving the multi-arm bandit*

We're now ready to get started with a real reinforcement learning problem and look at the relevant concepts and skills needed to solve this problem as we go. But before we get too fancy, building something like AlphaGo, let's first consider a simple problem. Let's say you're at a casino, and in front of you are 10 slot machines with a flashy sign that says "Play for free! Max payout is \$10!" Wow, not bad! Intrigued, you ask one of the employees what's going on, because it seems too good to be true, and she says, "It's really true, play as much as you want, it's free. Each slot machine is guaranteed to give you a reward between \$0 and \$10. Oh, by the way, keep this to yourself, but those 10 slot machines each have a different average payout, so try to figure out which one gives the most rewards on average, and you'll be making tons of cash!"

 What kind of casino is this? Who cares, let's just figure out how to make the most money! Oh by the way, here's a joke: What's another name for a slot machine? A onearmed bandit! Get it? It has one arm (a lever) and it generally steals your money. We could call our situation a 10-armed bandit problem, or an *n*-armed bandit problem more generally, where *n* is the number of slot machines. While this problem sounds pretty fanciful so far, you'll see later that these *n*-armed bandit (or multi-armed bandit) problems do have some very practical applications.

 Let's restate our problem more formally. We have *n* possible actions (here *n* = 10) where an action means pulling the arm, or lever, of a particular slot machine, and at each play (*k*) of this game we can choose a single lever to pull. After taking an action (*a*) we will receive a reward,  $R_k$  (reward at play *k*). Each lever has a unique probability distribution of payouts (rewards). For example, if we have 10 slot machines and play many games, slot machine #3 may give out an average reward of \$9 whereas slot machine #1 only gives out an average reward of \$4. Of course, since the reward at each play is probabilistic, it is possible that lever #1 will by chance give us a reward of \$9 on a single play. But if we play many games, we expect on average that slot machine #1 will be associated with a lower reward than #3.

 Our strategy should be to play a few times, choosing different levers and observing our rewards for each action. Then we want to only choose the lever with the largest observed average reward. Thus, we need a concept of expected reward for taking an action (*a*) based on our previous plays. We'll call this expected reward  $Q_k(a)$  mathematically: you give the function an action (given we're at play *k*), and it returns the expected reward for taking that action. This is shown formally here:

| <b>Math</b>                        | <b>Pseudocode</b>                                                                                                                        |  |  |  |  |
|------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|--|--|--|--|
| $R_1 + R_2 +  + R_k$<br>$Q_k(a)$ = | def exp reward(action, history):<br>rewards for action = history[action]<br>return sum (rewards for action) /<br>len(rewards for action) |  |  |  |  |

That is, the expected reward at play *k* for action *a* is the arithmetic mean of all the previous rewards we've received for taking action *a*. Thus, our previous actions and observations influence our future actions. We might even say some of our previous actions *reinforce* our current and future actions, but we'll come back to this later. The function  $Q_k(a)$  is called a *value function* because it tells us the value of something. In particular, it is an *action*-*value function* because it tells us the value of taking a particular action. Since we typically denote this function with the symbol *Q*, it's also often called a *Q function*. We'll come back to value functions later and give a more sophisticated definition, but this will suffice for now.

#### *2.2.1 Exploration and exploitation*

When we first start playing, we need to play the game and observe the rewards we get for the various machines. We can call this strategy *exploration*, since we're essentially randomly exploring the results of our actions. This is in contrast to a different strategy we could employ called *exploitation*, which means that we use our current knowledge about which machine seems to produce the most rewards, and keep playing that machine. Our overall strategy needs to include some amount of exploitation (choosing the best lever based on what we know so far) and some amount of exploration (choosing random levers so we can learn more). The proper balance of exploitation and exploration will be important to maximizing our rewards.

 How can we come up with an algorithm to figure out which slot machine has the largest average payout? Well, the simplest algorithm would be to just select the action associated with the highest Q value:

| <b>Math</b>                            | <b>Pseudocode</b>                                                                                                |  |  |  |  |  |  |  |
|----------------------------------------|------------------------------------------------------------------------------------------------------------------|--|--|--|--|--|--|--|
| $\forall a_i \in A_k$                  | def get best action (actions, history) :<br>exp rewards = [exp reward(action, history) for action in<br>actionsl |  |  |  |  |  |  |  |
| $a^*$ = argmax <sub>a</sub> $Q_k(a_i)$ | return argmax (exp rewards)                                                                                      |  |  |  |  |  |  |  |

|  | Table 2.3 | Computing the best action, given the expected rewards |  |  |  |  |  |  |  |
|--|-----------|-------------------------------------------------------|--|--|--|--|--|--|--|
|--|-----------|-------------------------------------------------------|--|--|--|--|--|--|--|

The following listing shows it as legitimate Python 3 code.

![](_page_6_Figure_8.jpeg)

We use our above function  $Q_k(a)$  on all the possible actions, and select the action that returns the maximum average reward. Since  $Q_k(a)$  depends on a record of our previous actions and their associated rewards, this method will not evaluate actions that we haven't already explored. Thus, we might have previously tried levers #1 and #3 and noticed that lever #3 gives us a higher reward, but with this method we'll never think to try another lever, say #6, which, unbeknownst to us, actually gives out the highest average reward. This method of simply choosing the best lever that we know of so far is called a *greedy* (or exploitation) method.

### *2.2.2 Epsilon-greedy strategy*

We need some exploration of other levers (other slot machines) to discover the true best action. One simple modification to our previous algorithm is to change it to an  $\varepsilon$ (epsilon)-greedy algorithm, such that with a probability,  $\varepsilon$ , we will choose an action,  $a$ , at random, and the rest of the time (probability  $1 - \varepsilon$ ) we will choose the best lever based on what we currently know from past plays. Most of the time we will play greedy, but sometimes we will take a risk and choose a random lever to see what happens. The result will, of course, influence our future greedy actions. Let's see if we can solve this in code with Python.

![](_page_7_Figure_4.jpeg)

In this casino example, we will be solving a 10-armed bandit problem, so  $n = 10$ . We've also defined a numpy array of length *n* filled with random floats that can be understood as probabilities. Each position in the probs array corresponds to an arm, which is a possible action. For example, the first element has index position 0, so action 0 is arm 0. Each arm has an associated probability that weights how much reward it pays out.

 The way we've chosen to implement our reward probability distributions for each arm is this: Each arm will have a probability, e.g., 0.7, and the maximum reward is \$10. We will set up a for loop going to 10, and at each step it will add 1 to the reward if a random float is less than the arm's probability. Thus, on the first loop it makes up a random float (e.g., 0.4). 0.4 is less than 0.7, so reward  $+= 1$ . On the next iteration, it makes up another random float (e.g., 0.6) which is also less than 0.7, so reward  $+= 1$ . This continues until we complete 10 iterations, and then we return the final total reward, which could be anything between 0 and 10. With an arm probability of 0.7,
the *average* reward of doing this to infinity would be 7, but on any single play it could be more or less.

```
def get_reward(prob, n=10):
     reward = 0
     for i in range(n):
         if random.random() < prob:
              reward += 1
     return reward
  Listing 2.3 Defining the reward function
```

You can check this by running it:

```
>>> np.mean([get reward(0.7) for _ in range(2000)])
7.001
```

This output shows that running this code 2,000 times with a probability of 0.7 indeed gives us a mean reward of close to 7 (see the histogram in figure 2.2).

![](0__page_8_Figure_6.jpeg)

Figure 2.2 The distribution of rewards for a simulated *n*-armed bandit with a 0.7 probability of payout.

The next function we'll define is our greedy strategy of choosing the best arm so far. We need a way to keep track of which arms were pulled and what the resulting reward was. Naively, we could just have a list and append observations such as (arm, reward), e.g., (2, 9), indicating we chose arm 2 and received reward 9. This list would grow longer as we played the game.

 There's a much simpler approach, however, since we really only need to keep track of the average reward for each arm—we don't need to store each observation. Recall

that to calculate the mean of a list of numbers,  $x_i$  (indexed by  $i$ ), we simply need sum up all the  $x_i$  values and then divide by the number of  $x_i$ , which we will denote  $k$ . The mean is often denoted with the Greek letter  $\mu$  (mu).

$$
\mu = \frac{1}{k} \sum_{i} x_i
$$

The Greek uppercase symbol  $\Sigma$  (sigma) is used to denote a summation operation. The *i* notation underneath means we sum each element,  $x_i$ . It's basically the math equivalent of a for loop like:

```
sum = 0x = [4, 5, 6, 7]for j in range(len(x)):
    sum = sum + x[j]
```

If we already have an average reward  $\mu$  for a particular arm, we can update this average when we get a new reward by recomputing the average. We basically need to undo the average and then recompute it. To undo it, we multiply  $\mu$  by the total number of values, *k*. Of course, this just gives us the sum, not the original set of values—you can't undo a sum. But the total number is what we need to recompute the average with a new value. We just add this sum to the new value and divide by *k* + 1, the new total number of values.

$$
\mu_{new} = \frac{k \cdot \mu_{old} + x}{k + 1}
$$

We can use this equation to continually update the average reward observed for each arm as we collect new data, and this way we only need to keep track of two numbers for each arm:  $k$ , the number of values observed, and  $\mu$ , the current running average. We can easily store this in a  $10 \times 2$  numpy array (assuming we have 10 arms). We'll call this array the record.

```
>>> record = np.zeros((n,2))
array([[0., 0.],
      [0., 0.][0., 0.] [0., 0.],
      [0., 0.][0., 0.][0., 0.],
      [0., 0.][0., 0.][0., 0.]]
```

The first column of this array will store the number of times each arm has been pulled, and the second column will store the running average reward. Let's write a function for updating the record, given a new action and reward.

```
def update record(record, action, r):
   new r = (record[action,0] * record[action,1] + r) / (record[action,0] +
     1)
    record[action,0] += 1
   record[action, 1] = new r return record
  Listing 2.4 Updating the reward record
```

This function takes the record array, an action (which is the index value of the arm), and a new reward observation. To update the average reward, it simply implements the mathematical function we described previously, and then increments the counter recording how many times that arm has been pulled.

 Next we need a function that will select which arm to pull. We want it to choose the arm associated with the highest average reward, so all we need to do is find the row in the record array with biggest value in column 1. We can easily do this using numpy's built-in argmax function, which takes in an array, finds the largest value in the array, and returns its index position.

```
Listing 2.5 Computing the best action
```

```
def get best arm(record):
    arm index = np.argmax(record[:,1],axis=0)
     return arm_index
                                                       Uses numpy argmax 
                                                       on column 1 of the 
                                                        record array
```

Now we can get into the main loop for playing the *n*-armed bandit game. If a random number is greater than the epsilon parameter, we just calculate the best action using the get best arm function and take that action. Otherwise we take a random action to ensure some amount of exploration. After choosing the arm, we use the get\_reward function and observe the reward value. We then update the record array with this new observation. We repeat this process a bunch of times, and it will continually update the *record* array. The arm with the highest reward probability should eventually get chosen most often, since it will give out the highest average reward.

We've set it to play 500 times in the following listing, and to display a matplotlib scatter plot of the mean reward against plays. Hopefully we'll see that the mean reward increases as we play more times.

![](0__page_10_Figure_8.jpeg)

![](0__page_11_Figure_1.jpeg)

As you can see in figure 2.3, the average reward does indeed improve after many plays. Our algorithm is *learning*; it is getting reinforced by previous good plays! And yet it is such a simple algorithm.

![](0__page_11_Figure_3.jpeg)

Figure 2.3 This plot shows that the average reward for each slot machine play increases over time, indicating we are successfully learning how to solve the *n*-armed bandit problem.

The problem we've considered here is a *stationary* problem because the underlying reward probability distributions for the arms does not change over time. We certainly could consider a variant of this problem where this is not true—a nonstationary problem. In this case, a simple modification would be to allow new reward observations to update the average reward value stored in the record in a skewed way, so that it would be a weighted average, weighted toward the newest observation. This way, if things change over time, we would be able to track them to some degree. We won't implement this slightly more complex variant here, but we will encounter nonstationary problems later in the book.

## *2.2.3 Softmax selection policy*

Imagine another type of bandit problem: A newly minted doctor specializes in treating patients with heart attacks. She has 10 treatment options, of which she can choose only 1 to treat each patient she sees. For some reason, all she knows is that these 10 treatments have different efficacies and risk profiles for treating heart attacks—she doesn't know which one is the best yet. We could use the *n*-armed bandit algorithm from the previous solution, but we might want to reconsider our  $\varepsilon$ -greedy policy of randomly choosing a treatment once in a while. In this new problem, randomly choosing a treatment could result in patient death, not just losing some money. We really want to make sure we don't choose the worst treatment, but we still want some ability to explore our options to find the best one.

 This is where a *softmax* selection might be most appropriate. Instead of just choosing an action at random during exploration, softmax gives us a probability distribution across our options. The option with the largest probability would be equivalent to the best arm action in the previous solution, but it will also give us some idea about which are the second and third best actions, for example. This way we can randomly choose to explore other options while avoiding the very worst options, since they will be assigned tiny probabilities or even 0. Here's the softmax equation:

| Table 2.4 | The softmax equation |  |
|-----------|----------------------|--|
|-----------|----------------------|--|

| <b>Math</b>                                                                             | <b>Pseudocode</b>                                                                                      |
|-----------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| $Q_k(A)/\tau$<br>Pr(A)<br>$\sum_{n} \frac{Q_k(i)}{e}$<br>$\overline{\phantom{a}}$ i = 1 | def softmax(vals, tau):<br>$softmax$ = $pow(e, vals / tau) / sum( pow(e, vals / tau))$<br>return softm |

 $Pr(A)$  is a function that accepts an action-value vector (array) and returns a probability distribution over the actions, such that higher value actions have higher probabilities. For example, if your action-value array has four possible actions and they all currently have the same value, say  $A = \begin{bmatrix} 10 \\ 10 \\ 10 \\ 10 \end{bmatrix}$ , then Pr(A) =  $\begin{bmatrix} 0.25 \\ 0.25 \\ 0.10 \end{bmatrix}$ 0.25, 0.25, 0.25]. In other words, all the probabilities are the same and must sum to 1.

 The numerator of the fraction exponentiates the action-value array divided by a parameter,  $\tau$ , yielding a vector of the same size (i.e., length) as the input. The denominator sums over the exponentiation of each individual action value divided by  $\tau$ , yielding a single number.

<sup>τ</sup> is a parameter called *temperature* that scales the probability distribution of actions. A high temperature will cause the probabilities to be very similar, whereas a low temperature will exaggerate differences in probabilities between actions. Selecting a value for this parameter requires an educated guess and some trial and error. The mathematical exponential  $e^x$  is a function call to np. exp(...) in numpy. It will apply

the function element-wise across the input vector. Here's how we actually write the softmax function in Python.

```
def softmax(av, tau=1.12):
    softmax = np.exp(av / tau) / np.sum( np.exp(av / tau)) return softm
  Listing 2.7 The softmax function
```

When we implement the previous 10-armed bandit problem using softmax, we don't need the get best arm function anymore. Since softmax produces a weighted probability distribution across our possible actions, we can randomly select actions according to their relative probabilities. That is, our best action will get chosen more often because it will have the highest softmax probability, but other actions will be chosen at lower frequencies.

 To implement this, all we need to do is apply the softmax function over the second column (column index 1) of the record array, since that's the column that stores the current mean reward (the action values) for each action. It will transform these action values into probabilities. Then we use the np.random.choice function, which accepts an arbitrary input array,  $x$ , and a parameter,  $p$ , that is an array of probabilities that correspond to each element in *x*. Since our record is initialized to all zeros, softmax at first will return a uniform distribution over all the arms, but this distribution will quickly skew toward whatever action is associated with the highest reward. Here's an example of using softmax and the random choice function:

```
\Rightarrow \times = np.arange(10)
>>> x
array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
\Rightarrow \geq \frac{10}{5}>>> p = softmax(av)
>> p
array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
>>> np.random.choice(x,p=p)
3
```

We used the numpy arange function to create an array from 0 to 9, corresponding to the indices of each arm, so the random choice function will return an arm index according to the supplied probability vector. We can use the same training loop as we did previously; we just need to change the arm selection part so it uses softmax instead of get best arm, and we need to get rid of the random action selection that's part of the epsilon-greedy strategy.

```
Listing 2.8 Softmax action-selection for the n-armed bandit
```

```
n = 10probs = np.random.randn(n)record = np{\cdot}zeros((n,2))
```

![](0__page_14_Figure_1.jpeg)

Softmax action selection seems to do better than the epsilon-greedy method for this problem as you can tell from figure 2.4; it looks like it converges on an optimal policy faster. The downside to softmax is having to manually select the  $\tau$  parameter. Softmax here was pretty sensitive to  $\tau$ , and it takes some time playing with it to find a good value. Obviously with epsilon-greedy we had to set the epsilon parameter, but choosing that parameter was much more intuitive.

![](0__page_14_Figure_3.jpeg)

Figure 2.4 With the softmax policy, the *n-*armed bandit algorithm tends to converge faster on the maximal mean reward.

## *2.3 Applying bandits to optimize ad placements*

The slot machine example may not seem to be a particularly real-world problem, but if we add one element, it does become a practical business problem, with one big example being advertisement placement. Whenever you visit a website with ads, the company placing the ads wants to maximize the probability that you will click them.

 Let's say we manage 10 e-commerce websites, each focusing on selling a different broad category of retail items such as computers, shoes, jewelry, etc. We want to increase sales by referring customers who shop on one of our sites to another site that they might be interested in. When a customer checks out on a particular site in our network, we will display an advertisement to one of our other sites in hopes they'll go there and buy something else. Alternatively, we could place an ad for another product on the same site. Our problem is that we don't know which sites we should refer users to. We could try placing random ads, but we suspect a more targeted approach is possible.

## *2.3.1 Contextual bandits*

Perhaps you can see how this just adds a new layer of complexity to the *n*-armed bandit problem we considered at the beginning of the chapter. At each play of the game (each time a customer checks out on a particular website) we have  $n = 10$  possible actions we can take, corresponding to the 10 different types of advertisements we could place. The twist is that the best ad to place may depend on which site in the network the current customer is on. For example, a customer checking out on our jewelry site may be more in the mood to buy a new pair of shoes to go with their new diamond necklace than they would be to buy a new laptop. Thus our problem is to figure out how a particular site relates to a particular advertisement.

 This leads us to *state spaces*. The *n*-armed bandit problem we started with had an *n*element *action space* (the space or set of all possible actions), but there was no concept of state. That is, there was no information in the environment that would help us choose a good arm. The only way we could figure out which arms were good is by trial and error. In the ad problem, we know the user is buying something on a particular site, which may give us some information about that user's preferences and could help guide our decision about which ad to place. We call this contextual information a *state* and this new class of problems *contextual* bandits (see figure 2.5).

![](0__page_15_Figure_5.jpeg)

Figure 2.5 Overview of a contextual bandit for advertisement placement. The agent (which is a neural network algorithm) receives state information (in this case, the current website the user is on), which it uses to choose which of several advertisements it should place at the checkout step. Users will click on the advertisement or not, resulting in reward signals that get relayed back to the agent for learning.
DEFINITION A *state* in a game (or in a reinforcement learning problem more generally) is the set of information available in the environment that can be used to make decisions.

### *2.3.2 States, actions, rewards*

Before we move on, let's consolidate some of the terms and concepts we've introduced so far. Reinforcement learning algorithms attempt to model the world in a way that computers can understand and calculate. In particular, RL algorithms model the world as if it merely involved a set of *states, S* (state space), which are a set of features about the environment, a set of *actions, A* (action space), that can be taken in a given state, and *rewards, r*, that are given for taking an action in a specific state. When we speak of taking a particular action in a particular state, we often call it a *state-action pair* (*s*, *a*).

NOTE The objective of any RL algorithm is to maximize the rewards over the course of an entire episode.

Since our original *n*-armed bandit problem did not have a state space, only an action space, we just needed to learn the relationship between actions and rewards. We learned the relationship by using a lookup table to store our experience of receiving rewards for particular actions. We stored action-reward pairs (*ak*, *rk*) where the reward at play *k* was an average over all past plays associated with taking action *ak*.

 In our *n*-armed bandit problem, we only had 10 actions, so a lookup table of 10 rows was very reasonable. But when we introduce a state space with contextual bandits, we start to get a combinatorial explosion of possible state-action-reward tuples. For example, if we have a state space of 100 states, and each state is associated with 10 actions, we have 1,000 different pieces of data we need to store and recompute. In most of the problems we'll consider in this book, the state space is intractably large, so a simple lookup table is not feasible.

 That's where deep learning comes in. When they're properly trained, neural networks are great at learning abstractions that get rid of the details of little value. They can learn composable patterns and regularities in data such that they can effectively compress a large amount of data while retaining the important information. Hence, neural networks can be used to learn complex relationships between state-action pairs and rewards without us having to store all such experiences as raw memories. We often call the part of an RL algorithm that makes the decisions based on some information the *agent*. In order to solve the contextual bandit we've been discussing, we'll employ a neural network as our agent.

 First, though, we will take a moment to introduce PyTorch, the deep learning framework we will be using throughout this book to build neural networks.

# *2.4 Building networks with PyTorch*

There are many deep learning frameworks available today, with TensorFlow, MXNet, and PyTorch probably being the most popular. We chose to use PyTorch for this book because of its simplicity. It allows you to write native-looking Python code and still get all the goodies of a good framework like automatic differentiation and builtin optimization. We'll give you a quick introduction to PyTorch here, but we'll explain more as we go along. If you need to brush up on basic deep learning, see the appendix where we have a fairly detailed review of deep learning and more thorough coverage of PyTorch.

 If you're comfortable with the numpy multidimensional array, you can replace almost everything you do with numpy with PyTorch. For example, here we instantiate a  $2 \times 3$  matrix in numpy:

```
>>> import numpy
>>> numpy.array([[1, 2, 3], [4, 5, 6]])
array([[1, 2, 3],
      [4, 5, 6]
```

And here is how you instantiate the same matrix with PyTorch:

```
>>> import torch
>>> torch.Tensor([[1, 2, 3], [4, 5, 6]])
1 2 3
4 5 6
[torch.FloatTensor of size 2x3]
```

The PyTorch code is basically the same as the numpy version, except in PyTorch we call multidimensional arrays *tensors*. Unsurprisingly, this is also the term used in TensorFlow and other frameworks, so get used to seeing multidimensional arrays referred to as tensors. We can and do refer to the *tensor order*, which is basically how many indexed dimensions the tensor has. This gets a little confusing because sometimes we speak of the dimension of a vector, in which case we're referring to the length of the vector. But when we speak of the order of a tensor, we mean how many indices it has. A vector has one index, meaning every element can be "addressed" by a single index value, so it's an order 1 tensor or 1-tensor for short. A matrix has two indices, one for each dimension, so it's a 2-tensor. Higher order tensors can be referred to as a *k-*tensor, where *k* is the order, a non-negative integer. On the other end, a single number is a 0-tensor, also called a *scalar*, since it has no indices.

## *2.4.1 Automatic differentiation*

The most important features of PyTorch that we need and that numpy doesn't offer are automatic differentiation and optimization. Let's say we want to set up a simple linear model to predict some data of interest. We can easily define the model using ordinary numpy-like syntax:

```
>>> x = torch.Tensor([2,4]) #input data
>>> m = torch.randn(2, requires_grad=True) #parameter 1
>>> b = torch.randn(1, requires grad=True) #parameter 2
>>> y = m*x+b #linear model
>>> loss = (torch.sum(y_known - y))**2 #loss function
>>> loss.backward() #calculate gradients
>>> m.grad
tensor([ 0.7734, -90.4993])
```

You simply supply the requires grad=True argument to PyTorch tensors that you want to compute gradients for, and then call the backward() method on the last node in your computational graph, which will backpropagate gradients through all the nodes with requires grad=True. You can then do gradient descent with the automatically computed gradients.

### *2.4.2 Building Models*

For most of this book, we won't bother dealing directly with automatically computed gradients. Instead we'll use PyTorch's nn module to easily set up a feedforward neural network model and then use the built-in optimization algorithms to automatically train the neural network without having to manually specify the mechanics of backpropagation and gradient descent. Here's a simple two-layer neural network with an optimizer set up:

```
model = torch.nn.Sequential(
    torch.nn.Linear(10, 150),
    torch.nn.ReLU(),
    torch.nn.Linear(150, 4),
    torch.nn.ReLU(),
)
loss fn = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
```

We've set up a two-layer model with ReLU (rectified linear units) activation functions, defined a mean-squared error loss function, and set up an optimizer. All we have to do to train this model, given that we have some labeled training data, is start a training loop:

```
for step in range(100):
   y pred = model(x)loss = loss fin(y pred, y correct) optimizer.zero_grad()
       loss.backward()
        optimizer.step()
```

The x variable is the input data to the model. The y\_correct variable is a tensor representing the labeled, correct output. We make the prediction using the model, calculate the loss, and then compute the gradients using the backward() method on the last node in the computational graph (which is almost always the loss function).

Then we just run the step() method on the optimizer, and it will run a single step of gradient descent. If we need to build more complex neural network architectures than the sequential model, we can write our own Python class, inhereit from PyTorch's module class, and use that instead:

```
from torch.nn import Module, Linear
class MyNet(Module):
   def __init__(self):
       super(MyNet, self). init ()
       self.fc1 = Linear(784, 50)self.fc2 = Linear(50, 10) def forward(self, x):
       x = F.relu(self.fc1(x))
       x = F.relu(self.fc2(x))
        return x
model = MyNet()
```

That's all you need to know about PyTorch for now to be productive with it. We will discuss a few other bells and whistles as we progress through the book.

# *2.5 Solving contextual bandits*

We've built a simulated environment for a contextual bandit. The simulator includes the state (a number from 0 to 9 representing 1 of the 10 websites in the network), reward generation (ad clicks), and a method that chooses an action (which of 10 ads to serve). The following listing shows the code for the contextual bandit environment, but don't spend much time thinking about it as we want to demonstrate how to use it, not how to code it.

```
class ContextBandit:
    def __init (self, arms=10):
         self.arms = arms
        self.init distribution(arms)
         self.update_state()
    def init distribution(self, arms):
        self.handit matrix = np.random.randn(arms, arms) def reward(self, prob):
         reward = 0
         for i in range(self.arms):
              if random.random() < prob:
                 reward += 1
         return reward
     def get_state(self):
         return self.state
  Listing 2.9 Contextual bandit environment
                                                    Number of states = number of 
                                                    arms, to keep things simple. 
                                                    Each row represents a state 
                                                    and each column an arm.
```

```
def update state(self):
    self.state = np.random.randint(0,self.arms)
def qet reward(self,arm):
    return self.reward(self.bandit matrix[self.get state()][arm])
 def choose_arm(self, arm): 
    reward = self.get_reward(arm)
    self.update state()
    return reward
                                      Choosing an arm 
                                      returns a reward and 
                                     updates the state.
```

The following code snippet demonstrates how to use the environment. The only part we need to build is the agent, which is generally the crux of any RL problem, since building an environment usually just involves setting up input/output with some data source or plugging into an existing API.

```
env = ContextBandit(arms=10)
state = env.get_state()
reward = env.choose_arm(1)
print(state)
>>> 2
print(reward)
>>> 8
```

The simulator consists of a simple Python class called ContextBandit that can be initialized to a specific number of arms. For simplicity, the number of states equals the number of arms, but in general the state space is often much larger than the action space. The class has two methods: One is get\_state(), which is called with no arguments and will return a state sampled randomly from a uniform distribution. In most problems your state will come from a much more complex distribution. Calling the other method, choose  $arm(...)$ , will simulate placing an advertisement, and it returns a reward (e.g., proportional to the number of ad clicks). We need to always call get\_state and then choose\_arm, in that order, to continually get new data to learn from.

 The ContextBandit module also includes a few helper functions, such as the softmax function and a *one-hot encoder*. A one-hot encoded vector is a vector where all but 1 element is set to 0. The only nonzero element is set to 1 and indicates a particular state in the state space.

 Rather than using a single static reward probability distribution over *n* actions, like our original bandit problem, the contextual bandit simulator sets up a different reward distribution over the actions for each state. That is, we will have *n* different softmax reward distributions over actions for each of *n* states. Hence, we need to learn the relationship between the states and their respective reward distributions, and then learn which action has the highest probability for a given state.

 As with all of our projects in this book, we'll be using PyTorch to build the neural network. In this case, we're going to build a two-layer feedforward neural network that uses rectified linear units (ReLU) as the activation function. The first layer accepts a

10-element one-hot (also known as 1-of-K, where all elements but one are 0) encoded vector of the state, and the final layer returns a 10-element vector representing the predicted reward for each action given the state.

 Figure 2.6 shows the forward pass of the algorithm we've described. Unlike the lookup table approach, our neural network agent will learn to predict the rewards that each action will result in for a given state. Then we use the softmax function to give us a probability distribution over the actions and sample from this distribution to choose an arm (advertisement). Choosing an arm will give us a reward, which we will use to train our neural network.

![](1__page_21_Figure_3.jpeg)

Figure 2.6 A computational graph for a simple 10-armed contextual bandit. The **get\_state()** function returns a state value, which is transformed into a one-hot vector that becomes the input data for a two-layer neural network. The output of the neural network is the predicted reward for each possible action, which is a dense vector that is run through a softmax to sample an action from the resulting probability distribution over the actions. The chosen action will return a reward and updates the state of the environment.  $\theta_1$  and  $\theta_2$  represent the weight parameters for each layer. The N, R, and P symbols denote the natural numbers (0, 1, 2, 3, …), the real numbers (a floating-point number, for our purposes), and a probability, respectively. The superscript indicates the length of the vector, so  $\mathbb{P}^{10}$  represents a 10-element vector where each element is a probability (such that all the elements sum to 1).

Initially our neural network will produce a random vector such as [1.4, 50, 4.3, 0.31, 0.43, 11, 121, 90, 8.9, 1.1] when in state 0. We will run softmax over this vector and sample an action, most likely action 6 (from actions 0 through 9), since that is the biggest number in the example vector. Choosing action 6 will generate a reward of say 8. Then we train our neural network to produce the vector [1.4, 50, 4.3, 0.31, 0.43, 11, 8, 90, 8.9, 1.1], since that is the true reward we received for action 6, leaving the rest of the values unchanged. The next time when the neural network sees state 0, it will produce a reward prediction for action 6 closer to 8. As we continually do this over many states and actions, the neural network will eventually learn to predict accurate rewards for each action given a state. Thus, our algorithm will be able to choose the best action each time, maximizing our rewards.

 The following code imports the necessary libraries and sets up some *hyperparameters* (parameters to specify model structure):

```
import numpy as np
import torch
arms = 10N, D_in, H, D_out = 1, arms, 100, arms
```

In the preceding code,  $N$  is the batch size,  $D$  in is the input dimension, H is the hidden dimension, and  $D$  out is the output dimension.

 Now we need to set up our neural network model. It is a simple sequential (feedforward) neural network with two layers as we described earlier.

```
model = torch.nn.Sequential(
    torch.nn.Linear(D_in, H),
     torch.nn.ReLU(),
     torch.nn.Linear(H, D_out),
    torch.nn.ReLU(),
)
```

We'll use the mean squared error loss function here, but others could work too.

```
loss_fn = torch.nn.MSELoss()
```

Now we set up a new environment by instantiating the ContextBandit class, supplying the number of arms to its constructor. Remember, we've set up the environment such that the number of arms will be equal to the number of states.

```
env = ContextBandit(arms)
```

The main for loop of the algorithm will be very similar to our original *n*-armed bandit algorithm, but we have added the step of running a neural network and using the output to select an action. We'll define a function called train (shown in listing 2.10) that accepts the environment instance we created previously, the number of epochs we want to train for, and the learning rate.

 In the function, we'll set a PyTorch variable for the current state, which we'll need to one-hot encode using the one\_hot(…) encoding function:

```
def one_hot(N, pos, val=1):
    one hot vec = np{\text{.zeros}}(N)one hot vec[pos] = val
     return one_hot_vec
```

Once we enter the main training for loop, we'll run our neural network model with the randomly initialized current state vector. It will return a vector that represents its guess for the values of each of the possible actions. At first, the model will output a bunch of random values since it is not trained.

 We'll run the softmax function over the model's output to generate a probability distribution over the actions. We'll then select an action using the environment's choose  $arm(...)$  function, which will return the reward generated for taking that action; it will also update the environment's current state. We'll turn the reward (which is a non-negative integer) into a one-hot vector that we can use as our training data. We'll then run one step of backpropagation with this reward vector, given the state we gave the model. Since we're using a neural network model as our action-value function, we no longer have any sort of action-value array storing "memories;" everything is being encoded in the neural network's weight parameters. The whole train function is shown in the following listing.

![](1__page_23_Figure_2.jpeg)

Go ahead and run this function. When we train this network for 5,000 epochs, we can plot the moving average of rewards earned over the training time (see figure 2.7; we omitted the code to produce such a graph). Our neural network indeed learns a fairly good understanding of the relationship between states, actions and rewards for this contextual bandit. The maximum reward payout for any play is 10, and our average is topping off around 8.5, which is close to the mathematical optimum for this particular bandit. Our first deep reinforcement learning algorithm works! Okay, it's not a very deep network, but still!
![](2__page_24_Figure_1.jpeg)

Figure 2.7 A training graph showing the average rewards for playing the contextual bandit simulator using a two-layer neural network as the action-value function. We can see the average reward rapidly increases during training time, demonstrating our neural network is successfully learning.

# *2.6 The Markov property*

In our contextual bandit problem, our neural network led us to choose the best action given a state without reference to any other prior states. We just gave it the current state, and it produced the expected rewards for each possible action. This is an important property in reinforcement learning called the *Markov property*. A game (or any other control task) that exhibits the Markov property is said to be a *Markov decision process* (MDP). With an MDP, the current state alone contains enough information to choose optimal actions to maximize future rewards. Modeling a control task as an MDP is a key concept in reinforcement learning.

 The MDP model simplifies an RL problem dramatically, as we do not need to take into account all previous states or actions—we don't need to have memory, we just need to analyze the present situation. Hence, we always attempt to model a problem as (at least approximately) a Markov decision processes. The card game Blackjack (also known as 21) is an MDP because we can play the game successfully just by knowing our current state (what cards we have, and the dealer's one face-up card).

 To test your understanding of the Markov property, consider each control problem or decision task in the following list and see if it has the Markov property or not:

- Driving a car
- Deciding whether to invest in a stock or not
- Choosing a medical treatment for a patient
- **Diagnosing a patient's illness**

- **Predicting which team will win in a football game**
- Choosing the shortest route (by distance) to some destination
- Aiming a gun to shoot a distant target

Okay, let's see how you did. Here are our answers and brief explanations:

- Driving a car can generally be considered to have the Markov property because you don't need to know what happened 10 minutes ago to be able to optimally drive your car. You just need to know where everything is right now and where you want to go.
- Deciding whether to invest in a stock or not does not meet the criteria of the Markov property since you would want to know the past performance of the stock in order to make a decision.
- Choosing a medical treatment seems to have the Markov property because you don't need to know the biography of a person to choose a good treatment for what ails them right now.
- In contrast, *diagnosing* (rather than treating) would definitely require knowledge of past states. It is often very important to know the historical course of a patient's symptoms in order to make a diagnosis.
- Predicting which football team will win does not have the Markov property, since, like the stock example, you need to know the past performance of the football teams to make a good prediction.
- Choosing the shortest route to a destination has the Markov property because you just need to know the distance to the destination for various routes, which doesn't depend on what happened yesterday.
- Aiming a gun to shoot a distant target also has the Markov property since all you need to know is where the target is, and perhaps current conditions like wind velocity and the particulars of your gun. You don't need to know the wind velocity of yesterday.

We hope you can appreciate that for some of those examples you could make arguments for or against it having the Markov property. For example, in diagnosing a patient, you may need to know the recent history of their symptoms, but if that is documented in their medical record and we consider the full medical record as our current state, then we've effectively induced the Markov property. This is an important thing to keep in mind: many problems may not *naturally* have the Markov property, but often we can induce it by jamming more information into the state.

 DeepMind's deep Q-learning (or deep Q-network) algorithm learned to play Atari games from just raw pixel data and the current score. Do Atari games have the Markov property? Not exactly. In the game Pacman, if our state is the raw pixel data from our current frame, we have no idea if the enemy a few tiles away is approaching us or moving away from us, and that would strongly influence our choice of actions to take. This is why DeepMind's implementation actually feeds in the last four frames of gameplay,

effectively changing a non-MDP into an MDP. With the last four frames, the agent has access to the direction and speed of all players.

 Figure 2.8 gives a lighthearted example of a Markov decision process using all the concepts we've discussed so far. You can see there is a three-element state space S = {crying baby, sleeping baby, smiling baby}, and a two-element action space  $A =$ {feed, don't feed}. In addition, we have transition probabilities noted, which are maps from an action to the probability of an outcome state (we'll go over this again in the next section). Of course, in real life, you as the *agent* have no idea what the transition probabilities are. If you did, you would have a *model* of the environment. As you'll learn later, sometimes an agent does have access to a model of the environment, and sometimes not. In the cases where the agent does not have access to the model, we may want our agent to learn a model of the environment (which may just approximate the true, underlying model).

![](2__page_26_Figure_3.jpeg)

Figure 2.8 A simplified MDP diagram with three states and two actions. Here we model the parenting decision process for taking care of an infant. If the baby is crying, we can either administer food or not, and with some probability the baby will transition into a new state, and we'll receive a reward of  $-1$ ,  $+1$ , or  $+2$ (based on the baby's satisfaction).

## *2.7 Predicting future rewards: Value and policy functions*

Believe it or not, we actually smuggled a lot of knowledge into the previous sections. The way we set up our solutions to the *n*-armed bandit and contextual bandit are standard reinforcement learning methods, and as such, there is a whole bunch of established terminology and mathematics behind what we did. We introduced a few terms already, such as state and action spaces, but we mostly just described things in natural language. In order for you to understand the latest RL research papers and for us to make future chapters less verbose, it's important to become acquainted with the jargon and the mathematics.

 Let's review and formalize what you've learned so far (summarized in figure 2.9). A reinforcement learning algorithm essentially constructs an *agent,* which acts in some *environment*. The environment is often a game, but is more generally whatever process produces states, actions, and rewards. The agent has access to the current state of the environment, which is all the data about the environment at a particular time point,  $s_t \in S$ . Using this state information, the agent takes an action,  $a_t \in A$ , which may deterministically or probabilistically change the environment to be in a new state,  $s_{t+1}$ .

 The probability associated with mapping a state to a new state by taking an action is called the *transition probability*. The agent receives a reward, *rt*, for having taken action  $a_t$  in state  $s_t$  leading to a new state,  $s_{t+1}$ . And we know that the ultimate goal of the agent (our reinforcement learning algorithm) is to maximize its rewards. It's really the state transition,  $s_t \rightarrow s_{t+1}$ , that produces the reward, not the action per se, since the action may probabilistically lead to a bad state. If you're in an action movie (no pun intended) and you jump off a roof onto another roof, you may land gracefully on the other roof or miss it completely and fall—your peril is what's important (the two possible resulting states), not the fact that you jumped (the action).

![](2__page_27_Figure_3.jpeg)

Figure 2.9 The general process of a reinforcement learning algorithm. The environment produces states and rewards. The agent takes an action,  $a_t$ , given a state, *st*, at time *t* and receives a reward, *rt*. The agent's goal is to maximize rewards by learning to take the best actions in a given state.

#### *2.7.1 Policy functions*

How exactly do we use our current state information to decide what action to take? This is where the key concepts of *value functions* and *policy functions* come into play, which we already have a bit of experience with. Let's first tackle policies.

In words, a policy,  $\pi$ , is the strategy of an agent in some environment. For example, the strategy of the dealer in Blackjack is to always hit until they reach a card value of 17 or greater. It's a simple fixed strategy. In our *n*-armed bandit problem, our policy was an epsilon-greedy strategy. In general, a policy is a function that maps a state to a probability distribution over the set of possible actions in that state.

Table 2.5 The policy function

| <b>Math</b>                                        | <b>English</b>                                                                                          |
|----------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| $\pi$ , s $\rightarrow$ Pr(A   s), where s $\in$ S | A policy, $\pi$ , is a mapping from states to the (probabilistically) best<br>actions for those states. |

In the mathematical notation, *s* is a state and  $Pr(A \mid s)$  is a probability distribution over the set of actions *A*, given state *s*. The probability of each action in the distribution is the probability that the action will produce the greatest reward.

### *2.7.2 Optimal policy*

The policy is the part of our reinforcement learning algorithm that chooses actions given its current state. We can then formulate the *optimal policy*—it's the strategy that maximizes rewards.

Table 2.6 The optimal policy

| <b>Math</b>                   | <b>English</b>                                                                                                                                                                                        |
|-------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| $\pi^*$ = argmax $E(R \pi)$ , | If we know the expected rewards for following any possible policy, $\pi$ , the opti-<br>mal policy, $\pi$ <sup>*</sup> , is a policy that, when followed, produces the maximum possi-<br>ble rewards. |

Remember, a particular policy is a map or function, so we have some sort of set of possible policies; the optimal policy is just an argmax (which selects the maximum) over this set of possible policies as a function of their expected rewards.

 Again, the whole goal of a reinforcement learning algorithm (our agent) is to choose the actions that lead to the maximal expected rewards. But there are two ways we can train our agent to do this:

- *Directly***—We can teach the agent to learn what actions are best, given what state** it is in.
- *Indirectly*—We can teach the agent to learn which states are most valuable, and then to take actions that lead to the most valuable states.

This indirect method leads us to the idea of value functions.

### *2.7.3 Value functions*

*Value functions* are functions that map a state or a state-action pair to the *expected value* (the expected reward) of being in some state or taking some action in some state. You may recall from statistics that the expected reward is just the long-term average of rewards received after being in some state or taking some action. When we speak of *the* value function, we usually mean a state-value function.

Table 2.7 The state-value function

| <b>Math</b>                          | <b>English</b>                                                                                                                                         |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| $V_r$ s $\rightarrow$ $E(R s,\pi)$ , | A value function, $V_m$ is a function that maps a state, s, to the expected<br>rewards, given that we start in state s and follow some policy, $\pi$ . |

This is a function that accepts a state, *s*, and returns the expected reward of starting in that state and taking actions according to our policy,  $\pi$ . It may not be immediately obvious why the value function depends on the policy. Consider that in our contextual bandit problem, if our policy was to choose entirely random actions (i.e., sample actions from a uniform distribution), the value (expected reward) of a state would probably be pretty low, since we're definitely not choosing the best possible actions. Instead, we want to use a policy that is not a uniform distribution over the actions, but is the probability distribution that would produce the maximum rewards when sampled. That is, the policy is what determines observed rewards, and the value function is a reflection of observed rewards.

 In our first *n*-armed bandit problem, you were introduced to state-action-value functions. These functions often go by the name *Q function* or *Q value*, which is where deep Q-learning comes from, since, as you'll see in the next chapter, deep learning algorithms can be used as Q functions.

| Table 2.8 | The action-value (Q) function |  |  |
|-----------|-------------------------------|--|--|
|-----------|-------------------------------|--|--|

| <b>Math</b>                                     | <b>English</b>                                                                                                                                                                                           |
|-------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| $Q_{\pi}$ (s a) $\rightarrow$ E(R a,s, $\pi$ ), | $Q_{\pi}$ is a function that maps a pair, (s, a), of a state, s, and an action, a, to<br>the expected reward of taking action a in state s, given that we're using the<br>policy (or "strategy") $\pi$ . |

In fact, we sort of implemented a deep Q-network to solve our contextual bandit problem (although it was a pretty shallow neural network), since it was essentially acting as a Q function. We trained it to produce accurate estimates of the expected reward for taking an action given a state. Our policy function was the softmax function over the output of the neural network.

 We've covered many of the foundational concepts in reinforcement learning just by using *n*-armed and contextual bandits as examples. We also got our feet wet with deep reinforcement learning in this chapter. In the next chapter we'll implement a full-blown deep Q-network similar to the algorithm that DeepMind used to play Atari games at superhuman levels. It will be a natural extension of what we've covered here.

### *Summary*

- State spaces are the set of all possible states a system can be in. In Chess, this would be the set of all valid board configurations. An action is a function that maps a state, *s*, to a new state, *s*′. An action may be stochastic, such that it maps a state, *s*, probabilistically to a new state, *s*′. There may be some probability distribution over the set of possible new states from which one is selected. The action-space is the set of all possible actions for a particular state.
- The environment is the source of states, actions, and rewards. If we're building an RL algorithm to play a game, then the game is the environment. A model of an environment is an approximation of the state space, action space, and transition probabilities.
- Rewards are signals produced by the environment that indicate the relative success of taking an action in a given state. An expected reward is a statistical concept that informally refers to the long-term average value of some random variable *X* (in our case, the reward), denoted  $E[X]$ . For example, in the *n*-armed bandit case,  $E[R|a]$  (the expected reward given action *a*) is the long-term average reward of taking each of the *n*-actions. If we knew the probability distribution over the actions, *a*, then we could calculate the precise value of the expected reward for a game of *N* plays as  $E[R|a_i] = \sum_{i=1}^{N} a_i p_i \cdot r$ , where *N* is the number of plays of the game,  $p_i$  refers to the probability of action  $a_i$ , and  $r$  refers to the maximum possible reward.
- An agent is an RL algorithm that learns to behave optimally in a given environment. Agents are often implemented as a deep neural network. The goal of the agent is to maximize expected rewards, or equivalently, to navigate to the highest value state.
- A policy is a particular strategy. Formally, it's a function that either accepts a state and produces an action to take or produces a probability distribution over the action space, given the state. A common policy is the epsilon-greedy strategy, where with probability  $\varepsilon$  we take a random action in the action space, and with probability  $\varepsilon$  – 1 we choose the best action we know of so far.
- In general, a value function is any function that returns expected rewards given some relevant data. Without additional context, it typically refers to a state-value function, which is a function that accepts a state and returns the expected reward of starting in that state and acting according to some policy. The Q value is the expected reward given a state-action pair, and the Q function is a function that produces Q values when given a state-action pair.
- The Markov decision process is a decision-making process by which it is possible to make the best decisions without reference to a history of prior states.