from flask import Flask, render_template, send_from_directory, abort
from urllib.parse import quote
import os

app = Flask(__name__)

ROOT_DIR   = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(ROOT_DIR, 'static')


@app.template_filter('url_encode')
def url_encode_filter(s):
    return quote(str(s), safe='')


PROJECTS = [
    {
        "id": "web-design",
        "name": "Web Design",
        "folder": "Web Design",
        "description": "An AI-based platform that helps users discover interior products that match their space, style, and needs. The project simplifies the decoration process through personalized recommendations, curated product options, and a user-centered digital experience.",
        "accent": "#A78BFA",
        "cover_image": "musebackground.jpg",
        "preview_image": None,
        "images": [],
        "pdfs": ["muse.pdf", "museposter.pdf", "muse magazine ad.pdf"],
        "live_link": "https://muse-website-zms.vercel.app/"
    },
    {
        "id": "conceptual-poster-design",
        "name": "Conceptual Poster Design",
        "folder": "conceptual poster design",
        "description": "A poster design created for Zeynep Yüceler's award recognized short story A Convenient Day. Through a minimal black and white composition, the poster reflects the story's tension between control, timing, and unexpected consequences.",
        "accent": "#86C8A4",
        "preview_image": "a convenient day mockup poster.png",
        "images": ["a convenient day mockup poster.png", "zehraminasarioglangra401ğroject3.jpg"],
        "pdfs": []
    },
    {
        "id": "encyclopaedia-design",
        "name": "Encyclopedia Design",
        "folder": "encyclopaedia design",
        "description": "A comprehensive editorial design project reimagining the encyclopaedia format with modern typography and layout. The work balances information density with visual clarity and elegant structure.",
        "accent": "#E8D060",
        "cover_image": "encyclopedia cover.jpg",
        "preview_image": None,
        "images": [],
        "pdfs": ["encyclopaedia.pdf"]
    },
    {
        "id": "logo-design",
        "name": "Logo Design",
        "folder": "logo design",
        "description": "A typography-driven logo and brand identity project spanning labels, tags, and product mockups. The designs demonstrate versatility and visual cohesion across print and merchandise applications.",
        "accent": "#C39BD3",
        "preview_image": "Label Tag PSD MockUp.png",
        "images": ["Label Tag PSD MockUp.png"],
        "pdfs": ["Metal Mug Mockup.pdf", "TYPOGRAPHYFİNALPROJECT.pdf"]
    },
    {
        "id": "magazine-design",
        "name": "Magazine Design",
        "folder": "magazine design",
        "description": "A full magazine layout design featuring dynamic spreads and cohesive visual storytelling. The project showcases mastery of editorial grid systems, typographic rhythm, and page composition.",
        "accent": "#F0A830",
        "preview_image": "magazinemockup_compressed_page-0001.jpg",
        "images": ["magazinemockup_compressed_page-0001.jpg"],
        "pdfs": ["readerspread copy.pdf"]
    },
    {
        "id": "pawtions",
        "name": "Pawtions — Brand Identity",
        "folder": "pawtions jpg",
        "description": "A complete branding project for a pet-care brand covering posters, flyers, business cards, and merchandise. The playful yet professional identity system showcases end-to-end brand design.",
        "accent": "#FF9A7A",
        "preview_image": "pawtionsposter-1.jpg",
        "images": [
            "pawtionsposter-1.jpg",
            "poster pawtions-1.jpg",
            "flyer pawtions-1.jpg",
            "busssinesscardpaw.jpg",
            "anahtarlık pawtions -1.jpg",
            "Screenshot 2025-01-25 at 14.12.03.png"
        ],
        "pdfs": ["branding pawtions.pdf", "pawtions cover.pdf"]
    },
    {
        "id": "social-media-post-design",
        "name": "Social Media Post Design",
        "folder": "social media post design",
        "description": "A series of social media posts designed for real brands including Erasta and FitNFood. Each design adapts the brand's identity into engaging digital content for Instagram and beyond.",
        "accent": "#7EC8E3",
        "preview_image": "erasta 10 ağustos post.jpg",
        "images": [
            "erasta 10 ağustos post.jpg",
            "erasta ağustos pazartesi post.jpg",
            "erasta sinema.png",
            "erasta.png",
            "fitnfoodpostson1jpg.jpg"
        ],
        "pdfs": ["fitnfoodinstapost.pdf"]
    },
    {
        "id": "theatre-poster-design",
        "name": "Theatre Poster Design",
        "folder": "theatre poster design",
        "description": "A dramatic theatre poster that captures the essence of performance through powerful visual composition. The design balances classical theatre aesthetics with a bold, modern graphic sensibility.",
        "accent": "#E8A598",
        "cover_image": "theatre poster cover.jpg",
        "preview_image": None,
        "images": [],
        "pdfs": ["theatre poster design.pdf"]
    },
    {
        "id": "airbnb-promo-video",
        "name": "Airbnb Promo Video",
        "folder": "airbnb promo video",
        "description": "A motion graphics promotional video crafted for Airbnb, blending brand visuals with dynamic storytelling. The piece communicates the warmth and accessibility of the Airbnb experience through fluid animation.",
        "accent": "#FF6B6B",
        "cover_image": "airbnbcover.jpg",
        "preview_image": None,
        "images": [],
        "pdfs": [],
        "is_video": True,
        "drive_link": "https://drive.google.com/drive/folders/1NM0oyeWudqHJ8fV4UHKJ1eiHjHbb0PwF?usp=sharing"
    },
    {
        "id": "entropy-video-design",
        "name": "Entropy — Video Design",
        "folder": "entropy video design",
        "description": "A conceptual motion design piece that explores the visual language of entropy and disorder through typographic animation. The project transforms abstract forces into a compelling, rhythm-driven visual sequence.",
        "accent": "#AAAAAA",
        "cover_image": None,
        "preview_image": "Screenshot 2026-02-24 at 16.12.02.png",
        "images": [],
        "pdfs": [],
        "is_video": True,
        "drive_link": "https://drive.google.com/drive/folders/1Tea8C8VvsMsmNOwNrQNkMbAJ3-FEaZDZ?usp=sharing"
    },
    {
        "id": "kinetic-typography",
        "name": "Kinetic Typography Motion Design",
        "folder": "kinetic typography motion design  project",
        "description": "A kinetic typography project that brings words to life through expressive movement, rhythm, and playful visual storytelling. Type and motion are choreographed together to create an engaging animated experience.",
        "accent": "#E8D44D",
        "cover_image": "kinetic_typography_cover.png",
        "preview_image": None,
        "images": [],
        "pdfs": [],
        "is_video": True,
        "drive_link": "https://drive.google.com/drive/folders/1-ozzqtS9MqzXUGfG-ywfOvhsWTe9p_3E?usp=sharing"
    },
    {
        "id": "poster-design",
        "name": "Poster Design",
        "folder": "Poster Design",
        "description": "A bold poster series exploring the interplay of typography and visual composition. Each piece communicates a distinct message through striking layout and thoughtful use of space.",
        "accent": "#E8907A",
        "cover_image": "poster design cover.png",
        "preview_image": None,
        "images": [],
        "pdfs": ["pposterdesignforportfolio.pdf", "visualt.posterfinal.pdf"]
    },
    {
        "id": "product-package-redesign",
        "name": "Product Package Redesign",
        "folder": "Product Package Compositional Redesign",
        "description": "A typographic packaging redesign that brings a fresh visual identity to product presentation. The project reimagines packaging through expressive letterforms and bold compositional structure.",
        "accent": "#5ECFCF",
        "preview_image": "tipoambalajzehramina-01.jpg",
        "images": ["tipoambalajzehramina-01.jpg", "tipoambalajzehramina-02.jpg"],
        "pdfs": []
    },
    {
        "id": "catalog-design",
        "name": "Catalog Design",
        "folder": "catalog design",
        "description": "A clean and structured catalog layout designed for effective product communication. The design balances visual hierarchy with readable typography across multiple editorial spreads.",
        "accent": "#6EB4E8",
        "cover_image": "catalog design cover.png",
        "preview_image": None,
        "images": [],
        "pdfs": ["catalog design.pdf"]
    }
]


@app.route('/')
def index():
    return render_template('index.html', projects=PROJECTS)


@app.route('/picture')
def serve_picture():
    return send_from_directory(STATIC_DIR, 'backgroundsuzfoto.png')


@app.route('/cover/<path:filename>')
def serve_cover(filename):
    return send_from_directory(os.path.join(STATIC_DIR, 'covers'), filename)


@app.route('/file/<project_id>/<path:filename>')
def serve_file(project_id, filename):
    if not any(p['id'] == project_id for p in PROJECTS):
        abort(404)
    return send_from_directory(
        os.path.join(STATIC_DIR, 'projects', project_id), filename
    )


if __name__ == '__main__':
    app.run(debug=True, port=8000)
