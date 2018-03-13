
# Personalization project

For Amazon e-commerce, the recommender system plays a very important role in converting users to buyers. The more attractive our recommendation is, the more likely users are going to click on and find out more about relevant products, eventually leading to purchases. Thus, improving recommender system can result in higher click-through-rate, which translates to higher bottom line. 

Data set: Amazon Grocery and Gourmet Food

### Part 1 

Objective: Build basic recommendation models.  
Comparison of 3 models used for recommender system:
 
- Baseline model 
- Neighborhood-based collaborative filtering (KNN)
- Model-based collaborative filtering with SVD 

Details are in basic_model_evaluation.ipynb.


### Part 2

Objective: Build our own recommender system.

Recommender system handles sparse and dense data separately:

- For sparse data, we combine:
    - Content-based model (build our own) <br />
    - Association rule model (build our own) <br />

- For dense data, we combine:
    - Model-based CF
    - KNN <br />
    - Content-based model (build our own)

![Model Diagram](/part%20II/model.png)

Details are in part2_submission.ipynb	in folder Part II.

<p>Reference: <br />
- R. He, J. McAuley. Modeling the visual evolution of fashion trends with one-class collaborative filtering. WWW, 2016 <br />
- J. McAuley, C. Targett, J. Shi, A. van den Hengel. Image-based recommendations on styles and substitutes. SIGIR, 2015
