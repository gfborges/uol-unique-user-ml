from app import create_app

app = create_app()

def main():
    app.run("127.0.0.1", "5000")


if __name__ == "__main__":
    main()