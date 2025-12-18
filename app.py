from app import create_app

app = create_app()


from app.routes.buildings import buildings_bp
app.register_blueprint(buildings_bp)


if __name__ == "__main__":
    app.run(debug=True)
