# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
import numpy as np

# Parameters for the GIF
frames = 30
size = (16, 16)
palm_color = (34, 139, 34)
trunk_color = (139, 69, 19)
sky_color = (135, 206, 250)
sun_color = (255, 223, 0)

# Update parameters for the scene
sand_color = (255, 223, 186)
water_color = (64, 164, 223)
sunrise_colors = [(255, 69, 0), (135, 206, 250)]  # From red to blue for the sky gradient

# Function to blend colors for sunrise effect
def blend_colors(color1, color2, t):
    return tuple(int(color1[i] * (1 - t) + color2[i] * t) for i in range(3))

# Function to draw the palm tree with curvature
def draw_curved_palm(draw, frame):
    # Trunk (curved based on bezier control points)
    sway = int(1 * np.sin(frame / frames * 2 * np.pi))  # Slight swaying effect
    trunk_points = [
        (8, 15),
        (7 + sway, 12),
        (8, 8),
    ]

    draw.line(trunk_points, fill=trunk_color, width=1)
    # Leaves (adjusted for new trunk position)
    sway = int(2 * np.sin(frame / frames * 2 * np.pi))
    leaf_positions = [
        [(8, 8), (5, 6 + sway)],
        [(8, 8), (11, 6 - sway)],
        [(8, 8), (6, 7 - sway)],
        [(8, 8), (10, 7 + sway)],
    ]
    for leaf in leaf_positions:
        draw.line(leaf, fill=palm_color, width=1)


# Function to add the second palm tree
def draw_additional_palm(draw, frame):
    # Second palm tree (smaller and slightly higher)
    sway = int(1.5 * np.sin(frame / frames * 2 * np.pi))  # Sway effect
    trunk_points = [
        (12, 13),
        (11 + sway, 10),
        (12, 7),
    ]
    draw.line(trunk_points, fill=trunk_color, width=1)

    # Leaves for second palm
    leaf_positions = [
        [(12, 7), (10, 6 + sway)],
        [(12, 7), (14, 6 - sway)],
        [(12, 7), (11, 5 - sway)],
        [(12, 7), (13, 5 + sway)],
    ]
    for leaf in leaf_positions:
        draw.line(leaf, fill=palm_color, width=1)

def main():

    # Generate frames with sun properly behind water/sand and additional palm
    gif_frames = []
    for frame in range(frames):
        # Calculate sky gradient
        t = frame / frames
        sky_color = blend_colors(sunrise_colors[0], sunrise_colors[1], t)

        # Create image and draw base layers
        img = Image.new("RGB", size, sky_color)
        draw = ImageDraw.Draw(img)

        # Draw sun (behind water and sand)
        sun_y = 15 - (frame / frames * 15)
        draw.ellipse([4, sun_y, 12, sun_y + 8], fill=sun_color)

        # Draw water
        draw.rectangle([0, 10, 15, 15], fill=water_color)

        # Draw sand
        draw.rectangle([0, 12, 15, 15], fill=sand_color)

        # Draw first palm tree
        draw_curved_palm(draw, frame)

        # Draw second palm tree
        draw_additional_palm(draw, frame)

        gif_frames.append(img)

    # Erstellen einer globalen Palette (wichtig für einheitliche Farben)
    #palette_image = gif_frames[0].convert("P", palette=Image.ADAPTIVE, colors=256)

    # Frames konvertieren ohne Dithering
    gif_frames_no_dither = [
        frame.convert("P", palette=Image.ADAPTIVE, colors=256, dither=Image.NONE)
        for frame in gif_frames
    ]
    # Palette für konsistente Farben erstellen
    #palette_image = gif_frames[0].convert("P", palette=Image.ADAPTIVE, colors=256)
    #gif_frames = [frame.convert("RGB").quantize(palette=palette_image) for frame in gif_frames]

    # Save the updated GIF
    output_path_final_with_palm = "./palm_tree_sunrise_horizon_with_extra_palm.gif"
    gif_frames[0].save(
        output_path_final_with_palm,
        save_all=True,
        append_images=gif_frames_no_dither[1:],
        optimize=False,
        duration=100,  # 100ms per frame
        loop=0
    )

    output_path_final_with_palm

if __name__ == "__main__":
    main()
