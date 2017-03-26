"""
ChordExtractor

Usage:

extractor = ChordExtractor(fileName="AMIDIsong.mid")
normalizedChords = extractor.getNormalizedChords()
normalizedPitches = extractor.getNormalizedPitches()
normalizedDurations = extractor.getChordDurations()
"""

import music21
import chordgraph
        
class ChordExtractor(object):
    '''Constructor for ChordExtractor
        looks like you must pass in the full path.
        This also parses the file'''
    def __init__(self, fileName=None, parsedFile=None):
        if fileName: 
            self.parsedFile = music21.converter.parse(fileName)
        elif parsedFile:
            self.parsedFile = parsedFile
        else:
            raise Exception("Must pass fileName or parsedFile")
            
        self.measures = None
        self.chords = []
        self.normalizedChords = []
        self.chordsAsNumbers = []
        self.pitches = None
        self.normalizedPitches = []
        self.chordDurations = []
        self.chordGraph = chordgraph.ChordGraph()
    
    '''This method will take only those measures that are chord objects, and ignore the rest'''
    def extractChordObjects(self):
        if self.chords: #if the list is nonempty
            return
        self.measures = self.parsedFile.chordify()
        for measure in self.measures:
            if isinstance(measure, music21.chord.Chord):
                self.chords.append(measure)
     
    '''This returns a list of tuples of chords, where all names are changed to numbers'''           
    def getChordsAsNumbers(self):
            self.extractChordObjects()
            for chord in self.chords:
                chordTuple = tuple(chord.normalOrder)
                self.chordsAsNumbers.append(chordTuple)
            return self.chordsAsNumbers
     
    def getNormalizedChords(self):
        chordsAsNumbers = self.getChordsAsNumbers()
        for numberedChord in chordsAsNumbers:
            #find the closest normalized chords to given numbered chord, using the chord graph
            closestNormalizedChords = self.chordGraph.find_closest_normalized_chords(numberedChord) 
            #pick the first (since we are guaranteed to have at least 1) normalized chord
            self.normalizedChords.append(closestNormalizedChords[0])
        return self.normalizedChords
        
    '''This method will load all pitch objects into a list'''
    def extractPitches(self):
        if self.pitches:
            return
        self.pitches = self.parsedFile.pitches
       
    '''This method converts all pitch objects into numbers'''
    def getNormalizedPitches(self):
        self.extractPitches()
        for pitch in self.pitches:
            if isinstance(pitch, music21.pitch.Pitch):
                pitchNumber = pitch.pitchClass #pitchClass is the number of the pitch
                self.normalizedPitches.append(pitchNumber)
                
        return self.normalizedPitches
    
    def getChordDurations(self):
        if self.chords:
            return
        self.extractChordObjects()
        
        for chord in self.chords:
            if isinstance(chord, music21.chord.Chord):
                duration = chord.duration #chord.duration is an object that 
                                          #represents how many quarter notes a chord lasts
                self.chordDurations.append(duration.quarterLength) #quarterLength is the number itself
        return self.chordDurations
        
        
        
        
    ##TODO: figure out where the key signature is in the midi file parsed. 
