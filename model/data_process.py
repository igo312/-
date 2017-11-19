# -- coding utf-8 --

Created on Sat Oct 28 161639 2017

@author ��ʤ��
��ĺ�����
�����Ѿ��賿������
ϣ�����ѵ�������кõĽ��
��Ȼȷʵ���ҷ��˺ܶ��
���������Ѫ��
����

from tqdm import tqdm
import pandas as pd
from datetime import datetime
from sklearn import preprocessing
import numpy as np
import os
# the optimizer we will use
import xgboost as xgb


LOAD = False


# Define the data path ��and read it
path = 'Gcustomer&fixed-position'
save_path = r'Gcustomer&fixed-positionxgb_model'
dis_path = r'Gcustomer&fixed-positiondatashopshop_dis'
sp_lc_path=r'Gcustomer&fixed-positiondatashopshop_lc'
df = pd.read_csv(path + 'trainperson-ccf_first_round_user_shop_behavior.csv')
shop = pd.read_csv(path + 'trainshop-ccf_first_round_shop_info.csv')
test = pd.read_csv(path + 'Btest-evaluation_public.csv')

# ���̳�����ӳ�䵽ѵ������
df = pd.merge(df, shop[['shop_id', 'mall_id']], how='left', on='shop_id')

# ��ѵ�����Ͳ��Ի��ϲ�
'''Q1 ����������ƽ��
   A1ʹ��ΪNaNֵ�洢'''
train = df

# ��ȡmall��������������֮����mallΪ��λ��ѵ��
mall_list = list(set(list(shop.mall_id)))

# ��������
result = pd.DataFrame()

# �������趨
drop_num = 115;
threshold = 20;
remain_num = 2

# �ų���ѵ���õ��̳�
mall_already=os.listdir(r'Gcustomer&fixed-positiondatatest_mall__')
mall_already=[mall.split('.')[0] for mall in mall_already]
mall_list=[mall for mall in mall_list if mall not in mall_already]
for ID, mall in enumerate(mall_list)
    print('��ȡ {} �̳�����'.format(mall))
    train1 = train[train.mall_id == mall].reset_index(drop=True)
    print('����train1��shapeΪ{}'.format(train1.shape))
    '''�����ǹ��ھ�γ�ȵĴ������þ��봦���һЩ�쳣ֵ
        ע��ĳЩ�̵��Ӧ��ѵ�����ر�С����ôȥ����ѵ����������Ҫ���ǵ�'''
    buff_df = 0
    # ��ȡ���е�shop
    shop_list = []
    shop_list.extend(list(shop[shop.mall_id == mall].shop_id.values))
    # ɾ����Ϊ���쳣ֵ
    for shop_name in shop_list
        sp_lc=np.load(sp_lc_path+shop_name+'.npy');sp_lg=sp_lc[0];sp_lt=sp_lc[1]
        dis_data = pd.read_csv(dis_path + shop_name + '.csv').reset_index()
        shop_train = train1[train1.shop_id == shop_name].reset_index(drop=True)
        shop_train = shop_train.reset_index()
        if type(buff_df) == int
            buff_df = pd.merge(shop_train, dis_data[['dis','index']],
                               how='left', on=['index'])
            buff_df = buff_df.sort_values(['dis'], ascending=False)
            # ���д���
            remain = buff_df[buff_df.dis  drop_num]
            delate = buff_df[buff_df.dis = drop_num]
            delate.longitude=sp_lg; delate.latitude=sp_lt
            for index in range(delate.shape[0])
                delate[indexindex+1].longitude += np.random.randn()120
                delate[indexindex+1].latitude += np.random.rand()150
            buff_df = pd.concat([remain,delate])
        else
            buff = pd.merge(shop_train, dis_data[['dis','index']],
                               how='left', on=['index'])
            buff = buff.sort_values(['dis'], ascending=False)
            remain = buff[buff.dis = drop_num]
            delate = buff[buff.dis = drop_num]
            delate.longitude=sp_lg; delate.latitude=sp_lt
            for index in range(delate.shape[0])
                delate[indexindex+1].longitude += np.random.randn()120
                delate[indexindex+1].latitude += np.random.rand()150
            buff = pd.concat([remain,delate])
            buff_df = pd.concat([buff_df, buff])
    print('����buff_df��shapeΪ{}'.format(buff_df.shape))
    train1 = pd.concat([buff_df, test[test.mall_id==mall]])

    # ����洢����
    l = [];
    wifi_remain = []
    wifi_dict = {}
    wifi_con_remain = []
    # ��һ��һ�е�˳���ȡ���ݡ�
    for index, row in tqdm(train1.iterrows())
        # ��������
        wifi_list = [wifi.split('') for wifi in row['wifi_infos'].split(';')]

        # �ж��Ƿ�����
        status = 0

        for i in wifi_list

            # ���ｫ���û�ԭ����Ϣ�Ļ����ϼ���
            # Ԫ����Ϊwifi���ƣ�Ԫ��ֵΪ�ź�ǿ�ȵ���Ϣ
            row[i[0]] = int(i[1])

            # ��¼wifi���ֵĴ���
            if i[0] not in wifi_dict
                wifi_dict[i[0]] = 1
            else
                wifi_dict[i[0]] += 1

            # �洢���ӵ�wifi�ź�
            if i[2] == 'true'
                wifi_con_remain.append(i[0])
                status = 1

        if status == 0
            wifi_con_remain.append('NONE')

        # ����wifi��Ϣ
        if len(wifi_list)  3
            wifi_remain.append('NONE')
        else
            sort_list = sorted(wifi_list, key=lambda wifi_infos int(wifi_infos[1]), reverse=True)
            save_wifi = sort_list[remain_num]
            wifi_remain.append(row[[wifi_name[0] for wifi_name in save_wifi]])

        # ��¼�µ��û�����
        l.append(row)

    '''Ŀ�ģ��ֱ������ֵ��wifi�źţ���Ϊû�����ã�'''
    # ���ѭ����ȡ���˵�����ֵ��wifi����
    delate_wifi = []
    for i in wifi_dict
        if wifi_dict[i]  threshold
            delate_wifi.append(i)

    # ���ѭ����ȡ���˸�����ֵ��wifi����
    # ���Դ��ж�ɸѡ�����û��е���Ϣ
    # ע��key���Ժ���λ�õȵ���Ϣ��ֻ���ų��˲���Ҫ��wifi�ź�
    m = []
    for index, row in enumerate(l)
        new = {}
        for n in row.keys()
            if n not in delate_wifi
                new[n] = row[n]

        # �����������wifi��Ϣ
        if type(wifi_remain[index] == 'NONE') == bool
            pass
        else
            remain_dict = dict(zip(wifi_remain[index].keys(), wifi_remain[index].values))
            for n in remain_dict.keys()
                new[n] = remain_dict[n]

                # ������ӵ�wifi������ֵ��������Ϊ����wifiû�д�������,��������ȫ������
            try
                if type(wifi_con_remain[index] == 'NONE') == bool
                    pass
                else
                    new[wifi_con_remain[index]] = -15
            except
                pass

        m.append(new)
    # ��ȡ��������̵��Ӧ�û����յ����ݼ�
    train1 = pd.DataFrame(m)

    # ��ȡѵ����
    df_train = train1[train1.shop_id.notnull()]
    # ��������õ�ѵ����
    train1.to_csv(r'Gcustomer&fixed-positiondatatest_mall__' + mall + '.csv')
    print('{} {}�̳����ݱ������'.format(datetime.now(), mall))
    # ��ȡ���Լ�
    df_test = train1[train1.shop_id.isnull()]
    # ��ȡ��ǩ
    '''  ���������ǽ��̵��ǩ���Ƶ��˶�Ӧ���̳���   '''
    lbl = preprocessing.LabelEncoder()
    lbl.fit(list(df_train['shop_id'].values))
    # ��ӱ�ǩ
    df_train['label'] = lbl.transform(list(df_train['shop_id'].values))
    # ��������
    num_class = df_train['label'].max() + 1

    # ���峬����
    # ��������ʹ���Ҳ����
    params = {
        'objective' 'multisoftmax',
        'min_child_weight' 2,
        'gamma' 0.25,
        'subsample' 0.82,
        'colsample_bytree' 0.7,
        'eta' 0.08,
        'max_depth' 4,
        'eval_metric' 'merror',
        'seed' 0,
        'missing' -999,
        'num_class' num_class,
        'scale_pos_weight' 0.8,
        'silent' 1,

    }

    # ��ȡ����wifi��λ��
    feature = [x for x in train1.columns if
               x not in ['user_id', 'label', 'shop_id', 'time_stamp', 'mall_id', 'wifi_infos', 'DATE', 'Unnamed 0']]

    # Ϊ��֮����ظ�ѵ�����������ȱ�������
    xgbtrain = xgb.DMatrix(df_train[feature], df_train['label'])
    xgbtest = xgb.DMatrix(df_test[feature])

    # ����ѵ�������������������һ������
    # df_train = noise_Add(df_train)


    '''��������ʹ��'''

    # ѵ������

    ''' Q2 ����ѵ�������ݵ�׼ȷ��ʽ
    A2��ѵ������Columns��������wifi�뾫��ά����ɵ����ݣ�
    ֵ��ע����ǣ�����wifi������ÿһ���û������У�����pd������ı����Զ���NaN����
    ���ڷ��������ǿ��Լ��ݵ�'''

    watchlist = [(xgbtrain, 'train'), (xgbtrain, 'test')]
    num_rounds = 140
    if LOAD
        model = xgb.Booster({'nthread' 4})
        model.load_model(save_path + '6')
        model.train(params, xgbtrain, num_rounds, watchlist, early_stopping_rounds=15)
    else
        model = xgb.train(params, xgbtrain, num_rounds, watchlist, early_stopping_rounds=6)
    # ����ģ��
    model.save_model(save_path + mall + '.model')

    # ���Բ���
    df_test['label'] = model.predict(xgbtest)
    df_test['shop_id'] = df_test['label'].apply(lambda x lbl.inverse_transform(int(x)))
    # ��¼���
    r = df_test[['row_id', 'shop_id']]
    result = pd.concat([result, r])
    result['row_id'] = result['row_id'].astype('int')
    result.to_csv(path + 'sub.csv', index=False)

