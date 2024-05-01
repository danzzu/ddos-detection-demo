from parserpcap import pcap_dataframe
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import CategoricalNB
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import pandas as panda

dataset = 'dataset_sdn.csv'
raw_data = panda.read_csv(dataset)

error_message = 'DDoS detected'
normal_message = "No threat detected"

# X independent features : IP source / destination, Packet count, Byte of the packet, duration / in nano-second, Protocol, Port number
# Y dependent features : label -> 1 for malicious and 0 for none.
raw_data = raw_data.loc[: , ['src','dst','bytecount', 'port_no', 'Protocol' ,'label']]

# Categorical 
categorical_features = ['src','dst','Protocol']
# Converting those non-numerical value to 0s and 1s
one_hot = OneHotEncoder()
# Instead of dropping and concat lists, ColumnTransformer help us to achieve the same result with filtering which categories it needs to feature encode.
# Without sparse_threshold, it would occur that transforming would cause the array to be in CSR matrix rather than Sparse Matrix.
transformer = ColumnTransformer([("one_hot",
                                  one_hot,
                                  categorical_features)],
                                 remainder='passthrough',
                                 sparse_threshold=0)


X = raw_data.drop('label',axis=1)
# Focus on the label only for y dependent
y = raw_data['label']
transform_X = transformer.fit_transform(X)
# Splitting the data for 80% train and 20% test
X_train, X_test, y_train, y_test = train_test_split(transform_X, y, test_size=0.2, random_state=0)
model = CategoricalNB()
model.fit(X_train,y_train)

print("Accuracy from Test : ", model.score(X_test,y_test) * 100, "%")

# Parse the pcap file into a DataFrame [TODO]
new_data_file = 'ack_attack_fixed.pcap'
pcap_data = pcap_dataframe(new_data_file)

