from sym_resnet import get_symbol as get_baseline_symbol
import sym_common as sym

def fcn_unit(data_l, data_h, name, num_filter):
    data_up = sym.upsampling_nearest(data=data_l, name=name + '_up', scale=2)
    data = data_up + data_h
    data_conv = sym.conv(data=data, name=name + '_conv_3x3', num_filter=num_filter, kernel=3)
    return data_conv

def get_symbol(num_layers, inv_resolution, num_filter, **kwargs):
    in_layer_list = get_baseline_symbol(num_layers=num_layers,
                                        inv_resolution=32,
                                        out_intermediate_layer=True,
                                        num_deformable_group=0,
                                        **kwargs)
    for i in range(len(in_layer_list)):
        name = 'conv%d_reduce' % (i + 2)
        in_layer_list[i] = sym.conv(data=in_layer_list[i], name=name, num_filter=num_filter, kernel=1)
    conv2 = in_layer_list[0]  # 4
    conv3 = in_layer_list[1]  # 8
    conv4 = in_layer_list[2]  # 16
    # conv5 = in_layer_list[3]  # 32
    conv5_relu = in_layer_list[4]  # 32
    if inv_resolution == 32:
        return conv5_relu
    conv4 = fcn_unit(conv5_relu, conv4, name='fcn_conv4', num_filter=num_filter)
    if inv_resolution == 16:
        return conv4
    conv3 = fcn_unit(conv4, conv3, name='fcn_conv3', num_filter=num_filter)
    if inv_resolution == 8:
        return conv3
    conv2 = fcn_unit(conv3, conv2, name='fcn_conv2', num_filter=num_filter)
    if inv_resolution == 4:
        return conv2
    else:
        raise ValueError("no experiments done on resolution {}".format(inv_resolution))

