from colormath.color_conversions import convert_color
from colormath.color_objects import HSVColor, BaseRGBColor, LabColor

math_strip = open('math_uniform_strip.svg', 'w')
perc_strip = open('perceptually_uniform_strip.svg', 'w')

saturation = 1
value = 1 # great naming btw
step = 10

def rgb_from_hue(hue):
    return convert_color(HSVColor(hue, saturation, value), BaseRGBColor)

math_strip.write('<svg width="512" height="32" version="1.1" xmlns="http://www.w3.org/2000/svg">\n')
math_strip.write('\t<defs>\n\t\t<linearGradient id="gradient">\n')

for i in range(step):
    rgb = rgb_from_hue(360 / step * i + 1)
    color = rgb.get_rgb_hex()
    math_strip.write(f'\t\t<stop offset="{(i / step)}" stop-color="{color}"/>\n')
    
math_strip.write('\t\t</linearGradient>\n')
math_strip.write('\t</defs>\n')
math_strip.write('\t<rect x="0" y="0" width="512" height="32" fill="url(#gradient)"/>\n')
math_strip.write('</svg>\n')


def lab_from_hue(hue):
    return convert_color(HSVColor(hue, saturation, value), LabColor)

perc_strip.write('<svg width="512" height="32" version="1.1" xmlns="http://www.w3.org/2000/svg">\n')
perc_strip.write('\t<defs>\n\t\t<linearGradient id="gradient">\n')

for i in range(step):
    perc_strip.write(f'\t\t<stop offset="{(i / step)}" stop-color="#000"/>\n')
    
perc_strip.write('\t\t</linearGradient>\n')
perc_strip.write('\t</defs>\n')
perc_strip.write('\t<rect x="0" y="0" width="512" height="32" fill="url(#gradient)"/>\n')
perc_strip.write('</svg>\n')
