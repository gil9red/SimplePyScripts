#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/llSourcell/deep_dream_challenge

# IF    "FutureWarning: Conversion of the second argument of issubdtype from `float` to `np.floating` is deprecated"
# THEN: pip3 install h5py==2.8.0rc1

# pip install tensorflow
import tensorflow as tf
import numpy as np
import PIL.Image
import matplotlib.pyplot as plt
import urllib.request
import os
import zipfile


def main():
    # Step 1 - download google's pre-trained neural network
    url = 'https://storage.googleapis.com/download.tensorflow.org/models/inception5h.zip'
    data_dir = 'data/'
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    model_name = os.path.split(url)[-1]
    local_zip_file = os.path.join(data_dir, model_name)
    if not os.path.exists(local_zip_file):
        # Download
        model_url = urllib.request.urlopen(url)
        with open(local_zip_file, 'wb') as output:
            output.write(model_url.read())
        # Extract
        with zipfile.ZipFile(local_zip_file, 'r') as zip_ref:
            zip_ref.extractall(data_dir)

    # start with a gray image with a little noise
    img_noise = np.random.uniform(size=(224, 224, 3)) + 100.0

    model_fn = 'tensorflow_inception_graph.pb'

    # Step 2 - Creating Tensorflow session and loading the model
    graph = tf.Graph()
    sess = tf.InteractiveSession(graph=graph)

    with tf.gfile.FastGFile(os.path.join(data_dir, model_fn), 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    t_input = tf.placeholder(np.float32, name='input')  # define the input tensor
    imagenet_mean = 117.0
    t_preprocessed = tf.expand_dims(t_input - imagenet_mean, 0)
    tf.import_graph_def(graph_def, {'input': t_preprocessed})

    layers = [op.name for op in graph.get_operations() if op.type == 'Conv2D' and 'import/' in op.name]
    feature_nums = [int(graph.get_tensor_by_name(name + ':0').get_shape()[-1]) for name in layers]

    print('Number of layers', len(layers))
    print('Total number of feature channels:', sum(feature_nums))

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

    def showarray(a):
        a = np.uint8(np.clip(a, 0, 1) * 255)
        plt.imshow(a)
        plt.show()

    def savearray(a, file_name):
        a = np.uint8(np.clip(a, 0, 1) * 255)
        PIL.Image.fromarray(a).save(file_name)

    def visstd(a, s=0.1):
        '''Normalize the image range for visualization'''
        return (a - a.mean()) / max(a.std(), 1e-4) * s + 0.5

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

    def tffunc(*argtypes):
        '''Helper that transforms TF-graph generating function into a regular one.
        See "resize" function below.
        '''
        placeholders = list(map(tf.placeholder, argtypes))

        def wrap(f):
            out = f(*placeholders)

            def wrapper(*args, **kw):
                return out.eval(dict(zip(placeholders, args)), session=kw.get('session'))

            return wrapper

        return wrap

    def resize(img, size):
        img = tf.expand_dims(img, 0)
        return tf.image.resize_bilinear(img, size)[0, :, :, :]

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

    def render_deepdream(t_obj, sess, img0=img_noise, iter_n=10, step=1.5, octave_n=4, octave_scale=1.4):
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

    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    savearray(img_noise / 255.0, '{}/noise.png'.format(output_dir, 'noise'))

    # FROM noise
    layer = 'mixed4c'
    t_obj = tf.square(T(layer))
    img = render_deepdream(t_obj, sess)
    # showarray(img / 255.0)
    savearray(img / 255.0, '{}/{}_{}.png'.format(output_dir, 'noise', layer))

    # FROM filename
    t_obj = tf.square(T(layer))
    img0 = PIL.Image.open('pilatus800.jpg')
    img0 = np.float32(img0)
    img = render_deepdream(t_obj, sess, img0)
    savearray(img / 255.0, '{}/{}_{}.png'.format(output_dir, 'pilatus800', layer))

    # FROM filters
    layer = 'mixed4d_3x3_bottleneck_pre_relu'
    filter_name = {'Tornado': 84, 'Flowers': 139, 'Fireworks': 50, 'Caves': 38, 'Mountains': 142, 'Van Gogh': 1}
    for name, channel in filter_name.items():
        t_obj = tf.square(T(layer)[:, :, :, channel])
        img = render_deepdream(t_obj, sess, img0)
        savearray(img / 255.0, '{}/{}_{}_{}.png'.format(output_dir, 'pilatus800', name, layer))

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
    #
    # filter_name = {'Tornado': 84, 'Flowers': 139, 'Fireworks': 50, 'Caves': 38, 'Mountains': 142, 'Van Gogh': 1}
    # for name, channel in filter_name.items():
    #     t_obj = tf.square(T(layer)[:, :, :, channel])
    #     img = render_deepdream(t_obj, sess, img0)
    #     savearray(img / 255.0, 'output/output_{}.png'.format(name))


if __name__ == '__main__':
    main()
