from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['students']


@app.route('/')
def index():
    students = db.students.find()
    return render_template('index.html', students=students)


@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        reg_no = request.form['reg_no']
        name = request.form['name']
        year = request.form['year']
        department = request.form['department']
        section = request.form['section']
        phone = request.form['phone']
        db.students.insert_one({
            'reg_no': reg_no,
            'name': name,
            'year': year,
            'department': department,
            'section': section,
            'phone': phone
        })
        return redirect(url_for('index'))
    return render_template('add_student.html')


@app.route('/edit-student/<string:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = db.students.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        db.students.update_one(
            {'_id': ObjectId(id)},
            {
                '$set': {
                    'reg_no': request.form['reg_no'],
                    'name': request.form['name'],
                    'year': request.form['year'],
                    'department': request.form['department'],
                    'section': request.form['section'],
                    'phone': request.form['phone']
                }
            }
        )
        return redirect(url_for('index'))
    return render_template('edit_student.html', student=student)


@app.route('/delete-student/<string:id>', methods=['POST'])
def delete_student(id):
    db.students.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
