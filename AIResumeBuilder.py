import streamlit as st
from fpdf import FPDF
import google.generativeai as genai


st.set_page_config(page_title="AI Resume & Portfolio Builder", layout="centered")


genai.configure(api_key="YOUR GOOGLE API KEY HERE")
model = genai.GenerativeModel('gemini-2.5-flash')


st.title("🎓 AI Resume & Portfolio Builder")
st.header("📀 Choose Your Resume Style")
res_type = st.radio(
    "Select the tone and look of your resume:",
    ["Classic", "Professional", "Simple"],
    horizontal=True,
    help="Classic: Traditional & Formal | Professional: Modern & Bold | Simple: Clean & Minimalist"
)


if res_type == "Classic":
    primary_color = "#000000"
    font_family = "serif"
elif res_type == "Professional":
    primary_color = "#1E3A8A"
    font_family = "sans-serif"
else:
    primary_color = "#475569"
    font_family = "monospace"


st.markdown(f"""
    <style>
    .stTextInput input, .stTextArea textarea {{
        border: 2px solid {primary_color} !important;
        border-radius: 5px !important;
    }}
    div.stButton > button {{
        background-color: {primary_color} !important;
        color: white !important;
        width: 100%;
        font-weight: bold;
        height: 3em;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background-color: #fff5f7;
        padding: 15px;
        border-radius: 11px;
        justify-content: center
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: #ffffff; 
        border: 2px solid #d1d5db;
        border-radius: 5px;
        font-weight: bold;
        padding: 15px;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {primary_color} !important;
        color: white !important;
    }}
    .resume-paper {{
        background-color: white;
        padding: 50px;
        border: 1px solid #d1d5db;
        color: black;
        font-family: {font_family};
        line-height: 1.5;
        margin-top: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}
    .res-header {{ text-align: center; margin-bottom: 20px; }}
    .res-name {{ font-size: 28px; font-weight: bold; color: {primary_color}; margin: 0; }}
    .res-contact {{ font-size: 12px; color: #4b5563; margin-top: 5px; }}
    .res-section-title {{ 
        font-weight: bold; 
        font-size: 14px; 
        text-transform: uppercase; 
        border-bottom: 2px solid {primary_color}; 
        margin-top: 15px;
        margin-bottom: 5px;
    }}
    .res-content {{ font-size: 13px; text-align: justify; }}
    </style>
    """, unsafe_allow_html=True)



def create_pdf(name, job, contact_line, summary, edu_text, ai_content, internship_text, r_style):
    pdf = FPDF()
    pdf.add_page()

    # Map style to PDF Fonts
    f_map = {"Classic": "Times", "Professional": "Arial", "Simple": "Courier"}
    font = f_map[r_style]

    pdf.set_font(font, 'B', 22)
    pdf.set_text_color(30, 58, 138) if r_style == "Professional" else pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 12, name.upper(), ln=True, align='C')

    pdf.set_font(font, size=9)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 6, contact_line, ln=True, align='C')

    pdf.set_font(font, 'I', 11)
    pdf.cell(0, 6, job, ln=True, align='C')
    pdf.ln(4)

    def add_section(title, content):
        pdf.set_font(font, 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, title, ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)
        pdf.set_font(font, size=10)
        clean_text = content.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 6, txt=clean_text)
        pdf.ln(4)

    add_section("PROFESSIONAL SUMMARY", summary)
    add_section("EDUCATION", edu_text)
    if internship_text.strip(): add_section("EXPERIENCE", internship_text)
    add_section("PROJECTS & TECHNICAL SKILLS", ai_content)

    return pdf.output(dest='S')



if 'proj_count' not in st.session_state: st.session_state.proj_count = 1
if 'edu_count' not in st.session_state: st.session_state.edu_count = 1


def inc_proj(): st.session_state.proj_count += 1


def inc_edu(): st.session_state.edu_count += 1



st.header("🎯 Target the Role")
jd_text = st.text_area("Paste Job Description (JD) here", height=100,
                       placeholder="Paste the job requirements here to help the AI tailor your resume...")
target_job = st.text_input("Target Job Title", placeholder="e.g. Frontend Developer")

st.divider()

tab1, tab2, tab3 = st.tabs(["👤 Personal & Education", "💻 Projects", "💼 Internship"])

with tab1:
    st.subheader("Personal Details")
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Full Name", placeholder="Rakesh Sharma")
        email = st.text_input("Email ID", placeholder="RakeshS@example.com")
        github = st.text_input("GitHub Link", placeholder="github.com/RakeshSharma")
    with c2:
        phone = st.text_input("Phone Number", placeholder="+91 12345 67890")
        linkedin = st.text_input("LinkedIn Link", placeholder="linkedin.com/in/RakeshSharma")

    st.divider()
    st.subheader("Education Qualification")
    edu_entries = []
    for j in range(st.session_state.edu_count):
        st.markdown(f"**Education #{j + 1}**")
        ec1, ec2 = st.columns(2)
        with ec1:
            deg = st.text_input(f"Degree/Course", key=f"deg_{j}", placeholder="B.E. Computer Science")
            yr = st.text_input(f"Year of Passing", key=f"yr_{j}", placeholder="2026")
        with ec2:
            inst = st.text_input(f"Institution/University", key=f"inst_{j}", placeholder="University Name")
            scr = st.text_input(f"Score (CGPA/%)", key=f"scr_{j}", placeholder="9.0 CGPA")
        edu_entries.append(f"{deg} | {inst} ({yr}) | Score: {scr}")
    st.button("➕ Add More Education", on_click=inc_edu)
    edu_summary = "\n".join(edu_entries)

with tab2:
    st.subheader("Projects")
    proj_list = []
    for i in range(st.session_state.proj_count):
        st.markdown(f"**Project #{i + 1}**")
        p_n = st.text_input(f"Title", key=f"pn_{i}", placeholder="e.g. AI Resume Builder")
        p_s = st.text_input(f"Stack", key=f"ps_{i}", placeholder="Python, Streamlit, OpenAI")
        p_d = st.text_area(f"Description", key=f"pd_{i}",
                           placeholder="Describe your role and the impact of the project...")
        proj_list.append({"name": p_n, "stack": p_s, "desc": p_d})
    st.button("➕ Add More Projects", on_click=inc_proj)

with tab3:
    st.subheader("Internship")
    has_internship = st.checkbox("Include Internship")
    intern_details = ""
    if has_internship:
        ic1, ic2 = st.columns(2)
        with ic1:
            company = st.text_input("Company", placeholder="Company Name")
            role = st.text_input("Role", placeholder="Internship Role")
        with ic2:
            span = st.text_input("Span", placeholder="June 2025 - Aug 2025")
        work_done = st.text_area("Details of Work", placeholder="List your key contributions and technologies used...")
        intern_details = f"Role: {role} at {company}\nDuration: {span}\nDetails: {work_done}"

st.divider()

if st.button("✨ Generate Professional Resume"):
    if not (name and email and jd_text):
        st.error("Please fill in Name, Email, and JD!")
    else:

        style_prompts = {
            "Classic": "Use formal, sophisticated language and focus on academic rigor.",
            "Professional": "Use powerful action verbs and focus on data-driven achievements.",
            "Simple": "Keep the language direct, clear, and easy to scan."
        }

        with st.spinner(f"🤖 AI is crafting your {res_type} resume..."):
            all_projs = "".join([f"\n- {p['name']} ({p['stack']}): {p['desc']}" for p in proj_list])

            prompt = f"""
            Analyze JD: {jd_text}
            Style Instruction: {style_prompts[res_type]}
            Candidate: {name}
            Education: {edu_summary}
            Internship: {intern_details}
            Projects: {all_projs}
            Task: 1. Generate 3-sentence summary. 2. Rewrite Internship/Projects using STAR method.
            Format: SUMMARY: [Text] INTERN: [Text] PROJECTS: [Text]
            """

            try:
                response = model.generate_content(prompt)
                raw_txt = response.text
                ai_summary = raw_txt.split("SUMMARY:")[1].split("INTERN:")[0].strip() if "SUMMARY:" in raw_txt else ""
                ai_intern = raw_txt.split("INTERN:")[1].split("PROJECTS:")[0].strip() if "INTERN:" in raw_txt else ""
                ai_projects = raw_txt.split("PROJECTS:")[1].strip() if "PROJECTS:" in raw_txt else raw_txt

                contact_line = f"{email} | {phone} | {linkedin} | {github}"
                final_intern_text = f"{role} at {company} ({span})\n{ai_intern}" if has_internship else ""

                st.markdown(f"""
                <div class="resume-paper">
                    <div class="res-header">
                        <p class="res-name">{name.upper()}</p>
                        <p class="res-contact">{contact_line}</p>
                        <p style="margin:2px;"><i>{target_job}</i></p>
                    </div>
                    <div class="res-section-title">Professional Summary</div>
                    <div class="res-content">{ai_summary}</div>
                    <div class="res-section-title">Education</div>
                    <div class="res-content" style="white-space: pre-wrap;">{edu_summary}</div>
                    {"<div class='res-section-title'>Experience</div><div class='res-content' style='white-space: pre-wrap;'>" + final_intern_text + "</div>" if has_internship else ""}
                    <div class="res-section-title">Projects & Technical Skills</div>
                    <div class="res-content" style="white-space: pre-wrap;">{ai_projects}</div>
                </div>
                """, unsafe_allow_html=True)

                pdf_bytes = create_pdf(name, target_job, contact_line, ai_summary, edu_summary, ai_projects,
                                       final_intern_text, res_type)
                st.download_button(f"📥 Download {res_type} PDF", pdf_bytes, f"{name}_Resume.pdf", "application/pdf")
            except Exception as e:
                st.error(f"Error: {e}")