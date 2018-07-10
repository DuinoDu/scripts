import mxnet as mx

def Conv(data, num_filter, kernel, stride, pad, depth_mult=1, name=None, suffix='', bn_mom=0.9, workspace=512):
    conv = mx.sym.Convolution(data=data, num_filter=num_filter, kernel=kernel, num_group=depth_mult,
                              stride=stride, pad=pad, no_bias=True, workspace=workspace, name='%s%s' % (name, suffix))
    bn = mx.sym.BatchNorm(data=conv, fix_gamma=False, eps=2e-5, momentum=bn_mom, name='%s%s_bn' % (name, suffix))
    act = mx.sym.Activation(data=bn, act_type='relu', name='%s%s_relu' % (name, suffix))
    return act

def separable_conv(data, n_in_ch, n_out_ch, kernel, stride, dilate=(1, 1), depth_mult=1,
                   name=None, suffix='', bn_mom=0.9, workspace=512):
    # depthwise
    pad_h = ((kernel[0] - 1) * dilate[0] + 1) // 2
    pad_w = ((kernel[1] - 1) * dilate[1] + 1) // 2
    dw_out = mx.sym.Convolution(data=data, num_filter=n_in_ch, kernel=kernel, num_group=depth_mult,
                                stride=stride, pad=(pad_h, pad_w), dilate=dilate, no_bias=True, workspace=workspace,
                                name='%s%s_dw' % (name, suffix))
    # pointwise
    pw_out = mx.sym.Convolution(data=dw_out, num_filter=n_out_ch, kernel=(1, 1), stride=(1, 1),
                                pad=(0, 0), num_group=1, no_bias=True, workspace=workspace,
                                name='%s%s_pw' % (name, suffix))
    return pw_out

def residual_unitA(data, n_in_ch, n_out_ch1, n_out_ch2, dim_match, act_first=False, dilate=1, inc_dilate=False,
                   name=None, suffix='', bn_mom=0.9, workspace=512):
    dilate_factor = 1
    stride = 2
    if inc_dilate:
        assert stride > 1
        dilate_factor = stride
        stride = 1

    if act_first:
        data = mx.sym.Activation(data=data, act_type='relu', name=name + '_relu1')
    sep_out1 = separable_conv(data, n_in_ch=n_in_ch, n_out_ch=n_out_ch1, kernel=(3, 3), stride=(1, 1),
                              dilate=(dilate, dilate), depth_mult=n_in_ch, name=name + '_sp1', suffix=suffix,
                              bn_mom=bn_mom, workspace=workspace)
    sep_out1_bn = mx.sym.BatchNorm(data=sep_out1, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name + '_sp1_bn')
    act_out2 = mx.sym.Activation(data=sep_out1_bn, act_type='relu', name=name + '_relu2')

    sep_out2 = separable_conv(act_out2, n_in_ch=n_out_ch1, n_out_ch=n_out_ch2, kernel=(3, 3), stride=(1, 1),
                              depth_mult=n_out_ch1, name=name + '_sp2', suffix=suffix,
                              bn_mom=bn_mom, workspace=workspace)
    sep_out2_bn = mx.sym.BatchNorm(data=sep_out2, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name + '_sp2_bn')

    pool_out = mx.symbol.Pooling(data=sep_out2_bn, kernel=(3, 3), stride=(stride, stride), pad=(1, 1), pool_type='max', name=name + '_pool')
    if dim_match:
        short_cut = data
    else:
        short_cut = mx.sym.Convolution(data=data, num_filter=n_out_ch2, kernel=(1, 1), stride=(stride, stride), pad=(0, 0),
                                       no_bias=True, workspace=workspace, name=name + '_sc')
        short_cut = mx.sym.BatchNorm(data=short_cut, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name + '_sc_bn')
    return pool_out + short_cut, dilate * dilate_factor

def residual_unitB(data, n_in_ch, n_out_ch1, n_out_ch2, n_out_ch3, dim_match, dilate=1, name=None, suffix='', bn_mom=0.9, workspace=512):
    # first separable_conv
    act_out1 = mx.sym.Activation(data=data, act_type='relu', name=name + '_relu1')
    sep_out1 = separable_conv(act_out1, n_in_ch=n_in_ch, n_out_ch=n_out_ch1, kernel=(3, 3), stride=(1, 1), dilate=(dilate, dilate),
                              depth_mult=n_in_ch, name=name + '_sp1', suffix=suffix, bn_mom=bn_mom, workspace=workspace)
    sep_out1_bn = mx.sym.BatchNorm(data=sep_out1, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name + '_sp1_bn')
    # second separable_conv
    act_out2 = mx.sym.Activation(data=sep_out1_bn, act_type='relu', name=name + '_relu2')
    sep_out2 = separable_conv(act_out2, n_in_ch=n_out_ch1, n_out_ch=n_out_ch2, kernel=(3, 3), stride=(1, 1),
                              depth_mult=n_out_ch1, name=name + '_sp2', suffix=suffix, bn_mom=bn_mom, workspace=workspace)
    sep_out2_bn = mx.sym.BatchNorm(data=sep_out2, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name + '_sp2_bn')
    # third separable_conv
    act_out3 = mx.sym.Activation(data=sep_out2_bn, act_type='relu', name=name + '_relu3')
    sep_out3 = separable_conv(act_out3, n_in_ch=n_out_ch2, n_out_ch=n_out_ch3, kernel=(3, 3), stride=(1, 1),
                              depth_mult=n_out_ch2, name=name + '_sp3', suffix=suffix, bn_mom=bn_mom, workspace=workspace)
    sep_out3_bn = mx.sym.BatchNorm(data=sep_out3, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name + '_sp3_bn')
    if dim_match:
        short_cut = data
    else:
        short_cut = mx.sym.Convolution(data=data, num_filter=n_out_ch3, kernel=(1, 1), stride=(1, 1), pad=(0, 0),
                                       no_bias=True, workspace=workspace, name=name + '_sc')
        short_cut = mx.sym.BatchNorm(data=short_cut, fix_gamma=False, eps=2e-5, momentum=bn_mom, name=name + '_sc_bn')
    return sep_out3_bn + short_cut

def get_symbol(inv_resolution=32, **kwargs):
    bn_mom = 0.9
    workspace = 512
    if inv_resolution == 32:
        inc_dilate_list = [False, False, False, False]
    elif inv_resolution == 16:
        inc_dilate_list = [False, False, False, True]
    elif inv_resolution == 8:
        inc_dilate_list = [False, False, True, True]
    else:
        raise ValueError("no experiments done on resolution {}".format(inv_resolution))

    data = kwargs['data'] if 'data' in kwargs else mx.sym.Variable(name='data')
    # data_shape = (4, 3, 352, 256)

    # conv1
    conv1_1 = Conv(data, num_filter=32, kernel=(3, 3), stride=(2, 2), pad=(0, 0), bn_mom=bn_mom, workspace=workspace, name="conv1_1")
    conv1_2 = Conv(conv1_1, num_filter=64, kernel=(3, 3), stride=(1, 1), pad=(0, 0), bn_mom=bn_mom, workspace=workspace,name="conv1_2")
    # print conv1_1.infer_shape(data=data_shape)[1]
    # print conv1_2.infer_shape(data=data_shape)[1]

    # conv2 block
    dilate = 1
    res2, dilate = residual_unitA(conv1_2, n_in_ch=64, n_out_ch1=128, n_out_ch2=128, act_first=False, dim_match=False,
                                  dilate=dilate, inc_dilate=inc_dilate_list[0], name='conv2')
    # print res2.infer_shape(data=data_shape)[1]

    # conv3 block
    res3, dilate = residual_unitA(res2, n_in_ch=128, n_out_ch1=256, n_out_ch2=256, act_first=True, dim_match=False,
                                  dilate=dilate, inc_dilate=inc_dilate_list[1], name='conv3')
    # print res3.infer_shape(data=data_shape)[1]

    # conv 4  block
    res4, dilate = residual_unitA(res3, n_in_ch=256, n_out_ch1=728, n_out_ch2=728, act_first=True, dim_match=False,
                                  dilate=dilate, inc_dilate=inc_dilate_list[2], name='conv4')
    # print res4.infer_shape(data=data_shape)[1]

    # conv5 block
    res5_1 = residual_unitB(res4, n_in_ch=728, n_out_ch1=728, n_out_ch2=728, n_out_ch3=728, dim_match=True, dilate=dilate, name='conv5_1')
    res5_2 = residual_unitB(res5_1, n_in_ch=728, n_out_ch1=728, n_out_ch2=728, n_out_ch3=728, dim_match=True, dilate=dilate, name='conv5_2')
    res5_3 = residual_unitB(res5_2, n_in_ch=728, n_out_ch1=728, n_out_ch2=728, n_out_ch3=728, dim_match=True, dilate=dilate, name='conv5_3')
    res5_4 = residual_unitB(res5_3, n_in_ch=728, n_out_ch1=728, n_out_ch2=728, n_out_ch3=728, dim_match=True, dilate=dilate, name='conv5_4')
    res5_5 = residual_unitB(res5_4, n_in_ch=728, n_out_ch1=728, n_out_ch2=728, n_out_ch3=728, dim_match=True, dilate=dilate, name='conv5_5')
    res5_6 = residual_unitB(res5_5, n_in_ch=728, n_out_ch1=728, n_out_ch2=728, n_out_ch3=728, dim_match=True, dilate=dilate, name='conv5_6')
    res5_7 = residual_unitB(res5_6, n_in_ch=728, n_out_ch1=728, n_out_ch2=728, n_out_ch3=728, dim_match=True, dilate=dilate, name='conv5_7')
    res5_8 = residual_unitB(res5_7, n_in_ch=728, n_out_ch1=728, n_out_ch2=728, n_out_ch3=728, dim_match=True, dilate=dilate, name='conv5_8')
    # print res5_8.infer_shape(data=data_shape)[1]

    # conv6 block
    res6, dilate = residual_unitA(res5_8, n_in_ch=728, n_out_ch1=728, n_out_ch2=1024, act_first=True, dim_match=False,
                                  dilate=dilate, inc_dilate=inc_dilate_list[3], name='conv6')
    # print res6.infer_shape(data=data_shape)[1]

    # conv7
    conv7 = separable_conv(res6, n_in_ch=1024, n_out_ch=1536, kernel=(3, 3), stride=(1, 1), dilate=(dilate, dilate), depth_mult=1024, name='conv7')
    conv7_bn = mx.sym.BatchNorm(data=conv7, fix_gamma=False, eps=2e-5, momentum=bn_mom, name='conv7_bn')
    conv7_act = mx.sym.Activation(data=conv7_bn, act_type='relu', name='conv7_relu')
    # print conv7_act.infer_shape(data=data_shape)[1]

    # conv8
    conv8 = separable_conv(conv7_act, n_in_ch=1536, n_out_ch=2048, kernel=(3, 3), stride=(1, 1), dilate=(dilate, dilate), depth_mult=1536, name='conv8')
    conv8_bn = mx.sym.BatchNorm(data=conv8, fix_gamma=False, eps=2e-5, momentum=bn_mom, name='conv8_bn')
    conv8_act = mx.sym.Activation(data=conv8_bn, act_type='relu', name='conv8_relu')
    # print conv8_act.infer_shape(data=data_shape)[1]

    return conv8_act











