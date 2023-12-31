"""
functions to plot utils
"""

from .common import *


def set_bounds(limx, limy) -> sp.Polygon:
    return sp.Polygon(
        spg.Point(limx[0], limy[1]),
        spg.Point(limx[0], limy[0]),
        spg.Point(limx[1], limy[0]),
        spg.Point(limx[1], limy[1])
        )


def snapshot(folder, filename):
    import os
    sessions = os.path.expanduser('~') + '/Sessions'
    out = f'{sessions}/{folder}/'
    os.makedirs(out, exist_ok=True)
    filename = out + filename
    plt.savefig(filename, dpi=120)
    print_log(f'    * {filename}')
    return filename


def snapshot_2(folder, filename, transparent=False):
    import os
    folder = os.path.abspath(folder)
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, filename)
    plt.savefig(filename, dpi=120, transparent=transparent)
    print_log(f'    * {filename}')
    return filename


def display(filename):
    from IPython import display
    display.Image(filename)


#  def ax_prep(ax, ax_btm, bounds, xlabel):
    #  ax.clear()
    #  ax_btm.clear()
    #  ax.axis(False)
    #  ax_btm.axis(False)
    #  #  ax.spines['bottom'].set_color('k')
    #  #  ax.spines['top'].set_color('k')
    #  #  ax.spines['right'].set_color('k')
    #  #  ax.spines['left'].set_color('k')
    #  #  ax.tick_params(axis='x', colors='k')
    #  #  ax.tick_params(axis='y', colors='k')
    #  vmin = bounds.vertices[0]
    #  vmax = bounds.vertices[2]
    #  ax.set_xlim(float(vmin.x.evalf()), float(vmax.x.evalf()))
    #  ax.set_ylim(float(vmin.y.evalf()), float(vmax.y.evalf()))
    #  ax.invert_yaxis()

    #  #  ax.set_xlabel(xlabel, fontdict={'color': 'w', 'size':'20'})
    #  ax_btm.text(0.5, 0.5, xlabel, ha='center', va='center', fontdict={'color': 'w', 'size':'20'})


def adjust_ratio(w, h, ratio):
    # TODO: account for header and footer
    if w / h < ratio:
        w = ratio * h
    if w / h > ratio:
        h = w / ratio
    return w, h

def adjust_lims(limx, limy, margin_ratio=0.1):
    # TODO: adjust ratio for header footer
    w = abs(limx[1] - limx[0])
    w_margin = w * margin_ratio
    limx[0] -= w_margin
    limx[1] += w_margin
    w = abs(limx[1] - limx[0])

    h = abs(limy[1] - limy[0])
    h_margin = h * margin_ratio
    limy[0] -= h_margin
    limy[1] += h_margin
    h = abs(limy[1] - limy[0])

    #  w2, h2 = adjust_ratio(w, h)
    w2, h2 = (w, h)
    xdiff = abs(w2 - w) / 2
    ydiff = abs(h2 - h) / 2

    limx[0] -= xdiff
    limx[1] += xdiff
    limy[0] -= ydiff
    limy[1] += ydiff

    return limx, limy


def get_limits_from_points(pts):
    '''find x, y limits from a set of points'''
    limx = [0, 0]
    limy = [0, 0]
    if pts:
        pt = list(pts)[0]
        ptx = float(pt.x.evalf())
        pty = float(pt.y.evalf())
        limx[0] = ptx
        limx[1] = ptx
        limy[0] = pty
        limy[1] = pty

        for pt in pts:
            ptx = float(pt.x.evalf())
            pty = float(pt.y.evalf())
            # print(x, y)
            limx[0] = ptx if ptx < limx[0] else limx[0]
            limx[1] = ptx if ptx > limx[1] else limx[1]
            limy[0] = pty if pty < limy[0] else limy[0]
            limy[1] = pty if pty > limy[1] else limy[1]

    return limx, limy



####
# more generalized plot setup
def ax_set_bounds(ax, bounds):
    vmin = bounds.vertices[0]
    vmax = bounds.vertices[2]
    ax.set_xlim(float(vmin.x.evalf()), float(vmax.x.evalf()))
    ax.set_ylim(float(vmin.y.evalf()), float(vmax.y.evalf()))

def ax_set_spines(ax):
    ax.spines['bottom'].set_color('k')
    ax.spines['top'].set_color('k')
    ax.spines['right'].set_color('k')
    ax.spines['left'].set_color('k')
    ax.tick_params(axis='x', colors='k')
    ax.tick_params(axis='y', colors='k')

