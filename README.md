# Intelligent Movie Search and Recommendation System (Tollywood Focus)

An Information Retrieval Systems (IRS) college project that implements real-time semantic search and content-based movie recommendations using **TF-IDF (Term Frequency-Inverse Document Frequency) Vectorization** and **Cosine Similarity**, primarily focused on **Tollywood (Telugu Cinema)**.

Designed with a modern, responsive streaming interface inspired by Spotify/Netflix, featuring a dark background with attractive neon emerald green highlights.

---

## 🌟 Key Highlights & Features

1. **Intelligent Multi-Modal Search**:
   - **Movie Name**: Exact and partial title matching (e.g., `Baahubali`, `Pushpa`).
   - **Film Genre**: Action, Romance, Comedy, Thriller, Horror, Fantasy, Sci-Fi.
   - **Industry / Category**: Tollywood, Bollywood, Kollywood, Sandalwood, Mollywood.
   - **Storyline / Keywords**: Descriptive semantic queries without mentioning the title (e.g. `detective murder mystery`, `reincarnation fly revenge`, `cricket father son`).

2. **Tollywood-Prioritized Recommendation Engine**:
   - Recommends at least **5 similar Tollywood (Telugu) movies** for any selected film.
   - Recommendations are calculated purely from mathematical cosine similarities over TF-IDF feature matrices, never randomly generated.
   - Excludes the searched/selected movie from its own recommendations.
   - Graceful fallback messaging when fewer matches are available.

3. **Pure Information Retrieval Implementation**:
   - **Vector Space Model (VSM)** built with Scikit-Learn and Pandas.
   - **Sublinear TF Scaling**: Diminishes term domination via $1 + \log(\text{tf})$.
   - **Unigram & Bigram Features**: Captures compound phrases like `"period action"`, `"black magic"`, `"time travel"`.
   - **Relevance Scoring**: Computes and displays dynamic match percentage badges (e.g. `98% Match`).

4. **Modern Responsive Streaming Interface**:
   - Dark theme (`#0a0e14`, `#131c26`) with vivid emerald green highlights (`#00e676`).
   - Movie poster cards with badges for IMDb rating, industry, and relevance match.
   - Debounced live search autocomplete (`/api/suggest`).
   - Full keyboard shortcut support (`/` to focus search).
   - Local SVG fallback (`fallback.svg`) ensuring posters never break offline.
   - 100% responsive across mobile phones, tablets, and desktop computers.

5. **Local & Free**:
   - Works 100% locally on localhost.
   - Zero paid APIs, zero external API keys required.

---

## 📁 Project Folder Structure

```
intelligent-movie-search/
│
├── app.py                      # Flask web application and HTTP routing
├── ir_engine.py                # Information Retrieval engine (TF-IDF & Cosine Similarity)
├── movies.csv                  # Curated dataset with 50 verifiable movie records
├── requirements.txt            # Python dependencies (Flask, Pandas, Scikit-learn, NumPy)
├── test_ir.py                  # Automated test verification script
├── README.md                   # Complete documentation, setup guide & viva notes
│
├── templates/
│   ├── base.html               # Master layout with responsive navbar and footer
│   ├── index.html              # Home page with hero search and featured blockbusters
│   ├── search_results.html     # Search results with IR scores, filters, and empty state
│   ├── movie_details.html      # Movie details & Recommended Tollywood Movies section
│   ├── genres.html             # Genre browsing hub
│   ├── recommendations.html    # Interactive recommendation playground
│   └── about.html              # Academic IRS documentation and mathematical formulas
│
└── static/
    ├── css/
    │   └── style.css           # Custom dark streaming UI with emerald accents
    ├── js/
    │   └── script.js           # Live autocomplete, debouncing, and image fallbacks
    └── images/
        └── fallback.svg        # Clean vector poster placeholder for offline resilience
```

---

## 🛠️ Step-by-Step Installation & Setup (VS Code)

### Prerequisites
- Python 3.10+ (Python 3.14 supported)
- Visual Studio Code or any code editor

### Step 1: Open the Project in VS Code
1. Launch **VS Code**.
2. Go to **File** &rarr; **Open Folder...**
3. Select the project directory:
   ```
   C:\Users\VICTUS\.gemini\antigravity\scratch\intelligent-movie-search
   ```

### Step 2: Open a Terminal
In VS Code, press `Ctrl + \`` (backtick) or select **Terminal** &rarr; **New Terminal**.

### Step 3: Install Required Libraries
Run either of the following commands in the terminal:

```powershell
py -m pip install -r requirements.txt
```
*(Or if `python` is aliased in your environment:)*
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
Start the Flask development server:

```powershell
py app.py
```

You will see output similar to:
```
Starting Intelligent Movie Search and Recommendation System...
Serving on http://127.0.0.1:5000
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 5: Open in Your Browser
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧠 Information Retrieval Theory Explained

### 1. What is TF-IDF?
**TF-IDF** stands for **Term Frequency - Inverse Document Frequency**. It calculates how informative and discriminative a word is relative to a specific movie in the entire catalog.

- **Term Frequency (TF)**: How often a word appears in a movie's composite profile (title, genres, plot description).
  $$\text{TF}(t, d) = 1 + \ln(\text{count}(t, d))$$
- **Inverse Document Frequency (IDF)**: Penalizes generic words (like "movie", "man", "the") that occur across many documents and promotes rare, meaningful terms (like "Kattappa", "reincarnation", "cricket").
  $$\text{IDF}(t, D) = \ln\left(\frac{1 + |D|}{1 + \text{DF}(t)}\right) + 1$$
- **Combined Weight**:
  $$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

### 2. What is Cosine Similarity?
Each movie document and user query is represented as a high-dimensional vector $\vec{V}$ in Euclidean feature space.

Cosine Similarity measures the cosine of the angle $\theta$ between query vector $\vec{Q}$ and movie document vector $\vec{D}$:
$$\text{Cosine Similarity}(\vec{Q}, \vec{D}) = \frac{\vec{Q} \cdot \vec{D}}{\|\vec{Q}\| \|\vec{D}\|} = \frac{\sum_{i=1}^{V} Q_i D_i}{\sqrt{\sum_{i=1}^{V} Q_i^2} \sqrt{\sum_{i=1}^{V} D_i^2}}$$

- When $\theta = 0^\circ \implies \cos(\theta) = 1.0$: Identical topic or theme.
- When $\theta = 90^\circ \implies \cos(\theta) = 0.0$: Completely unrelated vectors.

---

## 🎯 Sample Demonstration Queries & Expected Outputs

| # | User Query | Purpose | Expected Top Search Results | Key Similar Tollywood Recommendations |
|---|---|---|---|---|
| **1** | `Baahubali` | Exact/Partial Title | *Baahubali: The Beginning*, *Baahubali 2* (98% Match) | *Magadheera*, *Eega*, *RRR*, *Mayabazar* |
| **2** | `investigative detective murder mystery` | Natural Storyline | *HIT: The Second Case* (98%), *Agent Sai Srinivasa Athreya* (94%), *Goodachari* (79%) | *HIT: The First Case*, *Brochevarevarura* |
| **3** | `cricket father son sport aspiration` | Emotional Concept | *Jersey* (98% Match) | *Dangal*, *Bommarillu*, *Arjun Reddy* |
| **4** | `reincarnation fly revenge` | Plot Synopsis | *Eega* (99% Match) | *Magadheera*, *Shyam Singha Roy*, *Arundhati* |
| **5** | `red sandalwood smuggling forest` | Story Elements | *Pushpa: The Rise*, *Pushpa 2: The Rule* (98% Match) | *Rangasthalam*, *Dasara*, *Salaar* |
| **6** | `village curse black magic tantric` | Subgenre Search | *Virupaksha* (97%), *Arundhati* (94%) | *Karthikeya 2*, *Kantara* |

---

## 🎓 College Viva / Project Q&A Quick Reference

**Q1: Why choose Vector Space Model (VSM) over Boolean Retrieval?**  
*Answer:* Boolean retrieval gives only binary results (match or no match). VSM ranks documents continuously by semantic relevance scores and permits partial matching.

**Q2: Why use Cosine Similarity instead of Euclidean Distance?**  
*Answer:* Euclidean distance is heavily distorted by document length (a movie with a 200-word synopsis would appear artificially far from a 30-word synopsis). Cosine similarity normalizes length and measures directional angular alignment.

**Q3: How does the system prioritize Tollywood movies?**  
*Answer:* The IR engine assigns an industry boost in the vector profile and filters the top $N$ recommendations by checking that `category == 'Tollywood'` or `language == 'Telugu'` before filling any remaining slots.

---

## 📄 License & Academic Attribution
Developed for Information Retrieval Systems (IRS) College Curriculum. Free for academic and educational evaluation.
