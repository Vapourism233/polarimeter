file = '/mnt/oscilloscope/yg/20230922/199188_60.wdf'
d = read_scope(file)
iref = 0
iprobe = [1, 2]

;FFT
dt = 10d-6
frange = [10d6, 20d6]
s = calc_spec(d.y, d.x, dt, frange=frange, iwinfn=0)
help, s, /structure

;get peak frequency
areft = total(s.y[*, *,iref], 1)
ret = max(areft, ifreq) 
ploti, s.f, abs(areft)

;get signal amplitude and phase
y = reform(s.y[*,, ifreq, *])
amp = abs(y) * (s.pcoef * 2.0)
yrp = y[*, iprobe] / (y[*, iref] # replicate(1.0, n_elements(iprobe)))
ph = atan(yrp, /phase)

pha = total(ph, 1) / n_elements(s.x)
print, 'phase[deg]:', strjoin(pha*180/!PI, format='(g0.3)'), ', ')
p = phq * 180 / !PI

ploti, s.x, (ph*180/!PI) 
