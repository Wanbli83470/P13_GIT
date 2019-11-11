import sys;
sys.path.append("./")
sys.path.append("../")

from plus.visual import create_plotter
import numpy as np

import torch

# the arg format needs to refer to Class Plotter in the visual.plotter
pltter = create_plotter('main', env='test', server='localhost', port=2018, backend='visdom')

# Registeration
pltter.register_plot_type(plot_name='test_scatter', plot_type='scatter')
pltter.register_plot_type(plot_name='train_loss', plot_type='line',
                          opts={'title':'test_plot_line', 'legend': ['l1','l2','l3']})

# Plot
X =  np.array([[1,1,1], [2,2,2], [3,3,3], [4,4,4]])
Y =  np.array([[1,4,3], [2,4,5], [1.5,5,4], [3,3,6]])

# X = np.array([1,2,3,4])
# Y = np.array([1,4,2,3])
pltter.update_plot('train_loss', X, Y)

# X = torch.Tensor([5,6,7,8])
X =  np.array([[5,5,5], [6,6,6], [7,7,7], [8,8,8]])
Y = torch.Tensor([[1,4,3], [2,4,5], [1.5,5,4], [3,3,6]])
pltter.update_plot('train_loss', X, Y)



# pltter.register_plot_type(plot_type='line', opts={'title':'test_plot_line_append'})
# np array
# iters = np.array([[1,1], [2,2], [3,3]])
# vals = np.array([[2,4],[1,5], [3,6]])


# iters = np.random.rand(255, 2)
# vals = (np.random.rand(255) + 1.5).astype(int)

# pltter.update_plot('test_plot_line', iters, vals)
# import ipdb;ipdb.set_trace()
# pltter.update_plot('test_plot_scatter', iters, Y=None)
# tensor

# tensor on gpu





