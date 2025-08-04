# *What is reinforcement learning?*

#### *This chapter covers*

- A brief review of machine learning
- Introducing reinforcement learning as a subfield
- The basic framework of reinforcement learning

*Computer languages of the future will be more concerned with goals and less with procedures specified by the programmer.*

—Marvin Minksy, 1970 ACM Turing Lecture

If you're reading this book, you are probably familiar with how deep neural networks are used for things like image classification or prediction (and if not, just keep reading; we also have a crash course in deep learning in the appendix). *Deep reinforcement learning* (DRL) is a subfield of machine learning that utilizes deep learning models (i.e., neural networks) in reinforcement learning (RL) tasks (to be defined in section 1.2). In image classification we have a bunch of images that correspond to a set of discrete categories, such as images of different kinds of animals, and we want a machine learning model to interpret an image and classify the kind of animal in the image, as in figure 1.1.

![](_page_1_Figure_1.jpeg)

![](_page_1_Figure_2.jpeg)

# *1.1 The "deep" in deep reinforcement learning*

Deep learning models are just one of many kinds of machine learning models we can use to classify images. In general, we just need some sort of function that takes in an image and returns a class label (in this case, the label identifying which kind of animal is depicted in the image), and usually this function has a fixed set of adjustable *parameters*—we call these kinds of models *parametric* models. We start with a parametric model whose parameters are initialized to random values—this will produce random class labels for the input images. Then we use a *training* procedure to adjust the parameters so the function iteratively gets better and better at correctly classifying the images. At some point, the parameters will be at an optimal set of values, meaning that the model cannot get any better at the classification task. Parametric models can also be used for *regression,* where we try to fit a model to a set of data so we can make predictions for unseen data (figure 1.2). A more sophisticated approach might perform even better if it had more parameters or a better internal architecture.

 Deep neural networks are popular because they are in many cases the most accurate parametric machine learning models for a given task, like image classification. This is largely due to the way they represent data. Deep neural networks have many layers (hence the "deep"), which induces the model to learn layered representations of input data. This layered representation is a form of *compositionality*, meaning that a complex piece of data is represented as the combination of more elementary components, and those components can be further broken down into even simpler components, and so on, until you get to atomic units.

 Human language is compositional (figure 1.3). For example, a book is composed of chapters, chapters are composed of paragraphs, paragraphs are composed of sentences, and so on, until you get to individual words, which are the smallest units of meaning. Yet each individual level conveys meaning—an entire book is meant to convey meaning, and its individual paragraphs are meant to convey smaller points. Deep neural networks can likewise learn a compositional representation of data—for example, they can represent an image as the composition of primitive contours and textures,

![](_page_2_Figure_1.jpeg)

![](_page_2_Figure_2.jpeg)

Figure 1.2 Perhaps the simplest machine learning model is a simple linear function of the form  $f(x) = mx + b$ , with parameters *m* (the slope) and *b* (the intercept). Since it has adjustable parameters, we call it a *parametric* function or model. If we have some 2-dimensional data, we can start with a randomly initialized set of parameters, such as  $[m = 3.4, b = 0.3]$ , and then use a training algorithm to optimize the parameters to fit the training data, in which case the optimal set of parameters is close to  $[m = 2, b = 1].$ 

![](_page_2_Figure_4.jpeg)

Figure 1.3 A sentence like "John hit the ball" can be decomposed into simpler and simpler parts until we get the individual words. In this case, we can decompose the sentence (denoted S) into a subject noun (N) and a verb phrase (VP). The VP can be further decomposed into a verb, "hit," and a noun phrase (NP). The NP can then be decomposed into the individual words "the" and "ball."

which are composed into elementary shapes, and so on, until you get the complete, complex image. This ability to handle complexity with compositional representations is largely what makes deep learning so powerful.

# *1.2 Reinforcement learning*

It is important to distinguish between problems and their solutions, or in other words, between the tasks we wish to solve and the algorithms we design to solve them. Deep learning algorithms can be applied to many problem types and tasks. Image classification and prediction tasks are common applications of deep learning because automated image processing before deep learning was very limited, given the complexity of images. But there are many other kinds of tasks we might wish to automate, such as driving a car or balancing a portfolio of stocks and other assets. Driving a car includes some amount of image processing, but more importantly the algorithm needs to learn how to *act*, not merely to classify or predict. These kinds of problems, where decisions must be made or some behavior must be enacted, are collectively called *control tasks*.

![](_page_3_Figure_4.jpeg)

Figure 1.4 As opposed to an image classifier, a reinforcement learning algorithm dynamically interacts with data. It continually consumes data and decides what actions to take—actions that will change the subsequent data presented to it. A video game screen might be input data for an RL algorithm, which then decides which action to take using the game controller, and this causes the game to update (e.g. the player moves or fires a weapon).

*Reinforcement learning* is a generic framework for representing and solving control tasks, but within this framework we are free to choose which algorithms we want to apply to a particular control task (figure 1.4). Deep learning algorithms are a natural choice as they are able to process complex data efficiently, and this is why we'll focus on *deep* reinforcement learning, but much of what you'll learn in this book is the general reinforcement framework for control tasks (see figure 1.5). Then we'll look at how you can design an appropriate deep learning model to fit the framework and solve a task. This means you will learn a lot about reinforcement learning, and you'll probably will learn some things about deep learning that you didn't know as well.

![](_page_4_Figure_1.jpeg)

for solving Figure 1.5 Deep learning is a subfield of machine learning. Deep learning algorithms can be used to power RL approaches to solving control tasks.

One added complexity of moving from image processing to the domain of control tasks is the additional element of time. With image processing, we usually train a deep learning algorithm on a fixed data set of images. After a sufficient amount of training, we typically get a high-performance algorithm that we can deploy to some new, unseen images. We can think of the data set as a "space" of data, where similar images are closer together in this abstract space and distinct images are farther apart (figure 1.6).

 In control tasks, we similarly have a space of data to process, but each piece of data also has a time dimension—the data exists in both time and space. This means that what the algorithm decides at one time is influenced by what happened at a previous time. This isn't the case for ordinary image classification and similar problems. Time

![](_page_4_Figure_5.jpeg)

Figure 1.6 This graphical depiction of words in a 2D space shows each word as a colored point. Similar words cluster together, and dissimilar words are farther apart. Data naturally lives in some kind of "space" with similar data living closer together. The labels A, B, C, and D point to particular clusters of words that share some semantics.

makes the training task dynamic—the data set upon which the algorithm is training is not necessarily fixed but changes based on the decisions the algorithm makes.

 Ordinary image classification-like tasks fall under the category of *supervised learning*, because the algorithm is trained on how to properly classify images by giving it the right answers. The algorithm at first takes random guesses, and it is iteratively corrected until it learns the features in the image that correspond to the appropriate label. This requires us to already know what the right answers are, which can be cumbersome. If you want to train a deep learning algorithm to correctly classify images of various species of plants, you would have to painstakingly acquire thousands of such images and manually associate class labels with each one and prepare the data in a format that a machine learning algorithm can operate on, generally some type of matrix.

 In contrast, in RL we don't know exactly what the right thing to do is at every step. We just need to know what the ultimate goal is and what things to avoid doing. How do you teach a dog a trick? You have to give it tasty treats. Similarly, as the name suggests, we train an RL algorithm by incentivizing it to accomplish some high-level goal and possibly disincentivize it from doing things we don't want it to do. In the case of a self-driving car, the high-level goal might be "get to point B from starting point A without crashing." If it accomplishes the task, we reward it, and if it crashes, we penalize it. We would do this all in a simulator, rather than out on the real roads, so we could let it repeatedly try and fail at the task until it learns and gets rewarded.

TIP In natural language, "reward" always means something positive, whereas in reinforcement learning jargon, it is a numeric quantity to be optimized. Thus, a reward can be positive or negative. When it is positive, it maps onto the natural language usage of the term, but when it is a negative value, it maps onto the natural language word "penalty."

The algorithm has a single objective—maximizing its reward—and in order to do this it must learn more elementary skills to achieve the main objective. We can also supply negative rewards when the algorithm chooses to do things we do not like, and since it is trying to maximize its reward, it will learn to avoid actions that lead to negative rewards. This is why it is called *reinforcement learning*: we either positively or negatively reinforce certain behaviors using reward signals (see figure 1.7). This is quite similar to how animals learn: they learn to do things that make them feel good or satisfied and to avoid things that cause pain.

![](_page_5_Figure_6.jpeg)

Figure 1.7 In the RL framework, some kind of learning algorithm decides which actions to take for a control task (e.g., driving a robot vacuum), and the action results in a positive or negative reward, which will positively or negatively reinforce that action and hence train the learning algorithm.

# *1.3 Dynamic programming versus Monte Carlo*

You now know that you can train an algorithm to accomplish some high-level task by assigning the completion of the task a high reward (i.e., positive reinforcement) and negatively reinforce things we don't want it to do. Let's make this concrete. Say the high-level goal is to train a robot vacuum to move from one room in a house to its dock, which is in the kitchen. It has four actions: go left, go right, go forward, and go reverse. At each point in time, the robot needs to decide which of these four actions to take. If it reaches the dock, it gets a reward of +100, and if it hits anything along the way, it gets a negative reward of –10. Let's say the robot has a complete 3D map of the house and has the precise location of the dock, but it still doesn't know exactly what sequence of primitive actions to take to get to the dock.

 One approach to solving this is called *dynamic programming* (DP), first articulated by Richard Bellman in 1957. Dynamic programming might better be called *goal decomposition* as it solves complex high-level problems by decomposing them into smaller and smaller subproblems until it gets to a simple subproblem that can be solved without further information.

 Rather than the robot trying to come up with a long sequence of primitive actions that will get it to the dock, it can first break the problem down into "stay in this room" versus "exit this room." Since it has a complete map of the house, it knows it needs to exit the room, because the dock is in the kitchen. Yet it still doesn't know what sequence of actions will allow it to exit the room, so it breaks the problem down further to "move toward the door" or "move away from the door." Since the door is closer to the dock, and there is a path from the door to the dock, the robot knows it needs to move toward the door, but again it doesn't know what sequence of primitive actions will get it toward the door. Lastly, it needs to decide whether to move left, right, forward, or reverse. It can see the door is in front of it, so it moves forward. It keeps this process up until it exits the room, when it must do some more goal decomposition until it gets to the dock.

 This is the essence of dynamic programming. It is a generic approach for solving certain kinds of problems that can be broken down into subproblems and subsubproblems, and it has applications across many fields including bioinformatics, economics, and computer science.

 In order to apply Bellman's dynamic programming, we have to be able to break our problem into subproblems that we know how to solve. But even this seemingly innocuous assumption is difficult to realize in the real world. How do you break the high-level goal for a self-driving car of "get to point B from point A without crashing" into small non-crashing subproblems? Does a child learn to walk by first solving easier sub-walking problems? In RL, where we often have nuanced situations that may include some element of randomness, we can't apply dynamic programming exactly as Bellman laid it out. In fact, DP can be considered one extreme of a continuum of problem-solving techniques, where the other end would be random trial and error.

 Another way to view this learning continuum is that in some situations we have maximal knowledge of the environment and in others we have minimal knowledge of the environment, and we need to employ different strategies in each case. If you need to use the bathroom in your own house, you know exactly (well, unconsciously at least) what sequence of muscle movements will get you to the bathroom from any starting position (i.e., dynamic programming-ish). This is because you know your house extremely well—you have a more or less perfect *model* of your house in your mind. If you go to a party at a house that you've never been to before, you might have to look around until you find the bathroom on your own (i.e., trial and error), because you don't have a good model of that person's house.

 The trial and error strategy generally falls under the umbrella of *Monte Carlo methods*. A Monte Carlo method is essentially a random sampling from the environment. In many real-world problems, we have at least some knowledge of how the environment works, so we end up employing a mixed strategy of some amount of trial and error and some amount of exploiting what we already know about the environment to directly solve the easy sub-objectives.

 A silly example of a mixed strategy would be if you were blindfolded, placed in an unknown location in your house, and told to find the bathroom by throwing pebbles and listening for the noise. You might start by decomposing the high-level goal (find the bathroom) into a more accessible sub-goal: figure out which room you're currently in. To solve this sub-goal, you might throw a few pebbles in random directions and assess the size of the room, which might give you enough information to infer which room you're in—say the bedroom. Then you'd need to pivot to another sub-goal: navigating to the door so you can enter the hallway. You'd then start throwing pebbles again, but since you remember the results of your last random pebble throwing, you could target your throwing to areas of less certainty. Iterating over this process, you might eventually find your bathroom. In this case, you would be applying both the goal decomposition of dynamic programming and the random sampling of Monte Carlo methods.

### *1.4 The reinforcement learning framework*

Richard Bellman introduced dynamic programming as a general method of solving certain kinds of control or decision problems, but it occupies an extreme end of the RL continuum. Arguably, Bellman's more important contribution was helping develop the standard framework for RL problems. The RL framework is essentially the core set of terms and concepts that every RL problem can be phrased in. This not only provides a standardized language for communicating with other engineers and researchers, it also forces us to formulate our problems in a way that is amenable to dynamic programming-like problem decomposition, such that we can iteratively optimize over local sub-problems and make progress toward achieving the global high-level objective. Fortunately, it's pretty simple too.

 To concretely illustrate the framework, let's consider the task of building an RL algorithm that can learn to minimize the energy usage at a big data center. Computers

need to be kept cool to function well, so large data centers can incur significant costs from cooling systems. The naive approach to keeping a data center cool would be to keep the air conditioning on all the time at a level that results in no servers ever running too hot; this would not require any fancy machine learning. But this is inefficient, and you could do better, since it's unlikely that all servers in the center are running hot at the same times and that the data center usage is always at the same level. If you targeted the cooling to where and when it mattered most, you could achieve the same result for less money.

 Step one in the framework is to define your overall objective. In this case, our overall objective is to minimize money spent on cooling, with the constraint that no server in our center can surpass some threshold temperature. Although this appears to be two objectives, we can bundle them together into a new composite *objective function*. This function returns an error value that indicates how off-target we are at meeting the two objectives, given the current costs and the temperature data for the servers. The actual number that our objective function returns is not important; we just want to make it as low as possible. Hence, we need our RL algorithm to minimize this objective (error) function's return value with respect to some input data, which will definitely include the running costs and temperature data, but may also include other useful contextual information that can help the algorithm predict the data center usage.

 The input data is generated by the *environment.* In general, the environment of a RL (or control) task is any dynamic process that produces data that is relevant to achieving our objective. Although we use "environment" as a technical term, it's not too far abstracted from its everyday usage. As an instance of a very advanced RL algorithm yourself, you are always in some environment, and your eyes and ears are constantly consuming information produced by your environment so you can achieve your daily objectives. Since the environment is a *dynamic process* (a function of time), it may be producing a continuous stream of data of varied size and type. To make things algorithm-friendly, we need to take this environment data and bundle it into discrete packets that we call the *state* (of the environment) and then deliver it to our algorithm at each of its discrete time steps. The state reflects our knowledge of the environment at some particular time, just as a digital camera captures a discrete snapshot of a scene at some time (and produces a consistently formatted image).

 To summarize so far, we defined an objective function (minimize costs by optimizing temperature) that is a function of the state (current costs, current temperature data) of the environment (the data center and any related processes). The last part of our model is the RL algorithm itself. This could be *any* parametric algorithm that can learn from data to minimize or maximize some objective function by modifying its parameters. It does *not* need to be a deep learning algorithm; RL is a field of its own, separate from the concerns of any particular learning algorithm.

 As we noted before, one of the key differences between RL (or control tasks generally) and ordinary supervised learning is that in a control task the algorithm needs to

make decisions and take actions. These actions will have a causal effect on what happens in the future. Taking an action is a keyword in the framework, and it means more or less what you'd expect it to mean. However, every action taken is the result of analyzing the current state of the environment and attempting to make the best decision based on that information.

 The last concept in the RL framework is that after each action is taken, the algorithm is given a *reward*. The reward is a (local) signal of how well the learning algorithm is performing at achieving the global objective. The reward can be a positive signal (i.e., doing well, keep it up) or a negative signal (i.e., don't do that) even though we call both situations a "reward."

 The reward signal is the only cue the learning algorithm has to go by as it updates itself in hopes of performing better in the next state of the environment. In our data center example, we might grant the algorithm a reward of +10 (an arbitrary value) whenever its action reduces the error value. Or more reasonably, we might grant a reward proportional to how much it decreases the error. If it increases the error, we would give it a negative reward.

 Lastly, let's give our learning algorithm a fancier name, calling it the *agent*. The agent is the action-taking or decision-making learning algorithm in any RL problem. We can put this all together as shown in figure 1.8.

![](_page_9_Figure_5.jpeg)

Figure 1.8 The standard framework for RL algorithms. The agent takes an action in the environment, such as moving a chess piece, which then updates the state of the environment. For every action it takes, it receives a reward (e.g., +1 for winning the game, –1 for losing the game, 0 otherwise). The RL algorithm repeats this process with the objective of maximizing rewards in the long term, and it eventually learns how the environment works.

In our data center example, we hope that our agent will learn how to decrease our cooling costs. Unless we're able to supply it with complete knowledge of the environment, it
will have to employ some degree of trial and error. If we're lucky, the agent might learn so well that it can be used in different environments than the one it was originally trained in. Since the agent is the learner, it is implemented as some sort of learning algorithm. And since this is a book about *deep* reinforcement learning, our agents will be implemented using *deep learning* algorithms (also known as *deep neural network*s, see figure 1.9). But remember, RL is more about the type of problem and solution than about any particular learning algorithm, and you could certainly use alternatives to deep neural networks. In fact, in chapter 3 we'll begin by using a very simple non-neural network algorithm, and we'll replace it with a neural network by the end of the chapter.

![](0__page_10_Figure_2.jpeg)

Figure 1.9 The input data (which is the state of the environment at some point in time) is fed into the agent (implemented as a deep neural network in this book), which then evaluates that data in order to take an action. The process is a little more involved than shown here, but this captures the essence.

The agent's only objective is to maximize its expected rewards in the long term. It just repeats this cycle: process the state information, decide what action to take, see if it gets a reward, observe the new state, take another action, and so on. If we set all this up correctly, the agent will eventually learn to understand its environment and make reliably good decisions at every step. This general mechanism can be applied to autonomous vehicles, chatbots, robotics, automated stock trading, healthcare, and much more. We'll explore some of these applications in the next section and throughout this book.

 Most of your time in this book will be spent learning how to structure problems in our standard model and how to implement sufficiently powerful learning algorithms

(agents) to solve difficult problems. For these examples, you won't need to construct environments—you'll be plugging into existing environments (such as game engines or other APIs). For example, OpenAI has released a Python Gym library that provides us with a number of environments and a straightforward interface for our learning algorithm to interact with. The code on the left of figure 1.10 shows how simple it is to set up and use one of these environments—a car racing game requires only five lines of code.

```
import gym
env = gym.make('CarRacing-v0')
env.reset()
env.step(action)
env.render()
```

![](0__page_11_Picture_3.jpeg)

Figure 1.10 The OpenAI Python library comes with many environments and an easy-to-use interface for a learning algorithm to interact with. With just a few lines of code, we've loaded up a car racing game.

## *1.5 What can I do with reinforcement learning?*

We began this chapter by reviewing the basics of ordinary supervised machine learning algorithms, such as image classifiers, and although recent successes in supervised learning are important and useful, supervised learning is not going to get us to artificial general intelligence (AGI). We ultimately seek general-purpose learning machines that can be applied to multiple problems with minimal to no supervision and whose repertoire of skills can be transferred across domains. Large data-rich companies can gainfully benefit from supervised approaches, but smaller companies and organizations may not have the resources to exploit the power of machine learning. General-purpose learning algorithms would level the playing field for everyone, and reinforcement learning is currently the most promising approach toward such algorithms.

 RL research and applications are still maturing, but there have been many exciting developments in recent years. Google's DeepMind research group has showcased some impressive results and garnered international attention. The first was in 2013 with an algorithm that could play a spectrum of Atari games at superhuman levels. Previous attempts at creating agents to solve these games involved fine-tuning the underlying algorithms to understand the specific rules of the game, often called *feature engineering*. These feature engineering approaches can work well for a particular game, but they are unable to transfer any knowledge or skills to a new game or domain. DeepMind's deep Q-network (DQN) algorithm was robust enough to work on seven

games without any game-specific tweaks (see figure 1.11). It had nothing more than the raw pixels from the screen as input and was merely told to maximize the score, yet the algorithm learned how to play beyond an expert human level.

![](0__page_12_Figure_2.jpeg)

Figure 1.11 DeepMind's DQN algorithm successfully learned how to play seven Atari games with only the raw pixels as input and the player's score as the objective to maximize. Previous algorithms, such as IBM's Deep Blue, needed to be fine-tuned to play a specific game.

More recently, DeepMind's AlphaGo and AlphaZero algorithms beat the world's best players at the ancient Chinese game Go. Experts believed artificial intelligence would not be able to play Go competitively for at least another decade because the game has characteristics that algorithms typically don't handle well. Players do not know the best move to make at any given turn and only receive feedback for their actions at the end of the game. Many high-level players saw themselves as artists rather than calculating strategists and described winning moves as being beautiful or elegant. With over  $10^{170}$ legal board positions, brute force algorithms (which IBM's Deep Blue used to win at chess) were not feasible. AlphaGo managed this feat largely by playing simulated games of Go millions of times and learning which actions maximized the rewards of playing the game well. Similar to the Atari case, AlphaGo only had access to the same information a human player would: where the pieces were on the board.

 While algorithms that can play games better than humans are remarkable, the promise and potential of RL goes far beyond making better game bots. DeepMind was able to create a model to decrease Google's data center cooling costs by 40%, something we explored earlier in this chapter as an example. Autonomous vehicles use RL to learn which series of actions (accelerating, turning, breaking, signaling) leads to passengers reaching their destinations on time and to learn how to avoid accidents. And researchers are training robots to complete tasks, such as learning to run, without explicitly programming complex motor skills.

 Many of these examples are high stakes, like driving a car. You cannot just let a learning machine learn how to drive a car by trial and error. Fortunately, there are an increasing number of successful examples of letting learning machines loose in harmless simulators, and once they have mastered the simulator, letting them try real hardware in the real world. One instance that we will explore in this book is algorithmic trading. A substantial fraction of all stock trading is executed by computers with little to no input from human operators. Most of these algorithmic traders are wielded by huge hedge funds managing billions of dollars. In the last few years, however, we've seen more and more interest by individual traders in building trading algorithms. Indeed, Quantopian provides a platform where individual users can write trading algorithms in Python and test them in a safe, simulated environment. If the algorithms perform well, they can be used to trade real money. Many traders have achieved relative success with simple heuristics and rule-based algorithms. However, equity markets are dynamic and unpredictable, so a continuously learning RL algorithm has the advantage of being able to adapt to changing market conditions in real time.

 One practical problem we'll tackle early in this book is advertisement placement. Many web businesses derive significant revenue from advertisements, and the revenue from ads is often tied to the number of clicks those ads can garner. There is a big incentive to place advertisements where they can maximize clicks. The only way to do this, however, is to use knowledge about the users to display the most appropriate ads. We generally don't know what characteristics of the user are related to the right ad choices, but we can employ RL techniques to make some headway. If we give an RL algorithm some potentially useful information about the user (what we would call the environment, or state of the environment) and tell it to maximize ad clicks, it will learn how to associate its input data to its objective, and it will eventually learn which ads will produce the most clicks from a particular user.

# *1.6 Why deep reinforcement learning?*

We've made a case for reinforcement learning, but why *deep* reinforcement learning? RL existed long before the popular rise of deep learning. In fact, some of the earliest methods (which we will look at for learning purposes) involved nothing more than storing experiences in a lookup table (e.g., a Python dictionary) and updating that table on each iteration of the algorithm. The idea was to let the agent play around in the environment and see what happened, and to store its experiences of what happened in some sort of database. After a while, you could look back on this database of knowledge and observe what worked and what didn't. No neural networks or other fancy algorithms.

 For very simple environments this actually works fairly well. For example, in Tic-Tac-Toe there are 255,168 valid board positions. The *lookup table* (also called a *memory table*) would have that many entries, which mapped from each state to a specific action (as shown in figure 1.12) and the reward observed (not depicted). During training, the algorithm could learn which move led toward more favorable positions and update that entry in the memory table.

 Once the environment gets more complicated, using a memory table becomes intractable. For example, every screen configuration of a video game could be considered a

![](0__page_14_Figure_1.jpeg)

#### **Game play lookup table**

different state (figure 1.13). Imagine trying to store every possible combination of valid pixel values shown on screen in a video game! DeepMind's DQN algorithm, which played Atari, was fed four  $84 \times 84$  grayscale images at each step, which would lead to 25628228 unique game states (256 different shades of grey per pixel, and 4\*84\*84=28228 pixels). This number is much larger than the number of atoms in the observable universe and would definitely not fit in computer memory. And this was after the images were scaled down to reduce their size from the original  $210 \times 160$ pixel color images.

![](0__page_14_Figure_4.jpeg)

Figure 1.13 A series of three frames of Breakout. The placement of the ball is slightly different in each frame. If you were using a lookup table, this would equate to storing three unique entries in the table. A lookup table would be impractical as there are far too many game states to store.

Storing every possible state isn't possible, but we could try to limit the possibilities. In the game Breakout, you control a paddle at the bottom of the screen that can move right or left; the objective of the game is to deflect the ball and break as many blocks at the top of the screen. In that case, we could define constraints—only look at the states when the ball is returning to the paddle, since our actions are not important while we are waiting for the ball at the top of the screen. Or we could provide our own features—instead of providing the raw image, just provide the position of the ball, paddle, and the remaining blocks. However, these methods require the programmer to understand the underlying strategies of the game, and they would not generalize to other environments.

 That's where deep learning comes in. A deep learning algorithm can learn to abstract away the details of specific arrangements of pixels and can learn the important features of a state. Since a deep learning algorithm has a finite number of parameters, we can use it to compress any possible state into something we can efficiently process, and then use that new representation to make our decisions. As a result of using neural networks, the Atari DQN only had 1792 parameters (convolutional neural network with  $168 \times 8$  filters,  $324 \times 4$  filters, and a 256-node fully connected hidden layer) as opposed to the  $256^{28228}$  key/value pairs that would be needed to store the entire state space.

 In the case of the Breakout game, a deep neural network might learn on its own to recognize the same high-level features a programmer would have to hand-engineer in a lookup table approach. That is, it might learn how to "see" the ball, the paddle, the blocks, and to recognize the direction of the ball. That's pretty amazing given that it's only being given raw pixel data. And even more interesting is that the learned highlevel features may be transferable to other games or environments.

 Deep learning is the secret sauce that makes all the recent successes in RL possible. No other class of algorithms has demonstrated the representational power, efficiency, and flexibility of deep neural networks. Moreover, neural networks are actually fairly simple!

# *1.7 Our didactic tool: String diagrams*

The fundamental concepts of RL have been well-established for decades, but the field is moving very quickly, so any particular new result could soon be out of date. That's why this book focuses on teaching skills, not details with short half-lives. We do cover some recent advances in the field that will surely be supplanted in the not too distant future, but we do so only to build new skills, not because the particular topic we're covering is necessarily a time-tested technique. We're confident that even if some of our examples become dated, the skills you learn will not, and you'll be prepared to tackle RL problems for a long time to come.

 Moreover, RL is a huge field with a lot to learn. We can't possibly hope to cover all of it in this book. Rather than be an exhaustive RL reference or comprehensive course, our goal is to teach you the foundations of RL and to sample a few of the most exciting recent developments in the field. We expect that you will be able to take what you've learned here and easily get up to speed in the many other areas of RL. Plus, we

have a section in chapter 11 that gives you a roadmap of areas you might want to check out after finishing this book.

 This book is focused on teaching well, but also rigorously. Reinforcement learning and deep learning are both fundamentally mathematical. If you read any primary research articles in these fields, you will encounter potentially unfamiliar mathematical notations and equations. Mathematics allows us to make precise statements about what's true and how things are related, and it offers rigorous explanations for how and why things work. We could teach RL without any math and just use Python, but that approach would handicap you in understanding future advances.

 So we think the math is important, but as our editor noted, there's a common saying in the publishing world: "for every equation in the book, the readership is halved," which probably has some truth to it. There's an unavoidable cognitive overhead in deciphering complex math equations, unless you're a professional mathematician who reads and writes math all day. Faced with wanting to present a rigorous exposition of DRL to give readers a top-rate understanding, and yet wanting to reach as many people as possible, we came up with what we think is a very distinguishing feature of this book. As it turns out, even professional mathematicians are becoming tired of traditional math notation with its huge array of symbols, and within a particular branch of advanced mathematics called *category theory*, mathematicians have developed a purely graphical language called *string diagrams*. String diagrams look very similar to flowcharts and circuit diagrams, and they have a fairly intuitive meaning, but they are just as rigorous and precise as traditional mathematical notations largely based on Greek and Latin symbols.

 Figure 1.14 shows a simple example of one type of string diagram that depicts, at a high level, a neural network with two layers. Machine learning (especially deep learning) involves a lot of matrix and vector operations, and string diagrams are particularly well-suited to describing these kinds of operations graphically. String diagrams are also great for describing complex processes because we can describe the process at varying levels of abstraction. The top panel of figure 1.14 shows two rectangles representing the two layers of the neural network, but then we can "zoom in" (look inside the box) on layer 1 to see what it does in more detail, which is shown in the bottom panel of figure 1.14.

 We will frequently use string diagrams throughout the book to communicate everything from complex mathematical equations to the architectures of deep neural networks. We will describe this graphical syntax in the next chapter, and we'll continue to refine and build it up throughout the rest of the book. In some cases, this graphical notation is overkill for what we're trying to explain, so we'll use a combination of clear prose and Python or pseudocode. We will also include traditional math notation in most cases, so you will be able to learn the underlying mathematical concepts one way or another, whether diagrams, code, or normal mathematical notation most connect with you.

![](0__page_17_Figure_1.jpeg)

Figure 1.14 A string diagram for a two-layer neural network. Reading from left to right, the top string diagram represents a neural network that accepts an input vector of dimension *n*, multiplies it by a matrix of dimensions *n* x *m*, returning a vector of dimension *m*. Then the nonlinear sigmoid activation function is applied to each element in the *m*-dimensional vector. This new vector is then fed through the same sequence of steps in layer 2, which produces the final output of the neural network, which is a *k*-dimensional vector.

## *1.8 What's next?*

In the next chapter, we will dive right into the real meat of RL, covering many of the core concepts, such as the tradeoff between exploration and exploitation, Markov decision processes, value functions, and policies (these terms will make sense soon). But first, at the beginning of the next chapter we'll introduce some of the teaching methods we'll employ throughout the book.

 The rest of the book will cover core DRL algorithms that much of the latest research is built upon, starting with deep Q-networks, followed by policy gradient approaches, and then model-based algorithms. We will primarily be utilizing OpenAI's Gym (mentioned earlier) to train our algorithms to understand nonlinear dynamics, control robots and play games (figure 1.15).

 In each chapter, we will open with a major problem or project that we will use to illustrate the important concepts and skills for that chapter. As each chapter progresses, we may add complexity or nuances to the starting problem to go deeper into some of the principles. For example, in chapter 2 we will start with the problem of maximizing rewards at a casino slot machine, and by solving that problem we'll cover most of the foundations of RL. Later we'll add some complexity to that problem and change the setting from a casino to a business that needs to maximize advertising clicks, which will allow us to round out a few more core concepts.

 Although this book is for those who already have experience with the basics of deep learning, we expect to not only teach you fun and useful RL techniques but also to hone your deep learning skills. In order to solve some of the more challenging projects, we'll need to employ some of the latest advances in deep learning, such as

![](0__page_18_Figure_1.jpeg)

Figure 1.15 A depiction of a Go board, an ancient Chinese game that Google DeepMind used as a testbed for its AlphaGo reinforcement learning algorithm. Professional Go player Lee Sedol only won one game out of five, marking a turning point for reinforcement learning, as Go was long thought to be impervious to the kind of algorithmic reasoning that chess is subject to. Source: <http://mng.bz/DNX0>.

generative adversarial networks, evolutionary methods, meta-learning, and transfer learning. Again, this is all in line with our skills-focused mode of teaching, so the particulars of these advances is not what's important.

### *Summary*

 Reinforcement learning is a subclass of machine learning. RL algorithms learn by maximizing rewards in some environment, and they're useful when a problem involves making decisions or taking actions. RL algorithms can, in principle, employ any statistical learning model, but it has become increasingly popular and effective to use deep neural networks.

- The agent is the focus of any RL problem. It is the part of the RL algorithm that processes input to determine which action to take. In this book we are primarily focused on agents implemented as deep neural networks.
- The environment is the potentially dynamic conditions in which the agent operates. More generally, the environment is whatever process generates the input data for the agent. For example, we might have an agent flying a plane in a flight simulator, so the simulator would be the environment.
- The state is a snapshot of the environment that the agent has access to and uses to make decisions. The environment is often a set of constantly changing conditions, but we can sample from the environment, and these samples at particular times are the state information of the environment we give to the agent.
- An action is a decision made by an agent that produces a change in its environment. Moving a particular chess piece is an action, and so is pressing the gas pedal in a car.
- A reward is a positive or negative signal given to an agent by the environment after it takes an action. The rewards are the only learning signals the agent is given. The objective of an RL algorithm (i.e., the agent) is to maximize rewards.
- The general pipeline for an RL algorithm is a loop in which the agent receives input data (the state of the environment), the agent evaluates that data and takes an action from a set of possible actions given its current state, the action changes the environment, and the environment then sends a reward signal and new state information to the agent. Then the cycle repeats. When the agent is implemented as a deep neural network, each iteration evaluates a loss function based on the reward signal and backpropagates to improve the performance of the agent.