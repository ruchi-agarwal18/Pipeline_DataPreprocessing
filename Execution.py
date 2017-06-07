from __future__ import division
import itertools
from sklearn.metrics import classification_report
import multiprocessing
import pickle
from sklearn.metrics import accuracy_score,mean_squared_error,r2_score
from sklearn.pipeline import Pipeline


#-------------------custom libraries---------------------------------#
from UserDataFunctions import *
from UserInterface import *

time = str(datetime.datetime.now()).replace(':','..')

def timer():
    return time

#Used for running classification pipelines parallely
def classification_evaluator(num,pipeline,train,target,data_test,y_true,target_names,queue):
    pipeline.fit(train,target)
    #print pipeline.named_steps['0'].transform(train)
    #print pipeline.predict(train)
    #print str(accuracy_score(pipeline.predict(train),target)) + "   " + str(num)
    store = log_models()
    #print pipeline
    store.topickle(num,pipeline)
    results = pipeline.predict(data_test)
    #print results
    accr = accuracy_score(results,y_true)
    df = classification_report(y_true, results, target_names=target_names)
    k = df.split()
    print str(accr)  + "   " + str(num)
    queue.put([num,accr,float(k[6]),float(k[7]),float(k[8])])

#used for running regression piplelines parallely
def regression_evaluator(num,pipeline,train,target,data_test,y_true,queue):
    model = pipeline.fit(train,target)
    store = log_models()
    store.topickle(num,model)
    results = model.predict(data_test)
    accr = r2_score(results,y_true)
    mse  = mean_squared_error(results,y_true)
    rmse = mse**0.5
    print str(rmse) + "   " + str(num)
    l = [accr,mse,rmse]
    queue.put(l)
    
    
def clustering_evaluator(num,pipeline,train,data_test,queue):
    model = pipeline.fit(train)
    store = log_models(timer())
    store.topickle(num,model)
    results = model.predict(data_test)
    
def convert_to_tuples(lst):
    listoftuples = []
    print lst
    for j,i in enumerate(lst):
        listoftuples.append( ( i[0] , DFTransform(i[1]) ) )
    return listoftuples
    #print l[0][1].fit_transform(a,b)    


#This method generates different combinations of pipelines possible
def generate_permutations():
    impute = get_functions("step0",step0)
    data_pre = get_functions("step1",step1)
    dim_red = get_functions("step2",step2)
    feature_sel = get_features()
    estimator = get_estimators()
    all_perms = None
    lst = [convert_to_tuples(impute),convert_to_tuples(data_pre),convert_to_tuples(dim_red),feature_sel,estimator]
    not_none = []
    for i in lst:
        if len(i) != 0:
            not_none.append(i)
    all_perms = list(itertools.product(*not_none))
    #print all_perms
    return all_perms


    
    
    
# This method constructs and executes all the pipelines

def get_pipelines(Xtrain,Xtest,ytrain = None,ytest = None):
    store = log_models()
    store.savedata(Xtrain,ytrain,Xtest,ytest)
    all_pipeline_combs = generate_permutations()
    #print all_pipeline_combs
    dic ={}
    train = Xtrain
    target = ytrain.values.ravel()
    y_true = ytest
    colname = ytrain.keys()[0]
    target_names = list(ytrain[colname].unique())
    for i in range(len(target_names)):
        target_names[i] = "class " + str(target_names[i])
    #print target_names
    queue = multiprocessing.Queue()
    for i in range(len(all_pipeline_combs)):
        element = all_pipeline_combs[i]
        pipeline_list = list(element)
        pipeline = Pipeline(steps= pipeline_list)
        p = None
        if check() == cla :
            p = multiprocessing.Process(target=classification_evaluator, args=(i,pipeline,train,target,Xtest,y_true,target_names,queue))
        elif check() == reg:
             p = multiprocessing.Process(target=regression_evaluator, args=(i,pipeline,train,target,Xtest,y_true,queue))
        elif check() == clu:
             p = multiprocessing.Process(target=clustering_evaluator, args=(i,pipeline,train,Xtest,queue))
        p.daemon = True
        p.start()
        #dic[i] = queue.get()
        #store.save_scores(dic)
        #print "hello" + str(i)
    for i in range(len(all_pipeline_combs)):
        dic[i] =  queue.get()
    return dic
    
    
def top_pipelines(dic):
    eval_metrics = metrics(check())
    resultdic = {"accr" : 1}
    if check() == cla:
        evaldic   = {"accr" : 0 , "precision" : 1, "recall" : 2, "f1-score" : 3 }
        for i in eval_metrics:
            n = sorted(dic.items(), key=lambda x: x[1][evaldic[i]])
            n.reverse()
            resultdic[i] = n[0][0]
    elif check() == reg:
        evaldic  = {"accr" : 0 , "MSE" : 1, "RMSE" : 2 }
        for i in eval_metrics:
            n = sorted(dic.items(), key=lambda x: x[1][evaldic[i]])
            n.reverse()
            resultdic[i] = n[0][0]
    for i in eval_metrics:
        print "Best According to " + str(i) + "  " + str(resultdic[i])
    return resultdic
    
def testcase(data):
    t = pd.DataFrame(np.array([data]))
    t.columns = a.columns
    #print t
    return t
    
if __name__ == "__main__":
    dic1 = get_pipelines(a,c,b,d)
#    res =  top_pipelines(dic1)
##    store = log_models()
##    k = timer()
##    store.rename(k)
#    num = raw_input("Enter The Pipeline Number::")
#    store = log_models()
#    model = store.unpickle(num)
##    print "model loaded"
#    print model
#    print ""
#    for i in model.named_steps:
#        print model.named_steps[i]
#    print ""
#    print "Original Data ::"
#    print a
#    print "1st step ::"
#    s0    =  model.named_steps['0'].transform(a)
#    print s0
#    print "2nd Step ::"
#    print model.named_steps['1'].transform(s0)
#    print "3rd Step"
#    print "features selected ::"
#    print model.named_steps['3'].get_feature_names() 
   
    
