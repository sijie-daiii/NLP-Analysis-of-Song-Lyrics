# **Song Lyrics NLP Analysis**

This project involves analyzing song lyrics using Natural Language Processing (NLP) techniques. The project processes song lyrics from `.lrc` files, performs sentiment analysis, generates word clouds, and visualizes word distributions using a Sankey diagram.
![1](https://github.com/user-attachments/assets/fa8acc03-efa6-4129-afcf-c7e45ea8a93a)


## **Project Structure**

```
final project
├── songs/
│   ├── Benson Boone - Beautiful Things.lrc
│   ├── Beyoncé - TEXAS HOLD 'EM.lrc
│   ├── Teddy Swims - Lose Control.lrc
│   ├── Disturbed - The Sound Of Silence.lrc
│   ├── Imagine Dragons - Eyes Closed.lrc
│   ├── David Guetta & OneRepublic - I Don't Wanna Wait.lrc
│   ├── Cyril - Stumblin' In.lrc
│   └── Artemas - i like the way you kiss me.lrc
├── stopwords/
│   ├── stopwords1.txt
│   ├── stopwords2.txt
│   └── stopwords-en.txt
├── parsers.py
├── main.py
├── nlp_api.py 
├── word_clouds.png
├── sentiment_comparison_plot.png
└── sankey_diagram.png

```

## **Description**

This project utilizes Python to analyze song lyrics from `.lrc` files. It focuses on several key tasks:

1. **Stopwords Filtering**: Removing common stopwords to focus on meaningful words in the lyrics.
2. **Word Count Analysis**: Counting the frequency of words in each song.
3. **Sentiment Analysis**: Analyzing the sentiment of the lyrics using the VADER sentiment analysis tool.
4. **Visualization**:
   - **Word Clouds**: Showing the most common words in each song.
   - **Sankey Diagram**: Visualizing word distribution across songs.
   - **Sentiment Comparison**: Comparing sentiment scores across different songs.

## **Setup**

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Install Dependencies**

   Make sure you have Python installed. Then, install the required Python packages using:

   ```bash
   pip install -r requirements.txt
   ```

   (If you `requirements.txt` method is not work, here’s a another approach to install the packages)

   ```txt
   pip install nltk matplotlib plotly wordcloud
   ```

3. **Run the Project**

   To process the lyrics and generate the visualizations, run the following command:

   ```bash
   python main.py
   ```

## **Data Sources**

- **Lyric Files**: [Lyricsify](https://www.lyricsify.com/)
- **Stopword Lists**:
  - [Stopwords List 1](https://gist.github.com/larsyencken/1440509)
  - [Stopwords List 2](https://github.com/stopwords-iso/stopwords-en/blob/master/stopwords-en.txt)
  - [Stopwords List 3](https://gist.github.com/sebleier/554280)

## **Generated Visualizations**

- **`word_clouds.png`**: Word clouds generated from the lyrics.
- ![word_clouds](https://github.com/user-attachments/assets/b070975a-b709-4a19-b935-4b179e18777d)
- 
- **`sentiment_comparison_plot.png`**: Bar chart comparing sentiment scores across songs.
- ![sentiment_comparison_plot](https://github.com/user-attachments/assets/e918df19-7b33-438a-875d-9302ab592cb6)
- 
- **`sankey_diagram.png`**: Sankey diagram showing word distribution across songs.
- ![wordcount_sankey](https://github.com/user-attachments/assets/925187d8-baf0-43e0-b9a7-b92495823280)


## **License**

This project is licensed under the MIT License.

---
