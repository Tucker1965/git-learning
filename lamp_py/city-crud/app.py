
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
# データベース接続設定 (環境に合わせて変更してください)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mstuser:p%40ssw0rd@ol8.lamp.com/mstdb'
db = SQLAlchemy(app)

print("---- app.py run ---")

class ScrapedCity(db.Model):
    __tablename__ = 'scraped_cities'
    citycd = db.Column(db.String(6), primary_key=True)
    name = db.Column(db.String(30))
    kana = db.Column(db.String(30))
    postno = db.Column(db.String(8))
    address = db.Column(db.String(100))
    telno = db.Column(db.String(20))
    impdate = db.Column(db.DateTime, primary_key=True, default=lambda: datetime.now(timezone.utc))

@app.route('/')
def index():
    cities = ScrapedCity.query.all()
    return render_template('index.html', cities=cities)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_city = ScrapedCity(
            citycd=request.form['citycd'],
            name=request.form['name'],
            kana=request.form['kana'],
            postno=request.form['postno'],
            address=request.form['address'],
            telno=request.form['telno'],
            impdate=datetime.now()
        )
        db.session.add(new_city)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', city=None)

@app.route('/edit/<citycd>', methods=['GET', 'POST'])
def edit(citycd):
    city = ScrapedCity.query.filter_by(citycd=citycd).first_or_404()
    if request.method == 'POST':
        city.name = request.form['name']
        city.kana = request.form['kana']
        city.postno = request.form['postno']
        city.address = request.form['address']
        city.telno = request.form['telno']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', city=city)

@app.route('/delete/<citycd>')
def delete(citycd):
    city = ScrapedCity.query.filter_by(citycd=citycd).first_or_404()
    db.session.delete(city)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
