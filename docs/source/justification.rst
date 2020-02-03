Why use Nemesyst
================

Nemesyst is a highly configurable hybrid parallelization deep learning framework, for distributed deep learning, that uses other backend framework(s) of your choice (Pytorch, TensorFlow, etc.) for training.

.. figure:: nemesyst_example.svg
    :alt: Nemesyst use-case example diagram.
    :figclass: align-center

    This image is a use case example of Nemesyst applied to a distributed refrigeration fleet over multiple sites, and both online and offline learning capabilities occuring simultaneously.

Nemesyst uses MongoDB as its core message passing interface (MPI). This means MongoDB is used to store, distribute, retrieve, and transform the data; store, distribute, and retrieve the trained models. In future we also hope to use it to transfer more specific processing instructions to individual learners. This way we use the already advanced functionality of MongoDB to handle complex and non-trivial problems such as tracing models back to the specific data trained with, the results and arguments present at the point of training, and being able to reload pre-trained models for further use, and, or training. This also means the same data can be transformed differently for different learners from the same source dynamically at the point of need.

.. Types of parallelisation:
..
.. * model parallelism; where a single model is trained using multiple hardware instances, and the same data.
.. * data parallelism; where different models are trained on a single hardware instance, using different data.
.. * hybrid parallelism; where each model is trained on independant groups of hardware and data.
.. * dynamic parallelism; where the parallelism strategy is dynamically used.
