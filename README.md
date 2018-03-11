# Personalization project

Data set: Amazon Grocery and Gourmet Food

Part 1 <br />
Objective: Increase conversion rate from product views to sales. <br />
Comparison of 3 models used for recommender system:
 + Baseline model <br />
 + Neighborhood-based collaborative filtering (KNN) <br />
 + Model-based collaborative filtering with SVD <br />
<br />
Please see part1_submission.ipynb	in folder part I for code to build and train the models

Math equation:

$$
\sum_{i=1}^n x = \frac{x(x+1)}{2}
$$

```python
print('this is a test')
```

<p>Part 2 <br />
Objective: Build our own recommender system.
<p>Recommender system handles sparse and dense data separately: <br />
For sparse data, we combine: <br />
 + Content-based model (build our own) <br />
 + Association rule model (build our own) <br />
For dense data, we combine: <br />
 + Model-based CF <br />
 + KNN <br />
 + Content-based model (build our own)<br />
<br />
Please see part2_submission.ipynb	in folder part II for code to build and train the models
<br />
<p>Reference: <br />
- R. He, J. McAuley. Modeling the visual evolution of fashion trends with one-class collaborative filtering. WWW, 2016 <br />
- J. McAuley, C. Targett, J. Shi, A. van den Hengel. Image-based recommendations on styles and substitutes. SIGIR, 2015
