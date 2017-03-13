import os.path
import dolfyn.adv.api as avm

accel_filter = 0.03

FILENAMES = [
    'TTM_NREL03_May2015',
    'TTM_NRELvector_Jun2012',
    'TTM01b_ADVbottom_NREL01_June2014',
    'TTM01_ADVtop_NREL02_June2014',
    'TTM01_ADVbottom_NREL01_June2014'
]


def load_data(filename):
    """Load ``filename``."""
    fname = './data_cache/' + filename
    if os.path.isfile(fname + '.VEC'):
        data = avm.read_nortek(fname + '.VEC')
    else:
        print 'The file has not been downloaded yet.'
    return data


def save_h5(data, filename):
    """Saves the data as a '.h5' file"""
    data.save('./data_cache/' + filename + '.h5')
    return


def bin_data(data):
    """Averages the data according to bin size"""
    binner = avm.TurbBinner(n_bin=19200, fs=data.fs, n_fft=19200)
    dat_bin = binner(data)
    dat_bin.add_data('Spec_velraw', binner.psd(data['velraw']), 'spec')
    return dat_bin


for filename in FILENAMES:
    data = load_data(filename)
    avm.clean.GN2002(data)
    avm.motion.correct_motion(data, accel_filter)
    avm.rotate.earth2principal(data)
    save_h5(data, filename)
    dat_bin = bin_data(data)
    save_h5(dat_bin, filename + '_binned')
