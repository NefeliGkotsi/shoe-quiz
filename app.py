import os
import streamlit as st

st.set_page_config(page_title="Massimo Dutti | Shoe Finder", layout="centered")

# --- Minimal styling (καφέ + σκούρο μπλε) ---
st.markdown("""
<style>
.block-container { padding-top: 1.6rem; max-width: 860px; }
div.stButton > button {
    background-color: #3E2F23;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.65rem 1.1rem;
    font-weight: 650;
}
div.stButton > button:hover { background-color: #1F2A44; }
.card {
    background: rgba(255,255,255,0.65);
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 18px;
    padding: 16px 16px;
}
.small { opacity: 0.78; font-size: 0.95rem; }
</style>
""", unsafe_allow_html=True)

st.title("Let Massimo Dutti choose your shoe for the day")
st.caption("Απαντήστεε 6 ερωτήσεις και δείτε την καλύτερη πρόταση (Massimo Dutti) με φωτογραφία.")
st.divider()

# --- Αποτελέσματα (στα ελληνικά) ---
RESULTS = {
    "Minimal Sneaker": {
        "image": "images/minimal.jpg",
        "brand": "Massimo Dutti",
        "model": "Δερμάτινο Minimal Sneaker",
        "price": "79.95€",
        "desc": "Minimal δερμάτινο sneaker για καθημερινό στυλ, εύκολο να συνδυαστεί."
    },
    "Smart Casual": {
        "image": "images/smart.jpg",
        "brand": "Massimo Dutti",
        "model": "Smart Casual Δερμάτινη Μπαλαρίνα",
        "price": "79.95€",
        "desc": "Προσεγμένο παπούτσι για δουλειά/έξοδο, ισορροπία άνεσης και κομψότητας."
    },
    "Formal": {
        "image": "images/formal.jpg",
        "brand": "Massimo Dutti",
        "model": "Formal Δερμάτινο με Τακούνι",
        "price": "89.95€",
        "desc": "Κλασική γραμμή για πιο επίσημες περιστάσεις."
    },
    "Outdoor": {
        "image": "images/outdoor.jpg",
        "brand": "Massimo Dutti",
        "model": "Δερμάτινο Μοκασίνι",
        "price": "89.95€",
        "desc": "Ανθεκτικό και σταθερό, χαρίζει άνεση και κομψότητα."
    },
    "Sport": {
        "image": "images/sport.jpg",
        "brand": "Massimo Dutti",
        "model": "Αθλητικό Sneaker",
        "price": "89.98",
        "desc": "Άνετο sneaker για κίνηση και καθημερινή δραστηριότητα."
    },
}
PROFILES = list(RESULTS.keys())

# --- state ---
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False

def reset_quiz():
    st.session_state.answers = {}
    st.session_state.submitted = False

def add_scores(scores, deltas):
    for k, v in deltas.items():
        scores[k] += v

def compute_result(answers_scores):
    scores = {p: 0 for p in PROFILES}
    for key in ["style", "use", "priority", "colors", "material", "shape"]:
        add_scores(scores, answers_scores[key])
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best = ranked[0][0]
    return best, ranked, scores

# --- progress ---
answered = len(st.session_state.answers)
st.progress(min(answered / 6, 1.0))
st.write(f"Βήματα: **{answered}/6**")

st.button("↩️ Reset", on_click=reset_quiz)
st.divider()

def step_radio(step_key, title, question, options, score_map, horizontal=False):
    st.subheader(title)
    choice = st.radio(
        question,
        options,
        index=None if step_key not in st.session_state.answers else options.index(st.session_state.answers[step_key]["_choice"]),
        horizontal=horizontal,
        key=f"ui_{step_key}"
    )
    if choice is not None:
        st.session_state.answers[step_key] = {"_choice": choice, "_scores": score_map[choice]}

# --- 6 ερωτήσεις ---
step_radio(
    "style",
    "1) Ύφος",
    "Διαλέξτε αυτό που σας εκφράζει περισσότερο:",
    ["Casual", "Smart casual", "Formal", "Outdoor", "Sport"],
    {
        "Casual": {"Minimal Sneaker": 3, "Smart Casual": 1},
        "Smart casual": {"Smart Casual": 3, "Minimal Sneaker": 1},
        "Formal": {"Formal": 4, "Smart Casual": 1},
        "Outdoor": {"Outdoor": 4},
        "Sport": {"Sport": 4},
    },
    horizontal=True
)

step_radio(
    "use",
    "2) Χρήση",
    "Πού θα το φοράτε πιο συχνά;",
    ["Καθημερινά", "Δουλειά/γραφείο", "Εκδηλώσεις", "Ταξίδια/περπάτημα", "Γυμναστική"],
    {
        "Καθημερινά": {"Minimal Sneaker": 3, "Smart Casual": 1},
        "Δουλειά/γραφείο": {"Smart Casual": 3, "Formal": 1},
        "Εκδηλώσεις": {"Formal": 3, "Smart Casual": 2},
        "Ταξίδια/περπάτημα": {"Outdoor": 2, "Minimal Sneaker": 2},
        "Γυμναστική": {"Sport": 4},
    }
)

step_radio(
    "priority",
    "3) Προτεραιότητα",
    "Τι μετράει περισσότερο;",
    ["Άνεση", "Στυλ", "Αντοχή", "Ελαφρύ", "Κλασικότητα"],
    {
        "Άνεση": {"Minimal Sneaker": 2, "Sport": 2},
        "Στυλ": {"Smart Casual": 3, "Formal": 2},
        "Αντοχή": {"Outdoor": 4},
        "Ελαφρύ": {"Sport": 3, "Minimal Sneaker": 2},
        "Κλασικότητα": {"Formal": 3, "Smart Casual": 2},
    },
    horizontal=True
)

step_radio(
    "colors",
    "4) Τόνοι / Χρώματα",
    "Ποια χρώματα προτιμάς;",
    ["Ουδέτερα", "Σκούρα", "Γήινα", "Έντονα", "Μονόχρωμο"],
    {
        "Ουδέτερα": {"Minimal Sneaker": 3, "Smart Casual": 1},
        "Σκούρα": {"Smart Casual": 2, "Formal": 2},
        "Γήινα": {"Outdoor": 2, "Smart Casual": 1},
        "Έντονα": {"Sport": 3, "Minimal Sneaker": 1},
        "Μονόχρωμο": {"Formal": 2, "Minimal Sneaker": 2},
    }
)

step_radio(
    "material",
    "5) Υλικό",
    "Τι υλικό προτιμάτε;",
    ["Δέρμα", "Σουέντ", "Ύφασμα/canvas", "Mesh/συνθετικό", "Αδιάβροχο"],
    {
        "Δέρμα": {"Smart Casual": 2, "Formal": 2},
        "Σουέντ": {"Smart Casual": 3},
        "Ύφασμα/canvas": {"Minimal Sneaker": 3, "Sport": 1},
        "Mesh/συνθετικό": {"Sport": 3, "Minimal Sneaker": 1},
        "Αδιάβροχο": {"Outdoor": 4},
    }
)

step_radio(
    "shape",
    "6) Γραμμή",
    "Τι γραμμή θέλετε;",
    ["Slim/minimal", "Κλασική", "Chunky", "Rugged/μποτάκι", "Αθλητική"],
    {
        "Slim/minimal": {"Minimal Sneaker": 3, "Formal": 1},
        "Κλασική": {"Smart Casual": 2, "Formal": 2},
        "Chunky": {"Sport": 2, "Minimal Sneaker": 1},
        "Rugged/μποτάκι": {"Outdoor": 4},
        "Αθλητική": {"Sport": 4},
    },
    horizontal=True
)

st.divider()

all_done = all(k in st.session_state.answers for k in ["style", "use", "priority", "colors", "material", "shape"])

if st.button("✅ Δείτε το αποτέλεσμα", disabled=not all_done):
    st.session_state.submitted = True

if st.session_state.submitted and all_done:
    answers_scores = {k: st.session_state.answers[k]["_scores"] for k in st.session_state.answers}
    best, ranked, scores = compute_result(answers_scores)
    product = RESULTS[best]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.success(f"Προτεινόμενο παπούτσι: {product['brand']} — {product['model']}")
    st.image(product["image"], use_container_width=True)
    st.write(f"**Τιμή:** {product['price']}")
    st.write(product["desc"])
    st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("Εναλλακτικές προτάσεις (Top 3)")
    top3 = ranked[:3]
    cols = st.columns(3)
    for i, (name, sc) in enumerate(top3):
        p = RESULTS[name]
        with cols[i]:
            st.image(p["image"], use_container_width=True)
            st.write(f"**{p['model']}**")
            st.write(f"<span class='small'>{p['price']} • score {sc}</span>", unsafe_allow_html=True)
