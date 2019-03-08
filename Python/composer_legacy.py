
import os
import music_track

class ComposerLegacy:

    composer_names = ["Beethoven", "Berlioz", "Borodin", "Brahms", "Bruch", "Bruckner", "Chaikovsky", "Chopin",
                      "Czerny", "Elgar", "Kalinnikov", "Mahler", "Mendelssohn", "Miaskovsky", "Mozart", "Paganini",
                      "Prokofiev", "Rachmaninoff", "Rott", "Shostakovich", "Sibelius", "Stravinsky", "Villa-Lobos",
                      "Wagner"]

    @staticmethod
    def is_composer_legacy (p_folder_name):
        return p_folder_name in ComposerLegacy.composer_names

    def __init__ (self, p_dir_name, p_comp_name):
        self.dir_name = p_dir_name
        self.name = p_comp_name
        self.music_tracks = []

    def collect_legacy (self):
        dir_name_len = len (self.dir_name)
        for root, folders, files in os.walk (self.dir_name):
            root_len = len (root)
            dir_names = ""

            if root_len > dir_name_len:
                dir_names = root [dir_name_len + 1:]

            for next_file in files:
                if music_track.MusicTrack.is_music_track (os.path.join (self.dir_name, next_file)):
                    new_track = music_track.MusicTrack ()
                    # new_track.parse_file_name (next_file, dir_names)
                    new_track.parse_file_name (next_file)
                    self.music_tracks.append (new_track)

    def print_legacy (self):
        i = 1
        output_str = ""

        for t in self.music_tracks:
            print (i, t.full_file_name)

            output_str = "\t"

            if t.file_number != "": output_str += t.file_number + " "
            output_str += t.full_genre

            if t.num_in_genre != "": output_str += " No." + t.num_in_genre
            if t.musical_key != "": output_str += '(' + t.musical_key +')'

            if t.opus_name != "": output_str += ", \'" + t.opus_name + "\'"

            if t.opus_number != "": output_str += ", Opus " + t.opus_number
            if t.opus_subnum != "": output_str += ", nno." + t.opus_subnum

            print (output_str, 'num', t.part_number, 'name', t.part_name)
            i += 1
