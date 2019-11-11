from .visual import create_viz
import collections
import numpy as np
TORCH_INSTALLED = True
try:
    import torch
except Exception:
    TORCH_INSTALLED = False

def _convert_data_to_nparray(X):
    if isinstance(X, torch.Tensor):
        X = X.detach().cpu().numpy()
    elif isinstance(X, list):
        X = np.array(X)
    return X

class Plotter(object):
    """
        The highest abstraction for plotter(visualization)

        0. Support different backends including visdom, tensorboard(not implemented)
        1. Plot the metrics such as train/val loss, accuracy, etc.
        2. support image, heatmap

        Usage:

    """
    ALLOWABLE_PLOT_TYPES = ['line', 'scatter']

    def __init__(self, name, env, server='localhost', port=8097, backend='visdom'):
        super(Plotter, self).__init__()

        self.name = name
        self.backend = backend
        self.env = env
        self.server = server
        self.port = port

        if backend == 'visdom':
            self._plotter = create_viz(name, env, port, server, backend)
        elif backend == 'tensorboard':
            self._plotter = create_viz(name, env, port, server, backend)
        else:
            raise ValueError("viz type is wrong. Neither visdom nor tensorboard")

    def _legalize_multiple_plot(self, iters, vals):
        """Check and convert the input for the multiple plot in one figure.
           Supported input format:(e.g. iters, vals)
           Case a. 1, [2,3]
           Case b. [2,2], [2,3]
        """
        #TODO: Legalize (Cuda) Tensor
        if not isinstance(iters, collections.Sequence):
            iters = [iters for i in range(len(vals))]
        assert len(iters) == len(vals)
        return iters, vals

    def register_plot_type(self, plot_name, plot_type, opts={}):
        """
        Register plot such as line, scatter which needs to be updated.
        :param title:
        :param plot_type: the form you want to plot such as line, scatter, etc.
        :param opts: dict
            title: (must exist)
        :return:
        """
        opts.setdefault('title', plot_name)
        assert plot_type in self.ALLOWABLE_PLOT_TYPES
        if self.backend == 'visdom':
            self._plotter.regis_visdom_logger(plot_name, plot_type, opts)
        else:
            raise NotImplementedError()

    def update_plot(self, plot_name, X, Y=None):
        """

        :param plot_name:
        :param x: (N*K) OR (N,)
         N is the number of points will be ploted in each plot
         K is the number of plots.
        :param y: Support tensor Shape: (N*K) Or (N,)
        :return:
        """
        #TODO: Temporary. Which needs to be refactored
        # if TORCH_INSTALLED:
            # X, Y = _convert_data_to_nparray(X), _convert_data_to_nparray(Y)
        # x, y = self._legalize_multiple_plot(x, y)
        self._plotter.update_plot(plot_name, X, Y)

    def image(self, *args, **kwargs):
        self._plotter.image(*args, **kwargs)

    def images(self, imgs, opts={'title':''}):
        self._plotter.images(imgs, opts)

    def heatmap(self, *args, **kwargs):
        self._plotter.heatmap(*args, **kwargs)


class PlotterManager(object):
    def __init__(self):
        self.plt_dict = {}

    def create_plotter(self, name, env, server, port, backend, plotter_cls=Plotter):
        plotter = plotter_cls(name, env, server, port, backend)
        assert name not in self.plt_dict, "Plotter Manager: the name in plt_dict already exist"
        self.plt_dict[name] = plotter
        return plotter

def get_plotter(name=None):
    name = name if name else 'root'
    return plt_manager.plt_dict[name]


def create_plotter(name, env, server='localhost', port=8097, backend='visdom', plotter_cls=Plotter):
    name = name if name else 'root'

    plotter = plt_manager.create_plotter(name, env, server, port, backend, plotter_cls)

    return plotter


plt_manager = PlotterManager()