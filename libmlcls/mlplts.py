# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 17:40:56 2013

@author: pietro
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot3d_df(df, axes, training, name=None, fmt='png', dpi=300):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for key in training:
        ax.scatter(df[axes[0]][training[key]['ids']],
                   df[axes[1]][training[key]['ids']],
                   df[axes[2]][training[key]['ids']],
                   c=training[key]['color'],
                   marker=training[key]['marker'],
                   label=key)
    ax.set_xlabel(axes[0])
    ax.set_ylabel(axes[1])
    ax.set_zlabel(axes[2])
    ax.legend()
    plt.show()
    if name:
        plt.savefig('%s.%s' % (name, fmt), dpi=dpi, format=fmt,
                    transparent=True, bbox_inches='tight')
