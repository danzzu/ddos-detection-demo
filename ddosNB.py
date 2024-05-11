from time import monotonic_ns
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import CategoricalNB, MultinomialNB, BernoulliNB, GaussianNB
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import pandas as panda

# Dataset File Name
dataset = 'dataset_sdn.csv'
# Read the Dataset and create a DataFrame (A matrix 2D)
raw_data = panda.read_csv(dataset)

# X independent features : DateTime, Source, Destination, Packet Count, Bytes Count, Duration in Nanosec, Packet Flows, Pair flow, Protocol
# Since Source and Destination will always be arbitrary and can be spoofed, we remove that column
    # Analyzing Source and Destination to find malicious address would be considered as another model
# Y dependent features : label -> 1 for malicious and 0 for none.
raw_data = raw_data.loc[: , ['dt', 'pktcount', 'bytecount', 'dur_nsec', 'flows', 'Pairflow', 'Protocol', 'label']]


# Instead of dropping and concat lists, ColumnTransformer help us to achieve the same result with filtering which categories it needs to feature encode.
# Without sparse_threshold, it would occur that transforming would cause the array to be in CSR matrix rather than Sparse Matrix.
preprocessor = ColumnTransformer(
    transformers=[
        ("proto",OneHotEncoder(), ['Protocol'])
    ],
    remainder='passthrough',
    sparse_threshold=0
)

# Independent layers
X = raw_data.drop('label',axis=1)

# Preprocessed X for Protocol which is object dtypes
transform_X = preprocessor.fit_transform(X)

# Train on dependent variable to determine if something is classified as malicous or not.
y = raw_data['label']

# Splitting the data for 80% train and 20% test
X_train, X_test, y_train, y_test = train_test_split(transform_X, y, test_size=0.2, random_state=0)

# Use to test our hypothesis (View the report on "System Architecture" section for more details.):
time_train = []
scores = []

start = monotonic_ns()
# Using Naive Bayes Categorical alpha = 1 (default) 
categorical = CategoricalNB()
# Fit the training X and Y to the model
categorical.fit(X_train,y_train)
ct_score = categorical.score(X_test,y_test)
end = monotonic_ns()
time_train.append(round((end - start)/1_000_000))
scores.append(ct_score)

# Multinomial Comparison.
start = monotonic_ns()
multinomial = MultinomialNB()
multinomial.fit(X_train, y_train)
mn_score = multinomial.score(X_test, y_test)
end = monotonic_ns()
time_train.append(round((end - start)/1_000_000))
scores.append(mn_score)

# Bernoulli Comparison.
start = monotonic_ns()
bernoulli = BernoulliNB()
bernoulli.fit(X_train, y_train)
b_score = bernoulli.score(X_test, y_test)
end = monotonic_ns()
time_train.append(round((end - start)/1_000_000))
scores.append(b_score)

# Gaussian Comparison.
start = monotonic_ns()
gaussian = GaussianNB()
gaussian.fit(X_train, y_train)
g_score = gaussian.score(X_test, y_test)
end = monotonic_ns()
time_train.append(round((end - start)/1_000_000))
scores.append(g_score)


models = ["Categorical NB", "Multinomial NB", "Bernoulli NB", "Gaussian NB"]

table = {
    "Model" : models,
    "Time(ms)" : time_train,
    "Score" : scores
}
# Print the score/accuracy of the model
table_frame = panda.DataFrame(table)
print(table_frame)