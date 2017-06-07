from sklearn.datasets import load_iris,load_diabetes  
from sklearn.cross_validation import train_test_split
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
import datetime
#s = "abcdefghijklmnopqrst"
#sam = 100000
#testsam = 500
#data = make_classification(n_samples = sam ,n_features = 5, n_informative = 2, n_redundant = 1, n_clusters_per_class=1)
#a = data[0][0:sam-testsam]
#c = data[0][sam-500:sam]
#b = data[1][0:sam-testsam]
#d = data[1][sam-500:sam]
#a = pd.DataFrame(a, columns = list(s[0:5]))
#c = pd.DataFrame(c, columns = list(s[0:5]))
#b = pd.DataFrame(b, columns = ["target"])
#d = pd.DataFrame(d, columns = ["target"])     

data = load_iris()
a,c,b,d = train_test_split(data['data'], data.target, test_size=0.33, random_state=42)     
a = pd.DataFrame(a,index = range(len(a)), columns = data.feature_names)
c = pd.DataFrame(c,index = range(len(c)), columns = data.feature_names)
b = pd.DataFrame(b,index = range(len(b)) , columns = ["target"])
d = pd.DataFrame(d,index = range(len(d)) , columns = ["target"])

""" 
a = pd.DataFrame( np.array([[1,11,0,98],[2,11,0,99],[102,11,1,98],[103,11,1,99],[50,11,0,98] ] ))
a.index = [1,2,3,4,5]
a.columns = ['c1','c2','c3','c4']
b = pd.DataFrame(np.array([0,0,1,1,0]))
data = a
c = pd.DataFrame(np.array([ [1,10,1,98],[20,1,1,99],[100,1,1,98] ,[45,11,0,99] ]) )
c.index = [1,2,3,4]
c.columns = ['c1','c2','c3','c4']
d = np.array([0,0,1,0])
 """    

#admiss = pd.read_csv('UCB.csv')
#admiss['Admit'] = admiss['Admit'].replace(['Admitted','Rejected'] , [0,1])
#admiss['Gender'] = admiss['Gender'].replace(['Male','Female'] , [0,1])
#admiss['Dept'] = admiss['Dept'].replace(list('ABCDEF') , range(0,6) )
#
#a = pd.DataFrame(admiss[['Gender','Dept','Freq']][0:15])
#b = pd.DataFrame(admiss['Admit'][0:15])
#c = pd.DataFrame(admiss[['Gender','Dept','Freq']][15:24])
#d = pd.DataFrame(admiss['Admit'][15:24])
#
#         
#data =   load_diabetes()
#a,c,b,d = train_test_split(data['data'], data.target, test_size=0.33, random_state=42)     
#a = pd.DataFrame(a,index = range(len(a)), columns = list("abcdefghij") )
#c = pd.DataFrame(c,index = range(len(c)), columns = list("abcdefghij"))
#b = pd.DataFrame(b,index = range(len(b)) , columns = ["target"])
#d = pd.DataFrame(d,index = range(len(d)) , columns = ["target"])       


#a = pd.DataFrame( np.array([[1,11,float('NaN'),98],[2,11,0,99],[102,11,float('NaN'),98],[float('NaN'),11,float('NaN'),99],[50,11,1,98] ] ))
#a.index = [1,2,3,4,5]
#a.columns = ['c1','c2','c3','c4']
#b = pd.DataFrame(np.array([0,0,1,1,0]))
#b.columns = ["target"]
#c = pd.DataFrame(np.array([ [1,10,1,98],[20,1,1,99],[100,1,1,98] ,[45,11,0,99] ]) )
#c.index = [1,2,3,4]
#c.columns = ['c1','c2','c3','c4']
#d = pd.DataFrame(np.array([0,0,1,0]))
#d.columns = ["target"]          

#a = pd.DataFrame( np.array([[1,11,float('NaN'),98],[2,11,0,99],[102,11,float('NaN'),98],[float('NaN'),11,float('NaN'),99],[50,11,1,98] ] ))
#a.index = [1,2,3,4,5]
#a.columns = ['c1','c2','c3','c4']
#b = pd.DataFrame(np.array([99,101,200,129,148]))
#b.columns = ["target"]
#c = pd.DataFrame(np.array([ [1,10,1,98],[20,1,1,99],[100,1,1,98] ,[45,11,0,99] ]) )
#c.index = [1,2,3,4]
#c.columns = ['c1','c2','c3','c4']
#d = pd.DataFrame(np.array([99,119,198,144]))
#d.columns = ["target"]          

#abalone = pd.read_csv('abalone.csv')
#abalone['M'] = abalone['M'].map({'M':0,'F':1,'I':2})
#abalone.columns = ['a','b','c','d','e','f','g','h','target']
##admiss['Dept'] = admiss['Dept'].replace(list('ABCDEF') , range(0,6) )


#-----------------------------------------------------------------------------------------------------------
#a,c,b,d = train_test_split(abalone[list('abcdefgh')], abalone.target, test_size=0.33, random_state=42)

