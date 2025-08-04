# *Distributional DQN: Getting the full story*

#### *This chapter covers*

- Why a full probability distribution is better than a single number
- **Extending ordinary deep Q-networks to output full** probability distributions over Q values
- **IMPLEMENTIFY Interpollar Article 10 Interpollect Interpollect Interpollect Interpollect Interpollect Interpollect** play Atari Freeway
- **Understanding the ordinary Bellman equation and** its distributional variant
- **Prioritizing experience replay to improve training** speed

We introduced Q-learning in chapter 3 as a way to determine the value of taking each possible action in a given state; the values were called action values or Q values. This allowed us to apply a policy to these action values and to choose actions associated with the highest action values. In this chapter we will extend Q-learning to not just determine a point estimate for the action values, but an entire distribution of action values for each action; this is called *distributional Q-learning*. Distributional Q-learning has been shown to result in dramatically better performance on standard benchmarks, and it also allows for more nuanced decision-making, as you will see. Distributional Q-learning algorithms, combined with some other techniques covered in this book, are currently considered a state-of-the-art advance in reinforcement learning.

 Most environments we wish to apply reinforcement learning to involve some amount of randomness or unpredictability, where the rewards we observe for a given state-action pair have some variance. In ordinary Q-learning, which we might call *expected-value Q-learning*, we only learn the average of the noisy set of observed rewards. But by taking the average, we throw away valuable information about the dynamics of the environment. In some cases, the rewards observed may have a more complex pattern than just being clustered around a single value. There may be two or more clusters of different reward values for a given state-action; for example, sometimes the same state-action will result in a large positive reward and sometimes in a large negative reward. If we just take the average, we will get something close to 0, which is never an observed reward in this case.

 Distributional Q-learning seeks to get a more accurate picture of the distribution of observed rewards. One way to do this would be to keep a record of all the rewards observed for a given state-action pair. Of course, this would require a lot of memory, and for state spaces of high dimensionality it would be computationally impractical. This is why we must make some approximations. But first, let's delve deeper into what expected-value Q-learning is missing, and what distributional Q-learning offers.

### *7.1 What's wrong with Q-learning?*

The expected-value type of Q-learning we're familiar with is flawed, and to illustrate this we'll consider a real-world medical example. Imagine we are a medical company, and we want to build an algorithm to predict how a patient with high blood pressure (hypertension) will respond to 4-week course of a new anti-hypertensive drug called Drug X. This will help us decide whether or not to prescribe this drug to an individual patient.

 We gather a bunch of clinical data by running a randomized clinical trial in which we take a population of patients with hypertension and randomly assign them to a treatment group (those who will get the real drug) and a control group (those who will get a placebo, an inactive drug). We then record blood pressure over time while the patients in each group are taking their respective drugs. At the end we can see which patients responded to the drug and how much better they did compared to the placebo (figure 7.1).

 Once we've collected our data, we can plot a histogram of the change in blood pressure after four weeks on the drug for the treatment and control groups. We might see something like the results in figure 7.2.

![](_page_2_Figure_1.jpeg)

Figure 7.1 In a randomized control trial of a drug, we study the outcome of some treatment compared to a placebo (a nonactive substance). We want to isolate the effect we are trying to treat, so we take a population with some condition and randomly sort them into two groups: a treatment group and a control group. The treatment group gets the experimental drug we are testing, and the control group gets the placebo. After some time, we can measure the outcome for both groups of patients and see if the treatment group, on average, had a better response than the placebo group.

If you first look at the control group histogram in figure 7.2, it appears to be a normallike distribution centered around –3.0 mmHg (a unit of pressure), which is a fairly insignificant reduction in blood pressure, as you would expect from a placebo. Our algorithm would be correct to predict that for any patient given a placebo, their expected blood pressure change would be –3.0 mmHg on average, even though individual patients had greater or lesser changes than that average value.

 Now look at the treatment group histogram. The distribution of blood pressure change is bimodal, meaning there are two peaks, as if we had combined two separate normal distributions. The right-most mode is centered at –2.5 mmHg, much like the control group, suggesting that this subgroup within the treatment group did not benefit from the drug compared to the placebo. However, the left-most mode is centered at –22.3 mmHg, which is a very significant reduction in blood pressure. In fact, it's greater than any currently existing anti-hypertensive drug. This again indicates that there is a subgroup within the treatment group, but this subgroup strongly benefits from the drug.

 If you're a physician, and a patient with hypertension walks into your office, all else being equal, should you prescribe them this new drug? If you take the expected value (the average) of the treatment group distribution, you'd only get about –13 mmHg change in blood pressure, which is between the two modes in the distribution. This is still significant compared to the placebo, but it's worse than many existing anti-hypertensives on the market. By that standard, the new drug does not appear to be very effective, despite the fact that a decent number of patients get tremendous benefit from it. Moreover, the expected value of –13 mmHg is very poorly representative of the distribution, since very few patients actually had that level of blood pressure reduction. Patients either had almost no response to the drug or a very robust response; there were very few moderate responders.

 Figure 7.3 illustrates the limitations of expected values compared to seeing the full distribution. If you use the expected values of blood pressure changes for each drug, and just pick the drug with the lowest expected value in terms of blood pressure

![](_page_3_Figure_1.jpeg)

Figure 7.2 Histogram of the measured blood pressure change for the control and treatment groups in a simulated randomized control trial. The *x*-axis is the change in blood pressure from the start (before treatment) to after treatment. We want blood pressure to decrease, so negative numbers are good. We count the number of patients who have each value of blood pressure change, so the peak at –3 for the control group means that most of those patients had a blood pressure drop of 3 mmHg. You can see that there are two subgroups of patients in the treatment group: one group had a significant reduction in blood pressure, and another group had minimal to no effect. We call this a bimodal distribution, where *mode* is another word for "peak" in the distribution.

![](_page_4_Figure_1.jpeg)

![](_page_4_Figure_2.jpeg)

Figure 7.3 Here we compare simulated Drug A to Drug X to see which lowers blood pressure the most. Drug A has a lower average (expected) value of –15.5 mmHg and a lower standard deviation, but Drug X is bimodal with one mode centered at –22.5 mmHg. Notice that for Drug X virtually no patients had a blood pressure change that fell near the average value.

change (ignoring patient-specific complexities, such as side effects), you will be acting optimally at the population level, but not necessarily at the individual level.

 So what does this have to do with deep reinforcement learning? Well, Q-learning, as you've learned, gives us the expected (average, time-discounted) state-action values. As you might imagine, this can lead to the same limitations we've been discussing in the case of drugs, with multimodal distributions. Learning a full probability distribution of state-action values would give us a lot more power than just learning the expected value, as in ordinary Q-learning. With the full distribution, we could see if there is multimodality in the state-action values and how much variance there is in the distribution. Figure 7.4 models the action-value distributions for three different actions, and you can see that some actions have more variance than others. With this additional information,

![](_page_5_Figure_3.jpeg)

Figure 7.4 Top: An ordinary Q function takes a state-action pair and computes the associated Q value. Middle: A distributional Q function takes a state-action pair and computes a probability distribution over all possible Q values. Probabilities are bounded in the interval [0,1], so it returns a vector with all elements in [0,1] and their sum is 1. Bottom: An example Q value distribution produced by the distributional Q function for three different actions for some state. Action A is likely to lead to an average reward of –5, whereas action B is likely to lead to an average reward of +4.

we can employ risk-sensitive policies—policies that aim not merely to maximize expected rewards but also to control the amount of risk we take in doing so.

 Most convincingly, an empirical study was done that evaluated several popular variants and improvements to the original DQN algorithm, including a distributional variant of DQN, to see which were most effective alone and which were most important in combination ("Rainbow: Combining Improvements in Deep Reinforcement Learning" by Hessel et al., 2017). It turns out that distributional Q-learning was the best-performing algorithm overall, among all the individual improvements to DQN that they tested. They combined all the techniques together in a "Rainbow" DQN, which was shown to be far more effective than any individual technique. They then tested to see which components were most crucial to the success of Rainbow, and the results were that distributional Q-learning, multistep Q-learning (covered in chapter 5), and prioritized replay (which will be briefly covered in section 7.7) were the most important to the Rainbow algorithm's performance.

 In this chapter you will learn how to implement a distributional deep Q-network (Dist-DQN) that outputs a probability distribution over state-action values for each possible action given a state. We saw some probability concepts in chapter 4, where we employed a deep neural network as a policy function that directly output a probability distribution over actions, but we will review these concepts and go into even more depth here, as these concepts are important to understand in order to implement Dist-DQN. Our discussion of probability and statistics may seem a bit too academic at first, but it will become clear why we need these concepts for a practical implementation.

 This chapter is the most conceptually difficult chapter in the whole book as it contains a lot of probability concepts that are difficult to grasp at first. There is also more math here than in any other chapter. Getting through this chapter is a big accomplishment; you will learn or review a lot of fundamental topics in machine learning and reinforcement learning that will give you a greater grasp of these fields.

## *7.2 Probability and statistics revisited*

While the mathematics behind probability theory is consistent and uncontroversial, the interpretation of what it means to say something as trivial as "the probability of a fair coin turning up heads is 0.5" is actually somewhat contentious. The two major camps are called *frequentists* and *Bayesians*.

 A frequentist says the probability of a coin turning up heads is whatever proportion of heads are observed if one could flip the coin an infinite number of times. A short sequence of coin flips might yield a proportion of heads as high as 0.8, but as you keep flipping, it will tend toward 0.5 exactly, in the infinite limit.

 Hence, probabilities are just frequencies of events. In this case, there are two possible outcomes, heads or tails, and each outcome's probability is its frequency after an infinite number of trials (coin flips). This is, of course, why probabilities are values between 0 (impossible) and 1 (certain), and the probabilities for all possible outcomes must sum to 1.

 This is a simple and straightforward approach to probability, but it has significant limitations. In the frequentist setting, it is difficult or perhaps impossible to make sense of a question like "what is the probability that Jane Doe will be elected to city council?" since it is impossible in practice and theory for such an election to happen an infinite number of times. Frequentist probability doesn't make much sense for these kinds of one-off events. We need a more powerful framework to handle these situations, and that is what Bayesian probability gives us.

 In the Bayesian framework, probabilities represent degrees of belief about various possible outcomes. You can certainly have a belief about something that can only happen once, like an election, and your belief about what is likely to happen can vary depending on how much information you have about a particular situation, and new information will cause you to update your beliefs (see table 7.1).

| Table 7.1 | <b>Frequentist versus Bayesian probabilities</b> |  |  |
|-----------|--------------------------------------------------|--|--|
|-----------|--------------------------------------------------|--|--|

| <b>Frequentist</b>                                   | <b>Bayesian</b>                                    |  |
|------------------------------------------------------|----------------------------------------------------|--|
| Probabilities are frequencies of individual outcomes | Probabilities are degrees of belief                |  |
| Computes the probability of the data given a model   | Computes the probability of a model given the data |  |
| Uses hypothesis testing                              | Uses parameter estimation or model comparison      |  |
| Is computationally easy                              | Is (usually) computationally difficult             |  |

The basic mathematical framework for probability consists of a *sample space*, Ω, which is the set of all possible outcomes for a particular question. In the case of an election, for example, the sample space is the set of all candidates eligible to be elected. There is a probability distribution (or measure) function,  $P:\Omega \to [0,1]$ , where *P* is a function from the sample space to real numbers in the interval from 0 to 1. You could plug in *P*(*candidate A*) and it will spit out a number between 0 and 1 indicating the probability of candidate A winning the election.

NOTE Probability theory is more complicated than what we've articulated here and involves a branch of mathematics called *measure theory*. For our purposes, we do not need to delve any deeper into probability theory than we already have. We will stick with an informal and mathematically nonrigorous introduction to the probability concepts we need.

The *support* of a probability distribution is another term we will use. The support is just the subset of outcomes that are assigned nonzero probabilities. For example, temperatures can't be less than 0 Kelvin, so negative temperatures would be assigned probability 0; the support of the probability distribution over temperatures would be from 0 to positive infinity. Since we generally don't care about outcomes that are impossible, you'll often see "support" and "sample space" used interchangeably, even though they may not be the same.

#### *7.2.1 Priors and posteriors*

If we were to ask you "what is the probability of each candidate in a 4-way race winning?" without specifying who the candidates were or what the election was about, you might refuse to answer, citing insufficient information. If we really pressed you, you might say that since you know nothing else, each candidate has a  $\frac{1}{4}$  chance of winning. With that answer, you've established a *prior probability distribution* that is uniform (each possible outcome has the same probability) over the candidates.

 In the Bayesian framework, probabilities represent beliefs, and beliefs are always tentative in situations when new information can become available, so a prior probability distribution is just the distribution you start with before receiving some new information. After you receive new information, such as some biographical information about the candidates, you might update your prior distribution based on that new information—this updated distribution is now called your *posterior probability distribution*. The distinction between prior and posterior distribution is contextual, since your posterior distribution will become a new prior distribution right before you receive another set of new information. Your beliefs are continually updated as a succession of prior distributions to posterior distributions (see figure 7.5), and this process is generically called *Bayesian inference*.

![](_page_8_Figure_4.jpeg)

Figure 7.5 Bayesian inference is the process of starting with a prior distribution, receiving some new information, and using that to update the prior into a new, more informed distribution called the posterior distribution.
## *7.2.2 Expectation and variance*

There are a number of questions we can ask a probability distribution. We can ask what the single "most likely" outcome is, which we commonly think of as the *mean* or *average* of the distribution. You're probably familiar with the calculation of the mean as taking the sum of all the results and dividing by the number of results. For example, the mean of the 5-day temperature forecast of [18, 21, 17, 17, 21]<sup>o</sup>C is [18 + 21 + 17 +  $17 + 21$ / $5 = 94/5 = 18.8$ °C. This is the average predicted temperature over a sample of 5 days in Chicago, Illinois, USA.

 Consider if instead we asked five people to give us their prediction for tomorrow's temperature in Chicago and they happened to give us the same numbers, [18, 21, 17, 17, 21]°C. If we wanted the average temperature for tomorrow, we would follow the same procedure, adding the numbers up and dividing by the number of samples (five) to get the average predicted temperature for tomorrow. But what if person 1 was a meteorologist, and we had a lot more confidence in their prediction compared to the other four people that we randomly polled on the street? We would probably want to weight the meteorologist's prediction higher than the others. Let's say we think that their prediction is 60% likely to be true, and the other four are merely 10% likely to be true (notice  $0.6 + 4 * 0.10 = 1.0$ ), this is a *weighted average*; it's computed by multiplying each sample by its weight. In this case, that works out as follows:  $[(0.6 * 18) + 0.1 * (21 + 17 + 17 + 21)] = 18.4$ <sup>o</sup>C.

 Each temperature is a possible outcome for tomorrow, but not all outcomes are equally likely in this case, so we multiply each possible outcome by its probability (weight) and then sum. If all the weights are equal and sum to 1, we get an ordinary average calculation, but many times it is not. When the weights are not all the same, we get a weighted average called the *expectation value* of a distribution.

 The expected value of a probability distribution is its "center of mass," the value that is most likely on average. Given a probability distribution,  $P(x)$ , where *x* is the sample space, the expected value for discrete distributions is calculated as follows.

| <b>Math</b>                         | <b>Python</b>                                                                                                                                                                                     |
|-------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| $\mathbb{E}[P] = \sum x \cdot P(x)$ | >>> $x = np.array([1, 2, 3, 4, 5, 6])$<br>>>> $p = np.array([0.1, 0.1, 0.1, 0.1, 0.2, 0.4])$<br>$\Rightarrow$ def expected value $(x, p)$ :<br>>>> return x @ p<br>>>> expected value(x,p)<br>4.4 |

Table 7.2 Computing an expected value from a probability distribution

The expected value operator (where *operator* is another term for *function*) is denoted , and it's a function that takes in a probability distribution and returns its expected value. It works by taking a value, *x*, multiplying by its associated probability,  $P(x)$ , and summing for all possible values of *x*.

In Python, if  $P(x)$  is represented as a numpy array of probabilities, probs, and another numpy array of outcomes (the sample space), the expected value is

```
>>> import numpy as np
>>> probs = np.array([0.6, 0.1, 0.1, 0.1, 0.1])
>>> outcomes = np.array([18, 21, 17, 17, 21])
>>> expected_value = 0.0
>>> for i in range(probs.shape[0]):
>>> expected value += probs[i] * outcomes[i]
>>> expected_value
18.4
```

Alternatively, the expected value can be computed as the inner (dot) product between the probs array and the outcomes array, since the inner product does the same thing—it multiplies each corresponding element in the two arrays and sums them all.

```
>>> expected_value = probs @ outcomes
>>> expected_value
18.4
```

A discrete probability distribution means that its sample space is a finite set, or in other words, only a finite number of possible outcomes can occur. A coin toss, for example, can only have one of two outcomes.

 However, tomorrow's temperature could be any real number (or if measured in Kelvin, it could be any real number from  $0$  to infinity), and the real numbers or any subset of the real numbers is infinite since we can continually divide them: 1.5 is a real number, and so is 1.500001, and so forth. When the sample space is infinite, this is a *continuous probability distribution*.

 In a continuous probability distribution, the distribution does not tell you the probability of a particular outcome, because with an infinite number of possible outcomes, each individual outcome must have an infinitely small probability in order for the sum to be 1. Thus, a continuous probability distribution tells you the *probability density* around a particular possible outcome. The probability density is the sum of probabilities around a small interval of some value—it's the probability that the outcome will fall within some small interval. The difference between discrete and continuous distributions is depicted in figure 7.6. That's all we'll say about continuous distributions for now because in this book we'll really only deal with discrete probability distributions.

 Another question we can ask of a probability distribution is its spread or *variance*. Our beliefs about something can be more or less confident, so a probability distribution can be narrow or wide respectively. The calculation of variance uses the expectation operator and is defined as  $Var(X) = \sigma^2 = \mathbb{E}[(X - \mu)^2]$ , but don't worry about remembering this equation—we will use built-in numpy functions to compute variance. Variance is either denoted *Var*(*X*) or  $\vec{\sigma}$  (sigma squared) where  $\sqrt[\backslash]{\sigma^2} = \sigma$  is the standard deviation, so the variance is the standard deviation squared. The  $\mu$  in this

![](0__page_11_Figure_1.jpeg)

Figure 7.6 Left: A discrete distribution is like a numpy array of probabilities associated with another numpy array of outcome values. There is a finite set of probabilities and outcomes. Right: A continuous distribution represents an infinite number of possible outcomes, and the y axis is the probability density (which is the probability that the outcome takes on a value within a small interval).

equation is the standard symbol for mean, which again is  $\mu = \mathbb{E}[X]$ , where *X* is a *random variable* of interest.

 A random variable is just another way of using a probability distribution. A random variable is associated with a probability distribution, and a probability distribution can yield random variables. We can create a random variable, *T*, for tomorrow's temperature. It is a random variable since it is an unknown value but it can only take on specific values that are valid with respect to its underlying probability distribution. We can use random variables wherever a normal deterministic variable might be used, but if we add a random variable with a deterministic variable, we will get a new random variable.

 For example, if we think tomorrow's temperature is just going to be today's temperature plus some random noise, we can model this as  $T = t_0 + e$ , where *e* is a random variable of noise. The noise might have *normal (Gaussian) distribution* centered around 0 with a variance of 1. Thus *T* will be a new normal distribution with mean  $t_0$  (today's temperature), but it will still have a variance of 1. A normal distribution is the familiar bell-shaped curve.

 Table 7.3 shows a few common distributions. The normal distribution gets wider or narrower depending on the variance parameter, but otherwise it looks the same for any set of parameters. In contrast, the beta and gamma distributions can look quite different depending on their parameters—two different versions of each of these are shown. Random variables are typically denoted with a capital letter like *X*. In Python, we might set up a random variable using numpy's random module:

```
\Rightarrow > t0 = 18.4
\Rightarrow \rightarrow T = lambda: t0 + np.random.randn(1)
>>> T()
array([18.94571853])
>> T()
array([18.59060686])
```

![](0__page_12_Figure_1.jpeg)

![](0__page_12_Figure_2.jpeg)

Here we made *T* an anonymous function that accepts no arguments and just adds a small random number to 18.4 every time it is called. The variance of *T* is 1, which means that most of the values that *T* returns will be within 1 degree of 18.4. If the variance was 10, the spread of likely temperatures would be greater. Generally we start with a prior distribution that has high variance, and as we get more information the variance decreases. However, it is possible for new information to increase the variance of the posterior if the information we get is very unexpected and makes us less certain.

# *7.3 The Bellman equation*

We mentioned Richard Bellman in chapter 1, but here we will discuss the Bellman equation, which underpins much of reinforcement learning. The Bellman equation shows up everywhere in the reinforcement learning literature, but if all you want to do is write Python, you can do that without understanding the Bellman equation. This section is optional; it's for those interested in a bit more mathematical background.

 As you'll recall, the Q function tells us the value of a state-action pair, and value is defined as the expected sum of time-discounted rewards. In the Gridworld game, for example,  $Q_{\pi}(s, a)$  tells us the average rewards we will get if we take action *a* in state *s* and follow policy  $\pi$  from then forward. The optimal  $Q$  function is denoted  $Q^*$  and is the Q function that is perfectly accurate. When we first start playing a game with a randomly initialized Q function, it is going to give us very inaccurate Q value predictions, but the goal is to iteratively update the Q function until it gets close to the optimal *Q*\* .

 The Bellman equation tells us how to update the Q function when rewards are observed,

$$
Q_{\pi}(s_t, a_t) \leftarrow r_t + \gamma \cdot V_{\pi}(s_{t+1}),
$$

where  $V_{\pi}(s_{t+1}) = max[Q_{\pi}(s_{t+1}, a)]$ 

So the Q value of the current state,  $Q_{\pi}(s_h, a)$ , should be updated to be the observed reward  $r_t$  plus the value of the next state  $V_\pi(s_{t+1})$  multiplied by the discount factor γ (the left-facing arrow in the equation means "assign the value on the right side to the variable on the left side"). The value of the next state is simply whatever the highest Q value is for the next state (since we get a different Q value for each possible action).

 If we use neural networks to approximate the Q function, we try to minimize the error between the predicted  $Q_{\pi}(s_h, a_t)$  on the left side of the Bellman equation and the quantity on the right side by updating the neural network's parameters.

#### *7.3.1 The distributional Bellman equation*

The Bellman equation implicitly assumes that the environment is deterministic and thus that observed rewards are deterministic (i.e., the observed reward will be always the same if you take the same action in the same state). In some cases this is true, but in other cases it is not. All the games we have used and will use (except for Gridworld) involve at least some amount of randomness. For example, when we downsample the

frames of a game, two originally different states will get mapped into the same downsampled state, leading to some unpredictability in observed rewards.

In this case, we can make the deterministic variable  $r_t$  into a random variable  $R(s_b, a)$  that has some underlying probability distribution. If there is randomness in how states evolve into new states, the Q function must be a random variable as well. The original Bellman equation can now be represented as

$$
Q(s_t, a_t) \leftarrow \mathbb{E}\left[R(s_t, a)\right] + \gamma \cdot \mathbb{E}\left[Q(S_{t+1}, A_{t+1})\right]
$$

Again, the Q function is a random variable because we interpret the environment as having stochastic transitions. Taking an action may not lead to the same next state, so we get a probability distribution over next states and actions. The expected Q value of the next state-action pair is the most likely Q value given the most likely next stateaction pair.

 If we get rid of the expectation operator, we get a full distributional Bellman equation:

$$
Z(s_t, a_t) \leftarrow R(s_t, a_t) + \gamma \cdot Z(S_{t+1}, A_{t+1})
$$

Here we use *Z* to denote the distributional Q value function (which we will also refer to as the *value distribution*). When we do Q-learning with the original Bellman equation, our Q function will learn the expected value of the value distribution because that is the best it can do, but in this chapter we will use a slightly more sophisticated neural network that will return a value distribution and thus can learn the distribution of observed rewards rather than just the expected value. This is useful for the reasons we described in the first section—by learning a distribution we have a way to utilize risk-sensitive policies that take into consideration the variance and possible multimodality of the distribution.

# *7.4 Distributional Q-learning*

We've now covered all the preliminaries necessary to implement a distributional deep Q-network (Dist-DQN). If you didn't completely understand all of the material in the previous sections, don't worry; it will become more clear when we start writing the code.

 In this chapter we are going to use one of the simplest Atari games in the OpenAI Gym, Freeway (figure 7.7), so that we can train the algorithm on a laptop CPU. Unlike other chapters, we're also going to use the RAM version of the game. If you look at the available game environments at <https://gym.openai.com/envs/#atari>, you will see that each game has two versions, with one being labeled with "RAM."

 Freeway is a game where you control a chicken with actions of UP, DOWN, or NO-OP ("no-operation" or do nothing). The objective is to move the chicken across the freeway, avoiding oncoming traffic, to get to the other side, where you get a reward of +1. If you don't get all three chickens across the road in a limited amount of time, you lose the game and get a negative reward.

![](0__page_15_Picture_1.jpeg)

Figure 7.7 Screenshot from the Atari game Freeway. The objective is to move the chicken across the freeway, avoiding oncoming traffic.

In most cases in this book, we train our DRL agents using the raw pixel representation of the game and thus use convolutional layers in our neural network. In this case, though, we're introducing new complexity by making a distributional DQN, so we'll avoid convolutional layers to keep the focus on the topic at hand and keep the training efficient.

 The RAM version of each game is essentially a compressed representation of the game in the form of a 128-element vector (the positions and velocities of each game character, etc.). A 128-element vector is small enough to process through a few fully connected (dense) layers. Once you are comfortable with the simple implementation we'll use here, you can use the pixel version of the game and upgrade the Dist-DQN to use convolutional layers.

## *7.4.1 Representing a probability distribution in Python*

If you didn't read the optional section 7.3, the only important thing you missed is that instead of using a neural network to represent a Q function,  $Q_{\pi}(s, a)$ , that returns a single Q value, we can instead denote a value distribution,  $Z_{\pi}(s,a)$ , that represents a random variable of Q values given a state-action pair. This probabilistic formalism subsumes the deterministic algorithms we've been using in prior chapters, since a deterministic outcome can always be represented by a *degenerate* probability distribution (figure 7.8), where all the probability is assigned to a single outcome.

 Let's first start with how we're going to represent and work with value distributions. As we did in the section on probability theory, we will represent a discrete probability distribution over rewards using two numpy arrays. One numpy array will be the possible outcomes (i.e., the *support* of the distribution), and the other will be an equal-sized

![](0__page_16_Figure_1.jpeg)

Figure 7.8 This is a *degenerate* distribution, since all the possible values are assigned a probability of 0 except for one value. The outcome values that are *not* assigned 0 probability are called the probability distribution's *support*. The degenerate distribution has a support of 1 element (in this case, the value 0).

array storing the probabilities for each associated outcome. Recall, if we take the inner product between the support array and the probability array, we get the expected reward of the distribution.

One problem with the way we're representing the value distribution,  $Z(s,a)$ , is that since our array is a finite size, we can only represent a finite number of outcomes. In some cases, the rewards are usually restricted within some fixed, finite range, but in the stock market, for example, the amount of money you can make or lose is theoretically unlimited. With our method, we have to choose a minimum and maximum value that we can represent. This limitation has been solved in a follow-up paper by Dabney et al., "Distributional Reinforcement Learning with Quantile Regression" (2017). We will briefly discuss their approach at the end of the chapter.

 For Freeway, we restrict the support to be between –10 and +10. All time steps that are *nonterminal* (i.e., those that don't result in a winning or losing state) give a reward of –1 to penalize taking too much time crossing the road. We reward +10 if the chicken successfully crosses the road and –10 if the game is lost (if the chicken doesn't cross the road before the timer runs out). When the chicken gets hit by a car, the game isn't necessarily lost; the chicken just gets pushed down away from the goal.

 Our Dist-DQN will take a state, which is a 128-element vector, and will return 3 separate but equal-sized tensors representing the probability distribution over the support for each of the 3 possible actions (UP, DOWN, NO-OP) given the input state. We will use a 51-element support, so the support and probability tensors will be 51 elements.

 If our agent begins the game with a randomly initialized Dist-DQN, takes action UP, and receives a reward of –1, how do we update our Dist-DQN? What is the target distribution and how do we compute a loss function between two distributions? Well, we use whatever distribution the Dist-DQN returns for the subsequent state,  $s_{t+1}$ , as a prior distribution, and we update the prior distribution with the single observed reward,  $r_t$ , such that a little bit of the distribution gets redistributed around the observed  $r_t$ .

If we start with a uniform distribution and observe  $r_t = -1$ , the posterior distribution should no longer be uniform, but it should still be pretty close (figure 7.9). Only if we repeatedly observe  $r<sub>t</sub> = -1$  for the same state should the distribution start to strongly peak around  $-1$ . In normal Q-learning, the discount rate,  $\gamma$  (gamma), controlled how much the expected future rewards contribute to the value of the current state. In distributional Q-learning, the  $\gamma$  parameter controls how much we update the prior toward the observed reward, which achieves a similar function (figure 7.10).

 If we discount the future a lot, the posterior will be strongly centered around the recently observed reward. If we weakly discount the future, the observed reward will only mildly update the prior distribution,  $Z(S_{t+1}, A_{t+1})$ . Since Freeway has sparse positive rewards in the beginning (because we need to take many actions before we observe our first win), we will set gamma so we only make small updates to the prior distribution.

 In listing 7.1 we set up an initial uniform discrete probability distribution and show how to plot it.

![](0__page_17_Figure_6.jpeg)
![](1__page_18_Figure_1.jpeg)

Normal-ish distribution

![](1__page_18_Figure_3.jpeg)

![](1__page_18_Figure_4.jpeg)

![](1__page_18_Figure_5.jpeg)

Figure 7.9 We've created a function that takes a discrete distribution and updates it based on observed rewards. This function is performing a kind of approximate Bayesian inference by updating a prior distribution into a posterior distribution. Starting from a uniform distribution (on top, we observe some rewards and we get a peaked distribution at 0 (shown in the middle), and then we observe even more rewards (all zeros), and the distribution becomes a narrow, normal-like distribution (as shown on the bottom).

![](1__page_19_Figure_1.jpeg)

Figure 7.10 This figure shows how a uniform distribution changes with lower or higher values for gamma (the discount factor).

We have defined a uniform probability distribution; now let's see how we update the distribution. We want a function, update\_dist(z, reward), that takes a prior distribution and an observed reward and returns a posterior distribution. We represent the support of the distribution as a vector from –10 to 10:

```
>>> support
array([-10. , -9.6, -9.2, -8.8, -8.4, -8. , -7.6, -7.2, -6.8,
      -6.4, -6., -5.6, -5.2, -4.8, -4.4, -4., -3.6, -3.2-2.8, -2.4, -2., -1.6, -1.2, -0.8, -0.4, 0., 0.4,
 0.8, 1.2, 1.6, 2. , 2.4, 2.8, 3.2, 3.6, 4. ,
        4.4, 4.8, 5.2, 5.6, 6. , 6.4, 6.8, 7.2, 7.6,
        8. , 8.4, 8.8, 9.2, 9.6, 10. ])
```

We need to be able to find the closest support element in the support vector to an observed reward. For example, if we observe  $r_t = -1$ , we'll want to map that to either  $-1.2$ or –0.8 since those are the closest (equally close) support elements. More importantly, we want the indices of these support elements so that we can get their corresponding probabilities in the probability vector. The support vector is static—we never update it. We only update the corresponding probabilities.

 You can see that each support element is 0.4 away from its nearest neighbors. The numpy linspace function creates a sequence of evenly spaced elements, and the spacing is given by  $\frac{v_{max} - v_{min}}{N-1}$ , where *N* is the number of support elements. If you plug 10, –10, and *N* = 51 into that formula, you get 0.4. We call this value *dz* (for delta Z), and we use it to find the closest support element index value by the equation  $b_j = \frac{r - v_{min}}{dz}$ , where  $b_j$  is the index value. Since  $b_j$  may be a fractional number, and indices need to be non-negative integers, we simply round the value to the nearest whole number with

 $np$ . round( $\dots$ ). We also need to clip any values outside the minimum and maximum support range. For example, if the observed  $r_t = -2$  then  $b_j = \frac{-2 - (-10)}{0.4} = \frac{-2 + 10}{0.4} = 20$ . You can see that the support element with index 20 is  $-2$ , which in this case exactly corresponds to the observed reward (no rounding needed). We can then find the corresponding probability for the –2 support element using the index.

 Once we find the index value of the support element corresponding to the observed reward, we want to redistribute some of the probability mass to that support and the nearby support elements. We have to take care that the final probability distribution is a real distribution and sums to 1. We will simply take some of the probability mass from the neighbors on the left and right and add it to the element that corresponds to the observed reward. Then those nearest neighbors will steal some probability mass from their nearest neighbor, and so on, as shown in figure 7.11. The amount of probability mass stolen will get exponentially smaller the farther we go from the observed reward.

![](1__page_20_Picture_3.jpeg)

Figure 7.11 The **update\_dist** function redistributes probability from neighbors toward the observed reward value.

In listing 7.2 we implement the function that takes a set of supports, the associated probabilities, and an observation, and returns an updated probability distribution by redistributing the probability mass toward the observed value.

```
def update dist(r,support,probs,lim=(-10.,10.),gamma=0.8):
     nsup = probs.shape[0]
  Listing 7.2 Updating a probability distribution
```

![](1__page_21_Figure_1.jpeg)

Let's walk through the mechanics of this to see how it works. We start with a uniform prior distribution:

```
>>> probs
array([0.01960784, 0.01960784, 0.01960784, 0.01960784, 0.01960784,
        0.01960784, 0.01960784, 0.01960784, 0.01960784, 0.01960784,
        0.01960784, 0.01960784, 0.01960784, 0.01960784, 0.01960784,
        0.01960784, 0.01960784, 0.01960784, 0.01960784, 0.01960784,
        0.01960784, 0.01960784, 0.01960784, 0.01960784, 0.01960784,
        0.01960784, 0.01960784, 0.01960784, 0.01960784, 0.01960784,
        0.01960784, 0.01960784, 0.01960784, 0.01960784, 0.01960784,
        0.01960784, 0.01960784, 0.01960784, 0.01960784, 0.01960784,
        0.01960784, 0.01960784, 0.01960784, 0.01960784, 0.01960784,
        0.01960784, 0.01960784, 0.01960784, 0.01960784, 0.01960784,
        0.01960784])
```

You can see that each support has a probability of about 0.02. We observe  $r_t = -1$ , and we calculate  $b_i \approx 22$ . We then find the nearest left and right neighbors, denoted *m*<sub>l</sub> and *m*<sub>r</sub>, to be indices 21 and 23, respectively. We multiply *m*<sub>l</sub> by  $\gamma^j$ , where *j* is a value that we increment by 1 starting at 1, so we get a sequence of exponentially decreasing gammas:  $\gamma^! , \gamma^2 , \ldots \, \gamma^j .$  Remember, gamma must be a value between 0 and 1, so the sequence of gammas will be 0.5, 0.25, 0.125, 0.0625 if  $\gamma = 0.5$ . So at first we take  $0.5 * 0.02 = 0.01$  from the left and right neighbors and add it to the existing probability at  $b_j = 22$ , which is also 0.02. So the probability at  $b_j = 22$  will become  $0.01 + 0.01 + 0.02 = 0.04$ .

Now the left neighbor,  $m_l$ , steals probability mass from its own left neighbor at index 20, but it steals less because we multiply by  $\mathcal{V}$ . The right neighbor,  $m_p$  does the same by stealing from its neighbor on the right. Each element in turn steals from either its left or right neighbor until we get to the end of the array. If gamma is close to 1, like 0.99, a lot of probability mass will be redistributed to the support close to *rt*.

Let's test our distribution update function. We'll give it an observed reward of  $-1$ starting from a uniform distribution.

![](1__page_22_Figure_1.jpeg)

You can see in figure 7.12 that the distribution is still fairly uniform, but now there is a distinct "bump" centered at –1. We can control how big this bump is with the discount factor  $\gamma$ . On your own, try changing gamma to see how it changes the update.

![](1__page_22_Figure_3.jpeg)

Figure 7.12 This is the result of updating an initially uniform probability distribution after observing a single reward. Some probability mass is redistributed toward the support element corresponding to the observed reward.

Now let's see how the distribution changes when we observe a sequence of varying rewards. (We have just made up this sequence of rewards; they do not come from the Freeway game.) We should be able to observe multimodality.

```
ob_rewards = [10,10,10,0,1,0,-10,-10,10,10]
for i in range(len(ob_rewards)):
    Z = update dist(ob rewards[i], torch.from number(support).float(), Z, \n lim=(vmin,vmax), gamma=0.5)
plt.bar(support, Z)
  Listing 7.4 Redistributing probability mass with a sequence of observations
```

You can see in figure 7.13 that there are now four peaks of varying heights corresponding to the four different kinds of rewards observed, namely 10, 0, 1, and –10. The highest peak (mode of the distribution) corresponds to 10, since that was the most frequently observed reward.

![](1__page_23_Figure_2.jpeg)

Figure 7.13 This is the result of updating an initially uniform probability distribution after observing a sequence of different rewards. Each "peak" in the distribution corresponds to an observed reward.

Now let's see how the variance decreases if we observe the same reward multiple times, starting from a uniform prior.

```
ob_rewards = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
for i in range(len(ob_rewards)):
    Z = update dist(ob rewards[i], torch.from numpy(support).float(), \setminus Z, lim=(vmin,vmax), gamma=0.7)
plt.bar(support, Z)
  Listing 7.5 Decreased variance with sequence of same reward
```

You can see in figure 7.14 that the uniform distribution transforms into a normal-like distribution centered at 5 with much lower variance. We will use this function to generate the target distribution that we want the Dist-DQN to learn to approximate. Let's build the Dist-DQN now.

![](1__page_24_Figure_1.jpeg)

Figure 7.14 The result of updating an initially uniform probability distribution after observing the same reward multiple times. The uniform distribution converges toward a normal-like distribution.

## *7.4.2 Implementing the Dist-DQN*

As we briefly discussed earlier, the Dist-DQN will take a 128-element state vector, pass it through a couple of dense feedforward layers, and then it will use a for loop to multiply the last layer by 3 separate matrices to get 3 separate distribution vectors. We will lastly apply the softmax function to ensure it is a valid probability distribution. The result is a neural network with 3 different output "heads." We collect these 3 output distributions into a single  $3 \times 51$  matrix and return that as the final output of the Dist-DQN. Thus, we can get the individual action-value distributions for a particular action by indexing a particular row of the output matrix. Figure 7.15 shows the overall architecture and tensor transformations. In listing 7.6 we define the function that implements the Dist-DQN.

![](1__page_24_Figure_5.jpeg)

Figure 7.15 The Dist-DQN accepts a 128-element state vector and produces 3 separate 51-element probability distribution vectors, which then get stacked into a single  $3 \times 51$  matrix.

![](1__page_25_Figure_1.jpeg)

In this chapter we will do gradient descent manually, and to make this easier we have our Dist-DQN accept a single parameter vector called theta that we will unpack and reshape into multiple separate layer matrices of the appropriate sizes. This is easier since we can just do gradient descent on a single vector rather than on multiple separate entities. We also will use a separate target network as we did in chapter 3, so all we need to do is keep a copy of theta and pass that into the same dist\_dqn function.

 The other novelty here is the multiple output heads. We're used to a neural network returning a single output vector, but in this case we want it to return a matrix. To do that, we set up a loop where we multiply l2 by each of three separate layer matrices, resulting in three different output vectors that we stack into a matrix. Other than that, it is a very simple neural network with a total of five dense layers.

 Now we need a function that will take the output of our Dist-DQN, a reward, and an action, and generate the target distribution we want our neural network to get closer to. This function will use the update\_dist function we used earlier, but it only wants to update the distribution associated with the action that was actually taken. Also, as you learned in chapter 3, we also need a different target when we've reached a terminal state. At the terminal state, the expected reward is the observed reward, since there are no future rewards by definition. That means the Bellman update reduces to  $Z(s_t, a_t) \leftarrow R(S_t, A_t)$ . Since we only observe a single reward, and there is no prior distribution to update, the target becomes what is called a *degenerate distribution*. That's just a fancy term for a distribution where all the probability mass is concentrated at a single value.

![](1__page_26_Figure_1.jpeg)

The get target dist function takes a batch of data of shape  $B \times 3 \times 51$  where *B* is the batch dimension, and it returns an equal-sized tensor. For example, if we only have one example in our batch,  $1 \times 3 \times 51$ , and the agent took action 1 and observed a reward of  $-1$ , this function would return a  $1 \times 3 \times 51$  tensor, except that the  $1 \times 51$  distribution associated with index 1 (of dimension 1) will be changed according to the update dist function using the observed reward of  $-1$ . If the observed reward was instead 10, the  $1 \times 51$  distribution associated with action 1 would be updated to be a degenerate distribution where all elements have 0 probability except the one associated with the reward of 10 (index 50).

## *7.5 Comparing probability distributions*

Now that we have a Dist-DQN and a way to generate target distributions, we need a loss function that will calculate how different the predicted action-value distribution is from the target distribution; then we can backpropagate and do gradient descent as usual, to update the Dist-DQN parameters to be more accurate next time. We often use the mean squared error (MSE) loss function when trying to minimize the distance between two batches of scalars or vectors, but this is not an appropriate loss function between two probability distributions. But there are many possible choices for a loss function between probability distributions. We want a function that will measure how different or distant two probability distributions are and that will minimize that distance.

 In machine learning, we are usually trying to train a parametric model (e.g., a neural network) to predict or produce data that closely matches empirical data from
some data set. Thinking probabilistically, we can conceive of a neural network as generating synthetic data and trying to train the neural network to produce more and more realistic data—data that closely resembles some empirical data set. This is how we train *generative* models (models that generate data); we update their parameters so that the data they generate looks very close to some training (empirical) data set.

 For example, let's say we want to build a generative model that produces images of celebrities' faces (figure 7.16). In order to do this, we need some training data, so we use the freely available CelebA data set that contains hundreds of thousands of high quality photographs of various celebrities such as Will Smith and Britney Spears. Let's call our generative model *P* and this empirical data set *Q*.

![](2__page_27_Figure_3.jpeg)

Figure 7.16 A generative model can be a probabilistic model that trains by maximizing the probability that it generates samples that are similar to some empirical data set. Training happens in an iterative loop where the empirical data is supplied to the generative model, which tries to maximize the probability of the empirical data. Before training, the generative model will assign low probability to examples taken from the training data set, and the objective is for the generative model to assign high probability to examples drawn from the data set. After a sufficient number of iterations, the generative model will have assigned high probability to the empirical data, and we can then sample from this distribution to generate new, synthetic data.

The images in data set *Q* were sampled from the real world, but they are just a small sample of the infinite number of photographs that already exist but are not in the data set and that could have been taken but were not. For example, there may just be one headshot photo of Will Smith in the data set, but another photo of Will Smith taken at a different angle could just as easily have been part of the data set. A photo of Will Smith with a baby elephant on top of his head, while not impossible, would be less likely to be included in the data set because it is less likely to exist (who would put a baby elephant on their head?).

 There are naturally more and less likely photos of celebrities, so the real world has a probability distribution over images of celebrities. We can denote this true probability distribution of celebrity photos as  $Q(x)$ , where *x* is some arbitrary image, and  $Q(x)$ tells us the probability of that image existing in the world. If  $x$  is a specific image in data set Q, then  $Q(x) = 1.0$ , since that image definitely exists in the real world. However, if we plug in an image that's not in the data set but likely exists in the real world outside of our small sample, then *Q*(*x*) might equal 0.9.

 When we randomly initialize our generative model *P*, it will output random-looking images that look like white noise. We can think of our generative model as a random variable, and every random variable has an associated probability distribution that we denote  $P(x)$ , so we can also ask our generative model what the probability of a specific image is given its current set of parameters. When we first initialize it, it will think all images are more or less equally probable, and all will be assigned a fairly low probability. So if we ask *P*("Will Smith photo") it will return some tiny probability, but if we ask *Q*("Will Smith photo"), we'll get 1.0.

 In order to train our generative model *P* to generate realistic celebrity photos using data set *Q*, we need to ensure the generative model assigns high probability to the data in *Q* and also to data not in *Q* but that plausibly could be. Mathematically, we want to maximize this ratio:

$$
LR = \frac{P(x)}{Q(x)}
$$

We call this the *likelihood ratio* (LR) between  $P(x)$  and  $Q(x)$ . *Likelihood* in this context is just another word for *probability*.

 If we take the ratio for an example image of Will Smith that exists in *Q* using an untrained *P*, we might get

$$
LR = \frac{P(x = \text{Will Smith})}{Q(x = \text{Will Smith})} = \frac{0.0001}{1.0} = 0.0001
$$

This is a tiny ratio. We want to backpropagate into our generative model and do gradient descent to update its parameters so that this ratio is maximized. This likelihood ratio is the objective function we want to maximize (or minimize its negative).

 But we don't want to do this just for a single image; we want the generative model to maximize the total probability of all the images in data set *Q*. We can find this total probability by taking the product of all the individual examples (because the probability of *A and B* is the probability of *A times* the probability of *B* when *A* and *B* are independent and come from the same distribution). So our new objective function is the product of the likelihood ratios for each piece of data in the data set. We have several math equations coming up but we're just using them to explain the underlying probability concepts; don't spend any time trying to remember them.

Table 7.4 The likelihood ratio in math and Python

| <b>Math</b>                          | <b>Python</b>                                                                                            |
|--------------------------------------|----------------------------------------------------------------------------------------------------------|
| $LR = \prod_i \frac{P(x_i)}{Q(x_i)}$ | $p = np.array([0.1, 0.1])$<br>$q = np.array([0.6, 0.5])$<br>$def \; lr(p,q):$<br>return np.prod( $p/q$ ) |

One problem with this objective function is that computers have a hard time multiplying a bunch of probabilities, since they are tiny floating-point numbers that when multiplied together create even smaller floating-point numbers. This results in numerical inaccuracies and ultimately numerical underflow, since computers have a finite range of numbers they can represent. To improve this situation, we generally use log probabilities (equivalently, log likelihoods) because the logarithm function turns tiny probabilities into large numbers ranging from negative infinity (when the probability approaches 0) up to a maximum of 0 (when the probability is 1).

Logarithms also have the nice property that  $log(a \cdot b) = log(a) + log(b)$ , so we can turn multiplication into addition, and computers can handle that a lot better without risking numerical instability or overflows. We can transform the previous product loglikelihood ratio equation into this:

| Table 7.5 | The log-likelihood ratio in math and Python |  |  |  |  |
|-----------|---------------------------------------------|--|--|--|--|
|-----------|---------------------------------------------|--|--|--|--|

| <b>Math</b>                                       | <b>Python</b>                                                                                                     |
|---------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| $LR = \sum_{i} \log \left( \frac{1}{Q_i} \right)$ | $p = np.array([0.1, 0.1])$<br>$q = np.array([0.6, 0.5])$<br>$def \text{lr}(p,q):$<br>return $np.sum(np.log(p/q))$ |

This log-probability version of the equation is simpler and better for computation, but another problem is that we want to weight individual samples differently. For example, if we sample an image of Will Smith from the data set, it should have a higher probability than an image of some less famous celebrity, since the less famous celebrity probably has fewer photos taken of them. We want our model to put more weight on learning images that are more probable out in the real world or, in other words, with respect to the empirical distribution  $Q(x)$ . We will weight each log-likelihood ratio by its *Q*(*x*) probability.

|  | Table 7.6 The weighted log-likelihood ratio in math and Python |  |  |  |  |
|--|----------------------------------------------------------------|--|--|--|--|
|--|----------------------------------------------------------------|--|--|--|--|

| <b>Math</b>                                                            | <b>Python</b>                                                                                                                    |
|------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| $LR = \sum_{i} Q(x_i) \cdot \log \left( \frac{P(x_i)}{Q(x_i)} \right)$ | $p = np.array([0.1, 0.1])$<br>$q = np.array([0.6, 0.5])$<br>def Ir(p,q):<br>$x = q * np.log(p/q)$<br>$x = np.sum(x)$<br>return x |

We now have an objective function that measures how likely a sample from the generative model is, compared to the real-world distribution of data, weighted by how likely the sample is in the real world.

 There's one last minor problem. This objective function must be maximized because we want the log-likelihood ratio to be high, but by convenience and convention we

prefer to have objective functions that are error or loss functions to be minimized. We can remedy this by adding a negative sign, so a high likelihood ratio becomes a small error or loss.

| The Kullback-Leibler divergence<br>Table 7.7 |  |
|----------------------------------------------|--|
|----------------------------------------------|--|

| <b>Math</b>                                                                              | <b>Python</b>                                                                                                                              |
|------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| $D_{KL}(Q \parallel P) = -\sum_{i} Q(x_i) \cdot \log \left( \frac{P(x_i)}{O(x)} \right)$ | $p = np.array([0.1, 0.1])$<br>$q = np.array([0.6, 0.5])$<br>$def \; lr(p,q):$<br>$x = q * np.log(p/q)$<br>$x = -1$ * np.sum(x)<br>return x |

You may notice we switched out *LR* for some strange symbols:  $D_{KI}(Q||P)$ . It turns out the objective function we just created is a very important one in all of machine learning; it's called the *Kullback-Leibler divergence* (KL divergence for short). The KL divergence is a kind of error function between probability distributions; it tells you how different two probability distributions are.

 Often we are trying to minimize the distance between a model-generated probability distribution and some empirical distribution from real data, so we want to minimize the KL divergence. As you just saw, minimizing the KL divergence is equivalent to maximizing the joint log-likelihood ratio of the generated data compared to the empirical data. One important thing to note is that the KL divergence is not symmetric, i.e.,  $D_{KL}(Q||P) \neq D_{KL}(P||Q)$ , and this should be clear from its mathematical definition. The KL divergence contains a ratio, and no ratio can equal its inverse unless both are 1, i.e.,  $\frac{a}{b} \neq \frac{b}{a}$  unless  $a = b$ .  $\frac{a}{b} \neq \frac{b}{a}$ 

 Although the KL divergence makes a perfect objective function, we can simplify it just a bit for our purposes. Recall that  $log(a/b) = log(a) - log(b)$  in general. So we can rewrite the KL divergence as

$$
D_{KL}(Q||P) = -\sum_{i} Q(x) \cdot \log(P(x_i)) - \log(Q(x_i))
$$

Note that in machine learning, we only want to optimize the model (update the parameters of the model to reduce the error); we cannot change the empirical distribution  $Q(x)$ . Therefore, we really only care about the weighted log probability on the left side:

$$
H(Q, P) = -\Sigma_i Q(x) \cdot \log(P(x_i))
$$

This simplified version is called the cross-entropy loss and is denoted *H*(*Q*,*P*). This is the actual loss function that we will use in this chapter to get the error between our predicted action-value distribution and a target (empirical) distribution.

 In listing 7.8 we implement the cross-entropy loss as a function that takes a batch of action-value distributions and computes the loss between that and a target distribution.

```
def lossfn(x,y): 
                loss = torch.Tensor([0.])
                loss.requires_grad=True
           \Rightarrow for i in range(x.shape[0]):
                  loss = -1 * totch.log(x[i].flatten(start dim=0)) @ y[i].flatten(start_dim=0) 
                    loss = loss + loss_
                return loss
             Listing 7.8 The cross-entropy loss function
                                                  Loss between prediction distribution 
   Loops loss = torch. Tensor (10.1) x and target distribution y
 through
   batch
dimension
                                                       Flattens along action dimension 
                                                       to get a concatenated sequence 
                                                      of the distributions
```

The loss fn function takes a prediction distribution, x, of dimensions  $B \times 3 \times 51$  and a target distribution, y, of the same dimensions, and then it flattens the distribution over the action dimension to get a  $B \times 153$  matrix. Then it loops through each  $1 \times 153$ row in the matrix and computes the cross entropy between the  $1 \times 153$  prediction distribution and the  $1 \times 153$  target distribution. Rather than explicitly summing over the product of x and y, we can combine these two operations and get the result in one shot by using the inner product operator, @.

 We could choose to just compute the loss between the specific action-value distribution for the action that was taken, but we compute the loss for all three action-value distributions so that the Dist-DQN learns to keep the other two actions not taken unchanged; it only updates the action-value distribution that was taken.

## *7.6 Dist-DQN on simulated data*

Let's test all the parts so far with a simulated target distribution to see if our Dist-DQN can successfully learn to match the target distribution. In listing 7.9 we take an initially uniform distribution, run it through our Dist-DQN, and update it using a synthetic vector of two reward observations.

![](2__page_31_Figure_7.jpeg)

![](2__page_32_Figure_1.jpeg)

The purpose of the preceding code is to test the Dist-DQN's ability to learn the distribution for two samples of synthetic data. In our synthetic data, action 0 is associated with a reward of 0, and action 2 is associated with a reward of 10. We expect the Dist-DQN to learn that state 1 is associated with action 1 and state 2 with action 2 and learn the distributions. You can see, in figure 7.17, with the randomly initialized parameter

![](2__page_32_Figure_3.jpeg)

Figure 7.17 This shows the predicted action-value distributions produced by an untrained Dist-DQN and the target distribution after observing a reward. There are three separate action-value distributions of length 51 elements, but here they've been concatenated into one long vector to illustrate the overall fit between the prediction and target. The first 51 elements correspond to the action-value distribution of the NO-OP operation, the second 51 elements correspond to the action-value distribution of the UP action, and the last 51 elements correspond to the DOWN distribution. You can see the prediction is a completely flat (uniform) distribution for all three actions, whereas the target distribution has a mode (a peak) for action 0 and some noisy peaks for the other two actions. The goal is to get the prediction to match the target distribution.

vector, that the prediction distribution for all three actions (remember, we flattened it along the action dimension) is pretty much a uniform distribution, whereas the target distribution has a peak within action 0 (since we plotted only the first sample). After training, the prediction and target distributions should match fairly well.

 The reason why a target network is so important is very clear with Dist-DQN. Remember, a target network is just a copy of the main model that we update after some lag time. We use the target network's prediction to create the target for learning, but we only use the main model parameters to do gradient descent. This stabilizes the training because without a target network the target distribution will change after each parameter update from gradient descent.

 Yet gradient descent is trying to move the parameters toward better matching the target distribution, so there is a circularity (hence instability) that can lead to the target distribution dramatically changing as a result of this dance between the Dist-DQN's predictions and the target distribution. By using a lagged copy of the Dist-DQN prediction (via a lagged copy of the parameters, which is the target network), the target distribution does not change every iteration and is not immediately affected by the continual updates from the main Dist-DQN model. This significantly stabilizes the training. If you reduce the update\_rate to 1 and try training, you will see that the target evolves into something completely wrong. Let's now look at how to train the Dist-DQN.

![](2__page_33_Figure_4.jpeg)

The top graphic in figure 7.18 shows that the target and prediction from Dist-DQN now match almost exactly after training (you may not even be able to see that there are two overlapping distributions anymore). It works! The loss plot on the bottom of figure 7.18 has those spikes from each time the target network is synchronized to the

![](2__page_34_Figure_2.jpeg)

Figure 7.18 Top: The concatenated action-value distributions for all three actions after training. Bottom: Loss plot over training time. The baseline loss is decreasing, but we see ever-increasing spikes.

main model and the target distribution suddenly changes, leading to a higher than normal loss at that time step. We can also look at the learned distributions for each action for each sample in the batch. The following listing shows how to do this.

![](2__page_35_Figure_2.jpeg)

In figure 7.19 you can see that in the first sample, the distribution on the left associated with action 0 has collapsed into a degenerate distribution at 0, just like the simulated data. Yet the other two actions remain fairly uniform with no clear peaks. Similarly, in the second sample in the batch, the action 2 (DOWN) distribution is a degenerate distribution at 10, as the data was also degenerate (a sequence of identical samples), and the other two actions remain fairly uniform.

![](2__page_35_Figure_4.jpeg)

Figure 7.19 Each row contains the action-value distributions for an individual state, and each column in a row is the distribution for actions 0, 1, and 2 respectively.

This Dist-DQN test has almost everything we will use in a real experiment with Atari Freeway. There are just two functions we need before we get to playing Freeway. One will preprocess the states returned from the OpenAI Gym environment. We will get a 128-element numpy array with elements ranging from 0 to 255, and we'll need to
convert it to a PyTorch tensor and normalize the values to be between 0 and 1 to moderate the size of the gradients.

 We also need a policy function that decides which actions to take, given the predicted action-value distributions. With access to a full probability distribution over action values, we can utilize more sophisticated risk-sensitive policies. In this chapter, we will use a simple policy of choosing actions based on their expected value, in order to keep complexity to a minimum. Although we are learning a full probability distribution, we will choose actions based on their expected value, just like in ordinary Q-learning.

![](3__page_36_Figure_3.jpeg)

Recall, we can compute the expected (or expectation) value of a discrete distribution by simply taking the inner product of the support tensor with the probability tensor. We do this for all three actions and select the one that has the highest expected value. Once you get comfortable with the code here, you can try coming up with a more sophisticated policy, perhaps one that takes into consideration the variance (i.e., the confidence) of each action-value distribution.

## *7.7 Using distributional Q-learning to play Freeway*

We're finally ready to use the Dist-DQN algorithm to play the Atari game Freeway. We don't need any other major functionality besides what we've already described. We will have a main Dist-DQN model and a copy—the target network to stabilize training. We will use an epsilon-greedy strategy with a decreasing epsilon value over epochs: with probability epsilon the action selection will be random, otherwise the action will be selected by the get\_action function, which chooses based on the highest expected value. We will also use an experience replay mechanism, just like with an ordinary DQN.

 We will also introduce a very basic form of *prioritized replay*. With normal experience replay, we store all the experiences the agent has in a fixed-size memory buffer, and new experiences displace old ones at random; then we randomly sample a batch from this memory buffer for training. In a game like Freeway, though, where

almost all actions result in  $a -1$  reward and we rarely get  $a +10$  or  $-10$  reward, the experience replay memory is going to be heavily dominated by data that all says basically the same thing. It's not very informative to the agent, and the truly significant experiences such as winning or losing the game get strongly diluted, significantly slowing learning.

 To alleviate this problem, whenever we take an action that leads to a winning or losing state of the game (i.e., when we get a reward of  $-10$  or  $+10$ ), we add multiple copies of this experience to the replay buffer to prevent it from being diluted by all the –1 reward experiences. Hence, we *prioritize* certain highly informative experiences over other less informative experiences because we really want our agent to learn which actions lead to success or failure rather than just game continuation.

 If you access the code for this chapter on this book's GitHub at [http://mng.bz/JzKp,](http://mng.bz/JzKp) you will find the code we used to record frames of the live game play during training. We also recorded the real-time changes in the action-value distributions so you can see how the game play affects the predicted distributions and vice versa. We do not include that code here in the book, as it would take too much space. In listing 7.13 we initialize the hyperparameters and variables we'll need for our Dist-DQN algorithm.

```
import gym
                  from collections import deque
                 env = gym.make('Freeway-ram-v0')
                 aspace = 3env.env.get action meanings()
                 vmin,vmax = -10,10
                 replay_size = 200
                 batch size = 50nsup = 51dz = (vmax - vmin) / (nsup-1)support = touchuingace(winin,vmax,nsup)Learning    dereeplay = deque(maxlen=replay_size)    data structure
               \triangleright lr = 0.0001
                 qamma = 0.1epochs = 1300eps = 0.20\rhd eps min = 0.05
                 priority_level = 5 
                 update freq = 25#Initialize DQN parameter vector
                 tot params = 128*100 + 25*100 + aspace*25*51
               \triangleright theta = torch.randn(tot params)/10.
                 theta.requires_grad=True
                 theta 2 = \text{theta}.detach() .clone()Listing 7.13 Dist-DQN plays Freeway, preliminaries
                                                                      Experience replay 
                                                                      buffer using the deque 
       rate
   Discount
     factor
                                          Starting epsilon 
                                          for epsilon-greedy 
                                          policy
    Ending/
  minimum
    epsilon
                                                              Prioritized-replay; duplicates 
                                                              highly informative experiences in 
                                                              the replay this many times
                                                              Updates the target 
                                                              network every 25 steps
                                                                                 The total number of 
                                                                                 parameters for Dist-DQN
  Randomly
  initializes
 parameters
for Dist-DQN
                                                                Initializes parameters for 
                                                               target network
```

```
losses = []
cum_rewards = [] 
renders = []
state = preproc state(env.reset())
                                               Stores each win (successful 
                                               freeway crossing) as a 1 in 
                                              this list
```

These are all the settings and starting objects we need before we get to the main training loop. All of it is roughly the same as what we did for the simulation test, except we have a prioritized replay setting that controls how many copies of a highly informative experience (such as a win) we should add to the replay. We also use an epsilon-greedy strategy, and we will start with an initially high epsilon value and decrease it during training to a minimum value to maintain a minimal amount of exploration.

![](3__page_38_Figure_3.jpeg)

![](3__page_39_Figure_1.jpeg)

Almost all of this is the same kind of code we used for the ordinary DQN a few chapters ago. The only changes are that we're dealing with Q distributions rather than single Q values and that we use prioritized replay. If you plot the losses, you should get something like figure 7.20.

![](3__page_39_Figure_3.jpeg)

Figure 7.20 The loss plot for training Dist-DQN on the Atari game Freeway. The loss gradually declines but has significant "spikiness" due to the periodic target network updates.

The loss plot in figure 7.20 generally goes down but has "spikiness" due to the updates of the target network, just like we saw with the simulated example. If you investigate the cum rewards list, you should get a list of ones  $[1, 1, 1, 1, 1, 1]$  indicating how many successful chicken crossings occurred. If you're getting four or more, that indicates a successfully trained agent.

 Figure 7.21 shows a mid-training game screenshot alongside the corresponding predicted action-value distributions (again, refer to the GitHub code to see how to do this).

![](3__page_40_Figure_2.jpeg)

Figure 7.21 Left: Screenshot of live gameplay in Atari Freeway. Right: The corresponding action-value distributions of each of the each actions overlaid. The spike on the right corresponds to the UP action and the spike on the left corresponds mostly to the NO-OP action. Since the right spike is larger, the agent is more likely to take the UP action, which seems like the right thing to do in this case. It is difficult to see, but the UP action also has a spike on top of the NO-OP spike on the left, so the UP action-value distribution is bimodal, suggesting that taking the UP action might lead to either a -1 reward or a +10 reward, but the +10 reward is more likely since that spike is taller.

In figure 7.21 you can see that the action-value distribution for the UP action has two modes (peaks): one at  $-1$  and the other at  $+10$ . The expectation value of this distribution is much higher than the other actions, so this action will be selected.

 Figure 7.22 shows a few of the learned distributions in the experience replay buffer, to give you a better view of the distributions. Each row is a sample from the replay buffer associated with a single state. Each figure in a row is the action-value distribution for the NO-OP, UP, and DOWN actions respectively. Above each figure is the expected value of that distribution. You can see that in all the samples, the UP action has the highest expected value, and it has two clear peaks: one at –1 and another at +10. The distributions for the other two actions have a lot more variance, because once the agent learns that going up is the best way to win, there are fewer and fewer experiences using the other two actions, so they remain relatively uniform. If we continued training for longer, they would eventually converge to a peak at –1 and possibly a smaller peak at –10, since with epsilon greedy we will still be taking a few random actions.

![](3__page_41_Figure_1.jpeg)

Figure 7.22 Each column has the action-value distributions for a particular action for a given state (row). The number above each plot is the expectation value for that distribution, which is the weighted average value for that distribution. The distributions look fairly similar by eye, but the expected values are distinct enough to result in significantly different action selections.

Distributional Q-learning is one of the biggest improvements to Q-learning in the past few years, and it's still being actively researched. If you compare Dist-DQN to ordinary DQN, you should find you get better overall performance with Dist-DQN. It is not well understood why Dist-DQN performs so much better, especially given that we are only choosing actions based on expected values, but a few reasons are likely. One is that training a neural network to predict multiple things at the same time has been shown to improve generalization and overall performance. In this chapter, our Dist-DQN learned to predict three full probability distributions rather than a single action value, so these auxiliary tasks force the algorithm to learn more robust abstractions.

 We also discussed a significant limitation in the way we've implemented Dist-DQN, namely that we're using discrete probability distributions with finite support, so we can only represent action values within a very small range, from –10 to 10. We could make this range wider at the cost of more computational processing, but we can never represent an arbitrarily small or large value with this approach. The way we've implemented it is to use a fixed set of supports but learn the set of associated probabilities.

 One fix to this problem is to instead use a fixed set of probabilities over a variable (learned) set of supports. For example, we can fix our probability tensor to range from 0.1 to 0.9, e.g., array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]), and we instead have our Dist-DQN predict the set of associated supports for these fixed probabilities. That is, we're asking our Dist-DQN to learn what support value has a probability of 0.1, and 0.2, and so on. This is called *quantile regression* because these fixed probabilities end up representing quantiles of the distribution (figure 7.23). We learn the supports at and below the 50th percentile (probability 0.5), the 60th percentile, and so on.

![](3__page_42_Figure_1.jpeg)

Figure 7.23 In quantile regression, rather than learning what probabilities are assigned to a fixed set of supports, we learn a set of supports that correspond to a fixed set of probabilities (quantiles). Here you can see that the median value is 1 since it is at the 50th percentile.

With this approach, we still have a discrete probability distribution, but we can now represent any possible action value—it can be arbitrarily small or large and we have no fixed range.

## *Summary*

- The advantages of distributional Q-learning include improved performance and a way to utilize risk-sensitive policies.
- Prioritized replay can speed learning by increasing the proportion of highly informative experiences in the experience replay buffer.
- The Bellman equation gives us a precise way to update a Q function.
- **The OpenAI Gym includes alternative environments that produce RAM states,** rather than raw video frames. The RAM states are easier to learn since they are usually of much lower dimensionality.
- Random variables are variables that can take on a set of outcomes weighted by an underlying probability distribution.
- The entropy of a probability distribution describes how much information it contains.
- The KL divergence and cross-entropy can be used to measure the loss between two probability distributions.
- The support of a probability distribution is the set of values that have nonzero probability.
- Quantile regression is a way to learn a highly flexible discrete distribution by learning the set of supports rather than the set of probabilities.