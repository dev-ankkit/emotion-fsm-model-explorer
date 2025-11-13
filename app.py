import streamlit as st
import pandas as pd
from dataclasses import dataclass, field, asdict
import logging

# Suppress Streamlit's internal warnings
logging.getLogger("streamlit").setLevel(logging.ERROR)

# ====================================================================
# === 1. DATA & WEIGHTS CLASSES ===
# ====================================================================

# --- Input Classes ---
@dataclass
class EmotionProfile:
product_familiarity: float = 0.1
cognitive_ability: float = 0.5
ocean_neuroticism: float = 0.5
ocean_openness: float = 0.5
ocean_conscientiousness: float = 0.5

@dataclass
class EmotionContext:
interface_complexity: float = 0.3
external_situation_pressure: float = 0.1

# --- Weights Classes ---
@dataclass
class ConfusedWeights:
base_intensity: float = 0.4
neuroticism_weight: float = 0.5
familiarity_weight: float = 0.2
cognitive_ability_weight: float = 0.1
interface_complexity_weight: float = 0.2

@dataclass
class InControlWeights:
base_intensity: float = 0.5
conscientiousness_weight: float = 0.2
familiarity_weight: float = 0.3
external_pressure_weight: float = 0.1

@dataclass
class NeutralWeights:
base_intensity: float = 0.1
neuroticism_weight: float = 0.1

@dataclass
class EmotionModelWeights:
confused: ConfusedWeights = field(default_factory=ConfusedWeights)
in_control: InControlWeights = field(default_factory=InControlWeights)
neutral: NeutralWeights = field(default_factory=NeutralWeights)

# ====================================================================
# === 2. CALCULATION LOGIC (Decoupled from the FSM) ===
# ====================================================================
# We use standalone functions here for clarity in the tool.

def calculate_confused_intensity(profile: EmotionProfile, context: EmotionContext, weights: ConfusedWeights) -> float:
"""Calculates the intensity for the 'Confused' state."""
intensity = weights.base_intensity

# Intrinsic
intensity += profile.ocean_neuroticism * weights.neuroticism_weight
intensity += (1.0 - profile.product_familiarity) * weights.familiarity_weight
intensity -= profile.cognitive_ability * weights.cognitive_ability_weight

# Extrinsic
intensity += context.interface_complexity * weights.interface_complexity_weight

return max(0.0, min(1.0, intensity))

def calculate_incontrol_intensity(profile: EmotionProfile, context: EmotionContext, weights: InControlWeights) -> float:
"""Calculates the intensity for the 'InControl' state."""
intensity = weights.base_intensity

# Intrinsic
intensity += profile.ocean_conscientiousness * weights.conscientiousness_weight
intensity += profile.product_familiarity * weights.familiarity_weight

# Extrinsic
intensity += context.external_situation_pressure * weights.external_pressure_weight

return max(0.0, min(1.0, intensity))

def calculate_neutral_intensity(profile: EmotionProfile, context: EmotionContext, weights: NeutralWeights) -> float:
"""Calculates the intensity for the 'Neutral' state."""
intensity = weights.base_intensity

# Intrinsic
intensity += profile.ocean_neuroticism * weights.neuroticism_weight

return max(0.0, min(1.0, intensity))

# ====================================================================
# === 3. STREAMLIT INTERACTIVE APP ===
# ====================================================================

st.set_page_config(layout="wide")
st.title("Emotion Model Tuning Dashboard")

# --- Sliders in the Sidebar ---
st.sidebar.header("Agent Profile (Intrinsic)")
p_neuro = st.sidebar.slider("Neuroticism", 0.0, 1.0, 0.5)
p_consc = st.sidebar.slider("Conscientiousness", 0.0, 1.0, 0.5)
p_open = st.sidebar.slider("Openness", 0.0, 1.0, 0.5)
p_cog = st.sidebar.slider("Cognitive Ability", 0.0, 1.0, 0.5)
p_fam = st.sidebar.slider("Product Familiarity", 0.0, 1.0, 0.2)

st.sidebar.header("Situational Context (Extrinsic)")
c_complex = st.sidebar.slider("Interface Complexity", 0.0, 1.0, 0.3)
c_pressure = st.sidebar.slider("External Pressure", 0.0, 1.0, 0.1)

# --- Model Weights in Expanders ---
st.sidebar.header("Model Tuning Weights")
with st.sidebar.expander("Confused State Weights"):
w_c_base = st.slider("Base Intensity", 0.0, 1.0, 0.4, key="w_c_base")
# Note: Weights can go > 1.0 to increase sensitivity
w_c_neuro = st.slider("Neuroticism Weight", 0.0, 2.0, 0.5, key="w_c_neuro")
w_c_fam = st.slider("Familiarity Weight", 0.0, 2.0, 0.2, key="w_c_fam")
w_c_cog = st.slider("Cognitive Ability Weight", 0.0, 2.0, 0.1, key="w_c_cog")
w_c_complex = st.slider("Interface Complexity Weight", 0.0, 2.0, 0.2, key="w_c_comp")

with st.sidebar.expander("InControl State Weights"):
w_ic_base = st.slider("Base Intensity", 0.0, 1.0, 0.5, key="w_ic_base")
w_ic_consc = st.slider("Conscientiousness Weight", 0.0, 2.0, 0.2, key="w_ic_consc")
w_ic_fam = st.slider("Familiarity Weight", 0.0, 2.0, 0.3, key="w_ic_fam")
w_ic_press = st.slider("External Pressure Weight", 0.0, 2.0, 0.1, key="w_ic_press")

with st.sidebar.expander("Neutral State Weights"):
w_n_base = st.slider("Base Intensity", 0.0, 1.0, 0.1, key="w_n_base")
w_n_neuro = st.slider("Neuroticism Weight", 0.0, 2.0, 0.1, key="w_n_neuro")


# --- Collect slider values into their dataclasses ---
profile = EmotionProfile(
product_familiarity=p_fam,
cognitive_ability=p_cog,
ocean_neuroticism=p_neuro,
ocean_openness=p_open,
ocean_conscientiousness=p_consc
)

context = EmotionContext(
interface_complexity=c_complex,
external_situation_pressure=c_pressure
)

weights = EmotionModelWeights(
confused=ConfusedWeights(
base_intensity=w_c_base,
neuroticism_weight=w_c_neuro,
familiarity_weight=w_c_fam,
cognitive_ability_weight=w_c_cog,
interface_complexity_weight=w_c_complex
),
in_control=InControlWeights(
base_intensity=w_ic_base,
conscientiousness_weight=w_ic_consc,
familiarity_weight=w_ic_fam,
external_pressure_weight=w_ic_press
),
neutral=NeutralWeights(
base_intensity=w_n_base,
neuroticism_weight=w_n_neuro
)
)

# --- Calculate the 3 intensities based on current slider values ---
i_confused = calculate_confused_intensity(profile, context, weights.confused)
i_incontrol = calculate_incontrol_intensity(profile, context, weights.in_control)
i_neutral = calculate_neutral_intensity(profile, context, weights.neutral)


# --- Main Page Layout ---
st.header("Live Intensity Output")
st.markdown("""
This bar chart shows the *potential* intensity for each of the three states,
given the current settings in the sidebar. This is the **most important**
part of the tool.
""")

# Create a DataFrame for the bar chart
chart_data = pd.DataFrame(
{
"State": ["Confused", "InControl", "Neutral"],
"Intensity": [i_confused, i_incontrol, i_neutral],
}
)

# Display the bar chart
st.bar_chart(chart_data.set_index("State"))

# --- Show the raw data objects ---
st.header("Current Model Configuration")
col1, col2, col3 = st.columns(3)

with col1:
st.subheader("Agent Profile")
st.json(profile.__dict__)

with col2:
st.subheader("Situation Context")
st.json(context.__dict__)

with col3:
st.subheader("Model Weights")
st.json(asdict(weights))
