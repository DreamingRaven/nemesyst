#!/usr/bin/env python3.6
import tensorflow as tf
import os
import sys

# creating prepend variable for logging
prePend = "[ " + os.path.basename(sys.argv[0]) + " ] "

# creating tensorflow session
sess = tf.Session()

# text test
hello = tf.constant("Hello, from TensorFlow.")
print(prePend, sess.run(hello))

# numeric test
a = tf.constant(10)
b = tf.constant(72)
print(prePend, "10 + 72 = ",sess.run(a+b))

print(prePend, "Fin.")