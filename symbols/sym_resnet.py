import logging
import numpy as np
import mxnet as mx
import sym_common as sym
from sym_common import cfg, remove_batch_norm_paras

def get_resnet_params(num_layer, inv_resolution=32):
    if num_layer == 18:
        units = [2, 2, 2, 2]
    elif num_layer == 26:
        units = [3, 3, 3, 3]
    elif num_layer == 34:
        units = [3, 4, 6, 3]
    elif num_layer == 50:
        units = [3, 4, 6, 3]
    elif num_layer == 101:
        units = [3, 4, 23, 3]
    elif num_layer == 152:
        units = [3, 8, 36, 3]
    elif num_layer == 200:
        units = [3, 24, 36, 3]
    elif num_layer == 269:
        units = [3, 30, 48, 8]
    else:
        raise ValueError("no experiments done on detph {}, you can do it youself".format(num_layer))
    filter_list = [256, 512, 1024, 2048] if num_layer >= 50 else [64, 128, 256, 512]
    bottle_neck = True if num_layer >= 50 else False
    if inv_resolution == 32:
        inc_dilate_list = [False, False, False, False]
    elif inv_resolution == 16:
        inc_dilate_list = [False, False, False, True]
    elif inv_resolution == 8:
        inc_dilate_list = [False, False, True, True]
    else:
        raise ValueError("no experiments done on resolution {}".format(inv_resolution))
    return units, filter_list, bottle_neck, inc_dilate_list

def non_local_block(data, num_filter, mode, prefix=''):
    mid_num_filter = int(num_filter * 0.5)
    if mode == 'gaussian':
        x_reshape = mx.sym.Reshape(data=data, shape=(0, 0, -1))
        f = mx.sym.batch_dot(x_reshape, x_reshape, transpose_a=True, transpose_b=False)
        f = mx.sym.SoftmaxActivation(data=f, mode='channel')
    elif 'embedded_gaussian' in mode:
        x1 = sym.conv(data=data, name=prefix + 'conv_x1', num_filter=mid_num_filter)
        x2 = sym.conv(data=data, name=prefix + 'conv_x2', num_filter=mid_num_filter)
        if 'compress' in mode:
            x1 = sym.pool(data=x1, name=prefix + 'pool_x1', kernel=3, stride=2, pad=1, pool_type='max')
        x1_reshape = mx.sym.Reshape(data=x1, shape=(0, 0, -1))
        x2_reshape = mx.sym.Reshape(data=x2, shape=(0, 0, -1))
        f = mx.sym.batch_dot(x1_reshape, x2_reshape, transpose_a=True, transpose_b=False)
        f = mx.sym.SoftmaxActivation(data=f, mode='channel')
    else:
        raise ValueError("unknown non-local mode {}".format(mode))

    g = sym.conv(data=data, name=prefix + 'conv_g', num_filter=mid_num_filter)
    if mode == 'embedded_gaussian_compress':
        g_pool = sym.pool(data=g, name=prefix + 'pool_g', kernel=3, stride=2, pad=1, pool_type='max')
    else:
        g_pool = g
    g_reshape = mx.sym.Reshape(data=g_pool, shape=(0, 0, -1))
    y = mx.sym.batch_dot(g_reshape, f)
    y = mx.sym.reshape_like(y, g)
    y = sym.conv(data=y, name=prefix + 'conv_y', num_filter=num_filter)
    return data + y

def resnet_residual_unit(data, num_filter, stride, dim_match, num_deformable_group=0,
                         dilate=1, inc_dilate=False, bottle_neck=True, prefix=''):
    dilate_factor = 1
    if inc_dilate:
        assert stride > 1
        dilate_factor = stride
        stride = 1
    if bottle_neck:
        bn1, relu1, conv1 = sym.bnreluconv(data=data, num_filter=int(num_filter * 0.25),
                                           kernel=1, stride=1,
                                           prefix=prefix, suffix='1')
        bn2, relu2, conv2 = sym.bnreluconv(data=conv1, num_filter=int(num_filter * 0.25),
                                           num_deformable_group=num_deformable_group,
                                           kernel=3, stride=stride, dilate=dilate,
                                           prefix=prefix, suffix='2')
        bn3, relu3, conv = sym.bnreluconv(data=conv2, num_filter=num_filter,
                                          kernel=1, stride=1,
                                          prefix=prefix, suffix='3')
    else:
        bn1, relu1, conv1 = sym.bnreluconv(data=data, num_filter=num_filter,
                                           no_bias=False if cfg.absorb_bn else True,
                                           num_deformable_group=num_deformable_group,
                                           kernel=3, stride=stride, dilate=dilate,
                                           prefix=prefix, suffix='1')
        bn2, relu2, conv = sym.bnreluconv(data=conv1, num_filter=num_filter,
                                          absorb_bn=cfg.absorb_bn,
                                          kernel=3, stride=1, dilate=1,
                                          prefix=prefix, suffix='2')
    if dim_match:
        shortcut = data
    else:
        shortcut = sym.conv(data=relu1, name=prefix + 'sc', num_filter=num_filter,
                            kernel=1, stride=stride, no_bias=True)
    return conv + shortcut, dilate * dilate_factor

def resnet_v1_residual_unit(data, num_filter, stride, dim_match, num_deformable_group=0,
                            dilate=1, inc_dilate=False, bottle_neck=True, prefix=''):
    dilate_factor = 1
    if inc_dilate:
        assert stride > 1
        dilate_factor = stride
        stride = 1
    if bottle_neck:
        conv1, bn1, relu1 = sym.convbnrelu(data=data, num_filter=int(num_filter * 0.25),
                                           kernel=1, stride=1,
                                           prefix=prefix, suffix='1')
        conv2, bn2, relu2 = sym.convbnrelu(data=relu1, num_filter=int(num_filter * 0.25),
                                           num_deformable_group=num_deformable_group,
                                           kernel=3, stride=stride, dilate=dilate,
                                           prefix=prefix, suffix='2')
        conv3, bn = sym.convbn(data=relu2, num_filter=num_filter,
                               kernel=1, stride=1,
                               prefix=prefix, suffix='3')
    else:
        conv1, bn1, relu1 = sym.convbnrelu(data=data, num_filter=num_filter,
                                           num_deformable_group=num_deformable_group,
                                           kernel=3, stride=stride, dilate=dilate,
                                           prefix=prefix, suffix='1')
        conv2, bn = sym.convbn(data=relu1, num_filter=num_filter,
                               kernel=3, stride=1, dilate=1,
                               prefix=prefix, suffix='2')
    if dim_match:
        shortcut = data
    else:
        _, shortcut = sym.convbn(data=data, num_filter=num_filter,
                                 kernel=1, stride=stride, no_bias=True,
                                 prefix=prefix, suffix='sc')
    res_relu = mx.sym.Activation(data=bn + shortcut, act_type='relu', name=prefix + 'relu')
    return res_relu, dilate * dilate_factor

def get_symbol(num_layer, net_type='resnet', inv_resolution=32, non_local_mode=None,
               use_dilate=True, deformable_units=[0, 0, 0, 0], num_deformable_group=[0, 0, 0, 0],
               prefix='', **kwargs):
    cfg.bn_use_global_stats = kwargs['bn_use_global_stats'] if 'bn_use_global_stats' in kwargs else True
    cfg.bn_eps = 2e-5
    units, filter_list, bottle_neck, inc_dilate_list = get_resnet_params(num_layer, inv_resolution)
    assert len(units) == 4
    assert len(num_deformable_group) == 4
    assert len(deformable_units) == 4

    input_dict = kwargs['input_dict'] if 'input_dict' in kwargs else None
    data = kwargs['data'] if 'data' in kwargs else mx.sym.Variable(name='data')

    if net_type == 'resnet':
        residual_unit = resnet_residual_unit
        body = sym.bn(data=data, name=prefix + 'bn_data', fix_gamma=True)
    elif net_type == 'resnet_v1':
        residual_unit = resnet_v1_residual_unit
        body = data
    elif net_type == 'resnet_v2':
        residual_unit = resnet_residual_unit
        body = data
    else:
        raise ValueError("unknown net type {}".format(net_type))

    # res1
    _, _, body = sym.convbnrelu(data=body, num_filter=64, kernel=7, stride=2, pad=3, prefix=prefix, suffix='0')
    body = sym.pool(data=body, name=prefix + 'pool0', kernel=3, stride=2, pad=1, pool_type='max')

    in_layer_list = []
    dilate = 1
    # res2
    body, dilate = residual_unit(data=body, num_filter=filter_list[0], stride=1,
                                 num_deformable_group=num_deformable_group[0] if 1 >= units[0] - deformable_units[0] + 1 else 0,
                                 dim_match=False, dilate=dilate, inc_dilate=inc_dilate_list[0],
                                 bottle_neck=bottle_neck, prefix=prefix + 'stage1_unit1_')
    dilate = dilate if use_dilate else 1
    for i in range(2, units[0] + 1):
        body, _ = residual_unit(data=body, num_filter=filter_list[0], stride=1,
                                num_deformable_group=num_deformable_group[0] if i >= units[0] - deformable_units[0] + 1 else 0,
                                dim_match=True, dilate=dilate, inc_dilate=False,
                                bottle_neck=bottle_neck, prefix=prefix + 'stage1_unit%d_' % i)
    in_layer_list.append(body)
    if input_dict is not None:
        logging.info('res2: {}'.format(body.infer_shape(**input_dict)[1]))

    # res3
    body, dilate = residual_unit(data=body, num_filter=filter_list[1], stride=2,
                                 num_deformable_group=num_deformable_group[1] if 1 >= units[1] - deformable_units[1] + 1 else 0,
                                 dim_match=False, dilate=dilate, inc_dilate=inc_dilate_list[1],
                                 bottle_neck=bottle_neck, prefix=prefix + 'stage2_unit1_')
    dilate = dilate if use_dilate else 1
    for i in range(2, units[1] + 1):
        body, _ = residual_unit(data=body, num_filter=filter_list[1], stride=1,
                                num_deformable_group=num_deformable_group[1] if i >= units[1] - deformable_units[1] + 1 else 0,
                                dim_match=True, dilate=dilate, inc_dilate=False,
                                bottle_neck=bottle_neck, prefix=prefix + 'stage2_unit%d_' % i)
    in_layer_list.append(body)
    if input_dict is not None:
        logging.info('res3: {}'.format(body.infer_shape(**input_dict)[1]))

    # res4
    body, dilate = residual_unit(data=body, num_filter=filter_list[2], stride=2,
                                 num_deformable_group=num_deformable_group[2] if 1 >= units[2] - deformable_units[2] + 1 else 0,
                                 dim_match=False, dilate=dilate, inc_dilate=inc_dilate_list[2],
                                 bottle_neck=bottle_neck, prefix=prefix + 'stage3_unit1_')
    dilate = dilate if use_dilate else 1
    for i in range(2, units[2] + 1):
        body, _ = residual_unit(data=body, num_filter=filter_list[2], stride=1,
                                num_deformable_group=num_deformable_group[2] if i >= units[2] - deformable_units[2] + 1 else 0,
                                dim_match=True, dilate=dilate, inc_dilate=False,
                                bottle_neck=bottle_neck, prefix=prefix + 'stage3_unit%d_' % i)
        # if i == units[2] - 1 and non_local_mode is not None:
        #     body = non_local_block(body, num_filter=filter_list[2], mode=non_local_mode)
        #     if input_dict is not None:
        #         logging.info('non_local_res4: {}'.format(body.infer_shape(**input_dict)[1]))
    in_layer_list.append(body)
    if input_dict is not None:
        logging.info('res4: {}'.format(body.infer_shape(**input_dict)[1]))

    # res5
    body, dilate = residual_unit(data=body, num_filter=filter_list[3], stride=2,
                                 num_deformable_group=num_deformable_group[3] if 1 >= units[3] - deformable_units[3] + 1 else 0,
                                 dim_match=False, dilate=dilate, inc_dilate=inc_dilate_list[3],
                                 bottle_neck=bottle_neck, prefix=prefix + 'stage4_unit1_')
    dilate = dilate if use_dilate else 1
    for i in range(2, units[3] + 1):
        body, _ = residual_unit(data=body, num_filter=filter_list[3], stride=1,
                                num_deformable_group=num_deformable_group[3] if i >= units[3] - deformable_units[3] + 1 else 0,
                                dim_match=True, dilate=dilate, inc_dilate=False,
                                bottle_neck=bottle_neck, prefix=prefix + 'stage4_unit%d_' % i)
    in_layer_list.append(body)
    if input_dict is not None:
        logging.info('res5: {}'.format(body.infer_shape(**input_dict)[1]))

    if net_type == 'resnet' or net_type == 'resnet_v2':
        bn1 = sym.bn(data=body, name=prefix + 'bn1', fix_gamma=False)
        relu1 = sym.relu(data=bn1, name=prefix + 'relu1')
        in_layer_list.append(relu1)

    return in_layer_list

def get_cls_symbol(num_classes=1000):
    body = get_symbol(num_layer=18, net_type='resnet_v1', bn_use_global_stats=False)[-1]
    pool1 = mx.sym.Pooling(data=body, global_pool=True, kernel=(7, 7), pool_type='avg', name='pool1')
    flat = mx.sym.Flatten(data=pool1)
    fc1 = mx.sym.FullyConnected(data=flat, num_hidden=num_classes, name='fc1')
    loss = mx.sym.SoftmaxOutput(data=fc1, name='softmax')
    return loss

def resnet_absorb_bn(arg_params, aux_params):
    aux_param_names = [_ for _ in aux_params]
    aux_param_names.sort()
    for aux_param_name in aux_param_names:
        if 'moving_mean' in aux_param_name:
            bn_name = aux_param_name[:len(aux_param_name) - len('_moving_mean')]
            if bn_name == 'stage1_unit1_bn1' or bn_name == 'bn_data' or bn_name == 'bn1':
                continue
            def _absorb_bn(conv_name):
                moving_mean = aux_params.pop(bn_name + '_moving_mean').asnumpy()
                moving_var = aux_params.pop(bn_name + '_moving_var').asnumpy()
                gamma = arg_params.pop(bn_name + '_gamma').asnumpy()
                beta = arg_params.pop(bn_name + '_beta').asnumpy()
                assert conv_name + '_bias' not in arg_params
                weight = arg_params[conv_name + '_weight'].asnumpy()
                bias = np.zeros((weight.shape[0],), dtype=np.float32)
                v, c = remove_batch_norm_paras(weight, bias, moving_mean, moving_var, gamma, beta)
                arg_params[conv_name + '_weight'] = mx.nd.array(v)
                arg_params[conv_name + '_bias'] = mx.nd.array(c)
            if bn_name == 'bn0':
                conv_name = 'conv0'
                _absorb_bn(conv_name)
            else:
                ss = bn_name.split('_')
                assert len(ss) == 3 and ss[0][:-1] == 'stage' and ss[1][:-1] == 'unit' and ss[2][:-1] == 'bn'
                stage_n = int(ss[0][-1])
                unit_n = int(ss[1][-1])
                bn_n = int(ss[2][-1])
                if bn_n > 1:
                    conv_name = 'stage%d_unit%d_conv%d' % (stage_n, unit_n, bn_n - 1)
                    _absorb_bn(conv_name)

def resnet_v1_absorb_bn(arg_params, aux_params):
    aux_param_names = [_ for _ in aux_params]
    aux_param_names.sort()
    for aux_param_name in aux_param_names:
        if 'moving_mean' in aux_param_name:
            bn_name = aux_param_name[:len(aux_param_name) - len('_moving_mean')]
            moving_mean = aux_params.pop(bn_name + '_moving_mean').asnumpy()
            moving_var = aux_params.pop(bn_name + '_moving_var').asnumpy()
            gamma = arg_params.pop(bn_name + '_gamma').asnumpy()
            beta = arg_params.pop(bn_name + '_beta').asnumpy()
            conv_name = bn_name.replace('bn', 'conv')
            assert conv_name + '_bias' not in arg_params
            weight = arg_params[conv_name + '_weight'].asnumpy()
            bias = np.zeros((weight.shape[0],), dtype=np.float32)
            v, c = remove_batch_norm_paras(weight, bias, moving_mean, moving_var, gamma, beta)
            arg_params[conv_name + '_weight'] = mx.nd.array(v)
            arg_params[conv_name + '_bias'] = mx.nd.array(c)
    assert len(aux_params) == 0
    for arg_param_name in arg_params:
        assert 'weight' in arg_param_name or 'bias' in arg_param_name

def absorb_bn(model_prefix, epoch, net_type):
    from common.utils.utils import load_param
    cfg.absorb_bn = True
    arg_params, aux_params = load_param(model_prefix, epoch)
    if net_type == 'resnet':
        resnet_absorb_bn(arg_params, aux_params)
    else:
        assert net_type == 'resnet_v1'
        resnet_v1_absorb_bn(arg_params, aux_params)
    model_prefix += '-absorb-bn'
    mx.model.save_checkpoint(model_prefix, epoch, None, arg_params, aux_params)
    return model_prefix


# def resnext_residual_unit(data, num_filter, stride, dim_match, num_deformable_group=0, num_group=32,
#                           dilate=1, inc_dilate=False, bottle_neck=True, prefix=''):
#     dilate_factor = 1
#     if inc_dilate:
#         assert stride > 1
#         dilate_factor = stride
#         stride = 1
#     if bottle_neck:
#         conv1, bn1, relu1 = sym.convbnrelu(data=data, num_filter=int(num_filter * 0.5),
#                                            kernel=1, stride=1,
#                                            prefix=prefix, suffix='1')
#         if num_deformable_group > 0:
#             conv2, bn2, relu2 = sym.dcnbnrelu(data=relu1, num_filter=int(num_filter * 0.5),
#                                               num_deformable_group=num_deformable_group,
#                                               kernel=3, stride=stride,
#                                               dilate=dilate, num_group=num_group,
#                                               prefix=prefix, suffix='2')
#         else:
#             conv2, bn2, relu2 = sym.convbnrelu(data=relu1, num_filter=int(num_filter * 0.5),
#                                                kernel=3, stride=stride,
#                                                dilate=dilate, num_group=num_group,
#                                                prefix=prefix, suffix='2')
#         conv3, bn = sym.convbn(data=relu2, num_filter=num_filter,
#                                kernel=1, stride=1,
#                                prefix=prefix, suffix='3')
#     else:
#         assert num_deformable_group == 0
#         conv1, bn1, relu1 = sym.convbnrelu(data=data, num_filter=num_filter,
#                                            kernel=3, stride=stride, dilate=dilate,
#                                            prefix=prefix, suffix='1')
#         conv2, bn = sym.convbn(data=relu1, num_filter=num_filter,
#                                kernel=3, stride=1, dilate=1,
#                                prefix=prefix, suffix='2')
#     if dim_match:
#         shortcut = data
#     else:
#         shortcut_conv = sym.conv(data=data, name=prefix + 'sc', num_filter=num_filter, kernel=1, stride=stride, no_bias=True)
#         shortcut = sym.bn(data=shortcut_conv, name=prefix + 'sc_bn', fix_gamma=False)
#     res_relu = mx.sym.Activation(data=bn + shortcut, act_type='relu', name=prefix + 'relu')
#     return res_relu, dilate * dilate_factor
