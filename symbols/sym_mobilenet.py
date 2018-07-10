import mxnet as mx
import logging

use_global_stats = True

def Conv(data, num_filter, kernel, stride, pad, depth_mult=1, name=None, suffix='', bn_mom=0.9, workspace=512):
    conv = mx.sym.Convolution(data=data, num_filter=num_filter, kernel=kernel, num_group=depth_mult,
                              stride=stride, pad=pad, no_bias=True, workspace=workspace, name='%s%s' % (name, suffix))
    bn = mx.sym.BatchNorm(data=conv, fix_gamma=False, eps=2e-5, use_global_stats=use_global_stats,
                          momentum=bn_mom, name='%s%s_bn' % (name, suffix))
    act = mx.sym.Activation(data=bn, act_type='relu', name='%s%s_relu' % (name, suffix))
    return act


def separable_conv_order(data, n_in_ch, n_out_ch, kernel, stride, pad, depth_mult=1, order=True, act_out_first=True,
                         bn_out_first=True, act_out_second=True, bn_out_second=True, name=None, suffix='', bn_mom=0.9,
                         workspace=512):
    if order:
        dw_out = mx.sym.Convolution(data=data, num_filter=n_in_ch, kernel=kernel, num_group=depth_mult, stride=stride,
                                    pad=pad, no_bias=True, workspace=workspace, name='%s%s_dw' % (name, suffix))
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
    else:
        pw_out = mx.sym.Convolution(data=data, num_filter=n_in_ch, kernel=(1, 1), stride=(1, 1),
                                    pad=(0, 0), num_group=1, no_bias=True, workspace=workspace,
                                    name='%s%s_pw' % (name, suffix))
        if bn_out_first:
            pw_out = mx.sym.BatchNorm(data=pw_out, fix_gamma=False, eps=2e-5, momentum=bn_mom,
                                      use_global_stats=use_global_stats, name='%s%s_pw_bn' % (name, suffix))
        if act_out_first:
            pw_out = mx.sym.Activation(data=pw_out, act_type='relu', name='%s%s_pw_relu' % (name, suffix))
        dw_out = mx.sym.Convolution(data=pw_out, num_filter=n_out_ch, kernel=kernel, num_group=depth_mult,
                                    stride=stride, pad=pad, no_bias=True, workspace=workspace,
                                    name='%s%s_dw' % (name, suffix))
        if bn_out_second:
            dw_out = mx.sym.BatchNorm(data=dw_out, fix_gamma=False, eps=2e-5, momentum=bn_mom,
                                      use_global_stats=use_global_stats, name='%s%s_bw_bn' % (name, suffix))
        if act_out_second:
            dw_out = mx.sym.Activation(data=dw_out, act_type='relu', name='%s%s_bw_relu' % (name, suffix))
        return dw_out


def get_symbol(alpha=0.5, inv_resolution=32, **kwargs):
    assert inv_resolution == 16 or inv_resolution == 32
    input_dict = kwargs['input_dict'] if 'input_dict' in kwargs else None
    data = kwargs['data'] if 'data' in kwargs else mx.sym.Variable(name='data')
    in_layer_list = []
    order = True
    bn_mom = 0.9
    workspace = 512

    conv1 = Conv(data, num_filter=int(32 * alpha), kernel=(3, 3), stride=(2, 2), pad=(1, 1), bn_mom=bn_mom,
                 workspace=workspace, name="conv1")
    conv2_dep_1 = separable_conv_order(conv1, n_in_ch=int(32 * alpha), n_out_ch=int(64 * alpha), kernel=(3, 3),
                                       stride=(1, 1), pad=(1, 1), depth_mult=int(32 * alpha), order=order,
                                       name='conv2_dep_1')

    # res2
    conv2_dep_2 = separable_conv_order(conv2_dep_1, n_in_ch=int(64 * alpha), n_out_ch=int(128 * alpha), kernel=(3, 3),
                                       stride=(2, 2), pad=(1, 1), depth_mult=int(64 * alpha), order=order,
                                       name='conv2_dep_2')
    conv3_dep_1 = separable_conv_order(conv2_dep_2, n_in_ch=int(128 * alpha), n_out_ch=int(128 * alpha), kernel=(3, 3),
                                       stride=(1, 1), pad=(1, 1), depth_mult=int(128 * alpha), order=order,
                                       name='conv3_dep_1')
    in_layer_list.append(conv3_dep_1)
    if input_dict is not None:
        logging.info('conv3_dep_1: {}'.format(conv3_dep_1.infer_shape(**input_dict)[1]))

    # res3
    conv3_dep_2 = separable_conv_order(conv3_dep_1, n_in_ch=int(128 * alpha), n_out_ch=int(256 * alpha), kernel=(3, 3),
                                       stride=(2, 2), pad=(1, 1), depth_mult=int(128 * alpha), order=order,
                                       name='conv3_dep_2')
    conv4_dep_1 = separable_conv_order(conv3_dep_2, n_in_ch=int(256 * alpha), n_out_ch=int(256 * alpha), kernel=(3, 3),
                                       stride=(1, 1), pad=(1, 1), depth_mult=int(256 * alpha), order=order,
                                       name='conv4_dep_1')
    in_layer_list.append(conv4_dep_1)
    if input_dict is not None:
        logging.info('conv4_dep_1: {}'.format(conv4_dep_1.infer_shape(**input_dict)[1]))

    # res4
    conv4_dep_2 = separable_conv_order(conv4_dep_1, n_in_ch=int(256 * alpha), n_out_ch=int(512 * alpha), kernel=(3, 3),
                                       stride=(2, 2), pad=(1, 1), depth_mult=int(256 * alpha), order=order,
                                       name='conv4_dep_2')
    conv5_dep_1 = separable_conv_order(conv4_dep_2, n_in_ch=int(512 * alpha), n_out_ch=int(512 * alpha), kernel=(3, 3),
                                       stride=(1, 1), pad=(1, 1), depth_mult=int(512 * alpha), order=order,
                                       name='conv5_dep_1')
    conv5_dep_2 = separable_conv_order(conv5_dep_1, n_in_ch=int(512 * alpha), n_out_ch=int(512 * alpha), kernel=(3, 3),
                                       stride=(1, 1), pad=(1, 1), depth_mult=int(512 * alpha), order=order,
                                       name='conv5_dep_2')
    conv5_dep_3 = separable_conv_order(conv5_dep_2, n_in_ch=int(512 * alpha), n_out_ch=int(512 * alpha), kernel=(3, 3),
                                       stride=(1, 1), pad=(1, 1), depth_mult=int(512 * alpha), order=order,
                                       name='conv5_dep_3')
    conv5_dep_4 = separable_conv_order(conv5_dep_3, n_in_ch=int(512 * alpha), n_out_ch=int(512 * alpha), kernel=(3, 3),
                                       stride=(1, 1), pad=(1, 1), depth_mult=int(512 * alpha), order=order,
                                       name='conv5_dep_4')
    conv5_dep_5 = separable_conv_order(conv5_dep_4, n_in_ch=int(512 * alpha), n_out_ch=int(512 * alpha), kernel=(3, 3),
                                       stride=(1, 1), pad=(1, 1), depth_mult=int(512 * alpha), order=order,
                                       name='conv5_dep_5')
    in_layer_list.append(conv5_dep_5)
    if input_dict is not None:
        logging.info('conv5_dep_5: {}'.format(conv5_dep_5.infer_shape(**input_dict)[1]))

    # res5
    stride = (2, 2) if inv_resolution == 32 else (1, 1)
    conv5_dep_6 = separable_conv_order(conv5_dep_5, n_in_ch=int(512 * alpha), n_out_ch=int(1024 * alpha), kernel=(3, 3),
                                       stride=stride, pad=(1, 1), depth_mult=int(512 * alpha), order=order,
                                       name='conv5_dep_6')
    conv6_sep_1 = separable_conv_order(conv5_dep_6, n_in_ch=int(1024 * alpha), n_out_ch=int(1024 * alpha),
                                       kernel=(3, 3), stride=(1, 1), pad=(1, 1), depth_mult=int(1024 * alpha),
                                       order=order, name='conv6_dep_1')
    in_layer_list.append(conv6_sep_1)
    if input_dict is not None:
        logging.info('conv6_sep_1: {}'.format(conv6_sep_1.infer_shape(**input_dict)[1]))

    return in_layer_list
