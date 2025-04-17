from flask import Flask, render_template, request, session, redirect, url_for, send_file
from io import BytesIO
from dotenv import load_dotenv
import os

from llm import create_llm

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # נדרש כדי להשתמש ב-session


@app.route("/", methods=["GET", "POST"])
def chat():
    if "messages" not in session:
        session["messages"] = [
            {"role": "system", "content": "אתה עוזר מיוחד שמנתח רעיונות של משתמשים לבניית אתרים. שאל שאלות כדי להבין את כל הפרטים הדרושים."},
            {"role": "assistant", "content": "היי! אני כאן כדי לעזור לך לתכנן את האתר שלך. תוכל לספר לי מה הרעיון שלך?"}
        ]
    if "site_summary" not in session:
        session["site_summary"] = "עדיין אין מספיק מידע על האתר."

    if request.method == "POST":
        user_input = request.form["user_input"]
        session["messages"].append({"role": "user", "content": user_input})

        response = llm.chat(session["messages"])

        ai_message = response
        session["messages"].append({"role": "assistant", "content": ai_message})

        # יצירת סיכום מעודכן על האתר
        summary_prompt = session["messages"] + [
            {
                "role": "user",
                "content": (
                    "בהתבסס על כל מה שנאמר עד עכשיו, נסח פרומפט מקצועי ותמציתי שמתאר את האתר שהמשתמש רוצה לבנות. "
                    "הפרומפט צריך להיות מנוסח כך שניתן יהיה להעביר אותו ישירות למערכת או למודל לבניית האתר בפועל. "
                    "כלול בתוכו את הדרישות שכבר נאספו: סוג האתר, עמודים נדרשים, פיצ'רים, מטרות, וטכנולוגיות (אם נמסרו). "
                    "לאחר מכן, הוסף גם סעיף קצר שמפרט אילו פרטי מידע חסרים או לא הוגדרו עד כה ושיהיה צורך להשלים אותם. "
                    "נא לנסח את התוצאה בצורה נקייה, ישירה, וללא הקדמות או שפה מדוברת – רק תוכן מדויק."
                )
            }
        ]

        summary_response = llm.chat(summary_prompt)

        session["site_summary"] = summary_response

    return render_template("chat.html", messages=session["messages"], summary=session["site_summary"])

@app.route("/reset")
def reset():
    session.pop("messages", None)
    session.pop("site_summary", None)
    return redirect(url_for("chat"))

@app.route("/download_prompt")
def download_prompt():
    prompt_text = session.get("site_summary", "אין מידע לשמור.")
    buffer = BytesIO()
    buffer.write(prompt_text.encode("utf-8"))
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="prompt.txt",
        mimetype="text/plain"
    )

if __name__ == "__main__":

    # Initialize the LLM with the Groq API key and model
    llm = create_llm("groq", api_key=os.getenv("GROQ_API_KEY"), model="llama3-70b-8192")

    app.run(debug=True)
