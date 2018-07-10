import logging
import mxnet as mx

use_global_stats = True
bn_out_first = True
act_out_first = False


def Conv(data, num_filter, kernel, stride, pad, depth_mult=1, name=None, suffix='', bn_mom=0.9, workspace=512):
    conv = mx.sym.Convolution(data=data, num_filter=num_filter, kernel=kernel, num_group=depth_mult,
                              stride=stride, pad=pad, no_bias=True, workspace=workspace, name='%s%s' % (name, suffix))
    return conv


def ConvB(data, num_filter, kernel, stride, pad, depth_mult=1, name=None, suffix='', bn_mom=0.9, workspace=512):
    conv = mx.sym.Convolution(data=data, num_filter=num_filter, kernel=kernel, num_group=depth_mult,
                              stride=stride, pad=pad, no_bias=True, workspace=workspace, name='%s%s' % (name, suffix))
    bn = mx.sym.BatchNorm(data=conv, fix_gamma=False, eps=2e-5, momentum=bn_mom,
                          use_global_stats=use_global_stats, name='%s%s_bn' % (name, suffix))
    return bn


def ConvBA(data, num_filter, kernel, stride, pad, depth_mult=1, name=None, suffix='', bn_mom=0.9, workspace=512):
    conv = mx.sym.Convolution(data=data, num_filter=num_filter, kernel=kernel, num_group=depth_mult,
                              stride=stride, pad=pad, no_bias=True, workspace=workspace, name='%s%s' % (name, suffix))
    bn = mx.sym.BatchNorm(data=conv, fix_gamma=False, eps=2e-5, momentum=bn_mom,
                          use_global_stats=use_global_stats, name='%s%s_bn' % (name, suffix))
    act = mx.sym.Activation(data=bn, act_type='relu', name='%s%s_relu' % (name, suffix))
    return act


def separable_conv(data, n_in_ch, n_out_ch, kernel, stride, pad, depth_mult=1,
                   act_out_first=True, bn_out_first=True,
                   act_out_second=True, bn_out_second=True,
                   name=None, suffix='', bn_mom=0.9, workspace=512):
    # depthwise
    dw_out = mx.sym.Convolution(data=data, num_filter=n_in_ch, kernel=kernel, num_group=depth_mult,
                                stride=stride, pad=pad, no_bias=True, workspace=workspace,
                                name='%s%s_dw' % (name, suffix))
    if bn_out_first:
        dw_out = mx.sym.BatchNorm(data=dw_out, fix_gamma=False, eps=2e-5, momentum=bn_mom,
                                  use_global_stats=use_global_stats, name='%s%s_dw_bn' % (name, suffix))
    if act_out_first:
        dw_out = mx.sym.Activation(data=dw_out, act_type='relu', name='%s%s_dw_relu' % (name, suffix))
    # pointwise
    pw_out = mx.sym.Convolution(data=dw_out, num_filter=n_out_ch, kernel=(1, 1), stride=(1, 1),
                                pad=(0, 0), num_group=1, no_bias=True, workspace=workspace,
                                name='%s%s_pw' % (name, suffix))
    if bn_out_second:
        pw_out = mx.sym.BatchNorm(data=pw_out, fix_gamma=False, eps=2e-5, momentum=bn_mom,
                                  use_global_stats=use_global_stats, name='%s%s_pw_bn' % (name, suffix))
    if act_out_second:
        pw_out = mx.sym.Activation(data=pw_out, act_type='relu', name='%s%s_pw_relu' % (name, suffix))
    return pw_out


def residual_unit_xception_like(data, n_in_ch, n_out_ch, stride, dim_match, aug_level=0, name=None,
                                suffix='', bn_mom=0.9, workspace=512):
    n_in_ch1 = n_in_ch
    n_out_ch1 = n_out_ch / 4
    n_in_ch2 = n_out_ch1
    n_out_ch2 = n_out_ch1
    n_in_ch3 = n_out_ch1
    n_out_ch3 = n_out_ch
    if (not dim_match) and (aug_level == 1):
        n_out_ch3 = n_out_ch - n_in_ch
    assert aug_level >= 0
    assert aug_level <= 2
    # first separable_conv
    sep_out1 = ConvBA(data=data, num_filter=n_out_ch1, kernel=(1, 1), stride=(1, 1) if aug_level >= 1 else stride,
                      pad=(0, 0), depth_mult=1,
                      name=name + '_sp1', suffix=suffix, bn_mom=bn_mom, workspace=workspace)
    # second separable_conv
    sep_out2 = ConvB(data=sep_out1, num_filter=n_out_ch2, kernel=(3, 3), stride=stride if aug_level >= 1 else (1, 1),
                     pad=(1, 1), depth_mult=n_in_ch2,
                     name=name + '_sp2', suffix=suffix, bn_mom=bn_mom, workspace=workspace)
    # third separable_conv
    sep_out3 = ConvB(data=sep_out2, num_filter=n_out_ch3, kernel=(1, 1), stride=(1, 1), pad=(0, 0), depth_mult=1,
                     name=name + '_sp3', suffix=suffix, bn_mom=bn_mom, workspace=workspace)
    if dim_match:
        short_cut = data
        sep_out = sep_out3 + short_cut
    elif aug_level == 0:
        short_cut = mx.sym.Convolution(data=data, num_filter=n_out_ch3, kernel=(1, 1), stride=stride, pad=(0, 0),
                                       no_bias=True,
                                       workspace=workspace, name=name + '_sc')
        short_cut = mx.sym.BatchNorm(data=short_cut, fix_gamma=False, eps=2e-5, momentum=bn_mom,
                                     use_global_stats=use_global_stats, name=name + '_sc_bn')
        sep_out = sep_out3 + short_cut
    elif aug_level == 1:
        short_cut = mx.sym.Pooling(data=data, kernel=(3, 3), pool_type='avg',
                                   stride=stride, pad=(1, 1), name=name + '_sc_pooling')
        sep_out = mx.sym.concat(sep_out3, short_cut, dim=1)
    else:
        short_cut = separable_conv(data=data, n_in_ch=n_in_ch1, n_out_ch=n_out_ch3, kernel=(3, 3), stride=stride,
                                   pad=(1, 1), depth_mult=n_in_ch1,
                                   bn_out_first=bn_out_first, act_out_first=act_out_first, act_out_second=False,
                                   name=name + '_sc', suffix=suffix, bn_mom=bn_mom, workspace=workspace)
        sep_out = sep_out3 + short_cut
    sep_out = mx.sym.Activation(data=sep_out, act_type='relu', name=name + '_sp_out_relu')
    return sep_out


def residual_unit_xception(data, n_in_ch, n_out_ch, stride, dim_match, bn_out_first=True, act_out_first=True,
                           aug_level=0, name=None, suffix='', bn_mom=0.9, workspace=512):
    n_in_ch1 = n_in_ch
    n_out_ch1 = n_out_ch / 4
    n_in_ch2 = n_out_ch1
    n_out_ch2 = n_out_ch1
    n_in_ch3 = n_out_ch1
    n_out_ch3 = n_out_ch
    # first separable_conv
    assert aug_level >= 0
    assert aug_level <= 2
    if aug_level <= 1:
        sep_out1 = separable_conv(data=data, n_in_ch=n_in_ch1, n_out_ch=n_out_ch1, kernel=(3, 3),
                                  stride=stride if aug_level == 0 else (1, 1), pad=(1, 1), depth_mult=n_in_ch1,
                                  bn_out_first=bn_out_first, act_out_first=act_out_first,
                                  name=name + '_sp1', suffix=suffix, bn_mom=bn_mom, workspace=workspace)
        sep_out2 = separable_conv(data=sep_out1, n_in_ch=n_in_ch2, n_out_ch=n_out_ch2, kernel=(3, 3),
                                  stride=(1, 1) if aug_level == 0 else stride, pad=(1, 1), depth_mult=n_in_ch2,
                                  bn_out_first=bn_out_first, act_out_first=act_out_first,
                                  name=name + '_sp2', suffix=suffix, bn_mom=bn_mom, workspace=workspace)
    else:
        if dim_match:
            sep_out1_a = separable_conv(data=data, n_in_ch=n_in_ch1, n_out_ch=n_out_ch1, kernel=(3, 3), stride=stride,
                                        pad=(1, 1), depth_mult=n_in_ch1,
                                        bn_out_first=bn_out_first, act_out_first=act_out_first, act_out_second=True,
                                        name=name + '_sp1_a', suffix=suffix, bn_mom=bn_mom, workspace=workspace)
            sep_out1_b = separable_conv(data=data, n_in_ch=n_in_ch1, n_out_ch=n_out_ch1, kernel=(3, 3), stride=stride,
                                        pad=(1, 1), depth_mult=n_in_ch1,
                                        bn_out_first=bn_out_first, act_out_first=act_out_first, act_out_second=True,
                                        name=name + '_sp1_b', suffix=suffix, bn_mom=bn_mom, workspace=workspace)
            sep_out1 = sep_out1_a + sep_out1_b
        else:
            sep_out1 = separable_conv(data=data, n_in_ch=n_in_ch1, n_out_ch=n_out_ch1, kernel=(3, 3), stride=stride,
                                      pad=(1, 1), depth_mult=n_in_ch1,
                                      bn_out_first=bn_out_first, act_out_first=act_out_first,
                                      name=name + '_sp1', suffix=suffix, bn_mom=bn_mom, workspace=workspace)
        sep_out2 = separable_conv(data=sep_out1, n_in_ch=n_in_ch2, n_out_ch=n_out_ch2, kernel=(3, 3), stride=(1, 1),
                                  pad=(1, 1), depth_mult=n_in_ch2,
                                  bn_out_first=bn_out_first, act_out_first=act_out_first,
                                  name=name + '_sp2', suffix=suffix, bn_mom=bn_mom, workspace=workspace)

    sep_out3 = separable_conv(data=sep_out2, n_in_ch=n_in_ch3, n_out_ch=n_out_ch3, kernel=(3, 3), stride=(1, 1),
                              pad=(1, 1), depth_mult=n_in_ch3,
                              bn_out_first=bn_out_first, act_out_first=act_out_first, act_out_second=False,
                              name=name + '_sp3', suffix=suffix, bn_mom=bn_mom, workspace=workspace)
    if dim_match:
        short_cut = data
    else:
        short_cut = separable_conv(data=data, n_in_ch=n_in_ch1, n_out_ch=n_out_ch3, kernel=(3, 3), stride=stride,
                                   pad=(1, 1), depth_mult=n_in_ch1,
                                   bn_out_first=bn_out_first, act_out_first=act_out_first, act_out_second=False,
                                   name=name + '_sc', suffix=suffix, bn_mom=bn_mom, workspace=workspace)

    sep_out = sep_out3 + short_cut
    sep_out = mx.sym.Activation(data=sep_out, act_type='relu', name=name + '_sp_out_relu')

    return sep_out


def get_symbol(net_type='xception_like', aug_level=1, inv_resolution=32, **kwargs):
    assert inv_resolution == 16 or inv_resolution == 32
    input_dict = kwargs['input_dict'] if 'input_dict' in kwargs else None
    data = kwargs['data'] if 'data' in kwargs else mx.sym.Variable(name='data')
    in_layer_list = []
    bn_mom = 0.9
    workspace = 512

    conv1 = ConvBA(data, num_filter=24, kernel=(3, 3), stride=(2, 2), pad=(1, 1), bn_mom=bn_mom, workspace=workspace,
                   name='conv1')
    pool_1 = mx.symbol.Pooling(data=conv1, kernel=(3, 3), stride=(2, 2), pad=(1, 1), pool_type='max', name='pool_1')
    in_layer_list.append(pool_1)
    if input_dict is not None:
        logging.info('pool_1: {}'.format(pool_1.infer_shape(**input_dict)[1]))

    if net_type == 'xception':
        # res3
        res2_1 = residual_unit_xception(data=pool_1, n_in_ch=24, n_out_ch=144, stride=(2, 2), dim_match=False,
                                        aug_level=aug_level, bn_out_first=bn_out_first, act_out_first=act_out_first,
                                        name='res2_1')
        res2_2 = residual_unit_xception(data=res2_1, n_in_ch=144, n_out_ch=144, stride=(1, 1), dim_match=True,
                                        aug_level=aug_level, bn_out_first=bn_out_first, act_out_first=act_out_first,
                                        name='res2_2')
        res2_3 = residual_unit_xception(data=res2_2, n_in_ch=144, n_out_ch=144, stride=(1, 1), dim_match=True,
                                        aug_level=aug_level, bn_out_first=bn_out_first, act_out_first=act_out_first,
                                        name='res2_3')
        res2_4 = residual_unit_xception(data=res2_3, n_in_ch=144, n_out_ch=144, stride=(1, 1), dim_match=True,
                                        aug_level=aug_level, bn_out_first=bn_out_first, act_out_first=act_out_first,
                                        name='res2_4')
        in_layer_list.append(res2_4)
        if input_dict is not None:
            logging.info('res2_4: {}'.format(res2_4.infer_shape(**input_dict)[1]))

        # res4
        res3_1 = residual_unit_xception(data=res2_4, n_in_ch=144, n_out_ch=288, stride=(2, 2), dim_match=False,
                                        aug_level=aug_level, bn_out_first=bn_out_first, act_out_first=act_out_first,
                                        name='res3_1')
        res3_2 = residual_unit_xception(data=res3_1, n_in_ch=288, n_out_ch=288, stride=(1, 1), dim_match=True,
                                        aug_level=aug_level, bn_out_first=bn_out_first, act_out_first=act_out_first,
                                        name='res3_2')
        res3_3 = residual_unit_xception(data=res3_2, n_in_ch=288, n_out_ch=288, stride=(1, 1), dim_match=True,
                                        aug_level=aug_level, bn_out_first=bn_out_first, act_out_first=act_out_first,
                                        name='res3_3')
        res3_4 = residual_unit_xception(data=res3_3, n_in_ch=288, n_out_ch=288, stride=(1, 1), dim_match=True,
                                        aug_level=aug_level, bn_out_first=bn_out_first, act_out_first=act_out_first,
                                        name='res3_4')
        res3_5 = residual_unit_xception(data=res3_4, n_in_ch=288, n_out_ch=288, stride=(1, 1), dim_match=True,
                                        aug_level=aug_level, bn_out_first=bn_out_first, act_out_first=act_out_first,
                                        name='res3_5')
        res3_6 = residual_unit_xception(data=res3_5, n_in_ch=288, n_out_ch=288, stride=(1, 1), dim_match=True,
                                        aug_level=aug_level, bn_out_first=bn_out_first, act_out_first=act_out_first,
                                        name='res3_6')
        res3_7 = residual_unit_xception(data=res3_6, n_in_ch=288, n_out_ch=288, stride=(1, 1), dim_match=True,
                                        aug_level=aug_level, bn_out_first=bn_out_first, act_out_first=act_out_first,
                                        name='res3_7')
        res3_8 = residual_unit_xception(data=res3_7, n_in_ch=288, n_out_ch=288, stride=(1, 1), dim_match=True,
                                        aug_level=aug_level, bn_out_first=bn_out_first, act_out_first=act_out_first,
                                        name='res3_8')
        in_layer_list.append(res3_8)
        if input_dict is not None:
            logging.info('res3_8: {}'.format(res3_8.infer_shape(**input_dict)[1]))

        # res5
        stride = (2, 2) if inv_resolution == 32 else (1, 1)
        res4_1 = residual_unit_xception(data=res3_8, n_in_ch=288, n_out_ch=576, stride=stride, dim_match=False,
                                        aug_level=aug_level, bn_out_first=bn_out_first, act_out_first=act_out_first,
                                        name='res4_1')
        res4_2 = residual_unit_xception(data=res4_1, n_in_ch=576, n_out_ch=576, stride=(1, 1), dim_match=True,
                                        aug_level=aug_level, bn_out_first=bn_out_first, act_out_first=act_out_first,
                                        name='res4_2')
        res4_3 = residual_unit_xception(data=res4_2, n_in_ch=576, n_out_ch=576, stride=(1, 1), dim_match=True,
                                        aug_level=aug_level, bn_out_first=bn_out_first, act_out_first=act_out_first,
                                        name='res4_3')
        res4_4 = residual_unit_xception(data=res4_3, n_in_ch=576, n_out_ch=576, stride=(1, 1), dim_match=True,
                                        aug_level=aug_level, bn_out_first=bn_out_first, act_out_first=act_out_first,
                                        name='res4_4')
        in_layer_list.append(res4_4)
        if input_dict is not None:
            logging.info('res4_4: {}'.format(res4_4.infer_shape(**input_dict)[1]))

    elif net_type == 'xception_like':
        # res3
        res2_1 = residual_unit_xception_like(data=pool_1, n_in_ch=24, n_out_ch=144, stride=(2, 2), dim_match=False,
                                             aug_level=aug_level, name='res2_1')
        res2_2 = residual_unit_xception_like(data=res2_1, n_in_ch=144, n_out_ch=144, stride=(1, 1), dim_match=True,
                                             aug_level=aug_level, name='res2_2')
        res2_3 = residual_unit_xception_like(data=res2_2, n_in_ch=144, n_out_ch=144, stride=(1, 1), dim_match=True,
                                             aug_level=aug_level, name='res2_3')
        res2_4 = residual_unit_xception_like(data=res2_3, n_in_ch=144, n_out_ch=144, stride=(1, 1), dim_match=True,
                                             aug_level=aug_level, name='res2_4')
        in_layer_list.append(res2_4)
        if input_dict is not None:
            logging.info('res2_4: {}'.format(res2_4.infer_shape(**input_dict)[1]))

        # res4
        res3_1 = residual_unit_xception_like(data=res2_4, n_in_ch=144, n_out_ch=288, stride=(2, 2), dim_match=False,
                                             aug_level=aug_level, name='res3_1')
        res3_2 = residual_unit_xception_like(data=res3_1, n_in_ch=288, n_out_ch=288, stride=(1, 1), dim_match=True,
                                             aug_level=aug_level, name='res3_2')
        res3_3 = residual_unit_xception_like(data=res3_2, n_in_ch=288, n_out_ch=288, stride=(1, 1), dim_match=True,
                                             aug_level=aug_level, name='res3_3')
        res3_4 = residual_unit_xception_like(data=res3_3, n_in_ch=288, n_out_ch=288, stride=(1, 1), dim_match=True,
                                             aug_level=aug_level, name='res3_4')
        res3_5 = residual_unit_xception_like(data=res3_4, n_in_ch=288, n_out_ch=288, stride=(1, 1), dim_match=True,
                                             aug_level=aug_level, name='res3_5')
        res3_6 = residual_unit_xception_like(data=res3_5, n_in_ch=288, n_out_ch=288, stride=(1, 1), dim_match=True,
                                             aug_level=aug_level, name='res3_6')
        res3_7 = residual_unit_xception_like(data=res3_6, n_in_ch=288, n_out_ch=288, stride=(1, 1), dim_match=True,
                                             aug_level=aug_level, name='res3_7')
        res3_8 = residual_unit_xception_like(data=res3_7, n_in_ch=288, n_out_ch=288, stride=(1, 1), dim_match=True,
                                             aug_level=aug_level, name='res3_8')
        in_layer_list.append(res3_8)
        if input_dict is not None:
            logging.info('res3_8: {}'.format(res3_8.infer_shape(**input_dict)[1]))

        # res5
        stride = (2, 2) if inv_resolution == 32 else (1, 1)
        res4_1 = residual_unit_xception_like(data=res3_8, n_in_ch=288, n_out_ch=576, stride=stride, dim_match=False,
                                             aug_level=aug_level, name='res4_1')
        res4_2 = residual_unit_xception_like(data=res4_1, n_in_ch=576, n_out_ch=576, stride=(1, 1), dim_match=True,
                                             aug_level=aug_level, name='res4_2')
        res4_3 = residual_unit_xception_like(data=res4_2, n_in_ch=576, n_out_ch=576, stride=(1, 1), dim_match=True,
                                             aug_level=aug_level, name='res4_3')
        res4_4 = residual_unit_xception_like(data=res4_3, n_in_ch=576, n_out_ch=576, stride=(1, 1), dim_match=True,
                                             aug_level=aug_level, name='res4_4')
        in_layer_list.append(res4_4)
        if input_dict is not None:
            logging.info('res4_4: {}'.format(res4_4.infer_shape(**input_dict)[1]))
    else:
        raise ValueError("no support net_type: {}".format(net_type))

    return in_layer_list

