# *Interpretable reinforcement learning: Attention and relational models*

#### *This chapter covers*

- **Implementing a relational reinforcement** algorithm using the popular self-attention model
- Visualizing attention maps to better interpret the reasoning of an RL agent
- Reasoning about model invariance and equivariance
- **Incorporating double Q-learning to improve the** stability of training

Hopefully by this point you have come to appreciate just how powerful the combination of deep learning and reinforcement learning is for solving tasks previously thought to be the exclusive domain of humans. Deep learning is a class of powerful learning algorithms that can comprehend and reason through complex patterns and data, and reinforcement learning is the framework we use to solve control problems.

 Throughout this book we've used games as a laboratory for experimenting with reinforcement learning algorithms as they allow us to assess the ability of these algorithms in a very controlled setting. When we build an RL agent that learns to play a game well, we are generally satisfied our algorithm is working. Of course, reinforcement learning has many more applications outside of playing games; in some of these other domains, the raw performance of the algorithm using some metric (e.g., the accuracy percentage on some task) is not useful without knowing *how* the algorithm is making its decision.

 For example, machine learning algorithms employed in healthcare decisions need to be explainable, since patients have a right to know *why* they are being diagnosed with a particular disease or why they are being recommended a particular treatment. Although conventional deep neural networks can be trained to achieve remarkable feats, it is often unclear what process is driving their decision-making.

 In this chapter we will introduce a new deep learning architecture that goes some way to unraveling this problem. Moreover, it not only offers interpretability gains but also performance gains in many cases. This new class of models is called *attention models* because they learn how to *attend to* (or focus on) only the salient aspects of an input. More specifically for our case, we will be developing a *self-attention model*, which is a model that allows each feature within an input to learn to attend to various other features in the input. This form of attention is closely related to the class of neural networks termed *graph neural networks*, which are neural networks explicitly designed to operate on graph structured data.

# *10.1 Machine learning interpretability with attention and relational biases*

A *graph* (also called a network) is a data structure that is composed of a set of *nodes* and *edges* (connections) between nodes (figure 10.1). The nodes could represent anything: people in a social network, publications in a publication citation network, cities connected by highways, or even images where each pixel is a node and adjacent pixels are connected by edges. A graph is a very generic structure for representing data with relational structure, which is almost all the data we see in practice. Whereas *convolutional neural networks* are designed to process grid-like data, such as images, and *recurrent neural networks* are well-poised for sequential data, graph neural networks are more generic in that they can handle any data that can be represented as a graph. Graph neural networks have opened up a whole new set of possibilities for machine learning and they are an active area of research (figure 10.2).

![](_page_1_Picture_6.jpeg)

Figure 10.1 A simple graph. Graphs are composed of nodes (the numberlabeled circles) and edges (the lines) between nodes that represent relationships between nodes. Some data is naturally represented with this kind of graph structure, and traditional neural network architectures are unable to process this kind of data. Graph neural networks (GNNs), on the other hand, can directly operate on graph-structured data.

*Self-attention models* (SAMs) can be used to construct graph neural networks, but our goal is not to operate on explicitly graph-structured data; we will instead be working with image data, as usual, but we will use a self-attention model to learn a graph

![](_page_2_Figure_1.jpeg)

Figure 10.2 A graph neural network can directly operate on a graph, compute over the nodes and edges, and return an updated graph. In this example, the graph neural network decides to remove the edge connecting the bottom two nodes. This is an abstract example, but the nodes could represent real world variables and the arrows represent causal direction, so the algorithm would be learning to infer causal pathways between variables.

representation of the features within the image. In a sense, we hope the SAM will convert a raw image into a graph structure, and that the graph structure it constructs will be somewhat interpretable. If we train a SAM on a bunch of images of people playing basketball, for example, we might hope it learns to associate the people with the ball, and the ball with the basket. That is, we want it to learn that the ball is a node, the basket is a node, and the players are nodes and to learn the appropriate edges between the nodes. Such a representation would give us much more insight into the mechanics of our machine learning model than would a conventional convolutional neural network or the like.

 Different neural network architectures such as convolutional, recurrent, or attention have different *inductive biases* that can improve learning when those biases are accurate. *Inductive reasoning* is when you observe some data and infer a more general pattern or rule from it. *Deductive reasoning* is what we do in mathematics when we start with some premises and by following logical rules assumed to be true, we can make a conclusion with certainty.

 For example, the syllogism "All planets are round. Earth is a planet. Therefore, the Earth is round" is a form of deductive reasoning. There is no uncertainty about the conclusion if we assume the premises to be true.

 Inductive reasoning, on the other hand, can only lead to probabilistic conclusions. Inductive reasoning is what you do when you play a game like chess. You cannot deduce what the other player is going to do; you have to rely on the available evidence

and make an inference. Biases are essentially your expectations before you have seen any data. If you always expected your chess opponent, no matter who it was, to make a particular opening move, that would be a strong (inductive) bias.

 Biases are often talked about in the pejorative sense, but in machine learning architectural biases are essential. It is the inductive bias of compositionality, i.e., that complex data can be decomposed into simpler and simpler components in a hierarchical fashion, that makes deep learning so powerful in the first place. If we know the data is images in a grid-like structure, we can make our models biased toward learning local features as convolutional neural networks do. If we know our data is relational, a neural network with a relational inductive bias will improve performance.

#### *10.1.1 Invariance and equivariance*

Biases are the prior knowledge we have about the structure of the data we wish to learn, and they make learning much faster. But there's more to it than just biases. With a convolutional neural network (CNN), the bias is toward learning local features, but CNNs also have the property of translation *invariance*. A function is said to be invariant to a particular transformation of its input when such a transformation does not change the output. For example, the addition function is invariant to the order of its inputs  $add(x,y) = add(y,x)$ , whereas the subtraction operator does not share this order invariance (this particular invariant property has its own special name: *commutativity*). In general, a function,  $f(x)$ , is invariant with respect to some transformation,  $g(x)$ , to its input, x, when  $f(g(x)) = f(x)$ . CNNs are functions in which a translation (movement up, down, left, or right) of an object in an image will not impact the behavior of the CNN classifier; it is invariant to translation (top panel of figure 10.3).

 If we use a CNN to detect the location of an object in an image, it is no longer invariant to translation but rather *equivariant* (bottom panel of figure 10.3). *Equivariance* is when  $f(g(x)) = g(f(x))$ , for some transformation function *g*. This equation says that if we take an image with a face in the center, apply a translation so the face is now in the top-left corner, and then run it through a CNN face detector, the result is the same as if we had just run the original centered image through the face detector and then translated the output to the top-left corner. The distinction is subtle, and often invariance and equivariance are used interchangeably since they are related.

 Ideally, we want our neural network architectures to be invariant to many kinds of transformations our input data might suffer. In the case of images, we generally want our machine learning model to be invariant to translations, rotations, smooth deformations (e.g., stretching or squeezing), and to noise. CNNs are only invariant or equivariant to translations but are not necessarily robust against rotations or smooth deformations.

 In order to get the kind of invariance we want, we need a *relational model*—a model that is capable of identifying objects and relating them to one another. If we have an image of a cup on top of a table, and we train a CNN to identify the cup, it will perform

![](_page_4_Figure_1.jpeg)

Figure 10.3 Invariance: Rotational invariance is a property of the function such that a rotation transformation of the input does not change the output of the function. Equivariance: Translational equivariance for a function is when applying the translation to the input results in the same output as when you apply the translation after the function has already been performed on the unaltered input.

well. But if we were to rotate the image 90 degrees, it would likely fail because it is not rotation-invariant, and our training data did not include rotated images. However, a (purely) relational model should, in principle, have no problem with this because it can learn to do relational reasoning. It can learn that "cups are on tables," and this relational description does not depend on a particular viewing angle. Hence, machine learning models with relational reasoning abilities can model powerful and generic relations between objects. *Attention models* are one way of achieving this and the topic of this chapter.

# *10.2 Relational reasoning with attention*

There are many possible ways of implementing a relational model. We know what we want: a model that can learn how objects in input data are related to one another. We also want the model to learn higher-level features over such objects, just like a CNN does. We also want to maintain the composability of ordinary deep learning models so we can stack together multiple layers (such as CNN layers) to learn more and more abstract features. And perhaps most important of all, we need this to be computationally efficient so we can train this relational model on large amounts of data.

 A generic model called *self-attention* meets all of these requirements, although it is less scalable than the other models we've looked at so far. Self-attention, as the name suggests, involves an attention mechanism in which the model can learn to attend to a subset of the input data. But before we get to self-attention, let's first talk about ordinary attention.

## *10.2.1 Attention models*

Attention models are loosely inspired by human and animal forms of attention. With human vision, we cannot see or focus on the entire field of view in front of us; our eyes make saccadic (rapid, jerky) movements to scan across the field of view, and we can consciously decide to focus on a particularly salient area within our view. This allows us to focus on processing the relevant aspects of a scene, which is an efficient use of resources. Moreover, when we're engaged in thought and reasoning, we can only attend to a few things at once. We also naturally tend to employ relational reasoning when we say things like "he is older than her" or "the door closed behind me;" we are relating the properties or behavior of certain objects in the world to others. Indeed, words in human language generally only convey meaning when related to other words. In many cases, there is no absolute frame of reference; we can only describe things as they relate to other things that we know.

*Absolute* (nonrelational) attention models are designed to function like our eyes in that they try to learn how to extract only the relevant parts of the input data for efficiency and interpretability (you can see what the model is learning to attend to when making a decision), whereas the self-attention model we will build here is a way of introducing relational reasoning into the model; the goal is not necessarily to distill the data.

 The simplest form of absolute attention for an image classifier would be a model that actively crops the image, selecting subregions from the image and only processing those (figure 10.4). The model would have to learn what to focus on, but this would tell us what parts of the image it is using to make its classification. This is difficult to implement because cropping is nondifferentiable. In order to crop a  $28 \times 28$  pixel image, we would need our model to produce integer-valued coordinates that form the rectangular subregion to subset, but integer-valued functions are noncontinuous and thus nondifferentiable, meaning we can't apply gradient descent-based training algorithms.

 We could train such a model using a genetic algorithm, as you learned in chapter 6, or we could use reinforcement learning. In the reinforcement learning case, the model would produce an integer set of coordinates, crop the image based on those coordinates, process the subregion, and make a classification decision. If it classifies correctly, it would get a positive reward, or it would get a negative reward for an incorrect classification. In this way, we could employ the REINFORCE algorithm you learned earlier to train the model to perform an otherwise nondifferentiable function. This

![](_page_6_Picture_1.jpeg)

Figure 10.4 An example of absolute attention where a function might simply look at subregions of an image and only process those one at a time. This can significantly reduce the computational burden, since the dimensionality of each segment is much smaller than the whole image.

procedure is described in the paper "Recurrent Models of Visual Attention" by Volodymyr Mnih et al. (2014). This form of attention is termed *hard* attention because it is nondifferentiable.

 There is also *soft* attention, which is a differentiable form of attention that simply applies a filter to minimize or maintain certain pixels in the image by multiplying each pixel in the image by a soft attention value between 0 and 1. The attention model can then learn to set certain pixels to 0 or maintain certain relevant pixels (figure 10.5). Since the attention values are real numbers and not integers, this form of attention is differentiable, but it loses the efficiency of a hard attention model, since it still needs to process the entire image rather than just a portion of it.

 In a self-attention model (SAM), the process is quite different and more complicated. Remember, the output of a SAM is essentially a graph, except that each node is constrained to only be connected with a few other nodes (hence the "attention" aspect).

![](_page_6_Picture_6.jpeg)

Figure 10.5 An example of soft attention where a model would learn which pixels to keep and which pixels to ignore (i.e., set to 0). Unlike the hard-attention model, the softattention model needs to process the entire image at once, which can be computationally demanding.

## *10.2.2 Relational reasoning*

Before we get into the details of self-attention, let's first sketch out how a general *relational reasoning module* ought to work. Any machine learning model is typically fed some raw data in the form of a vector or higher-order tensor, or perhaps a sequence of such tensors, as in language models. Let's use an example from language modeling, or *natural language processing* (NLP), because it is a bit easier to grasp than processing raw images. Let's consider the task of translating a simple sentence from English into Chinese.

| <b>English</b> | <b>Chinese</b> |
|----------------|----------------|
| I ate food.    | 我吃饭了.          |

Each word,  $w_i$ , in English is encoded as a fixed-length one-hot vector,  $w_i: \mathbb{B}^n$ , with dimensionality *n*. The dimensionality determines the maximal vocabulary size. For example, if  $n = 10$ , the model can only handle a vocabulary of 10 words in total, so usually it is much larger, such as  $n \approx 40000$ . Likewise, each word in Chinese is encoded as a fixed-length vector. We want to build a translation model that can translate each word of English into Chinese.

 The first approaches to this problem were based on recurrent neural networks, which are inherently sequential models, as they are capable of storing data from each input. A recurrent neural network, at a high level, is a function that maintains an internal state that is updated with each input that it sees (figure 10.6).

![](_page_7_Figure_6.jpeg)

![](_page_7_Figure_7.jpeg)

Most RNN language models work by first having an encoder model that consumes a single English word at a time, and once done gives its internal state vector to a different decoder RNN that outputs individual Chinese words one at a time. The problem with RNNs is that they are not easily parallelized because you must maintain an internal state, which depends on the sequence length (figure 10.7). If sequence lengths vary across inputs and outputs, you have to synchronize all the sequences until they're done processing.

 While many thought that language models needed recurrence to work well, given the natural sequential nature of language, researchers found that a relatively simple attention model with no recurrence at all could perform even better and is trivially parallelizable, making it easier to train faster and with more data. These are the socalled *transformer models*, which rely on self-attention. We will not get into their details we'll just sketch out the basic mechanism here.

![](_page_8_Figure_1.jpeg)

Figure 10.7 Schematic of an RNN language model. Two separate RNNs are used, an encoder and a decoder. The encoder takes an input sentence word by word and, once complete, sends its internal state to the decoder RNN, which produces each word in the target sentence until it halts.

The idea is that a Chinese word,  $c_i$  can be translated as a function of the weighted combination of a context of English words, *ei*. The context is simply a fixed-length collection of words that are in proximity to a given English word. Given the sentence "My dog Max chased a squirrel up the tree and barked at it," a context of three words for the word "squirrel" would be the subsentence "Max chased a squirrel up the tree" (i.e., we include the three words on either side of the target word).

 For the English phrase "I ate food" in figure 10.7, we would use all three words. The first Chinese word would be produced by taking a weighted sum of all the English words in the sentence:  $c_i = f(\sum a_i \cdot e_i)$ , where  $a_i$  is the (attention) weight, which is a number between 0 and 1 such that  $\Sigma a_i = 1$ . The function *f* would be a neural network, such as a simple feedforward neural network. The function as a whole would need to learn the neural network weights in  $f$  as well as the attention weights,  $a_i$ . The attention weights would be produced by some other neural network function.

 After successful training, we can inspect these attention weights and see which English words are attended to when translating to a given Chinese word. For example, when producing the Chinese word  $\ddagger \ddagger$ , the English word "I" would have a high attention weight associated with it, whereas the other words would be mostly ignored.

 This general procedure is called *kernel regression*. To take an even simpler example, let's say we have a data set that looks like figure 10.8, and we want to make a machine learning model that can take an unseen *x* and predict an appropriate *y*, given this training data. There are two broad classes of how to do this: *nonparametric* and *parametric* methods.

![](_page_9_Figure_1.jpeg)

Figure 10.8 Scatter plot of a nonlinear data set on which we might want to train a regression algorithm.

Neural networks are *parametric models* because they have a fixed set of adjustable parameters. A simple polynomial function like  $f(x) = ax^3 + bx^2 + c$  is a parametric model because we have three parameters  $(a,b,c)$  that we can train to fit this function to some data.

 A *nonparametric model* is a model that either has no trainable parameters or has the ability to dynamically adjust the number of parameters it has, based on the training data. Kernel regression is an example of a nonparametric model for prediction; the simplest version of kernel regression is to simply find the nearest  $x_i$  points in the training data, *X*, to some new input, *x*, and then return the corresponding  $y \in Y$  in the training data that is the average (figure 10.9).

 In this case, however, we have to choose how many points qualify as being the nearest neighbors to the input *x*, and it is problematic since all of these nearest neighbors contribute equally to the outcome. Ideally, we could weight (or attend to) all the points in the data set according to how similar they are to the input, and then take the weighted sum of their corresponding  $y_i$  to make a prediction. We'd need some function,  $f: X \to A$ : a function that takes an input  $x \in X$  and returns a set of attention weights  $a \in A$  that we could use to perform this weighted sum. This procedure is essentially exactly what we'll do in attention models, except that the difficulty lies in deciding how to efficiently compute the attention weights.

 In general, a *self-attention model* seeks to take a collection of objects and learn how each of those objects is related to the other objects via attention weights. In graph theory, a graph is a data structure,  $G = (N,E)$ , i.e., a collection of nodes, N, and edges (connections or relations) between nodes, *E*. The collection, *N*, might just be a set of
![](0__page_10_Figure_1.jpeg)

Figure 10.9 One way to perform nonparametric kernel regression to predict the *y* component of a new *x* value is to find the most similar (i.e., the closest) *x's* in the training data and then take the average of their respective *y* components.

node labels such as {0,1,2,3,...}, or each node might contain data, and thus each node might be represented by some feature vector. In the latter case, we can store our collection of nodes as a matrix  $N: \mathbb{R}^{n \times f}$ , where f is the feature dimension, such that each row is a feature vector for that node.

The collection of edges, *E*, can be represented by an *adjacency matrix*, *E*:  $\mathbb{R}^{n \times n}$ , where each row and column are nodes, such that a particular value in row 2, column 3 represents the strength of the relationship between node 2 and node 3 (right panel of figure 10.10). This is the very basic setup for a graph, but graphs can get more complicated where even the edges have feature vectors associated with them. We will not attempt that here.

![](0__page_10_Figure_5.jpeg)

Figure 10.10 The graph structure on the left can be represented quantitatively with a node feature matrix that encodes the individual node features and an adjacency matrix that encodes the edges (i.e., connections or arrows) between nodes. A 1 in the *a* row in the *b* column indicates that node *a* has an edge from *a* to *b*. The node features could be something like an RGBA value if the nodes represented pixels.

A self-attention model works by starting with a set of nodes,  $N: \mathbb{R}^{n \times f}$ , and then computes the attention weights between all pairs of nodes. In effect, it creates an edge matrix  $E: \mathbb{R}^{n \times n}$ . After creating the edge matrix, it will update the node features such that each node sort of gets blended together with the other nodes that it attends to. In a sense, each node sends a message to the other nodes to which it most strongly attends, and when nodes receive messages from other nodes, they update themselves. We call this one-step process a *relational module*, after which we get an updated node matrix, *N*: $\mathbb{R}^{n\times f}$ , that we can pass on to another relational module that will do the same thing (figure 10.11). By inspecting the edge matrix, we can see which nodes are attending to which other nodes, and it gives us an idea of the reasoning of the neural network.

![](0__page_11_Figure_2.jpeg)

Figure 10.11 A relational module, at the highest level, processes a node matrix,  $N: \mathbb{R}^{n \times f}$ , and outputs a new, updated node matrix,  $\hat{N}$ :  $\mathbb{R}^{n \times d}$ , where the dimensionality of the node feature may be different.

In a *self-attention language model*, each word from one language is attending to all the words in context of the other language, but the attention weights (or edges) represent to what degree each word is attending to (i.e., related to) each other word. Hence, a self-attention language model can reveal the meaning of a translated Chinese word with respect to the words in an English sentence. For example, the Chinese word 吃 means "eat," so this Chinese word would have a large attention weight to "eat" but would only weakly be attending to the other words.

 Self-attention makes more intuitive sense when used in language models, but in this book we've mostly dealt with machine learning models that operate on visual data, such as pixels from a video frame. Visual data, however, is not naturally structured as a collection of objects or nodes that we can directly pass into a relational module. We need a way of turning a bunch of pixels into a set of objects. One way to do it would be to simply call each individual pixel an object. To make things more computationally efficient, and to be able to process the image into more meaningful objects, we can first pass the raw image through a few convolutional layers that will return a tensor with dimensions (*C*,*H*,*W*) for channels, height, and width. In this way, we can define the objects in the convolved image as vectors across the channel dimension, i.e., each object is a vector of dimension *C*, and there will be  $N = H^*$  *W* number of objects (figure 10.12).

 After a raw image has been processed through a few trained CNN layers, we would expect that each position in the feature maps corresponds to particular salient features in the underlying image. For example, we hope the CNNs might learn to detect objects in the image that we can then pass into our relational module to process relations between objects. Each convolutional filter learns a particular feature for each spatial position, so taking all these learned features for a particular  $(x, y)$  grid position in an image yields a single vector for that position that encodes all the learned

![](0__page_12_Figure_1.jpeg)

**Convolutional filters**

![](0__page_12_Figure_3.jpeg)

features. We can do this for all the grid positions to collect a set of putative objects in the image, which we can represent as nodes in a graph, except that we do not know the connectivity between the nodes yet. That is what our relational reasoning module will attempt to do.

## *10.2.3 Self-attention models*

There are many possible ways to build a relational module, but as we've discussed, we will implement one based on a self-attention mechanism. We have described the idea at a high level, but it is time we got into the details of implementation. The model we'll build is based on the one described in the paper "Deep reinforcement learning with relational inductive biases" by Vinicius Zambaldi et al. (2019) from DeepMind.

We already discussed the basic framework of a node matrix  $N: \mathbb{R}^{n \times f}$  and an edge matrix  $E: \mathbb{R}^{n \times n}$ , and we discussed the need to process a raw image into a node matrix. Just like with kernel regression, we need some way of computing the distance (or inversely, the similarity) between two nodes. There is no single option for this, but one common approach is to simply take the *inner product* (also called *dot product*) between the two nodes' feature vectors as their similarity.

 The dot product between two equal-length vectors is computed by multiplying corresponding elements in each vector and then summing the result. For example, the inner product between vectors  $a = (1,-2,3)$  and  $b = (-1,5,-2)$  is denoted  $\langle a,b \rangle$  and is calculated as  $\langle a,b \rangle = \sum a_i b_i$ , which in this case is  $1 \cdot -1 + -2 \cdot 5 + 3 \cdot -2 = -1 - 10 - 6 = -17$ . The sign of each element in *a* and *b* are opposite, so the resulting inner product is a negative number indicating strong disagreement between the vectors. In contrast, if  $a = (1,-2,3)$ ,  $b = (2,-3,2)$  then  $\langle a,b \rangle = 14$ , which is a big positive number, since the two vectors are more similar element by element. Hence, the dot product gives us an easy

way to compute the similarity between a pair of vectors, such as nodes in our node matrix. This approach leads to what is called (scaled) *dot product attention*; the scaled part will come into play later.

 Once we have our initial set of nodes in the node matrix *N*, we will project this matrix into three new separate node matrices that are referred to as *keys, queries*, and *values*. With the kernel regression example, the query is the new *x* for which we want to predict the corresponding *y*, which is the value. The query is *x*, the *y* is the value. In order to find the value, we must locate the nearest  $x_i$  in the training data, which is the key. We measure the similarity between the query and the keys, find the keys that are most similar to the query, and then return the average value for that set of keys.

 This is exactly what we will do in self-attention, except that the queries, keys, and values will all come from the same origin. We multiply the original node matrix by three separate projection matrices to produce a query matrix, a key matrix, and a value matrix. The projection matrices will be learned during training just like any other parameters in the model. During training, the projection matrices will learn how to produce queries, keys, and values that will lead to optimal attention weights (figure 10.13).

 Let's take a single pair of nodes to make this concrete. Say we have a node (which is a feature vector),  $a:\mathbb{R}^{10}$ , and another node,  $b:\mathbb{R}^{10}$ . To calculate the self-attention of these two nodes, we first will project these nodes into a new space by multiplying by some projection matrices, i.e.,  $a_Q = a^TQ$ ,  $a_K = a^TK$ ,  $a_V = a^TV$ , where the superscript *T* 

![](0__page_13_Figure_5.jpeg)

Figure 10.13 A high-level view of a self-attention-based relational module. The input to a relational module is a node matrix *N*:Թ*<sup>n</sup>*×*<sup>f</sup>* with *n* nodes each with an *f*-dimensional feature vector. The relational module then copies this matrix for a total of three copies, and projects each one into a new matrix via a simple linear layer without an activation function, creating separate query, key, and value matrices. The query and key matrices are input to a compatibility function, which is any function that computes how compatible (similar in some way) each node is to each other node, resulting in a set of unnormalized attention weights,  $A: \mathbb{R}^{n \times n}$ . This matrix is then normalized via the softmax function across the rows, such that each row's values will sum to 1. The value matrix and normalized attention matrix are then multiplied,  $N = AV$ . The output of the relational module is then usually passed through one or more linear layers (not depicted).

indicates transposition, such that the node vector is now a column vector, e.g.,  $a^T$ :  $\mathbb{R}^{1\times10}$ , and the corresponding matrix is  $Q$ :  $\mathbb{R}^{10\times d}$ , such that  $a_Q = a^TQ$ :  $\mathbb{R}^d$ . We now have three new versions of *a* that may be of some different dimensionality from the input, e.g.,  $a_0, a_K, a_V$ :  $\mathbb{R}^{20}$ . We do the same for the node *b*. We can calculate how related *a* is to itself first by multiplying (via the inner product) its query and key together. Remember, we compute *all* pairwise interactions between nodes, including self-interactions. Unsurprisingly, objects are likely to be related to themselves, although not necessarily, since the corresponding queries and keys (after projection) may be different.

 After we multiply the query and key together for object *a*, we get an unnormalized attention weight,  $w_{a,a} = \langle a_0, a_K \rangle$ , which is a single scalar value for the self-attention between *a* and *a* (itself). We then do the same for the pairwise interaction between *a* and *b*, and *b* and *a*, and *b* and *b*, so we get a total of four attention weights. These could be arbitrarily small or large numbers, so we normalize all the attention weights using the softmax function, which as you may recall, takes a bunch of numbers (or a vector) and normalizes all the values to be in the interval  $[0,1]$  and forces them to sum to 1 so that they form a proper discrete probability distribution. This normalization forces the attention mechanism to only attend to what is absolutely necessary for the task. Without this normalization, the model could easily attend to everything, and it would remain un-interpretable.

 Once we have the normalized attention weights, we can collect them into an attention weight matrix. In our simple example with two objects, *a* and *b*, this would be a  $2 \times 2$  matrix. We can then multiply the attention matrix by each value vector, which will increase or decrease the elements in each vector value according to the attention weights. This will give us a set of new and updated node vectors. Each node has been updated based on the strength of its relationships to other nodes.

 Rather than multiplying individual vectors together one at a time, we can instead multiply entire node matrices together. Indeed, we can efficiently combine the three steps of key-query multiplication (to form an attention matrix), then attention-matrix with value-matrix multiplication, and finally normalization, into an efficient matrix multiplication,

$$
\hat{N} = softmax(QK^T) V
$$

where  $Q: \mathbb{R}^{n \times f}$ ,  $K^T: \mathbb{R}^{f \times n}$ ,  $V: \mathbb{R}^{n \times f}$ , where *n* is the number of nodes, *f* is the dimension of the node feature vector, *Q* is the query matrix, *K* is the key matrix, and *V* is the value matrix.

You can see that the result of  $QK<sup>T</sup>$  will be a  $n \times n$  dimensional matrix, which is an adjacency matrix as we described earlier, but in this context we call it the attention (weight) matrix. Each row and column represent a node. If the value in row 0 and column 1 is high, we know that node 0 attends strongly to node 1. The normalized attention (i.e., adjacency) weight matrix  $A = \text{softmax}(QK^T)$ :  $\mathbb{R}^{n \times n}$  tells us all the pairwise interactions between nodes. We then multiply this by the value matrix, which will update each node's feature vector according to its interactions with other nodes, such

that the final result is an updated node matrix, *N*ˆ:Թ*<sup>n</sup>*×*<sup>f</sup>* . We can then pass this updated node matrix through a linear layer to do additional learning over the node features and apply a nonlinearity to model more complex features. We call this whole procedure a *relational module* or *relational block*. We can stack these relational modules sequentially to learn higher order and more complex relations.

 In most cases, the final output of our neural network model needs to be a small vector, such as for Q values in DQN. After we've processed the input through 1 or more relational modules, we can reduce the matrix down to a vector by either doing a MaxPool operation or an AvgPool operation. For a node matrix *N*ˆ:Թ*<sup>n</sup>*×*<sup>f</sup>* , either of these pooling operations applied over the *n* dimension would result in a *f*-dimensional vector. MaxPool just takes the maximum value along the *n* dimension. We can then run this pooled vector through one or more linear layers before returning the final result as our Q values.

# *10.3 Implementing self-attention for MNIST*

Before we delve into the difficulties of reinforcement learning, let's try building a simple self-attention network to classify MNIST digits. The famous MNIST data set is 60,000 hand-drawn images of digits, where each image is  $28 \times 28$  pixels in grayscale. The images are labeled according to the digit that is depicted. The goal is to train a machine learning model to accurately classify the digits.

 This data set is very easy to learn, even with a simple one-layer neural network (a linear model). A multilayer CNN can achieve in the 99% accuracy range. While easy, it is a great data set to use as a "sanity check," just to make sure your algorithm can learn anything at all.

 We will first test out our self-attention model on MNIST, but we ultimately plan to use it as our deep Q-network in game playing, so the only difference between a DQN and an image classifier is that the dimensionality of the inputs and outputs will be different—everything in between can remain the same.

## *10.3.1 Transformed MNIST*

Before we build the model itself, we need to prepare the data and create some functions to preprocess the data so that it is in the right form for our model. For one, the raw MNIST images are grayscale pixel arrays with values from 0 to 255, so we need to normalize those values to be between 0 and 1, or the gradients during training will be too variable and training will be unstable. Because MNIST is so easy, we can also strain our model a bit more by adding noise and perturbing the images randomly (e.g., random translations and rotations). This will also allow us to assess translational and rotational invariance. These preprocessing functions are defined in the following listing.

#### Listing 10.1 Preprocessing functions

```
import numpy as np
from matplotlib import pyplot as plt
import torch
```

```
from torch import nn
              import torchvision as TV
              mnist data = TV.datasets.MNIST("MNIST/", train=True, transform=None,\
                                                         target transform=None, download=True) <
             mnist test = TV.datasets.MNIST("MNIST/", train=False, transform=None,\
                                                          target transform=None, download=True) \leftrightarrowAdds \begin{bmatrix} \rightarrow & \text{def} & \text{add} & \text{spots}(x, m=20, \text{std}=5, \text{val}=1) : \\ & & & & \end{bmatrix} testing data for validation
                   mask = torch.zeros(x.shape)
                  N = int(m + std * np.abs(np.random.randn())ids = np.random.random(np.prod(x.shape), size=N) mask.view(-1)[ids] = val
                   return torch.clamp(x + mask,0,1)
              def prepare images(xt,maxtrans=6,rot=5,noise=10):
                   out = torch.zeros(xt.shape)
                   for i in range(xt.shape[0]):
                        img = xt[i].unsqueeze(dim=0)
                       img = TV.transforms.functional.to pil image(img)
                      rand rot = np.random.randint(-1*rot,rot,1) if rot > 0 else 0
                      xtrans, ytrans = np.random.randnint(-maxtrans,maxtrans,2)img = TV.transforms.functional.affine(img, rand rot,
                    (xtrans,ytrans),1,0)
                        img = TV.transforms.functional.to_tensor(img).squeeze()
                        if noise > 0:
                            img = add_spots(img,m=noise)
                      maxval = img.view(-1) .max()if maxval > 0:
                           img = img.float() / maxval else:
                           img = img.float()out[i] = img return out
                                                                                  Downloads and loads the
                                                                                      MNIST training data
                                                                            Downloads and loads the MNIST
 random
 spots to
the image
                                                                               Preprocesses the images 
                                                                               and perform random 
                                                                               transformations of 
                                                                              rotation and translation
```

The add spots function takes an image and adds random noise to it. This function is used by the prepare images function, which normalizes the image pixels between 0 and 1 and performs random minor transformations such as adding noise, translating (shifting) the image, and rotating the image.

 Figure 10.14 shows an example of an original and perturbed MNIST digit. You can see that the image is translated up and to the right and has random dots sprinkled in. This makes the learning task more difficult because our model must learn translational, noise, and rotational invariant features in order to successfully classify. The prepare\_images function has parameters that let you tune how much the image will be perturbed, so you can control the difficulty of the problem.

## *10.3.2 The relational module*

Now we can dive into the relational neural network itself. Until now, all of the projects in this book were designed to be compelling enough to illustrate an important concept but simple enough to be able to run on a modern laptop without needing a GPU.

![](0__page_17_Picture_1.jpeg)

Figure 10.14 Left: Original MNIST digit for the number "5". Right: Transformed version that is translated to the top right and with random noise sprinkled in.

The computational demands of the self-attention module, however, are significantly greater than any of the other models we have built so far in the book. You can still try running this model on your laptop, but it will be significantly faster if you have a CUDA-enabled GPU. If you don't have a GPU, you can easily launch a cloud-based Jupyter Notebook using Amazon SageMaker, Google Cloud, or Google Colab (which is free as of this writing).

NOTE The code we show in this book will not include the necessary (but very minor) modifications necessary to run on a GPU. Please refer to this book's GitHub page at <http://mng.bz/JzKp>to see how to enable the code to run on a GPU, or consult the PyTorch documentation at [https://pytorch.org/docs/](https://pytorch.org/docs/stable/notes/cuda.html) [stable/notes/cuda.html](https://pytorch.org/docs/stable/notes/cuda.html).

In listing 10.2 we define a class that is the relational module. It is a single, but complex, neural network that includes an initial set of convolutional layers followed by the key, query, and value matrix multiplications.

```
class RelationalModule(torch.nn.Module):
                 def __ init (self):
                      super(RelationalModule, self).__init__()
                       self.ch_in = 1
                       self.conv1_ch = 16 
                       self.conv2_ch = 20
                       self.conv3_ch = 24
                       self.conv4_ch = 30
                      self.H = 28self.W = 28The dimension \longrightarrow self.node_size = 36
                       self.lin_hid = 100
                       self.out_dim = 10
                       self.sp_coord_dim = 2
                      self.N = int(16**2)self.conv1 = nn.Conv2d(self.ch_in,self.conv1 ch,kernel size=(4,4))
                       self.conv2 = nn.Conv2d(self.conv1_ch,self.conv2_ch,kernel_size=(4,4))
                Listing 10.2 Relational module
                                                     Defines the number 
                                                     of channels for each 
                                                     convolutional layer
                                                     self.H and self.W are the 
                                                     height and width of the 
                                                     The dimension input image, respectively.
 of the nodes
 after passing
  through the
    relational
      module
                                                     The number of objects or nodes, which 
                                                     is just the number of pixels after passing 
                                                     through the convolutions
```

```
 self.conv3 = nn.Conv2d(self.conv2_ch,self.conv3_ch,kernel_size=(4,4))
                      self.conv4 = nn.Conv2d(self.conv3_ch,self.conv4_ch,kernel_size=(4,4))

vector is the
                  \Rightarrow self.proj shape = (self.conv4 ch+self.sp coord dim,self.node size)
                     self.k proj = nn.Linear(*self.proj shape)
                      self.q_proj = nn.Linear(*self.proj_shape)
                     self.v proj = nn.Linear(*self.proj shape)

dimensions.
                     self.norm shape = (self.N,self.node size)
                 \Rightarrow self.k norm = nn.LayerNorm(self.norm shape, elementwise affine=True)
                      self.q_norm = nn.LayerNorm(self.norm_shape, elementwise_affine=True)
                     self.v norm = nn.LayerNorm(self.norm shape, elementwise affine=True)

learning
                      self.linear1 = nn.Linear(self.node_size, self.node_size)
                      self.norm1 = nn.LayerNorm([self.N,self.node_size], 
                  elementwise affine=False)
                     self.linear2 = nn.Linear(self.node size, self.out dim)
The dimensionality
    of each node
      number of
  channels in the
  last convolution
    plus 2 spatial
         Layer
  normalization
      improves
       stability.
```

The basic setup of our model is an initial block of four convolutional layers that we use to preprocess the raw pixel data into higher-level features. Our ideal relational model would be completely invariant to rotations and smooth deformations, and by including these convolutional layers that are only translation-invariant, our whole model is now less robust to rotations and deformations. However, the CNN layers are more computationally efficient than relational modules, so doing some preprocessing with CNNs usually works out well in practice.

 After the CNN layers, we have three linear projection layers that project a set of nodes into a higher-dimensional feature space. We also have some LayerNorm layers (discussed in more detail shortly), and a couple of linear layers at the end. Overall, it's not a complicated architecture, but the details are in the forward pass of the model.

```
def forward(self,x):
         N, Cin, H, W = x.shape
        x = self.count(x)x = torch.relu(x)
        x = self.comv2(x)x = x. squeeze()
        x = torch.relu(x)
        x = self.comv3(x)x = torch.relu(x)
        x = self.comv4(x)x = torch.relu(x)
        _{-'}<sub>-</sub>, CH, CW = x. shape
        xcoords = torch.arange(cW).repeat(cH,1).float() / cW
        ycoords = torch.arange(cH).repeat(cW,1).transpose(1,0).float() / cH
        spatial coords = torch.stack([xcoords,ycoords],dim=0)
        spatial coords = spatial coords.unsqueeze(dim=0)
        spatial coords = spatial coords.repeat(N,1,1,1)x = torch.cat([x, spatial coords], dim=1)
  Listing 10.3 The forward pass (continued from listing 10.2)
                                                 Appends the (x,y) coordinates of
                                                   each node to its feature vector
                                                    and normalizes to within the
                                                                interval [0, 1]
```

```
x = x. permute (0, 2, 3, 1)x = x. flatten(1, 2)K = self.k proj(x)Projects the input node 
K = self.k norm(K)matrix into key, query, 
                                and value matrices
Q = self.qproj(x)Q = self.q\_norm(Q)Batch matrix 
V = self.v proj(x)multiplies the query 
V = self.vnorm(V)and key matrices
A = torch.einsum('bfe, bqe->bfq', Q, K)
A = A / np.sqrt(self-node size) A = torch.nn.functional.softmax(A,dim=2) 
with torch.no qrad():
     self.att_map = A.clone()
E = torch.einsum('bfc, bcd->bfd', A, V)
                                            \leftarrowBatch matrix multiplies 
E = selfuinear1(E)
                                                 the attention weight 
E = torch.relu(E)
                                                 matrix and the value 
E = self.norm1(E)matrixE = E.max(dim=1)[0]
y = selfuinear2(E)
 y = torch.nn.functional.log_softmax(y,dim=1)
 return y
```

Let's see how this forward pass corresponds to the schematic back in figure 10.13. There are a few novelties used in this code that have not come up elsewhere in this book and that you may be unaware of. One is the use of the LayerNorm layer in PyTorch, which unsurprisingly stands for *layer normalization*.

LayerNorm is one form of neural network normalization; another popular one is called *batch normalization* (or just BatchNorm). The problem with unnormalized neural networks is that the magnitude of the inputs to each layer in the neural network can vary dramatically, and the range of values that the inputs can take can change from batch to batch. This increases the variability of the gradients during training and leads to instability, which can significantly slow training. Normalization seeks to keep all inputs at each major step of computation to within a relatively fixed, narrow range (i.e., with some constant mean and variance). This keeps gradients more stable and can make training much faster.

 As we have been discussing, self-attention (and the broader class of relational or graph) models are capable of feats that ordinary feedforward models struggle with due to their inductive bias of data being relational. Unfortunately, because the model involves a softmax in the middle, this can make training unstable and difficult as the softmax restricts outputs to within a very narrow range that can become saturated if the input is too big or small. Thus it is critical to include normalization layers to reduce these problems, and in our experiments LayerNorm improves training performance substantially, as expected.
## *10.3.3 Tensor contractions and Einstein notation*

The other novelty in this code is the use of the torch.einsum function. Einsum is short for *Einstein summation* (also called *Einstein notation*); it was introduced by Albert Einstein as a new notation for representing certain kinds of operations with tensors. While we could have written the same code without Einsum, it is much simpler with it, and we encourage its use when it offers improved code readability.

 To understand it, you must recall that tensors (in the machine learning sense, where they are just multidimensional arrays) may have 0 or more dimensions that are accessed by corresponding indices. Recall that a scalar (single number) is a 0-tensor, a vector is a 1-tensor, a matrix is a 2-tensor, and so on. The number corresponds to how many indices each tensor has. A vector has one index because each element in a vector can be addressed and accessed by a single nonnegative integer index value. A matrix element is accessed by two indices, its row and column positions. This generalizes to arbitrary dimensions.

 If you've made it this far, you're familiar with operations like the inner (dot) product between two vectors and matrix multiplication (either multiplying a matrix with a vector or another matrix). The generalization of these operations to arbitrary order tensors (e.g., the "multiplication" of two 3-tensors) is called a *tensor contraction*. Einstein notation makes it easy to represent and compute any arbitrary tensor contraction, and with self-attention, we're attempting to contract two 3-tensors (and later two 4-tensors) so it becomes necessary to use Einsum or we would have to reshape the 3 tensor into a matrix, do normal matrix multiplication, and then reshape it back into a 3-tensor (which is much less readable than just using Einsum).

This is the general formula for a tensor contraction of two matrices:

$$
C_{i,k} = \sum_j A_{i,j} B_{j,k}
$$

The output on the left,  $C_{i,k}$ , is the resulting matrix from multiplying matrices  $A: i \times j$ and  $B: j \times k$  (where  $i, j, k$  are the dimensions) such that dimension *j* for each matrix is the same size (which we know is required to do matrix multiplication). What this tells us is that element  $C_{0,0}$ , for example, is equal to  $\Sigma A_{0,i}B_{i0}$  for all *j*. The first element in the output matrix *C* is computed by taking each element in the first row of *A*, multiplying it by each element in the first column of *B*, and then summing these all together. We can figure out each element of *C* by this process of summing over a particular *shared index* between two tensors. This summation over a shared index is the process of tensor contraction, since we start with, for example, two input tensors with two indices each (for a total of four indices) and the output has two indices because two of the four get contracted away. If we did a tensor contraction over two 3-tensors, the result would be a 4-tensor.

 Einstein notation can also easily represent a batch matrix multiplication in which we have two collections of matrices and we want to multiply the first two matrices together, the second two together, etc., until we get a new collection of multiplied matrices.

#### Tensor contraction: example

Let's tackle a concrete example of a tensor contraction; we'll contract two matrices using Einstein notation.

$$
A = \begin{bmatrix} 1 & -2 & 4 \\ -5 & 9 & 3 \end{bmatrix}
$$
$$
B = \begin{bmatrix} -3 & -3 \\ 5 & 9 \\ 0 & 7 \end{bmatrix}
$$

Matrix A is a  $2 \times 3$  matrix and matrix B is  $3 \times 2$ . We will label the dimensions of these matrices using arbitrary characters. For example, we'll label matrix *A*:*i* × *j* with dimensions (indices) *i* and j, and matrix *B*:*j* × *k* with indices *j* and *k*. We could have labeled the indices using any characters, but we want to contract over the shared dimensions of  $A_j = B_j = 3$ , so we label them with the same characters.

$$
C = \begin{bmatrix} x_{0,0} & x_{0,1} \\ x_{1,0} & x_{1,1} \end{bmatrix}
$$

This *C* matrix represents the output. Our goal is to figure out the values of the *x* values, which are labeled by their indexed positions. Using the previous tensor contraction formula, we can figure out  $x<sub>0.0</sub>$  by finding row 0 of matrix *A* and column 0 of matrix *B*: $A_{0,j}$  = [1,–2,4] and  $B_{j,0}$  = [–3,5,0]<sup>T</sup>. Now we loop over the *j* index, multiplying each element of *A*0,*<sup>j</sup>* with *Bj*,0 and then summing them together to get a single number, which will be *x*<sub>0,0</sub> In this case, *x*<sub>0,0</sub> =  $ΣA$ <sub>0,*j*</sub> ⋅ *B*<sub>*j*,0</sub> =  $(1 ⋅ -3) + (-2 ⋅ 5) + (4 ⋅ 0) = -3 -$ 10 = –13. That was the calculation just for one element in the output matrix, element *C*<sub>0,0</sub>. We do this same process for all elements in *C* and we get all the values. Of course, we never do this by hand, but this is what is happening under the hood when we do a tensor contraction, and this process generalizes to tensors of higher order than just matrices.

Most of the time you will see Einstein notation written without the summation symbol, where it is assumed we sum over the shared index. That is, rather than explicitly writing  $C_{i,k}$  = Σ $A_{i,j}$  ⋅  $B_{j,k}$ , we often just write  $C_{i,k}$  =  $A_{i,j}B_{j,k}$  and omit the summation.

This is the Einsum equation for batch matrix multiplication,

$$
C_{b,i,k} = \sum_j A_{b,i,j} B_{b,j,k}
$$

where the *b* dimension is the batch dimension and we just contract over the shared *j* dimension. We will use Einsum notation to do batch matrix multiplication, but we can also use it to contract over multiple indices at once when using higher-order tensors than matrices.

In listing 10.3 we used  $A = \text{torch.einsum('bf, bge->bfg',Q,K)}$  to compute batched matrix multiplication of the *Q* and *K* matrices. Einsum accepts a string that contains

the instructions for which indices to contract over, and then the tensors that will be contracted. The string 'bfe,bge->bfg' associated with tensors *Q* and *K* means that *Q* is a tensor with three dimensions labeled, bfe, and *K* is a tensor with three dimensions labeled, bge, and that we want to contract these tensors to get an output tensor with three dimensions labeled, bfg. We can only contract over dimensions that are the same size and are labeled the same, so in this case we contract over the e dimension, which is the node feature dimension, leaving us with two copies of the node dimension, which is why the output is of dimension  $b \times n \times m$ . When using Einsum, we can label the dimensions of each tensor with any alphabetic characters, but we must make sure that the dimension we wish to contract over is labeled with the same character for both tensors.

 After the batch matrix multiplication, and we have the unnormalized adjacency matrix, we did  $A = A / np.sqrt(self node size)$  to rescale the matrix to reduce excessively large values and improve training performance; this is why we earlier referred to this is as *scaled* dot product attention.

 In order to get the *Q*, *K*, and *V* matrices, as we discussed earlier, we took the output of the last convolutional layer which is a tensor of dimensions batch  $\times$  channels  $\times$ height  $\times$  width, and we collapse the height and width dimensions into a single dimension of (height  $\times$  width = *n*) for the number of nodes, since each pixel position will become a potential node or object in the node matrix. Thus we get an initial node matrix of  $N: b \times c \times n$  that we reshape into  $N: b \times n \times c$ .

 By collapsing the spatial dimensions into a single dimension, the spatial arrangement of the nodes is scrambled and the network would struggle to discover that certain nodes (which were originally nearby pixels) are related spatially. That is why we add two extra channel dimensions that encode the  $(x, y)$  position of each node before it was collapsed. We normalize the positions to be in the interval [0, 1], since normalization almost always helps with performance.

 Adding these absolute spatial coordinates to the end of each node's feature vector helps maintain the spatial information, but it is not ideal since these coordinates are in reference to an external coordinate system, which means we're dampening some of the invariance to spatial transformations that a relational module should have, in theory. A more robust approach is to encode *relative* positions with respect to other nodes, which would maintain spatial invariance. However, this approach is more complicated, and we can still achieve good performance and interpretability with the absolute encoding.

 We then pass this initial node matrix through three different linear layers to project it into three different matrices with a potentially different channel dimension (which we will call *node-feature dimension* from this point), as shown in figure 10.15.

 Once we multiply the query and key matrices, we get an unnormalized attention weight matrix,  $A: b \times n \times n$ , where  $b =$  batch and  $n =$  the number of nodes. We then normalize it by applying softmax across the rows (dimension 1, counting from 0) such that each row sums to 1. This forces each node to only pay attention to a small number of other nodes, or to spread its attention very thinly across many nodes.

![](1__page_23_Figure_1.jpeg)

Then we multiply the attention matrix by the value matrix to get an updated node matrix, such that each node is now a weighted combination of all the other nodes. So if node 0 pays strong attention to nodes 5 and 9 but ignores the others, once we multiply the attention matrix with the value matrix, node 0 will be updated to be a weighted combination of nodes 5 and 9 (and itself, because nodes generally pay some attention to themselves). This general operation is termed *message passing* because each node sends a message (i.e., its own feature vector) to the nodes to which it is connected.

 Once we have our updated node matrix, we can reduce it down to a single vector by either averaging or max-pooling over the node dimension to get a single *d*-dimensional vector that should summarize the graph as a whole. We can pass that through a few ordinary linear layers before getting our final output, which is just a vector of Q values. Thus we are building a relational deep Q-network (Rel-DQN).

## *10.3.4 Training the relational module*

You might have noticed the last function call in the code is actually log softmax, which is not something we would use for Q-learning. But before we get to Q-learning, we will test our relational module on classifying MNIST digits and compare it to a conventional nonrelational convolutional neural network. Given that our relational module has the ability to model long-distance relationships in a way that a simple convolutional neural network cannot, we would expect our relational module to perform better in the face of strong transformations. Let's see how it does.

#### Listing 10.4 MNIST training loop

```
agent = RelationalModule() 
epochs = 1000batch_size=300
lr = 1e-3
opt = torch.optim.Adam(params=agent.parameters(),lr=lr)
lossfn = nn.NLLLoss()
for i in range(epochs):
     opt.zero_grad()
    batch ids = np.random.randint(0,60000,size=batch size)
     xt = mnist_data.train_data[batch_ids].detach()
                                      Creates an instance of 
                                     our relational module
                                                                        Randomly selects 
                                                                        a subset of the 
                                                                        MNIST images
```

![](1__page_24_Figure_1.jpeg)

This is a pretty straightforward training loop to train our MNIST classifier. We omitted the code necessary to store the losses for later visualization, but the unabridged code can be found in this book's GitHub repository. We told the prepare\_images function to randomly rotate the images by up to 30 degrees in either direction, which is a significant amount.

 Figure 10.16 shows how the relational module performed after 1,000 epochs (which is not long enough to reach maximum accuracy). The plots look good, but this is just performance on the training data.

![](1__page_24_Figure_4.jpeg)

Figure 10.16 The loss and accuracy over training epochs for the relational module on classifying MNIST digits

To really know how well it performs, we need to run the model on the test data, which is a separate set of data that the model has never seen before. We'll run it on 500 examples from the test data to calculate its accuracy.

```
def test_acc(model,batch_size=500):
   acc = 0.
   batch ids = np.random.randint(0,10000,size=batch size)
    xt = mnist_test.test_data[batch_ids].detach()
   xt = prepare images(xt,maxtrans=6,rot=30,noise=10) .unsqueeze(dim=1)Listing 10.5 MNIST test accuracy
```

```
 yt = mnist_test.test_labels[batch_ids].detach()
    preds = model(xt) pred_ind = torch.argmax(preds.detach(),dim=1)
    acc = (pred ind == yt).sum() .float() / batch size return acc, xt, yt
acc2, xt2, yt2 = test_acc(agent)
print(acc2)
>>> 0.9460
```

We get nearly  $95\%$  accuracy at test time with the relational module after just 1,000 epochs of testing. Again, 1,000 epochs with a batch size of 300 is not enough to reach maximal accuracy. Maximal accuracy with any decent neural network on (unperturbed) MNIST should be around the 98–99% mark. But we're not going for maximum accuracy here; we're just making sure it works and that it performs better than a convolutional neural network with a similar number of parameters.

 We used the following simple CNN as a baseline, which has 88,252 trainable parameters compared to the relational module's 85,228. The CNN actually has about 3,000 more parameters than our relational module, so it has a bit of an advantage.

![](1__page_25_Figure_4.jpeg)

Instantiate this CNN and swap it in for the relational module in the previous training loop to see how it compares. We get a test accuracy of only 87.80% with this CNN, demonstrating that our relational module is outperforming a CNN architecture, controlling for the number of parameters. Moreover, if you crank up the transformation level (e.g., add more noise, rotate even more), the relational module will maintain a higher accuracy than the CNN. As we noted earlier, our particular implementation of the relational module is not practically invariant to rotations and deformations because, in part, we've added the absolute coordinate positions; it's not all relational, but it has the ability to compute long-distance relations between features in the image, as opposed to a CNN that can just compute local features.

 We wanted to introduce relational modules not merely because they might get better accuracy on some data set, but because they are more interpretable than traditional neural network models. We can inspect the learned relationships in the attention weight matrix to see which parts of the input the relational module is using to classify images or predict Q values as shown in figure 10.17.

![](1__page_26_Picture_3.jpeg)

Figure 10.17 Left column: Original input MNIST images (after transformation). Right column: Corresponding self-attention weights showing where the model is paying the most attention.

We visualize this attention map by just reshaping the attention map into a square image:

>>> plt.imshow(agent.att\_map[0].max(dim=0)[0].view(16,16))

The attention weight matrix is a *batch*  $\times n \times n$  matrix where *n* is the number of nodes, which is  $16^2$  =  $256$  in our example, since after the convolutional layers the spatial extent

is reduced from the original  $28 \times 28$ . Notice in the top two examples of figure 10.17 that attention maps highlight the contour of the digit but with more intensity at certain parts. If you look through a number of these attention maps, you'll notice that the model tends to pay most attention to the inflection and crossover points of the digit. For the digit 8, it can successfully classify this image as the number 8 just by paying attention to the center of the 8 and the bottom part. You can also notice that in none of the examples is attention given to the added spots of noise in the input; attention is only given to the real digit part of the image, demonstrating that the model is learning to separate the signal from the noise to a large degree.

# *10.4 Multi-head attention and relational DQN*

We've demonstrated that our relational model performs well on the simple task of classifying MNIST digits and furthermore that by visualizing the learned attention maps we can get a sense of what data the model is using to make its decisions. If the trained model keeps misclassifying a particular image, we can inspect its attention map and see if perhaps it is getting distracted by some noise.

 One problem with the self-attention mechanism we've employed so far is that it severely constrains the amount of data that can be transmitted due to the softmax. If the input had hundreds or thousands of nodes, the model would only be able to put attention weight on a very small subset of those, and it may not be enough. We want to be able to bias the model toward learning relationships, which the softmax helps promote, but we don't want to necessarily limit the amount of data that can pass through the self-attention layer.

 In effect, we need a way to increase the bandwidth of the self-attention layer without fundamentally altering its behavior. To address this issue, we'll allow our model to have multiple attention *heads*, meaning that the model learns multiple attention maps that operate independently and are later combined (figure 10.18). One attention head

![](1__page_27_Figure_6.jpeg)

Figure 10.18 Multi-head dot product attention (MHDPA). Rather than use a single attention matrix, we can have multiple attention matrices called *heads* that can independently attend to different aspects of an input. The only difference is adding a new head dimension to the query, key and value tensors.

might focus on a particular region or features of the input, whereas another head would focus elsewhere. This way we can increase the bandwidth through the attention layer but we can still keep the interpretability and relational learning intact. In fact, multi-head attention can improve interpretability because within each attention head, each node can more strongly focus on a smaller subset of other nodes rather than having to spread its attention more thinly. Thus, multi-head attention can give us a better idea of which nodes are strongly related.

 With multi-head attention, the utility of Einsum becomes even more obvious as we will be operating on 4-tensors of dimension *batch* × *head* × *number of nodes* × *features*. Multi-head attention will not be particularly useful for MNIST because the input space is already small and sparse enough that a single attention head has enough bandwidth and interpretability. Hence, this is a good time to introduce our reinforcement learning task for this chapter. Because the relational module is the most computationally expensive model we've implemented in this book so far, we want to use a simple environment that still demonstrates the power of relational reasoning and interpretability in reinforcement learning.

 We will be coming full circle and returning to a Gridworld environment that we first encountered in chapter 3. But the Gridworld environment we will be using in this chapter is much more sophisticated. We'll be using the MiniGrid library found on GitHub at <https://github.com/maximecb/gym-minigrid>; it is implemented as an OpenAI Gym environment. It includes a wide variety of different kinds of Gridworld environments of varying complexity and difficulty. Some of these Gridworld environments are so difficult (largely due to sparse rewards) that only the most cutting-edge reinforcement learning algorithms are capable of making headway. Install the package using pip:

>>> pip3 install gym-minigrid

We will be using a somewhat difficult environment in which the Gridworld agent must navigate to a key, pick it up, use it to open a door, and then navigate to a goalpost in order to receive a positive reward (figure 10.19). This is a lot of steps before it ever sees a reward, so we will encounter the sparse reward problem. This would actually be a great opportunity to employ curiosity-based learning, but we will restrict ourselves to the smallest version of the grid, the MiniGrid, so that even a random agent would eventually find the goal, so we can successfully train without curiosity. For the larger grid variants of this environment, curiosity or related approaches would be almost necessary.

 There are a few other complexities to the MiniGrid set of environments. One is that they are partially observable environments, meaning the agent cannot see the whole grid but only a small region immediately surrounding it. Another is that the agent does not simply move left, right, up, and down but has an orientation. The agent can only move forward, turn left, or turn right; it is always oriented in a particular direction and must turn around before moving backward, for example. The agent's

![](1__page_29_Figure_1.jpeg)

![](1__page_29_Figure_2.jpeg)

partial view of the environment is *egocentric*, meaning the agent sees the grid as if it were facing it. When the agent changes direction without moving position, its view changes. The state we receive from the environment is a  $7 \times 7 \times 3$  tensor, so the agent only sees a  $7 \times 7$  subregion of the grid in front of it; the last (channel) dimension of the state encodes which object (if any) is present at that position.

 This Gridworld environment is a good testbed for our relational module because in order to successfully learn how to play, the agent must learn how to relate the key to the lock and the lock to being able to access the goal, which is all a form of relational reasoning. In addition, the game is naturally represented by a set of objects (or nodes), since each "pixel" position in the grid really is an actual object, unlike in the MNIST example. This means we can see exactly which objects the agent is paying attention to. We might hope it learns to pay most attention to the key, door, and goal square, and that the key is related to the door. If this turns out to be the case, it suggests the agent is learning not too differently than how a human would learn how to relate the objects on the grid.

 Overall we will repurpose the relational module we created earlier for the MNIST example as a relational DQN, so we really only need to change the output to a normal activation function rather than the log\_softmax we used for classification. But first, let's get back to implementing multi-head attention. As operating on higherorder tensors gets more complicated, we will get help from a package called Einops that extends the capabilities of PyTorch's built-in Einsum function. You can install it using pip:

>>> pip install einops >>> from einops import rearrange

There are only two important functions in this package (rearrange and reduce), and we will only use one, the rearrange function. rearrange basically lets us reshape the
dimensions of a higher-order tensor more easily and readably than the built-in PyTorch functions, and it has a syntax similar to Einsum. For example, we can reorder the dimensions of a tensor like this:

```
>> x = torch.randn(5,7,7,3)
>>> rearrange(x, "batch h w c -> batch c h w").shape
torch.Size([5, 3, 7, 7])
```

Or if we had collapsed the spatial dimensions *h* and *w* into a single dimension *N* for nodes, we can undo this:

```
\Rightarrow x = torch.randn(5,49,3)
>>> rearrange(x, "batch (h w) c -> batch h w c", h=7).shape
torch.Size([5, 7, 7, 3])
```

In this case, we tell it that the input has three dimensions but the second dimension is secretly two dimensions  $(h, w)$  that were collapsed, and we want to extract them out into separate dimensions again. We only need to tell it the size of *h* or *w*, and it can infer the size of the other dimension.

 The main change for multi-head attention is that when we project the initial node matrix *N*:  $\mathbb{R}^{b \times n \times f}$  into key, query, and value matrices, we add an extra head dimension:  $Q$ ,*K*,*V*:  $\mathbb{R}^{b \times h \times n \times d}$ , where *b* is the batch dimension, and *h* is the head dimension. We will (arbitrarily) set the number of heads to be 3 for this example, so  $h = 3$ ,  $n = 7 * 7 = 49$ ,  $d = 64$ , where *n* is the number of nodes (which is just the total number of grid positions in view), and *d* is the dimensionality of the node feature vectors, which is just something we choose empirically to be 64, but smaller or larger values might work just as well.

 We will need to do a tensor contraction between the query and key tensors to get an attention tensor,  $A: \mathbb{R}^{b \times h \times n \times n}$ , pass it through a softmax, contract this with the value tensor, collapse the head dimension with the last *n* dimension, and contract the last (collapsed) dimension with a linear layer to get our updated node tensor,  $N: \mathbb{R}^{b \times n \times d}$ , which we can then pass through another self-attention layer or collapse all the nodes into a single vector and pass it through some linear layers to the final output. We will stick with a single-attention layer for all examples.

 First we'll go over some specific lines in the code that are different from the singlehead attention model; the full model is reproduced in listing 10.7. In order to use PyTorch's built-in linear layer module (which is just a matrix multiplication plus a bias vector), we will create a linear layer where the last dimension size is expanded by the number of attention heads.

```
>>> self.proj_shape = (self.conv4_ch+self.sp_coord_dim,self.n_heads * 
    self.node_size)
>>> self.k proj = nn.Linear(*self.proj shape)
>>> self.q_proj = nn.Linear(*self.proj_shape)
>>> self.v proj = nn.Linear(*self.proj shape)
```

We make three separate, ordinary linear layers just as we did for the single-head attention model, but this time we'll expand the last dimension by multiplying it by the number of attention heads. The input to these projection layers is a batch of initial node matrices,  $N: \mathbb{R}^{b \times n \times c}$ , and the *c* dimension is equal to the output channel dimension of the last convolutional layer plus the two spatial coordinates that we append. The linear layer thus contracts over the channel dimension to give us query, key, and value matrices, Q,*K*,*V*:ℝ<sup>|</sup>∞™(<sup>h،d</sup>), so we will use the Einops rearrange function to expand out the last dimension into head and *d* dimensions.

```
>>> K = rearrange(self.k proj(x), "b n (head d) -> b head n d",
    head=self.n_heads)
```

We will extract out the separate head and *d* dimension and simultaneously reorder the dimensions so that the head dimension comes after the batch dimension. Without Einops, this would be more code and not nearly as readable.

 For this example, we will also abandon the dot (inner) product as the compatibility function (recall, this is the function that determines the similarity between the query and keys) and instead use something called *additive attention* (figure 10.20). The dot product attention would work fine, but we wanted to illustrate that it is not the only kind of compatibility function, and the additive function is actually a bit more stable and expressive.

![](2__page_31_Figure_5.jpeg)

Figure 10.20 The compatibility function computes the similarity between each key and query vector, resulting in an adjacency matrix.

With dot product attention, we compute the compatibility (i.e., the similarity) between each query and key by simply taking the dot product between each vector. When the two vectors are similar element-wise, the dot product will yield a large positive value, and when they are dissimilar, it may yield a value near zero or a big negative value. This means the output of the (dot product) compatibility function is unbounded in both directions, and we can get arbitrarily large or small values. This can be problematic when we then pass it through the softmax function, which can easily saturate. By *saturate* we mean that when a particular value in an input vector is dramatically larger than other values in the vector, the softmax may assign all its probability mass to that single value, setting all the others to zero, or vice versa. This can make our gradients too large or too small for particular values and destabilize training.

 Additive attention can solve this problem at the expense of introducing additional parameters. Instead of simply multiplying the *Q* and *K* tensors together, we'll instead pass them both through independent linear layers, add them together, and then apply an activation function, followed by another linear layer (figure 10.21). This allows for a more complex interaction between *Q* and *K* without as much risk of

## **Additive attention**

![](2__page_32_Figure_2.jpeg)

Figure 10.21 Additive attention is an alternative to dot product attention that can be more stable. Instead of multiplying the queries and keys together, we first pass them independently through linear layers and then add them together, apply a nonlinear function, and pass through another linear layer to change the dimensionality.

causing numerical instability, since addition will not exaggerate numerical differences like multiplication does. First we need to add three new linear layers for the additive attention.

```
>>> self.k lin = nn.Linear(self.node size, self.N)
>>> self.q lin = nn.Linear(self.node size, self.N)
>>> self.a_lin = nn.Linear(self.N, self.N)
```

In the forward method we define the actual computation steps for additive attention:

```
>>> A = torch.nn.functional.elu(self.q lin(Q) + self.k lin(K))
\Rightarrow > A = self.a lin(A)
>>> A = torch.nn.functional.softmax(A, dim=3)
```

As you can see, we pass *Q* through a linear layer and *K* through its own linear layer, add them together, and then apply a nonlinear activation function. Then we pass this result through another linear layer and lastly apply the softmax across the node rows, which finally yields the attention weight tensor.

 Now we do the same as before and contract the attention tensor with the *V* tensor along the last *n* dimension to get a tensor with dimensions  $b \times h \times n \times d$ , which is a multi-headed node matrix.

```
>>> E = torch.einsum('bhfc,bhcd->bhfd',A,V)
```

What we want at the end of the self-attention module is an updated node matrix with dimensions  $b \times n \times d$ , so we will concatenate or collapse the head dimension and *d* dimension, and then pass this through a linear layer to reduce the dimensionality back down to size *d*.

```
\Rightarrow \ge \le = rearrange(E, 'b head n d -> b n (head d)')
>>> E = selfuinear1(E)
>>> E = torch.relu(E)
>> E = self.norm1(E)
```

The final shape of this is now  $b \times n \times d$ , which is exactly what we want. Since we're only going to use a single self-attention module, we want to reduce this 3-tensor into a 2 tensor of just a batch of vectors, so we will maxpool over the *n* dimension, and then pass the result through a final linear layer, which represents the Q values.

```
>>> E = E.max(dim=1)[0]
\Rightarrow y = \text{selfu. linear2(E)
>>> y = torch.nn.functional.elu(y)
```

That's it. We just went through all the core lines of code, but let's see it all together and test it out.

```
Listing 10.7 Multi-head relational module
class MultiHeadRelationalModule(torch.nn.Module):
    def __ init (self):
        super(MultiHeadRelationalModule, self). init ()
         self.conv1_ch = 16 
         self.conv2_ch = 20
         self.conv3_ch = 24
         self.conv4_ch = 30
        self.H = 28self.W = 28 self.node_size = 64
         self.lin_hid = 100
         self.out_dim = 5
         self.ch_in = 3
         self.sp_coord_dim = 2
        self.N = int(7**2)We use 1 x 1 convolutions to
         self.n_heads = 3
                                                     preserve the spatial organization
                                                           of the objects in the grid.
         self.conv1 = 
     nn.Conv2d(self.ch_in,self.conv1_ch,kernel_size=(1,1),padding=0)
                                                                              \epsilon self.conv2 = 
     nn.Conv2d(self.conv1_ch,self.conv2_ch,kernel_size=(1,1),padding=0)
        self.proj shape = (self.conv2 ch+self.sp coord dim,self.n heads *
     self.node_size)
        self.k proj = nn.Linear(*self.proj shape)
        self.q proj = nn.Linear(*self.proj shape)
                                                                    Sets up linear 
        self.v proj = nn.Linear(*self.proj shape)
                                                                    layers for additive 
                                                                    attentionself.k lin = nn.Linear(self.node size, self.N)
         self.q_lin = nn.Linear(self.node_size,self.N)
        self.a lin = nn.Linear(self.N,self.N)
        self.node shape = (self.n heads, self.N,self.node size)
        self.k norm = nn.LayerNorm(self.node shape, elementwise affine=True)
        self.q norm = nn.LayerNorm(self.node shape, elementwise affine=True)
        self.v norm = nn.LayerNorm(self.node shape, elementwise affine=True)
        self.linear1 = nn.Linear(self.n heads * self.node size, self.node size)
         self.norm1 = nn.LayerNorm([self.N,self.node_size],
             elementwise_affine=False)
        self.linear2 = nn.Linear(self.node size, self.out dim)
```

```
 def forward(self,x):
                N, Cin, H, W = x.shape
                x = self.count(x)x = torch.relu(x)
                x = self.comv2(x)x = torch.relu(x)
                with torch.no qrad():
                     self.conv_map = x.clone() 
                _{\text{--}}, _{\text{CH}}, _{\text{CW}} = x.shape
                 xcoords = torch.arange(cW).repeat(cH,1).float() / cW
                ycoords = torch.arange(cH).repeat(cW,1).transpose(1,0).float() / cH
                spatial coords = torch.stack([xcoords,ycoords],dim=0)
                 spatial_coords = spatial_coords.unsqueeze(dim=0)
                 spatial_coords = spatial_coords.repeat(N,1,1,1)
                x = torch.cat([x, spatial coords], dim=1)
                x = x.\text{permute}(0, 2, 3, 1)x = x. flatten(1, 2)K = rearrange(self.k proj(x), "b n (head d) -> b head n d",
                     head=self.n_heads)
                K = self.k norm(K)Q = rearrange(self.q proj(x), "b n (head d) -> b head n d",
                     head=self.n_heads)
                Q = self.qnorm(Q)V = rearrange(self.v proj(x), "b n (head d) -> b head n d",
                     head=self.n_heads)
                 V = self.v_norm(V) 
                A = torch.nn.functional.elu(self.q lin(Q) + self.k lin(K))
                A = self.a lin(A) A = torch.nn.functional.softmax(A,dim=3) 
                with torch.no qrad():
                 self.att map = A.clone()
               E = torch.einsum('bhfc,bhcd->bhfd',A,V)
                E = rearrange(E, 'b head n d -> b n (head d)')
                E = selfuinear1(E)
                E = torch.relu(E)
                E = self.norm1(E)E = E.max(dim=1)[0]
                y = selfuinear2(E)
                 y = torch.nn.functional.elu(y)
                 return y
                                                         Saves a copy of the 
                                                         post-convolved input 
                                                         for later visualization
 Additive
attention
    Saves a
 copy of the
  attention
    weights
   for later
visualization
                                                                       Batch-matrix multiplies the 
                                                                       attention weight matrix with 
                                                                       the node matrix to get an 
                                                                       updated node matrix.
                                                                             Collapses the head 
                                                                             dimension with the 
                                                                             feature d dimension
```

## *10.5 Double Q-learning*

Now let's get to training it. Because this Gridworld environment has sparse rewards, we need to make our training process as smooth as possible, especially since we're not using curiosity-based learning.

 Remember back in chapter 3 when we introduced Q-learning and a target network to stabilize training? If not, the idea was that in ordinary Q-learning we compute the target Q value with this equation:

$$
Q_{new} = r_t + \gamma \cdot \max(Q(s_{t+1}))
$$

The problem with this is that every time we update our DQN according to this equation so that its predictions get closer to this target, the  $Q(s_{t+1})$  is changed, which means the next time we go to update our Q function, the target  $Q_{new}$  is going to be different even for the same state. This is problematic because as we train the DQN, its predictions are chasing a moving target, leading to very unstable training and poor performance. To stabilize training, we create a duplicate Q function called the *target function* that we can denote  $Q'$ , and we use the value  $Q'(s_{t+1})$  to plug into the equation and update the main Q function.

$$
Q_{new} = r_t + \gamma \cdot \max(Q'(s_{t+1}))
$$

We only train (and hence backpropagate into) the main Q function, but we copy the parameters from the main Q function to the target Q function, *Q*′, every 100 (or some other arbitrary number of) epochs. This greatly stabilizes training because the main Q function is no longer chasing a constantly moving target, but a relatively fixed target.

 But that's not all that's wrong with that simple update equation. Because it involves the max function, i.e., we select the maximum predicted Q value for the next state, it leads our agent to overestimate Q values for actions, which can impact training especially early on. If the DQN takes action 1 and learns an erroneously high Q value for action 1, that means action 1 is going to get selected more often in subsequent epochs, further causing it to be overestimated, which again leads to training instability and poor performance.

 To mitigate this problem and get more accurate estimates for Q values, we will implement double Q-learning, which solves the problem by disentangling actionvalue estimation from action selection, as you will see. A *double deep Q-network* (DDQN) involves a simple modification to normal Q-learning with a target network. As usual, we use the main Q-network to select actions using an epsilon-greedy policy. But when it comes time to compute  $Q_{\text{new}}$ , we will first find the argmax of Q (the main Q-network). Let's say argmax $(Q(s_{t+1})) = 2$ , so action 2 is associated with the highest action value in the next state given the main Q function. We then use this to index into the target network, *Q*′, to get the action value we will use in the update equation.

$$
a = \operatorname{argmax}(Q(s_{t+1}))
$$
$$
x = Q'(s_{t+1})[a]
$$
$$
Q_{new} = r_t + \gamma \cdot x
$$

We're still using the Q value from the target network, *Q*′, but we don't choose the highest Q value from *Q*′; we choose the Q value in *Q*′ based on the action associated with the highest Q value in the main Q function. In code:

```
>>> state batch, action batch, reward batch, state2 batch, done batch =
     get minibatch(replay, batch size)
>>> q_pred = GWagent(state_batch)
```

```
>>> astar = torch.argmax(q_pred,dim=1)
>>> qs = Tnet(state2_batch).gather(dim=1,index=astar.unsqueeze(dim=1)).squeeze()
>>> targets = 
     get qtarget ddqn(qs.detach(),reward batch.detach(),gamma,done batch)
```

The get\_qtarget\_ddqn function just computes  $Q_{new} = r_t + \gamma \cdot x$ :

```
>>> def get qtarget ddqn(qvals,r,df,done):
>>> targets = r + (1-done) * df * qvals
>>> return targets
```

We provide done, which is a Boolean, because if the episode of the game is done, there is no next state on which to compute  $Q(s_{t+1})$ , so we just train on  $r_t$  and set the rest of the equation to 0.

 That's all there is to double Q-learning; just another simple way to improve training stability and performance.

## *10.6 Training and attention visualization*

We have most of the pieces now, but we need a few other helper functions before training.

```
import gym
from gym minigrid.minigrid import *
from gym minigrid.wrappers import FullyObsWrapper, ImgObsWrapper
from skimage.transform import resize
def prepare_state(x): 
    ns = torch.from number(x).float() .permute(2,0,1).unsqueeze(dim=0) #maxv = ns.floatten() max() ns = ns / maxv
     return ns
def get minibatch(replay, size):
    batch ids = np.random.random(0, len(replay), size)batch = [reply[x] for x in batch ids] #list of tuples
    state batch = torch.cat([s for (s,a,r,s2,d) in batch],)
    action batch = torch.Tensor([a \text{ for } (s,a,r,s2,d) \text{ in batch}]).long()
    reward batch = torch.Tensor([r \text{ for } (s,a,r,s2,d) \text{ in batch}]\)state2 batch = torch.cat([s2 for (s, a, r, s2, d) in batch], dim=0)
    done batch = torch.Tensor([d for (s,a,r,s2,d) in batch])
    return state batch, action batch, reward batch, state2 batch, done batch
def get qtarget ddqn(qvals,r,df,done):
    targets = r + (1-done) * df * qvals
     return targets
  Listing 10.8 Preprocessing functions
                                              Normalizes the state tensor 
                                             and converts to PyTorch tensor
                                              Gets a random mini-batch 
                                              from the experience replay 
                                              memory
                                                     Calculates the 
                                                     target Q value
```

These functions just prepare the state observation tensor, produce a mini-batch and calculate the target Q value as we discussed earlier.

 In listing 10.9 we define the loss function we will use and also a function to update the experience replay.

```
def lossfn(pred,targets,actions):
    loss = touchmean(torch.pow() targets.detach() -\
     pred.qather(dim=1,index=actions.unsquaree(dim=1)). squaree(() \ ,2),dim=0)
     return loss
def update replay(replay, exp, replay size):
 r = \exp[2]N = 1 if r > 0:
     N = 50 for i in range(N):
       replay.append(exp)
   return replay
action map = \{0:0, 1:1,
    2:2,
     3:3,
     4:5,
}
   Listing 10.9 Loss function and updating the replay
                                             Loss function
                                                         Adds new experiences 
                                                         to the experience replay 
                                                         memory; if the reward 
                                                         is positive, we add 50 
                                                         copies of the memory.
                        Maps the action 
                         outputs of the 
                         DQN to a subset 
                        of actions in the 
                        environment
```

The update replay function adds new memories to the experience replay if it is not yet full; if it is full, it will replace random memories with new ones. If the memory resulted in a positive reward, we add 50 copies of that memory, since positive reward memories are rare and we want to enrich the experience replay with these more important memories.

 All the MiniGrid environments have seven actions, but in the environment we will use in this chapter, we only need to use five of the seven actions, so we use a dictionary to translate from the output of DQN, which will produce actions 0–4, to the appropriate actions in the environment, which are {0,1,2,3,5}.

The MiniGrid's action names and corresponding action numbers are listed here:

```
 [<Actions.left: 0>,
 <Actions.right: 1>,
 <Actions.forward: 2>,
 <Actions.pickup: 3>,
 <Actions.drop: 4>,
 <Actions.toggle: 5>,
 <Actions.done: 6>]
```

In listing 10.10 we jump into the main training loop of the algorithm.

![](2__page_38_Figure_1.jpeg)

```
if i % update freq == 0:
     Tnet.load_state_dict(GWagent.state_dict())
                                                             Synchronizes the main 
                                                             DQN with the target 
                                                             DQN every 100 steps
```

Our self-attention double DQN reinforcement learning algorithm will learn how to play fairly well after about 10,000 epochs, but it may take up to 50,000 epochs before it reaches maximum accuracy.

 Figure 10.22 shows the log-loss plot we get, and we also plotted the average episode length. As the agent learns to play, it should be able to solve the games in fewer and fewer steps.

If you test the trained algorithm, it should be able to solve  $\geq 94\%$  of the episodes within the maximum step limit. We even recorded video frames during training, and the agent clearly knows what it is doing when you watch it in real time. We have omitted a lot of this accessory code to keep the text clear; please see the GitHub repository for the complete code.

![](2__page_39_Figure_5.jpeg)

![](2__page_39_Figure_6.jpeg)

Figure 10.22 Top: Log-loss plot during training. The loss drops quickly in the beginning, increases a bit, and then very slowly begins decreasing again. Bottom: Average episode length. This gives us a better idea of the performance of the agent since we can clearly see it is solving the episodes in a shorter number of steps during training.
## *10.6.1 Maximum entropy learning*

We are using an epsilon-greedy policy with epsilon set to 0.5, so the agent is taking random actions 50% of the time. We tested using a number of different epsilon levels but found 0.5 to be about the best. If you train the agent with epsilon values ranging from a low of 0.01, to 0.1, to 0.2, all the way to a high of say 0.95, you will notice the training performance follows an inverted-U curve, where too low a value for epsilon leads to poor learning due to lack of exploration, and too high a value for epsilon leads to poor learning due to lack of exploitation.

 How can the agent perform so well even though it is acting randomly half the time? By setting the epsilon to be as high as possible until it degrades performance, we are utilizing an approximation to the principle of maximum entropy, or *maximum entropy learning*.

 We can think of the entropy of an agent's policy as the amount of randomness it exhibits, and it turns out that maximizing entropy up until it starts to be counterproductive actually leads to better performance and generalization. If an agent can successfully achieve a goal even in the face of taking a high proportion of random actions, it must have a very robust policy that is insensitive to random transformations, so it will be able to handle more difficult environments.

## *10.6.2 Curriculum learning*

We trained this agent only on the  $5 \times 5$  version of this Gridworld environment so that it would have a small chance of randomly achieving the goal and receiving a reward. There are also bigger environments, including a  $16 \times 16$  environment, which would make randomly winning extremely unlikely. An alternative to (or addition to) curiosity learning is to use a process called *curriculum learning*, which is when we train an agent on an easy variant of a problem, then retrain on a slightly harder variant, and keep retraining on harder and harder versions of the problem until the agent can successfully achieve a task that would have been too hard to start with. We could attempt to solve the  $16 \times 16$  grid without curiosity by first training to maximum accuracy on the  $5 \times 5$  grid, then retraining on the  $6 \times 6$  grid, then the  $8 \times 8$  grid, and finally the  $16 \times 16$  grid.

## *10.6.3 Visualizing attention weights*

We know we can successfully train a relational DQN on this somewhat difficult Gridworld task, but we could have used a much less fancy DQN to do the same thing. However, we also cared about visualizing the attention weights to see what exactly the agent has learned to focus on when playing the game. Some of the results are surprising, and some are what we would expect.

 To visualize the attention weights, we had our model save a copy of the attention weights each time it was run forward, and we can access it by calling GWagent.att map, which returns a *batch* × *head* × *height* × *width* tensor. All we need to do is run the model forward on some state, select an attention head, and select a node to visualize, and then reshape the tensor into a  $7 \times 7$  grid and plot it using plt. imshow.

```
>>> state_ = env.reset()
>>> state = prepare_state(state_)
>>> GWagent(state)
>>> plt.imshow(env.render('rgb_array'))
>>> plt.imshow(state[0].permute(1,2,0).detach().numpy())
>>> head, node = 2, 26
>>> plt.imshow(GWagent.att_map[0][head][node].view(7,7))
```

We decided to look at the attention weights for the key node, the door node, and the agent node to see which objects are related to each other. We found the node in the attention weights that corresponds to the node in the grid by counting the grid cells, since both the attention weights and the original state are a  $7 \times 7$  grid. We intentionally designed the relational module such that the original state and attention weight matrices are the same dimensionality; otherwise it becomes difficult to map the attention weights onto the state. Figure 10.23 shows the original full view of the grid in a random initial state and the corresponding prepared state.

![](3__page_41_Figure_4.jpeg)

Figure 10.23 Left: The full observation of the environment. Right: The corresponding partial state view that the agent has access to.

The partial view is a little confusing at first because it is an egocentric view, so we annotated it with the positions of the agent  $(A)$ , key  $(K)$ , and the door  $(D)$ . Because the agent's partial view is always  $7 \times 7$  and the size of the full grid is only  $5 \times 5$ , the partial view always includes some empty space. Now let's visualize the corresponding attention weights for this state.

 In figure 10.24, each column is labeled as a particular node's attention weights (i.e., the nodes to which it is paying attention), restricting ourselves to just the agent, key, and door nodes out of a total of  $7 \times 7 = 49$  nodes. Each row is an attention head, from head 1 to head 3, top to bottom. Curiously, attention head 1 does not appear to

![](3__page_42_Figure_1.jpeg)

Figure 10.24 Each row corresponds to an attention head (e.g., row 1 corresponds to attention head 1). Left column: The self-attention weights for the agent, which shows the objects to which the agent is paying most attention. Middle column: The self-attention weights for the key, which shows the objects to which the key is paying most attention. Right column: The self-attention weights for the door.

be focusing on anything obviously interesting; in fact, it is focusing on grid cells in empty space. Note that while we're only looking at 3 of the 49 nodes, even after looking at all of the nodes, the attention weights are quite sparse; only a few grid cells at most are assigned any significant attention. But perhaps this isn't surprising, as the attention heads appear to be specializing.

 Attention head 1 may be focusing on a small subset of landmarks in the environment to get an understanding of location and orientation. The fact that it can do this with just a few grid cells is impressive.

 Attention heads 2 and 3 (rows 2 and 3 in figure 10.24) are more interesting and are doing close to what we expect. Look at attention head 2 for the agent node: it is strongly attending to the key (and essentially nothing else), which is exactly what we would hope, given that at this initial state its first job is to pick up the key. Reciprocally, the key is attending to the agent, suggesting there is a bidirectional relation from agent to key and key to agent. The door is also attending to the agent most strongly, but there's also a small amount of attention given to the key and the space directly in front of the door.

 Attention head 3 for the agent is attending to a few landmark grid cells, again, probably to establish a sense of position and orientation. Attention head 3 for the key is attending to the door and the door is reciprocally attending to the key.

 Putting it all together, we get that the agent is related to the key which is related to the door. If the goal square was in view, we might see that the door is also related to the goal. While this is a simple environment, it has relational structure that we can learn with a relational neural network, and we can inspect the relations that it learns. It is interesting how sparsely the attention is assigned. Each node prefers to attend strongly to a single other node, with sometimes a couple other nodes that it weakly attends to.

 Since this is a Gridworld, it is easy to partition the state into discrete objects, but in many cases such as the Atari games, the state is a big RGB pixel array, and the objects we would want to focus on are collections of these pixels. In this case it becomes difficult to map the attention weights back to specific objects in the video frame, but we can still see which parts of the image the relational module as a whole is using to make its decisions. We tested a similar architecture on the Atari game Alien (we just used  $4 \times$ 4 kernel convolutions instead of  $1 \times 1$  and added some maxpooling layers), and we can see (in figure 10.25) that it indeed learns to focus on salient objects in the video frame (code not shown).

![](3__page_43_Figure_4.jpeg)

Figure 10.25 Left: Preprocessed state given to the DQN. Middle: Raw video frame. Right: Attention map over state. We can see that the attention map is focused on the alien in the bottom center of the screen, the player in the center, and the bonus at the top, which are the most salient objects in the game.

Relational modules using the self-attention mechanism are powerful tools in the machine learning toolkit, and they can be very useful for training RL agents when we want some idea of how they're making decisions. Self-attention is one mechanism for performing message passing on a graph, as we discussed, and it's part of the broader field of graph neural networks, which we encourage you to explore further. There are many implementations of graph neural networks (GNNs) but particularly relevant for us after this chapter is the *graph attention network*, which uses the same self-attention mechanism we just implemented but with the added ability to operate on more general graph-structured data.

## *Summary*

- Graph neural networks are machine learning models that operate on graphstructured data. Graphs are data structures composed of a set of objects (called nodes) and relations between objects (called edges). A natural graph type is a social network in which the nodes are individuals and the edges between nodes represent friendships.
- An adjacency matrix is a matrix with dimensions *A*:*N* × *N* where *N* is the number of nodes in a graph that encodes the connectivity between each pair of nodes.
- **Message passing is an algorithm for computing updates to node features by iter**atively aggregating information from a node's neighbors.
- Inductive biases are the prior information we have about some set of data; we use them to constrain our model toward learning certain kinds of patterns. In this chapter we employed a relational inductive bias, for example.
- We say a function, *f* is invariant to some transformation, *g*, when the function's output remains unchanged when the input is first transformed by *g*:  $f(g(x)) = f(x)$ .
- We say a function,  $f$ , is equivariant to some transformation,  $g$ , when applying the transformation to the input is the same as applying the transformation to the output:  $f(g(x)) = g(f(x))$ .
- Attention models are designed to increase the interpretability and performance of machine learning models by forcing the model to only "look at" (attend to) a subset of the input data. By examining what the model learns to attend to, we can have a better idea of how it is making decisions.
- Self-attention models model attention between objects (or nodes) in an input rather than just the model attending to different parts of the input. This naturally leads to a form of graph neural network, since the attention weights can be interpreted as edges between nodes.
- **Multi-head self-attention allows the model to have independent attention** mechanisms that can each attend to a different subset of the input data. This allows us to still get interpretable attention weights but increases the bandwidth of information that can flow through the model.
- Relational reasoning is a form of reasoning based on objects and relationships between objects, rather than using absolute frames of reference. For example, "a book is on the top" relates the book to the table, rather than saying the book is at position 10 and the table is at position 8 (an absolute reference frame).
- Inner (dot) product is a product between two vectors that results in a single scalar value.

- Outer product is a product between two vectors that results in a matrix.
- **Einstein notation or Einsum lets us describe generalized tensor-tensor products** called tensor contractions using a simple syntax based on labeling the indices of a tensor.
- Double Q-learning stabilizes training by separating action-selection and actionvalue updating.