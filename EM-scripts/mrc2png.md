Convert mrc to png file, in batch:

```sh
e2proc2d.py ../Hb_107_Jun02_17_17_21.mrc Hb_107_Jun02_17_17_21.png --process=filter.lowpass.gauss:cutoff_freq=0.1 --process normalize

for i in ../*_[0-9][0-9].mrc; do e2proc2d.py $i `basename $i`.png --process=filter.lowpass.gauss:cutoff_freq=0.1 --process normalize;done

for i in ../*_[0-9][0-9].mrc; do e2proc2d.py $i `basename $i .mrc`.png --process=filter.lowpass.gauss:cutoff_freq=0.1 --process normalize;done

```
