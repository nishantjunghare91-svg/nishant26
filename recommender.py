import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')

class BollywoodRecommender:
    def __init__(self):
        self.movies = None
        self.ratings = None
        self.user_item_matrix = None
        self.movie_features = None
        self.movie_similarity = None
        self.user_similarity = None
        self.scaler = MinMaxScaler()
        
    def load_bollywood_data(self):
        bollywood_movies = {
            'title': [
                'Dilwale Dulhania Le Jayenge', 'Sholay', '3 Idiots', 'Dangal', 'PK',
                'Bajrangi Bhaijaan', 'Lagaan', 'Gadar: Ek Prem Katha', 'Kuch Kuch Hota Hai',
                'Kabhi Khushi Kabhie Gham', 'Hum Aapke Hain Koun', 'Veer-Zaara', 'Om Shanti Om',
                'Chennai Express', 'Tiger Zinda Hai', 'Sultan', 'Baahubali 2', 'Sanju',
                'Padmaavat', 'Raazi', 'Andhadhun', 'Badhaai Ho', 'Stree', 'Uri', 'Kesari',
                'Gully Boy', 'Dream Girl', 'Housefull 4', 'War', 'Saaho', 'Kabir Singh',
                'Chhichhore', 'Super 30', 'Mission Mangal', 'Article 15', 'Bharat',
                'Total Dhamaal', 'Student of the Year 2', 'De De Pyaar De', 'Kalank',
                'Drive', 'PM Narendra Modi', 'Blank', 'Jab Harry Met Sejal',
                'Toilet: Ek Prem Katha', 'Secret Superstar', 'Hindi Medium', 'Newton',
                'Bareilly Ki Barfi', 'Shubh Mangal Saavdhan', 'Tumhari Sulu'
            ],
            'genres': [
                'Romance Drama Family','Action Adventure Drama','Comedy Drama','Biography Drama Sport','Comedy Drama Sci-Fi',
                'Action Adventure Drama','Drama Musical Sport','Action Drama Romance','Comedy Drama Romance','Drama Family Romance',
                'Comedy Drama Family Romance','Drama Family Romance','Action Comedy Drama Romance','Action Comedy','Action Thriller',
                'Action Drama Sport','Action Drama Fantasy','Biography Comedy Drama','Drama History Romance','Action Drama Thriller',
                'Crime Drama Mystery Thriller','Comedy Drama Family','Comedy Horror','Action Drama War','Action Drama History War',
                'Drama Music','Comedy','Action Comedy','Action Thriller','Action Drama Sci-Fi Thriller','Action Drama Romance',
                'Comedy Drama','Biography Drama','Drama Sci-Fi','Action Comedy Drama','Comedy','Comedy Romance','Comedy Drama Romance',
                'Drama Musical Romance','Action Thriller','Biography Drama','Thriller','Comedy Drama Romance','Comedy Drama','Drama',
                'Drama','Comedy Drama','Comedy Romance','Comedy Drama'
            ],
            'cast': [
                'Shah Rukh Khan Kajol','Amitabh Bachchan Dharmendra','Aamir Khan Sharman Joshi',
                'Aamir Khan Fatima Sana Shaikh','Aamir Khan Anushka Sharma','Salman Khan Kareena Kapoor',
                'Aamir Khan Gracy Singh','Sunny Deol Ameesha Patel','Shah Rukh Khan Kajol Rani Mukerji',
                'Shah Rukh Khan Kajol Hrithik Roshan','Salman Khan Madhuri Dixit','Shah Rukh Khan Preity Zinta',
                'Shah Rukh Khan Deepika Padukone','Shah Rukh Khan Deepika Padukone','Salman Khan Katrina Kaif',
                'Salman Khan Anushka Sharma','Prabhas Anushka Shetty','Ranbir Kapoor Paresh Rawal',
                'Deepika Padukone Shahid Kapoor','Alia Bhatt Vicky Kaushal','Ayushmann Khurrana Tabu',
                'Ayushmann Khurrana Neena Gupta','Shraddha Kapoor Rajkummar Rao','Vicky Kaushal',
                'Akshay Kumar Parineeti Chopra','Ranveer Singh Alia Bhatt','Ayushmann Khurrana Nushrratt Bharuccha',
                'Akshay Kumar','Hrithik Roshan Tiger Shroff','Prabhas Shraddha Kapoor',
                'Shahid Kapoor Kiara Advani','Sushant Singh Rajput Mrunal Thakur','Hrithik Roshan Mrunal Thakur',
                'Vidya Balan','Ayushmann Khurrana Sayani Gupta','Salman Khan Katrina Kaif',
                'Ajay Devgn','Tiger Shroff Tara Sutaria','Ajay Devgn Rakul Preet Singh',
                'Varun Dhawan Alia Bhatt','Siddharth Malhotra','Ajay Devgn Rakul Preet Singh',
                'Varun Dhawan Alia Bhatt','Shah Rukh Khan Anushka Sharma','Akshay Kumar Bhumi Pednekar',
                'Zaira Wasim Aamir Khan','Irrfan Khan Saba Qamar','Rajkummar Rao Pankaj Tripathi',
                'Kriti Sanon Ayushmann Khurrana','Ayushmann Khurrana Bhumi Pednekar','Vidya Balan Manav Kaul'
            ],
            'director': [
                'Aditya Chopra','Ramesh Sippy','Rajkumar Hirani','Nitesh Tiwari','Rajkumar Hirani',
                'Kabir Khan','Ashutosh Gowariker','Anees Bazmee','Karan Johar','Karan Johar',
                'Sooraj Barjatya','Yash Chopra','Farah Khan','Rohit Shetty','Ali Abbas Zafar',
                'Ali Abbas Zafar','S S Rajamouli','Rajkumar Hirani','Sanjay Leela Bhansali',
                'Meghna Gulzar','Sriram Raghavan','Amit Sharma','Amar Kaushik','Aditya Dhar',
                'Anurag Singh','Zoya Akhtar','Raaj Shaandilyaa','Farhad Samji','Siddharth Anand',
                'Suhas','Sandeep Reddy Vanga','Nitesh Tiwari','Vikas Bahl','Jagan Shakti',
                'Anubhav Sinha','Ali Abbas Zafar','Indra Kumar','Punit Malhotra','Akiv Ali',
                'Abhishek Varman','Tarun Mansukhani','Omung Kumar','Behzad Khambata','Imtiaz Ali',
                'Shree Narayan Singh','Advait Chandan','Saket Chaudhary','Amit V Masurkar',
                'Ashwiny Iyer Tiwari','R S Prasanna','Suresh Triveni'
            ],
            'year': [
                1995,1975,2009,2016,2014,2015,2001,2001,1998,2001,
                1994,2004,2007,2013,2017,2016,2017,2018,2018,2018,
                2018,2018,2018,2019,2019,2019,2019,2019,2019,2019,
                2019,2019,2019,2019,2019,2019,2019,2019,2019,2019,
                2019,2019,2019,2017,2017,2017,2017,2017,2017,2017
            ]
        }

        # Fix lengths automatically
        min_len = min(len(v) for v in bollywood_movies.values())
        for key in bollywood_movies:
            bollywood_movies[key] = bollywood_movies[key][:min_len]

        bollywood_movies['movie_id'] = list(range(1, min_len + 1))

        self.movies = pd.DataFrame(bollywood_movies)

        # Ratings
        np.random.seed(42)
        user_ids = np.repeat(range(1, 21), 15)
        movie_ids = np.random.choice(self.movies['movie_id'], 300)
        ratings = np.random.choice([1,2,3,4,5], 300)

        self.ratings = pd.DataFrame({
            'user_id': user_ids,
            'movie_id': movie_ids,
            'rating': ratings
        })

    def preprocess_features(self):
        self.movies['features'] = (
            self.movies['genres'] + ' ' +
            self.movies['cast'] + ' ' +
            self.movies['director'] + ' ' +
            self.movies['year'].astype(str)
        )

        tfidf = TfidfVectorizer(stop_words='english')
        self.movie_features = tfidf.fit_transform(self.movies['features'])

    def create_matrices(self):
        self.user_item_matrix = self.ratings.pivot_table(
            index='user_id', columns='movie_id', values='rating'
        ).fillna(0)

        self.user_item_matrix_norm = self.scaler.fit_transform(self.user_item_matrix)
        self.movie_similarity = cosine_similarity(self.movie_features)
        self.user_similarity = cosine_similarity(self.user_item_matrix_norm)

    def content_based_recommend(self, movie_title):
        idx = self.movies[self.movies['title'].str.contains(movie_title, case=False)].index[0]
        scores = list(enumerate(self.movie_similarity[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]

        return [self.movies.iloc[i]['title'] for i, _ in scores]


def main():
    rec = BollywoodRecommender()
    rec.load_bollywood_data()
    rec.preprocess_features()
    rec.create_matrices()

    movie = input("Enter movie name: ")
    recs = rec.content_based_recommend(movie)

    print("\nRecommended Movies:")
    for r in recs:
        print("👉", r)


if __name__ == "__main__":
    main()