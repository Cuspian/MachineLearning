"""
Chord Graph

Usage:

g = ChordGraph()
g.find_closest_normalized_chords((0, 1, 2)) # ((0, 3, 7),)
"""

W1 = 1
W2 = 3

tonicless_normalized_chords = {
    (0, 3, 6) : "diminished",
    (0, 3, 7) : "minor",
    (0, 4, 7) : "major",
    (0, 4, 8) : "augmented",
    (0, 5, 7) : "suspended",
    (0, 3, 6, 9) : "diminished seventh",
    (0, 3, 6, 10) : "half diminished seventh",
    (0, 3, 7, 10) : "minor seventh",
    (0, 4, 7, 10) : "dominant seventh",
    (0, 4, 7, 11) : "major seventh",
    (0, 3, 7, 10, 14) : "minor ninth",
    (0, 4, 7, 10, 13) : "dominant minor ninth",
    (0, 4, 7, 10, 14) : "dominant ninth",
    (0, 4, 7, 11, 14) : "major ninth",
}

def generate_normalized_chords():
    for chord in sorted(tonicless_normalized_chords):
        yield tuple(x % 12 for x in chord)

def note_distance(p, q):
    """
    The distance between the two notes: p and q.
    """
    return W1 * min((p - q) % 12, (q - p) % 12)
    # return W1 * abs(q - p) % 12

def hammingish_distance(p, q):
    if len(p) != len(q):
        raise Exception("hammingish distance not defined for words of different lengths.")
    h = 0
    for i in range(len(p)):
        h += note_distance(p[i], q[i])
    return W1 * h

## TODO: Replace with lru cache.
_levenshteinish_cache = {}
def levenshteinish_distance(p, q):
    past = _levenshteinish_cache.get((p, q))
    if past:
        return past

    cost = 0
    if len(p) == 0: return W2 * len(q)
    if len(q) == 0: return W2 * len(p)
    if p[-1] != q[-1]:
        cost = min(2 * W2, note_distance(p[-1], q[-1]))
    result = min(levenshteinish_distance(p[:-1], q) + W2,
                 levenshteinish_distance(p, q[:-1]) + W2,
                 levenshteinish_distance(p[:-1], q[:-1]) + cost)
    _levenshteinish_cache[(p, q)] = result
    return result

class ChordGraph:
    def __init__(self):
        self._history = {}
        self.normalized_chords = tuple(generate_normalized_chords())

    def distance(self, r, s):
        return levenshteinish_distance(r, s)

    def distance_ub(self, r, s):
        len_r = len(r)
        len_s = len(s)
        if len_r == len_s:
            return hammingish_distance(r, s)
        return max(len_r, len_s)

    def distance_lb(self, r, s):
        return W2 * abs(len(s) - len(r))

    def find_closest_normalized_chords(self, seq):
        """
        Finds the closest named chords to the input chord.

        input: A seqence of integers representing a chord in the key of C.
               The `normalOrder` property of the `music21.chord.Chord` class
               is an appropriate input for this method.
        output: A tuple of tuples containing the notes of the named chords
                closest to the input, in the key of C.
                It is my understanding theat these are the "normalized chords"
                from the lecture notes.
        """
        past = self._history.get(seq)
        if past:
            return past
        possible = self._find_candidates(seq)
        closest = {}
        for p in possible:
            closest.setdefault(self.distance(seq, p), []).append(p)
        least = min(closest)
        chords = tuple(closest[least])
        self._history[seq] = chords
        return chords

    def _find_candidates(self, seq):
        min_ub = 10000
        possible = []
        for chord in self.normalized_chords:
            ub = self.distance_ub(seq, chord)
            if ub < min_ub:
                min_ub = ub
                possible = [chord]
            else:
                if self.distance_lb(seq, chord) < ub:
                    possible.append(chord)
        return possible

