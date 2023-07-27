from project import app


if __name__ == "__main__":
    port = 5001
    print(f"Running Simulator port:{port} \n")
    app.run(host="0.0.0.0", port=port, debug=True)
