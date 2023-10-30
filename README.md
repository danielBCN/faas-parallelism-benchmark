# FaaS Parallelism Benchmark

FaaS platforms are believed to provide great parallelism capabilities.
The experiments in this repository explore how [AWS Lambda](aws), [Azure Functions](azure), [Google Cloud Functions](gcp) and [IBM Cloud Functions](ibm) behave with parallel compute intensive tasks.
For that we run several experiments with such tasks and plot their timeline while showing the parallelism achieved.

This repository contains the scripts to run the experiments and plot the timeline evolution.
We also include results and plots of several executions.

Read the full paper:

Daniel Barcelona-Pons and Pedro García-López. 2021. _Benchmarking parallelism in FaaS platforms._ Future Gener. Comput. Syst. 124, C (Nov 2021), 268–284. https://doi.org/10.1016/j.future.2021.06.005
