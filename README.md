Space-Shooter-Mission
Hey, this is my custom retro arcade shooter created for Hack Club! I wanted to try building an action-packed space game entirely in Python using Pygame and asyncio, without relying on any external image assets or pre-made sprite sheets.

Live Demo & Preview
Live Site: https://vansh-creator-ctrl.itch.io/mini-space-shooting-game Screenshot:<img width="447" height="444" alt="Capture code" src="https://github.com/user-attachments/assets/30ef0017-b730-47d5-b010-f9dbd7d79b9b" />


What I Built

Procedural Asset Generation: Built all game visuals (the player ship, alien variants, asteroids, and power-ups) directly in code using Pygame's drawing functions and custom surface blending.

Parallax Space Backgrounds: Created dynamic, multi-layered starfields that move at different speeds, alongside animated nebulas, planets, and rare passing comets.

Power-Up System: Added collectible boosters for Rapid Fire, Energy Shields, Multi-shot lasers, and extra lives to make gameplay more dynamic.

Visual Juice & Effects: Built custom explosion particle engines, engine thruster trails, screen shake on impact, hit flashes, and glowing UI text.

Web Compatibility: Used asyncio loops so the entire Pygame script can be compiled with Pygbag and played directly in the browser.

What I Learned
Building this helped me get a lot better at handling game loops, frame timing, and math-driven drawing logic in Python. Figuring out how to handle smooth particle lifetimes and vector movement without lagging the frame rate was definitely the trickiest part, but adding the screen shake and glowing text made it feel super satisfying when it all came together!
