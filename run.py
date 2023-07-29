from envaiot import app

if __name__ == "__main__":
    port = 5000
    print(f"Running EnvAIoT port:{port} \n")
    app.run(port=port, debug=True)
