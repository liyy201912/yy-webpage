import sys

sys.path.insert(0, "/Users/yli16/projects/.pip_pkgs")

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


DARK_BLUE = RGBColor(0x1A, 0x36, 0x5D)
ACCENT_BLUE = RGBColor(0x2B, 0x6C, 0xB0)
ACCENT_GREEN = RGBColor(0x2F, 0x85, 0x59)
ACCENT_PURPLE = RGBColor(0x73, 0x4A, 0xB8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SOFT_BG = RGBColor(0xF4, 0xF7, 0xFB)
CARD_BG = RGBColor(0xFA, 0xFB, 0xFD)
BORDER = RGBColor(0xE2, 0xE8, 0xF0)
LIGHT_GRAY = RGBColor(0x6B, 0x72, 0x80)
NEAR_BLACK = RGBColor(0x1F, 0x29, 0x37)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H


def add_solid_bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_textbox(slide, left, top, width, height):
    return slide.shapes.add_textbox(left, top, width, height)


def set_font(run, size=18, bold=False, color=NEAR_BLACK, name="Helvetica Neue"):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = name


def add_paragraph(tf, text, size=18, bold=False, color=NEAR_BLACK, align=PP_ALIGN.LEFT, space_after=Pt(6)):
    p = tf.add_paragraph()
    p.alignment = align
    p.space_after = space_after
    r = p.add_run()
    r.text = text
    set_font(r, size=size, bold=bold, color=color)
    return p


def add_title(slide, title, subtitle=None, accent=ACCENT_BLUE):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.56), Inches(0.08), Inches(0.5))
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent
    bar.line.fill.background()

    tb = add_textbox(slide, Inches(1.08), Inches(0.42), Inches(11.2), Inches(0.7))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = title
    set_font(r, size=30, bold=True, color=DARK_BLUE)

    if subtitle:
        add_paragraph(tf, subtitle, size=14, color=LIGHT_GRAY, space_after=Pt(0))


def add_card(slide, left, top, width, height, fill_color=CARD_BG, border_color=BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1)
    return shape


def add_metric(slide, left, top, width, height, number, label, accent=ACCENT_BLUE):
    shape = add_card(slide, left, top, width, height, fill_color=SOFT_BG, border_color=SOFT_BG)
    tf = shape.text_frame
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].space_before = Pt(8)
    r = tf.paragraphs[0].add_run()
    r.text = number
    set_font(r, size=24, bold=True, color=accent)

    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run()
    r2.text = label
    set_font(r2, size=11, color=LIGHT_GRAY)


def add_list_panel(slide, left, top, width, height, title, items, accent=ACCENT_BLUE):
    add_card(slide, left, top, width, height)
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(0.06), height)
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent
    bar.line.fill.background()

    tb = add_textbox(slide, left + Inches(0.22), top + Inches(0.16), width - Inches(0.32), height - Inches(0.24))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = title
    set_font(r, size=18, bold=True, color=DARK_BLUE)
    p.space_after = Pt(8)

    for item in items:
        add_paragraph(tf, "• " + item, size=12, color=LIGHT_GRAY, space_after=Pt(5))


def add_direction_card(slide, left, top, width, height, title, summary, reps, accent):
    add_card(slide, left, top, width, height)
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(0.07), height)
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent
    bar.line.fill.background()

    tb = add_textbox(slide, left + Inches(0.25), top + Inches(0.2), width - Inches(0.36), height - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = title
    set_font(r, size=20, bold=True, color=DARK_BLUE)
    p.space_after = Pt(8)
    add_paragraph(tf, summary, size=13, color=LIGHT_GRAY, space_after=Pt(10))
    add_paragraph(tf, "Representative work: " + reps, size=12, bold=True, color=accent, space_after=Pt(0))


def add_work_card(slide, left, top, width, height, title, meta, bullets, accent):
    add_card(slide, left, top, width, height, fill_color=SOFT_BG, border_color=SOFT_BG)
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(0.06), height)
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent
    bar.line.fill.background()

    tb = add_textbox(slide, left + Inches(0.24), top + Inches(0.12), width - Inches(0.36), height - Inches(0.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = title
    set_font(r, size=16, bold=True, color=DARK_BLUE)
    p.space_after = Pt(1)

    add_paragraph(tf, meta, size=11, bold=True, color=accent, space_after=Pt(6))
    for bullet in bullets:
        add_paragraph(tf, "• " + bullet, size=11, color=LIGHT_GRAY, space_after=Pt(3))


# Slide 1: title
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_solid_bg(slide, DARK_BLUE)

tb = add_textbox(slide, Inches(1.4), Inches(1.8), Inches(10.6), Inches(1.3))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
r = p.add_run()
r.text = "Yanyu Li"
set_font(r, size=50, bold=True, color=WHITE)
add_paragraph(tf, "Ph.D., Northeastern University", size=23, color=RGBColor(0xC8, 0xD8, 0xEE), align=PP_ALIGN.CENTER, space_after=Pt(16))
add_paragraph(
    tf,
    "Efficient AI  |  Vision Transformers  |  Diffusion Models  |  Mobile and Edge Deployment",
    size=17,
    color=RGBColor(0xA6, 0xBB, 0xD6),
    align=PP_ALIGN.CENTER,
    space_after=Pt(14),
)
add_paragraph(tf, "59 publications  |  2,963 citations  |  h-index 23", size=15, color=RGBColor(0x92, 0xAB, 0xC9), align=PP_ALIGN.CENTER, space_after=Pt(0))

tb2 = add_textbox(slide, Inches(1.8), Inches(5.7), Inches(9.8), Inches(0.55))
tf2 = tb2.text_frame
p = tf2.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
r = p.add_run()
r.text = "li.yanyu@northeastern.edu   |   scholar.google.com/citations?user=XUj8koUAAAAJ   |   github.com/liyy201912"
set_font(r, size=13, color=RGBColor(0xA6, 0xBB, 0xD6))


# Slide 2: about me
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_solid_bg(slide, WHITE)
add_title(slide, "About Me", "Bio, background, and current research focus.")

tb = add_textbox(slide, Inches(1.0), Inches(1.35), Inches(7.2), Inches(2.15))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
r = p.add_run()
r.text = (
    "I am a researcher in efficient AI, working at the intersection of vision transformers, "
    "diffusion models, model compression, and hardware-aware deployment. My goal is to bring "
    "state-of-the-art machine learning systems to mobile and edge platforms without sacrificing "
    "accuracy, quality, or practicality."
)
set_font(r, size=17, color=NEAR_BLACK)
p.space_after = Pt(10)
add_paragraph(
    tf,
    "My work includes 59 publications, 2,963 citations, h-index 23, and 7 patents / patent applications, "
    "with papers at NeurIPS, CVPR, ICCV, ICLR, AAAI, IJCAI, ECCV, HPCA, FPGA, and FPL.",
    size=14,
    color=LIGHT_GRAY,
    space_after=Pt(8),
)
add_paragraph(
    tf,
    "Current interests: efficient vision backbones, mobile text-to-image and video generation, quantization, "
    "sparse training, neural architecture search, and algorithm-hardware co-design.",
    size=14,
    color=LIGHT_GRAY,
    space_after=Pt(0),
)

metrics = [("2,963", "Citations"), ("23", "h-index"), ("59", "Publications"), ("7", "Patents")]
for idx, (number, label) in enumerate(metrics):
    x = Inches(8.7) + (idx % 2) * Inches(1.9)
    y = Inches(1.45) + (idx // 2) * Inches(1.2)
    add_metric(slide, x, y, Inches(1.7), Inches(1.0), number, label)

add_list_panel(
    slide,
    Inches(1.0),
    Inches(3.9),
    Inches(5.6),
    Inches(2.1),
    "Education",
    [
        "Ph.D. in Computer Engineering, Northeastern University (2019-2024); Advisor: Prof. Yanzhi Wang",
        "M.S. in Mechanical Engineering (Robotics), Boston University (2017-2019)",
        "B.E. in Mechanical Engineering, Tsinghua University (2011-2015)",
    ],
)
add_list_panel(
    slide,
    Inches(6.9),
    Inches(3.9),
    Inches(5.45),
    Inches(2.1),
    "Experience Highlights",
    [
        "Snap Inc.: efficient diffusion models, mobile generative AI, and quality-aware text encoders",
        "CoCoPIE LLC: algorithm-hardware co-design for compressed and quantized networks",
        "Kuaishou Technology: GAN compression and dynamic pruning",
    ],
    accent=ACCENT_GREEN,
)


# Slide 3: summary of research directions
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_solid_bg(slide, WHITE)
add_title(slide, "Summary of Research Directions", "Three main directions organize the research portfolio.")

add_direction_card(
    slide,
    Inches(1.0),
    Inches(1.55),
    Inches(3.75),
    Inches(4.7),
    "Efficient Vision Transformers",
    "Lightweight transformer backbones for recognition and dense prediction under mobile latency and memory constraints.",
    "EfficientFormer, EfficientFormerV2, Pruning-as-Search",
    ACCENT_BLUE,
)
add_direction_card(
    slide,
    Inches(4.95),
    Inches(1.55),
    Inches(3.75),
    Inches(4.7),
    "Diffusion Models and Generative AI",
    "Fast and practical text-to-image and video generation with improvements in quality control, acceleration, and compression.",
    "SnapFusion, TextCraftor, BitsFusion",
    ACCENT_GREEN,
)
add_direction_card(
    slide,
    Inches(8.9),
    Inches(1.55),
    Inches(3.45),
    Inches(4.7),
    "Compression and Hardware-Aware Optimization",
    "Quantization, sparse training, FPGA acceleration, and deployment-oriented model design.",
    "Mix and Match, FILM-QNN, Auto-ViT-Acc",
    ACCENT_PURPLE,
)


# Slide 4: direction 1
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_solid_bg(slide, WHITE)
add_title(
    slide,
    "Direction 1: Efficient Vision Transformers",
    "Most cited and representative work on mobile-speed visual architectures.",
    accent=ACCENT_BLUE,
)

add_work_card(
    slide,
    Inches(1.0),
    Inches(1.45),
    Inches(11.35),
    Inches(1.42),
    "EfficientFormer: Vision Transformers at MobileNet Speed",
    "NeurIPS 2022  |  764 citations",
    [
        "Proposed a dimension-consistent meta-block design that removes mobile-unfriendly transformer components while preserving strong accuracy.",
        "Showed that vision transformers can operate at MobileNet-class speed on real mobile devices, making transformer deployment practical.",
    ],
    ACCENT_BLUE,
)
add_work_card(
    slide,
    Inches(1.0),
    Inches(3.05),
    Inches(11.35),
    Inches(1.42),
    "Rethinking Vision Transformers for MobileNet Size and Speed",
    "ICCV 2023  |  428 citations",
    [
        "Refined the mobile transformer design space with better architecture choices for latency, model size, and accuracy.",
        "Strengthened the case for transformer backbones in real-time mobile vision by improving the efficiency-accuracy trade-off.",
    ],
    ACCENT_BLUE,
)
add_work_card(
    slide,
    Inches(1.0),
    Inches(4.65),
    Inches(11.35),
    Inches(1.42),
    "Pruning-as-Search: Efficient Neural Architecture Search via Channel Pruning and Structural Reparameterization",
    "IJCAI 2022  |  78 citations",
    [
        "Reformulated efficient architecture search using channel pruning and structural reparameterization instead of expensive search loops.",
        "Connected efficient model design with deployment-oriented architectures and reduced the cost of searching for compact models.",
    ],
    ACCENT_BLUE,
)
tb = add_textbox(slide, Inches(1.0), Inches(6.25), Inches(11.2), Inches(0.5))
tf = tb.text_frame
p = tf.paragraphs[0]
r = p.add_run()
r.text = "Related work: Towards Real-Time Segmentation on the Edge (AAAI 2023) extends efficient design ideas to dense prediction on edge devices."
set_font(r, size=11, color=LIGHT_GRAY)


# Slide 5: direction 2
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_solid_bg(slide, WHITE)
add_title(
    slide,
    "Direction 2: Diffusion Models and Generative AI",
    "Recent and highly visible work on efficient generative modeling for mobile and edge deployment.",
    accent=ACCENT_GREEN,
)

add_work_card(
    slide,
    Inches(1.0),
    Inches(1.45),
    Inches(11.35),
    Inches(1.42),
    "SnapFusion: Text-to-Image Diffusion Model on Mobile Devices within Two Seconds",
    "NeurIPS 2023  |  305 citations",
    [
        "Redesigned the text-to-image diffusion pipeline for on-device generation through efficient architecture and faster inference.",
        "Demonstrated that high-quality text-to-image diffusion can run in under two seconds on mobile hardware.",
    ],
    ACCENT_GREEN,
)
add_work_card(
    slide,
    Inches(1.0),
    Inches(3.05),
    Inches(11.35),
    Inches(1.42),
    "TextCraftor: Your Text Encoder Can Be Image Quality Controller",
    "CVPR 2024  |  32 citations",
    [
        "Showed that the text encoder can act as an explicit control knob for image quality and text-image alignment.",
        "Improved generation quality without relying only on larger backbones or slower sampling procedures.",
    ],
    ACCENT_GREEN,
)
add_work_card(
    slide,
    Inches(1.0),
    Inches(4.65),
    Inches(11.35),
    Inches(1.42),
    "BitsFusion: 1.99 Bits Weight Quantization of Diffusion Model",
    "NeurIPS 2024  |  43 citations",
    [
        "Introduced ultra-low-bit weight quantization for diffusion models at 1.99 bits with compression-aware optimization.",
        "Pushed diffusion efficiency to an aggressive low-precision regime while maintaining useful generation quality.",
    ],
    ACCENT_GREEN,
)
tb = add_textbox(slide, Inches(1.0), Inches(6.25), Inches(11.2), Inches(0.5))
tf = tb.text_frame
p = tf.paragraphs[0]
r = p.add_run()
r.text = "Other recent work: LazyDiT (AAAI 2025), SF-V (NeurIPS 2024), SnapGen / SnapGen-V (CVPR 2025), and Improving the Diffusability of Autoencoders (2025)."
set_font(r, size=11, color=LIGHT_GRAY)


# Slide 6: direction 3
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_solid_bg(slide, WHITE)
add_title(
    slide,
    "Direction 3: Compression and Hardware-Aware Optimization",
    "Most cited systems work on quantization, sparse training, and FPGA-aware acceleration.",
    accent=ACCENT_PURPLE,
)

add_work_card(
    slide,
    Inches(1.0),
    Inches(1.45),
    Inches(11.35),
    Inches(1.42),
    "Mix and Match: A Novel FPGA-Centric Deep Neural Network Quantization Framework",
    "HPCA 2021  |  156 citations",
    [
        "Proposed an FPGA-centric quantization framework that mixes quantization schemes and precisions within a network.",
        "Aligned model compression with actual accelerator behavior instead of optimizing only abstract algorithmic metrics.",
    ],
    ACCENT_PURPLE,
)
add_work_card(
    slide,
    Inches(1.0),
    Inches(3.05),
    Inches(11.35),
    Inches(1.42),
    "FILM-QNN: Efficient FPGA Acceleration of Deep Neural Networks with Intra-Layer, Mixed-Precision Quantization",
    "FPGA 2022  |  128 citations",
    [
        "Developed intra-layer mixed-precision quantization for efficient FPGA deployment of deep neural networks.",
        "Improved hardware utilization and showed strong accuracy-efficiency trade-offs on real accelerator targets.",
    ],
    ACCENT_PURPLE,
)
add_work_card(
    slide,
    Inches(1.0),
    Inches(4.65),
    Inches(11.35),
    Inches(1.42),
    "Auto-ViT-Acc: An FPGA-Aware Automatic Acceleration Framework for Vision Transformer with Mixed-Scheme Quantization",
    "FPL 2022  |  104 citations",
    [
        "Built an FPGA-aware acceleration framework for vision transformers using mixed-scheme quantization and automatic mapping.",
        "Extended hardware-aware optimization from CNNs to transformer inference and practical deployment.",
    ],
    ACCENT_PURPLE,
)
tb = add_textbox(slide, Inches(1.0), Inches(6.25), Inches(11.2), Inches(0.5))
tf = tb.text_frame
p = tf.paragraphs[0]
r = p.add_run()
r.text = "Other related work: Layer Freezing and Data Sieving (NeurIPS 2022), NPAS (CVPR 2021), RMSMP (ICCV 2021), and SDA (FPL 2024)."
set_font(r, size=11, color=LIGHT_GRAY)


# Slide 7: closing
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_solid_bg(slide, DARK_BLUE)

tb = add_textbox(slide, Inches(1.5), Inches(2.15), Inches(10.2), Inches(0.95))
tf = tb.text_frame
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
r = p.add_run()
r.text = "Thank You"
set_font(r, size=46, bold=True, color=WHITE)
add_paragraph(tf, "Open to research collaborations and discussions on efficient AI, generative modeling, and mobile deployment.", size=18, color=RGBColor(0xB7, 0xCB, 0xE3), align=PP_ALIGN.CENTER, space_after=Pt(24))
add_paragraph(tf, "li.yanyu@northeastern.edu", size=17, color=RGBColor(0xB7, 0xCB, 0xE3), align=PP_ALIGN.CENTER, space_after=Pt(10))
add_paragraph(tf, "Google Scholar: scholar.google.com/citations?user=XUj8koUAAAAJ", size=17, color=RGBColor(0xB7, 0xCB, 0xE3), align=PP_ALIGN.CENTER, space_after=Pt(10))
add_paragraph(tf, "GitHub: github.com/liyy201912", size=17, color=RGBColor(0xB7, 0xCB, 0xE3), align=PP_ALIGN.CENTER, space_after=Pt(0))


out_path = "/Users/yli16/projects/yy-webpage/presentation.pptx"
prs.save(out_path)
print(f"Saved to {out_path}")
