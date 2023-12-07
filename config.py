# default
    # generate one virtual dd for all device dd, ordinal
    # ignore parameter [generate_number]

# number
    # generate [generate_number] dd in folder, ordinal
    # read parameter [generate_number]

# random
    # generate random device in dd's folder
    # read parameter [generate_number]

# specific
    # generate specific devices
    # read parameter [specific_devices]
    # ignore parameter [generate_number]

generate_mode = 'specific'
# generate_mode = 'default'

# full cover
    # generate dd until cover all [enum] [values] and [oneOf] in dd
    # ignore parameter [generate_number]
# full_cover = True
full_cover = False

# default = 100
# a value of devices number you want to generate
generate_number = 10

# normal
    # all [enum] [values] [oneOf]
    # normal -> cover at least one time
    # like : device A {propA:{oneOf: a, b}, propB:{oneOf: c, d, e}}
    #   result {propA:a, propB:c}, {propA:b, propB:d}, {propA:b, propB:e}
# full
    # all combination of [enum] [values] [oneOf]
    # full -> cover all combinaiton
            # like : device A {propA:{oneOf: a, b}, propB:{oneOf: c, d, e}}
            #   result {propA:a, propB:c}, {propA:a, propB:d}, {propA:a, propB:e}, 
            #     {propA:b, propB:c}, {propA:b, propB:d}, {propA:b, propB:e}
full_cover_mode = 'normal'


# default
    # random number between [min and max]
# min
    # use [min] value for all number properties
# max
    # use [max] value for all number properties
setting_value_number = 'default'

# when missing min/max
setting_default_number_min = 0
setting_default_number_max = 10


# defautl
    # random string
# a specifice string
    # string
setting_value_normal_string = 'default'


# default
    # random value for all bool type properties
# True or False
setting_value_bool = 'default'


# default
    # random number between [min and max]
# min
    # use [min] value for all number properties
# max
    # use [max] value for all number properties
# a specific value that you want 
    # int
setting_array_size = 'default'
# setting_array_size = 10

# when missing minItems/maxItems
setting_default_arraySize_min = 1
setting_default_arraySize_max = 10


# default 
    # a random value from 2000 - 2023
# current
    # use [now]
# a specifice value that you want
    # int
setting_value_year = 'default'

# default 
    # a random value from 1 - 12
# a specifice value that you want
    # int
setting_value_month = 'default'

# default 
    # a random value from 1 - 31 or 30 or 29 or 28
# current
    # use [now]
# a specifice value that you want
    # int
setting_value_day = 'default'

# default 
    # a random value from 0 - 23
# current
    # use [now]
# a specifice value that you want
setting_value_hour = 'default'

# default 
    # a random value from 0 - 59
# current
    # use [now]
# a specifice value that you want
    # int
setting_value_minute = 'default'

# default 
    # a random value from 0 - 59
# current
    # use [now]
# a specifice value that you want
    # int
setting_value_seconde = 'default'

# file
    # output to file
# print
    # print generated dd
output_type = 'file'

# skip device list
    # eoj list
    # format [eoj1, eoj2, eoj2, ...]
skip_list = []

# use setted value , ignore dd
    # format
        # {
        #   device_eoj_1: {epc11: value11, epc12: value12, ...},
        #   device_eoj_2: {epc21: value21, epc22: value22, ...},
        #   ...
        # }
specific_dev_properties = {}

# generate specific devices
    # list ['eoj', 'eoj', ...]
specific_devices = ['0x0134', '0x0273', '0x026B', '0x27B', '0x02A6', '0x0272', '0x0133', '0x03D3']


# dd files path
dd_path = './dd/'

# file output path
    # will make a dir [properties_json_{timestamp}] in this path
output_path = './'