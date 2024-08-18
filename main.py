from nlp_api import NaturalLanguageAPI
from parsers import read_lrc
import os

def load_stop_words(nlp_api, stopwords_dir):
    '''
    Load stop words from a directory of text files.
    :param nlp_api: the NaturalLanguageAPI object to load the stop words into
    :param stopwords_dir: the directory containing the stop words text files
    :return: None
    '''

    # Load stop words from each text file in the directory
    for stopfile in os.listdir(stopwords_dir):
        if stopfile.endswith('.txt'):
            nlp_api.load_stop_words(os.path.join(stopwords_dir, stopfile))

def load_songs(nlp_api, songs_dir):
    '''
    Load song lyrics from .lrc files in a directory.
    :param nlp_api: the NaturalLanguageAPI object to load the song lyrics into
    :param songs_dir: the directory containing the .lrc files
    :return: None
    '''

    # Load song lyrics from each .lrc file in the directory
    for file in os.listdir(songs_dir):
        if file.endswith('.lrc'):
            path = os.path.join(songs_dir, file)
            label = file[:-4]  # Remove the .lrc extension for the label
            nlp_api.load_text(filename=path, label=label, parser=read_lrc)

def main():
    songs_dir = 'songs'
    stopwords_dir = 'stopwords'

    # Initialize the NLP API
    nlp_api = NaturalLanguageAPI()

    # Load stop words and songs
    load_stop_words(nlp_api, stopwords_dir)
    if not os.path.isdir(songs_dir):
        print(f"Directory '{songs_dir}' not found.")
        return

    load_songs(nlp_api, songs_dir) # Load song lyrics from .lrc files

    # Visualization and Analysis
    nlp_api.wordcount_sankey(k=10, save_path='wordcount_sankey.png')
    nlp_api.generate_word_clouds(title='Word Clouds to show the most common words in the songs')
    nlp_api.compare_sentiment()

if __name__ == "__main__":
    main()
