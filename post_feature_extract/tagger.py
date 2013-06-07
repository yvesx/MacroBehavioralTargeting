#!/home/download/python2.7/bin/python2.7

# CFLAGS="-O3 -march=native -mtune=native" python setup.py build_ext --inplace
#
# This code is an optimized version of nltk:tag_pos and nltk:word_tokenize for
# pure lowercase alphabetic input strings.
#
# WARNING: This function assumes that the input tokens will be
# purely lowercase and alphabetic. If you need to handle mixed case
# tokens, or tokens with non-alphabetic characters, you MUST modify
# SATweetClass:update_tagger_pkl() to create and propagate a top-level
# dictionary for the 'shape' feature (as opposed to merging the shape
# weight into the initial_weights[] list).
# Additionally, you must create code within this function to determine
# the shape of each token and add the 'shape' feature to the
# features[] list.
# Finally, you must use the tokenizer in treebank.py of the NLTK instead
# of the tokenizing code in this function.

from numpy import max
from re import compile, sub

# List of contractions adapted from Robert MacIntyre's tokenizer.
CONTRACTIONS2 = [compile(r"(?i)\b(can)(not)\b"),
                 compile(r"(?i)\b(Gim)(me)\b"),
                 compile(r"(?i)\b(Gon)(na)\b"),
                 compile(r"(?i)\b(Got)(ta)\b"),
                 compile(r"(?i)\b(Lem)(me)\b"),
                 compile(r"(?i)\b(T)(is)\b"),
                 compile(r"(?i)\b(T)(was)\b"),
                 compile(r"(?i)\b(Wan)(na)\b")]
CONTRACTIONS3 = [compile(r"(?i)\b(Whad)(dd)(ya)\b"),
                 compile(r"(?i)\b(Wha)(t)(cha)\b")]
    

def tag_pos(item, encoding_labels, initial_weights, feature_lts):

    for regexp in CONTRACTIONS2:
        item = regexp.sub(r'\1 \2', item)
    for regexp in CONTRACTIONS3:
        item = regexp.sub(r'\1 \2 \3', item)
    tokens = item.split()
    
    tags=[]
    tappend = tags.append

    #cdef int index

    for index in range(len(tokens)):
        if index == 0:
            prevprevword = None
            prevword = None
            word = tokens[index]
            prevprevtag = None
            prevtag = None
        elif index == 1:
            prevword = word
            word = tokens[index]
            prevtag = tags[index-1]
        else:
            prevprevword = prevword
            prevword = word
            word = tokens[index]
            prevprevtag = prevtag
            prevtag = tags[index-1]

        features = [
            ('prevtag', prevtag),
            ('prevprevtag', prevprevtag),
            ('word', word),
            ('word.lower', word),
            ('suffix3', word[-3:]),
            ('suffix2', word[-2:]),
            ('suffix1', word[-1:]),
            ('prevprevword', prevprevword),
            ('prevword', prevword),
            ('prevtag+word', '%s+%s' % (prevtag, word)),
            ('prevprevtag+word', '%s+%s' % (prevprevtag, word)),
            ('prevword+word', '%s+%s' % (prevword, word))
            ]

        featureset = initial_weights
        for tpl in features:
          if tpl in feature_lts:
            featureset = featureset + feature_lts[tpl]

        tappend(encoding_labels[featureset.argmax()])

    return zip(tokens,tags)
