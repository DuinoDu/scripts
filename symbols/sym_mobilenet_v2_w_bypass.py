import mxnet as mx
import logging

use_global_stats = True
fix_gamma = False
eps = 2e-5
bn_mom = 0.9
workspace = 512
expansion_factor = 6
multiplier = 1.0
drop_ratio = 0.2
kernel = (3, 3)
pad = (1, 1)
fix_point_type = False
mirroring_level = 0


def inverted_residual_block(data,
                            input_channels,
                            output_channels,
                            stride=(1, 1),
                            is_change_stride=False,
                            bias=False,
                            t=expansion_factor,
                            is_fix_point=fix_point_type,
                            name=None):
    assert stride[0] == stride[1]
    in_channels = int(input_channels * multiplier) * t
    out_channels = int(output_channels * multiplier)

    if not is_fix_point:
        bottleneck_a = mx.sym.Convolution(data=data,
                                          num_filter=in_channels,
                                          kernel=(1, 1),
                                          pad=(0, 0),
                                          stride=(1, 1),
                                          no_bias=False if bias else True,
                                          num_group=1,
                                          workspace=workspace,
                                          name=name + '_conv2d_pointwise')
        bottleneck_a = mx.sym.BatchNorm(data=bottleneck_a,
                                        fix_gamma=fix_gamma,
                                        eps=eps,
                                        momentum=bn_mom,
                                        use_global_stats=use_global_stats,
                                        attr={'force_mirroring': 'True', 'cudnn_off': 'True'} if mirroring_level >= 2 else {},
                                        name=name + '_conv2d_pointwise_bn')
        bottleneck_a = mx.sym.Activation(data=bottleneck_a,
                                         act_type='relu',
                                         name=name + '_conv2d_pointwise_relu')
        if mirroring_level >= 1:
            bottleneck_a._set_attr(force_mirroring='True')

        bottleneck_b = mx.sym.Convolution(data=bottleneck_a,
                                          num_filter=in_channels,
                                          kernel=kernel,
                                          pad=pad,
                                          stride=stride,
                                          no_bias=False if bias else True,
                                          num_group=in_channels,
                                          workspace=workspace,
                                          name=name + '_conv2d_depthwise')
        bottleneck_b = mx.sym.BatchNorm(data=bottleneck_b,
                                        fix_gamma=fix_gamma,
                                        eps=eps,
                                        momentum=bn_mom,
                                        use_global_stats=use_global_stats,
                                        attr={'force_mirroring': 'True', 'cudnn_off': 'True'} if mirroring_level >= 2 else {},
                                        name=name + '_conv2d_depthwise_bn')
        bottleneck_b = mx.sym.Activation(data=bottleneck_b,
                                         act_type='relu',
                                         name=name + '_conv2d_depthwise_relu')
        if mirroring_level >= 1:
            bottleneck_b._set_attr(force_mirroring='True')

        bottleneck_c = mx.sym.Convolution(data=bottleneck_b,
                                          num_filter=out_channels,
                                          kernel=(1, 1),
                                          pad=(0, 0),
                                          stride=(1, 1),
                                          no_bias=False if bias else True,
                                          num_group=1,
                                          workspace=workspace,
                                          name=name + '_conv2d_linear_transform')
        bottleneck_c = mx.sym.BatchNorm(data=bottleneck_c,
                                        fix_gamma=fix_gamma,
                                        eps=eps,
                                        momentum=bn_mom,
                                        use_global_stats=use_global_stats,
                                        attr={'force_mirroring': 'True', 'cudnn_off': 'True'} if mirroring_level >= 2 else {},
                                        name=name + '_conv2d_linear_transform_bn')
        if stride[0] == 2 or is_change_stride:
            out_data = bottleneck_c
        elif input_channels == output_channels:
            out_data = bottleneck_c + data
        else:
            bottleneck_bypass = mx.sym.Convolution(data=data,
                                                   num_filter=out_channels,
                                                   kernel=(1, 1),
                                                   pad=(0, 0),
                                                   stride=(1, 1),
                                                   no_bias=False if bias else True,
                                                   num_group=1,
                                                   workspace=workspace,
                                                   name=name + '_bypass_conv')
            bottleneck_bypass = mx.sym.BatchNorm(data=bottleneck_bypass,
                                                 fix_gamma=fix_gamma,
                                                 eps=eps,
                                                 momentum=bn_mom,
                                                 use_global_stats=use_global_stats,
                                                 attr={'force_mirroring': 'True', 'cudnn_off': 'True'} if mirroring_level >= 2 else {},
                                                 name=name + '_bypass_bn')
            out_data = bottleneck_c + bottleneck_bypass
        if mirroring_level >= 1:
            out_data._set_attr(force_mirroring='True')
        return out_data
    else:
        assert False


def get_symbol(inv_resolution=32, **kwargs):
    assert inv_resolution == 16 or inv_resolution == 32
    input_dict = kwargs['input_dict'] if 'input_dict' in kwargs else None
    data = kwargs['data'] if 'data' in kwargs else mx.sym.Variable(name='data')
    in_layer_list = []

    # first convolution
    conv1_channels = int(32 * multiplier)
    if not fix_point_type:
        conv1 = mx.sym.Convolution(data=data,
                                   num_filter=conv1_channels,
                                   kernel=(3, 3),
                                   pad=(1, 1),
                                   stride=(2, 2),
                                   no_bias=True,
                                   num_group=1,
                                   workspace=workspace,
                                   name='conv1')
        conv1 = mx.sym.BatchNorm(data=conv1,
                                 fix_gamma=fix_gamma,
                                 eps=eps,
                                 momentum=bn_mom,
                                 use_global_stats=use_global_stats,
                                 attr={'force_mirroring': 'True', 'cudnn_off': 'True'} if mirroring_level >= 2 else {},
                                 name='conv1_bn')
        conv1 = mx.sym.Activation(data=conv1,
                                  act_type='relu',
                                  name='conv1_relu')
        if mirroring_level >= 1:
            conv1._set_attr(force_mirroring='True')
    else:
        assert False
    bottleneck1 = inverted_residual_block(data=conv1,
                                          input_channels=32,
                                          output_channels=16,
                                          stride=(1, 1),
                                          t=1,
                                          is_fix_point=fix_point_type,
                                          name='bottleneck1')
    if input_dict is not None:
        logging.info('bottleneck1: {}'.format(bottleneck1.infer_shape(**input_dict)[1]))

    # res2
    bottleneck2 = inverted_residual_block(data=bottleneck1,
                                          input_channels=16,
                                          output_channels=24,
                                          stride=(2, 2),
                                          t=expansion_factor,
                                          is_fix_point=fix_point_type,
                                          name='bottleneck2')
    bottleneck3 = inverted_residual_block(data=bottleneck2,
                                          input_channels=24,
                                          output_channels=24,
                                          stride=(1, 1),
                                          t=expansion_factor,
                                          is_fix_point=fix_point_type,
                                          name='bottleneck3')
    in_layer_list.append(bottleneck3)
    if input_dict is not None:
        logging.info('bottleneck3: {}'.format(bottleneck3.infer_shape(**input_dict)[1]))

    # res3
    bottleneck4 = inverted_residual_block(data=bottleneck3,
                                          input_channels=24,
                                          output_channels=32,
                                          stride=(2, 2),
                                          t=expansion_factor,
                                          is_fix_point=fix_point_type,
                                          name='bottleneck4')
    bottleneck5 = inverted_residual_block(data=bottleneck4,
                                          input_channels=32,
                                          output_channels=32,
                                          stride=(1, 1),
                                          t=expansion_factor,
                                          is_fix_point=fix_point_type,
                                          name='bottleneck5')
    bottleneck6 = inverted_residual_block(data=bottleneck5,
                                          input_channels=32,
                                          output_channels=32,
                                          stride=(1, 1),
                                          t=expansion_factor,
                                          is_fix_point=fix_point_type,
                                          name='bottleneck6')
    in_layer_list.append(bottleneck6)
    if input_dict is not None:
        logging.info('bottleneck6: {}'.format(bottleneck6.infer_shape(**input_dict)[1]))

    # res4
    bottleneck7 = inverted_residual_block(data=bottleneck6,
                                          input_channels=32,
                                          output_channels=64,
                                          stride=(2, 2),
                                          t=expansion_factor,
                                          is_fix_point=fix_point_type,
                                          name='bottleneck7')
    bottleneck8 = inverted_residual_block(data=bottleneck7,
                                          input_channels=64,
                                          output_channels=64,
                                          stride=(1, 1),
                                          t=expansion_factor,
                                          is_fix_point=fix_point_type,
                                          name='bottleneck8')
    bottleneck9 = inverted_residual_block(data=bottleneck8,
                                          input_channels=64,
                                          output_channels=64,
                                          stride=(1, 1),
                                          t=expansion_factor,
                                          is_fix_point=fix_point_type,
                                          name='bottleneck9')
    bottleneck10 = inverted_residual_block(data=bottleneck9,
                                           input_channels=64,
                                           output_channels=64,
                                           stride=(1, 1),
                                           t=expansion_factor,
                                           is_fix_point=fix_point_type,
                                           name='bottleneck10')
    bottleneck11 = inverted_residual_block(data=bottleneck10,
                                           input_channels=64,
                                           output_channels=96,
                                           stride=(1, 1),
                                           t=expansion_factor,
                                           is_fix_point=fix_point_type,
                                           name='bottleneck11')
    bottleneck12 = inverted_residual_block(data=bottleneck11,
                                           input_channels=96,
                                           output_channels=96,
                                           stride=(1, 1),
                                           t=expansion_factor,
                                           is_fix_point=fix_point_type,
                                           name='bottleneck12')
    bottleneck13 = inverted_residual_block(data=bottleneck12,
                                           input_channels=96,
                                           output_channels=96,
                                           stride=(1, 1),
                                           t=expansion_factor,
                                           is_fix_point=fix_point_type,
                                           name='bottleneck13')
    in_layer_list.append(bottleneck13)
    if input_dict is not None:
        logging.info('bottleneck13: {}'.format(bottleneck13.infer_shape(**input_dict)[1]))

    # res5
    stride = (2, 2) if inv_resolution == 32 else (1, 1)
    is_change_stride = False if inv_resolution == 32 else True
    bottleneck14 = inverted_residual_block(data=bottleneck13,
                                           input_channels=96,
                                           output_channels=160,
                                           stride=stride,
                                           is_change_stride=is_change_stride,
                                           t=expansion_factor,
                                           is_fix_point=fix_point_type,
                                           name='bottleneck14')
    bottleneck15 = inverted_residual_block(data=bottleneck14,
                                           input_channels=160,
                                           output_channels=160,
                                           stride=(1, 1),
                                           t=expansion_factor,
                                           is_fix_point=fix_point_type,
                                           name='bottleneck15')
    bottleneck16 = inverted_residual_block(data=bottleneck15,
                                           input_channels=160,
                                           output_channels=160,
                                           stride=(1, 1),
                                           t=expansion_factor,
                                           is_fix_point=fix_point_type,
                                           name='bottleneck16')
    bottleneck17 = inverted_residual_block(data=bottleneck16,
                                           input_channels=160,
                                           output_channels=320,
                                           stride=(1, 1),
                                           t=expansion_factor,
                                           is_fix_point=fix_point_type,
                                           name='bottleneck17')
    in_layer_list.append(bottleneck17)
    if input_dict is not None:
        logging.info('bottleneck17: {}'.format(bottleneck17.infer_shape(**input_dict)[1]))

    return in_layer_list






