import mxnet as mx

k_R = 96
G = 32
k_sec = {2: 3,
         3: 4,
         4: 20,
         5: 3}
inc_sec = {2: 16,
           3: 32,
           4: 24,
           5: 128}
bn_momentum = 0.9

def BK(data):
    return mx.symbol.BlockGrad(data=data)

# - - - - - - - - - - - - - - - - - - - - - - -
# Fundamental Elements
def BN(data, fix_gamma=False, momentum=bn_momentum, name=None):
    bn = mx.symbol.BatchNorm(data=data, fix_gamma=fix_gamma, momentum=bn_momentum, name=('%s__bn'%name))
    return bn

def AC(data, act_type='relu', name=None):
    act = mx.symbol.Activation(data=data, act_type=act_type, name=('%s__%s' % (name, act_type)))
    return act

def BN_AC(data, momentum=bn_momentum, name=None):
    bn = BN(data=data, name=name, fix_gamma=False, momentum=momentum)
    bn_ac = AC(data=bn, name=name)
    return bn_ac

def Conv(data, num_filter, kernel, stride=(1, 1), pad=(0, 0), dilate=(1, 1),
         name=None, no_bias=True, w=None, b=None, attr=None, num_group=1,
         num_deformable_group=0):
    assert w is None and b is None
    if num_deformable_group == 0:
        conv = mx.symbol.Convolution(data=data, num_filter=num_filter, num_group=num_group, kernel=kernel, pad=pad, stride=stride, dilate=dilate,
                                     name=('%s__conv' % name), no_bias=no_bias, attr=attr)
    else:
        from sym_common import deformable_conv
        assert attr is None
        conv = deformable_conv(data=data, num_filter=num_filter, num_group=num_group, kernel=kernel[0], pad=pad[0], stride=stride[0], dilate=dilate[0],
                               name=('%s__conv' % name), no_bias=no_bias, num_deformable_group=num_deformable_group)
    return conv

# - - - - - - - - - - - - - - - - - - - - - - -
# Standard Common functions < CVPR >
def Conv_BN(data, num_filter, kernel, pad, stride=(1, 1), dilate=(1, 1), name=None, w=None, b=None, no_bias=True,
            attr=None, num_group=1, num_deformable_group=0):
    cov = Conv(data=data, num_filter=num_filter, num_group=num_group, kernel=kernel, pad=pad, stride=stride, dilate=dilate,
               name=name, w=w, b=b, no_bias=no_bias, attr=attr, num_deformable_group=num_deformable_group)
    cov_bn = BN(data=cov, name=('%s__bn' % name))
    return cov_bn

def Conv_BN_AC(data, num_filter, kernel, pad, stride=(1, 1), dilate=(1, 1), name=None, w=None, b=None, no_bias=True,
               attr=None, num_group=1, num_deformable_group=0):
    cov_bn = Conv_BN(data=data, num_filter=num_filter, num_group=num_group, kernel=kernel, pad=pad, stride=stride, dilate=dilate,
                     name=name, w=w, b=b, no_bias=no_bias, attr=attr, num_deformable_group=num_deformable_group)
    cov_ba = AC(data=cov_bn, name=('%s__ac' % name))
    return cov_ba

# - - - - - - - - - - - - - - - - - - - - - - -
# Standard Common functions < ECCV >
def BN_Conv(data, num_filter, kernel, pad, stride=(1, 1), dilate=(1, 1), name=None, w=None, b=None, no_bias=True,
            attr=None, num_group=1, num_deformable_group=0):
    bn = BN(data=data, name=('%s__bn' % name))
    bn_cov = Conv(data=bn, num_filter=num_filter, num_group=num_group, kernel=kernel, pad=pad, stride=stride, dilate=dilate,
                  name=name, w=w, b=b, no_bias=no_bias, attr=attr, num_deformable_group=num_deformable_group)
    return bn_cov

def AC_Conv(data, num_filter, kernel, pad, stride=(1, 1), dilate=(1, 1), name=None, w=None, b=None, no_bias=True,
            attr=None, num_group=1, num_deformable_group=0):
    ac = AC(data=data, name=('%s__ac' % name))
    ac_cov = Conv(data=ac, num_filter=num_filter, num_group=num_group, kernel=kernel, pad=pad, stride=stride, dilate=dilate,
                  name=name, w=w, b=b, no_bias=no_bias, attr=attr, num_deformable_group=num_deformable_group)
    return ac_cov

def BN_AC_Conv(data, num_filter, kernel, pad, stride=(1, 1), dilate=(1, 1), name=None, w=None, b=None, no_bias=True,
               attr=None, num_group=1, num_deformable_group=0):
    bn = BN(data=data, name=('%s__bn' % name))
    ba_cov = AC_Conv(data=bn, num_filter=num_filter, num_group=num_group, kernel=kernel, pad=pad, stride=stride, dilate=dilate,
                     name=name, w=w, b=b, no_bias=no_bias, attr=attr, num_deformable_group=num_deformable_group)
    return ba_cov

# - - - - - - - - - - - - - - - - - - - - - - -
# Standard Dual Path Unit
def DualPathFactory(data, num_1x1_a, num_3x3_b, num_1x1_c, name, inc, G, _type='normal', dilate=1, inc_dilate=False, num_deformable_group=0):
    kw = 3
    kh = 3
    pw = ((kw - 1) * dilate + 1) // 2
    ph = ((kh - 1) * dilate + 1) // 2

    # type
    if _type is 'proj':
        key_stride = 1
        has_proj = True
    elif _type is 'down':
        key_stride = 2
        has_proj = True
    else:
        assert _type == 'normal'
        key_stride = 1
        has_proj = False
    key_stride_name = key_stride

    dilate_factor = 1
    if inc_dilate:
        assert key_stride > 1
        dilate_factor = key_stride
        key_stride = 1

    if type(data) is list:
        data_in = mx.symbol.Concat(*[data[0], data[1]], name=('%s_cat-input' % name))
    else:
        data_in = data

    if has_proj:
        c1x1_w = BN_AC_Conv(data=data_in, num_filter=(num_1x1_c+2*inc), kernel=(1, 1), stride=(key_stride, key_stride),
                            name=('%s_c1x1-w(s/%d)' % (name, key_stride_name)), pad=(0, 0))
        data_o1 = mx.symbol.slice_axis(data=c1x1_w, axis=1, begin=0, end=num_1x1_c, name=('%s_c1x1-w(s/%d)-split1' %(name, key_stride_name)))
        data_o2 = mx.symbol.slice_axis(data=c1x1_w, axis=1, begin=num_1x1_c, end=(num_1x1_c+2*inc), name=('%s_c1x1-w(s/%d)-split2' % (name, key_stride_name)))
    else:
        data_o1 = data[0]
        data_o2 = data[1]

    # MAIN
    c1x1_a = BN_AC_Conv(data=data_in, num_filter=num_1x1_a, kernel=(1, 1), pad=(0, 0), name=('%s_c1x1-a' % name))
    c3x3_b = BN_AC_Conv(data=c1x1_a, num_filter=num_3x3_b, kernel=(kw, kh), pad=(pw, ph), dilate=(dilate, dilate),
                        name=('%s_c%dx%d-b' % (name, kw, kh)), stride=(key_stride, key_stride), num_group=G,
                        num_deformable_group=num_deformable_group)
    c1x1_c = BN_AC_Conv(data=c3x3_b, num_filter=(num_1x1_c+inc), kernel=(1, 1), pad=(0, 0), name=('%s_c1x1-c' % name))
    c1x1_c1 = mx.symbol.slice_axis(data=c1x1_c, axis=1, begin=0, end=num_1x1_c, name=('%s_c1x1-c-split1' % name))
    c1x1_c2 = mx.symbol.slice_axis(data=c1x1_c, axis=1, begin=num_1x1_c, end=(num_1x1_c+inc), name=('%s_c1x1-c-split2' % name))

    # OUTPUTS
    summ = mx.symbol.ElementWiseSum(*[data_o1, c1x1_c1], name=('%s_sum' % name))
    dense = mx.symbol.Concat(*[data_o2, c1x1_c2], name=('%s_cat' % name))

    return [summ, dense], dilate * dilate_factor


def get_symbol(inv_resolution=32, num_deformable_group=0, **kwargs):
    if inv_resolution == 32:
        inc_dilate_list = [False, False, False, False]
    elif inv_resolution == 16:
        inc_dilate_list = [False, False, False, True]
    elif inv_resolution == 8:
        inc_dilate_list = [False, False, True, True]
    else:
        raise ValueError("no experiments done on resolution {}".format(inv_resolution))

    # define Dual Path Network
    data = kwargs['data'] if 'data' in kwargs else mx.sym.Variable(name='data')
    input_dict = {'data': (2, 3, 512, 512), 'rois': (2, 4, 5)}

    # conv1
    conv1_x_1 = Conv(data=data, num_filter=64, kernel=(7, 7), name='conv1_x_1', pad=(3, 3), stride=(2, 2))
    conv1_x_1 = BN_AC(conv1_x_1, name='conv1_x_1__relu-sp')
    conv1_x_x = mx.symbol.Pooling(data=conv1_x_1, pool_type="max", kernel=(3, 3), pad=(1, 1), stride=(2, 2), name="pool1")
    print conv1_x_x.infer_shape(**input_dict)[1]  # [(8L, 64L, 88L, 64L)]

    # conv2
    dilate = 1
    bw = 256
    inc = inc_sec[2]
    R = (k_R*bw)/256
    conv2_x_x, dilate = DualPathFactory(conv1_x_x, R, R, bw, 'conv2_x__1', inc, G, 'proj', dilate=dilate, inc_dilate=inc_dilate_list[0])
    for i_ly in range(2, k_sec[2]+1):
        conv2_x_x, _ = DualPathFactory(conv2_x_x, R, R, bw, ('conv2_x__%d' % i_ly), inc, G, 'normal', dilate=dilate, inc_dilate=False)
    print conv2_x_x[0].infer_shape(**input_dict)[1]  # [(8L, 256L, 88L, 64L)]
    print conv2_x_x[1].infer_shape(**input_dict)[1]  # [(8L, 80L, 88L, 64L)]

    # conv3
    bw = 512
    inc = inc_sec[3]
    R = (k_R*bw)/256
    conv3_x_x, dilate = DualPathFactory(conv2_x_x, R, R, bw, 'conv3_x__1', inc, G, 'down', dilate=dilate, inc_dilate=inc_dilate_list[1])
    for i_ly in range(2, k_sec[3]+1):
        conv3_x_x, _ = DualPathFactory(conv3_x_x, R, R, bw, ('conv3_x__%d' % i_ly), inc, G, 'normal', dilate=dilate, inc_dilate=False)
    print conv3_x_x[0].infer_shape(**input_dict)[1]  # [(8L, 512L, 44L, 32L)]
    print conv3_x_x[1].infer_shape(**input_dict)[1]  # [(8L, 192L, 44L, 32L)]

    # conv4
    bw = 1024
    inc = inc_sec[4]
    R = (k_R*bw)/256
    conv4_x_x, dilate = DualPathFactory(conv3_x_x, R, R, bw, 'conv4_x__1', inc, G, 'down', dilate=dilate, inc_dilate=inc_dilate_list[2])
    for i_ly in range(2, k_sec[4]+1):
        conv4_x_x, _ = DualPathFactory(conv4_x_x, R, R, bw, ('conv4_x__%d' % i_ly), inc, G, 'normal', dilate=dilate, inc_dilate=False)
    print conv4_x_x[0].infer_shape(**input_dict)[1]  # [(8L, 1024L, 22L, 16L)]
    print conv4_x_x[1].infer_shape(**input_dict)[1]  # [(8L, 528L, 22L, 16L)]

    # conv5
    bw = 2048
    inc = inc_sec[5]
    R = (k_R*bw)/256
    conv5_x_x, dilate = DualPathFactory(conv4_x_x, R, R, bw, 'conv5_x__1', inc, G, 'down', dilate=dilate, inc_dilate=inc_dilate_list[3],
                                        num_deformable_group=num_deformable_group)
    for i_ly in range(2, k_sec[5]+1):
        conv5_x_x, _ = DualPathFactory(conv5_x_x, R, R, bw, ('conv5_x__%d' % i_ly), inc, G, 'normal', dilate=dilate, inc_dilate=False,
                                       num_deformable_group=num_deformable_group)
    print conv5_x_x[0].infer_shape(**input_dict)[1]  # [(8L, 2048L, 11L, 8L)]
    print conv5_x_x[1].infer_shape(**input_dict)[1]  # [(8L, 640L, 11L, 8L)]

    # output: concat
    conv5_x_x = mx.symbol.Concat(*[conv5_x_x[0], conv5_x_x[1]], name='conv5_x_x_cat-final')
    conv5_x_x = BN_AC(conv5_x_x, name='conv5_x_x__relu-sp')
    print conv5_x_x.infer_shape(**input_dict)[1]  # [(8L, 2688L, 11L, 8L)]

    return conv5_x_x


if __name__ == "__main__":
    data_shape = (1, 3, 2048, 2048)
    net_symbol = get_symbol()
    #output_shape = net_symbol.infer_shape(data=data_shape)
    #print('network output shape:', output_shape[1])
