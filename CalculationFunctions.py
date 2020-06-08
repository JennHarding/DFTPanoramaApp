
from music21 import stream, note, pitch, chord, meter, corpus, converter
from math import pi

import Corpus
from dftArrayClass import dft_array


def parse_score(score_string, measure_nums):
    if score_string in Corpus.music21_corpus:
        working_score = corpus.parse(score_string)
    elif score_string in Corpus.mozSQs:
        working_score = converter.parse(Corpus.corpus+Corpus.moz+score_string)
    elif score_string in Corpus.harbs:
        working_score = converter.parse(Corpus.corpus+Corpus.harb+score_string)
    elif score_string in Corpus.mess_misc:
        working_score = converter.parse(Corpus.corpus+Corpus.mess+score_string)
    elif score_string in Corpus.meis:
        working_score = converter.parse(Corpus.corpus+Corpus.mei+score_string)
    elif score_string in Corpus.tests:
        working_score = converter.parse(Corpus.corpus+Corpus.test+score_string)
    elif score_string in Corpus.elvis_corpus:
        working_score = converter.parse(Corpus.corpus+Corpus.elvis+score_string)
    
    if measure_nums == (0,0):
        return working_score
    else:
        return working_score.measures(measure_nums[0], measure_nums[1])


def split_time_signature(numerator):
    if numerator < 4:
        return [numerator]
    elif numerator == 4:
        return [2, 2]
    else: 
        return [3, *split_time_signature(numerator-3)]


def convert_time_signature(ts):
    ms = meter.MeterSequence(ts.ratioString)
    if ms.numerator in [2, 3, 4]:
        ms.partitionByCount(ms.numerator)
        return ms
    else:
        partition_list = split_time_signature(ts.numerator)
        ms.partitionByList(partition_list)
        return ms


def get_beat_offsets_from_score(score):
    time_signature_list = []
    meter_sequence_list = []
    offset_list = [0]
    for m in score.semiFlat.getElementsByClass('Measure'):
        if m.timeSignature is not None:
            time_signature_list.append(m.timeSignature)
        else:
            time_signature_list.append(m.getContextByClass('TimeSignature'))
        
    for ts in time_signature_list:
        meter_sequence_list.extend(convert_time_signature(ts))
        
    duration_list = [m.duration for m in meter_sequence_list]

    for idx, i in enumerate(duration_list):
        offset_list.append(i.quarterLength + offset_list[idx])
    
    return offset_list


def update_array(array, note_, strategy):
    if strategy == 'Onset':
        array[note_.pitch.pitchClass] += 1
    elif strategy == 'Duration':
        array[note_.pitch.pitchClass] += note_.quarterLength
    elif strategy == 'Flat':
        array[note_.pitch.pitchClass] = 1
    return array


def get_measure_number(score, offset):
    beat_measure_tuple = score.beatAndMeasureFromOffset(offset)
    measure_number = beat_measure_tuple[1].number
    return measure_number
    
    
def sliding_window(score, beat_offset_list, window_size, strategy, log=True, edo=12):
    all_arrays = []
    for idx, window_begin in enumerate(beat_offset_list[:-window_size]):
        window_end = beat_offset_list[idx + window_size]
        array = [0]*edo
        measure1 = get_measure_number(score=score, offset=window_begin)
        
        if window_end == beat_offset_list[-1]:
            measure2 = get_measure_number(score=score, offset=beat_offset_list[-2])
        else:
            measure2 = get_measure_number(score=score, offset=window_end)
        
        for elem in score.semiFlat.getElementsByOffset(
            offsetStart=window_begin, 
            offsetEnd=window_end, 
            includeEndBoundary=False).getElementsByClass(['Note', 'Chord']):
            
            if isinstance(elem, chord.Chord):
                for a in elem.notes:
                    array = update_array(
                        array=array, 
                        note_=a, 
                        strategy=strategy)
            elif isinstance(elem, note.Note):
                array = update_array(
                    array=array, 
                    note_=elem, 
                    strategy=strategy)

        all_arrays.append(dft_array(
            array=array, 
            log_weight=log, 
            measure_range=(measure1, measure2)))
        
    return all_arrays


def score_to_data(config):  
     
    repertoire, excerpt, measures, window, strat, log = config
    parsed_score = parse_score(score_string=repertoire, measure_nums=measures)
    # parsed_score.show('musicxml')
    beat_offset_list = get_beat_offsets_from_score(score=parsed_score.parts[0])

    if strat == "Duration" or strat == "Flat":
        adjusted_score = parsed_score.sliceByBeat(addTies=False)
    else:
        adjusted_score = parsed_score.stripTies(retainContainers=True)
    # adjusted_score.show('musicxml')
    
    multisets = sliding_window(
        score=adjusted_score, 
        beat_offset_list=beat_offset_list, 
        window_size=window, 
        strategy=strat, 
        log=log)

    return multisets