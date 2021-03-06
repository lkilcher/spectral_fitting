import dolfyn.adv.api as avm
from os.path import isfile

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
    data = avm.load(fname + '.h5')
    return data


def load_raw(filename):
    filename = './data_cache/' + filename
    if isfile(filename + '_raw.h5'):
        data = avm.load(filename + '_raw.h5')
    else:
        data = avm.read_nortek(filename + '.VEC')
        data.save(filename + '_raw.h5')
    return data


def crop_data(data):
    """Crops the data"""
    t_range_inds = ((data.props['time_range'][0] < data.mpltime) &
                    (data.mpltime < data.props['time_range'][1]))
    return data.subset(t_range_inds)


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


if __name__ == '__main__':

    for filename in FILENAMES:
        data = load_raw(filename)
        avm.motion.correct_motion(data, accel_filter)
        avm.rotate.earth2principal(data)
        data = crop_data(data)
        avm.clean.GN2002(data)
        save_h5(data, filename + '_processed')
        dat_bin = bin_data(data)
        save_h5(dat_bin, filename + '_binned')
