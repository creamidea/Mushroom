#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from head import *
from db_base import MssqlConnection
from db_env import *

class DbOperator(MssqlConnection):
    def __init__(self, serverIp = db_conn_info['HOST'], dbName = db_conn_info['DATABASE'], \
                 uid = db_conn_info['USER'], pwd = db_conn_info['PASSWORD']):
        MssqlConnection.__init__(self, serverIp, dbName, uid, pwd)

    def get_room_info(self, room_id):
        """
        通过Room ID获取房间信息
        
        :param room_id: 房间号
        :rtype: 待定
        {
            "roomId": room_id,
            "roomName": "房间1",
            "plantId": 1,
            "plantName": "蘑菇",
            "nowPolicy": 1,
        }
        """
        plant_dict = {}
        try:
            room_id = int(room_id)
        except Example:
            return -1
        self.connect()
        sql_str = u'''select top 1 tb_room.room_id, room_description, tb_plant.plant_id, plant_name, policy_id from 
                            tb_policy_instance left join tb_plant 
                            on tb_policy_instance.plant_id = tb_plant.plant_id, tb_room
                      where tb_policy_instance.policy_instance_id in (select distinct policy_instance_id from tb_absolute_time) 
                            and tb_room.room_id = %d and state >= %d''' %(room_id, POLICY_RUNNING)
        # 这里有一个问题，当用户向tb_policy_instance表中一次添加了多个（>=2）个同房间不同开始时间的policy_instance时，
        # 理论上是可以的，但这时就会有上述的查询返回多组，其中只有一组是正在执行的，其他的均为当前执行周期结束后才执行的新的周期。
        plant_room = self.queryAll(sql_str)
        self.close()
        try:
            plant_dict['roomId']    = plant_room[0][0]
            plant_dict['roomName']  = plant_room[0][1]
            plant_dict['plantId']   = plant_room[0][2]
            plant_dict['plantName'] = plant_room[0][3]
            plant_dict['nowPolicy'] = plant_room[0][4]
        except IndexError, e:
            print 'get nothing in room_id: %d' %room_id
        # plant_dict = [{
        #     "roomId": room_id,
        #     "roomName": "房间1",
        #     "plantId": 1,
        #     "plantName": "蘑菇",
        #     "nowPolicy": 1,
        # }]
        return plant_dict
    # TODO: 2014-03-30不能使用
    def get_all_room(self):
        """
        获取所有房间的最新基础信息
        :rtype:
        [{
            "roomId": room_id,
            "roomName": "房间1",
            "plantId": 1,
            "plantName": "蘑菇",
            "nowPolicy": 1,
        }, ...]
        """
        sql_str = '''
                select room_id from tb_room
                '''
        self.connect() 
        room_list = self.queryAll(sql_str)
        self.close()
        all_room_info = []
        for i in room_list:
            all_room_info.append(self.get_room_info(i[0]))
            
        # all_room_info = [{
        #     "roomId": 1,
        #     "roomName": "房间1",
        #     "plantId": 1,
        #     "plantName": "蘑菇",
        #     "nowPolicy": 1,
        #     },
        #     {
        #     "roomId": 2,
        #     "roomName": "房间2",
        #     "plantId": 2,
        #     "plantName": "蘑菇",
        #     "nowPolicy": 1,
        #     },
        #     {
        #     "roomId": 3,
        #     "roomName": "房间3",
        #     "plantId": 3,
        #     "plantName": "蘑菇",
        #     "nowPolicy": 1,
        #     }
        #     ]
        # print ">>>", all_room_info
        # all_room_info = all_room_info[0]
        return all_room_info

    def get_room_controllers(self, room_id):
        """
        获取房间的所有控制器信息
        """
        sql_str = u'''
        select controller_type, controller_id, state from tb_controller where room_id = %d
        ''' % int(room_id)
        self.connect()
        data = self.queryAll(sql_str)
        self.close()
        print data
        result = {}
        for item in data:
            # 这里注意一下：1为开启，0为关闭
            temp = dict(cid=item[1], state=item[2])
            # if not result.has_key(item[0]):
            #     result[item[0]] = []
            # TODO: 修正这里，不需要数组，直接字典
            result[item[0]] = temp
        return result

    def get_room_sensors(self, room_id):
        """
        获取房间的所有传感器信息
        """

        sql_str = u'''
        select sensor_type, sensor_id, position from tb_sensor where room_id=%d
        ''' % int(room_id)
        self.connect()
        data = self.queryAll(sql_str)
        self.close()
        result = {}
        for item in data:
            temp = dict(sid=item[1], position=item[2])
            if not result.has_key(item[0]):
                result[item[0]] = []
            result[item[0]].append(temp)
        
        return result
    def delete_plant(self, plant_name):
        return (0, None)
    def update_plant(self, plant_id, new_name):
        return (0, None)

    def get_latest_data(self, room_id):
        sql_str = "SELECT top 1 instance_id, sense_time, room_id FROM tb_instance WHERE room_id = %d ORDER BY instance_id DESC " %(room_id)
        self.connect()
        result = self.queryAll(sql_str)
        try:
            instance_id = result[0][0]
            sense_time  = result[0][1].strftime('%Y/%m/%d %H:%M:%S')
        except IndexError, e:
            return -1
        else:
        
            sql_str = '''select tb_data.sensor_id, data, sensor_type from tb_data left join tb_sensor
                        on tb_sensor.sensor_id = tb_data.sensor_id
                    where instance_id = %d''' %instance_id
            result = self.queryAll(sql_str)
        finally:
            self.close()
        if len(result) < 1:
            return -1
        json_inst = {'instance_id'  : instance_id,
                     'sense_time'   : sense_time,
                     'room_id'      : room_id,
                     'sense_data'   :{
                                      'temperature' : [],
                                      'humidity'    : [],
                                      'co2'         : [],
                                      'light'       : [],
                                      }
                    }
        
        for one_row in result:
            sensor_type = one_row[2]
            sensor_id   = one_row[0]
            data        = one_row[1]
            
            json_inst['sense_data'][sensor_type].append({'id': sensor_id, 'data': data})
        
        return json_inst
    
    def get_time_range_data(self, room_id, start_time, end_time):
        """
        获取指定房间的指定范围环境信息（采集值）
        
        :param room_id: 房间号
        :param start_time: 开始时间
        :param end_time: 结束时间
        :rtype: 指定时间段的数据队列
        [
        {
            "sensorId": 1,
            "sensorType": "temperature",
            "position": "上1",
            "values":
            (
                ("2014/01/08 21:08", 100),
                ("2014/01/08 21:09", 200),
                ("2014/01/08 21:15", 300),
                ("2014/01/08 22:15", 300),
            )
        },
        ...
        ]
        """
        sql_str = u'''
                    SELECT tb_temp.sensor_id, tb_sensor.sensor_type, position, sense_time, data
                    FROM (SELECT sensor_id, sense_time, data 
                          FROM tb_instance
                          LEFT JOIN tb_data ON tb_instance.instance_id = tb_data.instance_id
                          WHERE sense_time >= '%s' AND sense_time < '%s' AND room_id = %d) AS tb_temp
                    LEFT JOIN tb_sensor ON tb_temp.sensor_id = tb_sensor.sensor_id
                    ORDER BY sensor_id, sense_time
                    ''' % (start_time, end_time, room_id)
        self.connect()
        data = self.queryAll(sql_str)
        self.close()
        temp_dict = {}
        for i in data:
            time = i[3].strftime('%Y/%m/%d %H:%M:%S')
            if temp_dict.has_key(i[0]):
                temp_dict[i[0]]['values'].append((time, i[4]))
            else:
                temp = {}
                temp['sensorId'] = i[0]
                temp['sensorType'] = i[1]
                temp['position'] = i[2]
                temp['values'] = [(time, i[4])]
                temp_dict[i[0]] = temp
        data_list = []
        for v in temp_dict.itervalues():
            v['values'] = tuple(v['values'])
            data_list.append(v)
        # print "[in db/db_operator]: ", data_list
 
        # data_list = [
        # {
        #     "sensorId": 1,
        #     "sensorType": "temperature",
        #     "position": "上1",
        #     "values":
        #     (
        #         ("2014/01/08 21:08", 100),
        #         ("2014/01/08 21:09", 200),
        #         ("2014/01/08 21:15", 300),
        #        ("2014/01/08 22:15", 300),

        #     )
        # },
        # {
        #     "sensorId": 2,
        #     "sensorType": "temperature",
        #     "position": "上2",
        #     "values":
        #     (
        #         ("2014/01/08 21:08", 410),
        #         ("2014/01/08 21:09", 320),
        #         ("2014/01/08 21:15", 134),

        #     )
        # },
        # {
        #     "sensorId": 5,
        #     "sensorType": "temperature",
        #     "position": "上2",
        #     "values":
        #     (
        #         ("2014/01/08 21:08", 100),
        #         ("2014/01/08 21:09", 200),
        #         ("2014/01/08 21:15", 134),
        #         ("2014/01/08 21:22", 140),
        #         ("2014/01/08 21:34", 112),
        #         ("2014/01/08 21:45", 234),
        #         ("2014/01/08 21:56", 243),
        #         ("2014/01/08 22:01", 324),

        #     )
        # },
        # {
        #     "sensorId": 3,
        #     "ensorType": "humidity",
        #     "position": "上2",
        #     "values":
        #     (
        #         ("2014/01/08 21:08", 400),
        #         ("2014/01/08 21:09", 500),
        #         ("2014/01/08 21:15", 100),
        #     )
        # },
        # ]

        return data_list
    
    
    def certain_sensor_time_range_data(self, sensor_id, start_time, end_time):
        sql_str = '''
                    select sense_time, position, sensor_type, data from
                        tb_data left join tb_instance on tb_data.instance_id = tb_instance.instance_id --as tb_temp
                        left join tb_sensor on tb_sensor.sensor_id = tb_data.sensor_id
                    where tb_data.sensor_id = %d and sense_time >= '%s' and sense_time <= '%s'
                    ''' %(sensor_id, start_time, end_time)

        self.connect()
        result = self.queryAll(sql_str)
        self.close()
        json_inst = {
                      "sensorId": sensor_id,
                      "sensorType": "",
                      "position": "",
                      "values":[],

                     }

        for one_row in result:
            sense_time  = one_row[0].strftime('%Y/%m/%d %H:%M:%S')
            position    = one_row[1]
            sensor_type = one_row[2]
            data        = one_row[3]

            json_inst['sensorType'] = sensor_type
            json_inst['position']   = position
            json_inst['values'].append((sense_time, data))

        json_inst['values'] = tuple(json_inst['values'])
        return json_inst
    
    def update_room_name(self, room_id, room_description):
        """
        修改房间名称
        
        :param room_id: 房间号
        :param room_description: 房间描述
        :rtype: 修改结果，code: 0 成功， -1 失败
        """

        sql_str = u'''
                    update tb_room
                    set room_description = '%s'
                    where room_id = %d
                ''' %(room_description, room_id)
        self.connect()
        self.executeDML(sql_str)
        self.close()
        result = {}
        result['code'] = 0
        result['definition'] = ''
        return result
    
    def update_plant_info(self, plant_id, plant_name):
        """
        修改植物名称
        
        :param plant_id: 植物编号
        :param plant_name: 植物名
        :rtype: 修改结果，code: 0 成功， -1 失败
        """
        sql_str = u'''
                    update tb_plant
                    set plant_name = '%s'
                    where plant_id = %d
                    ''' %(plant_name, plant_id)
        self.connect()
        self.executeDML(sql_str)
        self.close()
        self.load_table()
        return {'code': 0, 'definition': ''}
    
    def all_policy_info(self):
        """
        获取养殖模式简要信息
        
        :rtype: 所有养殖策略简要信息
        """
        sql_str = u'''
            select policy_id, description from tb_policy
            '''
        self.connect()
        temp_list = self.queryAll(sql_str)
        self.close()
        policy_list = []
        for i in temp_list:
            policy_list.append({'policyId':i[0], 'description': i[1]})
        return policy_list
    
    def get_policy_2_bk(self, policy_id):
        """
        获取指定策略的部分信息
        
        :param policy_id: 策略号
        :rtype: 指定格式的策略信息
        """
        policy_info = self.get_policy(policy_id)
        policy_info['rules'] = policy_info['policy']
        policy_info.pop('policy')
        
        policy_info['now']  = -1
        policy_info['old']  = []
        policy_info['plan'] = []
        
        self.connect()
        sql_str = " select policy_instance_id from tb_policy_instance where policy_id = %d and state = %d " %(policy_id, POLICY_RUNNING)
        now_instance_id = self.queryAll(sql_str)[0][0] 
        policy_info['now'] = now_instance_id
        
        sql_str = " select policy_instance_id from tb_policy_instance where policy_id = %d and state = %d " %(policy_id, POLICY_NEW)
        plan_instance_id_list = self.queryAll(sql_str)
        for instance in plan_instance_id_list:
            policy_info['plan'].append(instance[0])
            
        sql_str = " select policy_instance_id from tb_policy_instance where policy_id = %d and state = %d " %(policy_id, POLICY_OLD)
        old_instance_id_list= self.queryAll(sql_str) 
        for instance in old_instance_id_list:
            policy_info['old'].append(instance[0])
        
        return policy_info
    def get_policy_2_bk2(self, policy_id):
        """
        获取指定策略的部分信息
        
        :param policy_id: 策略号
        :rtype: 指定格式的策略信息,失败返回 FAI
        """
        policy_info = self.get_policy(policy_id)
        policy_info['rules'] = policy_info['policy']
        policy_info.pop('policy')
        
        policy_info['now']  = []
        policy_info['old']  = []
        policy_info['plan'] = []
        
        self.connect()
        try:
            sql_str = " select policy_instance_id from tb_policy_instance where policy_id = %d and state = %d " %(policy_id, POLICY_RUNNING)
        
            now_instance_id = self.queryAll(sql_str)
            policy_info['now'] = now_instance_id[0][0]
        except IndexError:
            pass
                
        try: 
            sql_str = " select policy_instance_id from tb_policy_instance where policy_id = %d and state = %d " %(policy_id, POLICY_NEW)
            plan_instance_id_list = self.queryAll(sql_str)
            for instance in plan_instance_id_list:
                policy_info['plan'].append(instance[0])
        except IndexError:
            pass
        
        try: 
            sql_str = " select policy_instance_id from tb_policy_instance where policy_id = %d and state = %d " %(policy_id, POLICY_OLD)
            old_instance_id_list= self.queryAll(sql_str) 
            for instance in old_instance_id_list:
                policy_info['old'].append(instance[0])
            return policy_info
        except IndexError:
            return FAI

    def get_policy(self, policy_id):
        """
        获取指定养殖模式的全部信息
        
        :param policy_id: 策略号
        :rtype: 指定养殖模式的详细信息
        """
        sql_str = u'''
                select description, interval_date, hours, 
                temperature_peak, temperature_valle, humidity_peak, humidity_valle,
                co2_peak, co2_valle, reserved1_peak, reserved1_valle  
                from tb_rule left join tb_policy 
                on tb_rule.policy_id = tb_policy.policy_id
                where tb_policy.policy_id = %d 
                ''' %(policy_id)
        self.connect()
        temp_list = self.queryAll(sql_str)
        self.close()
        policy_info = {}
        policy_info['policyId'] = policy_id
        policy_info['policy'] = []
        try:
            policy_info['description'] = temp_list[0][0]
        except IndexError, e:
            policy_info['description'] = ''
            return policy_info
            
        for i in temp_list:
            temp = {}
            temp['date']        = i[1]
            temp['hour']        = i[2]
            temp['temperature'] = (i[3], i[4])
            temp['humidity']    = (i[5], i[6])
            temp['co2']         = (i[7], i[8])
            temp['brightness']  = (i[9], i[10])
            temp['light']       = ''
            policy_info['policy'].append(temp)
            
        return policy_info 

    def current_policy(self, room_id):
        """
        获取正在执行的养殖策略
        
        :param room_id: 房间号
        :rtype: 指定房间的当前养殖模式的详细信息
        """
        sql_str = u'''
                    select change_time, 
                            temperature_peak, temperature_valle, 
                            humidity_peak, humidity_valle, 
                            co2_peak, co2_valle, 
                            reserved1_peak, reserved1_valle, light_color,
                            tb_policy.policy_id, tb_policy.description, vw_task.policy_instance_id
                    from vw_task left join tb_policy_instance on vw_task.policy_instance_id = tb_policy_instance.policy_instance_id
                        left join tb_policy on tb_policy_instance.policy_id = tb_policy.policy_id
                    where vw_task.room_id = %d
                    ''' %(room_id)
        self.connect()
        temp_list = self.queryAll(sql_str)
        self.close()
        rule_list = []
        for i in temp_list:
            temp = {}
            temp['changeTime']        = i[0].strftime('%Y/%m/%d %H:%M:%S')
            temp['temperature'] = (i[1], i[2])
            temp['humidity']    = (i[3], i[4])
            temp['co2']         = (i[5], i[6])
            temp['brightness']  = (i[7], i[8])
            temp['lightColor']       = ''
            rule_list.append(temp)
            
        current_policy = {'pid': temp_list[0][10],
                  'description' : temp_list[0][11],
                  'now': '2014/04/20 22:02:00',
                  'rules': rule_list,
                  }
            
        return current_policy
    
    def new_policy(self, description, rules):
        """
        创建新策略
        :param description: 策略描述，长度限制  <20字符
        :rtype: 成功返回新建的策略号， 失败返回 -1
        """
        
        if len(description) > 20:
            log_msg = 'description is too long, please make sure the lenght less than 20'
            print 
            return -1
        sql_str = u"insert into tb_policy(description) values('%s')" %(description)
        try:
            self.connect()
            self.executeDML(sql_str)
            sql_str = "select top 1 policy_id from tb_policy where description = '%s' order by policy_id desc" %(description)
            policy_id = self.queryAll(sql_str)[0][0]
            self.close()
            
            if len(rules) > 0:
                self.create_rule(policy_id, rules)
                
            return (0, policy_id)
        except KeyboardInterrupt, e:
            print e
            return (-1, ERR)
    
    def new_policy_instance(self, policy_id, plant_name, room_desc, start_time):
        """
        创建新的策略实例
        
        :param policy_id: 策略号
        :param plant_name: 名称
        :param room_desc: 房间描述
        :param start_time: 开始执行时间,格式要求： 2013-12-17 15:45:00 （格式受限于SQLServer）
        :rtype: 成功返回新建的实例号，失败返回-1
        """
        self.connect()
        # print policy_id, plant_name, room_desc, start_time, '================'
        try:
            plant_id = self.plant_name2id[plant_name]
        except KeyError:
            self.executeDML("insert into tb_plant(plant_name) values('%s')" %(plant_name))
            self.load_table()
            plant_id = self.plant_name2id[plant_name]
        finally:
            self.close()
        
        self.connect()
        try:
            room_id = self.room_desc2id[room_desc]
        except KeyError, e:
            # 不允许新建房间
            print e
            return (-1, str(e))
            # self.executeDML("insert into tb_room(room_description) values('%s')" %(room_desc))
            # self.load_table()
            # room_id = self.room_desc2id[room_desc]
        finally:
            self.close()
        print policy_id, plant_id, room_id, start_time
        self.connect()
        try:
            sql_str = '''insert into tb_policy_instance(policy_id, plant_id, room_id, start_time, state) 
                        values(%d, %d, %d, '%s', %d)''' %(policy_id, plant_id, room_id, start_time, POLICY_NEW)
            self.executeDML(sql_str)
            instance_id = self.queryAll('''SELECT TOP 1 policy_instance_id \
                                           FROM tb_policy_instance \
                                           WHERE policy_id = %d \
                                           ORDER BY policy_instance_id DESC''' %(policy_id))[0][0]
        except Exception, e:
            print 'in create_policy_instance: '
            print e
            return (-1, str(e))
        else:
            return (0, instance_id)
        finally:
            self.close()

    def new_policy_instance_bk(self, params):
        """
        新建全新养殖模式
        
        :param params: 封装了新建策略必须的信息的字典
        :rtype: 新建结果，code: 0 成功， -1 失败
        """
        print ">>>>", params
        policy_id = self.create_policy(params['description'])
#         print 'policy_id = %d' %policy_id
        instance_id = self.create_policy_instance(policy_id, params['plantName'], params['roomId'], params['startAt'])
#         print 'instance_id = %d ' %instance_id
        # for i in range(len(params['policy'])):
        result = None
        for item in params['policy']:
            result = self.create_rule(policy_id, \
                         int(item['date']), \
                         int(item['hour']),\
                         item['temperature'][1], \
                         item['temperature'][0],\
                         item['humidity'][1] ,\
                         item['humidity'][0], \
                         item['co2'][1], \
                         item['co2'][0], \
                         item['brightness'][1], \
                         item['brightness'][0], \
                         item['light'])
#         print 'result = %d' %result
        if policy_id >= 0 and instance_id >= 0 and result >= 0:
            return {'code': 0, 'definition': 'Successful'}, policy_id
        else:
            #TODO: 具体出错位置
            return {'code': -1, 'definition': 'Failed'}

    
    def update_policy_desc(self, policy_id, description):
        """
        修改现存policy的名称
        
        :param policy_id: 待修改的策略号
        :param description: 策略描述
        :rtype: 修改结果，code: 0 成功， -1 失败
        """
        sql_str = '''update tb_policy 
                      set description = '%s' 
                      where policy_id = %d
                      ''' %(description, policy_id)
        self.connect()
        self.executeDML(sql_str)
        self.close()
        return {'code': 0, 'definition': 'Successful'}
    
    def delete_policy(self, policy_id):
        """
        删除指定policy
        
        :param policy_id: 策略号
        :rtype: 删除结果， code: 0 成功， -1 失败
        """
        self.connect()
#         self.executeDML(u"select policy_instance_id from ")
#         self.executeDML(u'delete from tb_policy_instance where policy_id = %d' %(policy_id))
#         self.executeDML(u'delete from tb_rule where policy_id = %d' %(policy_id))
        self.executeDML(u'delete from tb_policy where policy_id = %d' %(policy_id))
        self.close()
        return {'code': 0, 'definition': 'Successful'}


    # =========================================
    def get_room_policy(self, room_id):
        data = [
            {'policyId': 1, 'description': 'hhh'},
            {'policyId': 2, 'description': 'aaa'},
        ]
        return data

    # 这个接口在做下修改，直接替换就可以了
    def get_policy_2(self, policy_id):
        """
        获取指定策略的部分信息
        
        :param policy_id: 策略号
        :rtype: 指定格式的策略信息,失败返回 FAI
        """
        policy_info = self.get_policy(policy_id)
        policy_info['rules'] = policy_info['policy']
        policy_info.pop('policy')
        
        policy_info['now']  = []
        policy_info['old']  = []
        policy_info['plan'] = []
        
        self.connect()
        try:
            sql_str = " select policy_instance_id from tb_policy_instance where policy_id = %d and state = %d" %(policy_id, POLICY_RUNNING)
        
            now_instance_list = self.queryAll(sql_str)
            for one_instance in now_instance_list:
                policy_info['now'].append(one_instance[0])
        except IndexError:
            pass
                
        try: 
            sql_str = " select policy_instance_id from tb_policy_instance where policy_id = %d and state = %d " %(policy_id, POLICY_NEW)
            plan_instance_id_list = self.queryAll(sql_str)
            for instance in plan_instance_id_list:
                policy_info['plan'].append(instance[0])
        except IndexError:
            pass
        
        try: 
            sql_str = " select policy_instance_id from tb_policy_instance where policy_id = %d and state = %d " %(policy_id, POLICY_OLD)
            old_instance_id_list= self.queryAll(sql_str) 
            for instance in old_instance_id_list:
                policy_info['old'].append(instance[0])
            return policy_info
        except IndexError:
            return FAI


    # 这个函数我改了下，通过policy查我觉得无意义，应为同一个policy同时可以在多个房间里执行，
    # 这样按照你之前的格式查出来的数据其实无意义（多个房间的相同策略的多个rule混杂在一起，但却有不同的now）
    # 而且完全可以通过 get_policy_2 加 get_policy_instance_now 两步实现同样的效果
    def get_policy_instance_now_temp(self, room_id = None):
        """
        获取中正在执行的实例
        
        :param room_id: 
        :rtype: 指定养殖模式的详细信息,失败返回FAI
        """
        try:
            sql_str = u'''
                    select change_time, 
                            temperature_peak, temperature_valle, 
                            humidity_peak, humidity_valle, 
                            co2_peak, co2_valle, 
                            reserved1_peak, reserved1_valle, light_color
                    from vw_task 
                    where vw_task.room_id = %d
                    order by change_time
                    ''' %(room_id)
            self.connect()
            temp_list = self.queryAll(sql_str)
            self.close()
            rule_list = []
            current_instance = {'now': '',
                              'rules': rule_list,
                              }
            current_rule_time = ''
            for i in temp_list:
                temp = {}
                temp['changeTime']  = i[0].strftime('%Y/%m/%d %H:%M:%S')
                temp['temperature'] = (i[1], i[2])
                temp['humidity']    = (i[3], i[4])
                temp['co2']         = (i[5], i[6])
                temp['brightness']  = (i[7], i[8])
                temp['light']       = ''
                rule_list.append(temp)
                if i[0] <= datetime.now():
                    current_rule_time = temp['changeTime']
            current_instance['now'] = current_rule_time
            return current_instance
        except Exception:
            return FAI
        
    def get_policy_instance_now(self, policy_id = None, room_id = None):
        """
        获取中正在执行的实例
        
        :param policy_id:
        :param room_id: 
        :rtype: 指定养殖模式的详细信息,失败返回FAI
        """

        if policy_id != None:
            
            sql_str = u'''
                    SELECT change_time,
                        temperature_peak, temperature_valle, 
                        humidity_peak, humidity_valle,
                        co2_peak, co2_valle,
                        reserved1_peak, reserved1_valle, 
                        light_color, policy_id, room_id
                    FROM vw_task
                    WHERE vw_task.policy_id = %d
                    ORDER BY change_time
                    ''' % (policy_id)
            
            self.connect()
            temp_list = self.queryAll(sql_str)
            self.close()
            if temp_list == ERR:
                return (-1, u"数据库语句执行失败")
            the_end = {}
            for i in temp_list:                
                policy_id           = i[10]
                room_id             = i[11]
                if the_end.has_key(room_id):
                    pass
                else:
                    the_end[room_id] = {
                        'roomId' : room_id,
                        'roomDesc' : self.room_id2desc[room_id],
                        'policy_id' : policy_id,
                        'now' : '',
                        'rules' : []
                    }
            for i in temp_list:
                temp = {}
                temp['changeTime']  = i[0].strftime('%Y/%m/%d %H:%M:%S')
                temp['temperature'] = (i[1], i[2])
                temp['humidity']    = (i[3], i[4])
                temp['co2']         = (i[5], i[6])
                temp['brightness']  = (i[7], i[8])
                temp['light']       = ''
                room_id             = i[11]
                the_end[room_id]['rules'].append(temp)
                
                if i[0] <= datetime.now():
                    the_end[room_id]['now'] = temp['changeTime']
                    
            end_list = [] 
            for key in the_end.keys():
                end_list.append(the_end[key])
            code = 0
            data = end_list
        
        elif room_id != None:
            sql_str = u'''
                    SELECT change_time,
                        temperature_peak, temperature_valle, 
                        humidity_peak, humidity_valle,
                        co2_peak, co2_valle,
                        reserved1_peak, reserved1_valle, 
                        light_color, policy_id, room_id
                    FROM vw_task
                    WHERE vw_task.room_id = %d
                    ORDER BY change_time
                    ''' %(room_id)
            self.connect()
            temp_list = self.queryAll(sql_str)
            self.close()
            
            rule_list = []
            current_instance = {
                'roomId' : room_id,
                'roomDesc' : self.room_id2desc[room_id],
                'now': '',
                'rules': rule_list,
            }
            current_rule_time = ''
            policy_id = -1
            for i in temp_list:
                temp = {}
                temp['changeTime']  = i[0].strftime('%Y/%m/%d %H:%M:%S')
                temp['temperature'] = (i[1], i[2])
                temp['humidity']    = (i[3], i[4])
                temp['co2']         = (i[5], i[6])
                temp['brightness']  = (i[7], i[8])
                temp['light']       = ''
                policy_id           = i[10]
                rule_list.append(temp)
                if i[0] <= datetime.now():
                    current_rule_time = temp['changeTime']
            current_instance['policyId'] = policy_id
            current_instance['now'] = current_rule_time
            code = 0
            data = [current_instance]
        else:
            code = -1
            f = sys.exc_info()[2].tb_frame.f_back
            data = "%s:%s" % (f.f_lineno, f.f_code.co_name)
            
        return (code, data)

    def get_policy_instance_now_bk(self, policy_id=None, room_id=None):
        data = [{
            "roomId": 1,
            "roomDesc": "hhh2222",
            "policyId": policy_id or 0,
            "now": "2014/04/19 14:08",
            "rules": [
                {"changeTime": "2014/04/19 14:08", "co2":(1,2), "temperature": (2,1), "humidity": (3,2), "brightness": (4,5)},
                {"changeTime": "2014/04/20 14:08", "co2":(1,2), "temperature": (2,1), "humidity": (3,2), "brightness": (4,5)},
                {"changeTime": "2014/04/21 14:08", "co2":(1,2), "temperature": (2,1), "humidity": (3,2), "brightness": (4,5)},
                {"changeTime": "2014/04/22 14:08", "co2":(1,2), "temperature": (2,1), "humidity": (3,2), "brightness": (4,5)},
                {"changeTime": "2014/04/23 14:08", "co2":(1,2), "temperature": (2,1), "humidity": (3,2), "brightness": (4,5)},
                {"changeTime": "2014/04/24 14:08", "co2":(1,2), "temperature": (2,1), "humidity": (3,2), "brightness": (4,5)},
            ]
        },
        {
            "roomId": 2,
            "roomDesc": "hhh",
            "policyId": policy_id or 0,
            "now": "2014/04/19 14:08",
            "rules": [
                {"changeTime": "2014/04/19 14:08", "co2":(1,2), "temperature": (2,1), "humidity": (3,2), "brightness": (4,5)},
                {"changeTime": "2014/04/20 14:08", "co2":(1,2), "temperature": (2,1), "humidity": (3,2), "brightness": (4,5)},
                {"changeTime": "2014/04/21 14:08", "co2":(1,2), "temperature": (2,1), "humidity": (3,2), "brightness": (4,5)},
                {"changeTime": "2014/04/22 14:08", "co2":(1,2), "temperature": (2,1), "humidity": (3,2), "brightness": (4,5)},
                {"changeTime": "2014/04/23 14:08", "co2":(1,2), "temperature": (2,1), "humidity": (3,2), "brightness": (4,5)},
                {"changeTime": "2014/04/24 14:08", "co2":(1,2), "temperature": (2,1), "humidity": (3,2), "brightness": (4,5)},
            ]
        }, 
        ]
        return data
    
    def get_policy_instance_plan_list(self, policy_id):
        """
        获取计划中的实例
        
        :param policy_id: 策略号
        :rtype: 指定格式的数据
        """
        instance_info = []
        
        sql_str = '''SELECT policy_instance_id, room_id, start_time, plant_id
                     FROM tb_policy_instance
                     WHERE policy_id = %d AND state = %d''' % (policy_id, POLICY_NEW)
        self.connect()
        instance_list = self.queryAll(sql_str)
        for one_instance in instance_list:
            temp_instance = {}
            temp_instance['policyInstanceId'] = one_instance[0]
            temp_instance['roomDesc'] = self.room_id2desc[one_instance[1]]
            temp_instance['startAt'] = one_instance[2].strftime('%Y/%m/%d %H:%M')
            temp_instance['plantName'] = self.plant_id2name[one_instance[3]]
            instance_info.append(temp_instance)
        self.close()
        return (0, instance_info)
    def get_policy_instance_plan_list_bk(self, policy_id):
        data = [
            {"policyInstanceId": 1, "roomDesc": "end", "plantName": "test", "startAt": "2014/04/13 22:12"},
            {"policyInstanceId": 2, "roomDesc": "end", "plantName": "test2", "startAt": "2014/04/15 22:12"},
        ]
        return data

    def get_policy_instance_done_list(self, policy_id):
        """
        获取执行过的实例
        
        :param policy_id: 策略号
        :rtype: 指定格式的数据
        """
        instance_info = []
        sql_str = ''' select policy_instance_id, room_id, start_time, plant_id from tb_policy_instance 
                        where policy_id = %d and state = %d ''' %(policy_id, POLICY_OLD)
        self.connect()
        instance_list = self.queryAll(sql_str)
        for one_instance in instance_list:
            temp_instance = {}
            temp_instance['policyInstanceId'] = one_instance[0]
            temp_instance['roomDesc'] = self.room_id2desc[one_instance[1]]
            temp_instance['startAt'] = one_instance[2].strftime('%Y/%m/%d %H:%M')
            temp_instance['plantName'] = self.plant_id2name[one_instance[3]]
            instance_info.append(temp_instance)
        self.close()
        return (0, instance_info)
    def get_policy_instance_done_list_bk(self, policy_id):
        data = [
            {"policyInstanceId": 1, "roomDesc": "end", "plantName": "test", "startAt": "2014/04/13 22:12"},
            {"policyInstanceId": 2, "roomDesc": "end", "plantName": "test2", "startAt": "2014/04/15 22:12"},
        ]
        return data

    def delete_policy_instance(self, policy_instance_id):
        sql_str = 'delete from tb_policy_instance where policy_instance_id = %d' %(policy_instance_id)
        self.connect()
        self.executeDML(sql_str)
        self.close()
        return SUC

    def update_policy_instance(self, policy_instance_id, room_desc, plant_name, start_time):
        """
        更改策略实例信息
        
        :param policy_instance_id: 实例号
        :param room_desc: 房间描述
        :param plant_name: 植物名称
        :param start_time: 开始执行时间
        :rtype: SUC 成功， FAI 失败， ERR 异常
        """
        policy_instance_id = int(policy_instance_id)
        self.connect()
        try:
            plant_id = self.plant_name2id[plant_name]
            room_id = self.room_desc2id[room_desc]
        except KeyError, e:
            print 'Some info provited not exist, please check it'
            code = -1
            data = str(e)
        else:
            sql_str = '''
                    UPDATE tb_policy_instance
                    SET room_id = %d, plant_id = %d, start_time = '%s'
                    WHERE policy_instance_id = %d
                    ''' % (room_id, plant_id, start_time, policy_instance_id)
            self.executeDML(sql_str)
            code = 0
            data = SUC
        finally:
            self.close()
            return (code, data)

if __name__ == '__main__':
    host = db_conn_info['HOST']
    db_name = db_conn_info['DATABASE']
    user = db_conn_info['USER']
    password = db_conn_info['PASSWORD']
    temp = DbOperator(host, db_name, user, password)
    temp.test_connection()
    
    for i in range(10):
        temp.insert_data(2, datetime.now().strftime('%Y-%m-%d'), 12.0, 12.1, 12.2, 12.3)
        print "now is instance: %d" %i
     
#     print temp.get_room_info(1) 
#     print temp.get_all_room()
#      
#     print len(temp.get_time_reange_data(2, '2013-12-24 0:0:0', '2013-12-25 0:0:0'))
#     print temp.all_policy_info()
#     print temp.get_policy(1)
#     print temp.current_policy(1)
     
#     print temp.update_plant_info(1, 'strowberry')
#     print temp.update_room_name(2, 'left_second')
#     print temp.update_policy_desc(1, 'second_test')
#      
#     dict = {
#             "roomId" : 1,
#             "description": 'forth',
#             "plantName": 'stowberry',
#             "policy": [{
#                             "date" : 1,
#                             "hour" : 12,
#                             "temperature": (10, 20),
#                             "humidity":  (20, 30),
#                             "co2":  (30, 40),
#                             "lightColor": "white",
#                         },
#                        {
#                             "date" : 1,
#                             "hour" : 12,
#                             "temperature": (11, 21),
#                             "humidity":  (21, 31),
#                             "co2":  (31, 41),
#                             "lightColor": "blue",
#                         },
#                        {
#                             "date" : 1,
#                             "hour" : 12,
#                             "temperature": (12, 22),
#                             "humidity":  (22, 32),
#                             "co2":  (32, 42),
#                             "lightColor": "yellow",
#                         },],
#             "startAt":"2014/01/03 16:07",
#             }
#  
#     print temp.new_policy_instance(dict)
#     print temp.delete_policy(14)
#       
#     
#     temp.transfor_absolute_time('2000-1-1 1:1:0')
    


