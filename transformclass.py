from __future__ import division
import pandas as pd
from sklearn.base import TransformerMixin       



from UserData import *


df = a
#returns A dictionary with features as keys and True - if categorical False - continuos  
def metadata():
    likely = {}
    for var in df.columns:
        likely[var] = (1.*df[var].nunique()/df[var].count() ) < 0.2
    return likely      
    
#return A list of categorical column names    
def category():
    dic = metadata()
    newdf = pd.DataFrame(index = df.index)
    for i in dic.keys():
        if dic[i] and i != "class":
            newdf[i] = df[i] 
    return list(newdf.columns)

#return a list of continuos names
def continuos():
    dic = metadata()
    newdf = pd.DataFrame(index = df.index)
    for i in dic.keys():
        if not dic[i] and i != "class":
            newdf[i] = df[i] 
    return list(newdf.columns.values)    

      
      
#Ftransform for Feature selection methods       
class NoFitMixin:
    def fit(self, X, y=None): 
        self.y = y
        if self.func.score_func.__name__ == "chi2":
            self.X = X[category()]
        else:
            self.X = X[continuos()]
        #print self.X
        #print self.X.shape
        if self.X.shape[1] == 0:
            #print "NOne --------------"
            return self
        self.func.fit(self.X,y)
        return self
        
class FTransform(TransformerMixin, NoFitMixin):
    def __init__(self, func, copy=False):
        #print func.score_func.__name__
        self.func   = func
        self.copy   = copy
        self.cat    = category()
        self.cont   = continuos()
        self.lst    =  ["No Selection Done"]
    def transform(self, X):
        if self.func.score_func.__name__ == "chi2":
            self.X = X[category()]
        else:
            self.X = X[continuos()]
        if self.X.shape[1] == 0:
            return X
        di = self.X.index
        dc = self.X.columns
        lst = {}
        #Mapping the columns names to their position
        for i in dc:
            lst[self.X.columns.get_loc(i)] = i
        self.out    = self.func.transform(self.X)
        #try:
        newcol = []  
        try:          
            #To get The position of indices which are selected
            right = self.func.get_support(indices=True)
            #using the dictionary to reverse map the postions to column names
            for i in right:
                newcol.append(lst[i])
            #print newcol 
            self.lst = newcol                  
            return pd.DataFrame(self.out,index=di,columns=newcol)
        except:
            l = []
            for i in range(self.out.shape[1]):
                l.append(chr(i+97))
            return pd.DataFrame(self.out,index=di,columns=l)
    def get_feature_names(self):
        return self.lst
    def fit_transform(self,X,y):
        self.fit(X,y)
        return self.transform(X)  
        
#For Missing Value and data Preprocessing        
class NoFitMixin1:
    def fit(self, X, y=None): 
        self.y = y
        self.func = self.func.fit(X,y)
        return self.func
class DFTransform(TransformerMixin, NoFitMixin1):
    def __init__(self, func, copy=False):
        self.func = func
        self.copy = copy    
    def transform(self, X):
        #X_ = X if not self.copy else X.copy()
        di = X.index
        dc = X.columns
        lst = {}
        for i in dc:
            lst[X.columns.get_loc(i)] = i
        out  = self.func.transform(X)
        try:
            right = self.func.get_support(indices=True)
            newcol = []
            for i in right:
                newcol.append(lst[i])
            return pd.DataFrame(out,index=di,columns=newcol)
        except Exception as e:
            l = []
            if out.shape[1] == len(dc):
                return pd.DataFrame(out,index=di,columns=dc)
            for i in range(out.shape[1]):
                l.append(str(i))
            return pd.DataFrame(out,index=di,columns=l)
    def fit_transform(self,X,y):
        self.fit(X,y)
        return self.transform(X)
    def transfo():
        return self.func.predict()

        
        
        
