import plotly.graph_objects as go
from collections import defaultdict, Counter
import nltk
import string
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np

nltk.download('vader_lexicon')

class NaturalLanguageAPI:
    '''
    A class to perform natural language processing tasks on text data.

    Attributes:
    - data (dict): a dictionary to store the processed data
    - stopwords (set): a set to store stopwords
    - sentiment_analyzer (SentimentIntensityAnalyzer): a sentiment analyzer object
    '''
    def __init__(self):
        self.data = {
            'word_count': defaultdict(dict),
            'word_length': defaultdict(dict),
            'sentiment': defaultdict(dict),
        }
        self.stopwords = set()
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def load_stop_words(self, stopfile):
        '''
        Load stopwords from a file, ignoring lines that start with '#', and add them to the set of stopwords.
        :param stopfile: the name of the file containing stopwords
        :return: None
        '''

        # Load stopwords from the file, ignoring lines starting with '#', and add them to the set
        try:
            with open(stopfile, 'r', encoding='utf-8') as file:
                for line in file:
                    clean_line = line.strip()
                    if not clean_line.startswith('#'): # Ignore lines starting with '#'
                        self.stopwords.update([clean_line])
        except FileNotFoundError: # Handle file not found error
            print(f"Stopwords file {stopfile} not found.")

    def load_text(self, filename, label=None, parser=None):
        '''
        Load text from a file and process it to generate word count, word length, and sentiment scores.
        :param filename: the name of the file to load
        :param label: the label to associate with the text
        :param parser: the function to use for parsing the text
        :return: None
        '''
        if label is None:
            label = filename
        if parser is None:
            parser = self._default_parser
        lyrics = parser(filename)

        # Process the lyrics to generate word count, word length, and sentiment
        cleaned_lyrics = self._clean_string(lyrics)
        wordcount = Counter(cleaned_lyrics.split())
        wordlength = {word: len(word) for word in cleaned_lyrics.split()}
        sentiment_scores = self.sentiment_analyzer.polarity_scores(lyrics)

        # Store the results in the data dictionary under the given label
        self.data['word_count'][label] = wordcount
        self.data['word_length'][label] = wordlength
        self.data['sentiment'][label] = sentiment_scores

    def _clean_string(self, lyrics: str) -> str:
        '''
        Clean the input string by removing punctuation and stopwords, and converting to lowercase.
        :param lyrics: the input string to clean
        :return: the cleaned string
        '''
        # Remove newlines, convert to lowercase, remove punctuation, and filter out stopwords
        lyrics = lyrics.replace('\n', ' ').lower()
        clean_lyrics = "".join(char for char in lyrics if char not in string.punctuation)
        return " ".join(word for word in clean_lyrics.split() if word not in self.stopwords)

    def wordcount_sankey(self, word_list=None, k=5, save_path=None):
        """
        Generate a Sankey diagram mapping texts to words.
        :param word_list: Optional list of words to include in the diagram. If None, the top k words are used.
        :param k: Number of top words to include if word_list is None. Default is 5.
        :param save_path: Optional path to save the Sankey diagram as an image or HTML file.
        """
        if word_list is None:
            common_words = self._find_common_words(k)
        else:
            common_words = set(word_list)

        # Prepare the data for the Sankey diagram
        sources, targets, values = self._prepare_sankey_data(common_words)

        # Generate and optionally save the Sankey diagram
        self._generate_sankey_diagram(sources, targets, values,
                                      list(self.data['word_count'].keys()) + list(common_words),
                                      save_path=save_path)

    def _find_common_words(self, k):
        """
        Find the union of the k most common words across all texts.
        :param k: Number of top words to find.
        :return: A set of the k most common words.
        """
        all_words = Counter()

        # Update the Counter with all word counts
        for wordcount in self.data['word_count'].values():
            all_words.update(wordcount)
        return {word for word, count in all_words.most_common(k)}

    def _prepare_sankey_data(self, common_words):
        """
        Prepare the data needed for the Sankey diagram based on common words.
        :param common_words: A set of words to include in the diagram.
        :return: Lists of sources, targets, and values for the Sankey diagram.
        """

        # Create a mapping of labels and words to indices
        sources, targets, values = [], [], []
        label_idx = {label: i for i, label in enumerate(self.data['word_count'])}
        word_idx = {word: i + len(label_idx) for i, word in enumerate(common_words)}

        # Create the connections between texts and words
        for label, wordcount in self.data['word_count'].items():
            for word, count in wordcount.items():
                if word in common_words:
                    sources.append(label_idx[label])
                    targets.append(word_idx[word])
                    values.append(count)

        return sources, targets, values

    def _generate_sankey_diagram(self, sources, targets, values, labels, save_path=None):
        """
        Create and show the Sankey diagram using the provided data, and optionally save it to a file.
        :param sources: List of source indices for the Sankey diagram.
        :param targets: List of target indices for the Sankey diagram.
        :param values: List of values for the connections in the Sankey diagram.
        :param labels: List of labels for all nodes in the Sankey diagram.
        :param save_path: Optional path to save the Sankey diagram as an image or HTML file.
        """

        # Create the Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            # Define the nodes in the diagram
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels
            ),
            # Define the links between nodes
            link=dict(
                source=sources,
                target=targets,
                value=values
            ))])

        # Update the layout of the diagram
        fig.update_layout(title_text="Word Count Sankey Diagram", font_size=10)

        # Show the diagram
        fig.show()

        # Save the figure if save_path is provided
        if save_path:
            if save_path.endswith('.html'):
                fig.write_html(save_path)
            else:
                fig.write_image(save_path)

    def generate_word_clouds(self, figsize=(20, 10), rows=None, cols=None,
                             save_path='word_clouds.png', title='Word Clouds for Text Files'):
        '''
        Generate word clouds for each text file based on word count.
        :param figsize: the size of the figure
        :param rows: the number of rows in the plot grid
        :param cols: the number of columns in the plot grid
        :param save_path: the path to save the plot
        :param title: the title of the plot
        :return: None
        '''

        # Calculate the number of rows and columns based on the number of text files
        n = len(self.data['word_count']) # Number of text files
        if rows is None or cols is None:
            rows = int(n ** 0.5)
            cols = -(-n // rows)  # Ceiling division

        plt.figure(figsize=figsize)

        # Generate word clouds for each text file
        for i, (label, wordcount) in enumerate(self.data['word_count'].items(), start=1):
            wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(wordcount)
            plt.subplot(rows, cols, i)
            plt.imshow(wc, interpolation='bilinear')
            plt.title(label)
            plt.axis('off')

        # Add a main title to the figure
        plt.suptitle(title, fontsize=24)

        plt.tight_layout()

        # Save the plot automatically to the specified path
        plt.savefig(save_path)
        plt.close()

    def _annotate_bars(self, rects, ax):
        '''
        Annotate the bars with their values.
        :param rects:  the bars to annotate
        :param ax: the axis to annotate on
        :return: None
        '''

        # Add annotations to the bars
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    def _plot_sentiment_bars(self, labels, pos_scores, neg_scores, neu_scores, compound_scores, ax, width=0.2):
        '''
        Plot the sentiment scores as grouped bars.
        :param labels: the labels for the text files
        :param pos_scores: the positive sentiment scores
        :param neg_scores: the negative sentiment scores
        :param neu_scores: the neutral sentiment scores
        :param compound_scores: the compound sentiment scores
        :param ax: the axis to plot on
        :param width: the width of the bars
        :return: None
        '''
        x = np.arange(len(labels))

        # Plot the bars for positive, negative, neutral, and compound scores
        rects1 = ax.bar(x - width*1.5, pos_scores, width, label='Positive', color='lightgreen')
        rects2 = ax.bar(x - width/2, neg_scores, width, label='Negative', color='salmon')
        rects3 = ax.bar(x + width/2, neu_scores, width, label='Neutral', color='lightblue')
        rects4 = ax.bar(x + width*1.5, compound_scores, width, label='Compound', color='dodgerblue')

        # Annotate the bars with their values
        self._annotate_bars(rects1, ax)
        self._annotate_bars(rects2, ax)
        self._annotate_bars(rects3, ax)
        self._annotate_bars(rects4, ax)

    def compare_sentiment(self, save_path='sentiment_comparison_plot.png'):
        '''
        Compare the sentiment scores for each text file.
        :param save_path: the path to save the plot
        :return: None
        '''

        # Extract the labels and sentiment scores from the data
        labels = [label.split("-", 1)[-1] if "-" in label else label for label in self.data['sentiment']]
        pos_scores = [self.data['sentiment'][label]['pos'] for label in self.data['sentiment']]
        neg_scores = [self.data['sentiment'][label]['neg'] for label in self.data['sentiment']]
        neu_scores = [self.data['sentiment'][label]['neu'] for label in self.data['sentiment']]
        compound_scores = [self.data['sentiment'][label]['compound'] for label in self.data['sentiment']]

        # Create a bar plot to compare the sentiment scores
        fig, ax = plt.subplots(figsize=(14, 8))
        self._plot_sentiment_bars(labels, pos_scores, neg_scores, neu_scores, compound_scores, ax)

        # Add labels, title, and legend to the plot
        ax.set_xlabel('Text Files')
        ax.set_ylabel('Scores')
        ax.set_title('Detailed Sentiment Analysis Including Compound Scores')
        ax.set_xticks(np.arange(len(labels)))
        ax.set_xticklabels(labels, rotation=45)
        ax.legend()

        # Save the plot to the specified path
        fig.tight_layout()
        plt.savefig(save_path)
        plt.close(fig)
