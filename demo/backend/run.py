from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # 初始化数据
        from app.init_data import init_data
        init_data()
    app.run(debug=True, port=5000)
