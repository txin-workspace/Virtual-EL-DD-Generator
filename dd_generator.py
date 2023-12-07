import json
import random
import string
import os
import time
from datetime import datetime
import sys
import copy

import static
import config


dict_comm_dd = {}
output_props_path = ''

current = datetime.now()
full_cover = False
cover_prop_value_dict = {}

obj_flag = False
obj_sub_prop_name = []

# for debug
dd_name = ''

def init():
    global dict_comm_dd
    # load common items dd
    comm_dd_file = open(config.dd_path + 'commonItems.json', mode = 'r')
    dict_comm_dd = json.load(comm_dd_file)['properties']
    comm_dd_file.close()

    # make properties json files dir
    dir_path = config.output_path + 'properties_json_{}'.format(time.time())
    os.mkdir(dir_path)

    global output_props_path
    output_props_path = dir_path + '/'
    # os.mkdir(output_props_path)


def load_dd_file(f_path: str):
    dd_file = open(f_path, mode = 'r')
    dict_dd = json.load(dd_file)
    dd_file.close()
    return dict_dd


def value_boolean() -> bool:
    return random.choice([True, False])


def value_int(min, max) -> int:
    return random.randint(min, max)


def value_multiple(min, max, multiple):
    if multiple == 1:
        return value_int(min, max)

    elif multiple < 1:
        return value_float(min, max, multiple)
        
    else:
        # multiple_int
        val = random.randint(min, max)
        val -= val % multiple
        if val > max or val < min:
            print('[value multiple] dd error ', min, max, multiple, val)
        return val


def value_float(min, max, multiple: float) -> float:
    return round(random.uniform(min, max), len(str(multiple).split('.')[1]))


def value_values(values: list, p_name):
    # print('values')
    global full_cover
    global cover_prop_value_dict

    global obj_sub_prop_name

    if full_cover != True:
        return values[random.randint(0, len(values) -1)]['value']

    else:
        p = dict_key_deep(cover_prop_value_dict, copy.deepcopy(obj_sub_prop_name))
        for v in values: p.append(v['value'])
        return None


def value_year_month():
    global current

    year = None
    month = None

    if config.setting_value_year == 'current':
        year = current.year
    elif type(config.setting_value_year) == int:
        year = config.setting_value_year
    else:
        if config.setting_value_year != 'default':
            print('[config error] config.setting_value_year', config.setting_value_year, 'use default')
        year = int('20{:02d}'.format(random.randint(0, 23)))

    if config.setting_value_month == 'current':
        month = current.month
    elif type(config.setting_value_month) == int:
        month = config.setting_value_month
    else:
        if config.setting_value_month != 'default':
            print('[config error] config.setting_value_month', config.setting_value_month, 'use default')
        month = random.randint(0, 12)
        
    return year, month


def value_day(year, month):
    day = None

    if config.setting_value_day == 'current':
        day = current.day
    elif type(config.setting_value_day) == int:
        month = config.setting_value_day
    else:
        if config.setting_value_day != 'default':
            print('[config error] config.setting_value_day', config.setting_value_day, 'use default')
        
        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = random.randint(1, 31)
        elif month in [4, 6, 9, 11]:
            day = random.randint(1, 30)
        elif month == 2 and ((year % 4 == 0 and year % 100 != 0) or year % 400 != 0):
            day = random.randint(1, 29)
        else:
            day = random.randint(1, 28)

    return day


def value_time():
    h = None
    m = None
    s = None

    if config.setting_value_hour == 'current':
        h = current.hour()
    elif type(config.setting_value_hour) == int:
        h = setting_value_hour
    else:
        if config.setting_value_hour != 'default':
            print('[config error] config.setting_value_hour', config.setting_value_hour, 'use default')
        h = random.randint(0, 23)

    if config.setting_value_minute == 'current':
        m = current.minute()
    elif type(config.setting_value_minute) == int:
        m = setting_value_minute
    else:
        if config.setting_value_minute != 'default':
            print('[config error] config.setting_value_minute', config.setting_value_minute, 'use default')
        m = random.randint(0, 59)

    if config.setting_value_seconde == 'current':
        s = current.second()
    elif type(config.setting_value_seconde) == int:
        s = setting_value_seconde
    else:
        if config.setting_value_seconde != 'default':
            print('[config error] config.setting_value_seconde', config.setting_value_seconde, 'use default')
        s = random.randint(0, 59)

    return h, m, s


def p_format_dt() -> str:
    ye, mo = value_year_month()
    d = value_day(ye, mo)
    h, m, s  = value_time()
    return '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(ye, mo, d, h, m, s)


def p_format_date() -> str:
    ye, mo = value_year_month()
    d = value_day(ye, mo)
    return '{:04d}-{:02d}-{:02d}'.format(ye, mo, d)
    

def p_format_time() -> str:
    h, m, s = value_time()
    return '{:02d}:{:02d}:{:02d}'.format(h, m, s)


def value_enum(list_enum: list, p_name):
    # print('enum')
    global full_cover
    global cover_prop_value_dict

    global obj_sub_prop_name
    
    if full_cover != True:
        return list_enum[random.randint(0, len(list_enum) -1)]
    
    else:
        p = dict_key_deep(cover_prop_value_dict, copy.deepcopy(obj_sub_prop_name))
        p.extend(list_enum)
        return None


def p_type_object(dict_props: dict, p_name):
    global obj_sub_prop_name

    value_obj = {}
    for prop in dict_props:
        value_obj[prop] = schema_type_switcher(dict_props[prop], prop)

    return value_obj


def value_normal_str() -> str:
    s = None
    if type(config.setting_value_normal_string) == str and config.setting_value_normal_string != 'default':
        s = config.setting_value_normal_string
    else:
        if config.setting_value_normal_string != 'default':
            print('[config error] config.setting_value_normal_string', config.setting_value_seconde, 'use default')
        s = string.ascii_uppercase
        s = ''.join(random.choice(s) for i in range(random.randint(10, 25)))

    return s


def p_type_array(dict_schema: dict, p_name):
    global dd_name
    # default for no min max
    array_size_min = config.setting_default_arraySize_min
    array_size_max = config.setting_default_arraySize_max

    if 'minItems' in dict_schema: 
        array_size_min = dict_schema['minItems']
    else:
        print('[dd array] no minItems', p_name, dd_name)

    if 'maxItems' in dict_schema: 
        array_size_max = dict_schema['maxItems']
    else:
        print('[dd array] no maxItems', p_name, dd_name)

    if array_size_max < array_size_min:
        print('[p_type_array] dd error', p_name, dd_name)
        array_size_max = array_size_min

    value_arr_size = None
    if config.setting_array_size == 'max':
        value_arr_size = array_size_max

    elif config.setting_array_size == 'min':
        value_arr_size = array_size_min

    elif type(config.setting_array_size) == int:
        value_arr_size = config.setting_array_size

    else:
        if config.setting_array_size != 'default':
            print('[config error] config.setting_array_size', config.setting_array_size, 'use default')
        value_arr_size = random.randint(array_size_min, array_size_max)
        
    value_array = []
    while len(value_array) < value_arr_size:
        value_array.append(schema_type_switcher(dict_schema['items'], p_name))

    return value_array



def dict_key_deep(dict_test, list_key):
    global obj_sub_prop_name
    global cover_prop_value_dict

    if list_key == []:
        return dict_test

    k = list_key.pop(0)

    if type(dict_test) == list:
        if len(dict_test) == 0 and list_key == []:
            if k not in dict_test:
                dict_test[k] = []

        elif len(dict_test) == 0 and list_key != []:
            if k not in dict_test:
                dict_test[k] = {}

        elif len(dict_test) != 0 and list_key == []:
            for obj in dict_test:
                for obj_k in obj:
                    if obj_k == k: 
                        return obj[obj_k]

            dict_test.append({k:[]})
            return dict_test[-1][k]

    elif type(dict_test) == dict and k not in dict_test:
        if list_key == []:
            dict_test[k] = []
        else:
            dict_test[k] = {}
        
    return dict_key_deep(dict_test[k], list_key)


def p_type_oneOf(list_oneof: list, p_name):
    # print('oneOf')
    global full_cover
    global cover_prop_value_dict
    global obj_sub_prop_name

    if full_cover != True:
        random_select = list_oneof[random.randint(0, len(list_oneof) -1)]
        return schema_type_switcher(random_select, p_name)

    else:
        p = dict_key_deep(cover_prop_value_dict, copy.deepcopy(obj_sub_prop_name))
            
        for one_value in list_oneof:
            # print('{}\n\t{}\n\t{}\n\t{}'.format(cover_prop_value_dict, p, obj_sub_prop_name, p_name))
            p.append(schema_type_switcher(one_value, p_name))

        return None
    
   

def p_type_bool(dict_schema, p_name):
    global obj_sub_prop_name

    if type(config.setting_value_bool) == bool:
        return config.setting_value_bool
    else:
        if config.setting_value_bool != 'default':
            print('[config error] config.setting_value_bool', config.setting_value_bool, 'use default')
        
        if 'values' in dict_schema:
            # obj_sub_prop_name.append(p_name)
            v = value_values(dict_schema['values'], p_name)
            # obj_sub_prop_name.remove(p_name)
            return v
        else:
            return value_boolean()


def p_type_number(dict_schema, p_name):
    global dd_name

    num_min = config.setting_default_number_min
    num_max = config.setting_default_number_max
    if 'minimum' in dict_schema:
        num_min = dict_schema['minimum']
    else:
        print('[dd number] no minimum', p_name, dd_name)

    if 'maximum' in dict_schema:
        num_max = dict_schema['maximum']
    else:
        print('[dd number] no maximum', p_name, dd_name)

    if num_max <= num_min:
        print('[p_type_number] dd error maximum and minmum', p_name, dd_name)
        num_max = num_min

    if config.setting_value_number == 'max':
        return num_max

    elif config.setting_value_number == 'mim':
        return num_min

    elif type(config.setting_value_number) == int:
        return config.setting_value_number

    else:
        if config.setting_value_number != 'default':
            print('[config error] config.setting_value_number', config.setting_value_number, 'use default')

        if 'multipleOf' in dict_schema:
            return value_multiple(num_min, num_max, dict_schema['multipleOf'])
        else:
            return value_int(num_min, num_max)


def p_type_string(dict_schema, p_name):
    if 'format' in dict_schema:
        if dict_schema['format'] == 'date':
            return p_format_date()
        elif dict_schema['format'] == 'time':
            return p_format_time()
        elif dict_schema['format'] == 'date-time':
            return p_format_dt()
        else:
            print('other string format', dict_schema['format'])

    elif 'enum' in dict_schema:
        return value_enum(dict_schema['enum'], p_name)

    else:
        return value_normal_str() 
            

def p_name_manufacturer():
    m_code = random.choice(static.manufacturers_code)
    while True:
        if m_code in static.manufacturers_ja and m_code in static.manufacturers_en:
            break
        m_code = random.choice(static.manufacturers_code)
    
    return {
        "code": m_code, 
        "descriptions": {
            "ja": static.manufacturers_ja[m_code],
            "en": static.manufacturers_en[m_code]
        }
    }


def p_name_protocol():
    return {
        "type": "ECHONET_Lite v1.5.0",
        "version": "Rel.Q"
    }


def p_name_installationLocation():
    return random.choice(static.locations)


def schema_type_switcher(dict_schema: dict, p_name):
    global obj_sub_prop_name

    if obj_sub_prop_name != [] and obj_sub_prop_name[-1] != p_name:
        obj_sub_prop_name.append(p_name)

    elif obj_sub_prop_name == []:
        obj_sub_prop_name.append(p_name)

    if 'oneOf' in dict_schema:
        v = p_type_oneOf(dict_schema['oneOf'], p_name)

    elif dict_schema['type'] == 'number':
        v = p_type_number(dict_schema, p_name)
     
    elif dict_schema['type'] == 'boolean':
        v = p_type_bool(dict_schema, p_name)

    elif dict_schema['type'] == 'string':
        v = p_type_string(dict_schema, p_name)

    elif dict_schema['type'] == 'object':
        v = p_type_object(dict_schema['properties'], p_name)
      
    elif dict_schema['type'] == 'array':
        v = p_type_array(dict_schema, p_name)

    else:
        print('other properties type: ', dict_schema['type'])

    if obj_sub_prop_name != [] and obj_sub_prop_name[-1] == p_name:
            obj_sub_prop_name.pop(-1)
    
    return v


# input dd[properties]
# output {property: value, p: v, p:v, ... ...}
def props_generator(dict_dd_props: dict, eoj_code: str) -> dict:
    global list_test_case_str
    dict_prop_val = {}

    for p in dict_dd_props:

        if eoj_code in config.specific_dev_properties and p in config.specific_dev_properties[eoj_code]:
            dict_prop_val[p] = config.specific_dev_properties[eoj_code][p]

        elif p == 'manufacturer':
            dict_prop_val['manufacturer'] = p_name_manufacturer()

        elif p == 'protocol':
            dict_prop_val['protocol'] = p_name_protocol()

        elif p == 'installationLocation':
            dict_prop_val['installationLocation'] = p_name_installationLocation()

        else: 
            dict_prop_val[p] = schema_type_switcher(dict_dd_props[p]['schema'], p)

    return dict_prop_val


def props_write_file(f_name: str, dict_props: dict) -> None:
    global output_props_path
    # print('write file: ', f_name, '.json')
    file_path = output_props_path + f_name + '.json'
    props_file = open(file_path, mode = ('w'))
    props_file.write(json.dumps(dict_props))
    props_file.close()
    # print('write props file finish: {}.json'.format(f_name))


def info_generator(dev_type, dev_poprs):
    return {
        'id': '{}-{}'.format(dev_type, random.getrandbits(128)),
        'deviceType': dev_type,
        'protocol': dev_poprs['protocol'],
        'manufacturer': dev_poprs['manufacturer']
    }


def desc_generator(dd_props):
    global dict_comm_dd
    dev_dd = copy.deepcopy(dd_props)
    dev_dd['properties'].update(dict_comm_dd)
    return dev_dd

# def main(gen_num):
def main():
    global full_cover
    global cover_prop_value_dict

    global dict_comm_dd
    global dd_name
    init()

    # load all devices dd file path
    list_dd_file = []

    for f_name in os.listdir('./dd/'):
        if '.json' not in f_name: continue
        if 'commonItems' in f_name: continue

        f_path = './dd/{}'.format(f_name)
        if os.path.isfile(f_path):
            list_dd_file.append(f_path)

    generate_vd_dd_path_list = []
    if  config.generate_mode == 'default':
        generate_vd_dd_path_list = list_dd_file

    elif config.generate_mode == 'number':
        num_count = 0
        if type(config.generate_number) != int:
            print('[config error] config.generate_number', config.generate_number, 'finish')
            return

        while num_count < config.generate_number:
            generate_vd_dd_path_list.append(list_dd_file[num_count % len(list_dd_file)])
            num_count += 1
        
    elif config.generate_mode == 'random':
        num_count = 0
        if type(config.generate_number) != int:
            print('[config error] config.generate_number', config.generate_number, 'finish')
            return
        
        dd_files_num = len(list_dd_file) -1
        while num_count < config.generate_number:
            generate_vd_dd_path_list.append(list_dd_file[random.randint(0, dd_files_num)])
            num_count += 1

    elif config.generate_mode == 'specific':
            generate_vd_dd_path_list.extend(list_dd_file)

    else:
        print('[config error] config.generate_mode', config.generate_mode, 'finish')
        return

    if config.full_cover == True:
        full_cover = True
        print('full cover mode True')

    output_list = []

    for dd_file_path in generate_vd_dd_path_list:
        # read one device's dd
        dvice_dd = load_dd_file(dd_file_path)

        # read config -> skiplist and skip devices
        if dvice_dd['eoj'] in config.skip_list: continue

        # init dict of avabiliable values
        if full_cover == True: cover_prop_value_dict = {}

        if config.generate_mode == 'specific':
            if dvice_dd['eoj'] not in config.specific_devices:
                continue

        # for debug
        dd_name = dvice_dd['deviceType']
        print('device: {}'.format(dd_name))
        print('path : {}'.format(dd_file_path))

        # generate properties
        device_props = props_generator(dvice_dd['properties'], dvice_dd['eoj'])

        # add common properties to properties
        device_props.update(props_generator(dict_comm_dd, '0x0000'))

        # generate device info
        # device_info = info_generator(dvice_dd['deviceType'], device_props)

        # generate device description
        device_description = desc_generator(dvice_dd)

        
        if full_cover != True:
            print('no full cover', full_cover)
            device_info = info_generator(dvice_dd['deviceType'], device_props)
            output_list.append(
                {
                    'info':device_info, 
                    'properties': device_props,
                    'dd': device_description
                }
            )
        else:
            print('mode:', config.full_cover_mode)

            if config.full_cover_mode == 'normal':
                # print('normal -> cover_prop_value_dict: \n\t{}'.format(cover_prop_value_dict))
                # print('normal -> device_props: \n\t{}'.format(device_props))
                max_len = 0

                # find longest list in cover_prop_value_dict
                max_len = clear_and_find_longest_list_in_data(cover_prop_value_dict)
                # print('max length: {}'.format(max_len))
                # print('changed dict: {}'.format(cover_prop_value_dict))

                len_count = 0
                while len_count < max_len:
                    tmp_dict = pair_available_values(copy.deepcopy(device_props), len_count)
                    # print(tmp_dict)
                    device_info = info_generator(dvice_dd['deviceType'], tmp_dict)

                    output_list.append(
                        {
                            'info':device_info, 
                            'properties': tmp_dict,
                            'dd': device_description
                        }
                    )

                    len_count += 1

            
            elif config.full_cover_mode == 'full':
                print('full mode not implement yet')

            else:
                print('[config error] config.full_cover_mode', config.full_cover_mode, 'finish')
                return
                    

        # read config and select the output way
        # output generated virtual device desc
        if config.output_type == 'print':
            for dev_props in output_list:
                print(dev_props)

        else:
            if config.output_type != 'file':
                print('[config error] config.output_type', config.output_type, 'use default')
            
            # output to file
            for dev_props in output_list:
                props_write_file(
                    '{}-{}'.format(dvice_dd['deviceType'], time.time()), 
                    dev_props)

        output_list = []


def pair_available_values(data, count, path = []):
    global cover_prop_value_dict

    if type(data) == dict:
        for d_name, d_value in data.items():
            path.append(d_name)

            if type(d_value) == list or type(d_value) == dict:
                pair_available_values(d_value, count, path)

            elif d_value == None:
                data[d_name] = find_value(copy.copy(path), count, cover_prop_value_dict)

            path.pop(-1)

    elif type(data) == list:

        array_size = len(data)
        item_counter = 0

        while item_counter < array_size:

            if data[item_counter] == None:
                data[item_counter] = find_value(copy.copy(path), count, cover_prop_value_dict)

            else:
                item_counter += 1
            
        for data_item in data:
            if type(data_item) == list or type(data_item) == dict:
                pair_available_values(data_item, count, path)
            
            # else:
            #     print('not list or dict in list: {} {} {}'.format(data_item, data, path))

    else:
        print('error: {}'.format(data))

    return data


def find_value(path, count, values_data):
    # print(values_data)
    # print(path)
    if len(path) != 0:
        k = path.pop(0)
        return find_value(path, count, values_data[k])

    else:
        if type(values_data) != list:
            print('find_value not list: {} {}'.format(values_data, path))
            return None

        else:
            l = len(values_data)
            return values_data[count % l]


def clear_and_find_longest_list_in_data(data):
    max_len = 0
    if type(data) == dict:
        data_keys = list(data.keys())
        if len(data_keys) == 1 and data[data_keys[0]] == None:
            return -1
        
        for data_key, data_value in data.items():
            if type(data_value) != dict and type(data_value) != list:
                continue
            
            n = clear_and_find_longest_list_in_data(data_value)
            if n == -1: 
                print('error')
            elif n > max_len:
                max_len = n
        
    elif type(data) == list:

        for data_item in data:
            if data_item == None:
                data.remove(data_item)

        for data_item in data:

            if type(data_item) != dict and type(data_item) != list:
                continue
            
            n = clear_and_find_longest_list_in_data(data_item)
            if n == -1: 
                # print('remove: {}'.format(data_item))
                data.remove(data_item)
            elif n > max_len: 
                max_len = n

        list_v_type = set()
        for data_item in data:
            if type(data_item) == int:
                list_v_type.add('int')

            elif type(data_item) == float:
                list_v_type.add('float')

            elif type(data_item) == str:
                list_v_type.add(data_item)
            
            elif type(data_item) == bool:
                list_v_type.add(data_item)
        
        if len(list_v_type) > max_len: 
            max_len = len(list_v_type)

    return max_len


if __name__ == '__main__':
    # main(int(sys.argv[1]))
    main()