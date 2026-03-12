import streamlit as st

st.set_page_config(page_title="Massimo Dutti | Shoe Finder", layout="centered")

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
.block-container {
    max-width: 1000px;
    padding-top: 1.2rem;
}
div.stButton > button {
    background-color: #3E2F23;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.65rem 1.1rem;
    font-weight: 600;
}
div.stButton > button:hover {
    background-color: #1F2A44;
}
.card {
    border: 1px solid rgba(0,0,0,0.10);
    border-radius: 18px;
    padding: 18px;
    background: rgba(255,255,255,0.80);
}
.chip {
    display:inline-block;
    padding: 6px 10px;
    border-radius: 999px;
    border: 1px solid rgba(0,0,0,0.12);
    font-size: 0.85rem;
    margin-right: 6px;
    margin-bottom: 6px;
    opacity: 0.85;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown("## Massimo Dutti")
st.title("Let Massimo Dutti pick your Shoe for the day")
st.caption("Απαντήστε σε 6 ερωτήματα και δείτε το παπούτσι που σας ταιριάζει περισσότερο.")
st.divider()

# -----------------------------
# Αποτελέσματα / προϊόντα
# -----------------------------
RESULTS = {
    "Minimal Sneaker": {
        "image": "images/minimal.jpg",
        "brand": "Massimo Dutti",
        "model": "Δερμάτινο Minimal Sneaker",
        "price": "79.95€",
        "desc": "Minimal sneaker για καθημερινό στυλ, εύκολο να συνδυαστεί.",
        "link": "https://www.massimodutti.com/gr/contrast-trainers-l11303750?pelement=56778565"
    },
    "Smart Casual": {
        "image": "images/smart.jpg",
        "brand": "Massimo Dutti",
        "model": "Smart Casual Μπαλαρίνα",
        "price": "79.95€",
        "desc": "Προσεγμένο παπούτσι για δουλειά και έξοδο, με ισορροπία άνεσης και κομψότητας.",
        "link": "https://www.massimodutti.com/gr/crackled-leather-ballet-flats-l11555650?pelement=56839111"
    },
    "Formal": {
        "image": "images/formal.jpg",
        "brand": "Massimo Dutti",
        "model": "Formal Δερμάτινο Τακούνι",
        "price": "89.95€",
        "desc": "Τακούνι για επίσημες περιστάσεις και πιο formal εμφανίσεις.",
        "link": "https://www.massimodutti.com/gr/highheel-slingback-shoes-l11404750?pelement=56717461"
    },
    "Outdoor": {
        "image": "images/outdoor.jpg",
        "brand": "Massimo Dutti",
        "model": "Suede Μοκασίνι",
        "price": "89.95€",
        "desc": "Ανθεκτικό και σταθερό, χαρίζει άνεση και κομψότητα",
        "link": "https://www.massimodutti.com/gr/split-leather-loafers-with-gathered-bow-l11543650?pelement=57441691"
    },
    "Sport": {
        "image": "images/sport.jpg",
        "brand": "Massimo Dutti",
        "model": "Αθλητικό Sneaker",
        "price": "89.95€",
        "desc": "Άνετο sneaker για κίνηση και δραστήρια καθημερινότητα.",
        "link": "https://www.massimodutti.com/gr/split-leather-trainers-with-piece-details-l11305750?pelement=57220497"
    }
}

PROFILES = list(RESULTS.keys())

# -----------------------------
# Επιλογές και scoring maps
# -----------------------------
STYLE_OPTIONS = ["Casual", "Smart casual", "Formal", "Outdoor", "Sport"]
STYLE_MAP = {
    "Casual": {"Minimal Sneaker": 3, "Smart Casual": 1},
    "Smart casual": {"Smart Casual": 3, "Minimal Sneaker": 1},
    "Formal": {"Formal": 4, "Smart Casual": 1},
    "Outdoor": {"Outdoor": 4},
    "Sport": {"Sport": 4},
}

USE_OPTIONS = ["Καθημερινά", "Δουλειά/γραφείο", "Εκδηλώσεις", "Ταξίδια/περπάτημα", "Γυμναστική"]
USE_MAP = {
    "Καθημερινά": {"Minimal Sneaker": 3, "Smart Casual": 1},
    "Δουλειά/γραφείο": {"Smart Casual": 3, "Formal": 1},
    "Εκδηλώσεις": {"Formal": 3, "Smart Casual": 2},
    "Ταξίδια/περπάτημα": {"Outdoor": 2, "Minimal Sneaker": 2},
    "Γυμναστική": {"Sport": 4},
}

PRIORITY_OPTIONS = ["Η άνεση", "Το στυλ", "Η αντοχή", "Η ελαφρότητα", "Η κομψότητα"]
PRIORITY_MAP = {
    "Η άνεση": {"Minimal Sneaker": 2, "Sport": 2},
    "Το στυλ": {"Smart Casual": 3, "Formal": 2},
    "Η αντοχή": {"Outdoor": 4},
    "Η ελαφρότητα": {"Sport": 3, "Minimal Sneaker": 2},
    "Η κομψότητα": {"Formal": 3, "Smart Casual": 2},
}

COLORS_OPTIONS = ["Ουδέτερα", "Σκούρα", "Γήινα", "Έντονα", "Μονόχρωμο"]
COLORS_MAP = {
    "Ουδέτερα": {"Minimal Sneaker": 3, "Smart Casual": 1},
    "Σκούρα": {"Smart Casual": 2, "Formal": 2},
    "Γήινα": {"Outdoor": 2, "Smart Casual": 1},
    "Έντονα": {"Sport": 3, "Minimal Sneaker": 1},
    "Μονόχρωμο": {"Formal": 2, "Minimal Sneaker": 2},
}

MATERIAL_OPTIONS = ["Δέρμα", "Σουέντ", "Ύφασμα/canvas", "Mixed", "Αδιάβροχο"]
MATERIAL_MAP = {
    "Δέρμα": {"Smart Casual": 2, "Formal": 2},
    "Σουέντ": {"Smart Casual": 3},
    "Ύφασμα/canvas": {"Minimal Sneaker": 3, "Sport": 1},
    "Mixed": {"Sport": 3, "Minimal Sneaker": 1},
    "Αδιάβροχο": {"Outdoor": 4},
}

SHAPE_OPTIONS = ["Slim/minimal", "Κλασική", "Chunky", "Κομψή", "Αθλητική"]
SHAPE_MAP = {
    "Slim/minimal": {"Minimal Sneaker": 3, "Formal": 1},
    "Κλασική": {"Smart Casual": 2, "Outdoor": 4},
    "Chunky": {"Sport": 2, "Minimal Sneaker": 1},
    "Κομψή": {"Outdoor": 4},
    "Αθλητική": {"Sport": 4},
}

# -----------------------------
# Session state
# -----------------------------
if "step" not in st.session_state:
    st.session_state.step = 1

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# -----------------------------
# Functions
# -----------------------------
def reset():
    st.session_state.step = 1
    st.session_state.answers = {}
    st.session_state.submitted = False

def add_scores(scores, deltas):
    for key, value in deltas.items():
        scores[key] += value

def compute_result():
    scores = {p: 0 for p in PROFILES}
    required_keys = ["style", "use", "priority", "colors", "material", "shape"]

    for key in required_keys:
        if key not in st.session_state.answers:
            st.error(f"Λείπει απάντηση για: {key}")
            return None, None, None

        if "scores" not in st.session_state.answers[key]:
            st.error(f"Λείπουν scores για: {key}")
            return None, None, None

        add_scores(scores, st.session_state.answers[key]["scores"])

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best = ranked[0][0]
    return best, ranked, scores

def chips_from_answers():
    chips = []
    if "style" in st.session_state.answers:
        chips.append(st.session_state.answers["style"]["choice"])
    if "colors" in st.session_state.answers:
        chips.append(st.session_state.answers["colors"]["choice"])
    if "material" in st.session_state.answers:
        chips.append(st.session_state.answers["material"]["choice"])
    if "priority" in st.session_state.answers:
        chips.append(st.session_state.answers["priority"]["choice"])
    return chips

def step_ui(key, title, question, options, score_map, horizontal=False):
    st.subheader(title)

    prev = st.session_state.answers.get(key, {}).get("choice", None)
    idx = options.index(prev) if prev in options else None

    choice = st.radio(
        question,
        options,
        index=idx,
        horizontal=horizontal,
        key=f"ui_{key}"
    )

    if choice in score_map:
        st.session_state.answers[key] = {
            "choice": choice,
            "scores": score_map[choice]
        }
    else:
        st.error(f"Η επιλογή '{choice}' δεν υπάρχει στο map της ερώτησης '{key}'.")

# -----------------------------
# Progress / navigation
# -----------------------------
st.progress((st.session_state.step - 1) / 6)
st.write(f"Βήμα **{st.session_state.step}/6**")

col_a, col_b, col_c = st.columns([1, 1, 1])

with col_a:
    st.button("↩️ Reset", on_click=reset)

with col_b:
    if st.session_state.step > 1 and not st.session_state.submitted:
        if st.button("⬅️ Πίσω"):
            st.session_state.step -= 1

with col_c:
    st.write("")

st.divider()

# -----------------------------
# Wizard
# -----------------------------
if not st.session_state.submitted:
    if st.session_state.step == 1:
        step_ui(
            "style",
            "1) Ύφος",
            "Διαλέξτε αυτό που σας εκφράζει περισσότερο:",
            STYLE_OPTIONS,
            STYLE_MAP,
            horizontal=True
        )

    elif st.session_state.step == 2:
        step_ui(
            "use",
            "2) Χρήση",
            "Πού θα το φοράτε πιο συχνά;",
            USE_OPTIONS,
            USE_MAP
        )

    elif st.session_state.step == 3:
        step_ui(
            "priority",
            "3) Προτεραιότητα",
            "Επιλέξτε το πιο σημαντικό για εσάς.",
            PRIORITY_OPTIONS,
            PRIORITY_MAP,
            horizontal=True
        )

    elif st.session_state.step == 4:
        step_ui(
            "colors",
            "4) Τόνοι/Χρώματα",
            "Ποια χρώματα προτιμάτε;",
            COLORS_OPTIONS,
            COLORS_MAP
        )

    elif st.session_state.step == 5:
        step_ui(
            "material",
            "5) Υλικό",
            "Τι υλικό προτιμάτε;",
            MATERIAL_OPTIONS,
            MATERIAL_MAP
        )

    elif st.session_state.step == 6:
        step_ui(
            "shape",
            "6) Γραμμή",
            "Τι γραμμή θέλετε;",
            SHAPE_OPTIONS,
            SHAPE_MAP,
            horizontal=True
        )

    nav1, nav2 = st.columns([1, 1])

    with nav1:
        if st.session_state.step < 6:
            if st.button("➡️ Επόμενο"):
                st.session_state.step += 1
        else:
            if st.button("✅ Δες αποτέλεσμα"):
                required_keys = ["style", "use", "priority", "colors", "material", "shape"]
                missing = [k for k in required_keys if k not in st.session_state.answers]

                if missing:
                    st.error(f"Δεν έχουν απαντηθεί όλα τα βήματα. Λείπουν: {', '.join(missing)}")
                else:
                    st.session_state.submitted = True

# -----------------------------
# Result
# -----------------------------
if st.session_state.submitted:
    best, ranked, scores = compute_result()

    if best is None:
        st.stop()

    product = RESULTS[best]
    chips = chips_from_answers()

    st.subheader("Αποτέλεσμα")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    left, right = st.columns([1.1, 1.2])

    with left:
        st.image(product["image"], use_container_width=True)

    with right:
        st.markdown(f"### {product['brand']}")
        st.markdown(f"## {product['model']}")
        st.markdown(f"**Τιμή:** {product['price']}")
        st.write(product["desc"])

        if chips:
            st.write("**Γιατί σας ταιριάζει:**")
            st.markdown(
                "".join([f"<span class='chip'>{chip}</span>" for chip in chips]),
                unsafe_allow_html=True
            )

        st.caption(f"Match score: {scores[best]}")

        if "link" in product and product["link"]:
            st.link_button("Δείτε το προϊόν", product["link"])

    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("🔎 Debug: Απαντήσεις & Σκορ"):
        st.write("### Επιλογές χρήστη")
        for key, value in st.session_state.answers.items():
            st.write(f"- **{key}**: {value['choice']}")

        st.write("### Τελικό σκορ")
        st.write(scores)

    st.write("")
    st.button("🔁 Ξανακάνετε το quiz", on_click=reset)
