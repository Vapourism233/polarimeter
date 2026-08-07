# Polarimeter

Data-analysis scripts from my master's thesis project on a waveguide-based
polarimeter (hardware: copper waveguide, oscilloscope, local oscillator +
mixers, power splitter).

## Project structure

| File | Purpose |
| --- | --- |
| [utils.py](utils.py) | Shared measurement loading and plotting helpers used by the other scripts |
| [spec.py](spec.py) | Windowed spectrogram / FFT utilities (spectrogram, window functions, 2-D plotting) |
| [diff.py](diff.py) | Compares beat-note frequency and amplitude of two mixers against the LO |
| [oscillator.py](oscillator.py) | Compares measured VCO tuning curves against reference data |
| [splitter.py](splitter.py) | Analyzes power-splitter channel balance and LO/mixer beat-frequency consistency |
| [process.py](process.py) | Characterizes a fluctuation time series via PSD (Welch) and single-bin amplitude tracking |
| [run.pro](run.pro) | IDL script used on the oscilloscope acquisition side to extract spectral amplitude/phase from raw scope traces |

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Each Python script is a small CLI (run with `-h` to see all options) that
expects the relevant `.txt`/`.npy` measurement files in the working
directory by default, e.g.:

```bash
python3 diff.py --lo-file LO_240704.txt --mixer1-file mixer478_ch1_240704.txt
python3 splitter.py --diagnostics
python3 process.py --input fluct_1us.npy --plot
```

Update : 2023/10/01
