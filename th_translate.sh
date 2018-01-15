#!/bin/sh

# this sample script translates a test set, including
# preprocessing (tokenization, truecasing, and subword segmentation),
# and postprocessing (merging subword units, detruecasing, detokenization).

# instructions: set paths to mosesdecoder, subword_nmt, and nematus,
# then run "./translate.sh < input_file > output_file"

# suffix of source languag
# path to moses decoder: https://github.com/moses-smt/mosesdecoder
mosesdecoder=/home/anton/deephack/extra_staff/mosesdecoder
# path to subword segmentation scripts: https://github.com/rsennrich/subword-nmt

cat /home/anton/deephack/data/input.txt | \
$mosesdecoder/scripts/tokenizer/normalize-punctuation.perl -l en | \
$mosesdecoder/scripts/tokenizer/tokenizer.perl -l en -penn | \
$mosesdecoder/scripts/recaser/truecase.perl -model truecase-model.en | \
python ./tf_translate.py |
$mosesdecoder/scripts/recaser/detruecase.perl > ./output.txt
