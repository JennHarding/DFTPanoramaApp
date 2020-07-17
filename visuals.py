import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np


# rgb_colors = {'f1_colors' : ['rgba(130,202,252,0.4)', 'rgba(61,122,253,0.6)', 'rgba(30,72,143,1)'], 
#               'f2_colors' : ['rgba(255,223,34,0.4)', 'rgba(242,171,21,0.6)', 'rgba(127,78,30,1)'], 
#               'f3_colors' : ['rgba(99,171,21,0.4)', 'rgba(105,131,57,0.6)', 'rgba(5,71,42,1)'],
#               'f4_colors' : ['rgba(207,98,117,0.4)', 'rgba(212,106,126,0.6)', 'rgba(117,8,81,1)'], 
#               'f5_colors' : ['rgba(196,142,253,0.4)', 'rgba(133,103,152,0.6)', 'rgba(67,5,65,1)'], 
#               'f6_colors' : ['rgba(211,182,131,0.4)', 'rgba(127,104,78,0.6)', 'rgba(65,2,0,1)']}

rgb_colors = {'f1_colors' : ['rgba(130,202,252,0.4)', 'rgba(06,130,219,0.6)', 'rgba(03,71,119,1)'], 
              'f2_colors' : ['rgba(255,223,34,0.4)', 'rgba(224,191,0,0.6)', 'rgba(143,121,0,1)'], 
              'f3_colors' : ['rgba(99,171,21,0.4)', 'rgba(73,127,16,0.6)', 'rgba(42,73,9,1)'],
              'f4_colors' : ['rgba(207,98,117,0.4)', 'rgba(172,53,73,0.6)', 'rgba(109,34,46,1)'], 
              'f5_colors' : ['rgba(196,142,253,0.4)', 'rgba(171,94,253,0.6)', 'rgba(49,1,101,1)'], 
              'f6_colors' : ['rgba(211,182,131,0.4)', 'rgba(135,105,49,0.6)', 'rgba(217,114,255,1)']}
            #   'f7_colors' : [],
            #   'f8_colors' : [],
            #   'f9_colors' : [],
            #   'f10_colors' : [],
            #   'f11_colors' : []
            #   }
hex_colors = {'f1_colors' : ['#89CBFB', '#098DEC', '#05528A'], 
              'f2_colors' : ['#F5D000', '#CCAD00', '#8F7900'], 
              'f3_colors' : ['#73C819', '#497F10', '#2A4909'],
              'f4_colors' : ['#C4455A', '#9B3143', '#6D222E'], 
              'f5_colors' : ['#CA9AFE', '#5902B6', '#310165'], 
              'f6_colors' : ['#D4B987', '#BE964B', '#876931'],
              'f7_colors' : ['#A88AA6', '#815F7F', '#463445'],
              'f8_colors' : ['#D33665', '#A7254C', '#64162E'],
              'f9_colors' : ['#12BA85', '#0D825D', '#074A35'],
              'f10_colors' : ['#FAB79E', '#F67D51', '#AE3509'],
              'f11_colors' : ['#9ECAD1', '#59A5B1', '#34676F'],
              'f12_colors' : ['#C1AF85', '#806D40', '#5F5130']}

xkcd_colors = {'f1_colors' : ['xkcd:sky', 'xkcd:lightish blue', 'xkcd:cobalt'],
               'f2_colors' : ['xkcd:sun yellow', 'xkcd:squash', 'xkcd:milk chocolate'],
               'f3_colors' : ['xkcd:fern', 'xkcd:swamp', 'xkcd:evergreen'],
               'f4_colors' : ['xkcd:rose', 'xkcd:pinkish', 'xkcd:velvet'],
               'f5_colors' : ['xkcd:lilac', 'xkcd:dark lavender', 'xkcd:eggplant purple'],
               'f6_colors' : ['xkcd:very light brown', 'xkcd:dark taupe', 'xkcd:deep brown']}


def quantize_array(array, quant=12):
    spacing = 360/quant
    q = np.around(array/spacing)
    return q * spacing


def magnitudes_panorama(df, color_dict, title=None, edo=12):
    f = Figure()
    a = f.add_subplot(111)
    for i in range(1, edo//2 + 1):
        a.fill_between(
            x=len(df[f'f{i} Magnitude']),
            y1=df[f'f{i} Magnitude'],
            color=color_dict[f'f{i}_colors'][0],
        )


def make_dataframes(score_data, edo=12):
    general_info = {'Window Number' : [x for x in range(0, len(score_data))],
         'Weighted Array' : [str(a.rounded_weighted_array()) for a in score_data],
         'Original Array' : [str(a.rounded_original_array()) for a in score_data],
         'Measure Range' : [f'{a.start_measure}–{a.end_measure}' for a in score_data]
         }

    phases = {f'f{i} Phase' : [a.phase_dict()[f'f{i}'] for a in score_data] for i in range(1, edo//2 +1)}
    phases['f6 Phase'] = [180 if x < -179 else x for x in phases['f6 Phase']]
    quantized_phases = {f'f{i} Quantized Phase' : [quantize_array(a.phase_dict()[f'f{i}']) for a in score_data] for i in range(1, edo//2 +1)}
    quantized_phases['f6 Quantized Phase'] = [180 if x < -179 else x for x in quantized_phases['f6 Quantized Phase']]
    magnitudes = {f'f{i} Magnitude' : [np.around(a.mag_dict()[f'f{i}'], decimals=2) for a in score_data] for i in range(1, edo//2 + 1)}

    master_dict = {**general_info, **phases, **quantized_phases, **magnitudes}

    # general_df = pd.DataFrame(general_info)
    # phase_df = pd.DataFrame(phases)
    # quant_phase_df = pd.DataFrame(quantized_phases)
    # mag_df = pd.DataFrame(magnitudes)
    # master_df = pd.concat(dict(General = general_df, Magnitudes = mag_df, Phases = phase_df, QuantizedPhases = quant_phase_df), axis=1)
    
    # master_df = pd.concat([mag_df, phase_df, quant_phase_df], axis=1)
    master_df = pd.DataFrame(master_dict)
    
    return master_df