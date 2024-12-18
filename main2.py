import streamlit as st
import requests
import pandas as pd
import pickle

st.title("Books You'ld Love to read!")

book = st.text_input("Enter a book name")

with open('/workspaces/codespaces-blank/sim_test.pkl', 'rb') as file:
  sim_test = pickle.load(file)

response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={book}")
data = response.json()

# print(response.text)

list_of_books = []
image_links = []

for i in data.get('items', []):
    volumeInfo = data.get('volumeInfo', {})
    list_of_books.append(volumeInfo.get('title'))
    image_links.append(volumeInfo.get('imageLinks', {}).get('smallThumbnail'))


df = pd.DataFrame({"title": list_of_books, "link": image_links})

button = st.button("Read")

if button:

    if book in df["title"].values:

        print("book in df")
        idx = df[df["title"] == book].index[0]
        sim_scores = sorted(
            list(enumerate(sim_test[idx])), key=lambda x: x[1], reverse=True
        )
        print(sorted(list(enumerate(sim_test[idx])), key=lambda x: x[1], reverse=True))
        first_elements = [item[0] for item in sim_scores]
        suggestions = df.iloc[first_elements]['title']
        
        st.dataframe(suggestions)

        st.image(df['link'][idx])

    else:
        print("Book not found in the dataset.")
        print(df["title"])
        st.subheader("Book Not Found")