# tensorflow LSTM tutorial to set up the framework for SC AI.
# https://www.tensorflow.org/tutorials/recurrent#language_modeling


# The core of the model consists of an LSTM cell that processes one word at a time 
# and computes probabilities of the possible values for the next word in the sentence. 
# The memory state of the network is initialized with a vector of zeros 
# and gets updated after reading each word. For computational reasons, 
# we will process data in mini-batches of size batch_size. In this example, 
# it is important to note that current_batch_of_words does not correspond to a "sentence" of words. 
# Every word in a batch should correspond to a time t. TensorFlow will automatically sum the gradients of each batch for you.

words_in_dataset = tf.placeholder(tf.float32, [time_steps, batch_size, num_features])
lstm = tf.contrib.rnn.BasicLSTMCell(lstm_size)
# Initial state of the LSTM memory.
hidden_state = tf.zeros([batch_size, lstm.state_size])
current_state = tf.zeros([batch_size, lstm.state_size])
state = hidden_state, current_state
probabilities = []
loss = 0.0
for current_batch_of_words in words_in_dataset:
    # The value of state is updated after processing each batch of words.
    output, state = lstm(current_batch_of_words, state)

    # The LSTM output can be used to make next word predictions
    logits = tf.matmul(output, softmax_w) + softmax_b
    probabilities.append(tf.nn.softmax(logits))
    loss += loss_function(probabilities, target_words)





# truncated back propagation
# Placeholder for the inputs in a given iteration.
words = tf.placeholder(tf.int32, [batch_size, num_steps])

lstm = tf.contrib.rnn.BasicLSTMCell(lstm_size)
# Initial state of the LSTM memory.
initial_state = state = tf.zeros([batch_size, lstm.state_size])

for i in range(num_steps):
    # The value of state is updated after processing each batch of words.
    output, state = lstm(words[:, i], state)

    # The rest of the code.
    # ...

final_state = state





# how to implement an iteration over the whole dataset:

# A numpy array holding the state of LSTM after each batch of words.
numpy_state = initial_state.eval()
total_loss = 0.0
for current_batch_of_words in words_in_dataset:
    numpy_state, current_loss = session.run([final_state, loss],
        # Initialize the LSTM state from the previous iteration.
        feed_dict={initial_state: numpy_state, words: current_batch_of_words})
    total_loss += current_loss




#The word IDs will be embedded into a dense representation (see the Vector Representations Tutorial) before feeding to the LSTM. This allows the model to efficiently represent the knowledge about particular words. It is also easy to write:
# embedding_matrix is a tensor of shape [vocabulary_size, embedding size]
word_embeddings = tf.nn.embedding_lookup(embedding_matrix, word_ids)







# To give the model more expressive power, we can add multiple layers of LSTMs to process the data. The output of the first layer will become the input of the second and so on.

# We have a class called MultiRNNCell that makes the implementation seamless:
def lstm_cell():
  return tf.contrib.rnn.BasicLSTMCell(lstm_size)
stacked_lstm = tf.contrib.rnn.MultiRNNCell(
    [lstm_cell() for _ in range(number_of_layers)])

initial_state = state = stacked_lstm.zero_state(batch_size, tf.float32)
for i in range(num_steps):
    # The value of state is updated after processing each batch of words.
    output, state = stacked_lstm(words[:, i], state)

    # The rest of the code.
    # ...

final_state = state














