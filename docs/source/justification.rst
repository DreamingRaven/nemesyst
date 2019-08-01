Why use Nemesyst
================
Nemesyst is a hybrid parallelisation deep learning framework, for distributed
deep learning, that uses other framework(s) of your choice

Types of parallelisation:

* model parallelism; where a single model is trained using multiple hardware instances, and the same data.
* data parallelism; where different models are trained on a single hardware instance, using different data.
* hybrid parallelism; where each model is trained on independant groups of hardware and data.
* dynamic parallelism; where the parallelism strategy is dynamically used.
