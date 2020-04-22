from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# Load dataset from UCI ML repo
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"

# Update column (feature) names
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']

dataset = read_csv(url, names=names)

# shape - 150 rows (examples) and 5 cols (attributes)
print(dataset.shape)
# peak into the dataset
print(dataset.head(20))
# stats
print(dataset.describe())
# class distribution
print(dataset.groupby('class').size())


# === Univariate Plots i.e. plots of each individual variable ===
# box and whisker plots
dataset.plot(kind='box', subplots=True, layout=(2, 2), sharex=False, sharey=False)
pyplot.show()

# histogram
dataset.hist()
pyplot.show()

# === Multivariate Plots i.e. relationship among the variables ===
# scatter plot
scatter_matrix(dataset)
pyplot.show()
