audio = {
    "n_fft": 1200,
    "num_freq": 601,
    "sample_rate": 16000,
    "hop_length": 160,
    "win_length": 400,
    "min_level_db": -100.0,
    "ref_level_db": 20.0,
    "preemphasis": 0.97,
    "power": 1,
}

model = {
  "lstm_dim": 400,
  "fc1_dim": 600,
  "fc2_dim": 601, # num_freq
}

data = {
  "train_dir": '/home/pren1/voicefilter_output/train',
  "test_dir": '/home/pren1/voicefilter_output/test',
  'audio_len': 3.0
}

form = {
  "input": '*.wav',
  "dvec": '*-dvec.txt', # will be calculated on-the-fly
  "target": {
    "wav": '*-target.wav',
    "mag": '*-target.pt'
  },
  "mixed": {
    "wav": '*-mixed.wav',
    "mag": '*-mixed.pt'
  }
}

train = {
    "batch_size": 12,
    "num_workers": 8,
    "adam": 0.001,
    "ckpt_interval": 600,
    "summary_interval": 120,
    "epoch": 100,
    "train_step_pre_epoch": 6965,
    "eval_example": 10
}

embedder = { # d-vector embedder. don't fix it!
  "num_mels": 40,
  "n_fft": 512,
  "emb_dim": 256,
  "lstm_hidden": 768,
  "lstm_layers": 3,
  "window": 80,
  "stride": 40,
}

log = {
  "chkpt_dir": 'chkpt',
  "log_dir": 'logs'
}