from svgpathtools import svg2paths2
from math import ceil
import numpy as np
import turtle
import re
from fire import Fire


def head_to(t, x, y, draw=True, offset_x=0, offset_y=0):
    wasdown = t.isdown()
    heading = t.towards(x + offset_x, y - offset_y)
    t.pen(pendown=draw)
    t.seth(heading)
    t.clearstamps()
    t.stamp()
    t.goto(x + offset_x, y - offset_y)
    t.pen(pendown=wasdown)

    dstr = f'''
wasdown = t.isdown()
heading = t.towards({x + offset_x}, {y - offset_y})
t.pen(pendown={draw})
t.seth(heading)
t.clearstamps()
t.stamp()
t.goto({x + offset_x}, {y - offset_y})
t.pen(pendown=wasdown)
'''
    return dstr

def draw_polygon(t, poly, fill='black', offset_x=0, offset_y=0):
    dstr = f't.color("{fill}", "{fill}")\n'
    t.color(fill,fill)
    p = poly[0]
    dstr += head_to(t,p[0],-(p[1]), False, offset_x=offset_x, offset_y=offset_y)
    for p in poly[1:]: 
        dstr += head_to(t,p[0],-(p[1]), offset_x=offset_x, offset_y=offset_y)
    t.up()
    dstr += 't.up()\n'
    return dstr

def draw_multipolygon(t, mpoly, fill='black', offset_x=0, offset_y=0):
    dstr = ''
    p = mpoly[0][0]
    dstr += head_to(t,p[0],-(p[1]), False, offset_x=offset_x, offset_y=offset_y)
    dstr += 't.begin_fill()\n'
    t.begin_fill()
    for i, poly in enumerate(mpoly):
        dstr += draw_polygon(t, poly, fill, offset_x=offset_x, offset_y=offset_y)
        if i!=0:
            dstr += head_to(t,p[0],-(p[1]), False, offset_x=offset_x, offset_y=offset_y)
    t.end_fill()
    dstr += 't.end_fill()\n'
    return dstr


def main(svg_file, speed=100, output_py='svg.py'):
    """
    Main function.
    Args:
        svg_file: SVG file to be converted to turtle commands.
        speed: Speed of turtle, higher is faster.
    """
    paths, attrs, svg_attr = svg2paths2(svg_file)
    svg_size = int(float(svg_attr['viewBox'].split()[-2])), int(float(svg_attr['viewBox'].split()[-1]))
    mx = max(svg_size)

    seg_res = 5
    polys = []
    for path in paths:
        poly = []
        for subpaths in path.continuous_subpaths():
            points = []
            for seg in subpaths:
                interp_num = ceil(seg.length()/seg_res)
                points.append(seg.point(np.arange(interp_num) / interp_num))
            if len(points) > 1:
                points = np.concatenate(points)
                points = np.append(points, points[0])
                poly.append(points)
        polys.append([[(p.real, p.imag) for p in pl] for pl in poly])

    turtle.Screen()
    t = turtle

    t.reset()
    t.setworldcoordinates(-50, -(mx+50), mx+50, 50)
    t.mode(mode='world')
    t.tracer(n=speed, delay=0)
    dstr = f"""
import turtle
turtle.Screen()
t = turtle

t.reset()
t.setworldcoordinates(-50, -({mx+50}), {mx+50}, 50)
t.mode(mode='world')
t.tracer(n={speed}, delay=0)
"""

    for poly, attr in zip(polys, attrs):
        args = {
            't': t,
            'mpoly': poly,
        }
        if 'fill' in attr:
            args['fill'] = attr['fill']
        elif 'style' in attr:
            m = re.findall(r'fill:\s*(#[a-zA-Z0-9]{6})', attr['style'])
            if m:
                args['fill'] = m[0]
        if 'transform' in attr:
            transform = attr['transform']
            m = re.findall(r'''translate\(([0-9\.]+),\s*([0-9\.]+)\)''', transform)
            if m:
                ox, oy = [float(x) for x in m[0]]
                args['offset_x'] = ox
                args['offset_y'] = oy
            # import pdb; pdb.set_trace()
        dstr += draw_multipolygon(**args)

    # head_to(t,mx/2,-(mx+40), False)

    t.hideturtle()
    t.clearstamps()
    turtle.done()

    dstr += '''

t.hideturtle()
t.clearstamps()
turtle.done()
'''
    with open(output_py, 'w') as f:
        f.write(dstr)


if __name__ == '__main__':
    Fire(main)
