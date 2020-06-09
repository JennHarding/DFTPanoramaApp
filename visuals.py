import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np




rgb_colors = {'f1_colors' : ['rgba(130,202,252,0.4)', 'rgba(61,122,253,0.6)', 'rgba(30,72,143,1)'], 
              'f2_colors' : ['rgba(255,223,34,0.4)', 'rgba(242,171,21,0.6)', 'rgba(127,78,30,1)'], 
              'f3_colors' : ['rgba(99,171,21,0.4)', 'rgba(105,131,57,0.6)', 'rgba(5,71,42,1)'],
              'f4_colors' : ['rgba(207,98,117,0.4)', 'rgba(212,106,126,0.6)', 'rgba(117,8,81,1)'], 
              'f5_colors' : ['rgba(196,142,253,0.4)', 'rgba(133,103,152,0.6)', 'rgba(67,5,65,1)'], 
              'f6_colors' : ['rgba(211,182,131,0.4)', 'rgba(127,104,78,0.6)', 'rgba(65,2,0,1)']}

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


def magnitudes_panorama(df, color_dict, title=None):
    f = Figure()
    a = f.add_subplot(111)
    for i in range(1, 7):
        a.fill_between(
            x=len(df[f'f{i} Magnitude']),
            y1=df[f'f{i} Magnitude'],
            color=color_dict[f'f{i}_colors'][0],
        )


def make_dataframes(score_data):
    general_info = {'Window Number' : [x for x in range(1, len(score_data) + 1)],
         'Weighted Array' : [str(a.rounded_weighted_array()) for a in score_data],
         'Original Array' : [str(a.rounded_original_array()) for a in score_data],
         'Measure Range' : [f'mm. {a.start_measure}–“{a.end_measure}' for a in score_data]
         }

    phases = {f'f{i} Phase' : [a.phase_dict()[f'f{i}'] for a in score_data] for i in range(1, 7)}
    phases['f6 Phase'] = [180 if x < -179 else x for x in phases['f6 Phase']]
    quantized_phases = {f'f{i} Quantized Phase' : [quantize_array(a.phase_dict()[f'f{i}']) for a in score_data] for i in range(1, 7)}
    quantized_phases['f6 Quantized Phase'] = [180 if x < -179 else x for x in quantized_phases['f6 Quantized Phase']]
    magnitudes = {f'f{i} Magnitude' : [a.mag_dict()[f'f{i}'] for a in score_data] for i in range(1, 7)}

    master_dict = {**general_info, **phases, **quantized_phases, **magnitudes}

    # general_df = pd.DataFrame(general_info)
    # phase_df = pd.DataFrame(phases)
    # quant_phase_df = pd.DataFrame(quantized_phases)
    # mag_df = pd.DataFrame(magnitudes)
    # master_df = pd.concat(dict(General = general_df, Magnitudes = mag_df, Phases = phase_df, QuantizedPhases = quant_phase_df), axis=1)
    
    # master_df = pd.concat([mag_df, phase_df, quant_phase_df], axis=1)
    master_df = pd.DataFrame(master_dict)
    
    return master_df