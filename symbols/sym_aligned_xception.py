import logging


import mxnet as mx

fix_gamma = False
eps = 2e-5
bn_mom = 0.9
mirroring_level = 0
use_global_stats = False


def Separable_conv2d(data,
                     in_channels,
                     out_channels,
                     kernel,
                     pad,
                     stride=(1, 1),
                     dilate=(1, 1),
                     bias=False,
                     bn_out=False,
                     act_out=False,
                     name=None,
                     workspace=512,
                     use_deformable=False):
    # depthwise
    pad = list(pad)
    if dilate[0] > 1:
        assert use_deformable
        pad[0] = ((kernel[0] - 1) * dilate[0] + 1) // 2
    if dilate[1] > 1:
        assert use_deformable
        pad[1] = ((kernel[1] - 1) * dilate[1] + 1) // 2
    if use_deformable:
        assert kernel[0] == kernel[1]
        assert pad[0] == pad[1]
        assert stride[0] == stride[1]
        assert dilate[0] == dilate[1]
        assert dilate[0] > 1
        from sym_common import deformable_conv
        dw_out = deformable_conv(data=data,
                                 num_deformable_group=4,
                                 num_filter=in_channels,
                                 kernel=kernel[0],
                                 pad=pad[0],
                                 stride=stride[0],
                                 dilate=dilate[0],
                                 no_bias=False if bias else True,
                                 num_group=in_channels,
                                 name=name + '_conv2d_depthwise')
    else:
        dw_out = mx.sym.Convolution(data=data,
                                    num_filter=in_channels,
                                    kernel=kernel,
                                    pad=pad,
                                    stride=stride,
                                    dilate=dilate,
                                    no_bias=False if bias else True,
                                    num_group=in_channels,
                                    workspace=workspace,
                                    name=name + '_conv2d_depthwise')
    if bn_out:
        dw_out = mx.sym.BatchNorm(data=dw_out,
                                  fix_gamma=fix_gamma,
                                  eps=eps,
                                  momentum=bn_mom,
                                  use_global_stats=use_global_stats,
                                  attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                                  if mirroring_level >= 2 else {},
                                  name=name + '_conv2d_depthwise_bn')
    if act_out:
        dw_out = mx.sym.Activation(data=dw_out,
                                   act_type='relu',
                                   name=name + '_conv2d_depthwise_relu')
        if mirroring_level >= 1:
            dw_out._set_attr(force_mirroring='True')
    #pointwise
    pw_out = mx.sym.Convolution(data=dw_out,
                                num_filter=out_channels,
                                kernel=(1, 1),
                                stride=(1, 1),
                                pad=(0, 0),
                                num_group=1,
                                no_bias=False if bias else True,
                                workspace=workspace,
                                name=name + '_conv2d_pointwise')
    return pw_out


def xception_residual_norm(data,
                           in_channels,
                           out_channels,
                           kernel=(3, 3),
                           pad=(1, 1),
                           stride=(1, 1),
                           bias=False,
                           bypass_type='norm',  # 'bypass_type: norm or separable'
                           name=None,
                           workspace=512):
    assert stride[0] == stride[1]
    assert stride[0] == 1

    sep1 = mx.sym.Activation(data=data,
                             act_type='relu',
                             name=name + '_sep1_relu')
    if mirroring_level >= 1:
        sep1._set_attr(force_mirroring='True')
    sep1 = Separable_conv2d(data=sep1,
                            in_channels=in_channels,
                            out_channels=out_channels,
                            kernel=kernel,
                            pad=pad,
                            stride=stride,
                            bias=bias,
                            bn_out=True,
                            act_out=False,
                            name=name + '_sep1_conv')
    sep1 = mx.sym.BatchNorm(data=sep1,
                            fix_gamma=fix_gamma,
                            eps=eps,
                            momentum=bn_mom,
                            use_global_stats=use_global_stats,
                            attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                            if mirroring_level >= 2 else {},
                            name=name + '_sep1_bn')

    sep2 = mx.sym.Activation(data=sep1,
                             act_type='relu',
                             name=name + '_sep2_relu')
    if mirroring_level >= 1:
        sep2._set_attr(force_mirroring='True')
    sep2 = Separable_conv2d(data=sep2,
                            in_channels=out_channels,
                            out_channels=out_channels,
                            kernel=kernel,
                            pad=pad,
                            stride=stride,
                            bias=bias,
                            bn_out=True,
                            act_out=False,
                            name=name + '_sep2_conv')
    sep2 = mx.sym.BatchNorm(data=sep2,
                            fix_gamma=fix_gamma,
                            eps=eps,
                            momentum=bn_mom,
                            use_global_stats=use_global_stats,
                            attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                            if mirroring_level >= 2 else {},
                            name=name + '_sep2_bn')

    sep3 = mx.sym.Activation(data=sep2,
                             act_type='relu',
                             name=name + '_sep3_relu')
    if mirroring_level >= 1:
        sep3._set_attr(force_mirroring='True')
    sep3 = Separable_conv2d(data=sep3,
                            in_channels=out_channels,
                            out_channels=out_channels,
                            kernel=kernel,
                            pad=pad,
                            stride=stride,
                            bias=bias,
                            bn_out=True,
                            act_out=False,
                            name=name + '_sep3_conv')
    sep3 = mx.sym.BatchNorm(data=sep3,
                            fix_gamma=fix_gamma,
                            eps=eps,
                            momentum=bn_mom,
                            use_global_stats=use_global_stats,
                            attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                            if mirroring_level >= 2 else {},
                            name=name + '_sep3_bn')

    if in_channels == out_channels:
        short_cut = data
    else:
        if bypass_type == 'norm':
            short_cut = mx.sym.Convolution(data=data,
                                           num_filter=out_channels,
                                           kernel=(1, 1),
                                           stride=(1, 1),
                                           pad=(0, 0),
                                           num_group=1,
                                           no_bias=False if bias else True,
                                           workspace=workspace,
                                           name=name + '_conv2d_bypass')
            short_cut = mx.sym.BatchNorm(data=short_cut,
                                         fix_gamma=fix_gamma,
                                         eps=eps,
                                         momentum=bn_mom,
                                         use_global_stats=use_global_stats,
                                         attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                                         if mirroring_level >= 2 else {},
                                         name=name + '_bypass_bn')

        elif bypass_type == 'separable':
            short_cut = Separable_conv2d(data=data,
                                         in_channels=in_channels,
                                         out_channels=out_channels,
                                         kernel=kernel,
                                         pad=pad,
                                         stride=stride,
                                         bias=bias,
                                         bn_out=True,
                                         act_out=False,
                                         name=name + '_bypass_separable')
            short_cut = mx.sym.BatchNorm(data=short_cut,
                                         fix_gamma=fix_gamma,
                                         eps=eps,
                                         momentum=bn_mom,
                                         use_global_stats=use_global_stats,
                                         attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                                         if mirroring_level >= 2 else {},
                                         name=name + '_bypass_bn')
        else:
            raise ValueError('no suppport bypass type:{}'
                             'for xception residual norm cell'.format(bypass_type))
    out = sep3 + short_cut
    return out


def xception_residual_reduction(data,
                                in_channels,
                                out_channels,
                                kernel=(3, 3),
                                pad=(1, 1),
                                stride=(2, 2),
                                bias=False,
                                bypass_type='norm',  # 'bypass_type: norm or separable'
                                first_act=True,
                                name=None,
                                workspace=512):
    assert stride[0] == stride[1]
    assert stride[0] == 2

    if first_act:
        sep1 = mx.sym.Activation(data=data,
                                 act_type='relu',
                                 name=name + '_sep1_relu')
        if mirroring_level >= 1:
            sep1._set_attr(force_mirroring='True')
    else:
        sep1 = data
    sep1 = Separable_conv2d(data=sep1,
                            in_channels=in_channels,
                            out_channels=out_channels,
                            kernel=kernel,
                            pad=pad,
                            stride=(1, 1),
                            bias=bias,
                            bn_out=True,
                            act_out=False,
                            name=name + '_sep1_conv')
    sep1 = mx.sym.BatchNorm(data=sep1,
                            fix_gamma=fix_gamma,
                            eps=eps,
                            momentum=bn_mom,
                            use_global_stats=use_global_stats,
                            attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                            if mirroring_level >= 2 else {},
                            name=name + '_sep1_bn')

    sep2 = mx.sym.Activation(data=sep1,
                             act_type='relu',
                             name=name + '_sep2_relu')
    if mirroring_level >= 1:
        sep2._set_attr(force_mirroring='True')
    sep2 = Separable_conv2d(data=sep2,
                            in_channels=out_channels,
                            out_channels=out_channels,
                            kernel=kernel,
                            pad=pad,
                            stride=(1, 1),
                            bias=bias,
                            bn_out=True,
                            act_out=False,
                            name=name + '_sep2_conv')
    sep2 = mx.sym.BatchNorm(data=sep2,
                            fix_gamma=fix_gamma,
                            eps=eps,
                            momentum=bn_mom,
                            use_global_stats=use_global_stats,
                            attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                            if mirroring_level >= 2 else {},
                            name=name + '_sep2_bn')

    sep3 = mx.sym.Pooling(data=sep2,
                          kernel=(3, 3),
                          stride=stride,
                          pad=(1, 1),
                          pool_type="max",
                          name=name + '_sep3_max_pooling')
    if bypass_type == 'norm':
        short_cut = mx.sym.Convolution(data=data,
                                       num_filter=out_channels,
                                       kernel=(1, 1),
                                       stride=stride,
                                       pad=(0, 0),
                                       num_group=1,
                                       no_bias=False if bias else True,
                                       workspace=workspace,
                                       name=name + '_conv2d_bypass')
        short_cut = mx.sym.BatchNorm(data=short_cut,
                                     fix_gamma=fix_gamma,
                                     eps=eps,
                                     momentum=bn_mom,
                                     use_global_stats=use_global_stats,
                                     attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                                     if mirroring_level >= 2 else {},
                                     name=name + '_bypass_bn')

    elif bypass_type == 'separable':
        short_cut = Separable_conv2d(data=data,
                                     in_channels=in_channels,
                                     out_channels=out_channels,
                                     kernel=kernel,
                                     pad=pad,
                                     stride=stride,
                                     bias=bias,
                                     bn_out=True,
                                     act_out=False,
                                     name=name + '_bypass_separable')
        short_cut = mx.sym.BatchNorm(data=short_cut,
                                     fix_gamma=fix_gamma,
                                     eps=eps,
                                     momentum=bn_mom,
                                     use_global_stats=use_global_stats,
                                     attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                                     if mirroring_level >= 2 else {},
                                     name=name + '_bypass_bn')
    else:
        raise ValueError('no suppport bypass type:{}for xception residual norm cell'.format(bypass_type))
    out = sep3 + short_cut
    return out


def xception_residual_reductionbranch(data,
                                      in_channels,
                                      out_channels,
                                      kernel=(3, 3),
                                      pad=(1, 1),
                                      stride=(2, 2),
                                      bias=False,
                                      bypass_type='norm',  # 'bypass_type: norm or separable'
                                      first_act=True,
                                      name=None,
                                      workspace=512):
    assert stride[0] == stride[1]
    assert stride[0] == 2

    if first_act:
        sep1 = mx.sym.Activation(data=data,
                                 act_type='relu',
                                 name=name + '_sep1_relu')
        if mirroring_level >= 1:
            sep1._set_attr(force_mirroring='True')
    else:
        sep1 = data
    sep1 = Separable_conv2d(data=sep1,
                            in_channels=in_channels,
                            out_channels=in_channels,
                            kernel=kernel,
                            pad=pad,
                            stride=(1, 1),
                            bias=bias,
                            bn_out=True,
                            act_out=False,
                            name=name + '_sep1_conv')
    sep1 = mx.sym.BatchNorm(data=sep1,
                            fix_gamma=fix_gamma,
                            eps=eps,
                            momentum=bn_mom,
                            use_global_stats=use_global_stats,
                            attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                            if mirroring_level >= 2 else {},
                            name=name + '_sep1_bn')

    sep2 = mx.sym.Activation(data=sep1,
                             act_type='relu',
                             name=name + '_sep2_relu')
    if mirroring_level >= 1:
        sep2._set_attr(force_mirroring='True')
    sep2 = Separable_conv2d(data=sep2,
                            in_channels=in_channels,
                            out_channels=out_channels,
                            kernel=kernel,
                            pad=pad,
                            stride=(1, 1),
                            bias=bias,
                            bn_out=True,
                            act_out=False,
                            name=name + '_sep2_conv')
    sep2 = mx.sym.BatchNorm(data=sep2,
                            fix_gamma=fix_gamma,
                            eps=eps,
                            momentum=bn_mom,
                            use_global_stats=use_global_stats,
                            attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                            if mirroring_level >= 2 else {},
                            name=name + '_sep2_bn')

    sep3 = mx.sym.Pooling(data=sep2,
                          kernel=(3, 3),
                          stride=stride,
                          pad=(1, 1),
                          pool_type="max",
                          name=name + '_sep3_max_pooling')
    if bypass_type == 'norm':
        short_cut = mx.sym.Convolution(data=data,
                                       num_filter=out_channels,
                                       kernel=(1, 1),
                                       stride=stride,
                                       pad=(0, 0),
                                       num_group=1,
                                       no_bias=False if bias else True,
                                       workspace=workspace,
                                       name=name + '_conv2d_bypass')
        short_cut = mx.sym.BatchNorm(data=short_cut,
                                     fix_gamma=fix_gamma,
                                     eps=eps,
                                     momentum=bn_mom,
                                     use_global_stats=use_global_stats,
                                     attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                                     if mirroring_level >= 2 else {},
                                     name=name + '_bypass_bn')

    elif bypass_type == 'separable':
        short_cut = Separable_conv2d(data=data,
                                     in_channels=in_channels,
                                     out_channels=out_channels,
                                     kernel=kernel,
                                     pad=pad,
                                     stride=stride,
                                     bias=bias,
                                     bn_out=True,
                                     act_out=False,
                                     name=name + '_bypass_separable')
        short_cut = mx.sym.BatchNorm(data=short_cut,
                                     fix_gamma=fix_gamma,
                                     eps=eps,
                                     momentum=bn_mom,
                                     use_global_stats=use_global_stats,
                                     attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                                     if mirroring_level >= 2 else {},
                                     name=name + '_bypass_bn')
    else:
        raise ValueError('no suppport bypass type:{} for xception residual norm cell'.format(bypass_type))
    out = sep3 + short_cut
    return out


def xception_residual_reductionbranch_dilate(data,
                                             in_channels,
                                             out_channels,
                                             kernel=(3, 3),
                                             pad=(1, 1),
                                             stride=(2, 2),
                                             dilate=(1, 1),
                                             bias=False,
                                             bypass_type='norm',  # 'bypass_type: norm or separable'
                                             first_act=True,
                                             name=None,
                                             workspace=512,
                                             use_deformable=False):

    if first_act:
        sep1 = mx.sym.Activation(data=data,
                                 act_type='relu',
                                 name=name + '_sep1_relu')
        if mirroring_level >= 1:
            sep1._set_attr(force_mirroring='True')
    else:
        sep1 = data
    sep1 = Separable_conv2d(data=sep1,
                            in_channels=in_channels,
                            out_channels=in_channels,
                            kernel=kernel,
                            pad=pad,
                            stride=(1, 1),
                            dilate=dilate,
                            bias=bias,
                            bn_out=True,
                            act_out=False,
                            name=name + '_sep1_conv',
                            use_deformable=use_deformable)
    sep1 = mx.sym.BatchNorm(data=sep1,
                            fix_gamma=fix_gamma,
                            eps=eps,
                            momentum=bn_mom,
                            use_global_stats=use_global_stats,
                            attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                            if mirroring_level >= 2 else {},
                            name=name + '_sep1_bn')

    sep2 = mx.sym.Activation(data=sep1,
                             act_type='relu',
                             name=name + '_sep2_relu')
    if mirroring_level >= 1:
        sep2._set_attr(force_mirroring='True')
    sep2 = Separable_conv2d(data=sep2,
                            in_channels=in_channels,
                            out_channels=out_channels,
                            kernel=kernel,
                            pad=pad,
                            stride=(1, 1),
                            dilate=dilate,
                            bias=bias,
                            bn_out=True,
                            act_out=False,
                            name=name + '_sep2_conv',
                            use_deformable=use_deformable)
    sep2 = mx.sym.BatchNorm(data=sep2,
                            fix_gamma=fix_gamma,
                            eps=eps,
                            momentum=bn_mom,
                            use_global_stats=use_global_stats,
                            attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                            if mirroring_level >= 2 else {},
                            name=name + '_sep2_bn')

    sep3 = mx.sym.Pooling(data=sep2,
                          kernel=(3, 3),
                          stride=stride,
                          pad=(1, 1),
                          pool_type="max",
                          name=name + '_sep3_max_pooling')
    if bypass_type == 'norm':
        short_cut = mx.sym.Convolution(data=data,
                                       num_filter=out_channels,
                                       kernel=(1, 1),
                                       stride=stride,
                                       pad=(0, 0),
                                       num_group=1,
                                       no_bias=False if bias else True,
                                       workspace=workspace,
                                       name=name + '_conv2d_bypass')
        short_cut = mx.sym.BatchNorm(data=short_cut,
                                     fix_gamma=fix_gamma,
                                     eps=eps,
                                     momentum=bn_mom,
                                     use_global_stats=use_global_stats,
                                     attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                                     if mirroring_level >= 2 else {},
                                     name=name + '_bypass_bn')
    else:
        raise ValueError('no suppport bypass type:{} for xception residual norm cell'.format(bypass_type))
    out = sep3 + short_cut
    return out

def get_symbol(bypass_type='norm', repeat=16, **kwargs):
    data = kwargs['data'] if 'data' in kwargs else mx.sym.Variable(name='data')
    input_dict = kwargs['input_dict'] if 'input_dict' in kwargs else None

    conv0_data = mx.sym.Convolution(data=data,
                                    num_filter=32,
                                    kernel=(3, 3),
                                    stride=(2, 2),
                                    pad=(1, 1),
                                    no_bias=True,
                                    workspace=512,
                                    name='aligned_xception_conv0')

    conv0_data = mx.sym.BatchNorm(data=conv0_data,
                                  fix_gamma=fix_gamma,
                                  eps=eps,
                                  momentum=bn_mom,
                                  use_global_stats=use_global_stats,
                                  attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                                  if mirroring_level >= 2 else {},
                                  name='aligned_xception_conv0_bn')

    conv0_data = mx.sym.Activation(data=conv0_data,
                                   act_type='relu',
                                   name='aligned_xception_conv0_relu')
    if mirroring_level >= 1:
        conv0_data._set_attr(force_mirroring='True')

    if input_dict is not None:
        logging.info('conv0_data: {}'.format(conv0_data.infer_shape(**input_dict)[1]))

    conv1_data = mx.sym.Convolution(data=conv0_data,
                                    num_filter=64,
                                    kernel=(3, 3),
                                    stride=(1, 1),
                                    pad=(1, 1),
                                    no_bias=True,
                                    workspace=512,
                                    name='aligned_xception_conv1')

    conv1_data = mx.sym.BatchNorm(data=conv1_data,
                                  fix_gamma=fix_gamma,
                                  eps=eps,
                                  momentum=bn_mom,
                                  use_global_stats=use_global_stats,
                                  attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                                  if mirroring_level >= 2 else {},
                                  name='aligned_xception_conv1_bn')

    conv1_data = mx.sym.Activation(data=conv1_data,
                                   act_type='relu',
                                   name='aligned_xception_conv1_relu')
    if mirroring_level >= 1:
        conv1_data._set_attr(force_mirroring='True')

    if input_dict is not None:
        logging.info('conv1_data: {}'.format(conv1_data.infer_shape(**input_dict)[1]))

    stem_res = xception_residual_reduction(data=conv1_data,
                                           in_channels=64,
                                           out_channels=128,
                                           kernel=(3, 3),
                                           stride=(2, 2),
                                           pad=(1, 1),
                                           bias=False,
                                           bypass_type=bypass_type,
                                           first_act=False,
                                           name='aligned_xception_stem_res1')

    if input_dict is not None:
        logging.info('stem_res: {}'.format(stem_res.infer_shape(**input_dict)[1]))

    stem_res = xception_residual_norm(data=stem_res,
                                      in_channels=128,
                                      out_channels=256,
                                      kernel=(3, 3),
                                      stride=(1, 1),
                                      pad=(1, 1),
                                      bias=False,
                                      bypass_type=bypass_type,
                                      name='aligned_xception_stem_res2')

    if input_dict is not None:
        logging.info('stem_res: {}'.format(stem_res.infer_shape(**input_dict)[1]))

    stem_res = xception_residual_reduction(data=stem_res,
                                           in_channels=256,
                                           out_channels=256,
                                           kernel=(3, 3),
                                           stride=(2, 2),
                                           pad=(1, 1),
                                           bias=False,
                                           bypass_type=bypass_type,
                                           first_act=True,
                                           name='aligned_xception_stem_res3')

    if input_dict is not None:
        logging.info('stem_res: {}'.format(stem_res.infer_shape(**input_dict)[1]))

    stem_res = xception_residual_norm(data=stem_res,
                                      in_channels=256,
                                      out_channels=728,
                                      kernel=(3, 3),
                                      stride=(1, 1),
                                      pad=(1, 1),
                                      bias=False,
                                      bypass_type=bypass_type,
                                      name='aligned_xception_stem_res4')

    if input_dict is not None:
        logging.info('stem_res: {}'.format(stem_res.infer_shape(**input_dict)[1]))

    stem_res = xception_residual_reduction(data=stem_res,
                                           in_channels=728,
                                           out_channels=728,
                                           kernel=(3, 3),
                                           stride=(2, 2),
                                           pad=(1, 1),
                                           bias=False,
                                           bypass_type=bypass_type,
                                           first_act=True,
                                           name='aligned_xception_stem_res5')

    if input_dict is not None:
        logging.info('stem_res: {}'.format(stem_res.infer_shape(**input_dict)[1]))

    for i in range(repeat):
        index = i + 6
        stem_res = xception_residual_norm(data=stem_res,
                                          in_channels=728,
                                          out_channels=728,
                                          kernel=(3, 3),
                                          stride=(1, 1),
                                          pad=(1, 1),
                                          bias=False,
                                          bypass_type=bypass_type,
                                          name='aligned_xception_stem_res{}'.format(index))

    if input_dict is not None:
        logging.info('stem_res: {}'.format(stem_res.infer_shape(**input_dict)[1]))

    index = repeat + 6
    dilate = (2, 2)
    use_deformable=True
    stem_res = xception_residual_reductionbranch_dilate(data=stem_res,
                                                        in_channels=728,
                                                        out_channels=1024,
                                                        kernel=(3, 3),
                                                        stride=(1, 1),
                                                        dilate=dilate,
                                                        pad=(1, 1),
                                                        bias=False,
                                                        bypass_type=bypass_type,
                                                        first_act=True,
                                                        use_deformable=use_deformable,
                                                        name='aligned_xception_stem_res'.format(index))
    stem_res = mx.sym.Activation(data=stem_res,
                                 act_type='relu',
                                 name='aligned_xception_stem_res_out_relu')
    if mirroring_level >= 1:
        stem_res._set_attr(force_mirroring='True')

    if input_dict is not None:
        logging.info('stem_res: {}'.format(stem_res.infer_shape(**input_dict)[1]))

    stem_sep1 = Separable_conv2d(data=stem_res,
                                 in_channels=1024,
                                 out_channels=1536,
                                 kernel=(3, 3),
                                 pad=(1, 1),
                                 stride=(1, 1),
                                 dilate=dilate,
                                 bias=False,
                                 bn_out=True,
                                 act_out=False,
                                 use_deformable=use_deformable,
                                 name='aligned_xcepiton_stem_separable1')
    stem_sep1 = mx.sym.BatchNorm(data=stem_sep1,
                                 fix_gamma=fix_gamma,
                                 eps=eps,
                                 momentum=bn_mom,
                                 use_global_stats=use_global_stats,
                                 attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                                 if mirroring_level >= 2 else {},
                                 name='aligned_xception_stem_separable1_bn')
    stem_sep1 = mx.sym.Activation(data=stem_sep1,
                                  act_type='relu',
                                  name='aligned_xception_stem_separable1_relu')
    if mirroring_level >= 1:
        stem_sep1._set_attr(force_mirroring='True')
    if input_dict is not None:
        logging.info('stem_sep1: {}'.format(stem_sep1.infer_shape(**input_dict)[1]))

    stem_sep2 = Separable_conv2d(data=stem_sep1,
                                 in_channels=1536,
                                 out_channels=1536,
                                 kernel=(3, 3),
                                 pad=(1, 1),
                                 stride=(1, 1),
                                 dilate=dilate,
                                 bias=False,
                                 bn_out=True,
                                 act_out=False,
                                 use_deformable=use_deformable,
                                 name='aligned_xcepiton_stem_separable2')
    stem_sep2 = mx.sym.BatchNorm(data=stem_sep2,
                                 fix_gamma=fix_gamma,
                                 eps=eps,
                                 momentum=bn_mom,
                                 use_global_stats=use_global_stats,
                                 attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                                 if mirroring_level >= 2 else {},
                                 name='aligned_xception_stem_separable2_bn')
    stem_sep2 = mx.sym.Activation(data=stem_sep2,
                                  act_type='relu',
                                  name='aligned_xception_stem_separable2_relu')
    if mirroring_level >= 1:
        stem_sep2._set_attr(force_mirroring='True')
    if input_dict is not None:
        logging.info('stem_sep2: {}'.format(stem_sep2.infer_shape(**input_dict)[1]))

    stem_sep3 = Separable_conv2d(data=stem_sep2,
                                 in_channels=1536,
                                 out_channels=2048,
                                 kernel=(3, 3),
                                 pad=(1, 1),
                                 stride=(1, 1),
                                 dilate=dilate,
                                 bias=False,
                                 bn_out=True,
                                 act_out=False,
                                 use_deformable=use_deformable,
                                 name='aligned_xcepiton_stem_separable3')
    stem_sep3 = mx.sym.BatchNorm(data=stem_sep3,
                                 fix_gamma=fix_gamma,
                                 eps=eps,
                                 momentum=bn_mom,
                                 use_global_stats=use_global_stats,
                                 attr={'force_mirroring': 'True', 'cudnn_off': 'True'}
                                 if mirroring_level >= 2 else {},
                                 name='aligned_xception_stem_separable3_bn')
    stem_sep3 = mx.sym.Activation(data=stem_sep3,
                                  act_type='relu',
                                  name='aligned_xception_stem_separable3_relu')
    if mirroring_level >= 1:
        stem_sep3._set_attr(force_mirroring='True')
    if input_dict is not None:
        logging.info('stem_sep3: {}'.format(stem_sep3.infer_shape(**input_dict)[1]))

    return stem_sep3







