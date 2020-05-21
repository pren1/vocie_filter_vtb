import numpy as np
from tensorboardX import SummaryWriter

from .plotting import plot_spectrogram_to_numpy
import config
'1'
import librosa
import os
def create_folders(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

class MyWriter(SummaryWriter):
    def __init__(self, logdir):
        super(MyWriter, self).__init__(logdir)

    def log_training(self, train_loss, step):
        self.add_scalar('train_loss', train_loss, step)

    def log_evaluation_avg(self, test_loss, sdr,step):
        self.add_scalar('test_loss', test_loss, step)
        self.add_scalar('SDR', sdr, step)
    
    def log_evaluation_data(self, mixed_wav, target_wav, est_wav,
                       mixed_spec, target_spec, est_spec, est_mask,
                       step,index) :
        index = str(index)
        self.add_audio('mixed_wav/' + index, mixed_wav, step, config.audio['sample_rate'])
        self.add_audio('target_wav/' + index, target_wav, step, config.audio['sample_rate'])
        self.add_audio('estimated_wav/' + index, est_wav, step, config.audio['sample_rate'])

        '2'
        create_folders('mixed_wav/')
        create_folders('target_wav/')
        create_folders('estimated_wav/')

        # print(index)
        librosa.output.write_wav('mixed_wav/' + index + '.wav', mixed_wav, config.audio['sample_rate'])
        librosa.output.write_wav('target_wav/' + index + '.wav', target_wav, config.audio['sample_rate'])
        librosa.output.write_wav('estimated_wav/' + index + '.wav', est_wav, config.audio['sample_rate'])

        self.add_image('mixed_spectrogram/' + index,
            plot_spectrogram_to_numpy(mixed_spec), step, dataformats='HWC')
        self.add_image('target_spectrogram/' + index,
            plot_spectrogram_to_numpy(target_spec), step, dataformats='HWC')
        self.add_image('estimated_spectrogram/' + index,
            plot_spectrogram_to_numpy(est_spec), step, dataformats='HWC')
        self.add_image('estimated_mask/' + index,
            plot_spectrogram_to_numpy(est_mask), step, dataformats='HWC')
        self.add_image('estimation_error_sq/' + index,
            plot_spectrogram_to_numpy(np.square(est_spec - target_spec)), step, dataformats='HWC')
