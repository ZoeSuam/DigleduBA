import json
import os
import logging
import random
from flask import session, jsonify, Flask

def get_exam_question():
    # Liste von Prüfungsfragen
    questions = [
        # Kapitel 1: Die Bilanz
        "Was versteht man unter einer Bilanz?",
        "Was sind Aktiva und Passiva?",
        "Wie wird das Eigenkapital in einer Bilanz berechnet?",
        "Erkläre die Unterscheidung zwischen Anlage- und Umlaufvermögen.",
        "Was bedeutet die Bilanzsumme?",
        "Beschreibe den Prozess einer Inventur und dessen Bedeutung für die Bilanz.",
        "Was bedeutet Aktivierung und was wird typischerweise aktiviert?",
        "Wie wird das Eigenkapital durch Jahresergebnisse beeinflusst?",
        "Erkläre den Begriff 'Gewinnermittlung durch Bilanzvergleich'.",
        "Was ist negatives Eigenkapital und welche Implikationen hat es?",

        # Kapitel 2: Die Gewinn- und Verlustrechnung (GuV-Rechnung)
        "Was ist der Hauptzweck einer GuV-Rechnung?",
        "Unterscheide zwischen Erträgen und Aufwendungen.",
        "Wie berechnet man das Jahresergebnis aus der GuV-Rechnung?",
        "Erkläre den Unterschied zwischen Umsatz und Gewinn.",
        "Was ist der Zusammenhang zwischen der GuV-Rechnung und der Bilanz?",
        "Welche Arten von Aufwendungen werden in der GuV-Rechnung berücksichtigt?",
        "Erkläre, warum die GuV-Rechnung wichtig für die Beurteilung der finanziellen Gesundheit eines Unternehmens ist.",
        "Welche Informationen liefert eine detaillierte Analyse der GuV-Rechnung?",
        "Wie beeinflussen Abschreibungen die GuV-Rechnung?",
        "Diskutiere die Rolle der GuV-Rechnung im Kontext der unternehmerischen Entscheidungsfindung.",

        # Kapitel 3: Kostenrechnung
        "Was versteht man unter Kostenrechnung und warum ist sie wichtig?",
        "Unterscheide zwischen Kostenarten, Kostenstellen und Kostenträgern.",
        "Erkläre das Konzept der Abschreibung und ihre Bedeutung in der Kostenrechnung.",
        "Was sind direkte und indirekte Kosten?",
        "Wie beeinflusst die Kostenstruktur Preisentscheidungen?",
        "Beschreibe den Unterschied zwischen variablen und fixen Kosten.",
        "Was versteht man unter einem Deckungsbeitrag?",
        "Wie wird der Break-Even-Point berechnet?",
        "Diskutiere die Bedeutung der kurzfristigen Preisuntergrenze.",
        "Wie können Kostenrechnungsmethoden zur Leistungsverbesserung beitragen?",

        # Weitere Kapitel
        # Kapitel 4: Investitionsrechnung
        "Was ist der Break-Even-Point und wie wird er berechnet?",
        "Erkläre die Berechnung des Return on Investment (ROI).",
        "Was sind Opportunitätskosten und wie beeinflussen sie Investitionsentscheidungen?",
        "Was ist der Unterschied zwischen statischer und dynamischer Investitionsrechnung?",
        "Diskutiere die Rolle von der Amortisationsdauer in Investitionsentscheidungen.",

        # Kapitel 5: Wirtschaftsrecht
        "Was sind die Grundprinzipien des Gesellschaftsrechts?",
        "Was versteht man unter Vertretungsbefugnis in einem Unternehmen?",
        "Erkläre den Unterschied zwischen Personengesellschaften und Kapitalgesellschaften.",
        "Was ist ein Konzern und welche rechtlichen Besonderheiten gelten dafür?",
        "Welche rechtlichen Folgen hat der Verzug bei Zahlungen im Geschäftsverkehr?"
    ]
    # Auswahl einer zufälligen Frage
    return random.choice(questions)



def generate_exam_questions(client, assistant_id, document_id):
    prompt = "Bitte generiere eine Prüfungsfrage basierend auf den folgenden Informationen:"
    instructions = "Generiere eine Prüfungsfrage auf basis des beigefügen Lehrbuchs, Die Frage sollte nicht allzu lang und soll eindeutig beantwortet werden können"

    response = client.beta.threads.create(
        assistant_id=assistant_id,
        messages=[
            {
                "role": "system",
                "content": {"document_id": document_id}  # Stelle sicher, dass das Dokument verfügbar ist
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        tools=[{"type": "retrieval"}],
        instructions=instructions
    )
    return response.messages[-1].content

def select_document(lesson_choice):
    # Mapping user choices to document file names
    document_map = {
        "Bilanzierung": "data/1_bilanzierung.docx",
        "Unternehmensziele/Kennzahlen": "data/2_UnternehmenszieleKennzahlen.docx",
        "Kostenrechnung": "data/3_Kostenrechnung.docx",
        "Investitionsrechnung": "data/4_Investitionsrechnung.docx",
        "Wirtschaftsrecht": "data/5_Wirtschaftsrecht.docx",
        "Finanzwesen": "data/6_Finanzwesen.docx"
    }
    return document_map.get(lesson_choice)  # Default to a general info document if no match

def get_exam_question2(tax):
    questions = {
        1: [
            # Bilanzierung
            "Listen Sie die Hauptbestandteile einer Bilanz auf.",
            "Beschreiben Sie den Unterschied zwischen Anlagevermögen und Umlaufvermögen.",
            # Unternehmensziele und Kennzahlen
            "Listen Sie die drei Hauptziele eines Unternehmens auf.",
            "Definieren Sie den Begriff 'Kennzahl'.",
            # Kostenrechnung
            "Definieren Sie den Begriff 'Kosten'.",
            "Listen Sie die Hauptkostenarten eines Unternehmens auf.",
            # Investitionsrechnung
            "Definieren Sie den Begriff 'Investition'.",
            "Listen Sie die Hauptarten von Investitionen auf.",
            # Wirtschaftsrecht
            "Definieren Sie den Begriff 'Vertrag'.",
            "Listen Sie die Hauptbestandteile eines Vertrags auf.",
            # Finanzwesen
            "Definieren Sie den Begriff 'Finanzierung'.",
            "Listen Sie die verschiedenen Finanzierungsarten eines Unternehmens auf."
        ],
        2: [
            # Bilanzierung
            "Erklären Sie mit eigenen Worten, warum die Bilanzsumme auf der Aktivseite und Passivseite immer gleich sein muss.",
            "Verdeutlichen Sie den Unterschied zwischen Eigenkapital und Fremdkapital anhand eines Beispiels.",
            # Unternehmensziele und Kennzahlen
            "Erklären Sie, warum die Rentabilität für ein Unternehmen wichtig ist.",
            "Verdeutlichen Sie den Unterschied zwischen Eigenkapitalrentabilität und Gesamtkapitalrentabilität anhand eines Beispiels.",
            # Kostenrechnung
            "Erklären Sie den Unterschied zwischen Fixkosten und variablen Kosten.",
            "Verdeutlichen Sie anhand eines Beispiels, wie die Gesamtkosten eines Unternehmens berechnet werden.",
            # Investitionsrechnung
            "Erklären Sie den Unterschied zwischen Sachinvestitionen und Finanzinvestitionen.",
            "Verdeutlichen Sie anhand eines Beispiels, wie der Nettobarwert (Net Present Value) einer Investition berechnet wird.",
            # Wirtschaftsrecht
            "Erklären Sie den Unterschied zwischen einem Kaufvertrag und einem Werkvertrag.",
            "Verdeutlichen Sie anhand eines Beispiels, was unter 'Vertragsfreiheit' zu verstehen ist.",
            # Finanzwesen
            "Erklären Sie den Unterschied zwischen Eigenfinanzierung und Fremdfinanzierung.",
            "Verdeutlichen Sie anhand eines Beispiels, wie ein Unternehmen seine Liquidität verbessern kann."
        ],
        3: [
            # Bilanzierung
            "Berechnen Sie das Eigenkapital eines Unternehmens, wenn das Gesamtvermögen 500.000 Euro und die Schulden 300.000 Euro betragen.",
            "Stellen Sie eine einfache Bilanz mit fiktiven Zahlen auf, die sowohl Anlage- als auch Umlaufvermögen sowie Eigen- und Fremdkapital enthält.",
            # Unternehmensziele und Kennzahlen
            "Berechnen Sie die Eigenkapitalquote eines Unternehmens, wenn das Eigenkapital 300.000 Euro und das Gesamtkapital 1.000.000 Euro beträgt.",
            "Ermitteln Sie die Liquidität 1. Grades (Cash Ratio) eines Unternehmens, wenn die liquiden Mittel 50.000 Euro und die kurzfristigen Verbindlichkeiten 200.000 Euro betragen.",
            # Kostenrechnung
            "Berechnen Sie die Gesamtkosten eines Unternehmens, wenn die Fixkosten 100.000 Euro und die variablen Kosten pro Einheit 50 Euro betragen und 2.000 Einheiten produziert werden.",
            "Ermitteln Sie den Break-even-Punkt eines Unternehmens, wenn die Fixkosten 200.000 Euro, die variablen Kosten pro Einheit 40 Euro und der Verkaufspreis pro Einheit 80 Euro betragen.",
            # Investitionsrechnung
            "Berechnen Sie den Nettobarwert einer Investition, wenn die Anfangsauszahlung 100.000 Euro beträgt, die jährlichen Rückflüsse 25.000 Euro und der Kalkulationszinssatz 5% sind, und die Nutzungsdauer 5 Jahre beträgt.",
            "Ermitteln Sie den internen Zinsfuß (Internal Rate of Return) einer Investition, wenn die Anfangsauszahlung 150.000 Euro beträgt und die jährlichen Rückflüsse 30.000 Euro über 6 Jahre betragen.",
            # Wirtschaftsrecht
            "Berechnen Sie den Schadensersatz, wenn ein Lieferant seine vertragliche Verpflichtung nicht erfüllt und dem Käufer dadurch ein Schaden von 10.000 Euro entsteht.",
            "Ermitteln Sie die Rechtsfolgen, wenn ein Vertrag aufgrund eines Irrtums angefochten wird.",
            # Finanzwesen
            "Berechnen Sie den Verschuldungsgrad eines Unternehmens, wenn das Fremdkapital 500.000 Euro und das Eigenkapital 250.000 Euro beträgt.",
            "Ermitteln Sie den Cashflow eines Unternehmens, wenn der Jahresüberschuss 100.000 Euro beträgt, Abschreibungen 20.000 Euro und die Veränderung des Working Capitals 10.000 Euro beträgt."
        ],
        4: [
            # Bilanzierung
            "Analysieren Sie die Bilanz eines Unternehmens und identifizieren Sie mögliche Gründe für eine hohe Verschuldung.",
            """
            | **Aktiva**                             | **Betrag (Euro)** | **Passiva**                       | **Betrag (Euro)** |
            |----------------------------------------|-------------------|-----------------------------------|-------------------|
            | **Anlagevermögen**                     | 200.000           | **Eigenkapital**                  | 100.000           |
            | **Umlaufvermögen**                     |                   | **Fremdkapital**                  |                   |
            | - Vorräte                              | 50.000            | - Langfristige Verbindlichkeiten  | 120.000           |
            | - Forderungen aus Lieferungen und Leistungen | 30.000     | - Kurzfristige Verbindlichkeiten  | 80.000            |
            | - Kassenbestand                        | 20.000            |                                   |                   |
            | **Summe Aktiva**                       | **300.000**       | **Summe Passiva**                 | **300.000**       |
            """,
            "Vergleichen Sie die Struktur der Aktiva und Passiva zweier Unternehmen und diskutieren Sie die finanziellen Risiken, die sich aus unterschiedlichen Verschuldungsgraden ergeben.",
            """
            | **Unternehmen A**                      |                   | **Unternehmen B**                 |                   |
            | **Aktiva**                             | **Betrag (Euro)** | **Aktiva**                        | **Betrag (Euro)** |
            |----------------------------------------|-------------------|-----------------------------------|-------------------|
            | **Anlagevermögen**                     | 300.000           | **Anlagevermögen**                | 250.000           |
            | **Umlaufvermögen**                     |                   | **Umlaufvermögen**                |                   |
            | - Vorräte                              | 100.000           | - Vorräte                         | 50.000            |
            | - Forderungen aus Lieferungen und Leistungen | 80.000     | - Forderungen aus Lieferungen und Leistungen | 60.000     |
            | - Kassenbestand                        | 20.000            | - Kassenbestand                   | 40.000            |
            | **Summe Aktiva**                       | **500.000**       | **Summe Aktiva**                  | **400.000**       |
            | **Passiva**                            | **Betrag (Euro)** | **Passiva**                       | **Betrag (Euro)** |
            |----------------------------------------|-------------------|-----------------------------------|-------------------|
            | **Eigenkapital**                       | 150.000           | **Eigenkapital**                  | 200.000           |
            | **Fremdkapital**                       |                   | **Fremdkapital**                  |                   |
            | - Langfristige Verbindlichkeiten       | 200.000           | - Langfristige Verbindlichkeiten  | 100.000           |
            | - Kurzfristige Verbindlichkeiten       | 150.000           | - Kurzfristige Verbindlichkeiten  | 100.000           |
            | **Summe Passiva**                      | **500.000**       | **Summe Passiva**                 | **400.000**       |
            """,
            # Unternehmensziele und Kennzahlen
            "Analysieren Sie die folgende Kennzahlentabelle eines Unternehmens und identifizieren Sie potenzielle finanzielle Schwächen.",
            """
            | **Kennzahl**               | **Wert**      |
            |----------------------------|---------------|
            | Eigenkapitalquote          | 15%           |
            | Gesamtkapitalrentabilität  | 5%            |
            | Liquidität 1. Grades       | 10%           |
            | Umsatzrentabilität         | 3%            |
            """,
            "Vergleichen Sie die Eigenkapitalquote und die Gesamtkapitalrentabilität zweier Unternehmen und diskutieren Sie, welches Unternehmen besser aufgestellt ist.",
            """
            | **Kennzahl**               | **Unternehmen A** | **Unternehmen B** |
            |----------------------------|-------------------|-------------------|
            | Eigenkapitalquote          | 40%               | 25%               |
            | Gesamtkapitalrentabilität  | 8%                | 10%               |
            """,
            # Kostenrechnung
            "Analysieren Sie die Kostenstruktur eines Unternehmens und identifizieren Sie potenzielle Einsparpotenziale.",
            "Vergleichen Sie die Auswirkungen von Fixkosten und variablen Kosten auf die Profitabilität eines Unternehmens bei unterschiedlichen Produktionsmengen.",
            # Investitionsrechnung
            "Analysieren Sie die Wirtschaftlichkeit einer Investition anhand des Nettobarwerts und des internen Zinsfußes.",
            "Vergleichen Sie die Vorteile und Nachteile der Amortisationsmethode und der Kapitalwertmethode bei der Bewertung von Investitionen.",
            # Wirtschaftsrecht
            "Analysieren Sie die rechtlichen Konsequenzen einer Vertragsverletzung im Handelsrecht.",
            "Vergleichen Sie die Unterschiede zwischen nationalem und internationalem Vertragsrecht.",
            # Finanzwesen
            "Analysieren Sie die Liquiditätslage eines Unternehmens anhand folgender Zahlen: Liquide Mittel: 80.000 Euro, kurzfristige Verbindlichkeiten: 120.000 Euro, kurzfristige Forderungen: 60.000 Euro.",
            "Vergleichen Sie die Eigenkapitalrentabilität zweier Unternehmen anhand folgender Daten: Unternehmen A: Eigenkapital: 500.000 Euro, Gewinn: 50.000 Euro; Unternehmen B: Eigenkapital: 300.000 Euro, Gewinn: 45.000 Euro."
        ],
        5: [
            # Bilanzierung
            "Entwerfen Sie ein Konzept zur Verbesserung der Eigenkapitalquote eines Unternehmens, das derzeit stark verschuldet ist.",
            "Entwickeln Sie einen Plan zur Restrukturierung der Bilanz eines Unternehmens, um die finanzielle Stabilität zu erhöhen.",
            # Unternehmensziele und Kennzahlen
            "Entwickeln Sie ein Konzept zur Verbesserung der Umsatzrentabilität eines Unternehmens, das derzeit eine Umsatzrentabilität von 2% aufweist.",
            "Entwerfen Sie ein umfassendes Kennzahlensystem für ein mittelständisches Unternehmen, das sowohl finanzielle als auch nicht-finanzielle Kennzahlen beinhaltet.",
            # Kostenrechnung
            "Entwickeln Sie ein Kostenmanagementsystem zur Kontrolle und Reduktion der variablen Kosten in einem Produktionsunternehmen.",
            "Entwerfen Sie ein Konzept zur Optimierung der Fixkostenstruktur eines Dienstleistungsunternehmens.",
            # Investitionsrechnung
            "Entwickeln Sie ein Investitionsbewertungsmodell, das sowohl quantitative als auch qualitative Faktoren berücksichtigt.",
            "Entwerfen Sie eine Strategie zur Priorisierung von Investitionsprojekten in einem Unternehmen.",
            # Wirtschaftsrecht
            "Entwickeln Sie einen Vertragsentwurf für einen internationalen Handelsvertrag unter Berücksichtigung der INCOTERMS.",
            "Entwerfen Sie ein Konzept zur Minimierung von Rechtsrisiken in internationalen Geschäftsbeziehungen.",
            # Finanzwesen
            "Entwickeln Sie ein Finanzplanungsmodell, das die Kapitalstruktur eines Unternehmens optimiert.",
            "Entwerfen Sie eine Strategie zur Verbesserung der Kreditwürdigkeit eines Unternehmens."
        ],
        6: [
            # Bilanzierung
            "Beurteilen Sie die Bilanz eines Unternehmens und geben Sie Empfehlungen zur Verbesserung der finanziellen Gesundheit.",
            """
            | **Aktiva**                             | **Betrag (Euro)** | **Passiva**                       | **Betrag (Euro)** |
            |----------------------------------------|-------------------|-----------------------------------|-------------------|
            | **Anlagevermögen**                     | 200.000           | **Eigenkapital**                  | 100.000           |
            | **Umlaufvermögen**                     |                   | **Fremdkapital**                  |                   |
            | - Vorräte                              | 50.000            | - Langfristige Verbindlichkeiten  | 120.000           |
            | - Forderungen aus Lieferungen u. L     | 30.000            | - Kurzfristige Verbindlichkeiten  | 80.000            |
            | - Kassenbestand                        | 20.000            |                                   |                   |
            | **Summe Aktiva**                       | **300.000**       | **Summe Passiva**                 | **300.000**       |
            """,
            "Vergleichen Sie die Bilanzen zweier Unternehmen und bewerten Sie, welches Unternehmen besser aufgestellt ist, um wirtschaftliche Herausforderungen zu bewältigen.",
            """
            | **Unternehmen A**                      |                   | **Unternehmen B**                 |                   |
            | **Aktiva**                             | **Betrag (Euro)** | **Aktiva**                        | **Betrag (Euro)** |
            |----------------------------------------|-------------------|-----------------------------------|-------------------|
            | **Anlagevermögen**                     | 300.000           | **Anlagevermögen**                | 250.000           |
            | **Umlaufvermögen**                     |                   | **Umlaufvermögen**                |                   |
            | - Vorräte                              | 100.000           | - Vorräte                         | 50.000            |
            | - Forderungen aus Lieferungen und L.   | 80.000            | - Forderungen aus Lieferungen u.L | 60.000            |
            | - Kassenbestand                        | 20.000            | - Kassenbestand                   | 40.000            |
            | **Summe Aktiva**                       | **500.000**       | **Summe Aktiva**                  | **400.000**       |
            | **Passiva**                            | **Betrag (Euro)** | **Passiva**                       | **Betrag (Euro)** |
            |----------------------------------------|-------------------|-----------------------------------|-------------------|
            | **Eigenkapital**                       | 150.000           | **Eigenkapital**                  | 200.000           |
            | **Fremdkapital**                       |                   | **Fremdkapital**                  |                   |
            | - Langfristige Verbindlichkeiten       | 200.000           | - Langfristige Verbindlichkeiten  | 100.000           |
            | - Kurzfristige Verbindlichkeiten       | 150.000           | - Kurzfristige Verbindlichkeiten  | 100.000           |
            | **Summe Passiva**                      | **500.000**       | **Summe Passiva**                 | **400.000**       |
            """,
            # Unternehmensziele und Kennzahlen
            "Beurteilen Sie die finanzielle Gesundheit eines Unternehmens anhand der folgenden Kennzahlen und geben Sie Empfehlungen zur Verbesserung.",
            """
            | **Kennzahl**               | **Wert**      |
            |----------------------------|---------------|
            | Eigenkapitalquote          | 20%           |
            | Gesamtkapitalrentabilität  | 4%            |
            | Liquidität 2. Grades       | 80%           |
            | Umsatzrentabilität         | 5%            |
            """,
            "Vergleichen und bewerten Sie die Kennzahlen der zwei Unternehmen und entscheiden Sie, welches für eine langfristige Investition besser geeignet ist.",
            """
            | **Kennzahl**               | **Unternehmen A** | **Unternehmen B** |
            |----------------------------|-------------------|-------------------|
            | Eigenkapitalquote          | 35%               | 30%               |
            | Gesamtkapitalrentabilität  | 9%                | 7%                |
            | Liquidität 2. Grades       | 100%              | 120%              |
            | Umsatzrentabilität         | 8%                | 6%                |
            """,
            # Kostenrechnung
            "Beurteilen Sie die Effizienz der Kostenstruktur eines Unternehmens und geben Sie Empfehlungen zur Verbesserung.",
            "Vergleichen Sie zwei Kostenmanagementsysteme und bewerten Sie, welches für ein mittelständisches Produktionsunternehmen geeigneter ist.",
            # Investitionsrechnung
            "Beurteilen Sie die Effektivität eines Investitionsprojekts anhand einer umfassenden Investitionsrechnung.",
            "Vergleichen Sie zwei unterschiedliche Investitionsprojekte und bewerten Sie, welches unter Berücksichtigung von Risiko und Rendite bevorzugt werden sollte.",
            # Wirtschaftsrecht
            "Beurteilen Sie die Rechtswirksamkeit eines Vertrags und geben Sie Empfehlungen zur Vertragsgestaltung.",
            "Vergleichen Sie zwei unterschiedliche Vertragsmodelle und bewerten Sie, welches für ein multinationales Unternehmen geeigneter ist.",
            # Finanzwesen
            "Beurteilen Sie die Kapitalstruktur eines Unternehmens und geben Sie Empfehlungen zur Optimierung.",
            "Vergleichen Sie die Auswirkungen von Eigenkapital- und Fremdkapitalfinanzierung auf die finanzielle Stabilität eines Unternehmens."
        ]
    }

    if tax in questions:
        import random
        return random.choice(questions[tax])
    else:
        return "Ungültiger Wert. Bitte einen Wert zwischen 1 und 6 eingeben."


#ask_question(count,tax)
def ask_question(count):
    #question = get_exam_question2(tax)  # Verwende den tax-Wert, um Fragen auszuwählen
    question = get_exam_question()
    formatted_question = f"{count}/5: {question}"
    return formatted_question

def evaluate_performance():
    total_score = session.get('score', 0)
    tax = session.get('tax', 2)  # Aktueller tax-Wert

    if total_score >= 4:
        tax += 1  # Sehr gut bestanden, erhöhe tax
    elif total_score < 2.5:
        tax = max(1, tax - 1)  # Nicht bestanden, reduziere tax, aber nicht unter 1

    session['tax'] = tax  # Speichere den neuen tax-Wert in der Session

    result_text = evaluate_performance_text(total_score)
    session.clear()
    return jsonify({"result": result_text, "new_tax": tax}), 200

def evaluate_performance_text(score):
    if score < 2.5:
        return "Nicht bestanden :("
    elif 2.5 <= score < 4:
        return "Bestanden!"
    elif score >= 4:
        return "Sehr gut Bestanden! :D"


def create_assistant(client):
    assistant_file_path = 'assistant.json'

    # Define the paths to your multiple document files (both DOCX and PDF)
    document_files = [
        'data/aufgaben.pdf',
        'data/Lernziele.docx',
        'data/1_bilanzierung.docx',
        'data/2_UnternehmenszieleKennzahlen.docx',
        'data/3_Kostenrechnung.docx',
        'data/4_Investitionsrechnung.docx',
        'data/5_Wirtschaftsrecht.docx',
        'data/6_Finanzwesen.docx',
        'data/document.pdf'

    ]

    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, 'r') as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data['assistant_id']
            print("Loaded existing assistant ID.")
    else:
        # Upload each document file and store the file IDs
        file_ids = []
        for document_file in document_files:
            # Print the current working directory
            logging.info("Current working directory: {}".format(os.getcwd()))
            print("Current working directory:", os.getcwd())

            # Full path to the file
            full_path = os.path.join(os.getcwd(), document_file)
            print("Full path to the file:", full_path)

            try:
                with open(document_file, "rb") as file_content:
                    file = client.files.create(file=file_content, purpose='assistants')
                    file_ids.append(file.id)
            except FileNotFoundError:
                print(f"File not found: {document_file}")
            except Exception as e:
                print(f"An error occurred: {e}")

        # Create the assistant with multiple file IDs
        assistant = client.beta.assistants.create(
            instructions="""
            Your role is to assist students in understanding business studies concepts by guiding their inquiry without directly providing answers. Encourage students to think critically by posing questions that stimulate deeper thought and understanding. Offer hints and suggest resources for further research, fostering independence and self-directed learning. Reinforce the importance of applying concepts to practical examples, helping students make connections between theory and real-world application. Lastly, ensure your guidance upholds academic integrity and inspires confidence in students ability to solve problems on their own. You now have multiple Knowledge documents with all the course materials content you can use as references.
            """,
            model="gpt-3.5-turbo-0125",
            tools=[{"type": "retrieval"},
                   {
                       "type": "function",
                       "function": {
                           "name": "select_document",
                           "description": "Selects the appropriate document based on user input for lesson choice.",
                           "parameters": {
                               "type": "object",
                               "properties": {
                                   "lesson_choice": {
                                       "type": "string",
                                       "description": "The user's lesson choice to determine the relevant document."
                                   }
                               },
                               "required": ["lesson_choice"]
                           }
                       }
                   }
                   ],
            file_ids=file_ids
        )

        with open(assistant_file_path, 'w') as file:
            json.dump({'assistant_id': assistant.id}, file)
            print("Created a new assistant with multiple documents and saved the ID.")

        assistant_id = assistant.id

    return assistant_id
