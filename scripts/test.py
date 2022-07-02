import datetime
ts1= 1655741049.438984




def checkTime(tsPrev):
    
    t2 = datetime.datetime.fromtimestamp(tsPrev)
    t1 = datetime.datetime.now()
    
    return([(t1-t2).seconds,(t1-t2).days])

x = checkTime(ts1)
print(x[0]/60)
print(x[1] )