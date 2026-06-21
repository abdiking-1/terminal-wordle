#!/usr/bin/python3
"""Definiera klasser för stavningskontroll och kör SpellCheckApp.main().

Klasser:
SpellingWarning -- Potentiellt stavfel med radnummer
och rättningsförslag.
Report -- Hanterar stavningsrapport för textfil.
SpellCheckApp -- Läser in filer och kör stavningskontroll.
"""

#FIXME fel filnamn, se körexempel på kurshemsidan.

#FIXME genomgående i era docstrings vill jag att ni skriver ut datatypen på argument och
# returvärde som t.ex (str) eller (dict), för att öka läsbarheten i koden.


import sys
from med import minimum_edit_distance
from time import time


def replacer(text):
    """Bearbeta text genom att ta bort skiljetecken och radbrytningar.

    #FIXME här vill jag att ni skriver ut datatypen inom parantes t.ex (str)
    # för att göra det tydligare för läsaren.
    # justera detta genomgående för alla doc strings.
    Argument:
    text -- Text (str).

    #FIXME samma sak här, skriv ut datatyp (str)
    Return:
    Bearbetad text som utan skiljetecken och radbrytningar (str).
    """
    textbearbetning = text
    textbearbetning = textbearbetning.replace("\n", " ")
    Char_del = [".", "?", "!", ":", ";", ",", "-", "–", "(", ")", '"', "'"]
    for character in Char_del:
        textbearbetning = textbearbetning.replace(character, "")
    textbearbetning = textbearbetning.replace("  ", " ")
    textbearbetning = textbearbetning.replace("   ", " ")
    return textbearbetning


class SpellingWarning:
    """Klass för varje potentiellt stavfel.

    Instansvariabler:
    _word -- Det felstavade ordet (str).
    _line -- Raden där ordet hittades (int).
    _suggestions -- Lista med rättningsförslag (list).


    Metoder:
    add_suggestion -- Lägg till ett rättningsförslag.
    find_same_length -- Hitta ord med samma längd.
    find_n_highest_freq -- Hitta de vanligaste orden.
    make_suggestions -- Skapa rättningsförslag.
    get_word -- Returnera felstavat ord.
    get_line -- Returnera radnummer.
    __str__ -- Returnera strängrepresentation av objektet.
    """

    def __init__(self, word, line):
        """Skapa ett SpellingWarning-objekt.

        Argument:
        word -- Felstavat ord som sträng (str).
        line -- Radnummer där ordet hittades som heltal (int).
        """
        self._word = word
        self._line = line
        self._sugestions = []

    def add_suggestion(self, word_sugestion):
        """Lägg till suggestion till listan self._suggestions.

        Argument:
        word_sugestions - ord som sträng (str).
        """
        self._sugestions.append(word_sugestion)

    def find_same_length(self, wordfreqdata):
        """Hitta alla ord i wordlist, samma längd som SpellingWarning.

        Argument:
        wordfreqdata: -- Dict av frekvensdata {ord:frekvens}, (dict).
        Spellingwarning: -- Spellingwarning objekt.

        Return:
        Dict av ord i wordfreqdata av samma längd som spellingwarning,
        {ord:frekvens} (dict).
        """
        lengthSW = len(self._word)
        Same_len_dict = {}
        # Iterera över alla ord i ordlistan
        for word in list(wordfreqdata.keys()):
            # Om lika långt som self._word, spara ordet och frekvensen
            if len(word) == lengthSW:
                Same_len_dict.update({word: wordfreqdata[word]})

        return Same_len_dict

    def find_n_highest_freq(self, same_len_dict, n=1000):
        """Hitta de n-st ord i Same_len_dict med högst frekvens.

        Argument:
        Same_len_dict -- Dictionary med par {ord:frekvens},
        med ord av samma längd som spelllingwarning (dict).
        n -- Längd av lista med mest frekventa ord (int) (default 1000).

        Return:
        Lista av de n mest frekventa ord av samma längd som self._word.
        """
        sorted_freq = sorted(list(same_len_dict.values()), reverse=True)
        # biggest_freq blir de n+1 första eller alla i sorterade listan.
        if len(sorted_freq) >= n+1:
            biggest_freq = sorted_freq[0:n]
        else:
            biggest_freq = sorted_freq
        lowest_freq = biggest_freq[-1]
        finishedlist = []
        # Iterera över alla ord av samma längd.
        for word in list(same_len_dict.keys()):
            # Spara ord med högre frekv än lowest_freq(n+1 största frekvensen).
            if same_len_dict[word] > lowest_freq:
                finishedlist.append(word)
        return finishedlist

    def make_suggestions(self, finishedlist, antal=3):
        """Skapa rättningsförslag baserat på redigeringsavstånd.

        Argument:
        finishedlist -- Lista med kandidatord som strängar.

        Nyckelargument:
        antal -- Antal rättningsförslag som ska sparas (default 3).
        """
        lowest_med = 0
        list_word_and_med = []
        # Iterera över alla ord i finishedlist, spara in [med,ord] i lista.
        for word in finishedlist:
            lowest_med = minimum_edit_distance(self._word, word)
            list_word_and_med.append([lowest_med, word])
        # Lamba hänvisas till på fö 6.1 slide 16
        #NOTE ok
        list_word_and_med.sort(key=lambda med_word_pair: med_word_pair[0])
        candidates = list_word_and_med[:antal]
        # Lägg in alla candidate_pairs (de 3 minsta med) i ._sugestions.
        for candidate_pair in candidates:
            self._sugestions.append(candidate_pair[1])

    def get_word(self):
        """Returnera okända ordet."""
        return self._word

    def get_line(self):
        """Returnera raden vart okända ordet hittades."""
        return self._line

    def __str__(self):
        """Skapa en rättningsrapport.

        Argument:
        filename -- Filnamn till textfil som ska rättas.

        Nyckelargument:
        runtime -- Tiden rättningen tog i sekunder (default 0).
        """
        sugestions_str = ""
        # Gå över alla rättningförslag, lägg in dem i sugestion_str.
        for sugestion in self._sugestions:
            sugestions_str += sugestion + ", "
        str1 = sugestions_str
        return "[line {}] {}: {}".format(self._line, self._word, str1)


class Report:
    """Klass för rättningsrapport av en textfil.

    Variabler:
    _filename -- Adress tilltextfilen som ska rättas.
    _time -- hur lång tid rättningen tog.

    Metoder:
    textfile_into_wordlist -- Använder _filename,
    returnerar alla ord i filename som lista.
    find_same_length -- Tar emot ordlista,
    returnerar lista med alla ord som är lika långa som spellingwarning.
    find_errors -- Tar emot ordlista, lista av ord i filename,
    returnerar alla stavfel.
    """

    def __init__(self, filename, runtime=0):
        """Skapa en rättningsrapport.

        Argument:
        filename -- Filnamn till textfil som ska rättas.

        Nyckelargument:
        runtime -- Hur lång tid rättningen tog.
        i sekunder (default 0).
        """
        self._filename = filename
        self._runtime = runtime
        self._spellingwarninglist = []

    def textfile_into_rowdict(self):
        """Använd self._filename, öppna och läs filen, delar upp i dict.

        Return:
        Dictionary på form {radnummer:lista av ord i rad}.
        """
        rownr_word_dict = {}
        openfile = open(self._filename, "r")
        for rownr, row in enumerate(openfile):
            rownr_word_dict[rownr + 1] = replacer(row).lower().split(" ")
            for word in rownr_word_dict[rownr+1]:
                if not word.isalpha():
                    rownr_word_dict[rownr+1].remove(word)
                if rownr_word_dict[rownr+1] == [""]:
                    del rownr_word_dict[rownr+1]
        openfile.close()

        return rownr_word_dict

    def find_errors(self, text_dict, wordfreqdata):
        """Hitta ord i text_dict - values som inte finns i wordfreqdata.

        Argument:
        text_dict -- Dictionary på form {radnummer:lista av ord i rad}.
        wordfreqdata -- Dictionary av ordfrekvensdata {ord:frekvens}.

        Return:
        Lista av SpellingWarning-objekt.
        """
        errors = []
        for row_number in list(text_dict.keys()):
            for word in text_dict[row_number]:
                if word not in list(wordfreqdata.keys()):
                    if len(word) != 0:
                        errors.append(SpellingWarning(word, row_number))
        self._spellingwarninglist = errors

    def find_suggestions(self, wordfreqdata):
        """Hitta rättningsförslag till alla stavfel.

        Argument:
        wordfreqdata -- Dictionary med ordfrekvensdata.
        Form {ord:frekvens}.
        """
        for spellingwarning in self._spellingwarninglist:
            same_len_dict = spellingwarning.find_same_length(wordfreqdata)
            finishedlist = spellingwarning.find_n_highest_freq(same_len_dict)
            spellingwarning.make_suggestions(finishedlist)

    def printstr(self):
        """Skapa en strängrepresentation av rapporten.

        Return:
        Sträng med alla stavfel och rättningsförslag.
        """
        returnstr = ""
        for spellingwarning in self._spellingwarninglist:
            returnstr += spellingwarning.__str__() + "\n"
        return returnstr

    def set_runtime(self, runtime):
        """Spara hur lång tid rättningen tog i self._runtime.

        Argument:
        runtime -- Körtid i sekunder som flyttal.
        """
        self._runtime = runtime

    def get_spellingwarninglist(self):
        """Returnera lista med alla SpellingWarning-objekt."""
        return self._spellingwarninglist

    def make_file(self):
        """Spara och skriv rättningar i textfil."""
        reportname = self._filename.rstrip(".txt") + "_report.txt"
        print("* Saving report to {}".format(reportname))
        text_file = open(reportname, "w")
        write_str = "Spellcheck for '{}' took {} seconds. \n\n".format(
            self._filename, self._runtime
        )
        text_file.write(write_str + self.printstr())
        text_file.close()


class SpellCheckApp:
    """Klass för att köra stavningskontrollen.

    Instansvariabler:
    _wordfreqdatafile -- Fil med ordfrekvensdata.
    _textfiles -- Lista med textfiler som ska rättas.

    Metoder:
    main -- Kör programmets huvudfunktion.
    call_report -- Skapa rapport för varje textfil.
    get_wordfreqdata -- Läs in ordfrekvensdata från fil.
    """

    def __init__(self):
        """Skapa SpellCheckApp.

        Hämtar filnamn från kommandoradsargument
        och sparar dem som instansvariabler.

        Instansvariabler:
        _wordfreqdatafile -- Fil med ordfrekvensdata.
        _textfiles -- Lista med textfiler som ska rättas.
        """
        #FIXME här kommer koden att krascha ifall användaren inte anger argument i terminalen.
        # ni behöver lägga till ett villkor som kontrollerar detta.
        self._wordfreqdatafile = sys.argv[1]
        self._textfiles = sys.argv[2:]

    #NOTE ok uppdelning av funktionallitet mellan main och call_report.
    def main(self):
        """Läs in frekvensdata och kör stavningskontroll."""
        wordfreqdata = self.get_wordfreqdata()
        print("* {} file(s) to check.".format(len(self._textfiles)))
        self.call_report(wordfreqdata)

    def call_report(self, wordfreqdata):
        """Skapa rättningsrapport för varje textfil.

        Argument:
        wordfreqdata -- Dictionary med ordfrekvensdata {ord:frekvens}.
        """
        for textfile in self._textfiles:
            starttid = time()
            str1 = "and looking for unknown words..."
            print("* Reading '{}' {}".format(textfile, str1))
            textreport = Report(textfile, 45)
            textreport_rowdict = textreport.textfile_into_rowdict()
            textreport.find_errors(textreport_rowdict, wordfreqdata)
            antal_fel = len(textreport.get_spellingwarninglist())
            print("* Found {} unknown words.".format(antal_fel))
            textreport.find_suggestions(wordfreqdata)
            textreport.set_runtime(time()-starttid)
            textreport.make_file()

    def get_wordfreqdata(self):  # Hämtad från ex1, modifierad.
        """Läs in ordfrekvensdata från fil.

        Return:
        Dictionary med ordfrekvensdata på form {ord:frekvens}.
        """
        str1 = "* Loading word frequency data from"
        print("{} {}.".format(str1, self._wordfreqdatafile))
        with open(self._wordfreqdatafile, encoding='utf-8') as file:
            freq_data_dict = {}
            for line in file:
                line_list = line.rstrip().split('\t')
                freq_data_dict[line_list[0]] = line_list[1]
        antal_ord = len(freq_data_dict)
        print("* Frequency data for {} words loaded.".format(antal_ord))
        return freq_data_dict


if __name__ == "__main__":
    spellchecker = SpellCheckApp()
    spellchecker.main()
