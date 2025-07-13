## 📝 Problem Statement

This project was built as part of the **Odoo Hackathon 2025**.

We chose the problem statement:

> **"Skill Swap Platform"** – Create a platform that enables users to exchange skills by matching what they offer with what they want to learn.

The goal was to promote collaborative learning, reduce entry barriers for skill acquisition, and build a peer-powered ecosystem of growth.

---



# Skillink 🎯

Match. Swap. Learn. Grow. Skillink helps you connect with people offering the skills you want, and wanting the skills you offer.

Skillink is a lightweight skill-swapping platform where users can register, offer their skills, request others', and grow together. 



## 📸 Screenshots
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/9802d0b6-339f-4816-b560-56caf95d2342" />


---

## Presentation Video

 <a href="https://drive.google.com/file/d/1ijC2zQXR8mbMJh8KAPAUfou9JSH1ml4q/view?usp=drive_link" target="_blank">
  <img width="800" alt="Demo Video" src="https://github.com/user-attachments/assets/ee1d0850-a3e2-4cab-acae-7fba1b3372f0" />
</a>

<p align="center"><b>🎬 Click the image above to watch the video</b></p>


---

## 🧠 Features

- 🔐 User Registration & Login
- ✍️ Create and edit skill profile
- 🔎 Search public profiles by offered/wanted skills
- 🔁 Request skill swaps
- 📩 Accept / reject / cancel swap requests
- ☁️ Fully styled using Tailwind CSS

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, Flask, SQLAlchemy |
| Frontend | HTML (rendered via Flask), Tailwind CSS |
| Database | SQLite (for demo), supports PostgreSQL |
| Deployment | Render / Replit / PythonAnywhere |
| Server | Gunicorn (for production) |

---

## 🚀 Getting Started Locally

1. **Clone the repo**
   ```bash
   git clone https://github.com/AayushSomvanshi/skillink.git
   cd skillink
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   python app.py
   ```

4. Visit: `http://127.0.0.1:5000`

---

## 📂 File Structure

```
skillink/
│
├── app.py               # Main Flask app
├── skillink.db          # SQLite database
├── requirements.txt     # Python dependencies
├── Procfile             # For deployment (Gunicorn)
├── runtime.txt          # Python version hint (Render)
└── README.md            # This file
```

---

## 💡 Future Improvements

- ✅ Add user feedback/rating system
- ✅ Add skill tags / categories
- ✅ Add messaging system
- ✅ Switch to PostgreSQL for production

---

## 👥 Authors

- [Aayush Somvanshi 😎](https://github.com/AayushSomvanshi)
- [Anshuman Verma 💪](https://github.com/AVPy234)


---

## 📃 License

This project is licensed under the [MIT License](LICENSE).
