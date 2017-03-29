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
        self.categorizedDurations = []
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
    
    '''A static method that converts a Duration object to a number'''
    @staticmethod
    def convertDurationToFloat(duration):
        durationAsString = str(duration)
        #find the part of the string after the " "; i.e. the number, and delete the > at the end
        durationAsString = durationAsString.split(" ")[1].replace(">", "")
        
        #if the duration is a fraction, convert it to a decimal
        
        if "/" in durationAsString:
            split = durationAsString.split("/")
            durationAsFloat = float(split[0]) / float(split[1])
        #otherwise, keep it the same
        else:
            durationAsFloat = float(durationAsString)
        
        #keep only 2 decimal places.
        durationAsFloat = round(durationAsFloat, 2)
        return durationAsFloat
     
    '''A method that collects all the chord durations and puts it into a vector'''
    def getChordDurations(self):
        if not self.chords:
            self.extractChordObjects()
        
        for chord in self.chords:
            if isinstance(chord, music21.chord.Chord):
                duration = chord.duration #chord.duration is an object that 
                                          #represents how long a chord is
                #the problem is that duration objects that aren't multiples of 4 display as Fraction objects.
                #to avoid this problem, parse the string representation of the object before creating vector.
                durationNumber = ChordExtractor.convertDurationToFloat(duration)
                self.chordDurations.append(durationNumber) 
        return self.chordDurations
    
    '''A method that will create a vector of ennumerated chord durations.  This is necessary to enable easy
        counting of different chord length types. It goes without saying that creating a dict keyed on floats
        is a very bad idea.'''
    def getCategorizedDurations(self):
        if not self.chordDurations:
            self.getChordDurations()
        
        for duration in self.chordDurations:
            category = ChordExtractor.categorize(duration)
            self.categorizedDurations.append(category)
            
        return self.categorizedDurations
    
    '''Converts a duration number into a category for easy enumeration.'''
    @staticmethod
    def categorize(duration):
        if duration<=0.1:
            return 0
        if duration<=0.2:
            return 1
        if duration<=0.3:
            return 2
        if duration<=0.4:
            return 3
        if duration<=0.5:
            return 4
        if duration<=0.6:
            return 5
        if duration<=0.7:
            return 6
        if duration<=0.8:
            return 7
        if duration<=0.9:
            return 8
        return 9
    
    
        
        
    ##TODO: figure out where the key signature is in the midi file parsed. 
