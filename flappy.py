import streamlit as st
import time
import random
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Flappy Stream", layout="wide")

# Constants
GRAVITY = 0.5
JUMP_STRENGTH = -7
PIPE_WIDTH = 60
PIPE_GAP = 150
PIPE_SPEED = 3

# Session state setup
def init_game():
    st.session_state.bird_y = 250
    st.session_state.velocity = 0
    st.session_state.pipes = []
    st.session_state.score = 0
    st.session_state.high_score = st.session_state.get("high_score", 0)
    st.session_state.running = False
    st.session_state.last_update = time.time()

# Initialize game
if "bird_y" not in st.session_state:
    init_game()

# Input (spacebar detection via JS)
space_pressed = streamlit_js_eval(js_expressions="keyPressed === 32", key="space_event")
if space_pressed and not st.session_state.running:
    st.session_state.running = True
    st.session_state.pipes = []
    st.session_state.velocity = JUMP_STRENGTH
    st.session_state.last_update = time.time()

elif space_pressed and st.session_state.running:
    st.session_state.velocity = JUMP_STRENGTH

# Game loop logic
if st.session_state.running:
    now = time.time()
    dt = now - st.session_state.last_update
    st.session_state.last_update = now

    # Bird physics
    st.session_state.velocity += GRAVITY
    st.session_state.bird_y += st.session_state.velocity

    # Generate pipes
    if len(st.session_state.pipes) == 0 or st.session_state.pipes[-1][0] < 400:
        new_top = random.randint(100, 300)
        st.session_state.pipes.append([600, new_top])

    # Move pipes
    new_pipes = []
    for x, top in st.session_state.pipes:
        x -= PIPE_SPEED
        if x + PIPE_WIDTH > 0:
            new_pipes.append([x, top])
    st.session_state.pipes = new_pipes

    # Collision and scoring
    bird_x = 150
    bird_radius = 20
    passed = False

    for pipe_x, pipe_top in st.session_state.pipes:
        if pipe_x < bird_x < pipe_x + PIPE_WIDTH:
            if not (pipe_top < st.session_state.bird_y < pipe_top + PIPE_GAP):
                st.session_state.running = False
        if pipe_x + PIPE_WIDTH < bird_x and not passed:
            st.session_state.score += 1
            passed = True

    # Check bounds
    if st.session_state.bird_y < 0 or st.session_state.bird_y > 500:
        st.session_state.running = False

    # Update high score
    st.session_state.high_score = max(st.session_state.high_score, st.session_state.score)

# Drawing the game
st.markdown("""
<style>
.canvas {{
    position: relative;
    width: 600px;
    height: 500px;
    background-color: #add8e6;
    border: 2px solid black;
}}
.bird {{
    position: absolute;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: yellow;
    left: 150px;
    top: {bird_y}px;
    z-index: 10;
}}
.pipe {{
    position: absolute;
    width: 60px;
    background: green;
}}
</style>
<div class="canvas">
<div class="bird" style="top: {bird_y}px"></div>
{pipes}
</div>
""".format(
    bird_y=st.session_state.bird_y,
    pipes="\n".join(
        f'<div class="pipe" style="left: {x}px; top: 0; height: {top}px"></div>' +
        f'<div class="pipe" style="left: {x}px; top: {top + PIPE_GAP}px; height: {500 - top - PIPE_GAP}px"></div>'
        for x, top in st.session_state.pipes
    )
), unsafe_allow_html=True)

# Display score
st.title("Flappy Stream 🐦")
st.subheader(f"Score: {st.session_state.score}")
st.subheader(f"High Score: {st.session_state.high_score}")

# Game Over handling
if not st.session_state.running and st.session_state.bird_y != 250:
    st.info("Game Over. Press spacebar to restart.")
    if space_pressed:
        init_game()

# Refresh the app to simulate animation
if st.session_state.running:
    time.sleep(0.03)
    st.experimental_rerun()
ß
