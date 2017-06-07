from sklearn import preprocessing as prep
from sklearn import linear_model
from sklearn.cluster import KMeans
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn import tree
from sklearn.feature_selection import chi2
from sklearn import svm
from sklearn.decomposition import PCA
import pickle
from sklearn.pipeline import FeatureUnion
#version conflict can occur for below line
from sklearn.grid_search import GridSearchCV
import os
import datetime
from sklearn.feature_selection import SelectFromModel

#-------------------custom libraries---------------------------------#
from UserInterface import *
from transformclass import *
     
models_linear = { 
                    "Logistic Regression"     : True ,
                    "Decision Trees"         : False,
                    "svm"                    : True ,
                    "RandomForestClassifier" : False                    
                } 

     
methodObj =  {
              'step0': {'Impute': prep.Imputer() },
              'step1': {'Normalize': prep.Normalizer(),'MinMax' : prep.MinMaxScaler()},
              'step2': {'PCA': PCA()},
              'step3': {'f_reg' :  SelectKBest( f_regression ) , 'Chi_2' : SelectKBest(chi2)  } 
              }

estimatorMethods =  {'Logistic Regression': linear_model.LogisticRegression(),
                     'Linear Regression': linear_model.LinearRegression(),
                        'Decision Trees' : tree.DecisionTreeClassifier(), 
                     'k-means': KMeans(),
                     'svm' : svm.SVC() ,
                     'Ridge' : linear_model.Ridge()
                     }


featureSelectiontoclass  = {
                              'f_reg' : SelectKBest(f_regression),
                              'Chi_2' : SelectKBest(chi2)  , 
                              'f_classif' : SelectKBest()
                          }
                 

def checker():
    if check() == cla:
        consistency_check(classification_features)
    elif check() == reg:
        consistency_check(regression_features)
#Cases Like if Having all Continuos variable and using Categorical Feature Selection and vice versa
def consistency_check(feature_dic):
    dic  = metadata()
    #All are categorical
    if sum(dic.values()) == len(dic):
        #make continuos Feature Selectors False
        if sum(feature_dic["continuos"].values()) > 0:
            print "Warning Continuos Feature Selectors are set to false Due to Absence of Continuos Features"
        for i in feature_dic["continuos"]:
            feature_dic[i] = False
    #All are continuos       
    elif sum(dic.values()) == 0:
        if sum(feature_dic["categorical"].values()) > 0:
            print "Warning categorical Feature Selectors are set to false Due to Absence of categorical Features"
        for i in feature_dic["categorical"]:
            feature_dic[i] = False
    
#used for forming combinations classification features
def feature_combinations(fdic):
    cont = []
    cat  = []
    l = fdic["continuos"]
    for i in l:
        if l[i] == True:
            cont.append(i)
    l = fdic["categorical"]
    for i in l:
        if l[i] == True:
            cat.append(i)
    if len(cont) != 0 and len(cat) != 0:
        return list(product(cont,cat))
    elif len(cont) != 0:
        return (cont)
    elif len(cat) != 0:
        return (cat)
    else:
        return []
        
#used to ensure only one algo is True [clustering,classification]         
def check():
     assert(sum(algo.values()) == 1)
     for i,j in algo.iteritems():
         if j:
             return i

#used to fetch the metrics
def metrics(algo):
    lst = []
    if algo == "Classification":
         for key,value in class_metrics["metrics"].iteritems():
                if value:
                    lst.append(key)
                
    elif algo == "Regression":
         for key,value in reg_metrics["metrics"].iteritems():
                if value:
                    lst.append(key)
    elif algo == "Clustering":
         for key,value in clus_metrics["metrics"].iteritems():
                if value:
                    lst.append(key)
    return lst
                     
                     
#used to set the parameters of the object                                 
def model_from_name(step_no,name):
    if methodObj.has_key(step_no):
        
        temp_dict = methodObj.get(step_no)
        param_dict = paramObj.get(step_no)
        if temp_dict.has_key(name):
            updated_param_dict = param_dict.get(name)
            #print updated_param_dict
            met = temp_dict.get(name)
            #print met
            met.set_params(**updated_param_dict)
            #print met
            
            
            

def get_method_step(step_no):
    true_methods = []
                
    for element in step_no:
        x= step_no.get(element)
        if x[0] == True:
            true_methods.append(element)
    return true_methods

#used to fetch the estimators
def get_estimators():
    true_estimators = []
    method_obj =[]
    family = estimators.get(check())
    for i in family:
        x = family.get(i)
        if x[0] == True:
            true_estimators.append(i) 
    for elements in true_estimators:
        method = estimatorMethods[elements]
        method_obj.append((elements, GridSearchCV(method,estimator_params[elements])  ) )
    
    return method_obj
        
        
        
#This function creates a list containing the method string and the method to be called  as a part of the pipeline
def get_functions(step_string, step_no):
    true_methods = get_method_step(step_no)
    print true_methods
    method_obj = []
    for elements in true_methods:
        #print methodObj[step_string]
        model_from_name(step_string,elements)
        #print methodObj[step_string]
        method = methodObj[step_string][elements]
        method_obj.append((elements, method))
    return method_obj
    
def get_wrappers():
    val = wrapper_based[check()]
    lst = []
    for i in val:
        if val[i] == True:
            lst.append(i)
    #Apply SelectFromModel
    #for i in lst:
                
            
#get_features() returns a list of tuples wiht Feature Union    
def get_features():
    if check() == cla:
        tup = feature_combinations(classification_features)
    elif check() == reg:
        tup = feature_combinations(regression_features)
    print tup
    func_with_params = []
    if len(tup) == 0:
        return []
    if type(tup[0]) != tuple:
        lst = []
        for j,i in enumerate(tup):
            tup[j] = featureSelectiontoclass[i].set_params(**feature_params[i])
        for j,i in enumerate(tup):
            tup[j] = ('0',FTransform(i))
        for j,i in enumerate(tup):
            tup[j] = ('3',FeatureUnion([i]))
        return tup
    else:        
        for j,i in enumerate(tup):
            l1        = featureSelectiontoclass[i[0]].set_params(**feature_params[i[0]])
            l2        = featureSelectiontoclass[i[1]].set_params(**feature_params[i[1]])
            tup[j]    = [l1,l2]
        for j,i in enumerate(tup):
            tup[j][0] = ('0',FTransform(i[0]))
            tup[j][1] = ('1',FTransform(i[1]))
        for j,i in enumerate(tup):
            tup[j] = ('3' , FeatureUnion([i[0],i[1]]))
            
        return tup

class log_models(): 
    def __init__(self):
        self.dir = None
        self.stamp = "duplica"
        self.flag = 0
        self.path = None
        if check() == cla:
            if not os.path.exists("muclassify"):
                os.makedirs("muclassify")
            self.dir = "muclassify"
        elif check() == reg:
            if not os.path.exists("muregression"):
                os.makedirs("muregression")
            self.dir  = "muregression"
        elif check() == clu:
            if not os.path.exists("muclustering"):
                os.makedirs("muclustering")
            self.dir  = "muclustering"
        self.path  =  self.dir + "\\" +self.stamp
        #print self.stamp
        if not os.path.exists(self.path):
            os.makedirs(self.path)  
    def topickle(self,num,model):
        pickle.dump( model, open( str(self.path) +"\\" +check() + str(num) + ".p", "wb" ) )
    def unpickle(self,num):
        model = pickle.load(open( str(self.path) + "\\" +check() + str(num) + ".p", "rb" ) )
        return model
    def savedata(self,Xtrain,ytrain,Xtest,ytest):
        Xtrain.to_csv( self.path +  "\\"   + "Xtrain.csv")
        ytrain.to_csv( self.path  +  "\\"   + "ytrain.csv")
        Xtest.to_csv(  self.path  +  "\\"   + "Xtest.csv")
        ytest.to_csv(  self.path  +  "\\"   + "ytest.csv")
    def save_scores(self,score_dic):
        pickle.dump(score_dic,open(self.path  + "\\" + "scores.p","wb") )
    def rename(self,TIME):
        for retry in range(100):
            try:
                os.rename(self.path,self.dir+ "\\" + TIME)
                break
            except:
                print "rename failed, retrying..."
       
