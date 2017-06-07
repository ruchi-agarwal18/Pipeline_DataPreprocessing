from itertools import  product


algo = {'Classification':True,'Regression' : False ,'Clustering' :False}

step0 = {'Impute': [True,{"missing_values" :'NaN', "strategy" : { 'mean' ,'median' , 'mode' } }]}

# --- Data Preprocessing --- #
step1 = {'None': [False], 'Recenter': [False], 'Standardize': [False],
         'Normalize': [True, {'norm': ['l2']}],
         'MinMax': [True, {'feature_range': [(0,1), (-1,1)]}]}
         
         
# --- Dimensionality Reduction --- #
step2 = {'PCA': [False, {'n_components': 5}],
         'IncrementalPCA': [False, {'n_components': 3}],
         'RandomizedPCA':  [False, {'n_components': 3}],
         'KernelPCA':      [False, {'n_components': 2,
                                    'kernel': ['linear','rbf','poly'], 'gamma': 2}],
         'Isomap': [False, {'n_components': 3, 'n_neighbors': 5}],
         'LLE':    [False, {'n_components': 3, 'n_neighbors': 5, 
                            'method': ['standard','modified','hessian','ltsa']}],
         'SE':   [False, {'n_components': 3, 'affinity': ['nearest_neighbors','rbf']}],
         'MDS':  [False, {'n_components': 3, 'metric': [True, False]}],
         'tSNE': [False, {'n_components': 3}],
         'RMB':  [False, {'n_components': 256}],
         'None': [False, {}]
         }
         
# --- Feature selection for classification --- #
classification_features = {
                            
                                     "continuos"  : { "f_reg" : True , "f_classif" :False },
                                    "categorical" : { "Chi_2" : True  }  
                            
        }
        
#--- Feature selection for regression ---#        
regression_features  =   {
                            
                                    "continuos"   :  {'f_reg' : True},
                                    "categorical" :  {"Chi_2" : False} 
                            
            }   
            
            
wrapper_based = { 
                   "Classification": { 
                          'RandomForestClassifier'     : True , 
                          'ExtraTreesClassifier'       : True , 
                          'GradientBoostingClassifier' : True ,
                          'AdaBoostClassifier'         : True
                   } , 
                   
                   "Regression" : {
                          'AdaBoostRegressor'          : True,
                          'ExtraTreesRegressor'        : True
                   }
            }            
            
            
            

estimators = {"Classification" :{ "Logistic Regression" : [ True], "Decision Trees" : [True]  , "svm" : [True]} ,
              
              "Regression" :{"Linear Regression" :[True], "Generalized Linear Regression" :[False], "Ridge" : [True]},
              "Clustering" :{ "k-means" : [False],"Heirarchial": [False]}
            }
                             


                    


#for metrics used for sorting  the pipelines 
class_metrics = {"models" :estimators["Classification"] ,"metrics" : {"accr":True ,"precision":True,"recall":True ,"f1-score":True,"AVC":False,"log loss":False} }
reg_metrics   = {"models" : estimators["Regression"]    ,"metrics" : {"accr" : True,"RMSE" : True,"MSE" : True}    }
clus_metrics  = {"models" : estimators["Clustering"]    ,"metrics" : {"adjusted_rand_score" : True,"BWSS" : True ,"homogeneity_score":True ,"mean square error" : True}   }

           
paramObj = {'step0': {'Impute':{"missing_values" :'NaN', "strategy" :'median', "axis" : 0}} ,
            'step1': {'Normalize': {"norm" : "l1"} , "MinMax" : {} },
            'step2':{'PCA': {"n_components" : 2}},
             }
estimator_params = {'Logistic Regression' : {'C': [0.001, 0.01]} ,
                    'svm' : {'kernel':('linear',), 'C':[0.1,1] } ,
                    'Decision Trees' : {}  ,
                    'Linear Regression' : {},
                    'Ridge'  : {'alpha' : [0.5,1]} ,
                    'Generalized Linear Regression' : {}   
                    
                    }
feature_params = {'f_reg' : {'k' : 1} , 'Chi_2' : {'k' : 1} , "f_classif" : {'k':1}   }

wrapper_params = { "Classification" : 
                                  {
                                    'RandomForestClassifier'     :  {'n_estimators' : 5} ,
                                    'ExtraTreesClassifier'       :  {'n_estimators' : 5}
                                 } ,
                     "Regression"  : 
                                 {
                                     'AdaBoostRegressor'        :   {}  
                                 }


                 }

cla  = "Classification"
reg  = "Regression"
clu  = "Clustering"
