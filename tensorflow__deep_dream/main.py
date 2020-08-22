#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# MOTE: То, что эта нейронная сеть делает называется "Инцепционизм" -- картины, «написанные» нейронными сетями.

# SOURCE: https://github.com/llSourcell/deep_dream_challenge

# OTHER:
#     https://github.com/llSourcell/deep_dream_challenge/blob/master/deep_dream.py
#     https://github.com/samkit-jain/Data-Science-by-Siraj-Raval/blob/a66b7791a4628f815dc683605dd224acad9bc277/deep_dream_challenge.py#L149
#     https://medium.com/@mrubash1/deepdream-accelerating-deep-learning-with-hardware-5085ea415d8a
#     https://github.com/mrubash1/DeepDream_Streaming_Video/tree/master/src
#     https://github.com/mrubash1/DeepDream_Streaming_Video/blob/master/src/deep_dream.py
#     https://github.com/mrubash1/DeepDream_Streaming_Video/blob/master/src/app.py

# Статьи на русском о DeepDream:
#     https://habrahabr.ru/company/io/blog/262267/
#     https://meduza.io/shapito/2015/06/19/hudozhnik-ot-gugla-neyronnye-seti-nauchilis-pisat-kartiny
#     https://meduza.io/galleries/2015/06/19/intseptsionizm

# LAYERS:
#     http://storage.googleapis.com/deepdream/visualz/tensorflow_inception/index.html
#
#     import requests
#     rs = requests.get('http://storage.googleapis.com/deepdream/visualz/tensorflow_inception/index.html')
#
#     from bs4 import BeautifulSoup
#     root = BeautifulSoup(rs.content, 'html.parser')
#     layers = [a.text for a in root.select('a')]
#     print(layers)  # ['conv2d0_pre_relu', 'conv2d1_pre_relu', 'conv2d2_pre_relu', 'head0_bottleneck_pre_relu', ...


# ABOUT CODE:
#     http://nbviewer.jupyter.org/github/tensorflow/tensorflow/blob/master/tensorflow/examples/tutorials/deepdream/deepdream.ipynb


# NOTE: "FutureWarning: Conversion of the second argument of issubdtype from `float` to `np.floating` is deprecated"
#       pip3 install h5py==2.8.0rc1

import os
import io
from timeit import default_timer

# pip install tensorflow==1.15
# pip install tensorflow-gpu==1.15
# pip install tensorflow
import tensorflow as tf
import numpy as np
import PIL.Image
# import matplotlib.pyplot as plt

from common import download_tensorflow_model, IMG_NOISE, showarray, savearray


# # Helper functions for TF Graph visualization
# # pylint: disable=unused-variable
# def strip_consts(graph_def, max_const_size=32):
#     """Strip large constant values from graph_def."""
#     strip_def = tf.GraphDef()
#     for n0 in graph_def.node:
#         n = strip_def.node.add()  # pylint: disable=maybe-no-member
#         n.MergeFrom(n0)
#         if n.op == 'Const':
#             tensor = n.attr['value'].tensor
#             size = len(tensor.tensor_content)
#             if size > max_const_size:
#                 tensor.tensor_content = "<stripped %d bytes>" % size
#     return strip_def

# def rename_nodes(graph_def, rename_func):
#     res_def = tf.GraphDef()
#     for n0 in graph_def.node:
#         n = res_def.node.add()  # pylint: disable=maybe-no-member
#         n.MergeFrom(n0)
#         n.name = rename_func(n.name)
#         for i, s in enumerate(n.input):
#             n.input[i] = rename_func(s) if s[0] != '^' else '^' + rename_func(s[1:])
#     return res_def

# def showarray(a):
#     a = np.uint8(np.clip(a, 0, 1) * 255)
#     plt.imshow(a)
#     plt.show()
#
# def savearray(a, file_name):
#     print('save:', file_name)
#
#     a = np.uint8(np.clip(a, 0, 1) * 255)
#     PIL.Image.fromarray(a).save(file_name)
#
# def visstd(a, s=0.1):
#     '''Normalize the image range for visualization'''
#     return (a - a.mean()) / max(a.std(), 1e-4) * s + 0.5

def T(layer):
    '''Helper for getting layer output tensor'''
    return graph.get_tensor_by_name("import/%s:0" % layer)


# def render_naive(t_obj, img0=img_noise, iter_n=20, step=1.0):
#     t_score = tf.reduce_mean(t_obj)  # defining the optimization objective
#     t_grad = tf.gradients(t_score, t_input)[0]  # behold the power of automatic differentiation!
#
#     img = img0.copy()
#     for _ in range(iter_n):
#         g, _ = sess.run([t_grad, t_score], {t_input: img})
#         # normalizing the gradient, so the same step size should work
#         g /= g.std() + 1e-8  # for different layers and networks
#         img += g * step
#     showarray(visstd(img))

data_dir = 'data/'

# Step 1 - download google's pre-trained neural network
download_tensorflow_model(data_dir)

model_fn = 'tensorflow_inception_graph.pb'

# Step 2 - Creating Tensorflow session and loading the model
graph = tf.Graph()
sess = tf.compat.v1.InteractiveSession(graph=graph)

with tf.io.gfile.GFile(os.path.join(data_dir, model_fn), 'rb') as f:
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(f.read())

t_input = tf.compat.v1.placeholder(np.float32, name='input')  # define the input tensor
imagenet_mean = 117.0
t_preprocessed = tf.expand_dims(t_input - imagenet_mean, 0)
tf.import_graph_def(graph_def, {'input': t_preprocessed})

layers = [op.name for op in graph.get_operations() if op.type == 'Conv2D' and 'import/' in op.name]
feature_nums = [int(graph.get_tensor_by_name(name + ':0').get_shape()[-1]) for name in layers]

print('Number of layers', len(layers))
print('Total number of feature channels:', sum(feature_nums))

# import webbrowser
# for layer in layers:
#     # "import/conv2d0_pre_relu/conv" -> "conv2d0_pre_relu"
#     name = layer.split('/')[1]
#     url = f'http://storage.googleapis.com/deepdream/visualz/tensorflow_inception/{name}.html'
#     webbrowser.open(url)


output_dir = 'output'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)


def tffunc(*argtypes):
    '''Helper that transforms TF-graph generating function into a regular one.
    See "resize" function below.
    '''
    placeholders = list(map(tf.compat.v1.placeholder, argtypes))

    def wrap(f):
        out = f(*placeholders)

        def wrapper(*args, **kw):
            return out.eval(dict(zip(placeholders, args)), session=kw.get('session'))

        return wrapper

    return wrap


def resize(img, size):
    img = tf.expand_dims(img, 0)
    return tf.compat.v1.image.resize_bilinear(img, size)[0, :, :, :]


resize = tffunc(np.float32, np.int32)(resize)


def calc_grad_tiled(img, t_grad, sess, tile_size=512):
    '''Compute the value of tensor t_grad over the image in a tiled way.
    Random shifts are applied to the image to blur tile boundaries over
    multiple iterations.'''
    sz = tile_size
    h, w = img.shape[:2]
    sx, sy = np.random.randint(sz, size=2)
    img_shift = np.roll(np.roll(img, sx, 1), sy, 0)
    grad = np.zeros_like(img)
    for y in range(0, max(h - sz // 2, sz), sz):
        for x in range(0, max(w - sz // 2, sz), sz):
            sub = img_shift[y:y + sz, x:x + sz]
            g = sess.run(t_grad, {t_input: sub})
            grad[y:y + sz, x:x + sz] = g
    return np.roll(np.roll(grad, -sx, 1), -sy, 0)


# TODO: TEST THIS
# SOURCE: https://github.com/samkit-jain/Data-Science-by-Siraj-Raval/blob/a66b7791a4628f815dc683605dd224acad9bc277/deep_dream_challenge.py#L149
def render_deepdreamvideo(sess):
    import imageio
    reader = imageio.get_reader('cockatoo.mp4')
    fps = reader.get_meta_data()['fps']
    writer = imageio.get_writer('output.mp4', fps=fps)

    for i, image in enumerate(reader):
        image = np.float32(image)

        # Apply gradient ascent to that layer and append to video
        image = writer.append_data(render_deepdream(tf.square(T('mixed4c')), sess, image))
        writer.append_data(image)

    writer.close()


def render_deepdream(t_obj, sess, img0=IMG_NOISE, iter_n=10, step=1.5, octave_n=4, octave_scale=1.4):
    t_score = tf.reduce_mean(t_obj)  # defining the optimization objective
    t_grad = tf.gradients(t_score, t_input)[0]  # behold the power of automatic differentiation!

    # split the image into a number of octaves
    img = img0
    octaves = []
    for _ in range(octave_n - 1):
        hw = img.shape[:2]
        lo = resize(img, np.int32(np.float32(hw) / octave_scale))
        hi = img - resize(lo, hw)
        img = lo
        octaves.append(hi)

    # generate details octave by octave
    for octave in range(octave_n):
        if octave > 0:
            hi = octaves[-octave]
            img = resize(img, hi.shape[:2]) + hi
        for _ in range(iter_n):
            g = calc_grad_tiled(img, t_grad, sess)
            img += g * (step / (np.abs(g).mean() + 1e-7))

        # # this will usually be like 3 or 4 octaves
        # # Step 5 output deep dream image via matplotlib
        # showarray(img / 255.0)

    return img


def render_deepdream_from_layer_by_channel(img0, name, layer, channel=None):
    t = default_timer()

    # t_obj = tf.square(T(layer)[:, :, :, channel])
    t_obj = T(layer)
    if channel:
        t_obj = t_obj[:, :, :, channel]

    # t_obj = tf.square(t_obj)
    img = render_deepdream(t_obj, sess, img0)

    if isinstance(name, str):
        if channel:
            file_name = f'{output_dir}/{name}__{layer}__{channel}.jpg'
        else:
            file_name = f'{output_dir}/{name}__{layer}.jpg'
    else:
        file_name = name

    savearray(img / 255.0, file_name)

    print(f'Elapsed {default_timer() - t:.2f} secs')
    print()


def main():
    #
    # # PRINT: layer by channels
    # t_obj_layers = [x.split('/')[1] for x in layers]
    # for l in t_obj_layers:
    #     print(l, int(T(l).get_shape()[-1]))
    #

    # Layer: mixed4d_5x5
    # Url:   http://storage.googleapis.com/deepdream/visualz/tensorflow_inception/mixed4d_5x5_pre_relu.html
    # Url:   https://microscope.openai.com/models/inceptionv1/mixed4d_5x5_0/1

    savearray(IMG_NOISE / 255.0, '{}/noise.png'.format(output_dir, 'noise'))
    print()

    # layer = 'mixed4c'
    # t_obj = tf.square(T(layer))
    img0 = PIL.Image.open('pilatus800.jpg')
    img0 = np.float32(img0)

    # FROM NOISE
    render_deepdream_from_layer_by_channel(IMG_NOISE, 'noise', 'mixed4d_5x5_pre_relu', 61)
    render_deepdream_from_layer_by_channel(IMG_NOISE, 'noise', 'head1_bottleneck_pre_relu', 1)

    # FROM FILENAME
    render_deepdream_from_layer_by_channel(img0, 'pilatus800', 'mixed4d_1x1_pre_relu', 39)
    render_deepdream_from_layer_by_channel(img0, 'pilatus800', 'mixed4d_5x5_pre_relu', 61)
    render_deepdream_from_layer_by_channel(img0, 'pilatus800', 'mixed4c_3x3_bottleneck_pre_relu', 64)
    render_deepdream_from_layer_by_channel(img0, 'pilatus800', 'mixed4c_3x3_bottleneck_pre_relu', 104)

    # Save to memory
    bytes_io = io.BytesIO()
    render_deepdream_from_layer_by_channel(IMG_NOISE, bytes_io, 'mixed4d_5x5_pre_relu', 61)
    bytes_io.seek(0)
    print(bytes_io.read(10))
    # b'\xff\xd8\xff\xe0\x00\x10JFIF'

    # # PROCESS FROM ALL LAYERS
    # # ['conv2d0_pre_relu', 'conv2d1_pre_relu', 'conv2d2_pre_relu', 'mixed3a_1x1_pre_relu', ...
    # t_obj_layers = [x.split('/')[1] for x in layers]
    # for name in t_obj_layers:
    #     render_deepdream_from_layer_by_channel(img0, name)
    #     # t_obj = tf.square(T(layer))
    #     # img = render_deepdream(t_obj, sess, img0)
    #     # savearray(img / 255.0, '{}/{}_{}.png'.format(output_dir, 'pilatus800', layer))

    # # FROM filters
    # layer = 'mixed4d_3x3_bottleneck_pre_relu'
    # filter_name = {'Tornado': 84, 'Flowers': 139, 'Fireworks': 50, 'Caves': 38, 'Mountains': 142, 'Van Gogh': 1}
    # for name, channel in filter_name.items():
    #     t_obj = tf.square(T(layer)[:, :, :, channel])
    #     img = render_deepdream(t_obj, sess, img0)
    #     savearray(img / 255.0, '{}/{}_{}_{}.png'.format(output_dir, 'pilatus800', name, layer))

    # TODO: test
    # render_deepdreamvideo(sess)

    #
    #
    # # Step 3 - Pick a layer to enhance our image
    # layer = 'mixed4d_3x3_bottleneck_pre_relu'
    # channel = 139  # picking some feature channel to visualize
    #
    # # img0 = img_noise
    #
    # # open image
    # img0 = PIL.Image.open('pilatus800.jpg')
    # img0 = np.float32(img0)
    #
    # # showarray(img0)
    #
    # # # # Step 4 - Apply gradient ascent to that layer
    # # # render_deepdream(tf.square(T('mixed4c')), img0)
    # # # t_obj = tf.square(T('mixed4c'))
    # # t_obj = tf.square(T(layer)[:, :, :, channel])
    # # img = render_deepdream(t_obj, sess, img0)
    # # # img = render_deepdream(tf.square(T('mixed4c')), sess, img0)
    # # # showarray(img / 255.0)
    # # savearray(img / 255.0, 'output.png')
    #
    # print(T('mixed4d_3x3_bottleneck_pre_relu'))
    # print(T('mixed4c'))
    # # print(T('abc'))
    # quit()


if __name__ == '__main__':
    main()
