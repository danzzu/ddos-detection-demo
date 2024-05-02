from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import CategoricalNB
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

# Using Naive Bayes Categorical alpha = 1 
model = CategoricalNB()

# Fit the training X and Y to the model
model.fit(X_train,y_train)

# Print the score/accuracy of the model
print("Accuracy from Test : ", model.score(X_test,y_test) * 100, "%")