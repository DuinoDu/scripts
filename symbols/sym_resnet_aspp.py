from sym_resnet import get_symbol as get_baseline_symbol
import sym_common as sym
import mxnet as mx


# Atrous Spatial Pyramid Pooling
def aspp_unit(data, prefix, num_filter, rate_list):
    conv1 = sym.conv(data=data, name=prefix+'1', num_filter=num_filter, kernel=1)
    conv2 = sym.conv(data=data, name=prefix+'2', num_filter=num_filter, kernel=3, dilate=rate_list[0])
    conv3 = sym.conv(data=data, name=prefix+'3', num_filter=num_filter, kernel=3, dilate=rate_list[1])
    conv4 = sym.conv(data=data, name=prefix+'4', num_filter=num_filter, kernel=3, dilate=rate_list[2])
    conv_concat = mx.sym.Concat(conv1, conv2, conv3, conv4, num_args=4, dim=1, auto_channel_switch=False)
    conv_fusion = sym.conv(data=conv_concat, name=prefix+'fusion', num_filter=num_filter, kernel=1)
    conv_relu = sym.relu(data=conv_fusion, name=prefix+'relu')
    return conv_relu


def get_symbol(num_layers, inv_resolution, **kwargs):
    assert inv_resolution == 16 or inv_resolution == 8
    in_layer_list = get_baseline_symbol(num_layers=num_layers,
                                        inv_resolution=inv_resolution,
                                        out_intermediate_layer=True,
                                        num_deformable_group=0,
                                        **kwargs)
    conv5_relu = in_layer_list[-1]
    if inv_resolution == 16:
        return aspp_unit(data=conv5_relu, prefix='conv5_s16_', num_filter=256, rate_list=[6, 12, 18])
    else:
        return aspp_unit(data=conv5_relu, prefix='conv5_s8_', num_filter=256, rate_list=[12, 24, 36])


