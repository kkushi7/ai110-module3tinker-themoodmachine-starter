# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

You may complete this model card for whichever version you used, or compare both if you explored them.

## 1. Model Overview

**Model type:**  
Describe whether you used the rule based model, the ML model, or both.  
I used the rule based model but also tested the ML model using Copilot. 

**Intended purpose:**  
What is this model trying to do?  
Classify short text messages as moods like positive, negative, neutral, or mixed as seen in social media and how people would text each now in this generation.

**How it works (brief):**  
For the rule based version, describe the scoring rules you created. 
We gave examples of messages that people could say and gave its direct mood to help the model score more accurately. 
For the ML version, describe how training works at a high level (no math needed).
The training works by automatically learning rules from the labeled examples given in the rule based version.



## 2. Data

**Dataset description:**  
Summarize how many posts are in `SAMPLE_POSTS` and how you added new ones.
There are around 15 posts in the sample posts and we are able to add new ones by continuing them in the list.

**Labeling process:**  
Explain how you chose labels for your new examples.  
Mention any posts that were hard to label or could have multiple valid labels.
I thought of phrases and comments I use as well as have seen on social media in comments or posts. 

**Important characteristics of your dataset:**  
Examples you might include:  

- Contains slang or emojis  
- Includes sarcasm  
- Some posts express mixed feelings  
- Contains short or ambiguous messages

**Possible issues with the dataset:**  
Think about imbalance, ambiguity, or missing kinds of language.

## 3. How the Rule Based Model Works (if used)

**Your scoring rules:**  
Describe the modeling choices you made.  
Examples:  

- How positive and negative words affect score  
- Negation rules you added  
- Weighted words  
- Emoji handling  
- Threshold decisions for labels

**Strengths of this approach:**  
Where does it behave predictably or reasonably well?
It behaves well with straightforward terms that give away if the context are positive or negative.

**Weaknesses of this approach:**  
Where does it fail?  
Examples: sarcasm, subtlety, mixed moods, unfamiliar slang.
If unsure, it tends to give back neutral when some of the examples show if it is positive or negative. 

## 4. How the ML Model Works (if used)

**Features used:**  
Describe the representation.  
Example: “Bag of words using CountVectorizer.”

**Training data:**  
State that the model trained on `SAMPLE_POSTS` and `TRUE_LABELS`.

**Training behavior:**  
Did you observe changes in accuracy when you added more examples or changed labels?

**Strengths and weaknesses:**  
Strengths might include learning patterns automatically.  
Weaknesses might include overfitting to the training data or picking up spurious cues.

## 5. Evaluation

**How you evaluated the model:**  
Both versions can be evaluated on the labeled posts in `dataset.py`.  
Describe what accuracy you observed.
It was accurate once adding in logic for predict label which was most accuarte with simple, straightforward key words.

**Examples of correct predictions:**  
Provide 2 or 3 examples and explain why they were correct.
"I am mad": correct because the keyword mad shows it was a negative statement
"I love this": correct because keyword love shows how it was a positive statement
**Examples of incorrect predictions:**  
Provide 2 or 3 examples and explain why the model made a mistake.  
If you used both models, show how their failures differed.
"I am crying": it gave back as neutral when I put it as negative
"Stoppp": it gave back as neutral when I put it as mixed since it has a more sarcastic tone.

## 6. Limitations

Describe the most important limitations:   
The dataset is small  
It cannot detect sarcasm reliably  
It depends heavily on the words you chose or labeled

## 7. Ethical Considerations

Discuss any potential impacts of using mood detection in real applications:  
Misclassifying a message expressing distress  
Misinterpreting mood for certain language communities  
Privacy considerations if analyzing personal messages

## 8. Ideas for Improvement

List ways to improve either model:  
Will need a bigger data set with more variations of less straightforward wording and emotions in the text.
Add better preprocessing for emojis or slang
Improve the rule based scoring method 
Add a real test set instead of training accuracy only