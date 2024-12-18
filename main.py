import streamlit as st
import requests
import pandas as pd
import pickle

st.title("Books You'd Love to Read!")

book = st.text_input("Enter a book name")

with open('/workspaces/codespaces-blank/sim_test.pkl', 'rb') as file:
  sim_test = pickle.load(file)

def get_book_data(book):
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={book}")
    data = response.json()
    return data
def extract_book_info(data):
    list_of_books = []
    image_links = []
    for item in data.get("items", []):
        volume_info = item.get("volumeInfo", {})
        list_of_books.append(volume_info.get("title"))
        image_links.append(volume_info.get("imageLinks", {}).get("smallThumbnail"))
    return list_of_books, image_links

def get_similar_books(sim_test, book, df):
    if book in df["title"].values:
        idx = df[df["title"] == book].index[0]
        sim_scores = sorted(list(enumerate(sim_test[idx])), key=lambda x: x[1], reverse=True)
        first_elements = [item[0] for item in sim_scores]
        suggestions = df.iloc[first_elements]['title']
        return suggestions
    else:
        return None

def display_results(suggestions, df, book):
    if suggestions is not None:
        st.dataframe(suggestions)
        st.image(df['link'][df["title"] == book].iloc[0])
    else:
        st.subheader("Book Not Found")

data = get_book_data(book)
list_of_books, image_links = extract_book_info(data)
df = pd.DataFrame({"title": list_of_books, "link": image_links})

button = st.button("Read")

if button:
    suggestions = get_similar_books(sim_test, book, df)
    display_results(suggestions, df, book)
    
    

