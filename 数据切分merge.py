import pandas as pd

path = '/root/tad'
ad_feature = pd.read_csv(path + '/data/adFeature.csv')
train = pd.read_csv(path + '/data/train.csv')
train['label'] = train['label'].map({1: 1, -1: 0})
test1 = pd.read_csv(path + '/data/test1.csv')
test2 = pd.read_csv(path + '/data/test2.csv')
full = pd.concat([train, test1, test2])
# 68996077
full = pd.merge(full, ad_feature, 'left', 'aid')
userFeature_data = []
with open(path + '/data/userFeature.data', 'r') as f:
    for i, line in enumerate(f):
        line = line.strip().split('|')
        userFeature_dict = {}
        for each in line:
            each_list = each.split(' ')
            userFeature_dict[each_list[0]] = ' '.join(each_list[1:])
        userFeature_data.append(userFeature_dict)
        if i % 1000000 == 0 and i > 0:
            print(i)
            user_feature = pd.DataFrame(userFeature_data)
            user_feature.uid = user_feature.uid.astype(int)
            temp_full = pd.merge(full, user_feature, 'inner', 'uid')
            print('合并成功')
            temp_full.to_csv(path + '/data/train/train_' + str(int(i / 1000000)) + '.csv', index=False)
            print('保存成功')
            full = full[~full.uid.isin(user_feature.uid)]
            print('还剩下', len(full))
            userFeature_data = []

    print('finnal')
    user_feature = pd.DataFrame(userFeature_data)
    user_feature.uid = user_feature.uid.astype(int)
    temp_full = pd.merge(full, user_feature, 'inner', 'uid')
    temp_full.to_csv(path + '/data/train/train_final.csv', index=False)



train = pd.DataFrame()
test = pd.DataFrame()
for i in [str(i+1) for i in range(44)]+['final']:
    file = path+'/data/train/train_'+i+'.csv'
    print(file)
    temp_data = pd.read_csv(file)
    train = pd.concat([train,temp_data[temp_data.label.notnull()]])
    test = pd.concat([test,temp_data[temp_data.label.isnull()]])
    print(len(train),len(test))

train.to_csv(path+'/data/full_train.csv',index=False)
test.to_csv(path+'/data/full_test.csv',index=False)

