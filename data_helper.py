from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_wtf import Form

from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import InputRequired, Email, Length

from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'

# app.config['MONGO_URI'] = 'mongodb://localhost:27017/MathJoy'
app.config['MONGO_URI'] = 'mongodb://192.168.11.216:27017/MathJoy'  # Liuda
# app.config['MONGO_URI'] = 'mongodb://192.168.11.119:27017/MathJoy'   # qas

app.config['MONGO_DBNAME'] = 'MathJoy'

mongo = PyMongo(app)

Bootstrap(app)

# (value, label)
PROGRAM_CHOICES = [('2', 'ISEE Lower'),
                   ('3', 'ISEE Medium'),
                   ('4', 'ISEE Upper'),
                   ('5', 'SSAT Medium'),
                   ('6', 'SSAT Upper')]

SECTION_CHOICES = [('isee.vr', 'isee.vr'),
                   ('isee.qs', 'isee.qs'),
                   ('isee.rc', 'isee.rc')]

PRODUCT_LEVEL_CHOICES = [('1', 'Basic'), ('2', 'Medium'), ('3', 'Advanced'), ('4', 'Test Practice')]

SKILL_TYPE_CHOICES = [('Word Application', 'Word Application'),
                      ('WordDefinitionPractice', 'Word Definition Practice'),
                      ('WordDefinitionList', 'Word Definition List')]

CHAPTER_CHOICES = []

for i in range(1, 10):
    CHAPTER_CHOICES.append(("Chapter" + str(i), "chapter " + str(i)))


class Skills_Level_Form(Form):
    user_name = StringField('User Name:', validators=[InputRequired()])
    program_id = SelectField('Program:', choices=PROGRAM_CHOICES)
    section_type = SelectField('Section Type:', choices=SECTION_CHOICES)
    level = SelectField('Level:', choices=PRODUCT_LEVEL_CHOICES)
    skill_type = SelectField('Skill Type:', choices=SKILL_TYPE_CHOICES)
    chapter_name = SelectField('Chapter:', choices=CHAPTER_CHOICES)
    submit = SubmitField('Seach')


@app.route('/')
def index():
    return render_template('index.html', title="Index")


@app.route('/skills_level', methods=['GET', 'POST'])
def skill_levels():
    from api.testprep_service import query_user_skills_level, get_user_id
    form = Skills_Level_Form()

    if form.validate_on_submit():
        user_id = get_user_id(form.user_name.data)
        if user_id:
            data = query_user_skills_level(user_id=user_id,
                                           program_id=form.program_id.data,
                                           section_type=form.section_type.data,
                                           level=form.level.data,
                                           skill_type=form.skill_type.data,
                                           chapter_name=form.chapter_name.data)

            return render_template('skills_level.html', form=form, title="Skill Levels", skill_levels=data)
        flash("Can not find user.")

    return render_template('skills_level.html', form=form, title="Skill Levels")


if __name__ == '__main__':
    app.run(debug=True, port=9527)
