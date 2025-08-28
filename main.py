import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(choice_text, analysis_text):
    doc = SimpleDocTemplate("player_decision_report.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("Psychological Decision Report", styles['Title']))
    story.append(Spacer(1, 20))

    # Player choice
    story.append(Paragraph(f"Player's Decision: {choice_text}", styles['Heading2']))
    story.append(Spacer(1, 12))

    # Psychological analysis
    story.append(Paragraph("Psychological Analysis:", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(analysis_text, styles['Normal']))

    doc.build(story)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <choice>")
        sys.exit(1)

    val = sys.argv[1]

    if val == "1":
        choice_text = "Uphold the Law"
        analysis_text = (
            "The player chose to uphold the law, prioritizing societal order and rules over "
            "individual compassion. This indicates a strong alignment with justice, discipline, "
            "and moral responsibility. It reflects a tendency toward rule-based ethical reasoning."
        )
    elif val == "2":
        choice_text = "Show Compassion"
        analysis_text = (
            "The player chose compassion, prioritizing human empathy and situational context over "
            "strict rules. This suggests emotional sensitivity, altruism, and an ability to connect "
            "deeply with others’ suffering. It reflects a more flexible, empathetic ethical reasoning."
        )
    else:
        choice_text = "Invalid Choice"
        analysis_text = "No valid analysis available because the choice was invalid."

    generate_report(choice_text, analysis_text)

    print("PDF generated: player_decision_report.pdf")
