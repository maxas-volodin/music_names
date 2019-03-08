
import os
import re


class MusicTrack:

    __known_genres = {
        'sinfonietta': 'Sinfonietta',   # Two works of Villa-Lobos
        'symphony': 'Symphony',
        'sinfonie': 'Symphony',         # German
        'symphonie': 'Symphony',        # French
        'симфония': 'Symphony',
        'concerto': 'Concerto',
        'koncert': 'Concerto',          # Polish
        'концерт': 'Concerto',
        'sonata': 'Sonata',
        'sonate': 'Sonata',
        'соната': 'Sonata',
        'suite': 'Suite',
        'сюита': 'Suite',
        'fantasy': 'Fantasia',
        'fantasia': 'Fantasia',
        'rhapsody': 'Rhapsody'
    }

    __genre_id_keys = {
        'Symphon': 'Symphony',
        'Concert': 'Concerto',
        'Sonat': 'Sonata',
        'Suit': 'Suite'
    }

    __genre_search_pattern = ""

    @staticmethod
    def is_music_track (p_file_name):
        return os.path.splitext (p_file_name)[1] in [".mp3", ".flac", ".ape", ".wav"]

    @staticmethod
    def recognize_genre (p_dir_names):

        search_pattern = "(?P<key>("

        for index, name in enumerate(MusicTrack.__genre_id_keys):
            search_pattern += name
            if index + 1 < len (MusicTrack.__genre_id_keys):
                search_pattern += "|"
            else:
                search_pattern += "))"

        match = re.search(search_pattern, p_dir_names)

        result = MusicTrack.__genre_id_keys[match.group('key')] if match else ''
        return result

    def __init__ (self):
        self.opus_name = ""
        self.opus_number = ""
        self.opus_subnum = ""

        self.main_genre = ""
        self.full_genre = ""
        self.num_in_genre = ""

        self.musical_key = ""
        self.sequence_number = ""

        self.track_name = ""
        self.track_number = ""
        self.file_number = ""

        self.part_name = ""
        self.part_number = ""

        self.full_file_name = ""
        self.encoding_type = ""

        for name in self.__known_genres:
            if self.__genre_search_pattern != "":
                self.__genre_search_pattern += "|"
            self.__genre_search_pattern += name

    def parse_file_name (self, p_file_name):
        self.full_file_name = p_file_name

        # parse input file name into elements

        self.encoding_type = os.path.splitext (p_file_name)[1]
        self.track_name = os.path.splitext (os.path.basename (p_file_name))[0]

        # create search string to work with

        search_string = self.track_name

        # bite off file number (may also be track number as well, but this logic comes later)

        match = re.search("^(?P<file_num>(#?\d+|\(#?\d+\)|\[#?\d+\]))[ .](?P<string_tail>.+)$", search_string)
        if match:
            self.file_number = match.group('file_num')
            search_string = match.group('string_tail')
            self.track_name = match.group('string_tail')

            match = re.search("^\D*(?P<file_num>(\d+))\D*$", self.file_number)
            self.file_number = match.group('file_num')

        # try to parse naming scheme of the type d-d [track name] first
        # if this is not recognized then try other patterns

        if not self.__parse_d_d_partname (search_string):

            # try recognizing opus number and name, such as in "Piano Sonata No. 15 in D, Op.28 'Pastoral'"

            match = re.search (r"[\s.,\-(](Op|op)[\s.,\-]+(?P<number>\d+\w*)(?P<subnum>\sno[\s.]\d+)*\s*(?P<name>((\'{1,2}[\w ]+\')|(\([\w ]+\))))*", search_string)

            if match:
                self.opus_number = match.group('number')

                tmp_str = match.group('subnum')

                if tmp_str is not None:
                    new_match = re.search ('(\d+)', tmp_str)
                    self.opus_subnum = new_match.group (1)

                tmp_str = match.group('name')

                if tmp_str is not None:
                    new_match = re.search (r'([\w ]+)', tmp_str)
                    self.opus_name = new_match.group (1)

                post_opus_chars = ""
                pre_opus_chars = search_string [0:match.start (0)]

                if match.end () + 1 < len (search_string):
                    post_opus_chars = search_string [match.end ():]

                self.__recognize_part_name (post_opus_chars)
                self.__recognize_genre (pre_opus_chars, True)
            else:
                self.__recognize_genre (search_string, False)

    # This method tries to recognize the d-d [track_name] naming pattern

    def __parse_d_d_partname (self, p_search_string):

        match = re.search(r"^(?P<number>\d+)[_-](?P<part_num>\d+)(?P<part_name>[ _.,\w-]*)$", p_search_string)

        if match:
            self.num_in_genre = match.group('number')
            self.part_number = match.group('part_num')
            self.part_name = match.group('part_name')

        return match is not None

    def __recognize_genre (self, track_name, part_name_known):

        genre_recognized = False
        part_name_start_pos = 0

        pattern = "(?i)(?P<genre>(" + self.__genre_search_pattern + "))"
        match = re.search (pattern, track_name)

        if match:
            org_genre_name = match.group ('genre')
            self.main_genre = self.__known_genres [org_genre_name.lower()]

            # if genre is recognized then try recognizing the a bigger pattern, e.g. "Piano Sonata No. 15"
            # note that qualifier "Piano", and number "No. 15") are optional

            new_pattern = r'(?i)(?P<type>.*?XXX.*?)((\s+(nr|no|#)[\s.]*(?P<num>\d+))*)*'
            new_pattern = new_pattern.replace ("XXX", org_genre_name)

            match = re.search (new_pattern, track_name)
            if match:
                tmp_str = match.group ('type')
                if tmp_str is None:
                    tmp_str = ""
                    print ("Unexpected error: not recognized genre" + org_genre_name + "in" + track_name)
                else:
                    part_name_start_pos = match.end('type') + 1

                self.full_genre = tmp_str

                tmp_str = match.group ('num')
                if tmp_str is not None:
                    self.num_in_genre = tmp_str
                    part_name_start_pos = match.end ('num')

                genre_recognized = True
        else:
            self.full_genre = track_name

        part_name_index = None

        if not part_name_known and part_name_start_pos < len (track_name):
            part_name_index = self.__recognize_part_name (track_name [part_name_start_pos:])
            if part_name_index is not None: part_name_index += part_name_start_pos

        # if genre has not been recognized (which means that genre is equal to full track name) and part name
        # has been recognized then it is likely that the part name is a subset of the genre string and needs
        # to be trimmed from it - unless the two strings are equal

        if genre_recognized is False and part_name_index is not None:
            if self.full_genre != self.part_name:
                match = re.search (self.part_name + "$", self.full_genre)
                if match:
                    self.full_genre = self.full_genre [:match.start ()]
            else:
                self.part_name = ""

    def __recognize_part_name (self, search_string):
        # match = re.search(r"[\s.,-]*(?P<part_num>[IVX]+|\d+)*[\s.,-]+(?P<part_name>[\D]+)$", search_string)

        # First, try recognizing a pattern with part number (can be in arabic or Roman numerals)
        # If this is not recognized then just pick up all non-white characters
        # (keep number-recognition group in place to unify further processing)

        match = re.search(r"^.*?((?P<part_num>[IVX]+|\d+)[\s.,-])+(?P<part_name>[\D]+)$", search_string)

        if not match:
            match = re.search(r"[\W]*((?P<part_num>[IVX]+|\d+)[\s.,-])*(?P<part_name>[\D]+)$", search_string)

        if match:
            self.part_number = match.group('part_num')
            self.part_name = match.group('part_name')

            return match.start ()

        return None
