import streamlit as st
import pandas as pd
from dataclasses import dataclass, field, asdict
import logging
import plotly.graph_objects as go
# Suppress Streamlit's internal warnings
logging.getLogger("streamlit").setLevel(logging.ERROR)
​
# ====================================================================
# === 1. DATA & WEIGHTS CLASSES ===
# ====================================================================
​
# --- Input Classes ---
@dataclass
class EmotionProfile:
    product_familiarity: float = 0.1
    cognitive_ability: float = 0.5
    ocean_neuroticism: float = 0.5
    ocean_openness: float = 0.5
    ocean_conscientiousness: float = 0.5
​
@dataclass
class EmotionContext:
    interface_complexity: float = 0.3
    external_situation_pressure: float = 0.1
​
# --- Weights Classes ---
@dataclass
class ConfusedWeights:
    base_intensity: float = 0.4
    neuroticism_weight: float = 0.5
    familiarity_weight: float = 0.2
    cognitive_ability_weight: float = 0.1
    openness_weight: float = 0.15
    interface_complexity_weight: float = 0.2
​
@dataclass
class InControlWeights:
    base_intensity: float = 0.5
    conscientiousness_weight: float = 0.2
    familiarity_weight: float = 0.3
    openness_weight: float = 0.25
    external_pressure_weight: float = 0.1
​
@dataclass
class NeutralWeights:
    base_intensity: float = 0.1
    neuroticism_weight: float = 0.1
    openness_weight: float = 0.1
​
@dataclass
class EmotionModelWeights:
    confused: ConfusedWeights = field(default_factory=ConfusedWeights)
    in_control: InControlWeights = field(default_factory=InControlWeights)
    neutral: NeutralWeights = field(default_factory=NeutralWeights)
​
# ====================================================================
# === 2. CALCULATION LOGIC (Decoupled from the FSM) ===
# ====================================================================
# We use standalone functions here for clarity in the tool.
​
def calculate_confused_intensity(profile: EmotionProfile, context: EmotionContext, weights: ConfusedWeights) -> float:
    """Calculates the intensity for the 'Confused' state."""
    intensity = weights.base_intensity
​
    # Intrinsic
    intensity += profile.ocean_neuroticism * weights.neuroticism_weight
    intensity += (1.0 - profile.product_familiarity) * weights.familiarity_weight
    intensity -= profile.cognitive_ability * weights.cognitive_ability_weight
    # Openness reduces confusion (more adaptable and willing to explore)
    intensity -= profile.ocean_openness * weights.openness_weight
​
    # Extrinsic
    intensity += context.interface_complexity * weights.interface_complexity_weight
​
    return max(0.0, min(1.0, intensity))
​
def calculate_incontrol_intensity(profile: EmotionProfile, context: EmotionContext, weights: InControlWeights) -> float:
    """Calculates the intensity for the 'InControl' state."""
    intensity = weights.base_intensity
​
    # Intrinsic
    intensity += profile.ocean_conscientiousness * weights.conscientiousness_weight
    intensity += profile.product_familiarity * weights.familiarity_weight
    # Openness increases feeling in control (more adaptable and willing to learn)
    intensity += profile.ocean_openness * weights.openness_weight
​
    # Extrinsic
    intensity += context.external_situation_pressure * weights.external_pressure_weight
​
    return max(0.0, min(1.0, intensity))
​
def calculate_neutral_intensity(profile: EmotionProfile, context: EmotionContext, weights: NeutralWeights) -> float:
    """Calculates the intensity for the 'Neutral' state."""
    intensity = weights.base_intensity
​
    # Intrinsic
    intensity += profile.ocean_neuroticism * weights.neuroticism_weight
    # Openness has a slight positive effect on neutral state
    intensity += profile.ocean_openness * weights.openness_weight
​
    return max(0.0, min(1.0, intensity))
​
# ====================================================================
# === 3. STREAMLIT INTERACTIVE APP ===
# ====================================================================
​
st.set_page_config(layout="wide", page_title="Emotion Model Dashboard", initial_sidebar_state="expanded")
​
# Add custom CSS to reduce top spacing
st.markdown("""
    <style>
    .main > div {
        padding-top: 1rem;
    }
    h1 {
        margin-bottom: 0.5rem !important;
        padding-top: 0.5rem !important;
    }
    h3 {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    h4 {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    .stMetric {
        padding: 0.5rem 0.75rem;
    }
    .element-container {
        margin-bottom: 0.5rem;
    }
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column"] > [data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
​
st.markdown("<h1 style='text-align: center; margin-bottom: 0.5rem; padding-top: 0.5rem;'>Emotion Model Tuning Dashboard</h1>", unsafe_allow_html=True)
​
# --- Sliders in the Sidebar ---
st.sidebar.header("Agent Profile (Intrinsic)")
p_neuro = st.sidebar.slider("Neuroticism", 0.0, 1.0, 0.5)
p_consc = st.sidebar.slider("Conscientiousness", 0.0, 1.0, 0.5)
p_open = st.sidebar.slider("Openness", 0.0, 1.0, 0.5)
p_cog = st.sidebar.slider("Cognitive Ability", 0.0, 1.0, 0.5)
p_fam = st.sidebar.slider("Product Familiarity", 0.0, 1.0, 0.2)
​
st.sidebar.header("Situational Context (Extrinsic)")
c_complex = st.sidebar.slider("Interface Complexity", 0.0, 1.0, 0.3)
c_pressure = st.sidebar.slider("External Pressure", 0.0, 1.0, 0.1)
​
# --- Model Weights in Expanders ---
st.sidebar.header("Model Tuning Weights")
with st.sidebar.expander("Confused State Weights"):
    w_c_base = st.slider("Base Intensity", 0.0, 1.0, 0.4, key="w_c_base")
    # Note: Weights can go > 1.0 to increase sensitivity
    w_c_neuro = st.slider("Neuroticism Weight", 0.0, 2.0, 0.5, key="w_c_neuro")
    w_c_fam = st.slider("Familiarity Weight", 0.0, 2.0, 0.2, key="w_c_fam")
    w_c_cog = st.slider("Cognitive Ability Weight", 0.0, 2.0, 0.1, key="w_c_cog")
    w_c_open = st.slider("Openness Weight", 0.0, 2.0, 0.15, key="w_c_open")
    w_c_complex = st.slider("Interface Complexity Weight", 0.0, 2.0, 0.2, key="w_c_comp")
​
with st.sidebar.expander("InControl State Weights"):
    w_ic_base = st.slider("Base Intensity", 0.0, 1.0, 0.5, key="w_ic_base")
    w_ic_consc = st.slider("Conscientiousness Weight", 0.0, 2.0, 0.2, key="w_ic_consc")
    w_ic_fam = st.slider("Familiarity Weight", 0.0, 2.0, 0.3, key="w_ic_fam")
    w_ic_open = st.slider("Openness Weight", 0.0, 2.0, 0.25, key="w_ic_open")
    w_ic_press = st.slider("External Pressure Weight", 0.0, 2.0, 0.1, key="w_ic_press")
​
with st.sidebar.expander("Neutral State Weights"):
    w_n_base = st.slider("Base Intensity", 0.0, 1.0, 0.1, key="w_n_base")
    w_n_neuro = st.slider("Neuroticism Weight", 0.0, 2.0, 0.1, key="w_n_neuro")
    w_n_open = st.slider("Openness Weight", 0.0, 2.0, 0.1, key="w_n_open")
​
​
# --- Collect slider values into their dataclasses ---
profile = EmotionProfile(
    product_familiarity=p_fam,
    cognitive_ability=p_cog,
    ocean_neuroticism=p_neuro,
    ocean_openness=p_open,
    ocean_conscientiousness=p_consc
)
​
context = EmotionContext(
    interface_complexity=c_complex,
    external_situation_pressure=c_pressure
)
​
weights = EmotionModelWeights(
    confused=ConfusedWeights(
        base_intensity=w_c_base,
        neuroticism_weight=w_c_neuro,
        familiarity_weight=w_c_fam,
        cognitive_ability_weight=w_c_cog,
        openness_weight=w_c_open,
        interface_complexity_weight=w_c_complex
    ),
    in_control=InControlWeights(
        base_intensity=w_ic_base,
        conscientiousness_weight=w_ic_consc,
        familiarity_weight=w_ic_fam,
        openness_weight=w_ic_open,
        external_pressure_weight=w_ic_press
    ),
    neutral=NeutralWeights(
        base_intensity=w_n_base,
        neuroticism_weight=w_n_neuro,
        openness_weight=w_n_open
    )
)
​
# --- Calculate the 3 intensities based on current slider values ---
i_confused = calculate_confused_intensity(profile, context, weights.confused)
i_incontrol = calculate_incontrol_intensity(profile, context, weights.in_control)
i_neutral = calculate_neutral_intensity(profile, context, weights.neutral)
​
​
# --- Main Page Layout ---
# Compact header and metrics
st.markdown("### Live Intensity Output")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Confused", f"{i_confused:.3f}")
with col2:
    st.metric("Neutral", f"{i_neutral:.3f}")
with col3:
    st.metric("InControl", f"{i_incontrol:.3f}")
with col4:
    max_intensity = max(i_confused, i_incontrol, i_neutral)
    dominant_state = ["Confused", "InControl", "Neutral"][
        [i_confused, i_incontrol, i_neutral].index(max_intensity)
    ]
    st.metric("Dominant State", dominant_state, delta=f"{max_intensity:.3f}")
​
# Create a DataFrame for the chart
chart_data = pd.DataFrame(
    {
        "State": ["Confused", "InControl", "Neutral"],
        "Intensity": [i_confused, i_incontrol, i_neutral],
    }
)
​
# Create interactive Plotly bar chart with fixed y-axis
fig = go.Figure()
​
# Add bars with custom colors
colors = ['#FF6B6B', '#2DBB3E', '#95E1D3']
for i, (state, intensity) in enumerate(zip(chart_data["State"], chart_data["Intensity"])):
    fig.add_trace(go.Bar(
        x=[state],
        y=[intensity],
        name=state,
        marker_color=colors[i],
        text=[f"{intensity:.3f}"],
        textposition='outside',
        hovertemplate=f"<b>{state}</b><br>Intensity: {intensity:.3f}<extra></extra>",
    ))
​
# Update layout with fixed y-axis and interactive features
fig.update_layout(
    title={
        'text': 'Emotion State Intensities',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 16},
        'y': 0.95,
        'yanchor': 'top'
    },
    xaxis_title="Emotion State",
    yaxis_title="Intensity",
    yaxis=dict(range=[0, 1.2], dtick=0.2),
    height=450,
    hovermode='x unified',
    showlegend=False,
    template='plotly_white',
    font=dict(size=12),
    margin=dict(l=50, r=50, t=50, b=40)
)
​
# Display the interactive chart
st.plotly_chart(fig, width='stretch')
​
# Add a line chart showing intensity comparison
st.markdown("#### Intensity Comparison")
fig_line = go.Figure()
​
# Create a connected line chart by plotting all points in sequence
fig_line.add_trace(go.Scatter(
    x=chart_data["State"],
    y=chart_data["Intensity"],
    mode='lines+markers',
    name='Intensity Trend',
    marker=dict(size=15, color='#888888'),
    line=dict(width=3, color='#888888'),
    hovertemplate="<b>%{x}</b><br>Intensity: %{y:.3f}<extra></extra>",
))
​
# Add individual colored markers for each state
for i, (state, intensity) in enumerate(zip(chart_data["State"], chart_data["Intensity"])):
    fig_line.add_trace(go.Scatter(
        x=[state],
        y=[intensity],
        mode='markers',
        name=state,
        marker=dict(size=20, color=colors[i], line=dict(width=2, color='white')),
        hovertemplate=f"<b>{state}</b><br>Intensity: {intensity:.3f}<extra></extra>",
        showlegend=False,
    ))
​
fig_line.update_layout(
    xaxis_title="Emotion State",
    yaxis_title="Intensity",
    yaxis=dict(range=[0, 1.2], dtick=0.2),
    height=350,
    hovermode='x unified',
    template='plotly_white',
    font=dict(size=12),
    margin=dict(l=50, r=50, t=30, b=40)
)
​
st.plotly_chart(fig_line, width='stretch')
​
# --- Show the raw data objects ---
st.markdown("### Current Model Configuration")
​
# Add expandable sections for better organization
with st.expander("📊 View Raw Configuration Data", expanded=False):
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
​
# Add interactive summary table
st.markdown("#### 📈 Intensity Summary Table")
summary_df = pd.DataFrame({
    "Emotion State": ["Confused", "InControl", "Neutral"],
    "Intensity": [i_confused, i_incontrol, i_neutral],
    "Percentage": [f"{(i_confused/1.2)*100:.1f}%", 
                   f"{(i_incontrol/1.2)*100:.1f}%", 
                   f"{(i_neutral/1.2)*100:.1f}%"]
})
​
st.dataframe(summary_df, width='stretch', hide_index=True)