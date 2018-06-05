import tensorflow as tf

words_in_dataset = []
words_in_dataset.append("hello, bonjour")
words_in_dataset.append("how, comment")
words_in_dataset.append("are, allez")
words_in_dataset.append("you, vous")
words_in_dataset.append("?, ?")

batch_size = 2
time_steps = 5
num_features = 5
lstm_size = 20


words_in_dataset = tf.placeholder(tf.float32, [time_steps, batch_size, num_features])
print(words_in_dataset)
lstm = tf.contrib.rnn.BasicLSTMCell(lstm_size)
print(lstm)
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




# # Placeholder for the inputs in a given iteration.
# words = tf.placeholder(tf.int32, [batch_size, num_steps])

# lstm = tf.contrib.rnn.BasicLSTMCell(lstm_size)
# # Initial state of the LSTM memory.
# initial_state = state = tf.zeros([batch_size, lstm.state_size])

# for i in range(num_steps):
#     # The value of state is updated after processing each batch of words.
#     output, state = lstm(words[:, i], state)

#     # The rest of the code.
#     # ...

# final_state = state