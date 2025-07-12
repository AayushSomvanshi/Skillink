# Skillink 🎯

Skillink is a lightweight skill-swapping platform where users can register, offer their skills, request others', and grow together — all powered by Flask.



## 📸 Screenshots
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/9802d0b6-339f-4816-b560-56caf95d2342" />




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
   git clone https://github.com/YOUR_USERNAME/skillink.git
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

- [Aayush Somvanshi](https://github.com/AayushSomvanshi)
- [Anshuman Verma]


---

## 📃 License

This project is licensed under the [MIT License](LICENSE).
