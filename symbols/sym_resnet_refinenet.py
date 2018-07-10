import math
from sym_resnet import get_symbol as get_baseline_symbol
import sym_common as sym
import mxnet as mx

def res_conv_unit(data, num_filter, prefix=''):
    relu1, conv1 = sym.reluconv(data=data, num_filter=num_filter, kernel=3, stride=1, prefix=prefix, suffix='1')
    relu2, conv2 = sym.reluconv(data=conv1, num_filter=num_filter, kernel=3, stride=1, prefix=prefix, suffix='2')
    return data + conv2

def res_conv_block(data, num_filter, prefix=''):
    conv_reduce = sym.conv(data=data, name=prefix + 'reduce', num_filter=num_filter, kernel=3, stride=1, no_bias=True)
    rcu1 = res_conv_unit(data=conv_reduce, num_filter=num_filter, prefix=prefix + 'branch1_')
    rcu2 = res_conv_unit(data=rcu1, num_filter=num_filter, prefix=prefix + 'branch2_')
    return rcu2

def mrf_block(data_list, num_filter, prefix=''):
    num_paths = len(data_list)
    if num_paths == 1:
        return data_list[0]
    new_data_list = []
    for i in range(num_paths):
        conv_name = prefix + 'path%d_reduce' % (i + 1)
        conv = sym.conv(data=data_list[i], name=conv_name, num_filter=num_filter, kernel=3, stride=1, no_bias=True)
        if i != num_paths - 1:
            upsample_name = prefix + 'path%d_upsample' % (i + 1)
            scale = int(math.pow(2, num_paths - i - 1))
            conv = sym.upsampling_bilinear(data=conv, name=upsample_name, scale=scale, num_filter=num_filter, need_train=True)
        new_data_list.append(conv)
    sum = mx.sym.ElementWiseSum(*new_data_list, name=prefix + 'sum')
    return sum

def chained_res_pool_block(data, num_filter, num_blocks=2, prefix=''):
    data_list = []
    relu = sym.relu(data=data, name=prefix + 'relu')
    data_list.append(relu)
    for i in range(num_blocks):
        conv_name = prefix + 'conv%d' % (i + 1)
        pool_name = prefix + 'pool%d' % (i + 1)
        conv = sym.conv(data=data_list[i], name=conv_name, num_filter=num_filter, kernel=3, stride=1, no_bias=True)
        pool = sym.pool(data=conv, name=pool_name, kernel=5, stride=1, pool_type='max')
        data_list.append(pool)
    sum = mx.sym.ElementWiseSum(*data_list, name=prefix + 'sum')
    return sum

def refinenet_unit(data_list, num_filter, num_blocks=2, prefix=''):
    mrf_output = mrf_block(data_list=data_list, num_filter=num_filter, prefix=prefix + 'MRF_')
    crp_output = chained_res_pool_block(data=mrf_output, num_filter=num_filter, num_blocks=num_blocks, prefix=prefix + 'CRP_')
    rcu_output1 = res_conv_unit(data=crp_output, num_filter=num_filter, prefix=prefix + "RCU_branch1_")
    rcu_output2 = res_conv_unit(data=rcu_output1, num_filter=num_filter, prefix=prefix + "RCU_branch2_")
    rcu_output3 = res_conv_unit(data=rcu_output2, num_filter=num_filter, prefix=prefix + "RCU_branch3_")
    return rcu_output3

def multi_refinenet(data_list, num_filter_list, num_blocks=2):
    data_num = len(data_list)
    rcu_list = []
    for i in range(data_num):
        prefix = 'RCU%d_' % (i + 1)
        rcu_list.append(res_conv_block(data=data_list[i], num_filter=num_filter_list[i], prefix=prefix))

    num_filter = num_filter_list[0]
    output = refinenet_unit(data_list=[rcu_list[0]], num_filter=num_filter, num_blocks=num_blocks, prefix='R1_')
    for i in range(1, data_num):
        input_list = [output, rcu_list[i]]
        num_filter = min(num_filter, num_filter_list[i])
        prefix = 'R%d_' % (i + 1)
        output = refinenet_unit(data_list=input_list, num_filter=num_filter, num_blocks=num_blocks, prefix=prefix)
    output_relu = sym.relu(data=output, name='output_relu')
    output_dropout = sym.dropout(data=output_relu, name='output_dropout')
    return output_dropout

def get_symbol(num_layers, inv_resolution, **kwargs):
    in_layer_list = get_baseline_symbol(num_layers=num_layers,
                                        inv_resolution=32,
                                        out_intermediate_layer=True,
                                        num_deformable_group=0,
                                        **kwargs)
    conv2 = in_layer_list[0]  # 4
    conv3 = in_layer_list[1]  # 8
    conv4 = in_layer_list[2]  # 16
    # conv5 = in_layer_list[3]  # 32
    conv5_relu = in_layer_list[4]  # 32
    if inv_resolution == 32:
        return conv5_relu
    elif inv_resolution == 16:
        return multi_refinenet(data_list=[conv5_relu, conv4], num_filter_list=[512, 256])
    elif inv_resolution == 8:
        return multi_refinenet(data_list=[conv5_relu, conv4, conv3], num_filter_list=[512, 256, 256])
    elif inv_resolution == 4:
        return multi_refinenet(data_list=[conv5_relu, conv4, conv3, conv2], num_filter_list=[512, 256, 256, 256])
    else:
        raise ValueError("no experiments done on resolution {}".format(inv_resolution))

