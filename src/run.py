print("1️⃣ before importing app")
from app import app
print("2️⃣ after importing app")

if __name__ == "__main__":
    print("3️⃣ before app.run")
    app.run(host="localhost", port=8010, debug=False)
